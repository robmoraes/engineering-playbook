# Operational Scenarios

Rehearsable examples for investigation, mitigation and recovery. These
scenarios apply [Operational Runbooks](../../runbooks/README.md) and
[Observability Standards](../../observability/README.md).

## Planned Scenario Families

| Directory | Purpose |
| --- | --- |
| [deployment-and-rollback](./deployment-and-rollback/) | Failed rollout, health verification and safe rollback |
| [runtime-and-platform](./runtime-and-platform/) | Containers, Swarm, resource exhaustion and future Kubernetes operation |
| [network-and-tls](./network-and-tls/) | DNS, certificate, reverse proxy and connectivity diagnostics |
| [data-and-recovery](./data-and-recovery/) | Storage, database, backups and restore verification |
| [security-incidents](./security-incidents/) | Credential exposure and trusted artifact restoration |

## Scenario Contract

Each scenario must include:

- symptom and environment assumptions;
- initial read-only diagnostics;
- expected observations;
- action authority and risk;
- mitigation or recovery procedure;
- validation and escalation criteria;
- evidence that should be preserved;
- relevant runbook and standards links.

Do not include commands that mutate production without surrounding safety,
scope and recovery context.
