# Spec-Driven Development Standards

Spec-driven development is a delivery and architecture practice where the
specification is the working agreement for what the system must do. Code,
tests, plans and implementation tasks are derived from the spec and checked
against it. The goal is not more documentation; the goal is fewer ambiguous
changes and less implementation drift.

This playbook uses spec-driven development for work where behavior,
constraints, contracts or user outcomes need to be agreed before implementation
starts.

## Core Model

Use these concepts explicitly:

| Concept | Meaning | Typical artifact |
| --- | --- | --- |
| Intent | Why the change exists and who benefits | issue, brief or spec introduction |
| Specification | What behavior and constraints must be true | `spec.md` |
| Acceptance example | Concrete scenario that proves expected behavior | scenario, example table or executable test |
| Contract | Machine-readable interface or data agreement | OpenAPI, schema, event contract or CLI contract |
| Plan | How the system will satisfy the spec | `plan.md` |
| Task list | Ordered implementation work with validation steps | `tasks.md` |
| Verification evidence | Proof that implementation matches the spec | tests, checks, review notes and demo evidence |
| Drift | Difference between spec, tests, code or shipped behavior | review finding, follow-up issue or spec update |

A specification is not a wish list. It is a small, testable contract between
product intent, engineering decisions and delivered behavior.

## Non-Negotiable Defaults

- Write the spec before implementation for any meaningful feature, workflow,
  API contract, data migration or operational behavior change.
- Specify what and why before choosing how. Technology choices belong in the
  plan unless they are already fixed constraints.
- Keep specs small enough to review and merge through trunk-based development.
- Resolve material ambiguity before planning. Do not let implementation
  discover requirements that should have been clarified.
- Include concrete acceptance examples for behavior that users, operators or
  integrators rely on.
- Use machine-readable contracts where the boundary is machine-consumed:
  OpenAPI for HTTP APIs, schemas for events, migration contracts for data and
  command contracts for CLIs.
- Treat tests as verification of the spec, not as a substitute for shared
  understanding.
- Update the spec when accepted behavior changes. Do not let stale
  documentation remain authoritative.
- Keep architecture decisions in ADRs when the spec requires a consequential
  boundary, datastore, dependency, runtime or cost change.

## When To Use

Use this standard when a change has one or more of these traits:

- new user workflow or meaningful behavior change;
- public or internal API contract;
- data model, migration or lifecycle rule;
- security, privacy, compliance or permission behavior;
- cross-service interaction or event contract;
- operational behavior such as retries, recovery, alerts or rollback;
- AI-assisted implementation where precise context reduces hallucinated code;
- high ambiguity, multiple stakeholders or costly rework risk.

For a typo, copy edit or obvious one-line correction, a full spec is not
required. The practice should reduce uncertainty, not become ceremony.

## Standard Workflow

The default workflow is:

```text
Intent -> Spec -> Clarify -> Check -> Plan -> Tasks -> Implement -> Verify
```

| Phase | Output | Gate |
| --- | --- | --- |
| Intent | Problem, users, outcome and scope boundary | Is the change worth doing now? |
| Spec | Required behavior, acceptance criteria and constraints | Can a reviewer tell what must be true? |
| Clarify | Open questions resolved or explicitly deferred | Are important ambiguities gone? |
| Check | Spec quality checklist | Is the spec testable and bounded? |
| Plan | Architecture, data, API, security and operational approach | Does the approach satisfy the spec without hidden scope? |
| Tasks | Ordered implementation and validation steps | Can work proceed incrementally? |
| Implement | Code, docs, migrations and tests | Does each change trace back to the spec? |
| Verify | Test results, contract checks and review evidence | Does shipped behavior match the spec? |

For complex work, repeat the loop in slices. A spec may define the larger
outcome while tasks implement one narrow vertical path at a time.

## Repository Structure

Persistent specifications SHOULD live near the code or book they govern. For
application repositories, use:

```text
specs/
  001-invite-team-member/
    spec.md
    plan.md
    tasks.md
    contracts/
      openapi.yaml
    examples/
      invitation-expiry.md
```

For documentation-only repositories, place the spec under the relevant book or
under `examples/decision-examples/` when it demonstrates the practice rather
than governing shipped behavior.

Number prefixes keep related artifacts sortable in review order. The slug
should name durable behavior, not the implementation technique.

## Specification Format

A feature spec SHOULD include:

```markdown
# Feature: <name>

## Intent

Problem:
Users or stakeholders:
Desired outcome:
Non-goals:

## Scope

In scope:
Out of scope:
Assumptions:
Dependencies:

## Behavior

1. Requirement.
2. Requirement.

## Acceptance Examples

Scenario:
Given ...
When ...
Then ...

## Data and Contracts

Inputs:
Outputs:
API/schema/event changes:
Persistence changes:

## Quality Attributes

Security:
Privacy:
Accessibility:
Performance:
Reliability:
Observability:

## Rollout and Operations

Migration:
Feature flag or configuration:
Rollback:
Monitoring:

## Open Questions

- Question, owner and deadline.
```

Remove sections that genuinely do not apply. Do not leave empty placeholders
that create false confidence.

## Writing Requirements

Good requirements are observable and bounded:

