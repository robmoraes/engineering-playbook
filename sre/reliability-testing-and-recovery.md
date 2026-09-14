# Reliability Testing And Recovery

Reliability is a claim about behavior under change and failure. Validate the
claim before a real incident supplies the first test.

## Start With A Failure Hypothesis

For each material scenario, record:

```text
Failure or change introduced:
Affected journey and expected impact:
Expected detection:
Expected containment/degradation:
Expected recovery and time/data bounds:
Safety boundary and abort condition:
Environment and authority:
Evidence to retain:
Owner and review trigger:
```

A test without an expected result is exploration. Exploration is useful, but
label it honestly and use tighter safety boundaries.

## Testing Ladder

Use the lowest-risk test that provides adequate evidence, then add depth as
consequence requires:

| Layer | Evidence |
| --- | --- |
| Static/design review | Failure modes, dependencies, limits and response assumptions are explicit |
| Automated component/integration test | Local fault handling and compatibility behave as designed |
| Load/soak test | Capacity, saturation, leaks and performance limits are measured |
| Staging recovery exercise | Rollback, restore, failover and procedures work in a representative environment |
| Game day | People, alerts, access, communication and system response work together |
| Bounded production experiment | Real behavior is validated where lower environments cannot provide sufficient fidelity |

Do not introduce production failure merely to appear mature. A bounded
experiment requires a material learning need that safer evidence cannot meet.

## What To Test

Select scenarios from the actual architecture:

- bad application or configuration rollout;
- dependency timeout, partial failure or incompatible response;
- lost process, replica, node or selected failure domain;
- queue, connection pool, disk, memory or quota exhaustion;
- retry storm, traffic spike or abusive client behavior;
- expired certificate, credential or external provider interruption;
- corrupt, missing or delayed data;
- backup restore and point-in-time recovery;
- control-plane, monitoring or deployment-path impairment;
- operator absence, access failure or escalation handoff.

Test correlated failures when the architecture shares a dependency. Ten
component tests do not prove the system survives one common control-plane or
data-store failure.

## Safe Experiment Rules

- Begin in local/staging environments where the behavior is representative.
- State the blast radius, affected data and authorized executor.
- Protect real users and sensitive data.
- Confirm observability before injecting failure.
- Define abort conditions and a tested rollback/containment path.
- Avoid overlapping risky changes or experiments.
- Maintain an independent communication/control path where feasible.
- Record the actual result, unexpected behavior and residual risk.
- Stop immediately if impact exceeds the authorized boundary.

A chaos tool does not create a safe experiment. Reliability engineering is in
the hypothesis, boundary, observation and resulting system improvement.

## Validate Deploy And Rollback

For the production delivery path, test:

- artifact and configuration identity;
- staged deployment and stop conditions;
- health plus critical-journey verification;
- prior compatible version availability;
- application, schema and configuration rollback compatibility;
- behavior when deployment automation fails partially;
- recovery when rollback is impossible.

A rollback command that has never been exercised is an assumption. If a data
migration prevents rollback, validate forward repair, restore or compatible
expand/migrate/contract behavior instead.

## Validate Data Recovery

Backup success is not recovery evidence. Test end to end:

```text
1. Select a protected recovery point without altering production.
2. Restore into an isolated controlled target.
3. Verify integrity, completeness and required decryption/access.
4. Validate the application or representative query against restored data.
5. Measure actual data loss and wall-clock recovery bounds.
6. Record dependencies, manual steps and failures.
7. Remove temporary restored sensitive data safely.
```

Confirm:

- backup coverage and retention match the data requirement;
- copies survive the failure domain they are intended to protect against;
- credentials, keys, tooling and capacity are available during recovery;
- the process works without unavailable production components;
- observed RPO/RTO meet the commitment or update the accepted limitation.

Detailed storage rules are in
[Infrastructure: Storage, Backup and Recovery](../infrastructure/storage-backup-and-recovery.md).

## Capacity And Overload Tests

Measure useful service capacity at the required latency/correctness, not only
the maximum request rate before a crash.

Test:

- ordinary, peak and launch traffic mix;
- a selected replica/node/dependency unavailable;
- scaling delay and quota exhaustion;
- timeout, retry and queue behavior under slowness;
- graceful degradation and load shedding;
- recovery after load returns to normal;
- observability behavior during saturation.

Use synthetic or sanitized data. Stop before uncontrolled impact to shared
environments.

## Game Day Record

```text
Scenario and learning objective:
Service/context:
Date, owner and participants:
Environment and authorized blast radius:
Preconditions and current health:
Expected alerts, response and recovery:
Abort conditions:
Timeline and observations:
Actual user/data/service impact:
Recovery verification:
Gaps and corrective owners:
Next validation:
```

Game days test the sociotechnical system: alerts, access, decisions,
communication, documentation and technology. Rotate roles and include a safe
handoff when those are part of the support model.

## Test Cadence

Use both time and change triggers:

| Claim | Example trigger |
| --- | --- |
| Low-impact rebuild | After material build/runtime change |
| Production rollback | After delivery or compatibility model change |
| Valuable-data restore | Scheduled by data/recovery consequence and after backup redesign |
| Critical failover | Regular exercise and after topology/control-plane change |
| Incident response | Regular scenario practice and after role/escalation change |
| Capacity boundary | Before expected growth/launch and after material performance change |

Record the chosen cadence in the Service Reliability Record. "Periodically"
without an owner or trigger is not a schedule.

## Use Failure As New Evidence

An incident or failed exercise supersedes an older successful claim. Update:

- the failure model;
- readiness and service records;
- monitoring and alert conditions;
- runbooks and access paths;
- rollback, restore or failover mechanisms;
- tests and their cadence;
- owned reliability work.

Repeat the narrow failed validation after repair. Do not close corrective work
solely because documentation now describes the intended behavior.
