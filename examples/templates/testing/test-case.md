# TC-{CAPABILITY}-{NNN} - {expected behavior}

| Field | Value |
| --- | --- |
| Traceability | `{requirement, acceptance criterion, contract, risk, defect or incident}` |
| Risk | `{critical, high, medium or low - consequence covered}` |
| Classification | `{level} / {type}` |
| Automation | `{automated, candidate, manual or not applicable}` |

## Objective

{One sentence describing the behavior or risk being verified.}

## Preconditions

- {Required system or entity state.}
- {Acting identity, role and permissions, when relevant.}
- {Configuration, time or dependency assumption, when relevant.}

## Test Data

| Data | Value or reproducible rule |
| --- | --- |
| `{name}` | `{synthetic value, boundary or generation rule}` |

## Scenario

**Given** {relevant initial context} \
**And** {additional condition, when necessary} \
**When** {one primary action or event} \
**Then** {observable expected outcome} \
**And** {additional observable outcome, when necessary}

## Cleanup

- {Required restoration, or remove this section when no cleanup is needed.}

## Evidence Expectations

- {Required evidence when pass or fail would otherwise be ambiguous, or remove
  this section.}

## Automation

- `{automated test path or stable report identifier, or remove this section}`

Execution result, tested build, environment, executor, timestamp, actual
result, collected evidence and defect links belong in a separate execution
record.
