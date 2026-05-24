# References

This section uses official reliability, operations and platform documentation
to establish safe operational practices. Severity labels, document layout,
example commands and lightweight workflows are local conventions adapted for
this playbook.

## Adopted and Adapted Guidance

| Source | Source guidance used | Convention adopted here |
| --- | --- | --- |
| Google, *Site Reliability Engineering - Managing Incidents* | Effective incident management limits disruption, restores operation and maintains documentation for analysis and handoff. | Material incidents maintain coordination, timeline, communication and verified recovery proportional to scale. |
| Google, *Site Reliability Engineering - Effective Troubleshooting* | Troubleshooting depends on systematic reasoning and system knowledge rather than random action. | Procedures investigate outside-in, record hypotheses and gather evidence before mutation where safe. |
| Google, *Site Reliability Engineering - Postmortem Culture: Learning from Failure* | Postmortems document incidents, understand contributing causes and drive effective preventive actions without blame. | Serious or repeating incidents create concise blameless reviews with owned corrective actions and runbook updates. |
| AWS Well-Architected Framework, *Operational Excellence - Operate* and *Use runbooks to perform procedures* | Operational events need owned response processes; runbooks are step-by-step guides with tools, permissions, exceptions, escalation and validation, maintained centrally and automated over time where beneficial. | Runbooks are stored as versioned documents, identify access and verification, and prioritize automation for safe repeatable actions. |
| AWS Well-Architected Framework, *Operational Readiness Review* | Operational readiness reviews validate that workloads can be operated safely and evolve from incident learning. | Production readiness checklist covers ownership, recovery, monitoring, access and review after material change. |
| Docker Docs, *Administer and maintain a swarm*, *Deploy services to a swarm* and `docker service` CLI | Swarm managers hold control state/quorum; service status/logs support diagnosis; service changes support controlled rollback from manager authority. | Swarm procedures treat manager access and quorum recovery as privileged, and use service rollback only after compatibility checks. |
| Kubernetes Docs, *Troubleshooting Applications*, *Debug Services*, *Troubleshooting Clusters* and `kubectl rollout` | Kubernetes diagnosis checks application resources, Services, Pods, nodes/events and rollout state; rollbacks and cluster actions alter runtime state. | Kubernetes commands are documented as optional runtime-specific procedures with read-only diagnosis before mutation. |
| Security and observability standards in this repository | Security containment and telemetry correlation are already defined as operational contracts. | Runbooks reference rather than duplicate secret handling and telemetry naming requirements. |

## Source Links

- Google SRE, *Managing Incidents*:
  <https://sre.google/sre-book/managing-incidents/>
- Google SRE, *Effective Troubleshooting*:
  <https://sre.google/sre-book/effective-troubleshooting/>
- Google SRE, *Postmortem Culture: Learning from Failure*:
  <https://sre.google/sre-book/postmortem-culture/>
- AWS Well-Architected, *Operate - Operational Excellence Pillar*:
  <https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/operate.html>
- AWS Well-Architected, *Use runbooks to perform procedures*:
  <https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_ready_to_support_use_runbooks.html>
- AWS Well-Architected, *Ensure a consistent review of operational readiness*:
  <https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_ready_to_support_const_orr.html>
- Docker Docs, *Administer and maintain a swarm of Docker Engines*:
  <https://docs.docker.com/engine/swarm/admin_guide/>
- Docker Docs, *Deploy services to a swarm*:
  <https://docs.docker.com/engine/swarm/services/>
- Docker Docs, `docker service` CLI:
  <https://docs.docker.com/reference/cli/docker/service/>
- Kubernetes Docs, *Troubleshooting Applications*:
  <https://kubernetes.io/docs/tasks/debug/debug-application/>
- Kubernetes Docs, *Debug Services*:
  <https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/>
- Kubernetes Docs, *Troubleshooting Clusters*:
  <https://kubernetes.io/docs/tasks/debug/debug-cluster/>
- Kubernetes Docs, `kubectl rollout`:
  <https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/>

## Local Conventions

- The four-level severity scheme is designed for this playbook and should be
  mapped to any existing organizational incident policy.
- Command examples favor read-only diagnosis and do not authorize access or
  production mutation by themselves.
- A small service may combine response roles while retaining timeline,
  verification and follow-up discipline.
- Automation is preferred for validated repeatable procedures, not for
  ambiguous or destructive intervention without guardrails.
