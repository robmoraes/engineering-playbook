# Journeys And Decisions

Design around the outcome a person needs. A database entity or a stakeholder's
requested screen is a starting input; investigate the work it is meant to
support.

## Minimum Discovery

Capture the following in the feature brief:

```text
User and role:
Task and desired outcome:
Trigger and entry point:
Frequency, device and working conditions:
Information the person already has:
Information the service already knows:
Required decisions and business rules:
Completion evidence and next step:
Likely interruption, mistake and recovery:
Known evidence, assumptions and open questions:
```

Observe an existing process, ask a representative user to explain a recent
case or inspect support issues. Identify whether users work occasionally,
repeat a task all day, use small screens or assistive technology, share a
device, or depend on an unreliable connection.

Stakeholder preference and developer intuition are inputs. Label them as
assumptions until evidence from the intended users supports them. Do not
invent personas or interview findings to fill an artifact.

## Map The Whole Task

Use a short sequence such as:

```text
Find customer -> check for existing record -> create if needed
-> verify saved details -> use customer in the next task
```

For each transition, name the actor, required information, action, resulting
state and way back. Include email verification, approval or background work
when completion depends on activity outside the current screen.

Account creation, customer registration and approval are different outcomes.
Saving a customer record must not imply that an account was activated or a
message sent unless the service actually performs those actions.

## Remove Unnecessary Work

Before adding a field, step or confirmation, ask:

- Is it necessary to complete this task now?
- Can the service derive or reuse it accurately and transparently?
- Can optional detail be supplied later?
- Does this choice prevent a meaningful mistake?
- Does the user understand the source and have a way to correct it?

Do not require an account for a task that can responsibly work without one.
Explain when identity or verification is needed. Carry known information
forward within the process, and allow correction where the business rules
permit it.

## Choose The Flow

| Situation | Starting choice | Validate |
| --- | --- | --- |
| Short familiar record creation | One page with related fields grouped | Scanning, keyboard order and recovery |
| Infrequent or conditional application | Focused steps with back navigation | Branching, saved answers and understandable progress |
| Repetitive expert data entry | Compact grouped form with efficient repeat actions | Error rate, focus order and throughput |
| Small contextual change | Inline edit or short dialog | Discoverability, save/cancel and focus return |
| Long or consequential edit | Dedicated page with context and review | Interruption, conflicts and consequences |

GOV.UK starts many public service flows with one thing per page. This playbook
adapts that guidance to task frequency and complexity; a wizard for every
field can slow repeated internal work. GOV.UK explicitly discusses grouping
questions for repetitive internal use in
[Structuring forms](https://www.gov.uk/service-manual/design/form-structure).

Extra steps can be justified when they reduce uncertainty or prevent expensive
errors. Removing a review step simply to increase conversion may reduce the
quality of the resulting decisions.

## Keep Control And Context

- Preserve meaningful back navigation, entered values and list filters.
- State whether leaving discards changes or retains a draft.
- If work can be resumed, identify what is saved, where and for how long.
- Re-evaluate dependent answers after a preceding choice changes; explain
  which information now needs attention.
- Offer a clear completion state and a relevant next action.

Use progressive disclosure for optional or uncommon detail. Keep costs,
material consequences and information required for the current decision
visible before commitment.

## Ethical Defaults

Defaults must be safe, transparent and appropriate to the task. Do not assume
consent, hide cancellation, disguise charges or use misleading urgency. Make
acceptance and refusal understandable. If a business request introduces such
behavior, explain the user consequence and propose a clear alternative.

## Definition Of An Intuitive Flow

Treat intuitiveness as a claim to test: a representative person can identify
the next action, predict its effect, complete the task and explain the final
state without coaching. Familiarity varies by audience and culture.

Use [Evaluation and Validation](./evaluation-and-validation.md) to check that
claim and the [Screen and Journey Brief](../examples/templates/ux/screen-brief.md)
to retain the decisions.
