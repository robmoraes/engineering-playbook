# CI/CD and Automation Security

Delivery pipelines sit between source code and production authority. Treat a
workflow that can publish an image or deploy production as privileged code.

## Pipeline Baseline

- Workflows MUST request only the permissions needed for their jobs.
- Production secrets MUST be bound to protected production environments or
  equivalent deployment gates.
- Pull requests from untrusted contexts MUST NOT receive deployment or
  publication credentials.
- Third-party workflow dependencies SHOULD be pinned to an immutable version,
  preferably a full commit SHA for privileged workflows.
- Logs and artifacts MUST NOT expose credentials or sensitive configuration.

## GitHub Actions Permissions

Set `GITHUB_TOKEN` permissions explicitly at workflow or job scope:

```yaml
name: Build and Test

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<full-commit-sha>
```

A release job may require additional narrowly stated permissions:

```yaml
permissions:
  contents: read
  packages: write
  id-token: write
```

`id-token: write` permits obtaining an OIDC token; it does not by itself grant
cloud deployment access. Trust policy at the target provider must restrict the
repository, workflow context, branch or environment allowed to assume the
role.

```text
Good                              Avoid
contents: read for tests          permissions: write-all
packages: write only in publish   Write permissions in PR validation
```

## Secrets in GitHub Actions

Use repository secrets only for credentials shared by all appropriate
workflows in that repository. Use environment secrets for deployment values
that differ in sensitivity and authorization:

```text
Repository secret: DEMO_REGISTRY_READ_TOKEN
Environment secret: PROD_DEPLOY_SSH_KEY
Environment secret: PROD_DATABASE_MIGRATION_TOKEN
```

Recommended production setup:

- configure a `prod` GitHub environment;
- restrict deployment branches or tags;
- require review before production deployment where another reviewer exists;
- store production-only credentials in that environment;
- avoid exposing secrets to arbitrary reusable workflows or pull requests.

Never intentionally print secret values to verify they exist. Validate the
operation that consumes the secret instead.

## Federated Credentials and OIDC

**Recommended:** prefer GitHub Actions OpenID Connect federation for cloud
deployment over long-lived cloud access keys. The workflow receives
short-lived credentials after satisfying provider trust conditions.

Operational tradeoff:

- OIDC reduces static secret rotation and leak persistence.
- It requires careful trust policy configuration; an overly broad repository
  or branch condition can grant unintended deployment access.

For small hosted projects whose provider does not support federation, a
narrowly scoped deployment token stored in a protected environment is
acceptable, provided it can be revoked and is not available to PR builds.

## Docker Hub and Registry Tokens

Registry credentials MUST be separated by action:

| Consumer | Required scope |
| --- | --- |
| Public image pull | No token unless rate limits require it |
| CI image publisher | Write only to required repositories |
| Production deployer | Pull/read only when images are private |
| Registry administrator | Human/admin workflow only, never application runtime |

Use Docker access tokens rather than account passwords for automation, and use
separate tokens for publishing and production pulling when feasible.

```text
Good                              Avoid
CI token writes orders-api only   Docker Hub account password in Actions
Production token reads images     One admin token used by CI and hosts
```

## Deployment Credentials

Deployment automation should authorize an operation, not confer general host
ownership.

Baseline for SSH-based deployment:

- dedicated deployment key or user;
- production credential stored only in the production deployment environment;
- target host fingerprint managed intentionally;
- command output reviewed so secret values are not echoed.

Recommended evolution:

- use orchestrator or cloud deployment identity rather than remote shell;
- gate production deployment on a reviewed artifact;
- record artifact digest, workflow run and actor for rollback and audit.

## Workflow Dependency Trust

A workflow executes actions and scripts with the permissions granted to its
job. Therefore:

- Pin privileged third-party actions to immutable full SHAs.
- Review dependency changes before merging workflow updates.
- Restrict who can modify workflow files or require code owner review when a
  project has multiple maintainers.
- Do not run untrusted pull request code in a job that has secrets or elevated
  repository permissions.

This control matters even in a public portfolio: a compromised build workflow
can publish a malicious image under a trusted project name.
