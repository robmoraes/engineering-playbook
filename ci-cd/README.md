# CI/CD Standards

Standards for building, validating, publishing and deploying software through
repeatable automation with controlled production risk.

## Delivery Position

The pipeline is part of the production system. It decides which source becomes
an artifact, which artifact reaches an environment and what evidence exists
when a deployment succeeds or fails.

Default delivery path:

```text
pull request -> validate/test/build
merge to main -> build once/scan/publish immutable artifact
release or approval -> deploy stg/verify/promote same artifact/deploy prod/verify
```

## Control Levels

| Context | Practical delivery default |
| --- | --- |
| **Personal/lab** | Automated validation and container build; manual deploy is acceptable when no production users or sensitive access exists |
| **Small public project** | Protected default branch, image publication from trusted branch/tag, isolated production secrets and verification after deploy |
| **Production system** | Immutable promoted artifacts, protected production deployment, rollback path, observability and minimal pipeline permissions |
| **Enterprise-grade workflow** | Governed reusable workflows, provenance/signing policy, controlled runners, audit and standardized deployment platforms where justified |

Do not add stages solely to make a pipeline look mature. Add validation,
approval and evidence where they prevent realistic failure or reduce recovery
time.

## Navigation

| Document | Covers |
| --- | --- |
| [Pipeline Principles](./pipeline-principles.md) | Delivery philosophy, pipeline shape, boundaries, environments and tradeoffs |
| [GitHub Actions Workflows](./github-actions-workflows.md) | Workflow design, naming, reuse, permissions, runners, cache and concurrency |
| [Build and Artifacts](./build-and-artifacts.md) | Container builds, Docker image publishing, artifacts, reproducibility and lifecycle |
| [Releases and Versioning](./releases-and-versioning.md) | Branching, tags, Semantic Versioning and release evidence |
| [Deployments and Promotion](./deployments-and-promotion.md) | Environment promotion, approvals, verification, rollback, Swarm, Kubernetes and GitOps |
| [Pipeline Operations](./pipeline-operations.md) | Failures, retries, telemetry, optimization, monorepos and cost |
| [Delivery Checklist](./delivery-checklist.md) | Project, release and production deployment review |
| [References](./references.md) | External sources and conventions adopted here |

## Non-Negotiable Defaults

- A deployable artifact MUST be traceable to source revision and pipeline run.
- Production MUST deploy an immutable version or digest, not only `latest`.
- Production credentials MUST NOT be exposed to pull-request validation.
- Validation failures MUST block publication or deployment of the affected
  change.
- A production deployment MUST define verification and rollback or recovery
  behavior.
- The same tested artifact SHOULD be promoted between environments rather than
  rebuilt per environment.

## Related Standards

- Names for workflows, jobs, branches, tags and environments are defined in
  [Naming: Automation and Environments](../naming/automation-and-environments.md)
  and [Naming: Source Control and Artifacts](../naming/source-control-and-artifacts.md).
- Credential and workflow trust rules are defined in
  [Security: CI/CD and Automation](../security/ci-cd-and-automation.md).
- Deployment topology and evolutionary decisions are defined in
  [Architecture: Delivery and Evolution](../architecture/delivery-and-evolution.md).
