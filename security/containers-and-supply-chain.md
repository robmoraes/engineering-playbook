# Containers and Supply Chain

Container security has two parts: build trustworthy artifacts and run them
with limited authority. A minimal image is useful, but it is not a substitute
for provenance, patching and runtime isolation.

## Container Runtime Baseline

- Containers SHOULD run as a non-root user unless a documented capability
  requires otherwise.
- Images MUST NOT contain secrets, local credentials or environment-specific
  secret files.
- Runtime filesystem access, mounts, ports and capabilities SHOULD be limited
  to application needs.
- Health checks SHOULD reflect application readiness without disclosing
  sensitive information.
- Production deployments MUST reference an identifiable image version or
  digest.

```dockerfile
FROM node:22-alpine AS runtime
WORKDIR /app
COPY --chown=node:node dist/ ./dist/
USER node
CMD ["node", "dist/server.js"]
```

```text
Good                              Avoid
Non-root runtime user             Running app as root by default
Secret mounted at runtime         COPY .env.production /app/.env
Image digest in production        Deploying :latest
```

## Optional Hardening

Apply when supported by the workload and deployment platform:

- read-only root filesystem;
- dropped Linux capabilities and no privilege escalation;
- explicit resource limits;
- network segmentation between public, application and data layers;
- base image and operating system vulnerability scanning;
- reduced or distroless runtime images when operability remains acceptable.

Do not select a hardening measure blindly. For example, a distroless image
reduces utilities and packages but can complicate emergency diagnostics. Use
telemetry and a debug procedure that compensates for that tradeoff.

## Image Selection and Trust

Prefer:

- official or organization-maintained base images;
- explicit version or digest pinning for production-sensitive builds;
- small supported runtime images;
- documented upgrade cadence for base images.

Avoid:

- anonymous community images for critical workloads without review;
- floating base tags as the only build reference for repeatable releases;
- copying binaries from undocumented download locations.

An image being public does not make it trusted. Record origin, version and
verification method for infrastructure-critical images such as reverse
proxies, observability components and deployment tooling.

## Image Publication and Promotion

The build pipeline SHOULD build once and promote the same immutable artifact:

```text
Build:   ghcr.io/acme/orders-api:sha-a13f2c91
Release: ghcr.io/acme/orders-api:1.8.2
Deploy:  ghcr.io/acme/orders-api@sha256:<verified-digest>
```

Do not rebuild separately for production after testing staging. Rebuilds can
introduce dependency or base-image changes not exercised by validation.

## Vulnerabilities and Patching

**Baseline:** scan application dependencies and production container images at
least during releases or before production deployment.

**Recommended:** run scanning in CI, track actionable high-impact findings and
rebuild images regularly for base image security updates.

**Advanced:** enforce deployment policy against defined severity and
exploitability criteria, with time-bound, documented exceptions.

A scanner finding is not automatically a release blocker. Evaluate whether the
package is present in the runtime image, reachable in the application context,
fixed upstream and relevant to exposure.

## Provenance and Signing

**Recommended for published or deployed artifacts:** retain source revision,
workflow run and image digest as release evidence.

**Advanced for higher trust boundaries:** generate and verify signed image
provenance or attestations before deployment, following a supply-chain
framework such as SLSA.

For a personal portfolio, an immutable digest and public workflow linking
source to image provides meaningful trust without requiring a full signing
platform. Add signature and attestation verification when other consumers
depend on the artifact or production impact grows.

## Orchestrator-Specific Notes

For Docker Swarm:

- use Swarm secrets rather than environment variables or files baked into
  images for runtime secret delivery;
- restrict access to manager nodes;
- isolate ingress and data networks by purpose;
- deploy immutable images and record the stack version or digest.

For Kubernetes-based workloads:

- apply a restricted workload security posture where compatible;
- avoid mounting service account tokens unless the workload needs Kubernetes
  API access;
- use namespaces and RBAC to segment workloads and operators;
- protect Secret access and consider encryption at rest or an external secret
  store for production workloads.
