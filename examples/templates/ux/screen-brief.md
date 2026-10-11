# Screen And Journey Brief - TASK_NAME

> Copy into the existing feature specification or its linked UX record.
> Replace placeholders; use `Not applicable` with a reason and distinguish
> known business rules from assumptions. Keep the record proportional.

## User And Outcome

- **User/role:** ROLE_AND_ACCESS
- **Task and trigger:** TASK_AND_ENTRY_POINT
- **Completion condition:** OBSERVABLE_RESULT
- **Frequency and context:** DEVICE_FREQUENCY_AND_CONSTRAINTS
- **Evidence:** OBSERVATION_OR_EXISTING_RESEARCH
- **Assumptions/open questions:** UNKNOWN_AND_VALIDATION_PLAN
- **Existing design system/components:** REFERENCE

## Journey

```text
ENTRY -> MAIN_STEPS -> CONFIRMED_OUTCOME -> NEXT_ACTION
```

- **Prerequisites and handoffs:** PRECONDITIONS_AND_DEPENDENCIES
- **Back, cancel and resume:** BEHAVIOR_AND_DRAFT_POLICY
- **Business rules and permissions:** AUTHORITATIVE_SPEC_LINK

## Screen Structure

- **Title and current object/context:** TITLE_AND_IDENTITY
- **Primary action:** LABEL_AND_RESULT
- **Secondary actions:** LABELS_AND_RESULTS
- **Navigation and help:** ROUTES_AND_CONTEXTUAL_HELP

## Field Decisions

| Field | Why needed now | Required/source | Control and accepted input | Correction/validation |
| --- | --- | --- | --- | --- |
| FIELD | PURPOSE | RULE_AND_SOURCE | CONTROL_AND_FORMAT | TIMING_AND_MESSAGE |

Record intentionally omitted fields when their omission is a material design
decision. State which answers are carried forward, editable or invalidated by
another choice.

## Action Contract

Repeat for consequential actions:

```text
Actor and permission:
Label and affected object/scope:
Expected effect and persistence point:
Immediate and pending feedback:
Confirmed outcome and next action:
Failure versus unknown-outcome behavior:
Duplicate and conflict handling:
Cancellation, reversal or undo limits:
```

## State Coverage

| State | User message/evidence | Available action | Data and focus behavior |
| --- | --- | --- | --- |
| Loading/empty/no matches | MESSAGE | ACTION | BEHAVIOR |
| Invalid input | SUMMARY_AND_FIELD_ERROR | CORRECT_AND_RESUBMIT | RETENTION_AND_FOCUS |
| Saving/pending | STATUS | AVAILABLE_ACTION | BEHAVIOR |
| Completed | CONFIRMED_RESULT | NEXT_ACTION | BEHAVIOR |
| Failed/unknown outcome | ACCURATE_STATUS | RECOVERY_OR_RECONCILIATION | BEHAVIOR |
| Conflict/expired session | EXPLANATION | SUPPORTED_RECOVERY | BEHAVIOR |

## Accessibility And Responsive Behavior

- **Labels, groups and descriptions:** SEMANTIC_MAPPING
- **Keyboard and focus:** ORDER_DIALOG_AND_ERROR_BEHAVIOR
- **Status announcements:** MESSAGE_AND_URGENCY
- **Small screens, zoom and long text:** EXPECTED_LAYOUT
- **Applicable criteria/known barriers:** COVERAGE_AND_GAPS

## Acceptance And Validation

| Scenario | Expected user/system outcome | Verification method |
| --- | --- | --- |
| PRIMARY_TASK | RESULT_AND_USER_UNDERSTANDING | METHOD |
| INPUT_ERROR | PRESERVED_WORK_AND_CORRECTION | METHOD |
| INTERRUPTION | ACCURATE_STATE_AND_SAFE_RECOVERY | METHOD |
| KEYBOARD_AND_ASSISTIVE_TECHNOLOGY | COMPLETABLE_TASK | METHOD |

- **Revision/environment:** REVISION_AND_CONTEXT
- **Checks actually performed:** RESULTS_AND_EVIDENCE
- **User sessions or proxy review:** METHOD_AND_OBSERVATIONS
- **Remaining issues/assumptions:** ISSUE_OWNER_AND_REVIEW_TRIGGER
