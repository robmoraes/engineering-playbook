# Test Case Standards

A test case is a reusable verification artifact for one behavior or closely
related risk. It should give a tester enough context to execute the check and
interpret the outcome while remaining small enough to review, maintain and
automate.

This standard combines a lightweight metadata envelope with a
behavior-oriented scenario. The metadata provides ownership and traceability;
the scenario expresses context, event and observable outcome using
`Given`, `When` and `Then` semantics.

## Design Principles

Test cases in this playbook SHOULD be:

- **behavior-focused:** describe what the system must do, not how it is
  implemented;
- **risk-aware:** explain the failure or consequence the case helps detect;
- **independent where practical:** avoid relying on execution order or state
  left by another case;
- **deterministic:** make data, time, identity and dependency assumptions
  controllable;
- **traceable:** connect to a requirement, acceptance criterion, contract,
  incident or product risk;
- **reusable:** keep execution-specific results outside the case definition;
- **proportional:** add detail only when it improves execution, diagnosis,
  coordination or governance.

Independence is not an excuse to duplicate expensive setup. Shared fixtures
and suite-level preparation are acceptable when the dependency is explicit
and failure diagnosis remains clear.

## When To Create a Maintained Test Case

Create or retain a test case when one or more of these conditions apply:

- behavior is critical to a user, operator or integration;
- failure can cause security, privacy, financial or data integrity impact;
- the check is part of smoke, regression, release or acceptance testing;
- multiple people or teams need a shared execution contract;
- setup, data or expected behavior is not obvious from the automated test;
- a defect, incident or recurring regression needs durable coverage;
- manual execution must be repeatable or auditable.

A separate maintained case is usually unnecessary for a trivial assertion
whose intent, setup and expected result are already clear in a nearby automated
test. Use an exploratory charter instead when the goal is learning about an
uncertain product area rather than repeating a predetermined check.

## Standard Structure

Every maintained test case MUST contain the following information unless the
repository's test management system supplies it unambiguously:

| Field | Requirement |
| --- | --- |
| Identifier and title | Stable identifier plus a short statement of expected behavior |
| Traceability | Requirement, acceptance criterion, contract, risk, defect or incident covered |
| Risk or priority | Consequence addressed or execution importance |
| Test classification | Relevant level and type, such as API/functional or system/security |
| Automation state | Automated, candidate, manual or not applicable |
| Objective | One sentence explaining what is verified |
| Preconditions | Required system state, identity, permissions and dependencies |
| Test data | Concrete values or deterministic rules for generating them |
| Scenario | Initial context, primary action or event and expected outcomes |
| Cleanup | Required restoration when the case creates persistent side effects |

Add environment, feature flag, locale, clock, device, browser, dependency or
evidence details only when they materially affect execution or interpretation.
Remove inapplicable optional sections rather than leaving empty placeholders.

## Identifiers and Titles

Use this default identifier when a test management tool does not provide one:

```text
TC-<CAPABILITY>-<NNN>
```

Examples:

```text
TC-INV-003
TC-AUTH-012
TC-CHECKOUT-041
```

The capability code SHOULD be stable domain language rather than a screen,
class or service name. Keep identifiers after retirement; do not reuse them
for different behavior.

Titles state the expected behavior:

```text
Good
TC-INV-003 - Reject an expired invitation
TC-AUTH-012 - Prevent a suspended user from creating a session

Avoid
TC-INV-003 - Invitation test
TC-AUTH-012 - Test login button
```

When cases are stored as files, use lowercase kebab-case while preserving the
identifier inside the document:

```text
tc-inv-003-reject-expired-invitation.md
```

## Traceability and Risk

A case MUST link to at least one source of expected behavior or risk:

- feature specification or acceptance criterion;
- user story, issue or business rule;
- API, event, schema or command contract;
- threat, control or quality risk;
- defect or incident that requires regression coverage.

Traceability should be navigable in both directions when the tool supports it:
reviewers can see which cases cover a requirement, and a case author can find
the current source of expected behavior.

Do not create links only for appearance. If the source is obsolete or too
vague to determine the expected result, clarify it before treating the case as
authoritative.

Use risk to decide test depth and execution order. A practical classification
is:

| Risk | Typical treatment |
| --- | --- |
| Critical | Must cover before release; automate stable regression where practical |
| High | Include in targeted regression and release decisions |
| Medium | Execute according to changed scope and available evidence |
| Low | Prefer lightweight or exploratory coverage unless repetition justifies automation |

Risk describes consequence and likelihood. Priority describes when the team
chooses to execute the case. Record both only when that distinction changes a
decision.

## Preconditions

Preconditions establish a known starting state. Include only facts needed to
understand or reproduce the scenario:

- user identity, role and permission state;
- relevant entity and lifecycle state;
- feature flags or configuration;
- dependency availability or simulated behavior;
- locale, timezone or controlled clock;
- environment capability that differs from the normal test baseline.

