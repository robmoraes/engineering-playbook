# Module Boundaries, Dependencies and Errors

A booking request can arrive over HTTP or through a queue. Both callers
need to know whether a reservation was confirmed, whether somebody else
claimed the slot, or whether the result is still unknown. Define those
outcomes in the booking module. Each caller can then decide what to tell
its client or broker using the same evidence.

This chapter uses the single-slot guarantee from
[Business Rule Placement](./business-rule-placement.md).

## Trace calls and imports

Consider a worker delivering a reservation message. At runtime the worker
calls `reserveSlot`, which checks the actor's permission and calls the
PostgreSQL adapter to claim the slot. The adapter returns evidence from the
transaction. The result travels back to the worker, which decides when to
acknowledge. The HTTP handler drives the same operation.

| Component | What its code depends on | Decision it owns |
| --- | --- | --- |
| HTTP handler | HTTP library and booking contract | Decode the request, establish the actor, map the result to a response. |
| Queue worker | Broker client and booking contract | Decode the message and its trusted actor context, then acknowledge or arrange redelivery. |
| Booking module | Its authorization policy and a storage operation it defines | Authorize the actor, interpret the claim and return a booking outcome. |
| PostgreSQL adapter | Booking's storage contract and the PostgreSQL driver | Execute the claim transaction and translate its result or failure. |

At startup, supply the PostgreSQL implementation to the booking operation.
This lets booking call storage at runtime while the adapter imports the
contract owned by booking. A change of database driver should ordinarily
touch the adapter and its wiring.

Start with a function if one operation such as `claimSlot` expresses the
whole dependency. Passing that function is enough to substitute a failing
store in a test. Introduce a named interface when several implementations
must satisfy a shared contract that callers maintain together. Keep the
operations on it specific to what the booking module uses.

## Define the public operation

`reserveSlot(actor, slotId, claimId)` takes an authenticated actor, an
existing bookable slot and a caller-provided identifier for this attempt.
The actor, slot and claim ID stay together across every retry. The operation
checks permission before attempting the write or looking up a prior claim.

- Return `Confirmed(confirmation, replayed)` after a committed write or
  after matching a stored claim to the same actor, slot and claim ID.
- Return `SlotTaken` when the slot is held by a different claim. Return
  `Forbidden` if the actor lacks permission. Neither outcome includes
  another customer's identity.
- Report `StoreUnavailable` for a transient failure known to precede the
  write. Report `CommitUnknown` when confirmation from the database was
  lost and the operation might already have committed.

Translate at the point that has the evidence. For example, the PostgreSQL
adapter can see that connecting failed before it sent any SQL. It can also
see that the connection was lost *after* it sent the commit. That timing
determines which failure it returns. Keep driver exceptions and query
details available in internal diagnostics.

For a claim conflict, the adapter uses the write targeted at the slot key
and reads the existing claim as described in the placement chapter. The
booking module compares the stored identity with the request. An unrelated
constraint violation or unexpected driver error is an internal failure.
Only evidence of a different claim on the requested slot warrants
`SlotTaken`.

## Translate the outcome at each entry point

| Booking outcome | HTTP handler | Queue worker |
| --- | --- | --- |
| Confirmed or replayed | Return `201` for creation or `200` with the original confirmation on replay. | Record the confirmation idempotently under the claim identity, then acknowledge. |
| Slot taken | Return `409`. A new booking choice is a new intent. | Record the terminal rejection and acknowledge. Retrying this claim cannot free the slot. |
| Forbidden | Return `403` for the authenticated actor. | Record the denial and finish the delivery according to the terminal-outcome policy. |
| Store unavailable | Return `503` if a response can be sent. A retry reuses the same claim identity. | Schedule a bounded retry with the same identity. Acknowledge the original delivery only once the retry is durably handed off, or use broker-managed redelivery. |
| Commit unknown | Return `503` with an unknown outcome if the connection to the client is open. A disconnected client may see only a timeout. | Keep the attempt recoverable and retry with the original identity, using the same durable retry policy. |
| Unexpected internal failure | Return `500` with a generic error and a correlation ID. | Route the delivery to the failed-message policy and retain the claim identity for investigation. |

With `CommitUnknown`, the next attempt either finds its original committed
claim or competes for the slot if the first write rolled back. Once the
retry budget is exhausted, preserve the claim identity and failure evidence
for reconciliation. Check the stored claim before reporting a final outcome.

## Review and verify a change

1. Inspect the booking module's imports and its public parameter, result
   and error types. A broker delivery tag, HTTP response or driver exception
   crossing this boundary identifies a translation to move into an adapter.
2. Drive both entry points with a store that fails before the write. Expect
   HTTP `503` and a recoverable worker delivery with the original claim ID.
   HTTP `409` or a terminal worker rejection exposes an error mapping bug.
3. Simulate a store that commits and then loses its confirmation. Redeliver
   the original attempt. Expect the original confirmation and exactly one
   stored claim. Repeat with a different authorized actor and claim ID for
   that slot. Expect `SlotTaken` and the original row to remain intact.

The [references and adoption notes](./references.md) explain the sources
behind these boundaries and delivery choices.
