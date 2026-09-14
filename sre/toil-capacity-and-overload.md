# Toil, Capacity And Overload

Reliable operation must scale through engineering rather than proportional
human intervention. Make operational work visible, remove recurring toil and
protect the service before demand exceeds safe capacity.

## Identify Toil

Toil is operational work that tends to be:

- manual or requires hands-on execution;
- repetitive and predictable;
- automatable or removable by design;
- reactive and tactical;
- without enduring service improvement;
- proportional to traffic, users, resources or service count.

Not every unpleasant or manual task is toil. First-time diagnosis, a
well-designed review and a migration that permanently removes risk can create
enduring value. Toil is a spectrum; classify it from evidence rather than job
title or personal preference.

Examples:

| Work | Classification |
| --- | --- |
| Restart the same unhealthy worker every week | Toil and likely missing remediation |
| Investigate a novel partial failure | Engineering/diagnostic work |
| Manually approve a high-risk irreversible migration | Potentially justified human control |
| Copy routine environment values between systems | Toil and configuration-risk source |
| Remove obsolete alerts and fix their ownership | Enduring reliability improvement |

## Maintain A Toil Record

For repeated operational work, capture:

```text
Task and trigger:
Service/journey affected:
Frequency and variability:
Hands-on and elapsed time:
Interrupt or paging impact:
Required access and execution risk:
Growth driver:
Current procedure/owner:
Can eliminate | simplify | automate | batch | reject:
Estimated engineering cost and time saved:
```

Use approximate consistent measurements before building a detailed tracking
system. A task repeated with the same decision path three times is a useful
prompt to evaluate toil, not an automatic requirement to automate it.

## Preserve Engineering Capacity

Each team or maintainer operating production SHOULD state how much operational
load is sustainable while retaining time for engineering improvement.

Review at least:

- pages and incidents;
- tickets and support requests;
- manual releases, restores and access changes;
- recurring investigation and report generation;
- interrupt fragmentation, not only total hours;
- post-incident and maintenance work;
- planned reliability engineering completed versus displaced.

Google's practice of limiting aggregate operational work to 50% protects an
engineering focus in its SRE organization. This playbook does not impose that
number universally. Set a local upper bound appropriate to staffing and
service commitments, then act when the trend breaches it.

For a solo maintainer, the most honest response to overload may be reducing
support promises, removing scope or selecting a managed capability rather than
adding more alerts and automation to an unsustainable service.

## Reduce Toil In Order

Consider these responses before creating automation:

1. **Eliminate** the need through a service or process change.
2. **Simplify** the task and remove unnecessary variants.
3. **Reject or reduce** work whose cost exceeds its user/reliability value.
4. **Batch** safe nonurgent work to reduce interrupts.
5. **Delegate to a supported capability** when ownership and economics fit.
6. **Automate** the stable decision and execution path.

Automation that needs frequent human repair can create a new source of toil.
Follow the [DevOps Automation Contract](../devops/platform-and-automation.md)
for authority, evidence, partial failure and lifecycle controls.

## Prioritize Toil Reduction

Prefer work with a strong combination of:

- high recurring hands-on time;
- frequent interruption or sleep impact;
- meaningful execution error or privilege risk;
- growth with service demand;
- several affected services or responders;
- clear, stable automation or design-removal path;
- measurable time or failure reduction.

Do not optimize solely for hours saved. Removing one rare but dangerous manual
production action may be more valuable than automating many harmless reports.

## Capacity Model

Capacity is the amount of useful service behavior deliverable within its
latency, correctness and reliability boundaries. Resource count alone is not
capacity.

For a production-critical path, record:

```text
Demand unit: requests | jobs | bytes | tenants | concurrent work | other
Current typical and peak demand:
Expected organic growth:
Known launch/event demand:
Tested service capacity at required behavior:
Limiting resource or dependency:
Required failure/maintenance reserve:
Current safe headroom:
Provisioning/scaling lead time:
Owner and review trigger:
```

Forecast beyond the time required to obtain and validate capacity. Include
organic growth and known discontinuities such as launches, migrations,
campaigns, tenant onboarding and dependency limits.

