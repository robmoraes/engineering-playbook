# Security Baseline Checklist

Use this checklist when creating a project, enabling CI/CD, preparing a public
portfolio release or reviewing a persistent deployment. Not every advanced
item is required; every unchecked baseline item needs remediation or an
explicit exception.

## Repository and Publication

- [ ] `.gitignore` excludes local environment files, private keys, credentials
  and sensitive exports.
- [ ] Example configuration contains keys and safe placeholder values only.
- [ ] No credentials, production data, private keys or sensitive Terraform
  state appear in repository history or release artifacts.
- [ ] Secret scanning or an equivalent review step is enabled before public
  publication.
- [ ] Documentation, screenshots and sample logs are sanitized for public use.

## Secrets and Credentials

- [ ] Every deployed secret has an identifiable consumer, environment, owner
  and revocation route.
- [ ] Production and non-production credentials are separate.
- [ ] Automation uses tokens or workload identities rather than personal
  passwords.
- [ ] Stored credentials have the smallest practical scope.
- [ ] Long-lived production credentials have a rotation or review procedure.

## Identity and Access

- [ ] Human administration uses individual identities and MFA where supported.
- [ ] Application runtime, CI publisher and production deployer identities are
  separated where their permissions differ.
- [ ] Preview and test workloads cannot read or write production resources.
- [ ] SSH private keys are not shared casually or stored in repositories.
- [ ] Elevated or emergency production access has a documented recovery path.

## CI/CD and Automation

- [ ] Workflow permissions are explicit and minimal.
- [ ] Pull request validation does not expose publication or deployment
  credentials.
- [ ] Production secrets are protected by an environment or equivalent
  deployment authorization boundary.
- [ ] Privileged third-party actions are reviewed and pinned immutably where
  practical.
- [ ] Production deployment records the image tag or digest and workflow run.
- [ ] OIDC federation is considered for cloud deployment instead of static
  long-lived keys.

## Containers and Runtime

- [ ] Container images contain no embedded secrets.
- [ ] Workloads run as non-root unless a justified exception is recorded.
- [ ] Production deploys a versioned or digest-pinned image, not only
  `latest`.
- [ ] Image and dependency vulnerability scanning runs before production
  deployment or release.
- [ ] Runtime secrets are injected through the platform, not committed
  configuration.
- [ ] Public, internal and data-plane network access is limited by purpose
  where the deployment supports it.

## Operations and Response

- [ ] Logs do not include tokens, authorization headers, passwords or
  credential-bearing URLs.
- [ ] Operators know how to revoke registry, CI and deployment credentials.
- [ ] A rollback or redeploy path exists for an untrusted image.
- [ ] A lightweight incident record template is available.

## Optional Hardening Review

- [ ] Short-lived workload or federated identity replaces static cloud keys.
- [ ] Centralized vaulting, audit trail or dynamic secrets is justified by
  workload impact.
- [ ] Image signing or provenance verification is appropriate for consumers and
  trust boundaries.
- [ ] Container capability restrictions and read-only filesystems are
  compatible with runtime needs.
- [ ] Administrative access is network restricted or time limited.

## Exception Record

When a baseline control cannot be met, record:

```text
Control:
Affected system and environment:
Reason:
Risk accepted:
Compensating measure:
Owner:
Review or removal date:
```
