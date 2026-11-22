# Migrating a Booking Identity Across Two Application Versions

The reservations API and its worker deploy independently. Both v1 callers
use `actor_id`. Version 2 calls the same identity `booked_by_id`. A direct
rename would break a v1 worker the next time it claims a slot. The rollout
below keeps both versions able to book through the application rollback window.

## Rollout contract

| Phase | v1 reads / writes | v2 reads / writes | Evidence to advance |
| --- | --- | --- | --- |
| Original | `actor_id` / `actor_id` | Offline | Capture existing claims and identify callers. |
| Expand and mix | `actor_id` / `actor_id` | View with fallback / `booked_by_id` | Each version reads a claim made by the other. |
| Backfill | `actor_id` / `actor_id` | View with fallback / `booked_by_id` | All historical rows have matching, populated identities. |
| Cut over reads | `actor_id` / `actor_id` | View of `booked_by_id` / `booked_by_id` | Drain v1 and finish the rollback window. |
| Contract | Retired | View of `booked_by_id` / `booked_by_id` | A fresh v2 write and historical reads succeed. |

During coexistence the view reads `booked_by_id`, falling back to `actor_id`
for older rows. The database copies each new identity in the booking transaction.
This example assumes insert-only claims, explicit column names in both clients,
and a trusted actor from the request or message. Reassigning a claim would
need its own update policy. The primary key on `slot_id` and its foreign key
to `slots` keep the [one-claim-per-slot guarantee](./reservation-schema.md)
in place throughout.

## 1. Seed and expand

Open two `psql` sessions, A and B, to one empty disposable PostgreSQL
database as its owner. A represents a v1 worker and B a v2 API replica.
Use autocommit except for explicit transactions. A also executes migration
SQL. Run this setup in A before connecting v2.

```sql
SET application_name = 'reservations-v1';
CREATE TABLE slots (slot_id integer PRIMARY KEY);
CREATE TABLE slot_claims (
    slot_id  integer PRIMARY KEY REFERENCES slots (slot_id),
    actor_id text NOT NULL,
    claim_id text NOT NULL
);
INSERT INTO slots SELECT generate_series(40, 46);
INSERT INTO slot_claims (slot_id, actor_id, claim_id)
VALUES (40, 'ana', 'a0'), (41, 'ben', 'b1');
```

In A, install the new column, write bridge and view in one transaction.
A before-insert trigger fills whichever name a caller omitted. The check
rejects a pair of conflicting identities. `NOT VALID` defers the scan of
existing rows while enforcing the check on new or updated rows.

```sql
BEGIN;
SET LOCAL lock_timeout = '2s';
ALTER TABLE slot_claims ADD COLUMN booked_by_id text;

CREATE FUNCTION mirror_booking_identity() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    NEW.booked_by_id := COALESCE(NEW.booked_by_id, NEW.actor_id);
    NEW.actor_id := COALESCE(NEW.actor_id, NEW.booked_by_id);
    RETURN NEW;
END;
$$;
CREATE TRIGGER mirror_booking_identity
    BEFORE INSERT ON slot_claims
    FOR EACH ROW EXECUTE FUNCTION mirror_booking_identity();
ALTER TABLE slot_claims ADD CONSTRAINT same_booking_identity
    CHECK (booked_by_id IS NOT NULL AND booked_by_id = actor_id) NOT VALID;

CREATE VIEW reservation_owners_v2 AS
    SELECT slot_id, COALESCE(booked_by_id, actor_id) AS booked_by_id, claim_id
    FROM slot_claims;
COMMIT;
```

Enable v2 after expansion commits. In a deployment, grant the application's
role the required access to the new view and column, and test as that role.
Set a lock wait budget appropriate for the service. If DDL times out,
roll back the failed transaction, inspect blockers and retry that phase.

## 2. Mix versions and interrupt a backfill

In **B (v2)**, read the pre-migration owners through the view. Expect Ana
and Ben even though their new columns are still null.

```sql
SET application_name = 'reservations-v2';
SELECT slot_id, booked_by_id FROM reservation_owners_v2 ORDER BY slot_id;
```

In **A**, prepare a bounded backfill and start its first batch. Leave the
transaction open after it returns slot 40.

```sql
PREPARE fill_identity(integer) AS
    WITH batch AS (
        SELECT slot_id FROM slot_claims
        WHERE booked_by_id IS NULL ORDER BY slot_id LIMIT $1 FOR UPDATE
    )
    UPDATE slot_claims AS c SET booked_by_id = c.actor_id
    FROM batch WHERE c.slot_id = batch.slot_id
    RETURNING c.slot_id;
BEGIN;
EXECUTE fill_identity(1);
```

While A holds that row, **B** books a different slot with only the new name.

```sql
INSERT INTO slot_claims (slot_id, booked_by_id, claim_id)
VALUES (42, 'cara', 'c2');
```

In **A (v1)**, commit the batch and pause the backfill. Read Cara's booking
through the old column, then make a v1 booking while slot 41 still needs
backfill. The select returns `cara, c2`.

```sql
COMMIT;
SELECT actor_id, claim_id FROM slot_claims WHERE slot_id = 42;
INSERT INTO slot_claims (slot_id, actor_id, claim_id)
VALUES (43, 'dan', 'd3');
```

