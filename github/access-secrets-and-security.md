# Access, Secrets and Security

Repository access and automation credentials must reflect what a person or
workflow actually needs to do. GitHub is often the first point from which
production authority, packages and public source can be altered.

## Access Model

| Principal | Typical permission | Reason |
| --- | --- | --- |
| Public visitor | Read public repositories only | Discover/evaluate content |
| Contributor | Fork/PR or triage as appropriate | Submit work without privileged change |
| Maintainer | Write/maintain selected repositories | Review and merge project changes |
| Platform owner | Admin only where settings/automation require it | Manage protected delivery boundaries |
| CI workflow | Explicit job-scoped token permissions | Perform one automated role |
| Deployment workflow | Environment-scoped deployment access | Change only intended environment |

Avoid granting admin rights to solve ordinary contribution or deployment
problems. Admin bypasses and settings changes increase the blast radius of
credential loss and mistakes.

## Team Permissions

For organization repositories:

- grant access through teams instead of individual exceptions where teams
  exist;
- separate maintainers, platform/deployment owners and security reviewers only
  where responsibilities differ;
- review dormant or elevated access periodically;
- avoid shared user accounts for automation.

For a personal account, use MFA and separate automation credentials from the
account's normal interactive authentication.

## Personal Access Tokens and Apps

Prefer in this order when practical:

1. `GITHUB_TOKEN` for workflow operations in its repository.
2. OIDC federation for external cloud deployment.
3. GitHub App installation access where organization automation needs
   controlled multi-repository access.
4. Fine-grained personal access token for a constrained integration that lacks
   a better identity method.
5. Classic PAT only when required by a platform capability and tightly scoped
   and managed.

Any long-lived token needs:

- named purpose and owner;
- minimum repository/permission scope;
- storage location;
- expiry/review and revocation procedure.

GitHub recommends GitHub Apps for organization access or long-lived
integrations. A PAT remains tied to the issuing user and can stop functioning
when that user's access changes; this is a material reliability concern for
shared automation.

```text
Good                                      Avoid
Fine-grained token for one integration   Classic PAT with repo/admin scopes for convenience
GITHUB_TOKEN for same-repo package push  Personal PAT embedded in workflow file
```

## Actions Secrets Scope

Place a secret at the narrowest scope matching its use:

| Scope | Use | Example |
| --- | --- | --- |
| Repository secret | Multiple trusted workflows in one repository need the same value | `DEMO_REGISTRY_READ_TOKEN` |
| Environment secret | Deployment authority/configuration differs by target environment | `PROD_DEPLOY_SSH_KEY` |
| Organization secret | Selected repositories use one maintained integration credential | Shared scanning integration token |

Environment-level secrets take precedence over repository and organization
secrets with the same name. Avoid relying on name shadowing as a design
mechanism; make environment purpose explicit in secret naming for privileged
values where it prevents mistakes.

Rules:

- restrict organization secrets to selected repositories unless all
  repositories genuinely need them;
- do not give production environment secrets to PR-triggered workflows;
- store Docker Hub publish tokens separately from production pull/deploy
  credentials;
- rotate/revoke credentials after suspected exposure before treating cleanup
  as complete.

See [Security: Secrets and Credentials](../security/secrets-and-credentials.md).

## Actions Security

Baseline for privileged workflows:

- declare minimal `permissions`;
- pin third-party actions to reviewed full commit SHAs;
- prevent untrusted pull request code from receiving secrets or powerful
  tokens;
- protect workflow files through review/CODEOWNERS where multiple maintainers
  exist;
- use environments or identity policy for production authorization;
- avoid printing configuration or secret values in logs.

```text
Good                                      Avoid
packages: write only in publisher job    permissions: write-all in validation
OIDC for cloud deploy                    Static cloud administrator key in secret
```

## Dependabot and Dependency Maintenance

Enable the dependency graph and Dependabot alerts where supported and relevant.
Configure version/security updates at a cadence that can actually be reviewed.

Tradeoffs:

| Configuration | Benefit | Cost |
| --- | --- | --- |
| Security alerts/updates | Faster visibility and fixes for known vulnerable dependencies | Review and compatibility testing required |
| Scheduled version updates | Reduces aging dependencies | PR volume/noise without triage discipline |
| Grouped updates | Less review noise | Larger combined compatibility surface |

For private registries, Dependabot secrets are separate from Actions secrets
and should receive read-only package access where possible.

## Code Scanning and Secret Scanning

Recommended for public repositories and production-facing code:

- secret scanning and push protection where available;
- dependency alerting for supported ecosystems;
- code scanning where the application language/exposure justifies it;
- required security checks for high-impact repositories once signal quality is
  sufficient.

Push protection helps stop supported secrets before they enter repository
history. It does not remove the need to revoke a credential if exposure has
already occurred or was bypassed.

Code scanning findings need triage. Blocking every low-confidence warning
without ownership produces bypass pressure rather than safer delivery.

## Auditability

At minimum, production-relevant changes should be attributable through:

- PR and review history;
- branch/ruleset enforcement;
- workflow run and deployment environment history;
- release/tag and artifact evidence;
- security alert resolution or credential rotation record when relevant.

Enterprise organizations may add centralized audit-log review and policy
reporting. Personal projects still benefit from avoiding untracked manual
production changes.
