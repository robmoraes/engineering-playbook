# DevOps Standards

A practical operating model for delivering, operating and improving software
through shared responsibility, short feedback loops and controlled automation.

## DevOps Position

DevOps is not a toolchain, a deployment job or a team placed between
development and operations. It is a way of organizing engineering work so
that the people who shape a system share responsibility for its useful
outcomes across design, delivery, operation, learning and retirement.

Default position:

1. Begin with the user or organizational outcome, then design the delivery
   system needed to support it.
2. Keep changes small, visible, testable, traceable and recoverable.
3. Move operational, security and quality feedback close to the change that
   can act on it.
4. Treat production behavior, failed changes and operator experience as
   inputs to engineering priorities.
5. Automate repeated work where the desired outcome, authority boundary and
   failure path are understood.
6. Improve the whole flow of work instead of optimizing one team or tool at
   the expense of the system.

The goal is not maximum deployment frequency or maximum automation. The goal
is a sustainable ability to deliver valuable change safely and learn from its
real effects.

## Operating Contexts

| Context | Practical DevOps expectation |
| --- | --- |
| **Learning/lab** | Versioned work, repeatable setup and safe credentials; document limitations rather than imitate production ceremony |
| **Maintained service** | Explicit owner, automated validation, traceable releases, useful operational evidence and a maintenance path |
| **Production service** | Controlled delivery, environment isolation, observable behavior, recovery procedure and owned incident response |
| **Critical service** | Stronger change controls, reliability objectives, tested recovery, sustainable response and evidence-driven improvement |
| **Shared platform** | Product-oriented capabilities, self-service contracts, consumer feedback, lifecycle ownership and blast-radius controls |

These contexts describe increasing consequence, not career seniority or
technology count. Apply the smallest set of practices that controls the real
risk and supports responsible operation.

## Navigation

| Document | Covers |
| --- | --- |
| [Operating Model](./operating-model.md) | Outcomes, lifecycle ownership, collaboration, authority and the DevOps Engineer role |
| [Flow and Continuous Delivery](./flow-and-continuous-delivery.md) | Value streams, small batches, WIP, integration, delivery and recovery flow |
| [Feedback, Measurement and Learning](./feedback-measurement-and-learning.md) | Feedback loops, DORA delivery metrics, learning culture and improvement cycles |
| [Platform and Automation](./platform-and-automation.md) | Automation boundaries, self-service, platforms as products and paved paths |
| [DevOps Checklist](./devops-checklist.md) | Adoption and periodic review across ownership, flow, delivery and operation |
| [References](./references.md) | External guidance and the practices adopted or adapted here |

## Relationship To SRE

DevOps is the baseline operating model. Site Reliability Engineering (SRE) is
a more specific discipline for defining, measuring and operating reliability
within that model.

This section requires teams to consider production outcomes, recovery and
operational sustainability. [SRE Standards](../sre/README.md) own detailed
guidance for service context, SLIs/SLOs, error-budget policy, on-call models,
operational toil, capacity and reliability reviews. Existing
[Observability](../observability/README.md),
[Infrastructure](../infrastructure/README.md) and
[Runbook](../runbooks/README.md) standards remain authoritative for their
implementation mechanics.

Shared ownership does not require every developer to hold production
administrator access or participate in the same on-call rotation. The access,
response and escalation model must match system impact, team capacity and
explicit authority boundaries.

## Non-Negotiable Defaults

- Every maintained system MUST have a stated purpose, owner and lifecycle
  status.
- Every production change MUST leave a traceable record of intent, authority,
  result and affected version or configuration. Routine changes MUST originate
  from reviewed versioned definitions.
- A production deployment MUST define how success is verified and how failure
  is contained, rolled back or recovered.
- Production feedback MUST be available to people who can prioritize and
  implement corrective work.
- Security, testing and operability MUST be considered during delivery rather
  than delegated only after release.
- Delivery and operational metrics MUST be used to improve a service and its
  system of work, not to rank or punish individuals.
- Material failures MUST produce owned learning or corrective action without
  using blame as a substitute for technical analysis.

## Related Standards

- Human responsibility and proportional engineering:
  [Professional Principles](../principles/README.md).
- Source collaboration and repository controls:
  [GitHub Standards](../github/README.md) and
  [Repository Standards](../repositories/README.md).
- Build, release, deployment and recovery mechanics:
  [CI/CD Standards](../ci-cd/README.md).
- Risk-focused validation: [Testing Standards](../testing/README.md).
- Runtime and platform capabilities:
  [Infrastructure Standards](../infrastructure/README.md).
- Production evidence: [Observability Standards](../observability/README.md).
- Reliability objectives, readiness and sustainable response:
  [SRE Standards](../sre/README.md).
- Embedded delivery and runtime protection:
  [Security Standards](../security/README.md).
- Incident and recovery procedures: [Operational Runbooks](../runbooks/README.md).
