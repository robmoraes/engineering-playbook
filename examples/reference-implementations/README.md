# Reference Implementations

Integrated examples demonstrating multiple standards together: source shape,
images, delivery, runtime topology, observability, security boundaries and
operational recovery.

## What Qualifies

A reference implementation is more than several config files. It SHOULD
include:

- documented problem and operating context;
- topology and trust/data boundaries;
- artifact build and delivery route;
- externalized configuration and secret interface;
- monitoring/health expectations;
- recovery or rollback procedure;
- validation steps;
- limitations, cost and scaling tradeoffs;
- ADRs for consequential choices where useful.

## Planned Implementations

| Directory | Purpose |
| --- | --- |
| [local-lab](./local-lab/) | Safe local or disposable learning environments |
| [small-production-service](./small-production-service/) | Production-oriented single service topology with explicit constraints |
| [platform-capability](./platform-capability/) | Shared capability such as ingress or telemetry serving multiple workloads |

## Boundaries

Do not build one giant demo that attempts to represent all supported tools.
Each implementation should demonstrate a coherent operational model and link
to specialized templates where reusable assets belong.
