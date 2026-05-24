# References and Adoption Notes

The sources below define GitHub platform behavior or provide concrete
experience with repository and decision-management models. This playbook
adapts them into a proportional repository standard. Its repository taxonomy,
default boundaries and portfolio curation rules are local conventions rather
than universal requirements.

## External Guidance and Adoption

| Source | Original guidance or platform behavior | Adoption in this playbook |
| --- | --- | --- |
| GitHub Docs, *About repositories* and *Setting repository visibility* | Repositories hold revision history and collaboration state; visibility controls exposure and visibility changes have feature/fork/security consequences. | Visibility is selected as a lifecycle and security decision, not only a presentation setting. |
| GitHub Docs, *Classifying your repository with topics* | Topics aid discovery; GitHub topics use lowercase letters, numbers and hyphens and topic names are public even for private repositories. | Shared/portfolio repositories use concise non-sensitive topics for discoverability. |
| GitHub Docs, *Creating a template repository* and *Creating a default community health file* | Templates reproduce starter directory/files; account/organization default community health files can apply where repositories lack local files. | Templates/defaults are used only for maintained baseline content and do not replace project-specific ownership or documentation. |
| GitHub Docs, *Archiving repositories* | Archived repositories are read-only; GitHub recommends updating README/description and closing work before archive. | Lifecycle policy includes credential/automation cleanup and clear successor/status notes before archive. |
| Google Research, Potvin and Levenberg, *Why Google Stores Billions of Lines of Code in a Single Repository* | Documents benefits and tradeoffs of Google's very large monorepo and the tooling/workflows required to support it. | Monorepo is evaluated by coupling, ownership and tooling; Google's model is evidence of possible scale, not a default prescription. |
| Architectural Decision Records, ADR GitHub Organization | An ADR captures one significant architecture decision, rationale and consequences; records form a decision log. | Repository-boundary, orchestration and production authority changes are captured through linked ADRs. |
| OpenGitOps, *GitOps Principles* | GitOps desired state is declarative, versioned and immutable, pulled automatically and continuously reconciled. | A deployment repository is called GitOps only when it participates in that operating model. |
| Semantic Versioning 2.0.0 | Version semantics apply to software declaring a public API. | Libraries/modules with public compatibility contracts may use SemVer; documentation and internal deployments do not claim it without such a contract. |

## Source Links

- GitHub Docs, *About repositories*:
  <https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories>
- GitHub Docs, *Setting repository visibility*:
  <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/managing-repository-settings/setting-repository-visibility>
- GitHub Docs, *Classifying your repository with topics*:
  <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics>
- GitHub Docs, *Creating a template repository*:
  <https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository>
- GitHub Docs, *Creating a default community health file*:
  <https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file>
- GitHub Docs, *Archiving repositories*:
  <https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories>
- Google Research, Potvin and Levenberg, *Why Google Stores Billions of Lines
  of Code in a Single Repository*:
  <https://research.google/pubs/why-google-stores-billions-of-lines-of-code-in-a-single-repository/>
- Architectural Decision Records:
  <https://adr.github.io/>
- OpenGitOps, *GitOps Principles*:
  <https://github.com/open-gitops/documents/blob/main/PRINCIPLES.md>
- Semantic Versioning 2.0.0:
  <https://semver.org/>

## Local Conventions

- Repositories are separated when ownership, access, release, deployment or
  lifecycle boundaries justify the maintenance cost.
- A monorepo is acceptable for several deliverables when coupling and
  ownership favor coordinated changes and CI/CD handles independent artifacts.
- Public portfolio repositories optimize for trustworthy discovery and honest
  maintenance status, not repository count.
- Documentation-first and shared-standards repositories are treated as
  maintained engineering products with references and safe examples.
