# Site Reliability Engineering Standards

Practical standards for defining, operating and improving service reliability
with software engineering, measurable objectives and sustainable human
response.

## SRE Position

Site Reliability Engineering (SRE) applies engineering to the work of running
services. Its purpose is not to prevent every failure. It is to make the
required reliability explicit, control risk, learn from production and reduce
the human effort needed to keep a service dependable.

Default position:

1. Define reliability from a user or dependent-system journey.
2. Choose an explicit reliability target instead of promising perfection.
3. Use SLIs, SLOs and error budgets to make risk and change decisions.
4. Detect material failure and prepare a safe response before production.
5. Treat changes, dependencies, capacity and data recovery as reliability
   concerns.
6. Measure operational work and engineer recurring toil out of the system.
7. Test reliability and recovery claims; hope and documentation alone are not
   evidence.

SRE is a discipline and an operating capability. A project can apply it
without creating an SRE team or using SRE as a job title.

## Reliability Survival Sequence

When time is limited, preserve this sequence:

| Moment | Minimum action |
| --- | --- |
| Before production | Name the owner, critical journey, known failure modes, support model, deployment verification and recovery path |
| Before a risky change | Confirm current service health, change authority, rollback/containment and observable success criteria |
| When alerted | Confirm user impact, identify the active change, declare ownership and choose the safest mitigation |
| During an incident | Stabilize service, preserve useful evidence, control concurrent changes and communicate state |
| Before resolution | Verify the affected journey, understand remaining risk and assign material follow-up |
| After failure | Learn without blame, improve the weakest defense and validate the updated procedure |

The detailed emergency procedure remains in
[Operational Runbooks](../runbooks/README.md). This section defines the
reliability policy that decides what must be prepared and why.

## Operating Contexts

| Context | Practical SRE expectation |
| --- | --- |
| **Learning/lab** | State that reliability is uncommitted; keep rebuild, credentials and exposure safe |
| **Maintained service** | Identify owner, user journey, health evidence, maintenance path and known limitations |
| **Production service** | Record service reliability, define meaningful SLI/SLO or a justified exception, alert actionable impact and test recovery |
| **Critical service** | Use error-budget policy, sustainable response, capacity evidence, staged change and regularly exercised recovery |
| **Shared platform** | Define consumer-facing reliability, dependency contracts, support boundaries and failure isolation proportional to blast radius |

Apply controls because impact requires them, not to claim an SRE maturity
label. A well-operated small service is preferable to an elaborate reliability
program that no available maintainer can sustain.

## Navigation

| Document | Covers |
| --- | --- |
| [Service Reliability Record](./service-reliability-record.md) | Service context, criticality, ownership, dependencies and canonical record |
| [Service-Level Management](./service-level-management.md) | SLIs, SLOs, error budgets, burn-rate alerting and decision policy |
| [Production Readiness and Change](./production-readiness-and-change.md) | Readiness review, launch evidence, staged change and risk acceptance |
| [On-Call, Incidents and Learning](./on-call-incidents-and-learning.md) | Support models, actionable paging, incident roles, communication and postmortems |
| [Toil, Capacity and Overload](./toil-capacity-and-overload.md) | Operational work, toil reduction, demand, headroom and overload protection |
| [Reliability Testing and Recovery](./reliability-testing-and-recovery.md) | Failure testing, game days, backup/restore and recovery evidence |
| [SRE Checklist](./sre-checklist.md) | Practical implementation and review checklist with stop conditions |
| [References](./references.md) | Google SRE reading map, external guidance and local adoption notes |

## Applying This Standard With Codex

When asked to deploy, productionize or reliability-review a service, Codex or
another implementer SHOULD:

1. Read this section and the relevant domain standards before changing files.
2. Identify the service context and critical user/dependent journey.
3. Create or update the
   [Service Reliability Record](./service-reliability-record.md).
4. Apply the [SRE Checklist](./sre-checklist.md) at the depth justified by
   impact.
5. Reuse the repository's CI/CD, observability, infrastructure, security and
   runbook standards instead of inventing parallel conventions.
6. Implement concrete controls and validation, not only documentation claims.
7. Report evidence, residual risk and every deliberate exception in the final
   handoff.

An instruction to "make it production-ready" does not authorize invented
business targets, hidden credentials, infrastructure purchase or unsupported
24/7 commitments. Record missing decisions and use safe proportional defaults
where they do not change service scope.

Suggested request:

```text
Apply the repository's SRE standards to SERVICE_OR_CHANGE.
Read sre/README.md, the SRE Checklist and the relevant domain standards before
implementation. Identify the reliability context and critical journey; update
the Service Reliability Record and use a proportional Production Readiness
Review. Do not invent SLOs, owners or support commitments. Implement and
validate concrete controls, then report evidence, residual risk and required
owner decisions.
```

## Stop Conditions

Do not represent a service as production-ready while any applicable condition
remains unresolved or explicitly unaccepted:

- no accountable owner or response route;
- no way to identify the deployed version or material configuration;
- no verification of the critical user/dependent journey;
- no rollback, containment or recovery path for a consequential change;
- valuable persistent data with no backup or reproducibility decision;
- production secrets or authority exposed to an untrusted workflow;
- paging configured without an actionable response or available responder;
- a reliability target or 24/7 promise with no measurement or staffing model;
- a known capacity or dependency failure that can create uncontrolled
  cascading impact.

A documented risk acceptance may permit launch when the responsible owner has
authority to accept the consequence, the limitation is communicated and a
review trigger exists. Acceptance does not make the risk disappear.

## Non-Negotiable Defaults

- Every production service MUST have an owned service reliability record or an
  equivalent authoritative record.
- Reliability MUST be evaluated through user or dependent-system behavior,
  not infrastructure health alone.
- Every SLO MUST define its SLI, target, window, data source, exclusions and
  owner.
- An error-budget policy MUST state which decisions change as reliability risk
  increases; it MUST NOT be used to punish individuals.
- Every page MUST require timely human action and link to useful diagnostic or
  response context.
- Production changes MUST expose verification and rollback, containment or
  recovery behavior proportional to impact.
- Valuable data recovery and critical failure-response claims MUST be tested
  at a defined cadence.
- Recurring operational toil MUST be visible and compete explicitly for
  engineering priority.

## Relationship To DevOps

[DevOps Standards](../devops/README.md) define the broader model for shared
ownership, flow, feedback and automation. SRE provides a concrete reliability
discipline within that model. It does not receive an unfinished service and
inherit all operational risk through a one-way handoff.

## Related Standards

- User outcomes and long-term responsibility:
  [Professional Principles](../principles/README.md).
- System boundaries and failure design:
  [Architecture Standards](../architecture/README.md).
- Build, rollout, verification and rollback:
  [CI/CD Standards](../ci-cd/README.md).
- Metrics, logs, traces, dashboards and alerts:
  [Observability Standards](../observability/README.md).
- Capacity, state, failure domains and recovery:
  [Infrastructure Standards](../infrastructure/README.md).
- Incident procedures and safe operational action:
  [Operational Runbooks](../runbooks/README.md).
- Access, secrets and response controls:
  [Security Standards](../security/README.md).
