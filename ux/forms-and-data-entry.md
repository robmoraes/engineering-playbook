# Forms And Data Entry

Treat a form as a conversation that supports a task. Collect only information
needed for the current purpose and make entering, checking and correcting it
straightforward.

## Justify Every Field

For each field, record its purpose, required/optional status, source, acceptable
values and correction rule. A storage column does not automatically need a
visible input.

- Remove fields with no current use; defer optional enrichment.
- Reuse known information when permitted, identify its source and allow
  correction where appropriate.
- Explain why sensitive or unexpected information is needed.
- Distinguish unknown, not applicable and an intentional empty value when the
  domain needs that distinction.
- Do not require a value merely because a database default was inconvenient.

## Layout And Instructions

Use a single column as the initial form layout. Group tightly related short
fields when their reading order remains obvious and they reflow correctly.
Use labels above or consistently adjacent to controls and legends for groups.

Give each control a persistent visible label. Placeholders are optional
examples, never the only label. State format requirements before submission.
Mark optional fields in words when most inputs are required; otherwise use an
equally explicit consistent convention for both statuses.

Keep help concise and close to its input. Associate labels, hints and errors
programmatically. Do not hide required instructions in hover-only tooltips.

## Choose Appropriate Controls

| Information | Starting control | Important condition |
| --- | --- | --- |
| Short open answer | Text input | Accept real-world text and meaningful length |
| Long explanation | Text area | Explain purpose and real limits |
| One of a few choices | Radio group | Make selection and labels clear |
| Multiple independent choices | Checkboxes | State selection constraints |
| One of many choices | Select or accessible searchable control | Search must not remove keyboard access |
| Immediate on/off setting | Switch | Expose state and save failure; prefer a checkbox for changes applied only on Save |
| Date | Date input or suitable segmented fields | Match locale and task; retain a keyboard path |
| Identifier | Text input with suitable input mode | Preserve leading zeros and punctuation semantics |

Prefer native controls where they satisfy the task. A custom picker requires
the full keyboard, focus and assistive-technology behavior of that control.

## Accept Human Input

- Support names with spaces, accents, apostrophes and different structures.
- Do not use numeric inputs for phone numbers, postal codes or identifiers.
- Provide correct autocomplete purposes and mobile keyboard hints.
- Allow paste and password-manager input, including authentication flows.
- Accept harmless formatting variations; normalize only when the domain
  permits it and avoid silently changing meaning.
- Explain supported dates, units and number formats using the user's locale.
- Do not force repeated entry of known values without a justified need.
- Make masks tolerant of editing, paste, assistive technology and deletion.

For address or identifier lookup, show progress and a meaningful no-result or
failure state. Provide manual entry when compatible with the service rules;
do not turn a helpful lookup into an undocumented availability dependency.

## Validation Timing

The local default is to validate on submission and provide a coherent set of
actionable errors. Add earlier validation only when it prevents meaningful
rework, after sufficient input exists and without disrupting typing. After a
field has failed, timely feedback while correcting it can be useful.

Do not announce an invalid email after the first character or issue a network
request on every keystroke without a deliberate need. Cancel or ignore stale
validation responses so they cannot overwrite newer input state.

Server validation is authoritative. Client checks improve feedback speed and
must remain consistent with server rules. Separate correctable input problems
from service failures and permission errors.

## Error Presentation

On unsuccessful submission:

1. Keep appropriate entered values; explain any sensitive values that must be
   entered again.
2. Show a concise summary when multiple fields or off-screen errors need
   attention, with links to the affected inputs.
3. Move focus intentionally to the summary or relevant error context.
4. Show a specific nearby error for each invalid field and associate it with
   the control; communicate invalid state programmatically.
5. Let the user correct and resubmit without repeating unaffected work.

`Enter an email address in the format name@example.com` is more actionable
than `Invalid value`. Preserve privacy when duplicate-account or recovery
messages could disclose whether someone has an account.

The summary-plus-field approach follows
[GOV.UK validation guidance](https://design-system.service.gov.uk/patterns/validation/).

## Save, Review And Repeat

- Label creation and editing distinctly: `Create customer`, `Save changes`.
- Keep submission reachable so users can discover validation errors; disable
  temporarily during a pending operation with visible feedback and recovery.
- Preserve drafts where task length and sensitivity justify them, with clear
  storage, retention and shared-device behavior.
- Provide review before consequential submission when it helps detect errors.
  Let people change answers without replaying unaffected steps.
- Use `Save and add another` only when repeated entry is a real need; confirm
  the previous save and intentionally reset or carry forward safe fields.
- Define behavior for concurrent edits, duplicates and interrupted requests.

Do not store sensitive drafts in browser persistence by default. Coordinate
retention and access with [Security Standards](../security/README.md).

Saving and recovery behavior follows [Feedback and Recovery](./feedback-and-recovery.md).
The [Customer Registration Example](../examples/templates/ux/customer-registration-example.md)
shows these rules applied to a small CRUD journey.
