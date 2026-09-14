# Platform And Automation

Automation and platforms should reduce repeated effort, waiting and risk while
preserving understandable control. A tool is successful when its users can
achieve a supported outcome safely without depending on hidden specialist
knowledge.

## Automate A Known Outcome

Before automating work, define:

```text
User and desired outcome:
Current trigger and frequency:
Inputs and authoritative source:
Required authority:
Expected output and evidence:
Failure and partial-failure behavior:
Rollback, recovery or escalation:
Owner and lifecycle expectation:
```

Good automation makes a safe, repeatable process faster and more consistent.
Automating an unclear process can multiply its failures and obscure where
responsibility belongs.

Prioritize automation when one or more are material:

- the action is frequent and deterministic;
- manual execution is error-prone or difficult to audit;
- delay blocks delivery or recovery;
- privilege can be narrowed through a controlled interface;
- consistent evidence is required;
- multiple users would otherwise rediscover the same work.

Retain a human decision where context, consequence or ambiguous evidence is
the essential control. Manual approval should have stated criteria; a button
with no meaningful decision is only a queue.

## Automation Contract

Maintained automation SHOULD define:

- supported outcome and non-goals;
- inputs, outputs and validation;
- identity and least-required permissions;
- idempotency or repeat-execution behavior;
- timeout, retry and concurrency behavior;
- logs, status and audit evidence;
- partial failure, rollback and recovery;
- owner, documentation and change policy;
- dependency, version and retirement lifecycle.

Privileged automation is production code. Review, test, observe and version it
in proportion to its authority and blast radius.

Detailed workflow, infrastructure and security controls are defined in
[CI/CD Standards](../ci-cd/README.md),
[Infrastructure Standards](../infrastructure/README.md) and
[Security Standards](../security/README.md).

## Platform As A Product

A platform is a maintained set of capabilities presented through usable
contracts to internal consumers. It may be as small as documented templates
and workflows or as broad as a managed deployment platform.

Treat a platform as a product:

| Product concern | Platform expectation |
| --- | --- |
| Users | Identify consuming teams, workloads and skill constraints |
| Problem | State which repeated friction, risk or duplication is reduced |
| Interface | Provide documented APIs, workflows, templates or service contracts |
| Experience | Make the supported path discoverable and usable without routine tickets |
| Feedback | Observe adoption, failure, wait time and consumer outcomes |
| Reliability | State availability, support, recovery and dependency expectations |
| Evolution | Version contracts, communicate changes and provide migration paths |
| Ownership | Maintain the capability rather than only launching it |

Do not build a platform because the label appears mature. A shared capability
is justified when multiple real consumers benefit enough to offset its
operating cost and shared blast radius.

## Paved Paths, Not Cages

A paved path combines known-good defaults, automation and documentation for a
recurring task. It should be:

- secure and observable by default;
- self-service for supported operations;
- composable with other capabilities;
- versioned and owned;
- easier than reimplementing common controls;
- explicit about limits and unsupported use cases;
- accompanied by an exception or escape path.

Consumer teams remain responsible for application behavior and for operating
within the platform contract. Platform teams remain responsible for the
shared capability. Neither can silently transfer its responsibility to the
other.

An escape path may require review where it changes security, reliability, cost
or shared-platform risk. Exceptions need an owner and reassessment trigger;
they should not become permanent undocumented forks.

```text
Good                                      Avoid
Template with replaceable defaults       Mandatory stack with no justified outcome
Self-service deploy with scoped access   Ticket required for every ordinary deploy
Versioned interface and migration guide  Breaking platform change announced after release
Documented exception path                Unsupported workaround hidden in application code
```

## Reduce Cognitive Load

Hide incidental implementation complexity while preserving the information a
consumer needs to operate safely. A useful abstraction answers:

- What outcome does this capability provide?
- Which inputs and responsibilities remain with the consumer?
- How can the consumer observe status and failure?
- Which service expectation and support route apply?
- How can the consumer leave or use an alternative?

An abstraction that hides failure, cost or ownership creates dependency rather
than enablement. Documentation and examples are part of the interface.

## Prefer Secure And Operable Defaults

Supported paths SHOULD provide by default where relevant:

- minimal scoped identities and environment isolation;
- secret delivery without embedding credentials in source or artifacts;
- immutable, attributable artifacts;
- standard service/environment identity in telemetry;
- health, deployment and failure evidence;
- backup or reproducibility decisions for state;
- versioned configuration and safe change history;
- bounded retention and cost controls.

A default is not universally safe. Consumers must still state data,
availability, exposure and compliance needs that require stronger controls.

## Build, Buy Or Share Deliberately

| Choice | Prefer when | Responsibility retained |
| --- | --- | --- |
| Documented local automation | One or few users, narrow need, low coordination cost | Code, dependencies, access and recovery |
| Shared internal capability | Repeated need, stable contract and several consumers | Product ownership, support, upgrades and blast radius |
| Managed service | Provider capability reduces undifferentiated operation | Configuration, data, access, integration and provider failure |
| Custom platform | Strategic or constrained need justifies dedicated engineering | Full product, reliability, security and lifecycle burden |

Build the smallest capability that addresses the verified constraint. Reuse
before centralizing; centralize only with ownership and a consumer contract.

## Evaluate Platform And Automation Outcomes

Useful signals include:

- successful self-service completion and time to first use;
- lead time or wait removed from the value stream;
- adoption and supported-path abandonment;
- automation failure and recovery behavior;
- repeated support requests and documentation gaps;
- consumer satisfaction and ability to diagnose failure;
- security/control coverage achieved by default;
- maintenance cost and shared operational load.

Raw adoption is not enough. Mandatory use can raise adoption while making
delivery slower. Evaluate whether the capability improves a consumer outcome
without creating disproportionate dependency.

## Relationship To SRE

DevOps treats repeated friction and unsafe manual work as candidates for
improvement. [SRE: Toil, Capacity and Overload](../sre/toil-capacity-and-overload.md)
defines operational toil more narrowly and connects it to engineering
capacity, service objectives and on-call sustainability.

## Platform Review Questions

- Which verified user constraint does this capability remove?
- Can the ordinary supported action be completed without a specialist ticket?
- Are authority, failure, recovery and ownership visible?
- Does the abstraction reduce complexity or merely move it out of sight?
- Are consumers able to observe and leave the capability safely?
- Is the shared blast radius justified by actual reuse?
- Has successful adoption improved delivery, safety or operator experience?
