# UX Checklist

Apply the relevant items to the complete task, including interruption and
correction. Record a reason for `Not applicable`; do not mark untested behavior
as verified. This checklist is a delivery aid, not a complete WCAG assessment.

## Goal And Journey

- [ ] User, task, context and completion condition are explicit.
- [ ] Evidence and assumptions are distinguished.
- [ ] The flow includes prerequisites, handoffs and a useful next step.
- [ ] Every required field and step has a current purpose.
- [ ] The flow fits occasional or repeated use rather than an arbitrary step
  or click limit.

## Screen And Content

- [ ] Title, current object and status make the location understandable.
- [ ] Actions use specific labels and communicate scope and consequences.
- [ ] Each action group has a clear priority.
- [ ] Navigation, vocabulary and components follow existing conventions.
- [ ] Empty, no-match, loading and error states are distinct.
- [ ] Search, sort and list context survive relevant navigation.
- [ ] Bulk actions state selection scope and count.
- [ ] Realistic long text, missing values and narrow layouts remain usable.

## Forms

- [ ] Required/optional status, labels and instructions are visible and
  programmatically associated.
- [ ] Input types, autocomplete and keyboards suit the actual data.
- [ ] Paste, common names and legitimate formatting variations are supported.
- [ ] Known information can be reused and corrected as appropriate.
- [ ] Validation timing avoids interrupting unfinished input.
- [ ] Failed submission retains appropriate values and identifies correction.
- [ ] Client and server validation agree on the business rules.
- [ ] Draft, final submission and repeated-entry actions have distinct effects.

## Action Feedback And Recovery

- [ ] Saving and completion reflect confirmed server behavior.
- [ ] A background request is distinguished from completed work.
- [ ] A consequential result remains inspectable after a toast disappears.
- [ ] Timeout/unknown outcomes have reconciliation and safe retry behavior.
- [ ] Duplicate effects are controlled beyond simply disabling the button.
- [ ] Unsaved work, expired sessions and concurrent edits have explicit paths.
- [ ] Destructive actions identify the object, consequence and recovery limits.
- [ ] Partial success identifies remaining failures and a safe next action.
- [ ] Error messages provide a useful next step without exposing sensitive data.

## Accessibility

- [ ] Main tasks work with keyboard alone and logical focus order.
- [ ] Focus is visible and usable beneath sticky elements and overlays.
- [ ] Names, roles, values and states are available to assistive technology.
- [ ] Errors and status changes are accessible without unnecessary focus jumps.
- [ ] Contrast, non-color cues and pointer targets meet applicable criteria.
- [ ] Narrow layout, text resize and text-spacing overrides preserve function.
- [ ] Dialogs support correct entry, containment, dismissal and focus return.
- [ ] Dragging and gesture interactions have appropriate alternatives.
- [ ] Authentication supports assistance such as password managers and paste.
- [ ] Applicable WCAG criteria beyond this short checklist are evaluated when
  making a conformance claim.

See [Accessibility](./accessibility.md) for exact distinctions between WCAG
requirements and local design defaults.

## Evidence And Learning

- [ ] Implemented behavior was exercised, including applicable failure states.
- [ ] Browser, viewport and assistive-technology checks are recorded.
- [ ] Usability observations identify participants and task context without
  unnecessary personal data.
- [ ] Proxy reviews and unvalidated assumptions are labeled honestly.
- [ ] Blocked access, data loss and misleading outcomes are resolved or
  explicitly reported as delivery gaps with accountable owners.
- [ ] Relevant regression cases and the feature specification are updated.

## Implementation Handoff

```text
User goal and affected screens:
Journey, fields and action decisions:
Components reused and intentional exceptions:
States and recovery implemented:
Validation performed and evidence:
User observations versus assumptions:
Remaining gaps, owners and next validation:
```
