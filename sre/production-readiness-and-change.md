# Production Readiness And Change

Production readiness is evidence that a service can be changed, observed and
recovered by the people who will own it. It is not a claim that failure has
been eliminated.

## When To Review

Perform a proportional Production Readiness Review (PRR) before:

- the first production launch of a maintained service;
- accepting real users, valuable data or privileged integrations;
- increasing service criticality or support commitment;
- transferring service or on-call ownership;
- a material runtime, topology, data, dependency or deployment change;
- a launch expected to change traffic or failure impact significantly;
- returning a persistently unstable service to normal change policy.

Routine low-risk releases use the established delivery and verification path;
they do not require a new full PRR.

Store the review with the service at:

```text
docs/operations/production-readiness.md
```

Use the reusable
[Production Readiness Review Template](../examples/templates/sre/production-readiness-review.md).

## Review Outcome

A PRR produces one explicit state:

| Decision | Meaning |
| --- | --- |
| Ready | Applicable controls have evidence and no unresolved stop condition remains |
| Ready with accepted risk | Named authority accepts specific residual risk, compensating control and review trigger |
| Not ready | A material uncontrolled condition prevents responsible production operation |

The reviewer and service owner may be the same person in a small project, but
the record must still separate evidence from aspiration.

## Readiness Evidence

### Purpose, Ownership And Support

- service purpose, users and critical journeys are stated;
- service, platform, data and escalation owners are known;
- support window matches available staffing;
- change and emergency authority are explicit;
- the [Service Reliability Record](./service-reliability-record.md) is current.

### Architecture And Dependencies

- entry points, trust boundaries, state and critical dependencies are known;
- failure domains and single points of failure are accepted or controlled;
- timeouts, retries and degradation behavior do not amplify dependency failure;
- capacity, quota and launch-demand assumptions are recorded;
- the design matches the required reliability instead of an unstated maximum.

### Delivery And Change

- source, artifact, configuration and deployment result are traceable;
- the same validated immutable artifact is promoted where applicable;
- production authority is minimal and isolated from untrusted changes;
- rollout, success criteria and automatic/manual stop conditions are defined;
- rollback, feature disablement, traffic removal or other containment is
  available;
- data/schema changes use compatible sequencing or have a tested recovery
  decision.

### Observability And Objectives

- critical journeys have observable user/dependent outcomes;
- an SLI/SLO and error-budget decision exist where production impact warrants
  them;
- deployed version and material configuration can be correlated with behavior;
- paging represents actionable impact or imminent risk;
- dashboards and queries support symptom-to-cause diagnosis;
- telemetry loss is distinguishable from service health where blindness is
  material.

### Response And Recovery

- alert routing and escalation work during the declared support window;
- responders can obtain required access without unsafe credential sharing;
- runbooks identify safety, diagnosis, mitigation and verification;
- valuable data has a backup or reproducibility decision;
- RPO/RTO or accepted recovery limitations are explicit;
- rollback, restore or failover claims have recent evidence;
- incident coordination and communication routes are known.

### Security And Lifecycle

- secrets, machine identities and operator access follow least privilege;
- relevant dependency, artifact and configuration risk is evaluated;
- sensitive telemetry and production data are protected;
- cost, retention, maintenance and dependency-update ownership are known;
- retirement can remove access, state, telemetry and shared dependencies.

Use the detailed domain checklists rather than copying their implementation
rules into the PRR.

## Plan A Production Change

For a consequential change, record:

```text
Change and intended outcome:
Owner and execution authority:
Affected services/journeys:
Current health and error-budget state:
Artifact/configuration/data change identity:
Dependency and capacity impact:
Rollout stages:
Success signals:
Stop conditions:
Rollback/containment/recovery:
Communication or support needs:
Evidence retained:
```

The plan may be encoded in a deployment workflow, change record or pull
request when it preserves these decisions. Avoid a second document that drifts
from the actual automation.

## Select Rollout Depth By Risk

| Change context | Reasonable rollout |
| --- | --- |
| Low-impact maintained service | Deploy, verify critical path and retain known-good rollback |
| Ordinary production service | Staged environment promotion, health/smoke verification and observable rollback |
| High-traffic or critical service | Representative canary or gradual exposure with control comparison and explicit stop criteria |
| Irreversible data or protocol change | Compatible expand/migrate/contract sequence, recovery evidence and tighter authority |
| Shared platform change | Consumer compatibility validation, staged blast radius and migration communication |

Canarying is not automatically safer. It needs representative traffic,
isolation, comparison signals, duration and a decisive stop/rollback path.
When those are unavailable, choose another bounded rollout and document the
remaining exposure.

## Change Safety Rules

- Confirm service health before attributing new failure to a rollout.
- Deploy one independently diagnosable risky change at a time where practical.
- Keep the prior compatible artifact and configuration addressable.
- Separate feature activation from binary rollout when it reduces risk.
- Give feature flags an owner, expected state and removal date.
- Use compatible schema and API evolution before removing old behavior.
- Verify from the routed user/dependent path, not process status alone.
- Stop expansion when a success criterion is absent or a stop condition fires.
- Reconcile emergency interactive changes back into versioned state.

Detailed implementation follows
[CI/CD: Deployments and Promotion](../ci-cd/deployments-and-promotion.md).

## Use Reliability State In Change Decisions

Before a risky release, review:

- current SLO/error-budget state;
- active incidents and unresolved material regressions;
- alerting or telemetry impairment;
- on-call and escalation availability;
- current capacity and unusual demand;
- overlapping infrastructure, dependency or data changes.

An exhausted error budget does not prohibit a security fix, incident
mitigation or reliability improvement. It does require explicit classification
and verification so that "urgent" does not become a route around risk control.

## Launch And Verification Sequence

```text
1. Confirm owner, authority, current health and support coverage.
2. Record artifact/configuration identity and prior known-good state.
3. Apply the smallest rollout stage.
4. Verify technical health and the critical journey.
5. Observe long enough to cover the failure signal relevant to the change.
6. Expand only while success criteria remain satisfied.
7. Record final state and remove temporary access or controls.
8. Keep heightened observation for delayed failure where applicable.
```

For batch or scheduled systems, verification may require a dry run, shadow
execution or completion of one representative cycle. A process starting is
not evidence that its output is correct.

## Risk Acceptance

An accepted readiness gap records:

```text
Unmet control and reason:
Affected journey/data/service:
Failure and user consequence:
Compensating control:
Detection and response:
Accountable accepting owner:
Review/removal date or trigger:
```

Cost or schedule pressure may explain acceptance but does not qualify as a
compensating control. Do not accept a risk on behalf of users, data owners or
service owners whose authority is required.

## Re-Review And Drift

Readiness decays as code, traffic, dependencies, people and infrastructure
change. Re-run the affected part of the PRR after a trigger; do not repeat
unrelated ceremony.

An incident, failed restore, repeated page or rollback failure is direct
evidence that a readiness assumption may be wrong. Update both the review and
the underlying control.
