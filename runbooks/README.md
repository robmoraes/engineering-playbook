# Operational Runbooks

Repeatable procedures for investigating, mitigating and recovering production
services and their supporting platform infrastructure.

## Runbook Position

A runbook exists to make a known operational action predictable under
pressure. It must tell an operator what symptom it addresses, which evidence
to collect, what authority is required, which action is safe, how to verify
recovery and when to escalate.

Default position:

1. Confirm user or operational impact before making a production change.
2. Collect enough evidence to avoid destroying the only useful failure signal.
3. Prefer a tested recovery or rollback route over improvised mutation.
4. Make communications, timeline and ownership explicit during material
   incidents.
5. Update runbooks after incidents, platform changes and failed procedures.

## Operating Contexts

| Context | Practical procedure depth |
| --- | --- |
| **Lab** | Rebuild or dispose safely; avoid production claims and privileged shortcuts becoming habits |
| **Non-production** | Reproduce failure, validate recovery steps and protect any shared credentials or data |
| **Production** | Preserve evidence, control authority, mitigate impact, verify recovery and retain a concise record |
| **Critical incident** | Assign coordination roles, maintain timeline/communications, escalate promptly and run post-incident analysis |

## Navigation

| Document | Covers |
| --- | --- |
| [Principles and Readiness](./principles-and-readiness.md) | Runbook design, safe action, automation tradeoffs and operational readiness |
| [Incident Response and Communication](./incident-response-and-communication.md) | Severity, first response, escalation, communication and timelines |
| [Troubleshooting Methodology](./troubleshooting-methodology.md) | Reproducible diagnosis, observability-assisted workflow and resource exhaustion |
| [Deployment Rollback and Service Recovery](./deployment-rollback-and-service-recovery.md) | Release failure, rollback, health verification and dependency checks |
| [Containers and Orchestration](./containers-and-orchestration.md) | Container diagnosis, Docker Swarm procedures and Kubernetes considerations |
| [Network, Edge, DNS and TLS](./network-edge-dns-and-tls.md) | Reverse proxy, connectivity, DNS and certificate investigation |
| [Data and Infrastructure Recovery](./data-and-infrastructure-recovery.md) | Database checks, storage, backups, host/control-plane and disaster recovery |
| [Security and Delivery Recovery](./security-and-delivery-recovery.md) | Credentials, secret exposure, CI/CD and trusted artifact restoration |
| [Commands and Safe Execution](./commands-and-safe-execution.md) | Diagnostic command catalog and production execution controls |
| [Templates and Checklists](./templates-and-checklists.md) | Runbook, incident, postmortem and operational readiness templates |
| [References](./references.md) | External sources and conventions adapted here |

## Non-Negotiable Defaults

- Every production runbook MUST state scope, owner, required access,
  diagnostics, mitigation/recovery, validation and escalation.
- Read-only investigation SHOULD precede mutating actions unless immediate
  containment is required to stop active harm.
- Production recovery MUST be verified from the affected user or operational
  path, not only from process/container status.
- Live secret values, customer data and unrestricted credentials MUST NOT be
  copied into incident notes, commands, screenshots or runbook examples.
- Emergency manual changes MUST be documented and reconciled with intended
  configuration or automation after stabilization.

## Related Standards

- Signals, alerts and diagnostic correlation:
  [Observability Standards](../observability/README.md).
- Topology, state and infrastructure operation:
  [Infrastructure Standards](../infrastructure/README.md).
- Deployment verification and rollback:
  [CI/CD Standards](../ci-cd/README.md).
- Credentials and security incidents:
  [Security Standards](../security/README.md).
- Container runtime and orchestration practices:
  [Docker Standards](../docker/README.md).
