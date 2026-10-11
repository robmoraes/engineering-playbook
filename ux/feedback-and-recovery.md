# Feedback And Recovery

Every meaningful action needs a clear relationship between user intent, the
system's actual state and the visible result. Design that relationship before
connecting a button to an API.

## Action Contract

For each consequential action, capture:

```text
Actor and permission:
Label and object/scope:
Prerequisites:
Expected effect and persistence point:
Immediate feedback:
Pending, completed, failed and unknown states:
Duplicate and concurrent-action behavior:
Recovery, cancellation or undo:
Next step and durable confirmation, if needed:
```

This is a local engineering convention. It connects the visibility and control
heuristics in [NN/G's usability guidance](https://www.nngroup.com/articles/ten-usability-heuristics/)
to implementable behavior.

## State Coverage

| State | What the user needs | Required behavior |
| --- | --- | --- |
| Loading | What is being retrieved | Stable layout, progress indication and failure path |
| Empty | Why there is no content yet | Appropriate first action |
| No matches | Which search/filter produced no results | Clear or adjust filters |
| Read-only or restricted | What is possible with current access | Explanation and supported next step |
| Invalid input | What to correct | Field context, retained values and correction path |
| Saving | Whether the request is still pending | Visible status and duplicate-action control |
| Completed | What changed | Confirmed result and relevant next action |
| Failed | What did not complete | Accurate explanation and safe recovery |
| Outcome unknown | Whether the change might have succeeded | Status reconciliation before unsafe retry |
| Conflict | Which state changed elsewhere | Review and reconcile without silent overwrite |
| Session expired | How to regain access | Appropriate input preservation and return to task |

Use the states that apply to the workflow. Loading or an error is not an empty
dataset; do not show `No customers yet` while a request has failed.

## Saving And Truthful Completion

The interface MUST report saved or completed state only after the relevant
system has confirmed it. An accepted background request means queued or
processing, not finished.

- Show immediate acknowledgment and meaningful waiting status.
- Keep submitted values visible while a request is pending.
- Restore a usable control state after failure.
- Give long operations a status location that survives navigation when needed.
- Announce important status changes accessibly without stealing focus.
- Use durable confirmation for consequential results, with the relevant object
  or reference and next steps. A short-lived toast may supplement it.

Completion guidance is informed by
[GOV.UK confirmation pages](https://design-system.service.gov.uk/patterns/confirmation-pages/).

## Retry And Unknown Outcome

A network timeout may occur after the server committed a change. The local
standard requires the UI and server contract to account for this ambiguity.

For record creation, payments or sending messages, use a supported operation
identifier, idempotency mechanism or reconciliation lookup before retrying.
Do not assert failure simply because the browser did not receive a response.

Example message when accurate:

```text
We could not confirm whether the customer was created.
Check the operation status before creating it again.
```

The status route must actually exist and be accessible. Disabling a button
prevents some repeated clicks; it does not handle retries, multiple tabs or
concurrent requests. Coordinate with
[Architecture: State, Reliability and Scale](../architecture/state-reliability-and-scale.md).

## Explicit Save And Autosave

Use explicit save as a simple default for record forms. Autosave may fit
continuous editing when users can understand its scope and undo behavior.

If autosave is used, expose unsaved, saving, saved and failed states; define
when persistence happens, handle overlapping changes and provide recovery.
Make it clear that navigating away is not a cancellation of already saved
changes. Keep destructive or externally visible actions explicit.

When leaving an explicit-save form, warn about meaningful unsaved changes.
Do not warn on an unchanged form or an ordinary successful navigation. Browser
unload warnings are not a durable draft strategy and may not run reliably.

## Delete, Archive And Undo

- Name the actual effect: archive, deactivate, remove access or delete.
- Identify the affected object and explain material downstream effects.
- Offer undo when reversal truly exists, with its time limit and scope.
- Use review/confirmation for costly or irreversible consequences.
- Put the action name on the confirming control, not only `Yes` or `OK`.
- Give cancellation a clear path and avoid initial focus on a destructive
  confirmation by default.

Do not require a confirmation dialog for every routine save. The WCAG error
prevention criterion allows several approaches for covered transactions,
including reversal, error checking or review before commitment.
[WCAG error prevention](https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data.html)

## Conflicts And Partial Success

When a record changes during editing, preserve the user's work and show the
latest authoritative state or a supported comparison path. Avoid silently
overwriting either version. State who or what changed it only when known and
permitted to disclose.

For batch actions, report successes and failures separately. A result such as
`8 customers archived; 2 could not be archived` must identify a supported way
to inspect or retry the failed items without repeating completed effects.

## Error Copy

Explain the situation, whether work was preserved and the next possible action.
Use a reference identifier when it helps support; keep stack traces, secrets
and sensitive implementation details out of the message.

Never show a retry, undo, cancellation or support promise that the product
cannot fulfill. Keep essential recovery available after a toast disappears.
