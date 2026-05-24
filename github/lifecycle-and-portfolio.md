# Lifecycle and Portfolio Presentation

Repositories have a lifecycle: creation, active delivery, publication,
maintenance and retirement. A public portfolio repository also communicates
engineering judgment to readers who will not know its private context.

## Repository Lifecycle

| Stage | Required focus |
| --- | --- |
| Create | Purpose, naming, visibility, initial documentation and secret hygiene |
| Develop | Branch/workflow consistency, tests and decisions captured as needed |
| Publish | Public content/security review, license intent, presentation and CI evidence |
| Operate | Releases, dependency/security maintenance, deployment evidence and support expectations |
| Retire | Final status, archive/read-only decision, token/deployment cleanup and successor references |

## Public Portfolio Standard

A portfolio repository SHOULD let a reviewer understand:

- what problem or engineering capability it demonstrates;
- architecture and technology decisions;
- how to run or inspect it safely;
- what automation exists and what it validates;
- which production-minded practices are demonstrated;
- whether the project is active, archived or educational.

Useful presentation elements:

```text
README summary and navigation
architecture overview or ADRs where consequential
CI/CD workflow visible and passing
sanitized example configuration
container/deployment examples where relevant
license or explicit usage intent
screenshots/demo link only after sensitive-data review
```

```text
Good                                      Avoid
Sanitized deployment diagram             Screenshot showing token or private hostname
Clear "reference implementation" scope  Claiming production readiness without operating detail
```

## Documentation Organization

Keep the README approachable and link deeper documentation:

```text
README.md                  quick evaluation and navigation
docs/                      usage or engineering notes
architecture/              decisions/topology when material
runbooks/                  operations for deployed projects
.github/                   collaboration and workflow controls
```

Avoid duplicating the same standard in multiple places. Link to playbook
standards where a repository adopts them and document only project-specific
choices or exceptions locally.

## Open-Source Readiness

Before inviting external use or contribution, consider:

- license and ownership rights;
- `CONTRIBUTING.md` where contributions are accepted;
- `SECURITY.md` for vulnerability reporting where software may be used by
  others;
- issue/PR templates and response expectations;
- dependency and secret scanning baseline;
- release and support stance;
- code of conduct when operating a contributor community.

A public portfolio repository is not automatically an open-source project with
support obligations. State whether code is a reference, actively maintained
tool or contribution-oriented project.

## GitHub Pages

GitHub Pages can provide portfolio documentation or a static project site.
Use it when it improves discovery or presentation, with these controls:

- publish only static content safe for public distribution;
- do not render environment exports, secrets or internal operational detail;
- review build actions and deployment permissions;
- define whether the site is built from a dedicated branch or Actions
  workflow;
- treat Pages output as publicly exposed content, including when it is sourced
  from a private repository under a plan that permits private repository
  Pages;
- verify a custom domain before use where applicable to reduce takeover risk;
- ensure custom domain and linked project claims remain maintained.

Pages is presentation hosting, not a place to expose internal dashboards or
administration interfaces.

## Monorepo Versus Multirepo on GitHub

| Model | Good fit | GitHub operating consequence |
| --- | --- | --- |
| Monorepo | Components change together or share one ownership/release model | CODEOWNERS paths and workflow filtering become important |
| Multirepo | Independent ownership, release or access boundaries | Templates/reusable workflows and cross-repository coordination matter |

Do not split repositories solely to appear service-oriented, and do not put
unrelated systems in one repository solely to avoid standardization work. Use
the ownership and delivery boundary that makes changes understandable.

## Archival Strategy

Archive a repository when it is no longer actively maintained and should not
accept normal changes. Before archiving:

- state archival reason and replacement, if any, in the README;
- disable or remove unnecessary scheduled/deployment workflows;
- revoke unused secrets, deploy keys and registry/cloud tokens;
- ensure published packages or deployment dependencies have an ownership plan;
- close or transfer meaningful open work;
- retain documentation needed to understand historical decisions.

Archived repositories are not exempt from prior exposure concerns; public
history and released artifacts remain accessible according to visibility.
Archiving makes repository content and collaboration records read-only until
the repository is unarchived, so revoke credentials and adjust automation
before archive rather than assuming it can be repaired afterward without
reopening the repository.

## Maintenance Expectations

For active public or deployed repositories, periodically review:

- outdated dependencies and vulnerability alerts;
- expired or unused credentials;
- broken workflows and obsolete badges/links;
- ownership and branch protection;
- release/support status;
- documentation claims that no longer match operation.

A clean portfolio is not one with only active projects. It is one where
maintenance status and engineering intent are honest and easy to determine.
