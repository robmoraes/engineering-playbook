# Choosing Automated Tests by Risk

Start with a failure someone could observe. Which parts of the system have
to run for that failure to occur? Choose the smallest check that includes
those parts, then place it before the first delivery decision that needs its
result. Record the expected outcome and any risk that remains open in the
[test case](./test-case-standards.md).

| If the change could break… | Choose | When the cost is justified |
| --- | --- | --- |
| A decision made from known inputs | Unit | The rule can run in process. Each additional input or boundary case costs little to exercise. |
| Behavior owned jointly by code and a dependency | Integration | Starting and resetting the real dependency is worthwhile when its behavior determines the result. |
| An interaction between independently released components | Contract | A consumer relies on a particular status or field. Checking a shared example lets either side release independently. |
| A user journey through deployed components | End-to-end | A routing or configuration error could break a critical outcome. That risk warrants the cost of staging, cleanup and diagnosis. |

## Four risks in the reservation flow

The API and the queue worker are two entry points to the same booking
operation. Both must check permission before claiming a slot or looking up
a previous attempt. A booking is confirmed only after its claim commits.
See [business rule placement](../software-design/business-rule-placement.md)
and the [caller contracts](../software-design/module-boundaries-and-errors.md).

### Unit — a revoked permission still allows a booking

Ana booked slot 42 as claim `a1`. Revoke her booking permission and call
`reserveSlot` with the same authenticated actor, slot and claim ID. Run the
real booking operation and permission rule. Give them a recording store
that would return Ana's original claim if called. Expect `Forbidden` and
zero claim reads or writes. A returned confirmation exposes a replay path
that bypasses the permission check.

Run this on the **pull request** and block merge on failure. The store double
can tell us whether booking touched storage, and the check runs entirely
in process. Whether the HTTP handler or worker supplies the correct actor
from its credentials remains a separate risk.

### Integration — two customers receive the same slot

Exercise the real booking operation and PostgreSQL adapter against a
disposable PostgreSQL database with the release schema. Give Ana and Ben
booking permission, distinct claim IDs and the same empty slot. Use two
independent connections at Read Committed. Hold Ana's write open, start
Ben's and observe that his transaction is waiting on hers before letting
Ana commit. Expect one confirmation for Ana and `SlotTaken` for Ben. Read
the slot from a fresh connection and expect exactly Ana's claim. Two
confirmations are a failure even if only one row survives. The
[two-session exercise](../databases/reservation-schema.md) shows how to
observe the wait and how the expected winner changes if Ana rolls back.
Use the [runnable contention test](../examples/snippets/databases/README.md#test-the-last-available-slot)
to automate the commit case and reproduce a timeout locally or in CI.

Run this in **pull request validation** for changes to booking, its storage
adapter or the schema. Block merge on a wrong outcome or if the test cannot
establish overlap within its timeout. A fake store can return a conflict on
cue, but only the real engine exercises the deployed unique key, wait and
commit visibility. This check leaves HTTP mapping and worker acknowledgement
untested.

### Contract — the client misreads an occupied slot as a success

Use the consumer's actual HTTP client to submit a booking against a stub
provider. Have the stub return the agreed `409` response with `SlotTaken`
and verify that the client reports the slot as taken. Save that interaction
as the contract. Provider verification replays its request against the real
HTTP handler and serializer and matches the response against the same
expectations. Supply the occupied-slot booking outcome behind the handler.
A provider that emits `200` or omits the error code the client uses breaks
this interaction even if its response is valid JSON.

Run the consumer example and provider verification in their respective
**pull requests**. Check a provider change against the expectations of
consumer versions still in use. Block an incompatible change before merge.
The stub makes the conflict reproducible. The provider check catches drift
from that expectation, while database contention and deployed routing stay
outside the contract.

### End-to-end — a worker confirms a booking the API cannot find

In staging, use a synthetic customer and a fresh test slot. Submit one
booking through the real broker and wait up to the worker's delivery
deadline for its durable confirmation. Through the deployed HTTP route,
resubmit the same authenticated actor, slot and claim ID. Expect `200`
with the original confirmation. A timeout, a fresh `201` or a different
confirmation fails the journey. For example, the worker and API could
both be healthy while pointing at different databases.

Run this **before release**, with the candidate artifact, broker, worker,
API, authentication and PostgreSQL wired as they will be for promotion.
Hold promotion on failure and retain the claim ID and component logs for
diagnosis. Use a slot per run and remove the synthetic fixture afterward.
A single journey leaves peak load and the losing side of a race untested.

After deployment, verify the promoted digest through the production route.
A bounded **smoke check** can replay a known synthetic booking on a slot
reserved for that purpose and require `200` with the original confirmation.
It can catch production routing or credential errors. If the fixture is
missing, the request could create a booking, so isolate it from customer
inventory. An unexpected `201` needs investigation before a retry can reuse
that slot. On failure, pause expansion, inspect the response and deployment
telemetry, and roll back only if the previous digest is compatible with
current data and configuration. See [pipeline principles](../ci-cd/pipeline-principles.md)
and [deployments and promotion](../ci-cd/deployments-and-promotion.md).

For each run, keep the revision or artifact digest, environment, expected
and observed outcome, and the evidence needed to reproduce a failure.
The [adoption notes](./references.md#automated-test-selection) identify
the sources behind these choices.
