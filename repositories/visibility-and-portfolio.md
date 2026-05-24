# Visibility and Portfolio

Repository visibility changes who can see source, history, workflows, issues,
artifacts and documentation. Treat visibility as part of repository design,
not a last-minute GitHub setting.

## Visibility Strategy

| Visibility | Use when | Operational consequence |
| --- | --- | --- |
| Public | Content is safe and intended for external discovery or reuse | Source and public repository material can be inspected by anyone |
| Private | Code, infrastructure, client context, credentials or publication rights are restricted | Access and feature availability depend on account/organization setup |
| Internal | Enterprise members should discover/use it, but it is not public | Organization-wide read exposure must be acceptable |

Use the least restrictive visibility that is safe and useful. Keeping a
portfolio reference private removes its discovery value; making operational
infrastructure public without sanitization creates unnecessary exposure.

## Publication Review

Before making a repository public, review:

- Git history and current tree for tokens, private keys and sensitive exports;
- Actions logs/artifacts and published packages/images;
- screenshots, diagrams, sample logs and configuration;
- client/employer ownership and licensing rights;
- private domains, IPs, cloud identifiers and environment details;
- dependency/source licenses where redistributed;
- documentation claims about readiness, support and deployment.

```text
Good                                      Avoid
Sanitized .env.example                   Production .env in an earlier commit
Synthetic domains in diagrams            Internal admin hostname in screenshot
Clear lab/reference status               "Production ready" with no operating evidence
```

Changing visibility does not remove information already committed or
published. If a credential was exposed, rotate/revoke it before cleanup.

## Discoverability Metadata

Every portfolio or shared repository SHOULD have:

```text
Repository name:  engineering-playbook
Description:      Practical platform engineering standards for containerized projects.
Topics:           platform-engineering, devops, docker, ci-cd, security
README:           Purpose, navigation and status
Homepage/demo:    Only where maintained and safe
```

Use topics carefully: on GitHub, topic names are public even when created for
a private repository. Do not encode confidential program or customer names in
topics.

## Portfolio Repository Types

| Type | Presentation focus |
| --- | --- |
| Working application | Problem, architecture, runnable/deployed evidence and delivery practices |
| Platform lab | Learning objective, topology, tradeoffs and non-production boundary |
| Engineering playbook | Navigability, rationale, references and consistent standards |
| Reusable template | Safe usage instructions, supported assumptions and update status |
| Archived project | Historical purpose, current status and successor if applicable |

A portfolio does not need every experiment public. Curate repositories that
demonstrate deliberate engineering choices and mark inactive work accurately.

## Internal Versus External Repositories

Separate public examples from internal operating configuration when exposure or
access differs:

```text
Public:
  engineering-playbook
  swarm-observability-lab

Private/internal:
  platform-environments
  customer-production-infrastructure
  incident-records
```

A public reference may show safe generic deployment patterns. It should not be
the source of truth for live production credentials, account configuration or
sensitive incident records.

## Documentation-First Publication

For standards, runbooks intended for sharing or architectural guidance:

- lead with a navigable README;
- separate overview/philosophy from actionable standards;
- cite external sources explicitly;
- publish sanitized templates/examples;
- state whether material is a personal convention, adopted recommendation or
  platform requirement.

This makes documentation credible without implying it represents a complete
enterprise policy program.

## Repository Quality Indicators

Repository quality should be visible from the repository itself, without
depending on private context.

| Indicator | Useful evidence |
| --- | --- |
| Clear purpose | Concise description and README scope |
| Ownership | Maintainer or ownership path appropriate to its context |
| Current guidance | Maintenance status, accurate links and validation commands |
| Delivery maturity | Documented release, deployment or publishing path where applicable |
| Operational safety | Sanitized examples, secret hygiene and recovery guidance for deployable assets |
| Honest presentation | Explicit lab, archived, sample or production-oriented status |

Keep indicators proportional. A portfolio lab does not need production change
management, but it should not imply controls or operating evidence it does not
have.

## Visibility Changes and Retirement

Before changing from public to private or private to public, review feature,
Pages, fork, Actions history and security implications through GitHub's current
visibility guidance. Visibility changes can alter accessibility and external
expectations.

When a public repository is no longer active, prefer marking it clearly and
archiving it over leaving users unable to tell whether it is maintained.
