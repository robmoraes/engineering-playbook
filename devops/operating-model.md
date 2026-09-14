# DevOps Operating Model

DevOps aligns the people who decide, build, deliver and operate a system around
one outcome. It replaces invisible handoffs and local optimization with
explicit ownership, usable feedback and shared improvement work.

## Optimize For Outcomes

A delivery process is useful only when it helps a person or organization
achieve an outcome with acceptable risk, delay and operating cost.

Before selecting tools or automation, state:

```text
Outcome and affected users:
System or service boundary:
Owner and participating roles:
Current delivery and recovery path:
Important security/reliability constraints:
Evidence that the outcome is improving:
```

Output volume, ticket completion and infrastructure count are activity
signals. They do not independently prove that a useful outcome was delivered.

## Whole-Lifecycle Ownership

Ownership continues after merge or deployment:

| Lifecycle concern | Ownership expectation |
| --- | --- |
| Discover | Understand the user, operational and organizational outcome |
| Design | Include testability, security, operability and recovery consequences |
| Implement | Keep intent visible and changes reviewable |
| Validate | Produce evidence proportional to change risk |
| Deliver | Preserve source, artifact, approval and deployment traceability |
| Operate | Detect user-affecting failure and provide a safe response path |
| Improve | Use feedback, incidents and friction to change the system of work |
| Retire | Remove access, data, dependencies, automation and operational noise safely |

Shared ownership means these concerns cannot be discarded at a team boundary.
It does not mean responsibility is anonymous or that everyone receives every
privilege. Each service, platform capability and production procedure still
needs a named accountable owner.

## Collaboration And Information Flow

Important information must reach the people able to act on it in time to
change an outcome. Prefer:

- cross-functional review of consequential changes;
- shared delivery and production evidence;
- documented interfaces, decisions and operating limits;
- direct collaboration when a handoff contains uncertainty;
- early escalation of risk or bad news;
- post-incident inquiry focused on system conditions and defenses.

A ticket can record work but cannot replace shared understanding. A handoff is
acceptable when its input, owner, completion condition and feedback route are
clear. A queue with no service expectation or context merely hides delay.

```text
Good                                      Avoid
Developer and operator review rollout    Operations receives an unexplained deploy ticket
Security constraint defined in design    Security review begins after release approval
Failure signal reaches service owner     Monitoring alerts a team unable to change the service
Platform contract documents boundaries   Platform knowledge lives with one administrator
```

## Responsibility And Authority

Responsibility needs enough authority to act, while authority remains
constrained by risk:

| Responsibility | Necessary capability | Boundary to preserve |
| --- | --- | --- |
| Application change | Read production evidence and improve code/config | No default platform-admin access |
| Deployment | Select and verify an approved artifact | No source rebuild or unrelated infrastructure authority |
| Platform operation | Maintain shared capability and recover it | No ownership of application-specific behavior |
| Security response | Contain exposure and coordinate remediation | No silent permanent product change |
| Incident coordination | Direct response, communication and escalation | No assumption of every specialist's authority |

Production access is not proof of ownership. Useful telemetry, documented
escalation and a controlled delivery path often give a service team the
feedback it needs without granting broad interactive access.

## DevOps Engineer Position

A DevOps Engineer enables safer and faster engineering work by improving the
system through which changes move. The role may build delivery automation,
infrastructure capabilities, observability foundations, security controls and
operational standards.

The role SHOULD:

- make the safe path understandable and convenient;
- expose clear contracts instead of relying on personal intervention;
- work with application, security and operations knowledge holders;
- preserve product-team responsibility for application behavior;
- reduce repeated waiting, error-prone work and privileged manual action;
- transfer knowledge and remove single-person dependencies;
- measure whether the capability improves flow and outcomes.

The role SHOULD NOT become the mandatory ticket queue for every deployment,
the sole owner of all production failures or the permanent interpreter of
undocumented automation. Centralizing those dependencies recreates the silo
that DevOps is intended to reduce.

## Sustainable Responsibility

Operational responsibility must fit available people, skills and time:

- define support and escalation expectations instead of implying continuous
  availability;
- distribute knowledge for consequential systems;
- automate high-frequency safe actions and document the remainder;
- reserve time for maintenance, dependency updates and corrective work;
- reduce recurring alerts and manual recovery rather than normalizing them;
- adjust commitments when operational load consumes delivery capacity.

A small project may have one maintainer. In that case, state the limitation,
keep recovery practical and avoid making service claims that require a team
that does not exist.

## Operating Model Smells

| Smell | Likely system problem |
| --- | --- |
| Deployments wait for one specialist | Knowledge or authority is unnecessarily centralized |
| Developers cannot see production behavior | Feedback is separated from the people who change the system |
| Operations repeatedly repairs the same failure | Corrective work is not reaching product priorities |
| Security appears only as a release gate | Risk feedback arrives too late |
| More parallel work makes delivery slower | WIP and handoffs hide the actual constraint |
| Platform adoption requires repeated tickets | Capability lacks a usable self-service contract |
| Success depends on a permanent hero | Documentation, automation or responsibility is incomplete |

## Relationship To SRE

This operating model establishes collaboration and whole-lifecycle
responsibility. SRE adds an opinionated reliability model for selected
services, including service-level objectives, error budgets, operational work
limits and sustainable response. Apply it through
[SRE Standards](../sre/README.md).

DevOps does not require a separate SRE team. Where one exists, it partners with
service teams; it does not receive an unfinished system and inherit all
reliability responsibility through a one-way handoff.

## Practitioner Compass

When deciding what to improve, ask:

- Which user or operational outcome is constrained?
- Where does work wait, fail, require rework or lose context?
- Who can see the problem, and who has authority to change it?
- Is the safe path also the easiest reasonable path?
- What production evidence returns to the people shaping the service?
- Which repeated dependency on a person should become documentation,
  automation or a supported platform capability?
- What should remain a deliberate human decision?
