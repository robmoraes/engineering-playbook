# Repository Configuration

A repository should make ownership, purpose, delivery status and documentation
discoverable before someone opens source files or workflow YAML.

## Repository Naming

Use lowercase kebab-case as defined in
[Naming: Source Control and Artifacts](../naming/source-control-and-artifacts.md):

```text
<system>[-<component-or-purpose>]

orders-api
portfolio-web
platform-infrastructure
engineering-playbook
```

```text
Good                                      Avoid
orders-api                                OrdersAPI_FINAL
platform-deploy-tools                     carlos-scripts
```

Names identify the durable capability, not the owner, hosting provider,
environment or temporary implementation.

## Visibility: Public or Private

Choose visibility before uploading history or artifacts:

| Visibility | Appropriate when | Requirements |
| --- | --- | --- |
| Public | Portfolio, open-source or public reference material with no confidential content | License/intent is clear, secrets/data removed, screenshots/docs reviewed |
| Private | Proprietary code, client data, unreleased work, sensitive infrastructure or unclear publication rights | Limit access and still apply secret/security hygiene |
| Public later | A useful project not yet sanitized or documented | Keep private until history, assets, dependencies and rights are reviewed |

Making a private repository public does not remove earlier secrets or sensitive
artifacts from history. Publication is a security and documentation review.

## Description, Homepage and Topics

A useful repository summary answers what the project is and its operating
context:

```text
Description:
Production-oriented engineering standards for containerized portfolio projects.

Homepage:
https://example.com/projects/engineering-playbook

Topics:
platform-engineering, devops, docker, ci-cd, documentation, security
```

Use topics for stable discovery concepts, not every dependency:

```text
Good                                      Avoid
docker, github-actions, platform         final, test-project, learning-new-tech-2026
```

For a portfolio repository, a concise description and relevant topics are part
of presentation quality; they should match the README and actual content.

## Default Branch

Use `main` as the default branch for new repositories. It is the trusted
integration branch and SHOULD remain deployable or publishable after required
checks pass.

Avoid long-lived branches such as `develop` unless the release model genuinely
requires a separate integration line and its cost is accepted.

## Baseline Repository Files

Select files according to repository purpose:

```text
README.md
LICENSE                         # public/open distribution where applicable
.gitignore
.editorconfig                   # useful for multi-editor consistency
.github/
  CODEOWNERS                    # team/critical ownership where meaningful
  PULL_REQUEST_TEMPLATE.md
  ISSUE_TEMPLATE/               # when accepting structured issues
  workflows/
SECURITY.md                     # public reusable software or higher-risk project
CONTRIBUTING.md                 # projects accepting external contributions
docs/ or architecture/          # deeper material as needed
```

Do not add empty governance files that no one will maintain. A portfolio demo
may need `README.md`, license decision, CI and sanitized configuration example;
an open-source library likely needs contribution and security reporting
guidance as well.

## README Convention

A project README SHOULD prioritize navigation and evaluation:

```markdown
# Project Name

One-line purpose and scope.

## What It Demonstrates

## Architecture or Runtime

## Running Locally

## Delivery and Deployment

## Documentation

## Security Notes

## License
```

Include only setup instructions that work or clearly state prerequisites.
Link substantial rationale to documentation rather than turning the landing
page into an unscannable charter.

## Repository Templates

Use a template repository or account/organization community health defaults
when several repositories share meaningful starter content:

```text
.github/
  PULL_REQUEST_TEMPLATE.md
  ISSUE_TEMPLATE/
  workflows/build-and-test.yml
.gitignore
README.md
```

Tradeoff:

| Approach | Benefit | Cost |
| --- | --- | --- |
| Per-repository setup | Tailored and simple for a few projects | Drift as projects multiply |
| Template repository | Consistent initial shape | Existing repositories do not receive improvements automatically |
| Shared organization defaults/workflows | Central consistency | Governance and versioning responsibility |

Create templates only for maintained defaults. A stale workflow template
spreads outdated security or dependency choices faster than manual setup.

## Documentation and ADR Placement

Place project architecture decisions in a visible location such as:

```text
architecture/decision-records/
docs/adr/
```

Link ADRs from the README or architecture index. Decisions affecting public
endpoints, datastores, deployment platforms, secrets, CI authority or runtime
failure domains should not exist only in pull request discussion.
