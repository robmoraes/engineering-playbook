# Safely Refactoring a Shared Booking Rule

An HTTP handler and a queue worker each decide whether a booking was created,
replayed or taken by another customer. A change to replay handling now needs
two edits. Move that decision to `reserveSlot` while preserving what each
caller observes. The database already enforces one claim per slot.
See [Business Rule Placement](./business-rule-placement.md) and the
[caller contracts](./module-boundaries-and-errors.md).

## Identify the code that moves

In this example, each entry point decodes its own input and obtains the actor
from trusted context. It passes the actor, slot and caller-supplied claim ID
to its private function. The HTTP handler maps the result to a response.
The worker records a terminal outcome durably before acknowledging delivery.

Here is the starting code in Python-style pseudocode. The existing
`claimSlot` storage operation returns `Confirmed` after a new claim commits,
`Existing` with the stored row for that slot, or a typed storage failure.

```python
def apiDecision(actor, slotId, claimId):
    if not mayBook(actor, slotId):
        return Forbidden()
    result = claimSlot(actor, slotId, claimId)
    if isinstance(result, Existing):
        if result.actor == actor and result.claimId == claimId:
            return Confirmed(claimId, replayed=True)
        return SlotTaken()
    return result

def workerDecision(actor, slotId, claimId):
    if not mayBook(actor, slotId):
        return Forbidden()
    result = claimSlot(actor, slotId, claimId)
    if isinstance(result, Existing):
        if (result.actor, result.claimId) == (actor, claimId):
            return Confirmed(claimId, replayed=True)
        return SlotTaken()
    return result
```

The extraction includes the permission check and the interpretation of the
write. The SQL, transaction boundary, HTTP mapping and broker acknowledgement
stay with their existing owners.

## Characterize both callers first

Drive the existing endpoint and worker with the cases below. Start each case
with a fresh slot 42 and use a new connection to inspect committed claims.
Capture HTTP status and confirmation, the worker's durable outcome, and the
order of outcome recording and acknowledgement. Keep these assertions at
the entry points throughout the refactor.

| Case | Arrange and act | Assertions before and after each edit |
| --- | --- | --- |
| API wins the race | Ana's HTTP claim `a1` holds the slot write open. Start Ben's worker claim `b1` and verify its session is waiting on Ana's write. Let Ana commit. | HTTP returns `201` with `a1`. The worker records `SlotTaken` for `b1`, then acknowledges. The only claim for 42 is `(Ana, a1)`. |
| Worker wins and receives a replay | Deliver Ben's `b1` to the worker on an empty slot. After the claim and confirmation are durable, simulate loss of the acknowledgement and redeliver the same attempt. | Both deliveries resolve to confirmation `b1`. The redelivery acknowledges, the durable confirmation count for the attempt is one, and the only claim for 42 is `(Ben, b1)`. |
| HTTP replay and conflict | After Ben reserves the slot, submit Ben's `b1` over HTTP, then Ana's `a1`. | Ben gets `200` with the original confirmation, Ana gets `409`. The row still belongs to Ben. |
| Storage unavailable before the write | Make storage return `StoreUnavailable` to each caller. | HTTP returns `503`. The worker keeps the same attempt eligible for retry under its existing delivery policy. The slot remains empty. |
| Permission denied | Seed Ana's claim, revoke her booking permission and resubmit the same attempt through each caller. | HTTP returns `403`. The worker records the denial and follows its terminal-outcome policy. Neither path calls claim storage, and the original row is unchanged. |

For the race, follow the [two-session exercise](./business-rule-placement.md#verify-the-decision)
to confirm the writes actually overlap. For the replay, keep the actor, slot
and claim ID fixed even if the broker assigns a new delivery tag. Also force
the worker's outcome recorder to fail once just after the claim has committed.
The delivery must remain recoverable. The assertions for that failure window
can be written directly against the fixture:

```text
Given Ben can book slot 42 and the outcome recorder fails on its next write
When the worker processes Ben's claim b1
Then slot 42 contains Ben's b1, the confirmation is pending and no ACK was sent
When the recorder recovers and the broker redelivers the same booking attempt
Then one confirmation for b1 is durable before the new delivery is acknowledged
And the only claim for slot 42 is still Ben's b1
```

Run the cases against the starting implementation and record what happened.
If the worker already acknowledges a failed write, for example, record the
observed result, its impact and the desired correction in a separate change.
Resolve a baseline defect that blocks the exercise before comparing versions.

## Move one caller at a time

1. **Extract the API body.** Move the body of `apiDecision` unchanged into
   `booking.reserveSlot(actor, slotId, claimId)`. Keep `apiDecision` as a
   one-line delegate and leave the worker on its private copy. Run the
   characterization cases. Also verify that a denied actor gets `Forbidden`
   before storage is called, including when an earlier claim exists.
2. **Switch the HTTP handler.** Replace its call to `apiDecision` with
   `booking.reserveSlot`, passing the same trusted actor and identifiers.
   Run the HTTP creation, replay, conflict and outage assertions. Repeat
   the mixed API/worker race while the worker still uses the old path.
3. **Switch the worker.** Replace its call to `workerDecision` with the
   same booking operation. Keep its existing result recorder, retry policy
   and acknowledgement order. Run the worker replay and recorder-failure
   checks, then repeat the race and outage cases through both callers.
4. **Remove the old functions.** Check for remaining callers of both private
   names, delete the unused delegate and duplicate body, and run the full
   baseline again. Compare the responses, recorded outcomes and final rows
   with the observations from the starting implementation.

Both callers now invoke the same booking operation.
In this sketch, `finishDelivery` applies the existing worker outcome policy.

```text
HTTP handler: outcome = booking.reserveSlot(actor, slotId, claimId)
              return httpResponse(outcome)

Queue worker: outcome = booking.reserveSlot(actor, slotId, claimId)
              finishDelivery(message, outcome)
```

In review, trace one call from each entry point to the single booking
decision. Look for extra writes, regenerated claim IDs or an acknowledgement
moved ahead of a durable result. Any of these could change a customer's
booking even if ordinary success tests still pass.

See the [refactoring sources and adoption notes](./references.md#safe-refactoring).
