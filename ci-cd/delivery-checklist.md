# CI/CD Delivery Checklist

Use this checklist when introducing delivery automation, releasing an image or
changing a production deployment path.

## Repository and Workflow Setup

- [ ] Default branch protections and required validation match project impact.
- [ ] Workflow files and job identifiers follow the naming standard.
- [ ] Workflow permissions are explicit and minimal.
- [ ] Pull-request workflows cannot read publication or production deployment
  credentials.
- [ ] Privileged third-party actions are reviewed and pinned immutably where
  appropriate.
- [ ] Reusable workflows declare their inputs, secrets and versioning
  expectations.

## Build and Artifact Publication

- [ ] Build uses locked or otherwise controlled dependency inputs.
- [ ] Container runtime image contains no secrets and follows container
  security baseline.
- [ ] One immutable image tag or digest is recorded for the source revision.
- [ ] Registry credentials are automation-specific and narrowly scoped.
- [ ] Vulnerability/security scan result or accepted exception is associated
  with the artifact.
- [ ] Artifact metadata includes source revision, workflow run and digest.
- [ ] Retention preserves any artifact needed for rollback or investigation.

## Release

- [ ] Release version/tag points to trusted validated source.
- [ ] Version strategy is documented: SemVer where a public contract exists,
  or a stated alternative.
- [ ] Where a changelog is maintained, notable release changes move from
  `Unreleased` into a dated, linked release entry.
- [ ] Release notes identify operational changes, migration requirements and
  rollback constraints.
- [ ] Published release tags are immutable after release.
- [ ] Hotfix procedure preserves source and artifact traceability.

## Environment and Deployment

- [ ] Production and non-production credentials and configuration are
  isolated.
- [ ] The artifact deployed to production is the tested/promoted immutable
  artifact, not a rebuild.
- [ ] Required approval or protected environment boundary is configured.
- [ ] Current known-good production digest/version is captured before deploy.
- [ ] Migration compatibility and recovery requirements have been reviewed.
- [ ] Deployment credentials grant only required environment authority.

## Verification and Rollback

- [ ] Deployment workflow verifies runtime image/version or digest.
- [ ] Healthcheck and smoke behavior validate the actual routed service path.
- [ ] Metrics/logs or other operational signals are reviewed for immediate
  regression.
- [ ] Rollback command/workflow and prior artifact are available.
- [ ] Recovery path is documented when data migrations prevent simple rollback.

## Operations and Optimization

- [ ] Workflow failures preserve actionable evidence.
- [ ] Retries are bounded and used only for transient, safely repeatable
  operations.
- [ ] Caches contain replaceable inputs only and do not cross unsafe trust
  boundaries.
- [ ] Parallelization does not race shared production changes.
- [ ] Runner choice, retention and build cost are reasonable for project
  scale.
- [ ] Self-hosted runners, when used, are isolated from untrusted workflow
  execution.

## Exception Record

For an unmet baseline deployment control, record:

```text
Control:
System/environment:
Reason:
Risk and operational consequence:
Compensating measure:
Owner:
Review/removal date:
```
