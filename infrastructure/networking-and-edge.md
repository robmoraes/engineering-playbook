# Networking and Edge

Network topology should express which systems may communicate and why. A
working connection is not evidence that exposure is safe.

## Network Segmentation

Recommended logical segments:

```text
edge-public-prod       ingress <-> public application routes
orders-private-prod    application internal communication
orders-data-prod       explicitly allowed clients <-> database
observability-prod     agents/exporters <-> telemetry services
management-prod        operator/automation <-> infrastructure control paths
```

| Rule | Rationale |
| --- | --- |
| Publish public ports only from edge-facing components | Reduces accidental exposure and simplifies audit |
| Keep data stores off public/edge networks | Limits access paths and blast radius |
| Restrict management endpoints to protected routes | Control-plane access is production authority |
| Attach workloads only to required networks | Prevents convenience-driven lateral access |
| Document firewall/security group intent | Operators need to know why traffic is permitted |

Follow naming conventions in
[Runtime and Infrastructure Resources](../naming/runtime-and-infrastructure.md).

## Reverse Proxy and Load Balancing

An edge proxy or load balancer commonly owns:

- TLS termination and renewal visibility;
- hostname or path routing;
- health-aware backend forwarding where supported;
- trusted forwarding-header configuration;
- access logs and edge-level request metrics;
- optional rate limiting, authentication integration or WAF controls where
  justified.

It should not become an undocumented implementation of business behavior.

```text
Good                                      Avoid
api.example.com -> private api service   Database port open via public load balancer
TLS renewal alert owned by platform      Certificate expiry found by users
Authenticated operations route           Public Grafana admin endpoint by default
```

### Load Balancing Tradeoffs

| Approach | Appropriate for | Consequence |
| --- | --- | --- |
| Single reverse proxy host | Lab or cost-sensitive small service | Simple and cheap; edge host is a single point of failure |
| Managed load balancer across instances/zones | User-facing production requiring edge resilience | Ongoing cost and provider dependency |
| Orchestrator routing mesh/ingress | Cluster services with understood network model | Debugging must account for routing abstraction |

## Docker Swarm Networking

Swarm distinguishes management traffic from application data traffic. Docker
documents encrypted control/management plane traffic and overlay networks for
service communication; application overlay encryption and network design still
require intentional configuration and validation.

Practical pattern:

```text
external client -> edge/load balancer -> proxy service on edge overlay
proxy service -> api service on private application overlay
api service -> database endpoint on data boundary only
```

Operational checks:

- required Swarm node-to-node firewall paths are intentionally permitted;
- shared ingress and private application overlays are separate;
- services do not join unrelated overlays merely for discovery convenience;
- routing mesh versus host-mode published ports is a deliberate choice;
- network behavior is included in incident diagnosis.

## Kubernetes Networking Considerations

Kubernetes `Service` objects provide stable access to changing Pods and
support the platform discovery model. Production network isolation still
depends on ingress/gateway configuration, cluster networking and enforced
network policy where the platform supports it.

Use Kubernetes when its networking and policy model is part of an operated
platform capability, not because a small service needs one public route.

## Service Discovery

Prefer platform-provided discovery:

| Runtime | Discovery mechanism |
| --- | --- |
| Small single-host deployment | Explicit private endpoint/service name |
| Docker Swarm | Service DNS and overlay network |
| Kubernetes | `Service` and cluster DNS |
| Managed data dependency | Provider endpoint supplied through configuration |

Discovery does not remove distributed failure. Clients still need timeouts,
bounded retries where safe and visibility into dependency failures.

## Cross-Zone and External Traffic

High availability commonly adds cross-zone traffic. In AWS and similar cloud
models, traffic architecture may create measurable transfer charges as well
as latency and dependency paths.

Review:

- which requests or replication paths cross availability zones;
- whether NAT gateways, load balancing or storage access cause avoidable
  cross-zone cost;
- whether cost reduction would compromise the selected failure-domain model;
- telemetry needed to verify traffic assumptions.

Do not collapse resilient placement into a single failure domain solely to
remove transfer charges without explicitly accepting the reliability change.
