# Source Control and Artifacts

These conventions cover source repositories and the immutable artifacts that
move through the delivery pipeline.

## Git Repositories

Repositories MUST use lowercase kebab-case:

```text
<system>[-<component-or-purpose>]
```

| Purpose | Good | Avoid |
| --- | --- | --- |
| Deployable application | `orders-api` | `Orders.API.Service` |
| Frontend | `portfolio-web` | `portfolio_front_end` |
| Infrastructure repository | `platform-infrastructure` | `infraStuff` |
| Shared operational tooling | `platform-deploy-tools` | `scripts-final` |

Do not repeat the GitHub organization in repository names. The namespace
already supplies ownership: `acme/orders-api`, not
`acme/acme-orders-api`.

## Branches

Use `main` as the default protected branch. Working branches use a type prefix
and a short hyphenated description:

```text
<type>/[<ticket>-]<description>

feat/OPS-142-add-healthcheck
fix/OPS-203-image-promotion
docs/naming-standards
chore/update-runner-image
```

Allowed type prefixes are `feat`, `fix`, `hotfix`, `docs`, `chore`, `refactor`
and `test`. Keep ticket identifiers in their tracker casing when used.

Release branches use a version, not a calendar nickname:

```text
release/v1.8
release/v1.8.2
hotfix/v1.8.3-db-timeout
```

| Good | Avoid | Reason |
| --- | --- | --- |
| `feat/OPS-142-add-healthcheck` | `feature/new health check!` | Safe in shells and CI filters |
| `release/v2.1` | `release/latest` | Identifies supported release line |
| `fix/token-refresh` | `carlos-fix` | Names work, not individuals |

Git allows a wider character set. This playbook deliberately limits branches
to letters, digits, `-`, `_`, `.` and one `/` separator pattern because these
names are routinely passed through shells, workflow filters and release tools.

## Internal Libraries and Packages

Library names represent a reusable capability and SHOULD not carry an
environment or runtime:

```text
JavaScript package:  @acme/http-client
Go module:           github.com/acme/observability-kit
Python distribution: acme-observability
```

Use the package ecosystem's mandated namespace or punctuation. Do not rewrite
an established ecosystem convention solely to look like a runtime resource.

```text
Good                              Avoid
@acme/http-client                 @acme/http_client_prod
acme-observability                shared-utils-new
```

## Files and Directories

Author-created documentation, scripts and configuration directories SHOULD use
lowercase kebab-case:

```text
deploy-and-rollback.md
github-actions/
docker-compose/
```

Preserve conventional or tool-required filenames exactly:

```text
README.md
Dockerfile
Makefile
.github/workflows/build-and-test.yml
compose.yaml
```

Avoid spaces, mixed case in custom paths, and duplicate suffixes such as
`deployment-final-v2.yaml`.

## Docker Image Repositories

A container image repository names one distributable component:

```text
[<registry>/]<namespace>/<system>-<component>

ghcr.io/acme/orders-api
docker.io/acme/portfolio-web
registry.example.com/platform/reverse-proxy
```

Use one image repository per independently deployed runtime. Do not put
environment in the image repository: the same immutable image should be
promoted from staging to production.

| Good | Avoid | Reason |
| --- | --- | --- |
| `ghcr.io/acme/orders-api` | `ghcr.io/acme/orders-api-prod` | Environment is deployment state |
| `ghcr.io/acme/orders-worker` | `ghcr.io/acme/orders-all` | Independently deployable artifact |
| `ghcr.io/acme/reverse-proxy` | `MyRegistry/Proxy_Image` | Portable lowercase repository name |

## Docker Tags and Digests

Every release image MUST receive an immutable tag, and production deployment
SHOULD resolve to an immutable digest.

| Use | Format | Example |
| --- | --- | --- |
| Released artifact | Semantic version | `1.8.2` |
| Source traceability | Git SHA prefix | `sha-a13f2c91` |
| Pull-request validation | PR number and SHA | `pr-184-a13f2c91` |
| Human convenience alias | Controlled mutable alias | `stable`, `1.8` |

```text
ghcr.io/acme/orders-api:1.8.2
ghcr.io/acme/orders-api:sha-a13f2c91
ghcr.io/acme/orders-api@sha256:<digest>
```

Do not deploy `latest` to a long-lived environment. It does not state which
artifact is running and can silently point to different content over time.
Do not use `prod` as the only image tag; promotion is an environment decision,
not a build identity.
