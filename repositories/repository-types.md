# Repository Types

A clear repository taxonomy improves discovery and prevents fundamentally
different assets from being governed as if they share the same lifecycle.

## Type Catalog

| Type | Owns | Typical outputs | Key concern |
| --- | --- | --- | --- |
| Application | User-facing or internal application capability | Container image, release artifact | Runtime/deployment and API/data ownership |
| Shared library/package | Reusable code contract | Versioned package/module | Compatibility and consumers |
| Internal tooling | Engineering automation or CLI | Binary/package/image | Operator access and maintenance ownership |
| Infrastructure as Code | Provisioned infrastructure definitions | Plans/applied infrastructure | Environment authority and state/security |
| Deployment/GitOps | Desired runtime/environment state | Applied release/configuration | Production change authority and reconciliation |
| Platform service | Shared engineering capability | Runtime service/module/docs | Blast radius and consumer contract |
| Operational/runbook | Procedures for operating systems | Documentation | Accuracy during incidents |
| Standards/playbook | Shared conventions and decisions | Documentation/templates | Adoption and evolution |
| Documentation-first | Architecture/reference/handbook content | Published docs/site | Discoverability and freshness |
| Experiment/lab | Learning or proof of concept | Demo output | Non-production boundary and honest status |

## Application Repositories

Use for deployable products or services:

```text
orders-api
portfolio-web
billing-worker
```

Expected content:

- application source and tests;
- runtime/build definition such as Dockerfile;
- delivery workflow or link to adopted delivery mechanism;
- configuration example without secrets;
- architecture/runtime notes where non-trivial;
- operating/deployment notes for deployed workloads.

One repository may own multiple tightly coupled deployables when the chosen
monorepo model is documented.

## Shared Libraries and Internal Packages

Use for independently consumed code whose compatibility matters:

```text
http-client
observability-kit
ui-components
```

Required discipline:

- published package/module identity;
- compatibility/version strategy;
- supported consumers or migration guidance;
- tests and publication workflow;
- no runtime environment configuration embedded in the package.

Do not extract a library repository merely for code reuse once. Independent
package maintenance is justified when consumers and versioned evolution exist.

## Internal Tooling Repositories

Internal tools include deployment CLIs, migration utilities or engineering
automation:

```text
platform-deploy-tools
database-maintenance-cli
```

Document:

- intended operators and privilege required;
- safe execution/dry-run or recovery behavior;
- supported environments;
- artifact/version delivery;
- audit impact for production-changing tools.

A script that can mutate production is an operational product even when its
codebase is small.

## Infrastructure-as-Code Repositories

Infrastructure repositories own declarations for networking, compute,
registries, DNS, identity or shared platform resources:

```text
platform-infrastructure
platform-network-prod
```

Expected boundaries:

- state backend and secret handling are documented without exposing values;
- environment/tenant/account authority is explicit;
- apply permissions are more restricted than plan/read workflows;
- module reuse and versions are controlled;
- changes include operational impact and rollback/recovery consideration.

Do not mix application source and broad production infrastructure merely for
convenience when their access or review boundaries differ.

## Deployment and GitOps Repositories

A deployment repository owns environment-specific desired state:

```text
platform-environments
orders-deployments
```

Typical content:

```text
environments/
├── stg/
│   └── orders-api.yaml
└── prod/
    └── orders-api.yaml
```

Use a distinct deployment repository when:

- environment promotion requires a separate approval/access boundary;
- runtime desired state must be audited independently from application source;
- a reconciler consumes declared state from Git.

Calling a repository `gitops` is justified only when the operating model uses
declarative, versioned desired state with automated pull/reconciliation as
defined by OpenGitOps. A repository containing shell deployment scripts is a
deployment repository, not automatically a GitOps repository.

## Platform Repositories

Platform repositories provide reusable operational capabilities:

```text
platform-observability
platform-ingress
platform-workflows
platform-terraform-modules
```

They SHOULD identify:

- consumer repositories/systems;
- supported contract or adoption path;
- operational ownership and failure impact;
- release/deprecation policy;
- how consumers obtain updates.

Shared platform code without a consumer contract becomes an undocumented
dependency with broad blast radius.

## Documentation, Standards and Playbooks

Documentation-first repositories are appropriate when the content is itself a
maintained product:

```text
engineering-playbook
platform-runbooks
architecture-handbook
```

Expected content:

- navigable index;
- topic-oriented modular documents;
- references for adopted external guidance;
- ownership and change expectations;
- examples/templates that do not contain sensitive information.

Do not bury system-specific runbooks in a general playbook when operators need
them alongside the deployed system's actual version and access context.

## Operational and Infrastructure Documentation Repositories

Use a dedicated operational or infrastructure documentation repository when
procedures, topology guidance or operating conventions span several owned
systems:

```text
platform-runbooks
infrastructure-handbook
```

Keep service-specific operating instructions beside the service or deployment
repository when they change with that workload. Centralize guidance only when
a clear platform owner is accountable for keeping cross-system material
current.

These repositories require a visibility review before publication. Do not
publish internal hostnames, account identifiers, secret locations, access
paths or incident detail that increases operational exposure.

## Labs and Learning Repositories

Labs are valid portfolio assets when clearly identified:

```text
swarm-observability-lab
oidc-deployment-lab
```

Document:

- learning goal and scope;
- whether it is deployable or intentionally disposable;
- non-production security boundary;
- status and maintenance expectations.

Avoid names and READMEs that imply production readiness for an unoperated
experiment.
