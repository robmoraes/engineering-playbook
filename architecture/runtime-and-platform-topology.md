# Runtime and Platform Topology

Runtime architecture connects software boundaries to deployable units,
networks, ingress, secrets, storage and operator responsibilities.

## Container-First Architecture

Container-first does not mean orchestrator-first. It means each application
runtime has a repeatable, versioned artifact with configuration and state kept
outside the image.

Baseline:

- produce one immutable image per independently deployed runtime;
- inject configuration and secrets at deployment or runtime;
- expose health behavior needed for operation;
- send persistent data to an owned backing service or volume strategy;
- run with restricted privileges as defined in
  [Container Security](../security/containers-and-supply-chain.md).

```text
Good                                      Avoid
orders-api image promoted by digest      Server configured manually after deployment
DATABASE_URL injected per environment    Production database embedded in container disk
```

## Reference Runtime Topology

For a small production deployment:

```text
Public DNS
  -> reverse proxy / TLS ingress
      -> public web or API service (stateless replicas where needed)
          -> private database
          -> private cache or queue when required
      -> observability exporter/agent
CI/CD
  -> image registry
  -> orchestrator deployment API or constrained deploy identity
```

Keep edge, application and data traffic separated conceptually even when a
small installation uses one host. This makes later isolation an infrastructure
change rather than a redesign of trust relationships.

## Reverse Proxy and Ingress

A reverse proxy at the edge commonly owns:

- TLS termination and certificate renewal;
- hostname/path routing;
- public-to-private forwarding;
- request metadata and access logging;
- optional basic rate controls or authentication integration.

It should not silently accumulate application business logic.

```text
Good                                      Avoid
api.example.com -> orders-api            Proxy rewriting domain behavior for each app
grafana.ops.example.com -> private auth  Databases published for proxy convenience
```

Operational implications:

- ingress is a shared failure domain for public services behind it;
- certificate renewal and routing configuration need monitoring;
- trusted forwarding headers must be configured intentionally;
- backend networks should not expose services directly to the internet.

## Service Discovery

Use the discovery mechanism supplied by the deployment platform before adding
a separate service registry.

| Runtime | Practical discovery approach |
| --- | --- |
| Single host Compose | Service name on an isolated application network |
| Docker Swarm | Swarm service discovery and overlay networks |
| Kubernetes | Kubernetes `Service` and cluster DNS |
| External managed dependency | Configuration reference and provider endpoint |

Client behavior must still tolerate discovery changes and dependency failure:
timeouts, bounded retries and health visibility matter regardless of registry.

## Network Segmentation

Use networks to express reachability boundaries:

```text
edge-public       reverse proxy <-> internet-facing services
orders-private    API/worker <-> application dependencies
orders-data       selected services <-> database
monitoring        agents/exporters <-> observability stack
```

Rules:

- databases and queues SHOULD NOT join public ingress networks;
- only edge services SHOULD publish public ports;
- internal administration endpoints SHOULD use private access paths;
- network attachment SHOULD follow needed communication, not convenience.

For naming, see
[Runtime and Infrastructure Resources](../naming/runtime-and-infrastructure.md).

## Docker Swarm Pattern

Docker Swarm is a reasonable practical orchestrator for small platforms that
need replicated services, declarative stacks, rolling updates, overlay
networks and built-in secret delivery without the operating surface of a
larger control plane.

Recommended stack layout:

```text
edge-prod             reverse proxy and public ingress network
orders-prod           api, worker and private app resources
observability-prod    metrics, logs and dashboards
```

Architectural consequences:

- manager node availability and backup matter because managers hold cluster
  control state;
- published ports may use Swarm routing mesh across nodes;
- overlay network connectivity and firewall requirements are platform
  dependencies;
- stateful storage still needs an explicit placement, backup and failover
  strategy.

Use Swarm when its feature set meets requirements and the team can operate it.
Do not treat an orchestrator migration as automatic evidence of architecture
improvement.

## Kubernetes Pattern

Kubernetes becomes a stronger candidate when requirements include richer
workload scheduling, namespace/RBAC policy, extensive controllers, portable
platform integrations or organizational use of a Kubernetes ecosystem.

Practical boundaries:

- `Deployment`/`Service` for stateless HTTP or worker workloads;
- `Ingress` or Gateway-facing layer for public routing;
- namespaces and network policy for separation where supported;
- managed stateful dependencies unless operating state in the cluster is a
  deliberate capability.

Consequences:

- the control plane, workload policy, upgrades and observability add operating
  scope;
- Kubernetes does not automatically solve application consistency,
  reliability, data recovery or bad service boundaries;
- small workloads may be better served by simpler deployment infrastructure.

## Infrastructure Dependencies

Every topology SHOULD list its non-code dependencies:

| Dependency | Design question |
| --- | --- |
| DNS and TLS | Who owns records and renewal failure detection? |
| Registry | Can a deployment recover if the registry is temporarily unavailable? |
| Database/storage | What durability, backup and restore path exists? |
| Identity provider | What happens when authentication dependency fails? |
| Observability stack | Can service impact be detected if telemetry is degraded? |
| Orchestrator/host | What is the recovery route for control-plane or node loss? |

Infrastructure dependencies are part of application architecture because they
determine deployability, recoverability and user-facing failure.
