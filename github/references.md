# References and Adoption Notes

These sources describe GitHub platform features or broadly used engineering
conventions. This playbook adapts them to repositories that range from public
portfolio work to production delivery. Its thresholds for process, preference
for concise governance and exact repository taxonomy are local conventions.

## External Guidance and Adoption

| Source | Original guidance or platform behavior | Adoption in this playbook |
| --- | --- | --- |
| GitHub Docs, *About repositories*, *Managing repository settings and features* and *Classifying your repository with topics* | GitHub repositories expose visibility, default branch, metadata and topics for discovery/management. | Repository identity includes purpose, intentional visibility, description, topics and a navigable README. |
| GitHub Docs, *About rulesets* and *Managing protected branches* | Rulesets and protected branches can require checks/reviews and restrict branch changes; multiple rulesets may apply. | `main` receives protection proportional to risk; organization rulesets are used for consistent multi-repository governance. |
| GitHub Docs, *About code owners* | CODEOWNERS requests responsible reviewers and can be required through branch protection. | Use ownership review for real team/sensitive-path boundaries, not symbolic files without reviewers. |
| GitHub Docs, *About issue and pull request templates*, *Managing labels* and *About milestones* | Templates collect contributor context; labels categorize work; milestones group issues/PRs. | Keep templates and taxonomy compact and useful for decisions and release visibility. |
| GitHub Docs, *Automatically generated release notes* | GitHub can generate release summaries from merged pull requests and contributors and categorize them through configuration. | Generated notes are a starting point; production-impact notes and artifact traceability remain curated. |
| GitHub Docs, *Secrets reference* and Actions security guidance | Secrets exist at organization, repository and environment scopes; workflows should limit permissions and protect credentials. | Secret scope follows smallest needed authority; production delivery uses protected environments/identity and minimal workflow permission. |
| GitHub Docs, *Managing environments for deployment* | Jobs referencing an environment must satisfy its protection rules before accessing environment secrets. | Production secrets and deployment authorization are assigned to protected environments where available and appropriate. |
| GitHub Docs, *Managing your personal access tokens* | Fine-grained PATs are recommended where possible; GitHub Apps are appropriate for organization access or long-lived integrations. | Prefer workflow tokens/OIDC/apps before long-lived personal tokens; token reliability and ownership are documented. |
| GitHub Docs, *About push protection*, *About secret scanning*, *About code scanning alerts* and *About Dependabot alerts* | GitHub detects secrets, code findings and vulnerable dependencies with feature/plan-specific behavior. | Public and production-facing repositories enable useful security signals and retain human triage/rotation responsibility. |
| GitHub Docs, *Secure use reference* | Self-hosted runners and workflow dependencies introduce trust and persistence concerns. | Public untrusted code does not run on production-connected runners; privileged actions are reviewed and pinned. |
| GitHub Docs, *Configuring a publishing source for GitHub Pages* and *About custom domains and GitHub Pages* | Pages can publish from a branch or Actions; Pages content is public and verified custom domains reduce takeover risk. | Portfolio Pages publishing receives a public-content and domain-security review. |
| GitHub Docs, *Archiving repositories* | Archived repositories become read-only; GitHub recommends closing work and updating README/description before archive. | Retirement includes status documentation and credential/automation cleanup before archival. |
| Conventional Commits 1.0.0 | Defines structured commit message prefixes for human and automated consumers. | Adopt Conventional Commits where release/changelog consistency benefits; do not require ceremony without use. |
| Semantic Versioning 2.0.0 | Defines version semantics for software declaring a public API. | Published contracts may use SemVer; repositories without a contract must not imply it. |
| Trunk Based Development | Describes development centered on a trunk with short-lived branches and optional release branches. | `main` plus short-lived branches is the default, with release branches when maintenance needs justify them. |

## Source Links

- GitHub Docs, *About repositories*:
  <https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories>
- GitHub Docs, *Managing your repository settings and features*:
  <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features>
- GitHub Docs, *Classifying your repository with topics*:
  <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics>
- GitHub Docs, *About rulesets*:
  <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets>
- GitHub Docs, *Managing protected branches*:
  <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches>
- GitHub Docs, *About code owners*:
  <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners>
- GitHub Docs, *About issue and pull request templates*:
  <https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates>
- GitHub Docs, *Managing labels*:
  <https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/managing-labels>
- GitHub Docs, *About milestones*:
  <https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones>
- GitHub Docs, *Automatically generated release notes*:
  <https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes>
- GitHub Docs, *Secrets reference*:
  <https://docs.github.com/en/actions/reference/security/secrets>
- GitHub Docs, *Security hardening for GitHub Actions*:
  <https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions>
- GitHub Docs, *Managing environments for deployment*:
  <https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments>
- GitHub Docs, *Managing your personal access tokens*:
  <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens>
- GitHub Docs, *About push protection*:
  <https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection>
- GitHub Docs, *About secret scanning*:
  <https://docs.github.com/en/code-security/concepts/secret-security/about-secret-scanning>
- GitHub Docs, *About code scanning alerts*:
  <https://docs.github.com/en/code-security/code-scanning/automatically-scanning-your-code-for-vulnerabilities-and-errors/about-code-scanning-alerts>
- GitHub Docs, *About Dependabot alerts*:
  <https://docs.github.com/en/code-security/dependabot/dependabot-alerts/about-dependabot-alerts>
- GitHub Docs, *Secure use reference*:
  <https://docs.github.com/en/actions/reference/security/secure-use>
- GitHub Docs, *Configuring a publishing source for GitHub Pages*:
  <https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site>
- GitHub Docs, *About custom domains and GitHub Pages*:
  <https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages>
- GitHub Docs, *Archiving repositories*:
  <https://docs.github.com/en/repositories/archiving-a-github-repository/archiving-repositories>
- Conventional Commits 1.0.0:
  <https://www.conventionalcommits.org/en/v1.0.0/>
- Semantic Versioning 2.0.0:
  <https://semver.org/>
- Trunk Based Development:
  <https://trunkbaseddevelopment.com/>

## Local Conventions

- Public portfolio repositories undergo publication review even when they are
  not maintained as open-source community projects.
- Pull requests are the normal traceability boundary once a repository has
  collaboration or production impact.
- Process features such as Projects, Discussions, CODEOWNERS and shared
  workflows are adopted when they solve a real ownership or coordination need.
- GitHub remains evidence and automation infrastructure; project-specific
  architecture and runbooks belong in maintained documentation, not only in
  issue history.
