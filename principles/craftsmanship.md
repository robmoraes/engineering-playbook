# Craftsmanship Without Ego

## Quality Is Service

Craftsmanship in software is not devotion to elaborate code or personal
style. It is care for correctness, clarity and changeability in proportion to
the system's consequences. The work is successful when it serves users and
can be responsibly maintained by people who did not write it.

Elegant implementation that cannot be operated, tested or understood is not a
professional success.

## Maintainability Is Respect

Software outlives the moment of implementation. Future maintainers may need
to diagnose an incident, change a rule or repair a security exposure under
time pressure. Respect for them appears in ordinary choices:

- clear naming and cohesive boundaries;
- tests around consequential behavior and regressions;
- small, reviewable changes with stated intent;
- explicit dependencies and configuration;
- migration and rollback planning for persistent data or live services;
- removal of obsolete paths when their continuing cost exceeds their value.

Readable code is not written for an imagined less capable engineer. It is
written because every engineer has limited time and incomplete context.

## Documentation As Care

Documentation reduces rediscovery and dangerous guesswork. A maintained
system SHOULD explain what it does, how it is run, where important state
lives, what can fail and how to recover.

Not every detail belongs in prose. Code expresses precise mechanism; tests
express verified behavior; runbooks express operational action; architecture
records express consequential decisions. Good documentation connects these
forms so that another person can act with confidence.

## Automation As Reduced Friction

Automation is worthwhile when it removes repeated error, repeated waiting or
unsafe manual work. It should leave a traceable result and an understandable
failure mode.

Automating an unclear or harmful process merely allows it to fail faster and
more often. Before automation, establish the desired outcome, the safe
boundary and the recovery path. Delivery implementation guidance is in
[CI/CD Standards](../ci-cd/README.md).

## Review And Humility

The author of a change is not its final judge. Seek review for correctness,
security, operability and comprehensibility. Receive defects as information
about the work, not as an injury to identity. Record why important decisions
were made so later engineers can improve them rather than repeat their
discovery.

## Quality Questions

- Is the behavior correct for ordinary and failure paths?
- Can the next engineer find the reason for this choice?
- Does testing protect the user-impacting behavior rather than only
  implementation details?
- Does the operational path match the quality of the code path?
- Is complexity serving a verified requirement or only the author's
  preference?
