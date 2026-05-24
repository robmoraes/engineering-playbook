# Topology and Environments

Infrastructure topology should describe traffic paths, placement, state,
administrative authority and failure domains. A diagram that only names
products is insufficient for operation.

## Reference Small Production Topology

```text
Internet
  -> DNS / TLS endpoint
  -> reverse proxy or managed load balancer             [edge]
       -> web/api replicas                              [runtime-private]
            -> managed database or owned data service   [data-private]
            -> object/storage dependency                [data-private]

CI/CD -> image registry -> constrained deploy identity -> runtime control API
Operators -> protected management path -> runtime/data diagnosis
Services -> metrics/logs/traces -> observability and alert routing
Backups -> protected backup destination -> restore procedure/test evidence
```

This topology is practical for an independently operated service. It does not
claim host or zone failure tolerance unless placement, data service behavior
and ingress availability provide it.

## Environment Strategy

| Environment | Purpose | Isolation expectation |
| --- | --- | --- |
| Local/lab | Development and experimentation | Disposable state; non-production credentials only |
| Development/shared test | Integration work | No production secrets or unsanitized production data |
| Staging | Deployment and operational validation | Production-like routes/config shape with isolated credentials/state |
| Production | User-facing or durable workload | Restricted authority, backup/recovery, monitoring and controlled change |

Rules:

- Artifacts MAY be promoted between environments; secrets, live state and
  privileged credentials MUST NOT be promoted with them.
- Production SHOULD have a separate account, project, cluster or similarly
  strong authority boundary when the workload has meaningful impact.
- Staging is useful only when it validates a production-relevant behavior.
  Avoid paying for an idle replica of production merely for appearances.

```text
Good                                      Avoid
Same image digest in stg and prod        Building a special production image on host
Separate prod secret store/access        Dev runner with production admin token
```

## Edge Versus Core

| Layer | Contains | Exposure |
| --- | --- | --- |
| Edge | DNS, TLS, reverse proxy, public load balancing | Internet-facing by purpose |
| Application core | API, workers, private internal endpoints | Accessible only through required paths |
| Data core | Databases, caches requiring protection, storage | Private and tightly scoped |
| Management core | control plane, state backend, admin access | Restricted operator/automation paths |
| Observability core | telemetry collection/storage/dashboards | Private or authenticated exposure |

Do not publish a database, cluster API or monitoring administrator interface
because it is quicker than building an appropriate management route.

## Shared Platform Services

| Service | Shared benefit | Failure implication |
| --- | --- | --- |
| Reverse proxy/ingress | Central TLS/routing | Edge outage can affect many services |
| Registry | Consistent artifact distribution | New deploys/recovery may stall when unavailable |
| Secrets store | Controlled runtime credentials | Workloads or rotations may fail when unavailable |
| Observability stack | Shared operational visibility | Failure can hide incidents |
| CI runners/deployment controller | Standard change route | Delivery is blocked or becomes manual |

Shared services SHOULD document consumers, availability expectations,
administrative access, backup/rebuild route and maintenance impact.

## Topology Documentation Standard

Each production topology SHOULD show:

- external and administrative entry points;
- environments, region/site and failure-domain placement;
- networks and permitted service-to-service paths;
- stateful dependencies and data ownership;
- deployment and registry path;
- secret distribution approach;
- telemetry and alert route;
- backup and disaster recovery boundary;
- known single points of failure and accepted constraints.

Use sanitized diagrams in public portfolio material. Replace real account IDs,
private endpoints and operator access details with realistic placeholders.
