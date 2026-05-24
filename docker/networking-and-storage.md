# Networking and Storage

Networks and storage determine whether containerized workloads remain isolated,
durable and recoverable. Container packaging does not make persistent data or
reachability safe by default.

## Network Design

Attach a service only to networks required for its communication:

```text
edge-public       reverse proxy <-> public application endpoints
orders-private    API <-> worker/cache
orders-data       API/worker <-> database
monitoring        exporters <-> observability platform
```

Rules:

- only ingress/edge components SHOULD publish internet-facing ports;
- databases and queues SHOULD remain off public ingress networks;
- administrative endpoints SHOULD not be exposed for deployment convenience;
- name networks by purpose, not a current implementation detail.

Compose example:

```yaml
services:
  proxy:
    image: nginx:1.27-alpine
    ports: ["443:443"]
    networks: [edge_public]

  api:
    image: ghcr.io/acme/orders-api@sha256:<digest>
    networks: [edge_public, orders_data]

  db:
    image: postgres:17-alpine
    networks: [orders_data]
    volumes: [orders_db_data:/var/lib/postgresql/data]

networks:
  edge_public:
  orders_data:
    internal: true

volumes:
  orders_db_data:
```

`internal: true` is a useful Compose boundary but not a complete production
network security strategy; host exposure and platform configuration still
matter.

## Container Writable Layer

Treat the container writable layer as disposable:

```text
Appropriate                         Inappropriate
Temporary compiled cache            Customer uploads that must survive replacement
Transient request scratch files     Database files with no volume/backup plan
```

The writable layer is coupled to the container lifecycle and is unsuitable as
the sole storage for business data.

## Bind Mounts Versus Named Volumes

| Mechanism | Best use | Tradeoff |
| --- | --- | --- |
| Bind mount | Local source code, developer configuration, intentional host integration | Host-path coupling and permission variability |
| Named volume | Docker-managed local persistence for development or defined single-host workloads | Persistence is host/platform scoped; backup remains explicit |
| External durable storage | Production data requiring recovery or scheduler mobility | Additional service/cost/operational ownership |
| `tmpfs` | Sensitive/transient runtime scratch where supported | Lost at stop/restart; capacity must be managed |

```text
Good                                      Avoid
Bind mount source code in dev            Bind mount arbitrary production host paths
Named volume for local PostgreSQL        Claiming named volume alone is backup
Managed durable DB for production data   Container layer used for uploads
```

## Volume Conventions

Volume use MUST document:

- data owner and purpose;
- durability and backup expectation;
- whether multiple replicas may access it safely;
- node affinity or portability constraint;
- restore/recovery procedure for production data.

Do not scale a stateful container across nodes unless the underlying storage
and application consistency model support it.

## Database Containers

Running a database in Docker can be appropriate for local development, labs
and deliberately operated small deployments. Production viability depends on
storage durability, backups, recovery testing, patching, placement and access
control, not on whether the process is containerized.

| Context | Practical choice |
| --- | --- |
| Development | Database container with named volume and disposable/test data |
| Personal lab | Containerized database acceptable with backups if data matters |
| Persistent production | Managed database often reduces operational burden; self-host only with explicit ownership |
| Critical system | Durability, failover and recovery objective drive the decision |

## Secrets and Configuration Mounts

Configuration without sensitive values may be mounted or supplied as platform
configuration. Secrets must use protected delivery:

```text
Good                                      Avoid
Swarm secret mounted in /run/secrets     Secret stored in compose.yaml
Local untracked .env for dev only        Production .env bind-mounted from shared host directory
```

Compose local development can read untracked environment files; do not mistake
this for a production secret management strategy.

## Backup and Restore

Volume presence is not a recovery plan. Production stateful dependencies need:

- backup mechanism and destination;
- retention and protection level;
- restore procedure;
- recovery verification cadence;
- knowledge of which image/schema version can read restored data.

A containerized restore command may simplify execution, but recovery ownership
remains with the system operator.
