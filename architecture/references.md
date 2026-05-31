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
| IETF BCP 47 and RFC 5646, *Tags for Identifying Languages* | Language tags identify languages and variants using interoperable subtags. | Application language and locale identifiers use BCP 47 tags such as `pt-BR`, `en-US`, `es-419` and `zh-Hant`. |
| Unicode CLDR Project and UTS #35, *Unicode Locale Data Markup Language* | CLDR provides locale data and LDML specifies structures and algorithms used for locale-sensitive behavior. | Applications rely on platform internationalization libraries and CLDR-backed behavior for formatting, plural rules, display names and collation rather than hard-coded patterns. |
| ICU Documentation, *Formatting Messages* | MessageFormat supports placeholders and selection among plural or other message variants. | User-facing messages use complete localizable strings with placeholders, plural rules and select rules instead of concatenated fragments. |
| W3C Internationalization, *Language tags in HTML and XML* and authoring techniques | Web content should identify language and support international authoring practices. | Web applications expose explicit document language and direction, avoid country flags as language identity and treat localization as content behavior, not only text replacement. |
| GitHub Spec Kit, *Spec-Driven Development* | Spec-driven development puts specifications at the center of AI-assisted work and refines changes through spec, plan, tasks and implementation phases. | The playbook adopts a tool-independent spec-first workflow where specs, plans, tasks and verification artifacts stay aligned through review. |
| Cucumber, *Behaviour-Driven Development* | BDD emphasizes shared understanding through concrete examples, formulation and automation. | Acceptance examples are used to clarify expected behavior and guide automated checks without requiring every project to use Cucumber. |
| Martin Fowler, *Specification by Example* | Examples can make behavior easier to understand and verify, but they do not replace collaboration or other requirement techniques. | Specs must combine concrete examples with scope, constraints, contracts and architecture decisions instead of relying on examples alone. |
| OpenAPI Initiative, *OpenAPI Specification* | OpenAPI provides authoritative machine-readable specifications for HTTP APIs. | API-facing spec-driven changes use OpenAPI or equivalent machine-readable contracts rather than prose-only endpoint descriptions. |

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
- IETF, *BCP 47 - Tags for Identifying Languages*:
  <https://datatracker.ietf.org/doc/bcp47/>
- RFC 5646, *Tags for Identifying Languages*:
  <https://www.rfc-editor.org/rfc/rfc5646>
- Unicode CLDR Project:
  <https://cldr.unicode.org/>
- Unicode CLDR, *UTS #35: Unicode Locale Data Markup Language*:
  <https://cldr.unicode.org/index/cldr-spec>
- ICU Documentation, *Formatting Messages*:
  <https://unicode-org.github.io/icu/userguide/format_parse/messages/>
- W3C Internationalization, *Language tags in HTML and XML*:
  <https://www.w3.org/International/articles/language-tags/>
- W3C Internationalization, *Authoring techniques*:
  <https://www.w3.org/International/techniques/authoring-html>
- GitHub Spec Kit, *Spec-Driven Development*:
  <https://github.github.io/spec-kit/concepts/sdd.html>
- GitHub Spec Kit, *Quick Start Guide*:
  <https://github.github.io/spec-kit/quickstart.html>
- Cucumber, *Behaviour-Driven Development*:
  <https://cucumber.io/docs/bdd/>
- Martin Fowler, *Specification By Example*:
  <https://martinfowler.com/bliki/SpecificationByExample.html>
- OpenAPI Initiative Publications:
  <https://spec.openapis.org/>

## Using References Responsibly

External sources are not a substitute for local context. When an ADR relies on
industry guidance, it should still state:

- the actual requirement or production risk;
- the relevant constraints and alternatives;
- what is adopted locally;
- what evidence would cause the decision to change.
