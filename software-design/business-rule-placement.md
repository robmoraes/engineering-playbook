# Business Rule Placement

When two callers can make the same business decision, give the decision one
owner in the application. When its correctness depends on shared state,
enforce it where that state changes. For a reservation, those responsibilities
belong to the booking module and the write that claims a slot.

## Find the owner

| Question | Where the answer belongs | Reservation example |
| --- | --- | --- |
| Can this input be decoded? | Entry point | Parse the slot ID from an HTTP request or queue message. |
| May this actor perform the action? | Shared operation or authorization policy it calls | Check the actor's booking permission on both paths. |
| What does the action mean? | Module that owns the capability | Return either a confirmed reservation or a slot already taken. |
| What must hold across concurrent writes? | Shared store, inside the write or transaction | Permit at most one claim for a slot. |
| How does the caller see the result? | Entry point | Translate the same outcome into an HTTP response or a worker disposition. |

Start with a named function in the owning module. A function that reads
explicit inputs is usually enough for a calculation such as a cancellation
fee. A rule about shared availability also needs a concurrency guarantee.
Introduce a separate interface when a real caller or dependency needs one.

## Worked example — reserve the last slot

Two customers see the last appointment as available. One books through the
API while a worker handles the other's request. Both availability reads can
be correct when made. Only one customer can receive a confirmed booking.

In this example a slot identifies one bookable place. A confirmed claim
lasts for the exercise. Cancellation and rebooking would require defining
which claims count as active.

1. The API decodes an HTTP request and the worker decodes a message. Each
   obtains the actor from trusted request or message context and calls
   `reserveSlot(actor, slotId, claimId)`. A retry uses the same actor,
   slot and claim ID as the original attempt. The booking module checks
   authorization before any write or replay lookup.
2. The module asks storage to claim the slot. In PostgreSQL, the claims
   table has a primary key on `slot_id` and stores the actor and claim ID.
   For an existing, bookable slot, use a conditional insert.

   ```sql
   INSERT INTO slot_claims (slot_id, actor_id, claim_id)
   VALUES ($1, $2, $3)
   ON CONFLICT (slot_id) DO NOTHING
   RETURNING claim_id;
   ```

3. A returned row confirms the new claim once the transaction commits.
   With PostgreSQL's default Read Committed isolation, if the insert returns
   no row, read the claim for that slot in a subsequent statement. A matching
   actor and claim ID replays the original confirmation. Another claim means
   `SlotTaken`. Keep the competing customer's details private.

The following responses are the contract for this example.

| Booking outcome | HTTP caller | Queue worker |
| --- | --- | --- |
| New claim committed | Return `201` with the confirmation. | Record the confirmation and acknowledge the message. |
| Same claim redelivered | Return `200` with the original confirmation. | Reuse the confirmation, avoid duplicate effects and acknowledge. |
| Slot taken by another claim | Return `409` with `SlotTaken`. | Record the rejection and acknowledge once durable. |
| Transient storage failure | If a reply is possible, return `503`. The client can retry with the same claim ID. | Keep the message eligible for bounded retry with the same claim ID. |

A timeout during commit may leave the caller unsure whether the claim was
stored. Redelivery with the original identity resolves that uncertainty.

An availability check can help the UI show useful choices. Two callers can
still pass that check before either writes. A lock held inside one application
process would leave the worker in the other process free to claim the slot.

## Verify the decision

Use two connections to the same disposable PostgreSQL database. For this
exercise, create the table once and commit it before starting either claim.

```sql
CREATE TABLE slot_claims (
    slot_id  integer PRIMARY KEY,
    actor_id text NOT NULL,
    claim_id text NOT NULL
);
```

To run the parameterized insert above in `psql`, prefix it with
`PREPARE claim_slot(integer, text, text) AS` in **each** session. Use
a fresh slot ID for each run. In this run both customers request slot 42.

| Step | Session and action | Expected observation |
| --- | --- | --- |
| 1 | A (API): `BEGIN ISOLATION LEVEL READ COMMITTED;` then `EXECUTE claim_slot(42, 'ana', 'a1');` | Returns `a1`. Keep the transaction open. |
| 2 | B (worker): `BEGIN ISOLATION LEVEL READ COMMITTED;` then `EXECUTE claim_slot(42, 'ben', 'b1');` | The write waits for A. |
| 3 | A: `COMMIT;` | The API can confirm Ana's booking. B's insert finishes with zero rows. |
| 4 | B: `SELECT actor_id, claim_id FROM slot_claims WHERE slot_id = 42;` then `COMMIT;` | The new statement sees `ana, a1`. The worker records `SlotTaken` for Ben and acknowledges. |

To verify overlap, obtain B's process ID with `SELECT pg_backend_pid();`
before step 2. While B's insert is pending, query
`SELECT pg_backend_pid() = ANY(pg_blocking_pids(<B_pid>));` in A,
substituting B's numeric ID. Proceed to step 3 when the query returns true.
If the wait never appears within 10 seconds, cancel B's pending write,
roll back both transactions and check that both sessions used the same slot.

From a fresh connection, read all claims for slot 42. Expect exactly one
row owned by Ana with claim ID `a1`. Then simulate a lost success response
by replaying Ana's original request. The insert returns zero rows and the
subsequent lookup matches the original claim, so Ana receives the same
confirmation. The stored row is unchanged.

At the application boundary also exercise a caller without booking permission
and a temporary storage outage. Check that authorization rejects the write,
and that the API and worker surface the outage as specified above.

## Reviewing an existing implementation

Trace the endpoint and the worker to their writes. If each owns a copy of
the rule, capture both callers' current behavior, move the decision behind
one operation, then route each caller through it. Review the final diff for
any remaining write path that can bypass the guarantee.

For source guidance and the assumptions behind the SQL example, see the
[adoption notes](./references.md).
