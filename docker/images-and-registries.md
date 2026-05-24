# Images and Registries

Container images are release artifacts. Registry layout, tags, provenance and
retention affect deployment safety, rollback and supply-chain trust.

## Image Repository Layout

Use one repository per independently deployed runtime:

```text
<registry>/<namespace>/<system>-<component>

docker.io/acme/orders-api
docker.io/acme/orders-worker
ghcr.io/acme/portfolio-web
registry.example.com/platform/edge-proxy
```

Do not add environment to the image repository. A trusted image is promoted
through environments with different runtime configuration.

```text
Good                                      Avoid
acme/orders-api                          acme/orders-api-prod
acme/orders-worker                       acme/orders-monolith-final
```

## Tagging Strategy

| Tag type | Example | Mutability | Use |
| --- | --- | --- | --- |
| Source trace tag | `sha-a13f2c91` | Immutable | Build and audit traceability |
| Release tag | `1.8.2` | Immutable | Human-consumable release version |
| Preview tag | `pr-184-a13f2c91` | Immutable or short-retained | Review environment artifact |
| Convenience alias | `1.8`, `stable` | Mutable by policy | Consumer convenience only |
| Floating convenience tag | `latest` | Mutable | Local/demo convenience, not production selection |

Production SHOULD select an image digest:

```text
ghcr.io/acme/orders-api@sha256:<verified-digest>
```

Semantic version tags are useful only when the software release contract uses
Semantic Versioning. An image for an internal continually deployed utility may
be fully traceable through a SHA tag and digest without pretending to offer a
public compatibility contract.

## Registry Roles

| Registry context | Practical use | Required discipline |
| --- | --- | --- |
| Docker Hub public repository | Public portfolio and broadly consumed images | Scoped publish token, clear tags, no embedded credentials |
| GitHub Container Registry | Source-linked public/private repository artifacts | Repository workflow permissions and package access reviewed |
| Private registry | Internal workloads or restricted artifacts | Availability, backups/retention, auth and deploy pull access owned |

A private registry improves access control; it does not make an unscanned or
untraceable image trustworthy.

## Publishing Workflow

Publication occurs from trusted CI/CD context after validation:

```text
test -> build -> scan -> publish SHA tag -> record digest/provenance
     -> release alias/version -> promote digest to deployment
```

Docker Hub authentication example:

```yaml
- name: Log in to Docker Hub
  uses: docker/login-action@<reviewed-full-sha>
  with:
    username: ${{ vars.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_PUBLISH_TOKEN }}

- name: Build and publish image
  uses: docker/build-push-action@<reviewed-full-sha>
  with:
    context: .
    push: true
    tags: acme/orders-api:sha-${{ github.sha }}
    provenance: mode=max
```

Registry credentials belong in CI secret storage and must never be supplied to
untrusted pull-request code.

## Provenance, SBOM and Scanning

Baseline:

- retain source revision, workflow run and resulting image digest;
- scan deployed or released images for relevant vulnerabilities;
- record accepted exceptions when a finding is not remediated immediately.

Recommended for published or higher-impact production images:

- generate build provenance attestations;
- generate an SBOM where consumers or incident response will use it;
- verify the expected source/build identity before sensitive deployment.

Advanced:

- signed attestations and policy enforcement at deployment admission or
  promotion boundaries.

Provenance shows how an artifact was built; it does not alone show that the
application is secure or operationally correct.

## Retention and Lifecycle

| Image category | Retention rule |
| --- | --- |
| Currently deployed digest | Retain |
| Known rollback candidate | Retain until replacement rollback path exists |
| Supported release tag | Retain for support window |
| Preview/PR images | Expire automatically after review window |
| Unreferenced development builds | Expire after investigation period |

Deleting all old images to save registry storage can remove the fastest safe
rollback option. Conversely, retaining every preview image forever creates
cost and obscures relevant artifacts.

## Base Image Governance

Choose official or trusted publisher images with documented maintenance. Track
base-image updates like dependency changes:

```text
Good                                      Avoid
Reviewed update to node runtime digest   Unknown third-party runtime image
Rebuild after security update            Assuming old immutable image is patched
```

An enterprise platform MAY maintain approved internal base images. A personal
portfolio normally benefits more from supported official bases plus regular
rebuilds than from operating a custom base-image program.
