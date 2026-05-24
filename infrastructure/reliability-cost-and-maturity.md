# Reliability, Cost and Maturity

Infrastructure maturity is not measured by the number of technologies in use.
It is measured by whether risk, reliability, recovery, cost and ownership are
understood for the system being operated.

## Failure Domains

| Failure domain | Example failure | Mitigation option | Remaining tradeoff |
| --- | --- | --- | --- |
| Process/container | Runtime crash | Health check and restart/replica | Dependency or bad release may affect every replica |
| Host/node | VM or disk loss | Multiple nodes or fast replacement | State and capacity still require design |
| Availability zone/site | Zonal networking/power disruption | Multi-zone placement and data failover | Cost and cross-zone dependencies |
| Control plane | Swarm manager quorum or cluster API failure | Redundant/managed control plane and recovery | Operator burden/provider dependency |
| Storage/data | Volume/database corruption/deletion | Backup, replication and tested restore | RPO/RTO and expense |
| Provider/region | Broad service disruption | Cross-region strategy where justified | Significant complexity and cost |
| Human/change | Bad deploy/IaC/credential change | Review, staged rollout, rollback and protected authority | Slower or more controlled changes |

## High Availability Decision

Use HA for a stated requirement:

| Design | Addresses | Does not address | Cost/complexity |
| --- | --- | --- | --- |
| Two application replicas on one host | Process/container failure | Host or zone failure | Low |
| Replicas across nodes | Node failure | Shared storage/control-plane/zone failure | Moderate |
| Multi-zone stateless runtime plus managed Multi-AZ data | Selected zonal/component failure | Bad data change or regional outage | Higher recurring cost |
| Cross-region recovery/active topology | Broader regional disruption | All operator/application errors | Highest operational burden |

```text
Good                                      Avoid
Accept single edge host with restore     Call it highly available because it uses containers
Pay for Multi-AZ due to service target   Add replicas without knowing failure domain
```

## Availability and Recovery Questions

Before adding redundancy, answer:

```text
Which user-visible behavior needs protection?
What outage/data-loss tolerance is acceptable?
Which failure domain is addressed?
How is failover or restore tested?
Can operators diagnose failure during the incident?
What recurring and operational cost is introduced?
What failure remains accepted?
```

AWS Well-Architected guidance is used here as a reference for fault isolation,
backups, recovery testing and workload availability decisions. It is not a
requirement to deploy every workload with AWS or across multiple zones.

## Cost-Aware Infrastructure

Cost review is part of architecture, not an afterthought:

- size compute and storage based on observed use, not hopeful growth;
- remove abandoned resources, snapshots, registries and environments;
- monitor data transfer, especially cross-zone paths and egress;
- compare managed-service cost with patching, backup and incident ownership;
- select HA only where reduced interruption justifies its cost;
- maintain budget visibility for portfolio and production workloads.

| Choice | Lower initial cost | Operational consequence |
| --- | --- | --- |
| One host and local volumes | Yes | Host/state recovery is owner responsibility |
| Managed database | Usually no | Reduced database operating burden; provider dependency |
| Multi-zone runtime/data | No | Better selected fault isolation; transfer/duplication cost |
| Self-hosted observability stack | Sometimes | Storage, upgrades and outage visibility become owned work |

## Maturity Levels

| Level | Suitable context | Expected capability |
| --- | --- | --- |
| 0 - Lab | Disposable learning | Document purpose, exposure and rebuild route; no production claims |
| 1 - Maintained hosted project | Portfolio or low-impact service | Versioned deployment, protected secrets, useful logs/health and valuable-data backup |
| 2 - Small production | Live service with operational responsibility | Environment boundary, controlled changes, alerting, restore procedure/test and owner |
| 3 - Resilient production | Material availability/data needs | Failure-domain design, capacity/HA decision, tested recovery and incident learning |
| 4 - Shared platform | Multiple consuming systems | Governance, reusable controls, dependency contracts, lifecycle and audited authority where justified |

Move upward because impact or scale requires it. A well-operated Level 2
system is preferable to a complex Level 4 imitation without staffing,
telemetry or recovery competence.

## Examples by Context

### Personal Lab

```text
One VM -> Docker Compose -> disposable services
Safe test credentials; no public admin ports; rebuild notes
```

### Cost-Sensitive Production

```text
DNS/TLS -> single proxy/runtime host -> managed database
Immutable deploy, backup/restore procedure, endpoint monitoring
Accepted single runtime-host outage documented
```

### Higher-Availability Production

```text
Managed load balancer across zones
  -> stateless application nodes/cluster workloads across zones
  -> managed Multi-AZ state where required
Protected backups, observability, controlled deploy and tested recovery
```
