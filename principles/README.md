# Professional Principles

Software engineering is valuable when it helps a person do something with
less friction, less uncertainty or less risk. A system may be commissioned by
an organization and shaped by commercial constraints, but its quality is
eventually experienced by the person who has to use it, trust it or recover
from its failure.

This section records the professional principles behind the technical
standards in this playbook. It is not a declaration that one engineer always
knows what users need. It is a commitment to listen carefully, make
consequential decisions explicit and treat software as work that affects real
people.

## Engineering Position

The default posture in this playbook is:

1. Build for the useful outcome a person is trying to reach, not only for the
   feature request as written.
2. Accept responsibility for security, reliability, data handling and
   comprehensibility as part of delivering functionality.
3. Prefer solutions that can be understood, operated and changed by others.
4. Use technical judgment with humility: measure behavior, document
   tradeoffs, seek review and correct mistakes.
5. Treat small systems seriously when they remove genuine friction from
   someone's day.

## Navigation

| Document | Covers |
| --- | --- |
| [Mission](./mission.md) | Why I build software and the concrete experience underlying this section |
| [Users First](./users-first.md) | User outcomes, stakeholder requests, friction, accessibility and failure paths |
| [Engineering Ethics](./engineering-ethics.md) | Harm, honesty, privacy, security, professional judgment and responsibility |
| [Craftsmanship](./craftsmanship.md) | Maintainability, documentation, review, testing and automation without ego |
| [Pragmatism](./pragmatism.md) | Simplicity, proportionate engineering, tradeoffs and technical debt |
| [Long-Term Responsibility](./long-term-responsibility.md) | Reliability, observability, recovery, stewardship and retirement |
| [References](./references.md) | External professional and operational sources, with adoption notes |

## From Principles To Practice

Principles matter only when they change engineering behavior:

- Architecture is evaluated by human consequences as well as topology and
  scale. See [Architecture Standards](../architecture/README.md).
- Delivery automation should reduce repetitive risk and make changes
  traceable. See [CI/CD Standards](../ci-cd/README.md).
- Operational visibility should enable responsible response to user-affecting
  failures. See [Observability Standards](../observability/README.md).
- Security protects users, their data and the organizations that serve them.
  See [Security Standards](../security/README.md).
- Runbooks make recovery safer when people are under pressure. See
  [Operational Runbooks](../runbooks/README.md).

## Use Of This Section

These documents provide a decision lens, not a universal process. For a
design, implementation, incident or review, ask:

- Who experiences the result, including a failure or misuse?
- What friction is removed and what new risk is introduced?
- Can another engineer understand, operate and change this safely?
- What evidence will show that the intended benefit is real?
- What obligation remains after the feature has shipped?
