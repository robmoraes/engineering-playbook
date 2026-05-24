# Repository Standards

Standards for choosing repository boundaries, organizing content and governing
project lifecycles across software, infrastructure, platform work and public
portfolio material.

## Repository Position

A repository is a unit of ownership, change history, access, automation and
documentation. It should represent a coherent engineering responsibility, not
simply a convenient folder in GitHub.

Default position:

1. Create a separate repository when ownership, visibility, deployment,
   access, release or operational lifecycle is meaningfully independent.
2. Keep related components together when they change, ship and are governed as
   one coherent system.
3. Make each repository discoverable through clear naming, metadata and
   navigable documentation.
4. Treat public publication and repository retirement as deliberate lifecycle
   events.
5. Use standards and templates to reduce drift, without manufacturing
   governance overhead for small projects.

## Organization Contexts

| Context | Practical default |
| --- | --- |
| **Personal repository** | One clear purpose, concise documentation and simple maintainable automation |
| **Portfolio repository** | Public-safe content, credible engineering narrative, working validation and honest maintenance status |
| **Internal company repository** | Explicit ownership, access boundary, CI/CD integration and lifecycle expectations |
| **Platform repository** | Strong operational ownership, dependency consumers, change control and recovery implications documented |
| **Enterprise-scale organization** | Repository taxonomy, reusable defaults, discovery inventory and policy controls where scale requires them |

## Navigation

| Document | Covers |
| --- | --- |
| [Principles and Boundaries](./principles-and-boundaries.md) | Repository purpose, ownership boundary, dependency and separation decisions |
| [Monorepo and Multirepo](./monorepo-and-multirepo.md) | Repository model tradeoffs, decision criteria and migration considerations |
| [Repository Types](./repository-types.md) | Applications, libraries, infrastructure, GitOps, platform, docs, labs and operational repositories |
| [Structure and Documentation](./structure-and-documentation.md) | Folder layouts, README standard, ADRs, examples and templates |
| [Visibility and Portfolio](./visibility-and-portfolio.md) | Public/private/internal strategy, metadata, discoverability and publication quality |
| [Ownership and Lifecycle](./ownership-and-lifecycle.md) | Owners, governance, dependencies, releases, onboarding and archival |
| [Repository Checklist](./repository-checklist.md) | Creation, publication, production and retirement review |
| [References](./references.md) | External sources and conventions adopted here |

## Non-Negotiable Defaults

- Repository names MUST follow
  [Naming: Source Control and Artifacts](../naming/source-control-and-artifacts.md).
- A repository MUST have an identifiable purpose and owner, even in a
  personal portfolio.
- Public repositories MUST be reviewed for secrets, sensitive data, rights and
  misleading operational claims before publication.
- Production-affecting repositories MUST expose their delivery, access and
  recovery implications through maintained documentation or links.
- Repositories SHOULD be archived or clearly marked when no longer maintained.

## Related Standards

- GitHub configuration, branches, releases and security features:
  [GitHub Standards](../github/README.md).
- Architecture decisions:
  [Architecture Decision Records](../architecture/decision-records/README.md).
- CI/CD artifact and deployment practices:
  [CI/CD Standards](../ci-cd/README.md).
- Secret and public-repository hygiene:
  [Security: Repository and Data Hygiene](../security/repository-and-data-hygiene.md).
