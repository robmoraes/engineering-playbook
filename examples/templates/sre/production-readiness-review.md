# Production Readiness Review - SERVICE_NAME

> Copy this file to `docs/operations/production-readiness.md` for the service.
> Link concrete evidence and remove checklist items only when a documented
> reason makes them not applicable.

## Review Context

- **Service/environment:** SERVICE_AND_ENVIRONMENT
- **Review trigger:** FIRST_LAUNCH_OR_MATERIAL_TRANSITION
- **Critical journey and consequence:** JOURNEY_AND_IMPACT
- **Service Reliability Record:** RECORD_LINK
- **Planned launch/change:** CHANGE_IDENTITY
- **Reviewer:** REVIEWER
- **Service owner:** OWNER
- **Decision date:** YYYY-MM-DD

## Decision

Select one:

- [ ] Ready
- [ ] Ready with accepted risk
- [ ] Not ready

**Rationale:** DECISION_AND_STRONGEST_EVIDENCE

## Purpose, Ownership And Support

- [ ] Purpose, consumers and critical journeys are current.
- [ ] Service, platform, data, escalation and change authority are explicit.
- [ ] Support window matches actual staffed coverage.
- [ ] Runbooks, dashboards and communication routes are accessible.

**Evidence/limitations:** LINKS_AND_FINDINGS

## Architecture, Capacity And Dependencies

- [ ] Entry points, trust boundaries, state and failure domains are known.
- [ ] Critical dependencies have timeout, retry and degradation decisions.
- [ ] Safe capacity covers expected demand and a named failure/launch reserve.
- [ ] Cascading-failure and shared-platform risks are controlled or accepted.

**Evidence/limitations:** LINKS_AND_FINDINGS

## Delivery, Configuration And Change

- [ ] Source, artifact, configuration and deployed result are traceable.
- [ ] Rollout stages, success signals and stop conditions are defined.
- [ ] Rollback, containment or another recovery path is exercised.
- [ ] Schema, API and feature activation sequencing preserve compatibility.
- [ ] Production authority is minimal and protected from untrusted changes.

**Evidence/limitations:** LINKS_AND_FINDINGS

## Observability And Service Levels

- [ ] Critical-journey behavior is observable.
- [ ] SLI/SLO or a justified exception is documented.
- [ ] Error-budget policy changes risk decisions where an SLO is used.
- [ ] Pages represent actionable impact and route to an available responder.
- [ ] Telemetry loss is visible when it invalidates readiness decisions.

**Evidence/limitations:** LINKS_AND_FINDINGS

## Response, Data And Recovery

- [ ] Responders have safe access during the declared support window.
- [ ] Incident coordination and escalation routes have been validated.
- [ ] Valuable state has a backup or explicit reproducibility decision.
- [ ] Observed restore/recovery evidence meets the stated bounds.
- [ ] Emergency changes and temporary access can be reconciled.

**Evidence/limitations:** LINKS_AND_FINDINGS

## Security, Cost And Lifecycle

- [ ] Secrets, machine identities, production access and telemetry are
  protected.
- [ ] Dependency/artifact risk and maintenance ownership are understood.
- [ ] Runtime, retention and support cost are accepted.
- [ ] Retirement can remove access, state, telemetry and dependencies safely.

**Evidence/limitations:** LINKS_AND_FINDINGS

## Launch Or Change Plan

```text
Owner and execution authority:
Current health and error-budget state:
Artifact/configuration/data identity:
Rollout stages:
Success signals:
Stop conditions:
Rollback/containment/recovery:
Observation period:
Communication/support needs:
Evidence retained:
```

## Gaps And Risk Acceptance

| Unmet control | Consequence | Compensating control/detection | Accepting owner | Review/removal trigger |
| --- | --- | --- | --- | --- |
| GAP | CONSEQUENCE | CONTROL | OWNER | DATE_OR_TRIGGER |

An owner may accept only risks within their authority. Schedule and cost
pressure explain a decision but are not compensating controls.

## Required Actions

| Action | Owner | Priority | Due/trigger | Completion evidence |
| --- | --- | --- | --- | --- |
| ACTION | OWNER | PRIORITY | DATE_OR_TRIGGER | EVIDENCE_LINK |

## Approval

- **Service owner:** NAME_AND_DATE
- **Required risk/data/security authority:** NAME_AND_DATE_OR_NOT_APPLICABLE
- **Next readiness review:** DATE_OR_CHANGE_TRIGGER
