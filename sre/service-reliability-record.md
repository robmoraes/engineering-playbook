# Service Reliability Record

A Service Reliability Record (SRR) is the compact source of truth for how a
service is expected to behave, who responds when it does not and which
evidence supports its production claims.

## Record Location

A maintained service SHOULD store the record with its versioned source at:

```text
docs/operations/service-reliability.md
```

An organization may use an authoritative service catalog instead. In that
case, the repository must link to the catalog record and must not maintain a
conflicting copy. Runbooks, dashboards and deployment workflows should link
back to the same service identity.

Use the reusable
[Service Reliability Record Template](../examples/templates/sre/service-reliability-record.md)
as a starting point.

## Reliability Context

Choose the context from [SRE Standards](./README.md) and state real impact:

| Context | Minimum record |
| --- | --- |
| Learning/lab | Purpose, owner, exposure, rebuild path and explicit lack of reliability commitment |
| Maintained service | Critical journey, dependencies, health evidence, support expectation and known limits |
| Production service | SLI/SLO decision, alerts, deployment/recovery paths, data protection and review cadence |
| Critical service | Error-budget policy, capacity and failure evidence, sustainable on-call and exercised recovery |
| Shared platform | Consumer contract, dependency/blast radius, support boundaries and platform recovery |

Context is not inferred from the technology. A single container can support a
critical workflow; a multi-cluster platform can still be an unsupported lab.

## Required Record

Every production SRR MUST contain:

```markdown
# Service Reliability Record - <service>

## Identity And Purpose

Service:
Repository:
Runtime/environment:
Lifecycle: experimental | maintained | production | retiring
Reliability context:
Purpose and users/dependents:
Critical journey(s):

## Ownership And Support

Service owner:
Technical escalation:
Support window: best effort | business hours | 24x7
Alert destination:
Change authority:
Last reviewed:

## Service-Level Management

SLI/SLO link or embedded definition:
Error-budget policy:
Known measurement gaps:

## Architecture And Dependencies

Entry point:
Critical dependencies and owners:
Persistent state and owner:
Failure/degradation behavior:
Capacity or quota limit:

## Delivery And Configuration

Artifact/configuration identity:
Deployment and verification:
Rollback/containment/recovery:
Feature flag or migration constraints:

## Operations

Service dashboard:
Alerts:
Runbooks:
Incident coordination route:

## Data And Disaster Recovery

Backup/reproducibility decision:
RPO/RTO or accepted limitation:
Restore/recovery procedure:
Last validation and result:

## Capacity And Reliability Validation

Demand unit, peak and growth:
Tested safe capacity and limiting resource:
Failure/maintenance reserve:
Reliability scenarios and evidence:
Next exercise trigger/date:

## Toil And Sustainability

Recurring operational work:
Accepted operations-work bound:
Dominant toil-reduction action:
Paging/support sustainability:

## Risks, Exceptions And Review

Accepted risks:
Temporary exceptions, owners and dates:
Next review trigger/date:
```

Use `Not applicable` only with a reason. An empty field is an unresolved
decision, not evidence that the concern does not exist.

## Define Critical Journeys

A critical journey is an outcome that a user or dependent system needs, such
as:

- authenticate and reach an account;
- submit and retrieve an order;
- enqueue and complete a payment job;
- read data within an accepted freshness bound;
- restore a protected dataset;
- provision a platform capability for a consuming service.

Name the entry point, completion condition and important failure behavior. Do
not define the journey as "the container is running" or "the endpoint returns
HTTP 200" unless that alone is the actual dependent outcome.

## Ownership And Support Model

The record distinguishes:

| Responsibility | Meaning |
| --- | --- |
| Service owner | Accountable for service behavior, priorities and accepted reliability risk |
| Platform owner | Accountable for the shared runtime capability and its consumer contract |
| On-call/responder | Available during the declared support window to assess and coordinate response |
| Change authority | Permitted to approve or execute a production change |
| Data owner | Decides protection, retention, recovery and disposition requirements |

One person may hold several roles in a small project, but the responsibilities
remain distinct. Do not claim 24x7 support when one person is merely reachable
occasionally. Use `best effort` or `business hours` and state the consequence.

## Dependency Record

For each critical dependency, record:

```text
Dependency and owner/provider:
Behavior used:
Timeout and retry boundary:
Failure/degradation behavior:
Quota or capacity limit:
Data/security consequence:
Operational evidence:
Escalation or fallback:
```

The record need not list every library. Include dependencies whose latency,
unavailability, data loss, quota exhaustion or incompatible change can break a
critical journey.

## Evidence, Not Links Alone

A dashboard link is useful only if the dashboard identifies the correct
service and journey. A runbook link is useful only if the procedure is current
and executable with available authority. A backup link is useful only if
restore has been validated.

For consequential claims, include the last validation date and result:

```text
Claim: production rollback restores the previous compatible artifact
Validated: 2026-09-14 in staging
Evidence: <workflow/run/result link>
Limitation: does not reverse destructive database migration
Next validation: before the next migration model change
```

## Review Triggers

Review the SRR when:

- the service enters production or changes reliability context;
- ownership, support or deployment authority changes;
- a critical journey or dependency changes;
- an SLO or error-budget policy changes;
- data, recovery, topology or rollout behavior changes materially;
- an incident reveals an incorrect assumption;
- a periodic review date arrives;
- the service begins retirement.

The review should update the source record and the controls it references.
Changing documentation without changing a known broken control does not close
the risk.
