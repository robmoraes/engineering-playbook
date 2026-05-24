# Infrastructure Standards

Standards for organizing, provisioning and operating infrastructure that
supports software delivery and production workloads.

## Infrastructure Position

Infrastructure exists to provide predictable runtime, connectivity, state,
access and recovery capabilities. It is successful when a maintainer can
understand what is running, change it safely, detect failure and recover
within an explicitly accepted cost and complexity envelope.

Default position:

1. Choose the simplest topology that satisfies availability, durability,
   security and recovery requirements.
2. Express repeatable infrastructure through versioned definitions and
   controlled automation.
3. Separate edge, application, data, management and observability concerns,
   even when they initially share a small footprint.
4. Design failure handling, backups and operator access before calling a
   system production-ready.
5. Add redundancy only with an understood failure domain, validation method
   and operating owner.

## Operating Contexts

| Context | Practical infrastructure expectation |
| --- | --- |
| **Personal lab** | Disposable or clearly limited infrastructure; no implied HA; safe credentials and useful learning documentation |
| **Cost-sensitive hosted project** | Automated deployment, backups for valuable data, basic monitoring and explicit single points of failure |
| **Small production environment** | Isolated production boundary, maintained ingress, recovery procedure, controlled access and observable deployments |
| **Highly available system** | Redundant failure domains, validated failover/recovery, capacity planning and service-level justification |
| **Enterprise platform** | Account/network segmentation, reusable provisioning controls, auditability, lifecycle governance and shared platform ownership |

## Navigation

| Document | Covers |
| --- | --- |
| [Principles and Boundaries](./principles-and-boundaries.md) | Infrastructure philosophy, ownership, trust boundaries and platform responsibilities |
| [Topology and Environments](./topology-and-environments.md) | Runtime layout, environment isolation, edge/core and shared platform services |
| [Networking and Edge](./networking-and-edge.md) | Ingress, load balancing, networks, service discovery and segmentation |
| [Clusters and Orchestration](./clusters-and-orchestration.md) | Docker Swarm, Kubernetes considerations, nodes, quorum and lifecycle |
| [Storage, Backup and Recovery](./storage-backup-and-recovery.md) | Stateful systems, persistent storage, backup, restore and disaster recovery |
| [Provisioning and Lifecycle](./provisioning-and-lifecycle.md) | IaC, immutable changes, cloud foundations, registry/deployment integration and technical debt |
| [Observability and Operations](./observability-and-operations.md) | Metrics, logs, alerts, runbooks, access and troubleshooting |
| [Reliability, Cost and Maturity](./reliability-cost-and-maturity.md) | HA decisions, failure domains, AWS tradeoffs, cost and maturity levels |
| [Infrastructure Checklist](./infrastructure-checklist.md) | Design, production readiness and lifecycle review |
| [References](./references.md) | External guidance and conventions adapted here |

## Non-Negotiable Defaults

- Infrastructure resources MUST be identifiable and named according to
  [Naming: Runtime and Infrastructure Resources](../naming/runtime-and-infrastructure.md).
- Production state MUST have a documented backup or reproducibility decision
  and a tested recovery expectation.
- Production access, secrets and machine identities MUST follow
  [Security Standards](../security/README.md).
- Public endpoints, privileged control planes and data stores MUST have
  intentional network exposure rather than incidental reachability.
- A production-affecting infrastructure change MUST be reviewable,
  attributable and recoverable or explicitly accepted as irreversible.
- Monitoring and runbooks SHOULD cover the failures the topology is intended
  to survive.

## Related Standards

- Runtime and service design: [Architecture Standards](../architecture/README.md).
- Image/runtime and orchestration usage: [Docker Standards](../docker/README.md).
- Artifact promotion and deployments: [CI/CD Standards](../ci-cd/README.md).
- Infrastructure repository boundaries: [Repository Standards](../repositories/README.md).
