# SRE Checklist

Use this checklist when productionizing, deploying or reliability-reviewing a
service. Record `not applicable` decisions with reasons and stop on unresolved
material conditions rather than checking boxes optimistically.

## Service Context

- [ ] Purpose, users/dependents and critical journeys are explicit.
- [ ] Reliability context matches actual impact rather than technology size.
- [ ] Service, platform, data and change owners are known.
- [ ] Support window and escalation match available staffing.
- [ ] A current Service Reliability Record is versioned or authoritatively
  linked.
- [ ] Known limitations and accepted risks have owners and review triggers.

## Service-Level Management

- [ ] SLI measures a user/dependent outcome at an appropriate boundary.
- [ ] Good, eligible, excluded and missing events are defined.
- [ ] SLO target and window follow user need, cost and support capacity.
- [ ] Measurement source and known gaps are documented.
- [ ] Error budget is calculated and visible where the SLO drives decisions.
- [ ] Error-budget policy defines healthy, at-risk and exhausted behavior.
- [ ] SLO and error budget are not used to evaluate individuals.
- [ ] Paging on budget burn is actionable and appropriate to traffic volume.

## Production Readiness

- [ ] Architecture, trust boundaries, state and critical dependencies are
  understood.
- [ ] Failure domains, timeouts, retries and degradation behavior are reviewed.
- [ ] Capacity and quota assumptions include launch and failure reserve.
- [ ] Source, artifact, configuration and deployment result are traceable.
- [ ] Production access and automation authority are minimal and controlled.
- [ ] Data/schema changes are compatible or have tested recovery.
- [ ] Readiness decision and any accepted gap are recorded.

## Change And Verification

- [ ] Current service health and error-budget state are reviewed before risk.
- [ ] Rollout depth is proportional to impact and evidence quality.
- [ ] Success and stop conditions are defined before execution.
- [ ] Prior compatible state or another containment/recovery path is available.
- [ ] Critical journey is verified after each material rollout stage.
- [ ] Delayed or batch failure receives an appropriate observation period.
- [ ] Emergency changes are recorded and reconciled into versioned state.

Apply the detailed [CI/CD Delivery Checklist](../ci-cd/delivery-checklist.md).

## Observability And Paging

- [ ] Service/environment/version identity exists across useful telemetry.
- [ ] User symptoms can be separated from infrastructure causes.
- [ ] Dashboards support SLO state and symptom-to-cause investigation.
- [ ] Every page represents prompt action that can reduce material impact.
- [ ] Page includes owner, symptom, query/dashboard, runbook and escalation.
- [ ] Telemetry blindness is detected where it invalidates safety decisions.
- [ ] Recurring noisy alerts create owned corrective work.

Apply the detailed
[Observability Checklist](../observability/observability-checklist.md).

## Response And Learning

- [ ] Responder can obtain safe access and identify current production state.
- [ ] Common mitigations and escalation have current runbooks.
- [ ] Incident declaration, roles, communication and timeline are understood.
- [ ] Recovery is verified through the affected journey.
- [ ] Temporary state and emergency access are reconciled after response.
- [ ] Material incidents receive blameless technical review.
- [ ] Corrective actions have owner, priority and completion evidence.

Apply the detailed [Operational Runbooks](../runbooks/README.md).

## Data And Disaster Recovery

- [ ] Valuable state has a backup or explicit reproducibility decision.
- [ ] RPO/RTO or accepted data/recovery limits are stated.
- [ ] Backup survives the failure domain it is intended to cover.
- [ ] Restore includes integrity and representative application validation.
- [ ] Recovery credentials, tooling and capacity are available when needed.
- [ ] Last validation result and next trigger/cadence are recorded.
- [ ] Temporary restored sensitive data is removed safely.

## Toil And Sustainability

- [ ] Repeated manual operational work is visible.
- [ ] Operational load preserves sufficient engineering improvement capacity.
- [ ] Toil reduction considers elimination before automation.
- [ ] Automation has authority, evidence, failure and lifecycle controls.
- [ ] Paging/support load is sustainable for the declared model.
- [ ] Service commitments are reduced or staffing/engineering changes occur
  when load exceeds the accepted bound.
- [ ] No critical operation depends on one undocumented person.

## Capacity And Overload

- [ ] Demand unit, peak, growth and limiting resource are known.
- [ ] Safe capacity is tested at required latency/correctness.
- [ ] Headroom covers a named failure, rollout or demand scenario.
- [ ] Scaling delay and external quotas are understood.
- [ ] Deadlines, bounded retries and queue/backpressure behavior are explicit.
- [ ] Service can reject or degrade work without uncontrolled collapse.
- [ ] Capacity trends route to planned work before becoming pages.

## Reliability Validation

- [ ] Material failure hypotheses have expected detection and recovery.
- [ ] Tests use the lowest-risk environment that provides adequate evidence.
- [ ] Production experiments, if any, have blast radius and abort conditions.
- [ ] Rollback, restore, failover and overload claims are exercised
  proportionally.
- [ ] Game days include human roles, access and communication when relevant.
- [ ] Failed validation updates the service model and produces owned repair.
- [ ] Reliability test cadence uses explicit dates or change triggers.

## Stop Conditions

Do not declare production readiness with an applicable unresolved condition:

- [ ] No service owner or response route.
- [ ] No deployed version/configuration identity.
- [ ] No critical-journey verification.
- [ ] No containment or recovery for a consequential change.
- [ ] Valuable data without a backup/reproducibility decision.
- [ ] Untrusted access to production authority or secrets.
- [ ] Paging with no available responder or useful action.
- [ ] Reliability/support commitment with no measurement or staffing.
- [ ] Uncontrolled dependency, capacity or cascading-failure risk.

Checking an item in this section means the stop condition exists. Resolve it
or record an authorized risk acceptance before proceeding.

## Codex Handoff

After implementing against this standard, report:

```text
Service and reliability context:
Critical journey protected:
Controls implemented or changed:
Validation performed and evidence:
SLO/error-budget decision:
Deployment and recovery behavior:
Residual risks and exceptions:
Required owner input or next review:
```

## Exception Record

```text
Control not applied:
Service/environment:
Reason and constraint:
Affected journey/data/reliability consequence:
Compensating control and detection:
Accepting owner:
Review/removal date or trigger:
```
