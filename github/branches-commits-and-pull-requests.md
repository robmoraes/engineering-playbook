# Branches, Commits and Pull Requests

The collaboration flow should keep the trusted branch reviewable and
releasable while avoiding process that exceeds project risk.

## Branch Strategy

The preferred strategy is
[Trunk-Based Development](./branching-strategies.md#preferred-model-trunk-based-development).
Traditional Gitflow is a secondary option only when a repository documents the
need for its persistent `develop` integration line and release workflow.

Trunk-based default:

```text
main                           trusted integration and release source
feat/OPS-142-add-healthcheck  short-lived change branch
fix/image-promotion           corrective change
docs/github-standards         documentation change
release/v1.8                  maintained/stabilized release line only when needed
hotfix/v1.8.3-db-timeout      urgent release-line correction
```

Short-lived branches reduce merge drift and make pull requests easier to
review. Release branches are appropriate where a released line must remain
supported while `main` continues moving; they are not required for every
deployment.

Repositories that select
[Traditional Gitflow](./branching-strategies.md#secondary-model-traditional-gitflow)
also protect `develop` and applicable `release/*` branches according to their
integration and release authority.

## Protection Model

Apply protection to `main` in proportion to consequence:

| Context | Baseline protection |
| --- | --- |
| Personal experiment | Direct pushes acceptable until publication/deployment begins |
| Public portfolio with CI | Required status checks before merge; avoid force pushes to `main` |
| Team or production repository | Pull request required, status checks required, conversations resolved, no force pushes/deletion |
| Higher-risk platform | Organization ruleset, required owners/reviews, controlled bypass and protected release/tag policy where supported |

Recommended production settings:

- require pull request before merge;
- require passing CI checks;
- dismiss stale approvals or require approval of the latest meaningful push
  where review bypass through later changes is a risk;
- require review from CODEOWNERS for sensitive paths where ownership exists;
- block force pushes and branch deletion;
- restrict bypass authority and use it only with documented incident need.

Rulesets are useful when multiple repositories or branch/tag patterns require
consistent organization policy. A single personal repository can use
repository-level branch protection without unnecessary administration.

## CODEOWNERS

Use `.github/CODEOWNERS` when review ownership is meaningful:

```text
# Default ownership
*                            @acme/platform-maintainers

# Sensitive delivery paths
/.github/workflows/          @acme/platform-maintainers
/infrastructure/             @acme/platform-maintainers
/security/                   @acme/security-reviewers
/architecture/decision-records/ @acme/platform-maintainers
```

For a personal repository, CODEOWNERS offers limited additional control if one
person is the only reviewer. It becomes useful as soon as team ownership or
external contribution exists.

Operational implication: a CODEOWNERS file improves routing only when branch
protection requires owner review and listed owners have the required access.

## Pull Request Standard

A pull request SHOULD state:

```markdown
## Purpose

What problem or outcome this change addresses.

## Changes

- Material change.

## Verification

- Tests or checks run.

## Operational Impact

- Deployment, migration, secrets, monitoring or rollback impact, or `None`.

## References

- Issue, ADR or release context where applicable.
```

Good PRs make review and future investigation easier:

```text
Good                                      Avoid
"Deploy image by immutable digest"       "updates"
Lists rollback impact                    No evidence for production change
Links ADR for new datastore              Major topology decision hidden in diff
```

Use draft pull requests for incomplete collaboration without requesting final
review prematurely.

## Commit Convention

Use concise imperative messages. Conventional Commits are adopted for
repositories where consistent changelog or release automation benefits from
structured commit/merge messages:

```text
feat: add image digest promotion
fix: prevent production secret exposure in preview job
docs: add repository lifecycle policy
chore: update runner image
```

Optional scope:

```text
feat(ci): publish provenance metadata
fix(auth): rotate expired token handling
```

Use `!` or `BREAKING CHANGE:` only when the published contract actually
changes incompatibly.

```text
Good                                      Avoid
fix: validate deploy digest input        small fixes
docs(github): add CODEOWNERS policy      WIP final final
```

Do not force developers to split coherent changes solely to manufacture a
perfect commit history. Prefer squash merging when a pull request represents
one logical delivered change and the repository uses the final commit message
for changelog or audit clarity.

## Review Expectations

Review should focus on risk and operability:

- correctness and test evidence;
- secrets, permissions and workflow authority;
- deployment, data migration and rollback effects;
- public API, documentation and compatibility impact;
- architecture decision capture when boundaries change.

Style-only concerns belong in formatters or documented conventions where
possible. Human review time should be spent on behavior and consequences.
