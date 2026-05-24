# Delivery and Evolution

Architecture must survive change. A topology that works only when deployed by
hand or understood by its original author is not a durable production design.

## Deployment Architecture

A deployable service SHOULD have:

- an immutable build artifact;
- environment-provided configuration and secrets;
- automated validation before deployment;
- a controlled production promotion path;
- health verification and rollback or recovery procedure;
- telemetry linking runtime behavior to deployed version.

```text
Commit -> test -> build image -> scan -> publish immutable artifact
       -> deploy stg -> verify -> approve/promote -> deploy prod -> observe
```

Build once and promote the same artifact through environments. Rebuilding for
production introduces untested dependency or base-image differences.

## Multi-Environment Strategy

Environments exist to isolate risk and validate meaningful production behavior:

| Environment | Purpose | Architecture expectation |
| --- | --- | --- |
| `dev` | Fast local/integration work | Lower-cost dependencies acceptable; no production access |
| `test` | Automated verification | Disposable, deterministic where possible |
| `stg` | Release and operational validation | Production-like routing, config shape and dependencies where material |
| `prod` | User-facing workload | Controlled deployment, durable data and monitored recovery path |
| `preview` | Change review | Disposable and isolated from production secrets/data |

Parity is valuable for risks that matter: database engine, image runtime,
routing behavior, secrets injection and migrations. Full infrastructure parity
may be wasteful for a small workload; document intentional differences.

## Observability-Driven Architecture

Before a system is production-ready, it must reveal:

- which version and environment is running;
- whether its public or critical behavior is healthy;
- dependency failures and latency;
- asynchronous backlog or failure where applicable;
- resource saturation relevant to scaling;
- events needed to diagnose access and deployment changes.

Architecture decisions should state what signals validate their intended
benefit. For example, extracting a background worker should be accompanied by
queue depth, completion latency and failure metrics rather than only a new
service diagram.

## Evolution Path

Use incremental changes that preserve recoverability:

| Stage | Architecture | Next trigger |
| --- | --- | --- |
| Experiment | Single app process and disposable local data | Need for public deployment or durable state |
| Portfolio deployment | Containerized app, external durable data, ingress, CI/CD and baseline monitoring | User traffic, background work or operational risk |
| Small production | Modular app, worker when needed, protected environments, backups and runbooks | Measured bottleneck or stricter availability |
| Critical workload | Explicit SLO, failure domain mitigation, tested recovery and tighter access boundaries | Team/region scale or higher continuity requirements |
| Platform scale | Shared paved paths, service ownership and governed runtime capabilities | Organizational need demonstrated by repetition |

This sequence is guidance, not a mandatory maturity ladder. A batch worker may
need a queue immediately; a stable internal service may never need
microservices.

## Technical Debt Management

Technical debt becomes architectural when it constrains reliability,
deployability, security or meaningful change.

Track debt when it represents:

- a known single point of failure beyond accepted recovery tolerance;
- a data boundary violation or unsafe direct dependency;
- manual deployment or recovery steps that are error-prone;
- unsupported runtime, base image or critical dependency;
- observability gaps preventing operation;
- recurring cost or performance inefficiency.

Debt record:

```text
Constraint:
Operational impact:
Current mitigation:
Trigger or deadline for action:
Candidate decision:
Owner:
```

Not every imperfect code structure needs an architecture record. Prioritize
constraints that affect production outcomes or future decisions.

## Changing Architecture Safely

For changes such as new datastores, extracted services, ingress migration,
orchestrator adoption or queue introduction:

1. Capture the context, proposed decision and alternatives in an ADR.
2. Identify changed trust, data, deployment and failure boundaries.
3. Establish how success and regressions will be observed.
4. Plan migration and rollback or compensating recovery.
5. Review the outcome after enough production evidence exists.

An ADR may be superseded later. The purpose is not to freeze design; it is to
avoid losing why a decision made sense at the time.
