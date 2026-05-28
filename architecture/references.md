# References and Adoption Notes

This architecture standard uses external guidance as input, then adapts it to
small and production-oriented platform contexts. The choice to prefer modular
deployment boundaries, require operational consequences in ADRs and introduce
complexity only after a demonstrated need is this playbook's convention, not a
requirement imposed by the external sources.

## External Guidance and Adoption

| Source | Relevant original guidance | Adoption in this playbook |
| --- | --- | --- |
| Google, *Site Reliability Engineering: Service Level Objectives* | Services should identify user-relevant behavior through indicators and objectives; unrealistic perfect availability can impose excessive cost and inhibit change. | Reliability investment is tied to measurable service behavior and recovery needs rather than vague HA claims. |
| Google, *Site Reliability Engineering: Monitoring Distributed Systems* | Monitoring supports rational decisions about system behavior and incidents. | Architecture changes identify telemetry needed to validate benefit and diagnose failure. |
| The Twelve-Factor App, *Processes*, *Backing Services* and *Dev/prod Parity* | Application processes should be stateless; backing services are attached resources; production-relevant gaps between environments should be reduced. | Container runtimes are replaceable, durable state is externalized and staging matches material production risks where cost permits. |
| AWS, *Well-Architected Framework* | Architecture decisions should account for operational excellence, security, reliability, performance efficiency, cost optimization and sustainability. | Reviews explicitly ask about operations, security, reliability and recurring cost without requiring AWS services. |
| Kubernetes Docs, *Cluster Architecture* and *Service* | Kubernetes provides a control plane/worker architecture and service abstraction with internal discovery and exposure options. | Kubernetes is considered when its policy and orchestration capabilities justify its operating surface; use platform service discovery first. |
| Docker Docs, *Swarm mode*, *Manage swarm service networks* and *Use Swarm mode routing mesh* | Swarm supplies service deployment, discovery, overlay networking and ingress routing behavior. | Docker Swarm is treated as a practical orchestration option with documented manager, ingress and stateful-storage consequences. |
| ADR GitHub Organization, *Architectural Decision Records*; Michael Nygard, *Documenting Architecture Decisions* | An ADR captures one significant decision, its rationale and consequences; a collection forms a decision log. | Significant production and platform decisions use lightweight versioned ADRs stored alongside this playbook. |
| Martin Fowler, *Microservices* and *Monolith First* | Microservices involve independently deployable services and bring tradeoffs; a monolith-first approach can reduce risk while boundaries are learned. | A modular deployable unit is the normal starting point; services are extracted for demonstrated isolation, scaling or ownership benefits. |
| RFC 3339, *Date and Time on the Internet: Timestamps* and RFC 9557, *Timestamps with Additional Information* | Internet timestamps should be unambiguous and fully qualified; RFC 9557 extends RFC 3339 with optional additional information such as named timezones. | API, log and event timestamps representing instants use RFC 3339 date-time strings with explicit offsets; extended timestamp syntax is used only when all producers and consumers support it. |
| IANA Time Zone Database, *Theory and pragmatics of the tz code and data* | The tz database records civil time history and predicted future rules using named timezone identifiers. | User, tenant, venue and schedule zones use IANA identifiers instead of timezone abbreviations or fixed offsets. |
| W3C, *Working with Time and Timezones* | Applications should distinguish instants, field-based times and floating times; future events need a timezone, not merely an offset. | The playbook separates instants, local dates/times, zoned future events, recurrences, durations and calendar periods in schemas and contracts. |
| PostgreSQL Docs and Wiki, *Date/Time Types* and *Don't Do This* | `timestamp with time zone` represents a point in time stored internally as UTC; PostgreSQL guidance warns against storing UTC in `timestamp without time zone`. | PostgreSQL-backed systems use `timestamptz` for instants and reserve naive date/time fields for intentional local civil values paired with an IANA timezone. |
| OpenAPI Format Registry, *date-time* and *date* | OpenAPI's `date-time` and `date` formats align with RFC 3339 definitions. | API schemas expose instant versus date-only semantics through OpenAPI formats and explicit timezone fields where needed. |

## Source Links

- Google, *Site Reliability Engineering - Service Level Objectives*:
  <https://sre.google/sre-book/service-level-objectives/>
- Google, *Site Reliability Engineering - Monitoring Distributed Systems*:
  <https://sre.google/sre-book/monitoring-distributed-systems/>
- The Twelve-Factor App, *Processes*:
  <https://12factor.net/processes>
- The Twelve-Factor App, *Backing services*:
  <https://12factor.net/backing-services>
- The Twelve-Factor App, *Dev/prod parity*:
  <https://12factor.net/dev-prod-parity>
- AWS, *Well-Architected Framework - The pillars of the framework*:
  <https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html>
- AWS, *Well-Architected Framework - Reliability design principles*:
  <https://docs.aws.amazon.com/wellarchitected/latest/framework/rel-dp.html>
- Kubernetes Docs, *Cluster Architecture*:
  <https://kubernetes.io/docs/concepts/architecture/>
- Kubernetes Docs, *Service*:
  <https://kubernetes.io/docs/concepts/services-networking/service/>
- Docker Docs, *Swarm mode*:
  <https://docs.docker.com/engine/swarm/>
- Docker Docs, *Manage swarm service networks*:
  <https://docs.docker.com/engine/swarm/networking/>
- Docker Docs, *Use Swarm mode routing mesh*:
  <https://docs.docker.com/engine/swarm/ingress/>
- Architectural Decision Records:
  <https://adr.github.io/>
- Michael Nygard, *Documenting Architecture Decisions*:
  <https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions>
- Martin Fowler and James Lewis, *Microservices*:
  <https://martinfowler.com/articles/microservices.html>
- Martin Fowler, *Monolith First*:
  <https://martinfowler.com/bliki/MonolithFirst.html>
- RFC 3339, *Date and Time on the Internet: Timestamps*:
  <https://www.rfc-editor.org/rfc/rfc3339>
- RFC 9557, *Date and Time on the Internet: Timestamps with Additional
  Information*:
  <https://www.rfc-editor.org/rfc/rfc9557>
- IANA Time Zone Database, *Theory and pragmatics of the tz code and data*:
  <https://data.iana.org/time-zones/theory.html>
- W3C, *Working with Time and Timezones*:
  <https://www.w3.org/TR/timezone/>
- PostgreSQL Docs, *Date/Time Types*:
  <https://www.postgresql.org/docs/current/datatype-datetime.html>
- PostgreSQL Wiki, *Don't Do This*:
  <https://wiki.postgresql.org/wiki/Don%27t_Do_This>
- OpenAPI Format Registry, *date-time*:
  <https://spec.openapis.org/registry/format/date-time>
- OpenAPI Format Registry, *date*:
  <https://spec.openapis.org/registry/format/date>

## Using References Responsibly

External sources are not a substitute for local context. When an ADR relies on
industry guidance, it should still state:

- the actual requirement or production risk;
- the relevant constraints and alternatives;
- what is adopted locally;
- what evidence would cause the decision to change.
