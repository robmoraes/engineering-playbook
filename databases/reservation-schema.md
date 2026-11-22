# A Reservation Schema Under Contention

Two customers see the last appointment slot as available. Ana books through
the API and Ben books through a worker. The invariant is **at most one
committed claim per slot**. An availability read helps customers choose a
slot. The database write decides which customer gets it.

## Model one place and one claim

Use an empty disposable PostgreSQL database. Open two `psql` sessions, A
and B, connected to that database as the same role. Run the setup once in A
with autocommit enabled. These regular tables must be visible to both sessions.

```sql
CREATE TABLE slots (
    slot_id integer PRIMARY KEY
);

CREATE TABLE slot_claims (
    slot_id  integer PRIMARY KEY REFERENCES slots (slot_id),
    actor_id text NOT NULL,
    claim_id text NOT NULL
);

INSERT INTO slots (slot_id) VALUES (42);
```

The foreign key on `slot_claims.slot_id` requires every claim to reference
an existing slot. The primary key on **that same column** allows only one
claim for the slot, even when different actors use different claim IDs.
A key on `(slot_id, actor_id)` would allow both customers to book it.
A slot without a claim is available. In this example a claim lasts for the
exercise and its actor and claim ID identify the attempt within the slot.

## Start the competing writes

In B, name the connection so A can check who is waiting. Keep these two
connections open across both runs.

```sql
SET application_name = 'lab-slot-claim-b';
```

In **A**, start Ana's claim. Leave the transaction open after the insert.

```sql
BEGIN ISOLATION LEVEL READ COMMITTED;
INSERT INTO slot_claims (slot_id, actor_id, claim_id)
VALUES (42, 'ana', 'a1')
ON CONFLICT (slot_id) DO NOTHING
RETURNING claim_id;
```

A sees `a1` from `RETURNING`. The application can confirm the reservation
only after a successful commit. In **B**, submit Ben's claim for slot 42.

```sql
BEGIN ISOLATION LEVEL READ COMMITTED;
INSERT INTO slot_claims (slot_id, actor_id, claim_id)
VALUES (42, 'ben', 'b1')
ON CONFLICT (slot_id) DO NOTHING
RETURNING claim_id;
```

B waits inside the insert while PostgreSQL checks the unique slot key.
In **A**, run this query before deciding the outcome. Expect one row with
`b_waits_for_a = t`. If it shows no wait, verify the database, slot and
open transactions before proceeding.

```sql
SELECT pg_backend_pid() = ANY(pg_blocking_pids(pid)) AS b_waits_for_a
FROM pg_stat_activity
WHERE datname = current_database() AND application_name = 'lab-slot-claim-b';
```

## Run 1 — A commits

Issue `COMMIT;` in **A**. Ana's claim is now confirmed. B's pending insert
finishes with **zero returned rows** because the specified key conflicts.
In **B**, read the slot in a separate statement, then finish the transaction.

```sql
SELECT actor_id, claim_id FROM slot_claims WHERE slot_id = 42;
COMMIT;
```

At Read Committed each statement gets a fresh snapshot. B now reads
`ana, a1`. This is a different attempt from `ben, b1`, so the worker
reports `SlotTaken`. A retry by the original actor with the same claim ID
would instead recover the original confirmation. An unrelated database
failure follows the [caller error contract](../software-design/module-boundaries-and-errors.md).

### Verify from a fresh connection

Open a **new** connection to the same database after both transactions end.
Run this query after each round. Its row count and identity describe the
committed result independently of either writer.

```sql
SELECT slot_id, actor_id, claim_id FROM slot_claims WHERE slot_id = 42;
```

For run 1 expect exactly one row, `42, ana, a1`.

## Run 2 — A rolls back

Reset the lab fixture in the verification connection with autocommit enabled.
Expect `DELETE 1`. Repeat the verification query and check that it returns
zero rows. The parent slot still exists. Close this connection.

```sql
DELETE FROM slot_claims
WHERE slot_id = 42 AND actor_id = 'ana' AND claim_id = 'a1';
```

1. Repeat the [A and B transaction blocks](#start-the-competing-writes).
   In A, verify `b_waits_for_a = t` again.
2. Issue `ROLLBACK;` in **A**. Its provisional claim is discarded, so Ana
   receives no booking confirmation.
3. B's pending insert now returns `b1` because the conflict disappeared.
   Issue `COMMIT;` in **B**. The worker can now report Ben's confirmation.
4. Open another fresh connection and run the verification query. Expect
   exactly one row, `42, ben, b1`.

Both outcomes follow from the same schema and write. A's transaction ending
determines whether B finds a committed competitor or can take the slot.
The [adoption notes](./references.md) distinguish the PostgreSQL guarantees
from the booking policy used by the API and worker.
