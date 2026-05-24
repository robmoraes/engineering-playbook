# Platform and Runtime Monitoring

Operational visibility must cover both the behavior users depend on and the
runtime layers that explain failure. Container orchestration changes which
infrastructure signals matter; it does not remove application instrumentation.

## Application Telemetry

Each production service SHOULD expose signals for:

- critical request or job outcomes;
- latency or completion delay;
- dependency failures and bounded timeout behavior;
- running version and environment;
- queue backlog/failures for asynchronous work;
- health behavior needed for delivery and operation.

Do not expose sensitive domain values or high-cardinality identities merely
because a library makes it easy to attach tags.

## Healthchecks

| Check | Purpose | Failure consequence |
| --- | --- | --- |
| Liveness/process health | Detect unrecoverable local process failure | May trigger restart |
| Readiness/traffic eligibility | Decide if instance should receive traffic | Remove from routing/rollout |
| External/synthetic check | Test user-relevant route | Alert and confirm impact |
| Deep diagnostic check | Explain dependency health | Used for diagnosis, not frequent restarts |

```text
Good                                      Avoid
Readiness reports ability to serve       Liveness fails whenever database is briefly slow
External check tests TLS/routing path     Container running treated as user success
```

Healthchecks should not leak dependency credentials, topology or sensitive
debug content.

## Host and Container Visibility

For host-based or containerized runtimes, capture:

- CPU, memory, filesystem and network saturation;
- host availability and time synchronization issues where relevant;
- container resource use and restart/exit behavior;
- runtime/image version and placement identity;
- disk pressure for state, logs and telemetry itself.

`node_exporter` is a common Prometheus exporter for host metrics. cAdvisor can
expose container resource metrics in Docker-based environments. Deploy them
only with controlled exposure: metric endpoints can reveal valuable internal
inventory and capacity information.

## Docker Swarm Visibility

For a Swarm environment, operational views SHOULD include:

- manager quorum and node availability;
- service desired versus running task state;
- update/rollback failures and deployed image identity;
- task placement and resource pressure;
- ingress/overlay connectivity symptoms;
- Swarm secret/access failures without secret values;
- stateful service placement and backup status.

Example diagnostic path:

```text
API route failing
  -> public probe/error-rate dashboard
  -> service task/update state and running digest
  -> affected node/container resources and logs
  -> overlay/dependency/storage checks
```

A task restart signal helps diagnosis; it should not automatically page when
replication absorbs it and users are unaffected.

## Kubernetes Considerations

When operating Kubernetes, provide visibility into:

- workload rollout, Pod readiness/restarts and resource constraints;
- node availability/capacity and scheduling failures;
- ingress/gateway and `Service` path behavior;
- persistent volume/storage and stateful dependencies;
- cluster/control-plane or managed-service signals available to operators;
- namespace/RBAC/audit-relevant events according to security requirements.

Use stable workload identity rather than ephemeral Pod names as the principal
dashboard grouping. Preserve Pod/instance identity for drill-down.

## Shared Platform Telemetry

Shared systems need their own visibility because they may hide or amplify
outages across applications:

| Platform dependency | Signals |
| --- | --- |
| Reverse proxy/edge | TLS validity, route availability, backend failures and latency |
| Image registry | publish/pull/deploy failure affecting release or recovery |
| Secrets delivery | access/rotation failures without values |
| CI/CD/deployer | failed production actions and verification outcome |
| Telemetry pipeline | ingestion/export failures, lag, dropped data and storage pressure |
| Backup service | job success and restore validation |

See [Infrastructure: Observability and Operations](../infrastructure/observability-and-operations.md)
for infrastructure ownership and runbook expectations.
