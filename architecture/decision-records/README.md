# Architecture Decision Records

Architecture Decision Records (ADRs) preserve context for choices that affect
system boundaries, operations, reliability, security, cost or delivery.
They are intentionally short enough to maintain alongside code and
infrastructure.

## When an ADR Is Required

Create an ADR for a decision that:

- introduces or replaces a datastore, queue, public endpoint, identity system
  or orchestration platform;
- splits or combines deployment/service boundaries;
- changes production availability, recovery, storage or failure-domain design;
- adopts a shared platform dependency or substantial external managed service;
- creates an intentional exception to an architecture, security or reliability
  standard;
- is difficult or expensive to reverse.

Do not create ADRs for routine dependency upgrades, trivial refactoring or
implementation detail that does not alter a meaningful constraint.

## Status Lifecycle

| Status | Meaning |
| --- | --- |
| `proposed` | Under review; not yet the agreed implementation direction |
| `accepted` | Decision approved for implementation or active use |
| `deprecated` | Still historically relevant but should not be used for new work |
| `superseded` | Replaced by another ADR, which must be linked |
| `rejected` | Considered but not adopted; retained only when the reasoning is useful |

Do not rewrite an accepted ADR to hide changed thinking. Write a new ADR that
supersedes it and link both records.

## File Convention

```text
architecture/decision-records/
├── README.md
├── template.md
└── 0001-use-managed-postgresql-for-orders.md
```

Use a zero-padded sequential number and a concise decision title:

```text
0001-use-docker-swarm-for-initial-runtime.md
0002-separate-background-worker-from-api.md
0003-adopt-managed-object-storage.md
```

## Decision Index

No project-specific decisions have been recorded yet. Add each accepted,
proposed or superseded ADR to the table when created.

| ADR | Status | Decision | Scope |
| --- | --- | --- | --- |
| - | - | No decisions recorded | - |

## Writing Guidance

An ADR should make these questions answerable months later:

1. What constraint or requirement forced a decision?
2. What was chosen and what alternatives were considered?
3. Which operational, cost, security and reliability consequences were
   accepted?
4. How will the choice be validated or reconsidered?

Keep discussion specific to the context. "Kubernetes is industry standard" is
not sufficient rationale. "We require namespace isolation and standardized
controllers already operated by the platform team" is actionable rationale.

Use [template.md](./template.md) for new records.