```text
Good
- A pending invitation exists for a user without an account.
- The invitation expires seven calendar days after creation.
- The test clock is fixed at 2026-07-09T09:00:00Z.

Avoid
- The environment is ready.
- The tester has the necessary data.
```

Do not repeat shared environment setup in every case. Link to a versioned
fixture, suite prerequisite or environment contract when that is the actual
source of truth.

## Test Data

Test data MUST be concrete or reproducible. State exact values when they make
the boundary or expected result understandable; otherwise state a generation
rule and required properties.

```markdown
| Data | Value or rule |
| --- | --- |
| Account | Synthetic active account with no existing invitations |
| Invitation creation | `2026-07-01T12:00:00Z` |
| Invitation expiry | `2026-07-08T12:00:00Z` |
| Acceptance attempt | `2026-07-09T09:00:00Z` |
```

- Use synthetic or approved masked data.
- Never place credentials, tokens or unnecessary personal data in a case.
- Identify values designed to exercise a boundary or equivalence class.
- Control time, randomness and external responses when they affect the result.
- State cleanup requirements for persistent, billable or externally visible
  data.

Use parameterized data when the behavior and setup remain the same:

```markdown
| Role | Expected status | Expected code |
| --- | --- | --- |
| Administrator | `201` | none |
| Member | `403` | `insufficient_permission` |
| Suspended administrator | `403` | `account_suspended` |
```

Create separate cases when a variation represents a different business rule,
risk, setup path or expected state transition. A large data table should not
hide several unrelated behaviors.

## Behavior-Oriented Scenario

Use `Given`, `When` and `Then` semantics:

- `Given` describes the relevant initial context;
- `When` describes one primary action or event;
- `Then` describes an observable outcome;
- `And` or `But` adds conditions or outcomes without changing their role.

Prefer three to five expressive steps. More steps are acceptable when the
workflow genuinely needs them, but a long scenario often signals multiple
behaviors or excessive interface detail.

```text
Scenario: expired invitation cannot be accepted
Given an invitation expired on 2026-07-08T12:00:00Z
And the invitee does not have an account
When the invitee attempts acceptance on 2026-07-09T09:00:00Z
Then the system rejects the request with code invitation_expired
And no account or authenticated session is created
```

Use the domain language spoken by product, engineering and QA. Do not expose
selectors, table names, internal classes or service calls unless that
technical interface is itself the subject of the test.

Use a procedural table only when the sequence itself is under test or a manual
operation cannot be expressed clearly as one business event:

```markdown
| Step | Action | Expected result |
| --- | --- | --- |
| 1 | Submit the valid approval request | The request enters `pending` state |
| 2 | Approve as an authorized reviewer | The request enters `approved` state |
```

Do not duplicate a `Then` outcome in a procedural table. Choose the clearest
single representation for the case.

## Expected Results

An expected result MUST be observable by the relevant actor or interface. It
may include:

- returned value, status and stable error code;
- visible user state or accessible message;
- published event or integration response;
- authorized state transition;
- absence of an unauthorized or destructive effect;
- operational signal promised by a specification.

```text
Good
- The API returns HTTP 410 with code invitation_expired.
- No account or authenticated session is created.

Avoid
- The request fails correctly.
- The invitation row has expired = 1.
```

Internal state may be asserted in a component or persistence-level test. In an
acceptance or system case, prefer the public contract and externally visible
effect so implementation changes do not create false regressions.

## Complete Example

```markdown
# TC-INV-003 - Reject an expired invitation

| Field | Value |
| --- | --- |
| Traceability | `SPEC-INV-01 / AC-04` |
| Risk | Critical - unauthorized access through an invalid invitation |
| Classification | API / functional and security |
| Automation | Automated |

## Objective

Verify that an expired invitation cannot create an account or session.

## Preconditions

- The invitee does not have an account.
- An invitation exists with a seven-day validity period.
- The test clock can be controlled.

## Test Data

| Data | Value |
| --- | --- |
| Created at | `2026-07-01T12:00:00Z` |
| Expires at | `2026-07-08T12:00:00Z` |
| Attempted at | `2026-07-09T09:00:00Z` |

## Scenario

**Given** the invitation expired at `2026-07-08T12:00:00Z` \
**And** the invitee does not have an account \
**When** the invitee attempts to accept the invitation \
**Then** the API returns HTTP `410` \
**And** the response code is `invitation_expired` \
**And** no account or authenticated session is created

## Cleanup

- Delete the synthetic invitation.

## Automation

- `tests/api/invitations/test_expired_invitation.py`
```

Start new cases from the copyable
[Test Case Template](../examples/templates/testing/test-case.md).

## Coverage Selection

Do not produce one case for every theoretical combination. Select cases from
requirements and risk using appropriate test design techniques:

