# Observability and Operations

Infrastructure operation requires enough telemetry and access to distinguish
application failure from network, node, storage, control-plane or provider
failure. Collecting signals without an operator decision path is not
operability.

## Infrastructure Observability Baseline

| Signal | Infrastructure questions it answers |
| --- | --- |
| Metrics | Is capacity, availability, latency or resource health degrading? |
| Logs | What changed, failed authentication, restarted or rejected traffic? |
| Traces/service telemetry | Is infrastructure behavior contributing to request impact? |
| Events/change records | Did a deploy, scaling event, node action or provider event precede failure? |
| Synthetic/health checks | Can users or dependent systems reach the intended route? |

Minimum production coverage:

- public endpoint/TLS and ingress health;
- node or runtime capacity and availability;
- orchestrator/control-plane state where operated;
- storage/database availability and backup execution;
- network/load balancer error behavior;
- registry and deployment-path failure where it affects recovery;
- privileged access and material infrastructure changes;
- cost/budget signals for cloud infrastructure.

## Monitoring and Alerting

Alert on operator-actionable impact or urgent risk. Keep informational signals
in dashboards or tickets unless an immediate human response changes outcome.

```text
Good                                      Avoid
Page on public route unavailable         Page on every container restart
Alert on failed backup/restore test      Assume backup success forever
Alert on expiring edge certificate       Wait for TLS user outage
Ticket on capacity trend                 Page on normal CPU fluctuation
```

For each page-level alert, document:

- user or recovery risk represented;
- initial verification command/dashboard;
- immediate containment or escalation step;
- dependency and owner;
- conditions for resolving the alert.

## Logging Infrastructure

Infrastructure logs SHOULD make change and failure diagnosable while
protecting sensitive material:

- collect ingress, runtime/orchestrator and privileged administrative events
  according to operational need;
- maintain consistent environment/system identifiers;
- avoid logging credentials, secret values or sensitive request bodies;
- define retention based on investigation need and cost;
- restrict access to logs that expose internal topology or user data.

Use the logging and label conventions in the naming standards rather than
inventing one identifier shape per platform.

## Operational Access

Administrative access is part of infrastructure architecture:

| Context | Practical access approach |
| --- | --- |
| Personal lab | Named key/account, protected secret storage and no unnecessary public admin ports |
| Small production | Individual identities, MFA where supported, restricted SSH/VPN/bastion or managed session path |
| Platform/enterprise | Segmented roles, short-lived or audited privileged access and break-glass procedure |

Routine deployment SHOULD use scoped automation rather than general operator
SSH. Emergency manual access must be reconciled with intended configuration
after stabilization.

See [Security: Identity and Access](../security/identity-and-access.md).

## Runbook Standard

A runbook is needed for failures that require operator judgment or privileged
action:

```text
Scenario:
User/operational impact:
Detection signal:
Required access:
Safety checks:
Diagnosis steps:
Containment/recovery steps:
Verification:
Rollback/escalation:
Evidence to retain:
```

Core infrastructure runbooks commonly cover:

- ingress/TLS failure;
- node loss or capacity exhaustion;
- orchestrator control-plane/quorum failure;
- failed deployment or registry unavailable;
- storage/database outage and restore;
- backup failure;
- expired/revoked infrastructure credential;
- observability outage.

## Troubleshooting Pattern

Use a layered investigation order to avoid random production changes:

1. Confirm user-facing symptom and scope.
2. Correlate recent deploys, configuration changes or provider events.
3. Inspect edge route, TLS, DNS and load-balancer state.
4. Inspect workload scheduling/health and node capacity.
5. Inspect internal network/discovery and downstream stateful dependencies.
6. Inspect credentials, quotas and external provider failures.
7. Recover through documented action; record evidence and reconcile drift.

```text
Good                                      Avoid
Confirm failure before failover          Restart random nodes until symptom changes
Preserve logs/events before mutation     Erase diagnostic evidence during incident
```

## Incident Learning

After a material infrastructure incident, record:

- impact and duration;
- triggering failure and contributing topology decisions;
- what detected the failure and what did not;
- recovery actions and whether runbooks were accurate;
- follow-up improvements to design, monitoring, access or recovery;
- accepted remaining risk and owner.

The purpose is to improve the operating system, not to create paperwork for
minor transient noise.