```text
Good
- A pending invitation expires 7 calendar days after creation.
- Expired invitations cannot be accepted and return error code
  invitation_expired.
- Admins can resend an expired invitation, creating a new expiry window.

Avoid
- Handle invitations better.
- Make invitation flow robust.
- Use a better token system.
```

Use product-domain language in the spec. Technical names may appear in the
plan, contracts or ADRs, but the spec should remain readable by non-authors.

Each requirement should be one of:

- a user-visible behavior;
- a domain rule;
- an interface contract;
- a data lifecycle rule;
- an operational or security constraint;
- a quality attribute with measurable expectation.

## Acceptance Examples

Acceptance examples anchor the spec in concrete behavior. Use the simplest
format that reviewers and automation can maintain:

```text
Scenario: expired invitation cannot be accepted
Given an invitation created on 2026-05-01
And the invitation expires after 7 calendar days
When the invitee accepts it on 2026-05-09
Then the system rejects the invitation
And the response code is invitation_expired
And no user account is created
```

Examples should cover:

- the main successful path;
- expected failures;
- boundary values;
- permission differences;
- data state transitions;
- relevant time, locale or concurrency behavior;
- operational outcomes where operators need evidence.

Do not turn examples into brittle UI scripts unless UI behavior is the thing
being specified. A domain or API test may be the better executable form.

## Technical Plan

The plan translates the spec into design. It SHOULD state:

- affected modules, services and ownership boundaries;
- data model and migration approach;
- API, event, CLI or integration contracts;
- security, privacy and access implications;
- observability and operational behavior;
- rollout, compatibility and rollback path;
- alternatives considered and why they were rejected;
- ADRs required by the architecture change rule.

The plan must not silently add product behavior. If the plan discovers new
behavior, update the spec or record it as explicitly out of scope.

## Task Breakdown

Tasks should be ordered for incremental validation:

```text
1. Add domain rule and unit tests for invitation expiry.
2. Add persistence field and migration for expiration timestamp.
3. Update accept-invitation API contract and error code.
4. Add integration test for expired invitation rejection.
5. Add admin resend behavior and acceptance example.
6. Add logs/metrics for rejected expired invitations.
7. Update user-facing documentation or copy.
```

Each task SHOULD identify its validation route. Avoid task lists that merely
repeat file names without behavior.

## AI-Assisted Development

When using an AI coding agent, the spec is the primary context contract:

- provide the spec, plan, relevant existing files and repository standards;
- ask the agent to identify ambiguity before editing;
- require changes to trace back to requirements or tasks;
- keep implementation slices small enough for review;
- verify generated code with normal tests, linters and human review;
- reject changes that invent behavior not present in the spec or plan.

AI output does not lower the standard for tests, security review or
architecture fit. The spec narrows the agent's search space; it does not
replace engineering judgment.

## Verification and Drift Control

Every spec-driven change SHOULD finish with explicit verification:

- acceptance examples covered by automated tests where practical;
- contract validation for APIs, events or schemas;
- migration or data lifecycle checks when state changes;
- security and permission checks for protected behavior;
- observability checks for logs, metrics or alerts promised by the plan;
- review of open questions, deferred scope and follow-up issues.

If implementation intentionally differs from the spec, update the spec in the
same change or document the follow-up. Do not merge known drift unless the PR
states the risk and owner.

## Relationship To ADRs and Tests

Specs, ADRs and tests have different jobs:

| Artifact | Answers | Changes when |
| --- | --- | --- |
| Spec | What must the system do and why? | Behavior or externally visible constraints change |
| ADR | Why did we choose this consequential design? | Architecture decision is made, superseded or retired |
| Test | Does implementation still satisfy the expected behavior? | Behavior, contract or regression coverage changes |

Do not hide architecture decisions inside a spec. Do not use ADRs as feature
requirements. Do not rely on tests alone to explain product intent.

## Pull Request Expectations

A pull request implementing a spec-driven change SHOULD include:

- spec path;
- summary of behavior delivered;
- verification evidence;
- contract or migration impact;
- open questions or intentionally deferred scope;
- links to ADRs where needed.

The PR should be small enough to review. If the spec is large, split
implementation into multiple short-lived trunk-based branches while preserving
the same spec as the source of truth.

## Reference Basis

This standard adopts external guidance as follows:

- GitHub Spec Kit informs the spec, plan, tasks and implementation phase model
  for AI-assisted development.
- Behavior-Driven Development and Specification by Example inform the use of
  concrete examples to create shared understanding and executable
  documentation.
- OpenAPI informs machine-readable HTTP API contracts.
- This playbook's ADR standard defines where consequential architecture
  choices are recorded.

See [Architecture References](./references.md) for source links and adoption
notes.

## Review Checklist

- [ ] Does the spec state intent, users, scope and non-goals?
- [ ] Are requirements observable, bounded and free of hidden implementation
      choices?
- [ ] Are material ambiguities resolved before planning?
- [ ] Are acceptance examples concrete enough to guide tests?
- [ ] Are API, event, data or CLI contracts represented in machine-readable
      form where appropriate?
- [ ] Does the plan identify architecture, security, data and operational
      consequences?
- [ ] Are tasks ordered for incremental implementation and validation?
- [ ] Is generated or assisted code checked against the spec rather than
      accepted as authoritative?
- [ ] Are tests and verification evidence linked to the acceptance examples?
- [ ] Are spec/code/test differences either fixed or explicitly tracked?
