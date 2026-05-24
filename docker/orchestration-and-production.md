# Orchestration and Production

Production container operation combines image discipline with scheduling,
networking, secrets, state, rollout behavior and recovery. The orchestrator
does not repair an image that lacks runtime clarity.

## Production Runtime Baseline

- Deploy immutable image references and record the digest in delivery evidence.
- Supply configuration and secrets through the environment platform, not image
  layers.
- Run as non-root and restrict filesystem/capabilities where compatible.
- Define health behavior and verify the actual service route after deployment.
- Set observed resource constraints or reservations for material workloads.
- Send logs to standard streams for platform collection.
- Provide rollback or recovery handling for each production release.

## Docker Swarm Deployment Pattern

Swarm is suitable for a small platform needing declarative services, overlay
networks, secrets and rolling updates without operating Kubernetes.

```yaml
services:
  api:
    image: ghcr.io/acme/orders-api@sha256:<digest>
    networks:
      - edge_public
      - orders_data
    secrets:
      - orders-api-db-password-prod
    deploy:
      replicas: 2
      resources:
        reservations:
          memory: 128M
        limits:
          memory: 512M
      update_config:
        parallelism: 1
        order: start-first
        failure_action: rollback
      rollback_config:
        parallelism: 1
        order: stop-first

networks:
  edge_public:
    external: true
  orders_data:
    driver: overlay

secrets:
  orders-api-db-password-prod:
    external: true
```

Operational implications:

- deploy commands require manager authority and should run through constrained
  automation;
- a service granted a Swarm secret receives it at runtime, commonly under
  `/run/secrets`;
- `start-first` needs temporary capacity and two simultaneously compatible
  versions;
- volumes attached to stateful services still require placement and recovery
  planning;
- automatic service rollback does not undo database schema changes.

## Kubernetes Compatibility

An infrastructure-aware image intended for Kubernetes SHOULD:

- run correctly without assuming a stable container identity or writable root
  filesystem;
- expose separate health semantics that map cleanly to readiness, liveness and
  startup probes where applicable;
- handle termination signals and a bounded shutdown period;
- work with configuration and secrets mounted or injected by the platform;
- avoid requiring Kubernetes API access unless explicitly designed for it.

Kubernetes runtime example:

```yaml
containers:
  - name: api
    image: ghcr.io/acme/orders-api@sha256:<digest>
    ports:
      - name: http
        containerPort: 3000
    readinessProbe:
      httpGet:
        path: /ready
        port: http
    livenessProbe:
      httpGet:
        path: /live
        port: http
    resources:
      requests:
        cpu: 100m
        memory: 128Mi
      limits:
        memory: 512Mi
```

Do not make liveness depend on every downstream dependency. A database outage
should usually remove readiness or report degraded behavior, not force every
application container into restart loops.

## Init Workloads and Migrations

Use an initialization task or job when work must finish before normal service
use, such as controlled schema migration or asset preparation.

Rules:

- migrations are explicit release actions with compatibility and recovery
  analysis;
- multiple replicas must not race non-idempotent migrations;
- startup containers are not a substitute for deployment coordination;
- failure should block unsafe rollout rather than silently continue.

```text
Good                                      Avoid
One controlled migration job per release Every app replica applies destructive migration at boot
```

In Compose or Swarm deployments, model migrations as a clearly invoked
one-off deployment task or pipeline step rather than embedding them invisibly
in an entrypoint.

## Sidecars

Sidecars are appropriate when supporting functionality shares lifecycle or
local communication needs with the application, for example a service proxy or
specialized log/telemetry adapter in a platform that uses that model.

Tradeoffs:

- every sidecar consumes resources and requires version/security lifecycle;
- co-located failure or startup behavior can affect the application;
- platform-native log collection may remove the need for a per-application log
  sidecar.

For Docker Compose or Swarm, model auxiliary processes as separate services
unless they truly share a unit lifecycle. For Kubernetes, use sidecars when
the Pod-level coupling is intentional and resource/probe behavior is defined.

## Debug and Diagnostic Operation

Production images SHOULD remain lean. Diagnostics can use:

- platform logs, metrics and traces;
- `docker service ps`, `docker service logs` or container inspect tools in
  authorized environments;
- separate debug target images built from the same source;
- Kubernetes ephemeral/debug container mechanisms when the platform uses them.

Never perform an emergency manual modification inside a production container
and then treat that mutated instance as the deployed fix. Build and deploy a
new recorded artifact after diagnosis.

## Lifecycle Management

Container operations should include:

| Lifecycle event | Required practice |
| --- | --- |
| Build | Trace source and dependencies; exclude secrets |
| Publish | Store immutable tag/digest and scan/provenance evidence as appropriate |
| Deploy | Supply scoped configuration/secrets and verify service behavior |
| Operate | Observe logs, health and resource usage |
| Patch | Rebuild and redeploy images when runtime/base dependencies change |
| Retire | Remove unused services, secrets, networks and expired artifacts safely |
| Recover | Roll back artifact or restore state according to documented failure mode |
