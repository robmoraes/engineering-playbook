# Principles and Boundaries

Infrastructure standards should reduce operational ambiguity. They should not
force a small system to mimic a large organization without the same failure,
scale or compliance requirements.

## Principles

### Simplicity Has Operational Value

Every additional node, network path, controller, storage layer or failover
mechanism creates an asset that must be patched, observed and recovered.
Prefer a single well-understood production topology over distributed
complexity that no one can diagnose.

```text
Good                                      Avoid
Single documented app host plus backups  Three-node cluster with no recovery test
Managed database for durable production  Self-hosted database HA without ownership
```

### Reliability Must Be Explicit

Redundancy is not a reliability claim by itself. Document:

- the failure being addressed;
- the availability or recovery objective that justifies the design;
- the remaining failure modes;
- the validation or recovery test;
- the additional cost and operator burden.

### Automation Must Leave Evidence

Infrastructure changes SHOULD originate in versioned configuration or a
controlled provider workflow and result in inspectable evidence. Manual
emergency action may be necessary; reconcile it into source and record the
reason after stabilization.

### Operability Is a Design Requirement

A topology is incomplete if maintainers cannot observe it or safely access it
under failure. Metrics, logs, alert routing, backup ownership and runbooks are
infrastructure components, not later polish.

### Boundaries Follow Risk

Separate infrastructure when access, blast radius, data sensitivity, failure
domain, cost ownership or lifecycle differs materially. Do not create
boundaries only to imitate a reference architecture.

## Infrastructure Boundary Model

| Boundary | Responsibility | Typical examples |
| --- | --- | --- |
| Edge | Receives external traffic and terminates or routes it | DNS, CDN/WAF where used, TLS ingress, reverse proxy, load balancer |
| Runtime | Runs application processes | Swarm services, Kubernetes workloads, VMs, serverless runtime |
| Data | Stores durable or sensitive state | Managed database, object storage, volumes, backup vault |
| Platform | Provides shared operational capabilities | Registry, CI runners, secrets store, observability, identity integration |
| Management | Permits change and diagnosis | IaC pipeline, orchestrator API, bastion/VPN/session manager |

Small installations may place several boundaries on the same provider account
or host. They should still document which communication and privilege paths
would be separated as risk grows.

## Ownership and Authority

For each production infrastructure domain, record:

```text
Purpose:
Owner:
Environment/account/project:
Provisioning source:
Change authority:
Runtime/operator access path:
State and backup owner:
Observability entry point:
Recovery procedure:
Cost owner/budget signal:
```

| Asset | Authority that needs control | Authority to avoid spreading |
| --- | --- | --- |
| Production network | Infrastructure/platform maintainer | Every application pipeline |
| Application deployment | Scoped deploy workflow/operator | General cloud administrator token |
| Database credentials | Workload and limited operator recovery path | Build system or public repository |
| Cluster managers/control plane | Platform administrators and constrained delivery | Routine developer SSH |
| Monitoring views | Operators and service maintainers | Write/admin privilege when read is enough |

## Platform Engineering Scope

A platform capability is justified when multiple workloads benefit from a
maintained operational contract:

- ingress and certificate management;
- image registry and artifact promotion;
- deployment environment or orchestrator;
- secrets delivery;
- metrics, logs and alerting;
- shared networking or identity foundations.

Shared services increase blast radius. They require ownership, upgrade
strategy, consumer documentation and a recovery path proportional to their
impact.

## Decision Record Triggers

Record an architecture or infrastructure decision when selecting or changing:

- orchestrator or cluster model;
- account, network or environment boundary;
- public ingress architecture;
- production data/storage or backup strategy;
- high availability or disaster recovery model;
- shared platform dependency;
- major managed-versus-self-hosted choice;
- material cost/reliability tradeoff.

Use the shared [ADR Standard](../architecture/decision-records/README.md) and
include deployment, monitoring, access, recovery and cost consequences.
