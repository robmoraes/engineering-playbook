# Ownership and Lifecycle

A repository with no owner eventually accumulates broken workflows, outdated
dependencies, unanswered security findings and unclear production authority.
Ownership can be lightweight, but it must be explicit.

## Repository Ownership Record

Each active repository SHOULD identify:

```text
Purpose:
Owner or maintaining team:
Visibility:
Primary artifact or output:
Deployment/runtime relationship:
Critical dependencies/consumers:
Support/maintenance status:
Retirement or handoff trigger:
```

For an individual portfolio, this record may live in the README or repository
description. For a platform organization, it may additionally live in a
service catalog, but the repository should still link to that owner source.

## Ownership Levels

| Repository kind | Ownership expectation |
| --- | --- |
| Lab/experiment | Creator and status clearly stated; no production dependency |
| Public portfolio app | Maintainer, support status and delivery/security hygiene |
| Production application | Operational owner, incident/recovery route and release authority |
| Shared library/module | Consumer contract, release/deprecation owner |
| Platform/infrastructure | Strong owner, change authority, consumers and failure impact |
| GitOps/deployment | Environment ownership and production promotion authority |

## Repository Lifecycle

```text
proposed -> active -> maintained or experimental -> deprecated -> archived
```

| State | Meaning | Required action |
| --- | --- | --- |
| `proposed` | New boundary being evaluated | Confirm purpose, owner and visibility |
| `active` | Work and change expected | Maintain docs, automation and security controls |
| `experimental` | Lab/reference not relied on for production | Mark limitations and avoid production secrets/dependencies |
| `deprecated` | Superseded or planned for removal | Document successor and migration/status |
| `archived` | Read-only historical reference | Revoke unused access and remove active automation before archive |

## Creation and Onboarding

When creating a repository:

1. Choose repository type and boundary.
2. Apply name, visibility and metadata.
3. Add structure appropriate to its output.
4. Configure validation/security controls proportional to impact.
5. Link owners, dependencies and delivery path.
6. Confirm a new engineer can understand how to inspect, run or contribute.

Onboarding documentation should avoid relying on private conversations:

- prerequisites and local setup;
- expected validation command/workflow;
- architecture/deployment links;
- where configuration comes from;
- how releases or updates occur;
- how to request access without exposing secrets.

## Versioning and Releases

Repositories publish different forms of output:

| Output | Versioning concern |
| --- | --- |
| Application deployment | Artifact digest and deployed release trace |
| Public library/module | Consumer compatibility and semantic versioning where API exists |
| Infrastructure module | Consumer upgrade compatibility and state-impact notes |
| Documentation/playbook | Revision history generally sufficient; release tags optional for stable editions |
| Deployment/GitOps config | Commit history and promoted artifact reference; environment change evidence |

Do not apply Semantic Versioning ceremonially to a repository with no public
contract. Do retain traceability for anything deployed or consumed elsewhere.

## Collaboration and Governance

Use governance proportionate to ownership:

| Scale | Practical governance |
| --- | --- |
| Personal project | Document status, validate changes and keep public content safe |
| Portfolio/deployed project | Protected main after deployment, visible CI/CD and maintained security hygiene |
| Team repository | PR review, owners, issue/release practice and access review |
| Platform/enterprise | Reusable controls, catalog/discovery, policy/rulesets and audited privileged change where justified |

Governance should reduce ambiguity and dangerous change, not create empty
approval steps.

## Shared Standards and Templates

An engineering playbook defines conventions; templates provide starter
implementation. Keep them separate conceptually:

```text
engineering-playbook        rationale and standards
platform-service-template   starter application repository
platform-workflows          reusable delivery automation
```

Each shared asset needs:

- owner and consumers;
- update/deprecation policy;
- versioned or otherwise controlled adoption mechanism;
- documentation of what downstream repositories must customize.

## Archival Strategy

Archive when no routine changes should be accepted or the repository is
superseded.

Before archiving:

- update README/description with archival status and replacement;
- close, transfer or document remaining issues/PRs;
- disable unnecessary scheduled or deployment automation;
- revoke unused tokens, deploy keys and environment credentials;
- verify production systems and packages no longer depend on unattended
  updates from this repository;
- retain decisions and operational history necessary for reference.

GitHub archived repositories are read-only until unarchived. Cleanup that
requires changing repository content or settings should therefore be completed
before archival where possible.

## Periodic Review

Review active portfolio and production-related repositories periodically for:

- accurate purpose, metadata and visibility;
- owner/consumer validity;
- dependency/security alert ownership;
- broken CI/CD or outdated deployment claims;
- stale secrets/access;
- unused repositories suitable for deprecation or archive.

Repository sprawl is reduced less by naming policy than by honest lifecycle
maintenance.