## Headroom And Failure Reserve

Headroom must cover the selected failure model, not an arbitrary percentage.
Examples:

- loss of one replica or node while retaining required latency;
- rollout overlap during start-first deployment;
- retry and queue growth during dependency degradation;
- traffic or batch spikes before scaling completes;
- restore or failover resource requirements;
- shared-platform consumer concurrency.

Autoscaling reduces some provisioning delay but does not create unlimited
capacity. Scaling can lag, hit quotas, amplify dependency load or fail when the
control plane is impaired. Test its trigger, limit and failure behavior.

## Observe Saturation

Monitor the resource that constrains useful work:

- concurrency and worker/thread/connection pools;
- queue depth, age and rejection;
- CPU throttling, memory pressure and garbage collection;
- disk capacity, latency and I/O contention;
- network limits and downstream quotas;
- response latency at current demand;
- autoscaling state and remaining provider quota.

Capacity alerts SHOULD state time or distance to service impact where
possible. Page when prompt action prevents imminent material harm; create
planned work for a gradual trend.

## Protect Against Overload

Design overload behavior before it is needed:

| Control | Purpose | Common failure if misused |
| --- | --- | --- |
| Deadline/timeout | Bound resource occupancy and caller wait | Independent layers create an impossible total deadline |
| Bounded retry with backoff/jitter | Recover selected transient failure | Retry multiplication creates a storm |
| Queue bound/backpressure | Limit admitted work and signal upstream | Unbounded age converts overload into delayed failure |
| Rate limit/quota | Protect service and fair use | One static limit ignores different workloads |
| Load shedding | Reject early before collapse | Late rejection consumes the same scarce resources |
| Graceful degradation | Preserve the most valuable journey | Degraded result is incorrect or invisible to users |
| Circuit/protective limit | Stop repeated calls to an unhealthy dependency | Recovery probes or fallback overload another path |
| Isolation/bulkhead | Contain one tenant/workload/failure domain | Shared hidden dependency defeats isolation |

Clients and servers share responsibility. A server should fail early and
cheaply when it cannot do useful work; a client should respect deadlines,
retry budgets and backpressure.

Detailed architecture tradeoffs are in
[Architecture: State, Reliability and Scale](../architecture/state-reliability-and-scale.md).

## Retry Standard

- Retry only operations that are safe or idempotent for the attempted scope.
- Use a finite attempt or elapsed-time budget.
- Apply exponential backoff and jitter for distributed clients where useful.
- Do not retry permanent validation, authorization or quota errors blindly.
- Keep the total work within the caller's deadline.
- Avoid retries at every layer; choose the layer able to make the decision.
- Expose attempts and final outcomes without logging sensitive payloads.
- Test behavior during dependency slowness and total failure.

## Graceful Degradation

Define what can be reduced or disabled while preserving the core journey:

```text
Protected journey:
Optional work/features:
Degradation trigger:
User/dependent-visible behavior:
Data correctness/freshness effect:
Recovery and re-enable criteria:
Owner and test evidence:
```

Returning fast incorrect success is not graceful degradation. Make reduced
quality, staleness or partial completion explicit to the consumer when it
changes meaning.

## Operational Overload

Treat these as evidence of an unsustainable service:

- recurring pages with no completed permanent action;
- responders unable to finish incident follow-up;
- manual work growing with traffic or service count;
- chronic support queues or privileged bottlenecks;
- maintenance and reliability projects continually displaced;
- alert fatigue, unsafe shortcuts or dependence on one expert;
- service commitments exceeding available support.

Respond by stabilizing work intake, reducing avoidable pages, dedicating
engineering effort to dominant causes and renegotiating ownership or service
commitments. Adding people without reducing linear toil postpones the same
failure at a larger scale.

## Review Questions

- Which operational work grows as the service grows?
- What recurring task can be eliminated rather than automated?
- Does available engineering time exceed reactive operational demand?
- What resource limits the critical journey under peak and failure?
- Is headroom validated against a named failure or only guessed?
- Do timeouts, retries and queues contain overload or amplify it?
- Can the service preserve a smaller correct journey under pressure?
