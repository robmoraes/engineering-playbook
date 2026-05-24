# Automation and Environments

Automation names need to work both in configuration syntax and in the
operator-facing CI/CD interface.

## GitHub Actions Workflows

Use distinct conventions for the workflow file, its display name and job
identifier:

| Element | Convention | Example |
| --- | --- | --- |
| Workflow file | lowercase kebab-case `.yml` | `.github/workflows/build-and-test.yml` |
| Workflow `name` | readable Title Case | `Build and Test` |
| Workflow `run-name` | action, target and traceable input | `Deploy orders-api to prod - v1.8.2` |
| Job ID | lowercase snake_case | `publish_image`, `deploy_prod` |
| Step `name` | imperative readable text | `Publish immutable image` |

```yaml
name: Deploy Production
run-name: Deploy orders-api to prod - ${{ inputs.image_tag }}

jobs:
  deploy_prod:
    name: Deploy to production
```

Use `-` in filenames because they are browsed and referenced as files. Use `_`
in job IDs because they are expression keys inside YAML and are frequently
referenced by `needs.deploy_prod`.

```text
Good                              Avoid
build-and-test.yml                pipelineFinal_NEW.yml
Deploy Production                 prod
publish_image                     Publish Image
```

## Pipeline and Stage Names

A pipeline should describe its outcome, not the tool executing it:

```text
build-and-test
publish-image
deploy-stg
deploy-prod
security-scan
```

Stages use a small stable vocabulary: `validate`, `test`, `build`, `scan`,
`publish`, `deploy`, `verify`, `rollback`. This makes pipeline order and
permissions legible across repositories.

Environment-specific deployment jobs MAY include the environment because their
permissions and approval gates differ: `deploy_stg` and `deploy_prod`.

## Environment Vocabulary

Use one canonical short value across deployment resource names, playbook-owned
labels, dashboard selectors and pipeline inputs:

| Value | Purpose | Persistent? | Production data permitted? |
| --- | --- | --- | --- |
| `dev` | Developer integration environment | Optional | No |
| `test` | Automated or manual verification | Optional | No |
| `stg` | Production-like release validation | Yes | Sanitized only |
| `prod` | Live user-facing workload | Yes | Yes |
| `sandbox` | Experiments and learning | Optional | No |
| `preview` | Per-change disposable review deployment | No | No |

Do not mix aliases such as `qa`, `stage`, `staging`, `prd` and `production`
within these owned identifiers. An external semantic convention may require a
translation. For example, OpenTelemetry
`deployment.environment.name` uses `production` and `staging`; map `prod` to
`production` and `stg` to `staging` at instrumentation or collection time.

## Environment in Names

Include an environment suffix where it prevents collision or makes a risky
operation explicit:

```text
orders-prod                 # Swarm stack
orders-api-db-password-prod # Shared secret store identifier
api.stg.example.com         # DNS endpoint
deploy_prod                 # Privileged deployment job
```

Omit the environment when an artifact is intended for promotion or its scope
already isolates environments:

```text
orders-api                  # Container image repository
@acme/http-client           # Internal package
api                         # Service inside stack orders-prod
```

## Environment Variables

Application environment variables MUST use uppercase snake case:

```text
DATABASE_URL
REDIS_TLS_ENABLED
OTEL_SERVICE_NAME
LOG_LEVEL
```

Prefix project-specific variables when collision or ownership is otherwise
unclear:

```text
ORDERS_RETRY_LIMIT
ORDERS_CHECKOUT_TIMEOUT_SECONDS
```

Never encode an environment in a variable key when the value changes by
deployment:

```text
Good                              Avoid
DATABASE_URL                      PROD_DATABASE_URL
API_BASE_URL                      STAGING_API_BASE_URL
```

The deployment supplies a different value for `DATABASE_URL` in each
environment. This keeps config external to code and prevents conditional
configuration from proliferating.

## Temporary and Preview Resources

Disposable resources MUST be recognizable and carry an expiration mechanism in
metadata or automation:

```text
<system>-preview-pr-<number>
<purpose>-tmp-<ticket-or-date>

portfolio-preview-pr-184
loadtest-tmp-OPS-244
```

Required metadata where the platform supports labels or tags:

```text
lifecycle=temporary
owner=platform
expires-at=2026-06-01
source-ref=pr-184
```

Names such as `test`, `temp2` and `new-prod-copy` are operationally unsafe:
they do not identify ownership or permit reliable cleanup.
