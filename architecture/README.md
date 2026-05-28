# Architecture Standards

Architecture guidance for building systems that can be deployed, operated,
changed and understood over time. This section documents decision logic and
operational consequences, not target-state diagrams detached from delivery.

## Architecture Position

The default posture in this playbook is:

1. Start with the simplest architecture that establishes clear domain,
   deployment, security and data boundaries.
2. Prefer a modular deployable unit until independent scaling, isolation,
   ownership or reliability needs justify distribution.
3. Treat state, network calls, third-party dependencies and operations as
   first-class design concerns.
4. Add platform complexity only with observable benefit and a clear owner.
5. Record consequential choices and their tradeoffs using Architecture
   Decision Records (ADRs).

## Operating Contexts

| Context | Practical default | Typical reason to invest further |
| --- | --- | --- |
| **Personal/lab** | One deployable application, managed data service or simple container stack, basic telemetry | Learning a production pattern or exposing a public service safely |
| **Small production** | Modular application, automated deployment, reverse proxy, isolated data, backups and monitoring | Availability, data durability, security or traffic growth |
| **Production-critical** | Explicit failure domains, recovery targets, SLOs, controlled rollouts and tested restore paths | User impact and recovery cost justify operational investment |
| **Enterprise-scale** | Team-aligned service ownership, governed platform capabilities and stronger isolation | Multiple teams, regulatory duties or broad organizational blast radius |

An architecture is not mature merely because it is distributed. It is mature
when its constraints, failure modes, cost and operating procedures are known.

## Navigation

| Document | Covers |
| --- | --- |
| [Principles and Tradeoffs](./principles-and-tradeoffs.md) | Decision priorities, simplicity, cost, reliability and build-versus-buy |
| [Boundaries and Service Design](./boundaries-and-service-design.md) | System boundaries, monolith versus microservices, APIs and data ownership |
| [Runtime and Platform Topology](./runtime-and-platform-topology.md) | Container-first runtime, ingress, discovery, networks, Swarm and Kubernetes |
| [State, Reliability and Scale](./state-reliability-and-scale.md) | Stateful workloads, failure domains, HA, distributed systems and scaling |
| [Time and Timezone Standards](./time-and-timezone-standards.md) | UTC instants, IANA timezones, API contracts, persistence, scheduling and display |
| [Delivery and Evolution](./delivery-and-evolution.md) | Environments, deployments, observability, technical debt and evolution paths |
| [Architecture Decisions](./decision-records/README.md) | ADR policy, decision index and template |
| [References](./references.md) | Source material and adopted conventions |

## Required Architecture Records

Any persistent production project SHOULD document:

- a context and runtime topology showing public entry points, services,
  stateful dependencies and trust boundaries;
- deployment model, environment boundaries and rollback or recovery route;
- data ownership, backup expectation and material third-party dependencies;
- major architecture decisions and known tradeoffs in ADRs;
- critical service indicators or observable signals needed to operate it.

## Change Rule

Architecture evolves through decisions, not silent drift. A change that adds a
datastore, public endpoint, orchestrator, asynchronous delivery path,
cross-service dependency, production failure domain or significant recurring
cost SHOULD include an ADR or update to the topology documentation.
