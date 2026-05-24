# Actions and Delivery Integration

GitHub Actions workflows can validate changes, publish artifacts and deploy
environments. A workflow with registry or production access is privileged
delivery code and must be reviewed accordingly.

## Workflow Organization

Use `.github/workflows/` with workflow roles visible from filenames:

```text
.github/workflows/
├── build-and-test.yml
├── publish-image.yml
├── deploy-stg.yml
├── deploy-prod.yml
└── reusable-container-build.yml
```

Follow job and display naming rules in
[CI/CD: GitHub Actions Workflows](../ci-cd/github-actions-workflows.md).

```text
Good                                      Avoid
deploy-prod.yml                          workflow-new-final.yml
name: Deploy Production                  name: CI2
job: publish_image                       job: job1
```

## Workflow Boundaries

| Workflow type | Typical authority | Must not receive |
| --- | --- | --- |
| Pull request validation | Source read and test execution | Production/deployment or image publish credentials |
| Trusted artifact publication | Package/registry write for owned image | General production administration |
| Staging deploy | Staging deploy identity/secrets | Production secrets |
| Production deploy | Protected production deploy identity | Unreviewed PR source execution |

Do not combine all roles in one workflow merely because GitHub Actions permits
it. Separate triggers and secrets when their authority differs.

## Validation Workflow Example

```yaml
name: Build and Test

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<reviewed-full-sha>
      - run: ./scripts/test.sh
```

For a portfolio repository, a visible green validation workflow is useful
evidence only when its commands actually exercise the documented project.

## Registry and Docker Hub Integration

Image publication should occur only from trusted branches/tags or explicitly
authorized workflows:

```yaml
- name: Log in to Docker Hub
  uses: docker/login-action@<reviewed-full-sha>
  with:
    username: ${{ vars.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_PUBLISH_TOKEN }}
```

Rules:

- use a scoped automation token, not an account password;
- never expose publish tokens to arbitrary pull-request code;
- publish immutable trace tags and preserve resulting digest;
- deploy a verified digest according to CI/CD standards.

For GHCR packages associated with the repository, prefer `GITHUB_TOKEN` with
only required `packages` permission rather than a separately stored long-lived
token when the workflow and package permissions support it.

## Environments and Deployments

Use GitHub environments to separate privileged deployment contexts:

```text
stg
prod
```

Production deployment SHOULD configure:

- production-only secrets or federated identity boundary;
- authorized deployment branches/tags or controlled manual dispatch;
- required reviewer where another responsible reviewer exists and impact
  justifies the control;
- concurrency protection preventing overlapping deploys to the same service;
- deployment evidence including selected version/digest and verification.

Environment approval is not a substitute for tests. It is a boundary for the
decision to apply a tested artifact to a sensitive environment.
GitHub only releases environment secrets to a job after the applicable
environment protection rules are satisfied; use that boundary intentionally
for production authority. Feature availability for private/internal
repositories depends on the GitHub plan in use and must be verified during
repository setup.

## Reusable Workflows and Automation Governance

Use reusable workflows when the same delivery contract is needed across
repositories. Treat them as versioned platform components:

- document inputs, outputs, permissions and required secrets;
- publish immutable/versioned references for callers;
- review breaking changes against consumers;
- keep high-impact actions visible in calling workflows or linked docs;
- identify an owner for dependency/security updates.

```text
Good                                      Avoid
Reusable build with documented inputs    Shared deploy workflow changed silently
Version-pinned reusable workflow         Calling mutable workflow from every prod repo
```

For a small portfolio with a few repositories, copied concise workflows may be
more understandable than premature central workflow governance.

## Self-Hosted Runners

Prefer GitHub-hosted runners for public repositories unless the job requires
private network access, specialized compute or another justified constraint.

Self-hosted runner requirements:

- do not run untrusted public fork code on runners with internal or production
  access;
- isolate runner groups/workflows by trust level;
- patch and monitor runner hosts;
- prevent persistence of credentials or job changes between runs;
- restrict network reachability and repository permission to what the job
  requires.

An inexpensive self-hosted runner is not a cost optimization if it becomes a
durable path from untrusted code to production systems.

## CI/CD Auditability

For production-facing repositories, retain or link:

- merged PR and reviewed source revision;
- workflow run creating the artifact;
- image/package digest or release artifact identifier;
- deployment run and actor/authorization boundary;
- verification and rollback reference.

This evidence allows incident response and rollback without reconstructing the
delivery path from terminal history.
