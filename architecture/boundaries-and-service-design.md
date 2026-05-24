# Boundaries and Service Design

System boundaries define ownership of behavior, data, change and failure.
Deployable services should follow boundaries that are already understood, not
serve as an expensive experiment for finding them.

## Boundary Model

A useful system map distinguishes:

| Boundary | Questions |
| --- | --- |
| Public edge | Which endpoints are internet-facing? Where do TLS, routing and rate controls apply? |
| Application capability | Which component owns each business action and its API contract? |
| Data ownership | Which component writes each dataset? Which readers need an API or event rather than direct table access? |
| Trust boundary | Where do identities, secrets, untrusted input or privileged operations cross? |
| Platform dependency | Which shared services, managed products or infrastructure components must remain available? |

Example small production topology:

```text
Internet
  -> reverse proxy / TLS ingress
    -> portfolio-web
    -> orders-api
         -> PostgreSQL (orders-owned data)
         -> object storage (uploaded receipts)
         -> email provider (external dependency)
    -> orders-worker
         -> same queue and orders-owned database
```

This topology can remain one repository or one application deployment while
still documenting its critical boundaries.

## Modular Monolith as Default Starting Point

A modular monolith is an application with explicit internal capability
boundaries and one primary deployment lifecycle.

Use it when:

- one team or engineer owns the system;
- domain boundaries are evolving;
- independent scaling is not proven necessary;
- a single release and runtime are operationally acceptable.

Require within it:

- separate modules for stable capabilities;
- clear data ownership at module level;
- interfaces that prevent arbitrary cross-module coupling;
- background jobs separated logically and, when useful, as a distinct process.

```text
Good                                      Avoid
orders module owns order transitions     controllers directly modify all tables
worker process reuses documented domain  microservices sharing one uncontrolled schema
```

## When Microservices Are Justified

Independent services become reasonable when at least one strong driver exists
and the boundary is stable:

| Driver | Evidence to seek |
| --- | --- |
| Independent scaling | One capability dominates compute, latency or throughput needs |
| Failure isolation | Failure in one capability must not interrupt another critical path |
| Independent delivery | Teams or release cadence genuinely require separate deployments |
| Security isolation | A capability holds different sensitive data or privileges |
| Technology/runtime constraint | A workload requires a materially different runtime with clear benefit |

Costs introduced by distribution include network latency and partial failure,
API compatibility, authentication between services, distributed telemetry,
deployment coordination and consistency choices across data ownership.

```text
Good                                      Avoid
Extract image processor due to measured  Split CRUD endpoints by database table
CPU isolation and queue workload
Separate payment boundary with scoped    Add five services because containers are available
credentials and explicit contract
```

## Service Decomposition Rules

- A service SHOULD own a coherent capability, not only a technical layer.
- A service SHOULD own writes to its data or expose controlled commands.
- Cross-service synchronous call chains SHOULD be short and observable.
- Shared libraries MAY reduce duplication but MUST NOT hide distributed data
  ownership or force lockstep releases.
- Events SHOULD describe meaningful completed facts, not leak internal table
  mutations as an integration contract.

An `orders-api` directly querying a `payments` service database removes the
benefit of service separation while retaining its operational costs.

## Public, Internal, Edge and Core Services

| Type | Responsibility | Typical controls |
| --- | --- | --- |
| Edge | TLS termination, routing, public policy enforcement | Public network, rate limiting, restricted backends |
| Public application | User-facing API or web delivery | Authentication, input validation, externally visible SLO |
| Internal service | Worker, admin API, internal integration | Private network, service identity, no direct internet route |
| Core dependency | Database, queue, identity, observability platform | Restricted access, backups, high operational scrutiny |

Do not make a service publicly routable simply because the application needs
to call it. Public exposure is an architectural and security decision.

## API and Asynchronous Communication

Prefer synchronous communication when the caller needs an immediate result and
the dependency is acceptable in its availability path. Prefer asynchronous
processing when work can complete later, needs buffering or must isolate slow
external systems.

| Pattern | Benefit | Consequence |
| --- | --- | --- |
| HTTP request/response | Simple client feedback and debugging | Caller inherits dependency latency/failure |
| Queue and worker | Buffering, retries and workload isolation | Eventual completion, idempotency and dead-letter handling needed |
| Event publication | Loose downstream integration | Schema evolution, ordering and duplicate handling needed |

Adding a broker only to call every consumer synchronously through messages is
usually complexity without useful decoupling.

## Shared Platform Services

Shared ingress, identity, registries, logging and monitoring reduce duplicated
work. They also increase shared blast radius.

For each shared service, document:

- consumers and criticality;
- authentication and network boundary;
- failure impact and fallback;
- upgrade ownership;
- capacity and cost model.

A shared reverse proxy that serves every application is appropriate in a small
platform, provided its failure affects all public applications and its recovery
path is therefore treated accordingly.
