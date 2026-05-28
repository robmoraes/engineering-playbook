# Build and Artifacts

Artifacts should be reproducible enough to investigate, immutable enough to
promote and identifiable enough to roll back. Container images are the primary
deployment artifact in this playbook.

## Build Inputs

A build MUST be traceable to:

- source revision;
- dependency lockfiles or dependency resolution inputs;
- Dockerfile/build definition;
- base image reference;
- immutable revision identifiers for downloaded or generated build-time
  content, schemas, assets or other source repositories;
- workflow run and builder context;
- resulting image tag and digest when published.

```text
Good                                      Avoid
Image digest linked to source SHA        Image named latest with unknown build source
Lockfile used in build                   Dependency versions resolved unpredictably
Static content archive pinned to v2.4.1 Downloading content from main during release build
```

A build that imports files from another repository or service has more than
one source revision. Pin that input to an immutable tag, commit SHA or
content-addressed object before publishing a release candidate, and retain
that identifier with the image digest. Rebuilding identical application source
against a moving documentation, schema or asset branch is a different build,
even if its release label would otherwise be unchanged.

Perfect bit-for-bit reproducibility is not always attainable immediately.
Traceability and immutable outputs are the minimum operating requirement.

## Multi-Stage Container Builds

Use multi-stage Docker builds to keep build tools outside the runtime image and
reduce unnecessary runtime content:

```dockerfile
FROM node:22-alpine AS build
WORKDIR /src
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force
COPY --from=build /src/dist ./dist
USER node
CMD ["node", "dist/server.js"]
```

Tradeoff: multi-stage builds reduce runtime surface and separate build
concerns, but still require base-image upgrades, vulnerability review and
correct dependency handling.

## Docker Image Publication

Each independently deployable service receives one image repository:

```text
docker.io/acme/orders-api
ghcr.io/acme/orders-worker
```

Publication policy:

| Event | Publish? | Tags |
| --- | --- | --- |
| Pull request | Optional for preview/testing only | `pr-184-a13f2c91` |
| Merge to trusted `main` | Yes for deployable candidate | `sha-a13f2c91` |
| Release | Yes or alias existing digest | `1.8.2`, optionally `1.8` |
| Production deploy | Select immutable artifact | Digest preferred |

```text
Good                                      Avoid
orders-api:sha-a13f2c91                 orders-api:prod as only identity
orders-api:1.8.2 at known digest         orders-api:latest in production
```

Mutable aliases such as `stable` or minor-version tags may be offered for user
convenience, but deployment evidence must retain the immutable digest.
Full source SHA tags are also acceptable where workflow expression simplicity
is preferred over shorter display values; the important property is immutable
traceability.

## Docker Hub Publishing Example

For Docker Hub, configure a dedicated automation token with repository write
access where supported, store it in CI secret storage and publish from trusted
workflow contexts only:

```yaml
- name: Authenticate to Docker Hub
  uses: docker/login-action@<full-commit-sha>
  with:
    username: ${{ vars.DOCKERHUB_USERNAME }}
    password: ${{ secrets.DOCKERHUB_PUBLISH_TOKEN }}

- name: Build and publish image
  uses: docker/build-push-action@<full-commit-sha>
  with:
    push: true
    tags: acme/orders-api:sha-${{ github.sha }}
    provenance: mode=max
```

Do not use an account password, expose the token to pull request code or issue
a registry administrator token when one repository publication scope is enough.
Add a semantic version alias only in a trusted release workflow after its
release version and source revision are selected.

## Artifact Metadata

For each release candidate or production release, retain:

```text
repository:      acme/orders-api
source revision: a13f2c91...
build inputs:    docs-content@v2.4.1, when applicable
workflow run:    URL or run identifier
image digest:    sha256:...
release version: 1.8.2, when applicable
scan result:     pass, accepted exception or report link
provenance:      attestation reference, when generated
```

Store deployable container images in a registry, not as generic CI artifacts.
Store reports such as SBOMs, test outputs or provenance references where they
can be associated with the release and retained according to project needs.

## Build Cache

Cache can materially lower CI time and registry/build cost, but it is an input
to the build and must not compromise trust.

Recommended:

- key dependency caches by lockfile and runtime/toolchain version;
- use BuildKit-compatible container layer caching;
- isolate or avoid cache restoration across untrusted and privileged workflow
  contexts when poisoning would be material;
- treat a cache miss as slower execution, not build failure.

```text
Good                                      Avoid
npm cache keyed by package-lock hash     Reusing arbitrary PR-produced output for prod publish
Build cache used to accelerate rebuild   Cache storing plaintext credentials
```

## Container Image Lifecycle

Maintain lifecycle rules for registry storage:

| Artifact | Retention approach |
| --- | --- |
| Released version deployed or supported | Retain while rollback/support is required |
| SHA artifact used by current environments | Retain |
| Superseded PR/preview images | Expire automatically after review window |
| Failed or unreferenced build output | Expire after investigation window |

Retention saves cost only when it does not remove an artifact needed for
rollback, incident analysis or provenance.
