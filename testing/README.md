# Software Testing Standards

Standards for designing, executing and maintaining software tests as
risk-focused verification artifacts. Testing provides evidence about product
behavior; it does not exist merely to complete a delivery stage.

## Testing Position

The default testing posture in this playbook is:

1. Derive tests from expected behavior, contracts and material product risks.
2. Keep test cases concise enough to review and execute without oral context.
3. Separate stable test design from execution history and collected evidence.
4. Verify observable outcomes rather than incidental implementation details.
5. Automate repeatable checks when their feedback value justifies maintenance.
6. Use exploratory testing to investigate uncertainty that scripted cases do
   not cover well.

A large test inventory is not evidence of quality. A useful test suite makes
important behavior and residual risk visible to the delivery team.

## Operating Contexts

| Context | Practical default |
| --- | --- |
| **Personal/lab** | Automate the critical path and retain concise cases only for behavior that needs repeatable verification |
| **Small production** | Trace critical and high-risk behavior to reusable cases, automate stable regression paths and record release evidence |
| **Production-critical** | Use explicit risk coverage, controlled test data, environment assumptions, execution records and defect traceability |
| **Enterprise-scale** | Add governed test management, ownership, retention and audit controls where product or regulatory risk requires them |

Documentation depth MUST remain proportional to consequence, repetition and
coordination needs. A low-risk copy change does not need the same artifact as
an authorization or financial transaction rule.

## Core Model

```text
requirement or risk -> test condition -> test case -> execution -> evidence
                                                   -> defect, when observed
```

| Artifact | Purpose |
| --- | --- |
| Test condition | Identifies behavior, rule or risk that needs verification |
| Test case | Defines reusable context, action, data and expected outcome |
| Test suite | Groups cases for a purpose such as smoke, regression or release |
| Execution record | Captures who or what ran a case, against which build and with what result |
| Evidence | Supports a result with relevant output, response, trace or screenshot |
| Defect | Records an observed difference between expected and actual behavior |
| Exploratory charter | Defines a bounded investigation when discovery is more valuable than scripted steps |

Do not use one artifact for all of these purposes. In particular, a test case
is not an accumulating execution log.

## Navigation

| Document | Covers |
| --- | --- |
| [Test Case Standards](./test-case-standards.md) | Required content, behavior-oriented format, test data, traceability, execution and lifecycle |
| [References](./references.md) | External testing guidance and conventions adopted here |

## Non-Negotiable Defaults

- Every maintained test case MUST identify the behavior, requirement or risk
  it verifies.
- Preconditions, test data and expected results MUST be explicit enough for
  another tester to execute the case without oral explanation.
- Expected results MUST describe observable behavior and MUST NOT be replaced
  by actual results after execution.
- Tests involving identity, permissions or protected data MUST identify the
  acting role and relevant access state.
- Test data and evidence MUST NOT contain production secrets or unnecessary
  personal data.
- Execution results MUST identify the tested build or revision and the
  relevant environment.
- Obsolete cases MUST be updated, superseded or retired when accepted behavior
  changes.

## Related Standards

- Specifications and acceptance examples are defined in
  [Architecture: Spec-Driven Development](../architecture/spec-driven-development.md).
- Pipeline test execution and evidence are governed by
  [CI/CD Standards](../ci-cd/README.md).
- Test identities, credentials and evidence follow
  [Security Standards](../security/README.md).
- Copyable test artifacts are available under
  [Testing Templates](../examples/templates/testing/).
