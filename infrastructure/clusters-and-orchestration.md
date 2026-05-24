# Clusters and Orchestration

An orchestrator provides placement and reconciliation capabilities. It also
creates a control plane, upgrade path, access boundary and recovery burden.
Select it for operational requirements rather than portfolio appearance.

## Selection Guide

| Situation | Practical approach |
| --- | --- |
| Local development or one disposable service | Docker Compose or provider-native runtime |
| Small multi-service production needing replicas/rolling update/overlay networks | Docker Swarm can be appropriate when its recovery model is operated |
| Platform requiring policy ecosystem, richer scheduling/controllers or established Kubernetes capability | Kubernetes or a managed Kubernetes service |
| Durable database requirement only | A managed data service may be more useful than adding an orchestrator |

## Docker Swarm Infrastructure Pattern

Swarm provides declarative services, manager reconciliation, service
discovery, overlay networking, secrets and rolling updates through Docker
Engine.

Example small production topology:

```text
Public ingress/load balancer
  -> worker nodes running replicated edge/application services

Manager nodes                    Worker nodes
  manager-01  manager-02          worker-01  worker-02
  manager-03                      worker-03

External durable database or explicitly operated stateful placement
Protected registry, backup and observability dependencies
```

### Manager and Quorum Rules

- A single-manager swarm is acceptable only where losing deployment/control
  operations until recovery is an accepted constraint.
- Production requiring control-plane availability SHOULD use an odd number of
  managers, commonly three, spread across the selected fault domains.
- Manager nodes hold swarm state and MUST have controlled access and backup/
  recovery procedures.
- Do not add managers casually: quorum and network reliability matter more
  than raw manager count.

Docker documents that services on a failed worker can be rescheduled, while a
loss of manager quorum prevents management operations. Running tasks may
continue, but the platform cannot safely reconcile normal change.

### Node Placement

Use node labels and placement constraints for intentional requirements:

```text
node.labels.role=edge
node.labels.storage=orders-primary
node.labels.zone=az-a
```

```text
Good                                      Avoid
Proxy on edge-labelled nodes             Every service pinned to manager-01
Stateful placement documented            Volume assumed portable across hosts
Replica spread verified                  Three tasks all in one failure domain
```

## Kubernetes Considerations

Kubernetes clusters consist of a control plane and worker nodes. Kubernetes
documentation describes production clusters as commonly using multiple
control-plane computers and multiple nodes for fault tolerance and high
availability.

Adopt Kubernetes when the operating model can own:

- cluster/control-plane availability or managed service dependency;
- node pools, upgrades and workload scheduling;
- RBAC, namespaces, secrets and network controls;
- persistent volume/storage class behavior;
- monitoring of cluster and workload layers;
- rollout and recovery behavior.

Kubernetes is not itself a backup strategy, application resilience design or
cost optimization plan.

## Node Lifecycle

For any multi-node runtime:

- inventory role, zone/site, capacity, operating system/runtime version and
  patch status;
- avoid naming nodes after current workloads;
- drain/remove or safely relocate workloads before disruptive maintenance;
- verify scheduling capacity before node replacement;
- rotate credentials or join tokens according to platform risk;
- remove retired node identity and stale access.

For naming, see
[Runtime and Infrastructure Resources](../naming/runtime-and-infrastructure.md).

## Cluster Lifecycle

| Event | Required consideration |
| --- | --- |
| Bootstrap | Secure initial authority, networking, registry access, secrets and backup source |
| Scale out | Capacity, placement, overlay/network routes, monitoring and cost |
| Upgrade | Compatibility, drain/rollout plan, control-plane availability and rollback/recovery |
| Node failure | Workload rescheduling, state attachment and operator alerting |
| Control-plane failure | Quorum/restore or provider recovery procedure |
| Retirement | Workload/state migration, secret/access revocation and retained evidence |

## Common Operational Failures

| Symptom | Investigation path |
| --- | --- |
| Service cannot deploy | Registry access, deploy authority, scheduling capacity, node health |
| Replica unavailable | Task/Pod events, health, resource constraint, node/network failure |
| Cross-node communication fails | Firewall, overlay/CNI health, service attachment and DNS discovery |
| Stateful service does not move | Volume/node affinity and recovery design |
| Cluster cannot accept changes | Manager/control-plane health and quorum/provider status |
