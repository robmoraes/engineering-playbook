# Storage, Backup and Recovery

Durable state is where infrastructure claims become testable. Replicas and
containers do not remove data ownership, consistency or restore obligations.

## Stateful Versus Stateless Infrastructure

| Workload | Default infrastructure treatment |
| --- | --- |
| Stateless web/API/worker | Replaceable runtime replicas using external configuration and state |
| Cache | Disposable only if loss and refill impact are acceptable |
| Database | Durable storage, backup, recovery and access control explicitly owned |
| Uploaded objects/assets | Durable object/file storage with retention and restore decision |
| Metrics/logs | Retention and failure impact selected according to operational need |
| Cluster/IaC state | Protected control state with recovery and access strategy |

```text
Good                                      Avoid
App replica replaced from image          Customer uploads on container layer
Database restore tested                  "Volume exists" treated as backup
```

## Storage Selection

| Storage approach | Use when | Tradeoff |
| --- | --- | --- |
| Local named volume | Development, labs or accepted single-host state | Low complexity; host loss affects data/availability |
| Attached block volume | One active writer with defined replacement/backup path | Node/zone attachment and failover constraints |
| Shared NFS/EFS-style filesystem | Multiple clients need shared POSIX-like files | Network dependency, latency/throughput and application locking behavior |
| Object storage | Uploads, artifacts, backups or immutable assets fit object access | Application must use object semantics |
| Managed database/storage service | Durable production data merits reduced operational burden | Provider cost and service constraints |

### Shared Storage and EFS/NFS Considerations

Shared filesystems may simplify multi-node access, but they do not solve
application consistency or performance automatically.

Before adopting shared file storage, confirm:

- whether concurrent writers are supported by the application;
- latency and throughput expectations under failure or scale;
- mount behavior and recovery when network/storage service degrades;
- backup/snapshot and restore capability;
- zone/region placement and data-transfer cost;
- permissions and secret exposure on mounted paths.

Use object storage for object-shaped data rather than creating a shared
filesystem only to preserve an older local-disk assumption.

## Stateful Orchestration

In Swarm or Kubernetes, a scheduler can move a workload only if its data can
move or be reached safely.

```text
Good                                      Avoid
DB managed outside cluster               DB service replicated over local volumes
Stateful node affinity documented        Replica count increased without consistency design
Volume restore/runbook tested            Stateful failover assumed from scheduler alone
```

If operating a stateful service inside an orchestrator, document storage
attachment, placement, failover semantics, patching, backup and restore
ownership before production use.

## Backup Standard

For every valuable production dataset, record:

```text
Data owner:
Backup source and mechanism:
Destination and access boundary:
Encryption/protection:
Retention:
Recovery point expectation (RPO):
Recovery time expectation (RTO):
Restore procedure:
Restore verification date/result:
Compatible application/schema version:
```

Baseline requirements:

- identify data requiring backup or explicitly document that it is
  reproducible/disposable;
- protect backup access separately from routine workload access;
- automate backups where data is persistent and material;
- test restoration, since a successful backup job does not prove recoverable
  data;
- retain enough configuration and artifact information to run restored state.

## Disaster Recovery

Disaster recovery should be selected against impact, not added by slogan.

| Context | Practical recovery expectation |
| --- | --- |
| Lab | Rebuild instructions; backup only if learning data matters |
| Portfolio app with durable user data | Automated backup and documented restore; accepted downtime stated |
| Small production | RPO/RTO decision, protected backups and restore test cadence |
| Critical/HA system | Failure-domain strategy, recovery automation where warranted and regular validation |

Recovery scenarios to document:

- application host or node replacement;
- database/storage corruption or loss;
- cluster manager/control-plane loss;
- secret or access failure;
- infrastructure configuration/state loss;
- regional/provider service disruption if the system claims that resilience.

## Backup Versus High Availability

High availability reduces interruption from selected failures. Backup and
recovery protect against data loss, corruption, destructive change or longer
outage. Production data generally needs both questions answered separately.

```text
Replicated database without backup       survives some node failure, not deletion
Nightly backup without failover          recovers data, but accepts outage
Multi-AZ with verified restore           addresses availability and recoverability at higher cost
```
