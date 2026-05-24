# GitHub Standards

Practical standards for managing repositories, collaboration, delivery
automation and security controls on GitHub.

## Repository Position

GitHub repositories are more than code storage. They expose project intent,
control changes to production-relevant files, run automation and preserve the
evidence required to understand releases and incidents.

Default posture:

1. Make repositories easy to identify, evaluate and operate.
2. Keep `main` releasable and protected in proportion to impact.
3. Use pull requests as the normal review and traceability boundary.
4. Give workflows, secrets and collaborators the minimum required authority.
5. Archive or transfer repositories intentionally when ownership ends.

## Adoption Context

| Context | Practical standard |
| --- | --- |
| **Personal project** | Clear README, predictable naming, lightweight branch workflow and no committed secrets |
| **Portfolio repository** | Public-safe presentation, demonstrable CI, sanitized documentation, license decision and security hygiene |
| **Team repository** | Protected branch, review ownership, issue/PR conventions, scoped automation and documented releases |
| **Enterprise-grade environment** | Organization rulesets, teams, audit, governed workflows/secrets, stronger scanning and lifecycle policy where justified |

## Navigation

| Document | Covers |
| --- | --- |
| [Repository Configuration](./repository-configuration.md) | Visibility, naming, descriptions, topics, documentation and templates |
| [Branches, Commits and Pull Requests](./branches-commits-and-pull-requests.md) | Branch policy, protection, CODEOWNERS, commit and review conventions |
| [Issues, Projects and Releases](./issues-projects-and-releases.md) | Labels, milestones, boards, discussions, tags, releases and release notes |
| [Actions and Delivery Integration](./actions-and-delivery-integration.md) | Workflow layout, CI/CD integration, Docker registries, reusable automation and runners |
| [Access, Secrets and Security](./access-secrets-and-security.md) | Teams, tokens, secrets, scanning, Dependabot and auditability |
| [Lifecycle and Portfolio Presentation](./lifecycle-and-portfolio.md) | Open-source readiness, Pages, documentation, archive strategy and portfolio quality |
| [Repository Checklist](./repository-checklist.md) | Setup, publication, team and production-readiness review |
| [References](./references.md) | Official sources and adopted conventions |

## Non-Negotiable Defaults

- Repository names MUST follow the shared naming convention and avoid hidden
  ownership or environment semantics.
- Secrets, private keys and sensitive production data MUST NOT be committed or
  exposed in public repository artifacts.
- Production-relevant automation MUST use explicit minimal permissions and
  protected credentials or identity.
- Released or deployed artifacts MUST remain traceable to source and workflow
  execution.
- A public portfolio repository MUST be reviewed as public documentation, not
  merely made visible.

## Related Standards

- Names, branches and tags:
  [Naming: Source Control and Artifacts](../naming/source-control-and-artifacts.md).
- GitHub Actions pipelines and releases:
  [CI/CD: GitHub Actions Workflows](../ci-cd/github-actions-workflows.md) and
  [CI/CD: Releases and Versioning](../ci-cd/releases-and-versioning.md).
- Pipeline authority and secrets:
  [Security: CI/CD and Automation](../security/ci-cd-and-automation.md).
- Architectural decision documentation:
  [Architecture Decision Records](../architecture/decision-records/README.md).