In **B (v2)**, verify that Dan's booking is visible through the new contract.
A competing claim for the same slot returns zero rows.

```sql
SELECT booked_by_id, claim_id FROM reservation_owners_v2 WHERE slot_id = 43;
INSERT INTO slot_claims (slot_id, booked_by_id, claim_id)
VALUES (43, 'eve', 'e3')
ON CONFLICT (slot_id) DO NOTHING RETURNING claim_id;
```

Use the following gate in A now, after resuming, and before cleanup. At the
pause expect `missing = 1` and `mismatched = 0`. The trigger populated both
identities for Cara and Dan while historical rows were being processed.

```sql
SELECT count(*) FILTER (WHERE booked_by_id IS NULL OR actor_id IS NULL) AS missing,
       count(*) FILTER (WHERE booked_by_id IS NOT NULL
                          AND booked_by_id IS DISTINCT FROM actor_id) AS mismatched
FROM slot_claims;
```

In **A**, simulate an interruption before the next batch commits. The update
returns slot 41. After rollback, rerun the gate and expect `1, 0` again.

```sql
BEGIN;
EXECUTE fill_identity(1);
ROLLBACK;
```

Resume in **A** with autocommit on. The first call fills slot 41 again and the
second returns zero rows. Recheck the gate and expect `0, 0`. On a larger
table, commit each batch and repeat while rows remain. If a session exits,
prepare the statement again. The null predicate picks up unfinished rows
and skips committed work. Investigate any mismatch before advancing.

```sql
EXECUTE fill_identity(1);
EXECUTE fill_identity(1);
DEALLOCATE fill_identity;
```

## 3. Cut over reads and rehearse application rollback

In A, validate the check across stored rows before promoting the new column.
Run validation as its own transaction so its scan finishes before the
stronger locks required for cutover. The view keeps its public column names,
order and types. Keep the trigger and both columns during the rollback window.

```sql
ALTER TABLE slot_claims VALIDATE CONSTRAINT same_booking_identity;
BEGIN;
SET LOCAL lock_timeout = '2s';
ALTER TABLE slot_claims ALTER COLUMN booked_by_id SET NOT NULL;
CREATE OR REPLACE VIEW reservation_owners_v2 AS
    SELECT slot_id, booked_by_id, claim_id FROM slot_claims;
COMMIT;
```

Rehearse rolling the application back to v1 while the expanded schema is
live. Pause B's v2 writes. In **A**, confirm that v1 reads `cara, c2` from
the v2 booking, then use v1 to book another slot.

```sql
SELECT actor_id, claim_id FROM slot_claims WHERE slot_id = 42;
INSERT INTO slot_claims (slot_id, actor_id, claim_id)
VALUES (44, 'fay', 'f4');
```

Resume v2 in **B**. Expect `fay, f4` for the booking made during rollback.
Run the identity gate again and expect `0, 0`.

```sql
SELECT booked_by_id, claim_id FROM reservation_owners_v2 WHERE slot_id = 44;
```

## 4. Retire the old column

Close session A in the lab. In B, run the following check. Expect zero rows.

```sql
SELECT pid, application_name, state
FROM pg_stat_activity
WHERE datname = current_database() AND application_name = 'reservations-v1';
```

Use B as migration operator for the remaining steps. In a deployment, check
the running revisions of API replicas and workers, drain old pools and jobs,
and verify that v2 can process scheduled jobs and retried messages. Check
version-tagged database activity and query logs over a period that covers
pool, job and retry lifetimes.
An empty session snapshot alone misses idle schedules and future reconnects.

Check dependent views, reports and indexes. If the customer-lookup index
from the [index exercise](./reservation-index.md) is in use, build and
verify its replacement on `booked_by_id` before dropping `actor_id`.
Repeat the identity gate in B. Proceed when both counts are zero, v2 reads and
writes have passed, old consumers have drained, and the team has closed the
v1 rollback window. The last point for an **application-only rollback** is
before the following transaction commits.

```sql
BEGIN;
SET LOCAL lock_timeout = '2s';
DROP TRIGGER mirror_booking_identity ON slot_claims;
ALTER TABLE slot_claims DROP CONSTRAINT same_booking_identity,
                       DROP COLUMN actor_id;
DROP FUNCTION mirror_booking_identity();
COMMIT;
```

In B, make a v2 booking and read the complete history. Expect six rows,
one per slot from 40 through 45, including the original claims by Ana and Ben.

```sql
INSERT INTO slot_claims (slot_id, booked_by_id, claim_id)
VALUES (45, 'gia', 'g5');
SELECT slot_id, booked_by_id, claim_id FROM reservation_owners_v2 ORDER BY slot_id;
```

After cleanup, v1 SQL references a missing column. Recover by rolling forward
with a compatible v2 build. If v1 must return, first re-expand the schema,
restore the write bridge, backfill `actor_id` from the surviving identities
and verify all bookings, including post-cleanup writes, before routing v1
traffic. Restoring an older backup also requires reconciling later bookings.
See [deployment and promotion](../ci-cd/deployments-and-promotion.md),
[rollback and service recovery](../runbooks/deployment-rollback-and-service-recovery.md)
and the [PostgreSQL adoption notes](./references.md#schema-migrations).
