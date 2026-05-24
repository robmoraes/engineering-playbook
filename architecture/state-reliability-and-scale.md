# State, Reliability and Scale

The most consequential architecture choices usually involve data and failure.
Stateless application replicas are easy to recreate; durable state and
cross-service correctness are not.

## Stateless and Stateful Workloads

Prefer stateless application processes:

- hold durable records in a datastore, object store or queue with an explicit
  durability model;
- treat local container filesystem and memory as replaceable;
- make instances disposable so deployments and recovery do not depend on a
  specific container.

Stateful components require additional design:

| Concern | Example decision |
| --- | --- |
| Durability | Database backups and retention |
| Recovery | Tested restoration and recovery time expectation |
| Placement | Node-local disk versus managed replicated storage |
| Consistency | Transaction boundary and concurrent write handling |
| Upgrade | Migration compatibility and rollback limitations |

```text
Good                                      Avoid
Uploads placed in durable object store   User data kept only in container volume without backup
Database restore procedure tested        "HA" declared because two app replicas exist
```

## Storage Strategy

Select storage from access and recovery needs, not familiarity alone.

| Data type | Practical starting point | When to invest further |
| --- | --- | --- |
| Relational application state | Managed PostgreSQL or backed-up database instance | Higher availability, read load or stricter recovery objective |
| Uploaded binary assets | Durable object storage | Replication or lifecycle policy required |
| Cache | Replaceable in-memory cache | Availability only if cache loss creates unacceptable load |
| Background work | Durable queue when work cannot be lost | Ordering, throughput or replay requirements |
| Logs/metrics | Centralized telemetry store with retention | Compliance, incident depth or cost governance |

Never confuse a mounted volume with a backup. A volume preserves state across
container replacement; it may not protect against node failure, deletion,
corruption or operator error.

## Distributed Systems Baseline

Once processing crosses a network or queue, assume:

- requests can time out after the remote side completed work;
- retries can duplicate operations;
- messages may arrive late, more than once or out of order;
- dependencies can be slow rather than entirely unavailable;
- clocks and instance-local memory cannot be used as global truth.

Practical controls:

| Failure | Control |
| --- | --- |
| Transient dependency error | Timeout and bounded retry with backoff |
| Duplicate command or delivery | Idempotency key or deduplication |
| Slow external provider | Async processing or circuit/protective limit where warranted |
| Failed async work | Retry policy and dead-letter/reconciliation path |
| Partial workflow completion | Explicit state machine or compensating operation |

```text
Good                                      Avoid
Idempotent payment callback handling     Blind retry of charge request
Timeout on email provider request        Worker blocked indefinitely on network call
```

Do not add distributed patterns speculatively to a single-process system.
Apply them at real boundaries where partial failure exists.

## Reliability Objectives

A critical production service SHOULD state what users depend on and how that
behavior is observed. Useful measures commonly include availability, request
latency, error rate, job completion delay and data durability.

| Workload | Example concern |
| --- | --- |
| Public API | Successful requests and latency |
| Worker pipeline | Completion time, backlog and failed jobs |
| Storage service | Durability and restore capability |
| Internal admin tool | Availability may be lower, but authorization correctness remains critical |

Do not promise high availability without designing and testing the relevant
failure and recovery path. A single low-impact portfolio application may
accept restore-based recovery. A production-critical ordering path may require
redundant components, controlled failover and a measured SLO.

## Failure Domains

Map what can fail together:

```text
Provider/account
  -> region or site
      -> cluster/control plane
          -> node
              -> container/process
                  -> dependency call
```

Replicas on the same host protect against a process crash, not host failure.
Several services behind one proxy remain exposed to proxy failure. Multiple
application nodes connected to one database still share a data failure domain.

Before investing in high availability, identify the actual dominant failure
domain and the recovery objective it threatens.

## High Availability Tradeoffs

| Pattern | Protects against | Does not solve | Cost |
| --- | --- | --- | --- |
| Multiple stateless replicas | Process/node loss and request capacity | Shared database or ingress failure | Compute and load balancing |
| Redundant ingress | Proxy/node outage | Backend or DNS failure | Routing and certificate complexity |
| Replicated/failover database | Primary database outage | Bad migrations or data deletion | Cost and operational testing |
| Multi-zone deployment | Zone failure | Region/provider or application defect | Higher infrastructure and data topology complexity |
| Multi-region active-active | Regional outage/latency needs | Consistency and operational errors | Very high data and operations complexity |

For small production, backups and a known restoration path often provide better
value than an untested HA setup. For production-critical services, restore-only
recovery may be inadequate.

## Scalability Philosophy

Scale in response to measured pressure:

1. Observe latency, saturation, throughput, errors and cost.
2. Remove avoidable inefficiencies such as missing indexes or oversized
   payloads.
3. Scale stateless compute horizontally when the workload permits.
4. Decouple expensive or delay-tolerant processing into workers when useful.
5. Scale or partition state only when proven necessary and understood.

```text
Good                                      Avoid
Extract worker after request latency     Partition database before workload exists
shows image processing bottleneck
```

The fastest architecture to scale is often the one whose operations, data
ownership and bottlenecks are already understandable.
