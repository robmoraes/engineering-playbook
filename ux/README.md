# UX And Screen Design Standards

Practical standards for building understandable, accessible and efficient
interfaces when a project has limited or no dedicated UX and design support.
Use them for web application screens, registration flows and internal tools.

## UX Position

The user should be able to answer five questions throughout a journey:

1. Where am I and which task can I complete here?
2. What information or decision is needed from me?
3. What will happen if I take this action?
4. What happened, and has my work been saved or completed?
5. How can I correct, leave, recover or continue?

The underlying decision strategy is to understand the task, remove unnecessary
work, make choices predictable and keep outcomes observable. Visual polish
supports this strategy; it cannot establish whether the right task was built.

## Decision Priorities

When requirements compete, use this local order and record material tradeoffs:

1. Protect access, user intent, data and consequential decisions.
2. Make the main task understandable and completable.
3. Prevent mistakes and make recovery possible.
4. Reduce repeated effort, waiting and memory demands.
5. Improve visual consistency and presentation.

Accessibility applies throughout these priorities. Efficiency means successful
completion with reasonable effort, including correction; a smaller click count
alone is not a success criterion.

## Starting Without A Designer

- Identify the people, task, context and constraints before composing screens.
- Reuse the product's existing design system and interaction patterns. Where
  none exists, choose a maintained accessible component foundation that fits
  the application and define a small consistent set of tokens and patterns.
- Write a short journey/screen brief within the feature specification.
- Implement the primary path plus failure, interruption and recovery states.
- Review with the checklist and observe representative people doing real
  tasks; record assumptions when user access is unavailable.

These standards provide a working baseline. Specialist input is valuable when
research uncertainty, accessibility barriers, high-consequence decisions or
complex workflows remain unresolved. A heuristic review is not user research.

## Navigation

| Document | Use when |
| --- | --- |
| [Journeys and Decisions](./journeys-and-decisions.md) | Defining the task, reducing steps and choosing a flow |
| [Screen Structure and Content](./screen-structure-and-content.md) | Organizing information, navigation, actions, lists and language |
| [Forms and Data Entry](./forms-and-data-entry.md) | Creating records, editing information or registering accounts |
| [Feedback and Recovery](./feedback-and-recovery.md) | Defining saving, errors, pending work, retries and destructive actions |
| [Accessibility](./accessibility.md) | Implementing keyboard, assistive technology and responsive behavior |
| [Evaluation and Validation](./evaluation-and-validation.md) | Checking task completion and learning from actual use |
| [UX Checklist](./ux-checklist.md) | Reviewing a screen or journey before delivery |
| [References](./references.md) | Understanding source guidance and local adaptations |

Start with the [Screen and Journey Brief](../examples/templates/ux/screen-brief.md)
and the [Customer Registration Example](../examples/templates/ux/customer-registration-example.md).

## Non-Negotiable Defaults

- A user-facing workflow MUST identify its user goal and completion condition.
- Actions MUST communicate their scope and material consequences.
- A consequential operation MUST distinguish requested, pending, completed,
  failed and unknown outcomes wherever those states can occur.
- Forms MUST justify required information, expose labels and instructions,
  retain appropriate input after errors and offer a correction path.
- Critical journeys MUST support keyboard use and accessible names, roles,
  states and feedback; production web interfaces target WCAG 2.2 level AA.
- Error handling MUST protect against avoidable data loss and duplicate
  effects. A disabled button alone does not guarantee this protection.
- Validation evidence MUST distinguish automated checks, human review and
  observed usability sessions. Unperformed checks remain unverified.

In this book, MUST denotes a required local control; SHOULD denotes a default
that can be adapted with a reason. WCAG requirements and heuristic guidance
are identified separately in the references.

## Applying This Standard With Codex

Read the entry point and relevant topic documents before changing a screen.
Inspect the existing product conventions, specification and components. Use
known business rules; record missing rules rather than inventing requirements
for personal data, permissions or consequential transactions.

Suggested implementation request:

```text
Apply ux/README.md and ux/ux-checklist.md to this screen or journey.
Identify the user, task and completion condition. Reuse existing components.
Define fields, actions, states and recovery before implementation. Cover
keyboard use, mobile layout, validation, saving and server failure. Verify the
implemented behavior and report evidence, assumptions and remaining gaps.
```

A small change can keep its brief in the existing issue or specification.
Use a separate record only when it helps maintain the decisions.

## Related Standards

- Human outcomes: [Users First](../principles/users-first.md).
- Behavior contracts: [Spec-Driven Development](../architecture/spec-driven-development.md).
- Languages and formatting: [Internationalization and Localization](../architecture/internationalization-and-localization.md).
- Regression evidence: [Testing Standards](../testing/README.md).
- Data, permissions and credentials: [Security Standards](../security/README.md).
- Reliable completion: [SRE Standards](../sre/README.md).
