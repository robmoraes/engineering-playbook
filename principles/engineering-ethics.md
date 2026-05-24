# Engineering Ethics

## Responsibility Is Part Of The Work

Software can save time, reveal information, control access, record decisions
and influence what people are able to do. Engineering ethics is therefore not
an optional discussion after implementation. It is the discipline of noticing
whose interests and risks are affected by a technical choice, then acting
honestly and competently.

The principles here are original practice for this playbook, informed by the
professional codes identified in [References](./references.md).

## Practical Duties

An engineer responsible for a system SHOULD:

- seek benefit for the people the system exists to serve and avoid reasonably
  foreseeable harm;
- represent capability, limitations, progress and risk truthfully;
- protect privacy, confidentiality and access according to the sensitivity of
  the data and action involved;
- decline to hide material failure, security exposure or misleading behavior;
- seek competent review when a decision exceeds personal experience or has
  significant consequences;
- correct known defects according to risk rather than convenience alone.

These duties apply to small systems too. The scale of deployment changes the
controls required, but not the obligation to handle people and their data with
care.

## Decisions With Human Consequences

Technical decisions often appear neutral when expressed as implementation
choices:

| Choice | Human consequence to examine |
| --- | --- |
| Collecting an additional field | Privacy, misuse, breach impact and whether it is needed |
| Hiding an error behind generic success | Incorrect decisions, wasted time and loss of trust |
| Removing an accessibility path | Exclusion from completing an ordinary task |
| Using broad credentials for convenience | Greater impact from mistake or compromise |
| Shipping without recovery or backup planning | Loss of work, service or records relied upon by users |
| Deferring maintenance indefinitely | Accumulated failure risk transferred to users and future maintainers |

## Honesty Under Constraint

Budgets and deadlines are real engineering inputs. They may justify a smaller
feature, a manual process or an explicit temporary limitation. They do not
justify pretending that a risk is absent.

When an important deficiency cannot be resolved immediately, document:

- who or what may be affected;
- severity and likelihood as currently understood;
- the temporary control or operational instruction;
- the accountable owner and review date;
- the condition that requires escalation or stops release.

## Privacy, Security And Trust

Security is not only a platform concern. Users trust systems with credentials,
personal information, work products and decisions. Minimize data collected,
restrict access, protect secrets and make incident response possible. The
implementation standard for those controls is maintained in
[Security Standards](../security/README.md).

## Professional Judgment

Good intent does not remove the need for competence. Use review, testing,
standards and evidence. Admit uncertainty early. A professional judgment is
stronger when its assumptions and limits can be inspected by others.