| Concern | Useful technique or case |
| --- | --- |
| Valid alternatives | Equivalence partitions or representative examples |
| Numeric, date or size limits | Boundary value analysis |
| Interacting rules | Decision table |
| Entity lifecycle | State transition coverage |
| User or service authority | Role and permission matrix |
| Ordered workflow | Scenario or end-to-end path |
| Unknown behavior or usability | Exploratory charter |

For a meaningful feature, consider the following coverage and record why a
category is omitted when its risk is material:

- primary successful path;
- expected business failures;
- boundary values;
- identity, role and permission differences;
- state transitions and invalid transitions;
- time, timezone, locale and concurrency behavior;
- integration failure, retry or recovery behavior;
- security, privacy, accessibility and data integrity outcomes.

The list is a risk prompt, not a requirement to multiply every case by every
category.

## Automation

A test case and an automated test are related but distinct artifacts. A case
explains the verification contract; automation implements repeatable execution.

Prioritize automation when the check is:

- critical or frequently used for regression;
- deterministic and stable enough to maintain;
- expensive or error-prone to repeat manually;
- needed as fast feedback in a pipeline;
- run across many datasets, contracts or configurations.

Keep a case manual when human observation is material, the behavior is still
changing rapidly or automation cost exceeds likely feedback value. Do not mark
a case automated only because a script exists; the script must assert the
current expected result and run in the intended feedback path.

When practical, record the automated test path, stable test name or report
identifier. Avoid copying implementation steps into the case.

## Execution Records and Evidence

Execution data belongs in a test management system, pipeline report or
separate execution record. It MUST NOT overwrite the reusable case definition.

An execution record SHOULD capture:

| Field | Purpose |
| --- | --- |
| Test case and revision | Identifies the exact verification contract used |
| Build or source revision | Identifies the tested software |
| Environment and relevant configuration | Defines where and under which material conditions it ran |
| Executor and timestamp | Identifies manual tester or automation run and time |
| Result | Passed, failed, blocked, skipped or not run |
| Actual result | Records the observed deviation or blocking condition when relevant |
| Evidence | Links to concise, access-controlled output supporting the result |
| Defect | Links a confirmed deviation without duplicating defect ownership |

Capture the smallest evidence that makes the result credible and diagnosable.
Prefer structured responses, logs, traces or reports over screenshots when
they communicate the behavior more precisely. Evidence MUST follow applicable
retention, access and sensitive-data rules.

## Lifecycle and Change Control

Review a case when:

- accepted behavior or its source specification changes;
- a contract, permission model or state transition changes;
- automation no longer matches the documented case;
- a defect or incident reveals missing coverage;
- repeated execution finds ambiguous setup or expected results;
- the case is flaky, redundant or no longer influences a decision.

Use the following lifecycle states where explicit state is useful:

```text
draft -> active -> superseded or retired
```

Do not silently rewrite historical execution evidence after changing a case.
Execution systems should preserve the case revision or snapshot that was used.

## Anti-Patterns

Avoid:

- titles such as `Test login` that do not state an outcome;
- preconditions such as `system is ready` or `valid data exists`;
- several unrelated user goals in one long case;
- step-by-step UI navigation when UI behavior is not under test;
- expected results such as `works`, `success` or `fails correctly`;
- production identities, secrets or copied customer data;
- duplicate cases differing only by values that belong in a dataset;
- cases with no requirement or risk link;
- automation status that is not verified against the actual suite;
- screenshots collected by default without diagnostic value;
- passed results recorded against an unknown build or environment.

## Definition of Ready

A test case is ready for execution when:

- [ ] its source behavior or risk is identified;
- [ ] the title and objective describe one clear verification goal;
- [ ] preconditions and data are reproducible;
- [ ] the action or event is unambiguous;
- [ ] expected outcomes are observable and bounded;
- [ ] identity, permissions, time and dependencies are explicit where relevant;
- [ ] cleanup and evidence needs are stated where relevant;
- [ ] another tester can execute it without oral context.

## Review Checklist

- [ ] Does the case protect behavior or risk that matters?
- [ ] Is it the smallest useful case for that behavior?
- [ ] Is traceability current and navigable?
- [ ] Are data and environment assumptions deterministic?
- [ ] Does the scenario use domain language rather than implementation detail?
- [ ] Can pass or fail be decided from the expected results?
- [ ] Are protected data and credentials excluded?
- [ ] Would parameters remove duplication without hiding different rules?
- [ ] Does automation, when declared, still implement the case?
- [ ] Are execution history and evidence stored separately from test design?

## Reference Basis

This standard adapts ISO/IEC/IEEE test documentation guidance rather than
requiring its complete document set. ISTQB guidance informs traceability,
risk-based selection and established test design techniques. Cucumber's
Gherkin guidance informs the concise context-event-outcome scenario structure;
using that structure does not require adopting Cucumber as a tool.

See [Testing References](./references.md) for source links and adoption notes.
