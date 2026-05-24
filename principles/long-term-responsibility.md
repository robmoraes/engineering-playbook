# Long-Term Responsibility

## Delivery Begins A Relationship

When people depend on software, delivery is the beginning of responsibility,
not its end. A deployed system needs ownership, observation, maintenance and
an eventual path for replacement or retirement.

The degree of investment depends on the impact of interruption, incorrect
behavior or data loss. The obligation to consider those outcomes does not.

## Reliability Respects User Time

An unavailable or unreliable system makes users wait, repeat work, seek help
or abandon a goal. Reliability work should start with the user-visible
behavior that matters: completing a search, recording an action, obtaining an
accurate result or recovering important data.

For persistent systems, define the level of reliability needed, the acceptable
failure behavior and the recovery route. Avoid claiming availability that
cannot be measured or supported. Operational standards are documented in
[Infrastructure Standards](../infrastructure/README.md) and
[Runbooks](../runbooks/README.md).

## Observability Is Accountability

Once a system is running, an engineer needs evidence of whether it is helping
or failing its users. Logs, metrics, traces, health checks and dashboards are
not decorations for production infrastructure. They enable detection,
diagnosis and honest evaluation.

Observability should answer practical questions:

- Are users able to complete the important workflow?
- Are failures increasing, and for whom?
- What changed before a regression?
- Can an operator diagnose a problem without exposing sensitive data?
- Did recovery restore the expected behavior?

Instrumentation and operational review conventions are in
[Observability Standards](../observability/README.md).

## Security Protects Continuity And Trust

A system is not dependable if it exposes credentials, loses data integrity or
gives unauthorized access to information and actions. Security protects
people and also preserves an organization's ability to serve them.

Apply least privilege, isolated environments, secret handling, artifact
traceability and an incident response path according to real exposure. Do not
postpone basic protection merely because a project began small. See
[Security Standards](../security/README.md).

## Stewardship Across Change

Long-lived systems accumulate changed requirements, dependencies and operating
conditions. Stewardship includes:

- knowing who owns the system and its important data;
- updating dependencies and controls according to risk;
- preserving decision history and operational knowledge;
- testing restore, migration and rollback paths where failure would matter;
- replacing or retiring systems deliberately, including data disposition and
communication to affected users.

## A Practical Completion Standard

A user-impacting system is not responsibly delivered until the team can state:

- what purpose it serves and for whom;
- how success and important failure are recognized;
- how sensitive access and data are protected;
- how change is deployed and reversed or recovered;
- who responds when its assumptions stop being true.

This standard does not demand enterprise ceremony for every tool. It demands
that care grow in proportion to reliance and consequence.
