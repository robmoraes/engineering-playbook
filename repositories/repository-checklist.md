# Repository Checklist

Use this checklist when creating a repository, making it public, adding
production responsibility or retiring it.

## Purpose and Boundary

- [ ] Repository purpose can be stated clearly in one paragraph.
- [ ] Repository type is known: application, library, tooling,
  infrastructure, deployment/GitOps, platform, docs/playbook or lab.
- [ ] Boundary matches ownership, visibility, release and operational needs.
- [ ] Monorepo/multirepo decision is documented where multiple components or
  repositories are involved.
- [ ] Cross-repository dependencies use explicit versioned/documented
  contracts.

## Identity and Discovery

- [ ] Name follows repository naming conventions.
- [ ] Description states the durable capability or purpose.
- [ ] Topics/tags are relevant, safe to expose and not excessive.
- [ ] README serves as a navigable entry point.
- [ ] Owner and maintenance/lifecycle status are discoverable.

## Structure and Documentation

- [ ] Folder layout is appropriate for repository type.
- [ ] Configuration examples contain safe placeholders only.
- [ ] Delivery, runtime and operations documentation exists or is linked where
  the repository affects deployment.
- [ ] ADR structure exists or is linked for consequential architecture
  decisions.
- [ ] Templates/examples are sanitized and maintained.
- [ ] Onboarding allows a maintainer to validate or inspect the project without
  relying on undocumented knowledge.

## Visibility and Portfolio Publication

- [ ] Public/private/internal visibility is deliberate.
- [ ] Public publication review covers Git history, artifacts, logs,
  screenshots, data and rights/licensing.
- [ ] Public README accurately distinguishes reference, lab, active service or
  supported reusable project.
- [ ] Portfolio repositories demonstrate real maintained practices rather than
  unsupported claims.
- [ ] Internal or sensitive operating repositories are not exposed merely to
  provide public examples.

## Delivery and Security

- [ ] CI/CD behavior matches the repository output and authority.
- [ ] Production-affecting repositories use reviewed/protected changes
  appropriate to risk.
- [ ] Secrets and state are not committed or exposed in examples.
- [ ] Public/deployed repositories apply applicable scanning and dependency
  hygiene standards.
- [ ] Released or deployed outputs remain traceable to repository source.

## Ownership and Lifecycle

- [ ] Owner or maintaining team is identified.
- [ ] Consumers, deployments or downstream dependencies are known for shared
  or platform repositories.
- [ ] Versioning/release policy matches the produced artifact or documentation.
- [ ] Deprecated repositories link successors or migration status.
- [ ] Archived repositories remove unnecessary access/automation and state the
  archival reason before becoming read-only.

## Exception Record

```text
Control:
Repository/type:
Reason:
Operational or governance impact:
Compensating measure:
Owner:
Review/removal date:
```
