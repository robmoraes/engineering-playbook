# GitHub Actions Workflows

GitHub Actions is the default workflow example in this playbook because it is
practical for public repositories and portfolio projects. The principles still
apply when another CI/CD system is used.

## File and Job Conventions

Use naming from
[Naming: Automation and Environments](../naming/automation-and-environments.md):

| Element | Convention | Example |
| --- | --- | --- |
| Workflow file | kebab-case `.yml` | `build-and-test.yml` |
| Workflow display name | readable title | `Build and Test` |
| Job ID | snake_case | `publish_image` |
| Step name | action-oriented phrase | `Publish immutable image` |

Recommended workflow files:

```text
.github/workflows/
├── build-and-test.yml
├── publish-image.yml
├── deploy-stg.yml
├── deploy-prod.yml
└── reusable-container-build.yml
```

Do not split workflows until their triggers, permissions or operational roles
are genuinely distinct. A small application can start with validation and
publish in one trusted workflow.

## Validation Workflow Example

```yaml
name: Build and Test

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: validate-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Check out source
        uses: actions/checkout@<full-commit-sha>
      - name: Set up runtime
        uses: actions/setup-node@<full-commit-sha>
        with:
          node-version: "22"
          cache: npm
      - name: Install locked dependencies
        run: npm ci
      - name: Run tests
        run: npm test
```

Operational intent:

- `contents: read` avoids unnecessary repository write authority.
- Concurrency cancels stale validation work for an updated branch.
- Locked dependency installation supports repeatability.
- Full SHA action pinning is particularly valuable in privileged workflows;
  teams may apply it everywhere for consistency.

## Publication Workflow Example

```yaml
name: Publish Image
run-name: Publish orders-api - ${{ github.sha }}

on:
  push:
    branches: [main]

permissions:
  contents: read
  packages: write

jobs:
  publish_image:
    runs-on: ubuntu-latest
    steps:
      - name: Check out source
        uses: actions/checkout@<full-commit-sha>
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@<full-commit-sha>
      - name: Authenticate to registry
        uses: docker/login-action@<full-commit-sha>
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - name: Build and publish immutable image
        uses: docker/build-push-action@<full-commit-sha>
        with:
          context: .
          push: true
          tags: ghcr.io/acme/orders-api:sha-${{ github.sha }}
          provenance: mode=max
```

Replace placeholder SHAs with reviewed immutable action revisions. For Docker
Hub, provide a repository-scoped access token stored as an appropriate secret
instead of a Docker Hub account password. This example uses Docker Build
provenance attached to the pushed image. If a workflow separately publishes
GitHub artifact attestations, grant only the additional permissions required by
that attestation action.

## Deployment Workflow Example

```yaml
name: Deploy Production
run-name: Deploy orders-api to prod - ${{ inputs.image_digest }}

on:
  workflow_dispatch:
    inputs:
      image_digest:
        description: Immutable published image digest
        required: true
        type: string

permissions:
  contents: read

concurrency:
  group: deploy-prod-orders-api
  cancel-in-progress: false

jobs:
  deploy_prod:
    environment: prod
    runs-on: ubuntu-latest
    env:
      IMAGE_DIGEST: ${{ inputs.image_digest }}
    steps:
      - name: Validate image digest input
        run: |
          [[ "$IMAGE_DIGEST" =~ ^sha256:[0-9a-f]{64}$ ]] || {
            echo "Invalid image digest input" >&2
            exit 1
          }
      - name: Deploy selected digest
        run: ./scripts/deploy-prod.sh "$IMAGE_DIGEST"
      - name: Verify production health
        run: ./scripts/verify-deployment.sh "https://api.example.com/health"
```

Use an environment-protected credential or OIDC identity inside the deploy
step according to the target platform. Do not cancel an in-progress production
deployment merely because a newer release is requested. Production scripts
must validate any externally supplied deployment selector before using it in a
command or manifest change.

## Reusable Workflows

Reusable workflows are appropriate when several repositories need the same
build or deployment contract.

Use them for:

- container build/publish with standard tags and metadata;
- standard validation for one technology stack;
- environment promotion with consistent evidence collection.

Rules:

- Publish reusable workflows with versioned references for consumers.
- Keep inputs and required secrets explicit.
- Do not hide high-impact deployment behavior behind an undocumented wrapper.
- Test changes against consuming repositories before broad rollout.

For one or two repositories, duplication may be easier to maintain than a
shared abstraction with no stable interface.

Minimal reusable container build contract:

```yaml
name: Reusable Container Build

on:
  workflow_call:
    inputs:
      image:
        required: true
        type: string
      tag:
        required: true
        type: string
    secrets:
      registry_token:
        required: true

jobs:
  publish_image:
    permissions:
      contents: read
      packages: write
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<full-commit-sha>
      - uses: docker/login-action@<full-commit-sha>
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.registry_token }}
      - uses: docker/build-push-action@<full-commit-sha>
        with:
          push: true
          tags: ${{ inputs.image }}:${{ inputs.tag }}
```

In a GitHub Container Registry workflow associated with the repository,
prefer passing `GITHUB_TOKEN` from the caller with only `packages: write`
authority rather than maintaining a separate long-lived registry token.

## Caching and Artifacts

Caching reduces repeated download/build time; artifacts preserve outputs needed
by later jobs or investigations.

| Mechanism | Use | Do not use for |
| --- | --- | --- |
| Dependency cache | Lockfile-keyed package downloads | Secrets or mutable deployment state |
| Build cache | Reusable container layers | Evidence of what was deployed |
| Workflow artifact | Test reports, SBOMs, metadata or signed build outputs | Long-term production artifact registry |
| Container registry | Versioned deployable images | Ad hoc debug output |

Restore caches from inputs that cannot be poisoned by untrusted workflows when
the subsequent job has privileged authority.

## Self-Hosted Runners

GitHub-hosted runners are the safer default for public repositories when they
can perform the work.

Self-hosted runners MAY be appropriate for private network access, specialized
hardware, large build cost or internal deployment paths. They introduce
operational responsibilities:

- runner host hardening, patching and isolation;
- prevention of persistence between jobs;
- access control for workflows permitted to target the runner;
- protection from untrusted pull-request execution;
- network reachability limited to required systems.

Never expose a production-connected self-hosted runner to arbitrary public fork
pull-request code.
