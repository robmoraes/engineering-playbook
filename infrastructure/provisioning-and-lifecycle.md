# Provisioning and Lifecycle

Infrastructure should be provisioned so that intended state, authority,
changes and recovery are reviewable. Automation is useful when it reduces
drift and risk, not when it obscures who can change production.

## Infrastructure as Code

Use versioned Infrastructure as Code (IaC) for infrastructure with ongoing
lifecycle or production impact:

- networks, security groups/firewalls and DNS foundations;
- compute, clusters and load balancers;
- managed data/storage dependencies and backup policies;
- identity roles/service accounts where feasible;
- observability and deployment foundations.

IaC SHOULD provide:

- reviewable change proposal or plan;
- isolated production execution authority;
- protected remote state where state is required;
- provider/tool version control;
- documented import, drift and emergency-change handling.

## State Management

Terraform and similar stateful IaC tools rely on state to map declared
resources to real provider objects. State may expose operational or sensitive
metadata and is a control asset.

Rules:

- do not commit live state to source repositories;
- store shared/production state in a protected backend with access control,
  version/recovery behavior and locking where supported;
- isolate state when environment or authority boundaries differ;
- restrict apply/write privileges more strongly than read/plan access;
- reconcile manual changes or imports deliberately.

```text
Good                                      Avoid
Protected prod state backend             terraform.tfstate committed to Git
Prod apply through scoped identity       Broad personal cloud key in CI
Plan review before change                Console changes with no reconciliation
```

## Immutable Infrastructure

Prefer replacement or controlled redeployment over long-lived, undocumented
in-place mutation where practical:

```text
Good                                      Avoid
Rebuild image and redeploy workload      SSH edit inside live container
Replace node from defined base config    Years of manual host drift
Versioned network/IaC change             Unrecorded production firewall edit
```

Immutability has limits: durable state, emergency remediation and some managed
resources require careful in-place operations. The objective is controlled
repeatability, not destructive recreation of data-bearing systems.

## Cloud and AWS Foundations

For AWS-based infrastructure, define:

- account and environment boundary;
- selected region and availability-zone strategy;
- VPC/subnet routing and public/private placement;
- IAM role paths for humans, workloads and automation;
- data/storage/backup services and encryption ownership;
- telemetry, budget and data-transfer visibility;
- recovery behavior for zonal or broader failures claimed by the design.

Use managed services where they reduce risk and operating effort enough to
justify cost and dependency. Self-hosting may be valid for a lab or controlled
small environment; it should not be treated as lower-cost production without
including maintenance, backups and incident response.

## Registry and Deployment Infrastructure

The infrastructure layer must make artifact delivery and runtime change
possible without granting unnecessary authority.

```text
source/build workflow -> image registry -> approved immutable digest
approved digest -> deployment authority -> runtime environment
runtime -> telemetry -> operator verification
```

Requirements:

- the registry has access, retention and availability expectations;
- deployed artifacts are identifiable by version or digest;
- deployment identity is environment-scoped;
- production deployment can verify runtime state and recover;
- CI/CD does not inherit broad infrastructure administrator access by default.

See [CI/CD Deployments and Promotion](../ci-cd/deployments-and-promotion.md)
and [Docker Images and Registries](../docker/images-and-registries.md).

## Lifecycle Management

| Stage | Infrastructure practice |
| --- | --- |
| Design | Document topology, boundaries, cost, failure modes and owner |
| Provision | Use controlled definitions, protected authority and observable outputs |
| Operate | Monitor health/cost/security, patch dependencies and maintain runbooks |
| Scale | Revisit capacity, state, networking, cost and failure domains |
| Upgrade | Validate compatibility, maintenance path and recovery |
| Deprecate | Communicate consumers, freeze new use and plan migration |
| Retire | Destroy safely, revoke access, retain required records/backups and remove costs |

## Infrastructure Technical Debt

Track debt when it creates operational exposure, for example:

- unsupported operating system/runtime or orchestrator versions;
- manual resources outside maintained provisioning;
- untested backup/restore;
- overly broad production credentials;
- unowned shared services;
- undocumented network exceptions;
- persistent capacity or transfer-cost waste;
- alert noise hiding real failures.

Technical debt records SHOULD include impact, interim control, owner and a
reasonable remediation or acceptance decision.
