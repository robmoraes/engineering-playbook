# Monorepo and Multirepo

Monorepo versus multirepo is an ownership and change-management decision, not
a proxy for architectural sophistication. Either model can support monoliths,
microservices, infrastructure and platform delivery.

## Definitions

| Model | Meaning |
| --- | --- |
| Monorepo | Multiple packages, components or deployables are maintained within one source-control repository |
| Multirepo | Components or systems are maintained in separate repositories with explicit dependency/integration contracts |

## Tradeoffs

| Concern | Monorepo advantage | Monorepo cost | Multirepo advantage | Multirepo cost |
| --- | --- | --- | --- | --- |
| Atomic change | Cross-component updates can land together | Large change scope can affect more owners | Independent change surfaces | Coordinated changes need version/release choreography |
| Discovery | One source tree for related work | Navigation/build impact grows | Clear component boundaries | System context spread across repositories |
| CI/CD | Shared tooling and integrated checks | Path filtering and selective build complexity | Per-component pipelines clear | Standards drift and duplicated work |
| Access | Simple when access boundary is shared | Weak fit for confidential/privileged separation | Granular visibility/permission boundaries | More administration |
| Release | Coordinated release easier | Independent releases need discipline | Natural independent release lifecycle | Compatibility/version coordination |
| Ownership | Good for one product/team | Ownership within tree requires CODEOWNERS/tooling | Ownership maps directly to repository | Shared work can become fragmented |

## Practical Decision Guidance

Choose a monorepo when:

- components are owned together and frequently change atomically;
- access and visibility requirements are the same;
- shared tooling and dependency updates provide practical value;
- CI can selectively validate and publish deployables as the repository grows.

Choose multiple repositories when:

- ownership or access must be independent;
- services, packages or infrastructure have genuinely separate release
  lifecycles;
- public and private content cannot share a repository safely;
- platform or environment configuration needs a distinct change/approval
  boundary.

```text
Good                                      Avoid
Monorepo for web/api packages changing   Monorepo combining public portfolio and private credentials
together under one owner
Separate deployment-config repo with     Splitting every directory into a repository
environment authority boundary            without owners or independent releases
```

## Small Project and Portfolio Guidance

For one engineer, a monorepo can be effective for a product containing a web
frontend, API and shared package if they form one portfolio story and share
delivery context:

```text
portfolio-platform/
├── apps/
│   ├── web/
│   └── api/
├── packages/
│   └── ui/
├── docs/
└── .github/workflows/
```

Use separate repositories when each project should be evaluated independently
or demonstrates a distinct capability:

```text
engineering-playbook
portfolio-web
orders-api
platform-observability-lab
```

Do not create a monorepo solely to reduce the visible number of incomplete
portfolio projects. Curate or archive projects instead.

## Internal and Platform Guidance

Platform organizations commonly separate:

```text
service source repositories
shared platform tooling/modules
environment/deployment configuration
standards/documentation
```

This separation can protect deployment authority and establish independent
ownership. It also requires versioned interfaces between repositories and a
discoverable service/catalog view.

An infrastructure monorepo can work well where one platform team owns related
modules and environments with consistent access. A multirepo model is often
safer when production environment authority, business units or confidentiality
must be isolated.

## Monorepo Requirements

A monorepo with multiple deliverables SHOULD define:

- component ownership or path responsibilities;
- changed-path CI behavior and integration checks;
- independent artifact naming/version behavior where deployables differ;
- documentation entry points for each product/component;
- dependency boundary rules between packages;
- release behavior: coordinated or independent.

```text
Good                                      Avoid
apps/api publishes orders-api image      Every change rebuilds/deploys all services by accident
CODEOWNERS for platform paths            Shared tree with unclear owners
```

## Multirepo Requirements

A multirepo system SHOULD define:

- where system architecture and dependency mapping lives;
- versioning and compatibility for shared packages/APIs/modules;
- how shared workflow or standard updates are distributed;
- who owns cross-repository releases and failure analysis;
- repository discovery metadata and lifecycle state.

Multirepo failure usually appears as invisible coupling or drift. If no one can
identify which versions work together, repository separation has hidden rather
than managed the system relationship.

## Migration and Review

Changing repository model is costly because it affects history, CI, permissions,
release automation, package identities and links.

Create an ADR before a significant split or consolidation, covering:

- decision driver and ownership;
- source/history movement approach;
- artifact/package naming continuity;
- workflow, secrets and permission migration;
- consumer dependency updates;
- documentation redirects and archive plan;
- rollback or recovery if migration interrupts delivery.

Google's monorepo experience demonstrates that very large monorepos can be
effective with extensive supporting tooling and workflows. It is evidence of
tradeoffs, not a default recommendation for every organization.
