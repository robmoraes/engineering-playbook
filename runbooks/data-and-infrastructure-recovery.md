# Data and Infrastructure Recovery

Stateful and infrastructure recovery procedures carry higher risk than
application restart or image rollback. Stop and escalate when the data version,
recovery target or destructive consequence is unclear.

## Database Operational Checks

Use when service symptoms suggest database connectivity, latency, storage,
migration or availability failure.

### Initial Assessment

- confirm affected service/environment and user impact;
- inspect application errors without printing credentials;
- identify database owner/service and current migration/release context;
- review database availability, connections, latency, storage and backup
  status through approved monitoring/provider tools;
- determine whether failure is access, capacity, query, schema, storage or
  provider availability.

```text
Good                                      Avoid
Inspect connection failure classification Paste DATABASE_URL into incident chat
Check migration record before rollback    Restore database because API logs are vague
```

### Recovery Decisions

| Failure | Possible response | Caution |
| --- | --- | --- |
| App regression, database healthy | Roll back compatible application | Check schema compatibility |
| Exhausted connection/resource limit | Reduce trigger/repair capacity safely | Scaling clients can worsen load |
| Credential/reference invalid | Restore intended secret/reference | Treat exposure separately |
| Failed compatible migration | Apply defined migration recovery | Preserve evidence and state |
| Corruption/data loss | Invoke restore/DR owner | Do not improvise destructive commands |

## Storage and Disk Exhaustion

1. Confirm affected filesystem/volume and which workload owns it.
2. Identify consumption class: logs, images, backups, database, uploads or
   unknown data.
3. Protect durable/stateful data before deletion.
4. Apply documented retention/cleanup or add controlled capacity.
5. Verify workload writes, backup behavior and alerts.

Read-only host checks:

```bash
df -h
df -i
docker system df
```

Avoid deleting Docker volumes, database files, snapshots or logs needed for
active incident analysis without owner approval and recovery understanding.

## Backup Restore Procedure Contract

Every restore-capable system SHOULD maintain:

```text
Dataset:
Environment:
Data owner:
Backup location/protection:
Selected recovery point:
Expected data loss window (RPO):
Expected service restoration window (RTO):
Compatible application/schema version:
Restore authority:
Pre-restore backup/evidence:
Validation query or application smoke:
```

### Restore Workflow

1. Confirm restore is required and identify accepted data-loss impact.
2. Select the correct backup and target environment.
3. Preserve current failure evidence and existing state where feasible.
4. Restrict writes or traffic if continuing writes would invalidate recovery.
5. Execute the approved restore procedure using protected authority.
6. Deploy or select compatible application/schema state.
7. Validate data integrity and user-facing operation.
8. Record recovered point, residual loss, duration and follow-up.

Backups are not trusted solely because jobs reported success; restore
validation must be practiced before a real incident where possible.

## Host or Node Recovery

For replaceable stateless nodes:

- identify affected workloads and whether capacity remains adequate;
- remove/drain unhealthy scheduling target through platform procedure;
- reprovision from defined configuration rather than hand-repairing drift;
- confirm workloads reschedule and user route recovers;
- review why node failure was detected and whether replacement was safe.

For state-attached nodes, do not replace or detach storage until placement,
attachment and recovery semantics are understood.

## Control Plane and Cluster Recovery

Loss of Swarm manager quorum or Kubernetes control-plane capability is an
infrastructure incident:

- confirm whether data plane workloads continue serving;
- freeze routine deploy/change operations;
- preserve cluster/control-plane status and backup evidence;
- engage the infrastructure owner;
- follow platform-specific recovery steps and backup requirements;
- verify scheduling/change capability plus user-facing workloads after
  restoration.

Do not rebuild a production cluster casually because application service status
is unclear.

## Disaster Recovery Escalation

Escalate immediately when:

- recovery involves data loss beyond an already approved tolerance;
- primary and backup integrity are uncertain;
- region/account/control-plane failure exceeds documented procedure;
- restored state requires unknown application compatibility;
- security exposure may have affected backup or infrastructure authority.

See [Infrastructure: Storage, Backup and Recovery](../infrastructure/storage-backup-and-recovery.md).
