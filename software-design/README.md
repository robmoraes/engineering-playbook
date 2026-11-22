# Software Design Standards

Use this book when changing behavior inside an application. Start with a
decision the software must make, identify the module that owns it and follow
one change through every caller that can produce the same effect.

## Where to start

| When you need to… | Read |
| --- | --- |
| Agree on what users should observe | [Spec-driven development](../architecture/spec-driven-development.md) |
| Decide which service owns the data | [Boundaries and service design](../architecture/boundaries-and-service-design.md) |
| Implement one rule shared by an endpoint and a worker | [Business rule placement](./business-rule-placement.md) |
| Record the expected results and evidence | [Test case standards](../testing/test-case-standards.md) |

## Applying the standard

For an implementation or review, write down the business rule in one
sentence. Name the operation that owns it, the callers that invoke it,
the write that enforces it and the test that would expose a violation.
Use the module and naming conventions already present in the application.

For example, ask a coding assistant to read the placement chapter, trace
the existing reservation paths, then implement the last-slot rule through
their shared operation. Ask it to show the result for each caller when
two customers compete for that slot.

See the [references](./references.md) for the reasoning behind these defaults.
