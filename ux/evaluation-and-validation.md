# Evaluation And Validation

Treat each important UX choice as a hypothesis about real use. Verify behavior
and observe task completion before concluding that a screen is intuitive.

## Three Types Of Evidence

| Method | What it can establish | Limitation |
| --- | --- | --- |
| Heuristic walkthrough | Likely issues in language, hierarchy, feedback and control | Reviewer judgment is not observed user behavior |
| Functional and accessibility checks | Whether specified interactions work in tested conditions | Passing selected checks does not prove usability or complete conformance |
| Usability session | How representative people understand and perform a task | Findings depend on participants, scenarios and context |

Use all three proportionally. For a minor copy edit, a focused review may be
enough. A new registration flow needs end-to-end checks and direct evidence
about understanding where feasible.

## A Lightweight Usability Session

1. Identify the main uncertainty, such as whether users understand when a
   record is saved.
2. Recruit actual or likely users, including relevant roles and access needs.
3. Give a realistic goal and starting context, using synthetic data.
4. Let the participant attempt the task without click-by-click instructions.
5. Observe hesitation, mistakes, recovery, completion and interpretation.
6. Ask neutral follow-up questions about what they expected and understood.
7. Fix the most consequential problems and repeat the relevant task.

Example task: `A new customer has contacted you. Record their details so a
colleague can find them, then correct their phone number.`

Avoid: `Click Add, enter the fields, press Save and then click Edit.` The second
script tests following instructions and hides navigation problems.

This method follows [GOV.UK moderated usability testing](https://www.gov.uk/service-manual/user-research/using-moderated-usability-testing).
Synthetic data is this playbook's local default for lightweight sessions;
GOV.UK also discusses using participants' real data when appropriate. Any such
use needs deliberate handling of access, consent and retention.

Small iterative sessions are useful for qualitative learning. There is no
universal five-person guarantee, required percentage of defects discovered or
sample size that proves accessibility. Cover materially different user groups
and tasks; use a suitable study design for quantitative claims.

## When Users Are Unavailable

Review the journey with a colleague unfamiliar with the implementation, use
known support evidence and exercise realistic scenarios. Record this as a
proxy review. Keep assumptions and the later user-validation opportunity
visible; do not relabel a colleague walkthrough as representative research.

## Minimum Screen Verification

Check the relevant journey with:

- keyboard-only navigation, activation, errors and focus recovery;
- a narrow viewport, zoom, longer translated text and realistic content;
- representative screen-reader output for labels, states and messages;
- empty data, many records, missing optional data and permission boundaries;
- invalid input, duplicate requests, slow responses and server failure;
- successful persistence, reload, interrupted submission and safe retry;
- unsaved changes, back navigation and concurrent edits where applicable.

Use existing [Testing Standards](../testing/README.md) for repeatable cases.
Automate stable, important behavior such as field-error mapping and duplicate
effects. Keep human evaluation for whether the labels and flow make sense.

## What To Measure

Select measures tied to the goal:

| Signal | Interpretation |
| --- | --- |
| Successful completion | The intended result exists and is understood |
| Assistance or critical errors | The flow prevents independent progress or causes wrong outcomes |
| Time and repeated effort | Work that may be reduced, interpreted with task complexity |
| Abandonment by stage | A possible obstacle to investigate, not proof of its cause |
| Corrections and support requests | Understanding or recovery may need improvement |

Record denominators and contexts. Report `3 of 4 observed participants` for a
small session, not an unsupported population success percentage. Do not
optimize completion by hiding consequences or making refusal difficult.

## Protect Research And Telemetry Data

Collect only evidence needed for the decision. Agree to recordings with
participants, set access and retention, and use synthetic data by default.
Avoid capturing passwords, field contents or unnecessary personal identifiers
in analytics. Session replay requires deliberate privacy review and effective
masking, not an automatic default.

Follow [Security: Repository and Data Hygiene](../security/repository-and-data-hygiene.md).

## Prioritize Findings

Fix blocked access, data loss, unintended consequential actions and false
completion before cosmetic inconsistencies. Then prioritize by task impact,
frequency, number of affected people and recovery difficulty. A rare barrier
can still be critical for the people affected by it.

Record the issue, observation, context, severity rationale, owner, correction
and retest evidence. Keep heuristic concerns distinct from observed failures.

## Delivery Evidence

```text
Journey and revision:
Checks performed and environments:
Observed user sessions or proxy review:
Successful and failed scenarios:
Known assumptions and limitations:
Issues resolved and retest evidence:
Remaining issues, owners and review triggers:
```
