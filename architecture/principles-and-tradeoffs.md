# Principles and Tradeoffs

This playbook treats architecture as the set of decisions that constrain how a
system changes and operates. The aim is not an idealized platform; it is a
system whose complexity is justified by real requirements.

## Principles

### Prefer operationally boring foundations

Use proven components and clear ownership before introducing coordination-heavy
architecture. A PostgreSQL database, containerized application and reverse
proxy can be a strong production design when they meet availability and scale
requirements.

```text
Good                                      Avoid
One recoverable datastore with backups   Three databases without ownership or restore tests
Documented container stack               New orchestrator only to appear cloud-native
```

### Make boundaries explicit before splitting deployment

Code boundaries, data ownership and APIs can be clarified inside one
deployable application. Service decomposition does not repair unclear domains;
it adds networks, releases and failure modes around them.

### Design for recovery, not only steady-state success

For each critical dependency, ask:

- What fails when it is unavailable or slow?
- How is failure detected?
- Can the system degrade, retry or recover without duplicating work?
- What data must be restored and within what time?

Availability claims without a tested recovery path are aspirations, not
architecture.

### Observe behavior before optimizing scale

Do not partition, replicate or introduce asynchronous processing solely because
traffic might increase. Establish telemetry and workload expectations, then
scale the bottleneck demonstrated by data.

### Treat security and cost as architectural inputs

Authentication boundaries, secret access, public exposure and data sensitivity
shape service boundaries and network topology. Recurring platform cost and
operator time are also architecture consequences.

## Simplicity Versus Capability

Architecture complexity is justified when it materially improves a requirement
that matters.

| Decision | Benefit | Operational cost | Adopt when |
| --- | --- | --- | --- |
| Single service deployment | Low coordination and easy debugging | Coarse scaling and release boundary | Workload is small or domain boundaries remain in motion |
| Separate worker process | Async work and independent resource sizing | Queue handling and job observability | Requests should not wait on background work |
| Independent microservice | Isolation and independent ownership/deployability | Network failures, API evolution, distributed tracing and data consistency | Boundary is stable and benefit exceeds operational cost |
| Replicated service | Higher request capacity and instance tolerance | Load balancing and statelessness requirements | Load or recovery objective requires replicas |
| Highly available datastore | Reduced single-node outage impact | Cost, failover behavior and recovery testing | Data/service availability target justifies it |

## Practical Versus Ideal Architecture

An ideal design may separate every concern, provide multi-zone resilience and
enforce complete platform policy. A practical design establishes the controls
whose absence would create unacceptable impact today, while making later
improvements possible.

| Context | Practical choice | Poor overinvestment |
| --- | --- | --- |
| Portfolio service | One application and managed database, versioned deployment and backups | Multi-cluster microservices with no users or operating time |
| Internal tool | Single regional deployment with restore procedure | Global active-active before downtime impact is known |
| Revenue-critical API | Redundancy across failure domains, SLO and controlled rollout | Assuming a single host is adequate because it has rarely failed |

The simpler option is not always cheaper. A single unmanaged database without
tested backups may cost more in recovery than a managed service.

## Build Versus Buy

Managed or third-party capabilities are architecture decisions because they
exchange implementation work for dependency, cost and provider constraints.

Evaluate:

| Question | Example consideration |
| --- | --- |
| Is this a differentiating capability? | Building authentication rarely differentiates a portfolio API |
| What is the operating burden? | Running a database requires backups, upgrades, monitoring and recovery |
| What lock-in is introduced? | Provider-specific events or identity integration may affect migration |
| What failure or exit path exists? | Export format, fallback provider or restoration procedure |
| What cost grows with usage? | Per-request queues, log retention, egress or managed database tier |

```text
Good                                      Avoid
Managed database with backup/exit plan   Self-hosting data solely to avoid a small monthly cost
External identity provider with ADR      Custom password system without security ownership
```

## Architecture Review Questions

Before adding a major component or changing topology:

1. What concrete requirement or observed constraint requires the change?
2. Which failure modes and operational tasks are introduced?
3. Which trust, data and deployment boundaries change?
4. What does this cost in infrastructure and engineering attention?
5. How is success observed, and how can the change be reversed?

Record consequential answers in an ADR rather than relying on memory.
