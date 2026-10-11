# Customer Registration Journey Example

This illustrative brief applies the UX standards to an internal customer
directory. It is a design example, not a tested interface or a universal
customer data model. Configuration and limitations are in the
[template README](./README.md).

## Context And Assumed Business Rules

An authorized support worker needs to create a customer record so colleagues
can find it later, then correct contact details if necessary. Work is frequent
on desktop and occasional on a small screen.

For this example only, the agreed rules are:

- a display name is required to identify a record;
- email and phone are optional contact methods;
- email matches can identify possible duplicates but are not proof of the
  same person;
- creating a record does not create a login or send a message;
- archiving hides the record from the default active list and is reversible;
- customer creation has a server operation identifier and status lookup;
- edits use a version check to detect concurrent changes.

These are hypothetical product decisions. Validate them before applying the
example to a real service. No user research or implementation test has been
performed for this artifact.

## Journey And Screen Choice

```text
Search customers -> inspect possible matches -> create if needed
-> view confirmed record -> edit contact details -> confirm saved change
```

Start with one grouped form because the task is short and repeated. The page
title is `Create customer`; brief supporting text explains that creation does
not send an invitation. Reuse the application's existing form controls.

| Field | Purpose and status | Input behavior |
| --- | --- | --- |
| Display name | Required for identification | Text; accept common name characters and organization names |
| Email | Optional contact method | Email input; allow paste and explain invalid format on submission |
| Phone | Optional contact method | Telephone input; preserve meaningful international formatting |

Do not ask for birth date, identity documents or address because the stated
task does not use them. Mark optional fields in words. Use `Create customer`
as the primary action and `Cancel` as secondary navigation.

## Create Action Contract

| Moment | User experience | System behavior |
| --- | --- | --- |
| Submit | `Creating customer...`; values remain visible | Validate and submit with a stable operation identifier |
| Invalid input | Summary linked to fields and specific messages | No record created; preserve appropriate values |
| Possible duplicate | Explain match and offer to inspect it | Do not merge solely on the matching email |
| Confirmed create | Record page states `Customer created` | Show server-confirmed identity and persisted details |
| Server failure | Explain failure and correction/retry route | Restore usable controls; do not claim success |
| Response lost | Explain that the result is not yet confirmed | Query the operation before retrying with the same identifier |

If the user inspects a possible duplicate, preserve their input so they can
return. Display only records they are authorized to see. Any override or merge
must follow the real application's permissions and business rules.

## Editing And Leaving

Prefill current values and label the action `Save changes`. After a confirmed
save, show the updated record and an accessible `Changes saved` status.

If a version conflict occurs, retain the user's draft and offer a comparison
with the latest record. Do not silently overwrite. On meaningful unsaved
navigation, offer `Keep editing` and `Discard changes`. There is no automatic
browser-persistent draft in this example.

After returning to the list, preserve the previous search and filters. If the
new or edited record does not match them, explain why it is not in the current
results and offer a direct link to it.

## Archiving

The action says `Archive customer`. Explain that it removes the customer from
the default active list and can be reversed. Confirm the new state after the
server response and provide a working restore path to authorized users.

This example does not authorize irreversible deletion. A different retention
or deletion requirement needs its own consequence and recovery decisions.

## Accessibility And Validation Plan

- Associate labels, optional hints and errors with each input.
- Move focus to the error summary on a failed multi-field submission.
- Announce routine saving/result status without repeatedly moving focus.
- Preserve logical keyboard order and readable reflow on a narrow screen.
- Verify that repeated submission cannot create duplicate effects.
- Exercise invalid input, lost response, permission failure and edit conflict.
- Observe a representative worker creating and correcting a synthetic record
  without coaching, then ask what was saved and whether any message was sent.

Expected outcome: the worker can find the resulting record, explain the
operation's actual effects and recover from a mistake. Record execution
evidence separately; none is implied by this plan.
