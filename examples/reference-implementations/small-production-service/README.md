# Small Production Service Reference Implementations

Integrated examples for a deliberately limited live service, such as a
containerized API behind managed or operated ingress with durable data,
delivery automation, monitoring and documented recovery.

| Implementation | What to run |
| --- | --- |
| [One slot, two booking paths](./reservations/README.md) | Start an API, worker and PostgreSQL with Compose. Race two synthetic customers and verify the winner through both entry points and the stored claim. |

Deploy the tested reservation image in a disposable lab, introduce a
reversible write-permission failure and measure recovery using
[booking probes and a stored control reservation](../../operational-scenarios/deployment-and-rollback/reservation-recovery/README.md).

Implementations must state accepted single points of failure, backup
and access strategy, cost assumptions and the conditions that would require a
more resilient topology.
