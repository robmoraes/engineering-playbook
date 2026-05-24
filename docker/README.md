# Docker Standards

Production-oriented standards for building, publishing and operating
containerized workloads consistently across local development, portfolio
services and managed deployment platforms.

## Container Position

Containers are packaging and runtime isolation boundaries, not a replacement
for application architecture or operational ownership.

Default position:

1. Build one immutable image for each independently deployed runtime.
2. Keep build tooling, runtime dependencies, configuration, secrets and
   persistent data intentionally separated.
3. Prefer small, supported and diagnosable runtime images over image-size
   optimization without operating benefit.
4. Run containers as replaceable processes and attach durability externally.
5. Deploy production by traceable image version or digest with health,
   rollback and security controls appropriate to impact.

## Usage Contexts

| Context | Practical default |
| --- | --- |
| **Development** | Compose-based dependencies, bind mounts or watch workflows, debug tooling and non-production data only |
| **Personal/lab** | Simple image builds and Compose/Swarm deployment are appropriate when credentials and public exposure remain controlled |
| **Production** | Multi-stage builds, non-root runtime, injected secrets, durable external state, immutable deployment reference and operational verification |
| **Enterprise-grade deployment** | Governed base images, provenance verification, vulnerability policy, workload restrictions and standardized platform integration where justified |

## Navigation

| Document | Covers |
| --- | --- |
| [Container Principles](./container-principles.md) | Container-first design, boundaries, tradeoffs and lifecycle model |
| [Dockerfiles and Builds](./dockerfiles-and-builds.md) | Dockerfile conventions, multi-stage builds, caching, dependencies and reproducibility |
| [Images and Registries](./images-and-registries.md) | Image naming, tags, Docker Hub/private registries, promotion and provenance |
| [Runtime and Process Model](./runtime-and-process-model.md) | Runtime users, entrypoints, configuration, healthchecks, logging and resources |
| [Networking and Storage](./networking-and-storage.md) | Networks, persistence, bind mounts, volumes, secrets and stateful concerns |
| [Compose and Local Development](./compose-and-development.md) | Compose conventions, local workflows, overrides, temporary containers and debugging |
| [Orchestration and Production](./orchestration-and-production.md) | Production deployment, Swarm, Kubernetes compatibility, sidecars and init tasks |
| [Operational Checklist](./operational-checklist.md) | Build, release, runtime and production review checklist |
| [References](./references.md) | External guidance and adopted conventions |

## Non-Negotiable Defaults

- Images MUST NOT contain committed secrets, runtime credentials or production
  environment files.
- Production MUST deploy a traceable immutable image tag or digest, never only
  `latest`.
- Persistent application data MUST NOT rely only on the disposable writable
  container layer.
- Containers SHOULD run as non-root unless a documented technical requirement
  justifies an exception.
- A production service MUST expose enough health and logging behavior to
  verify deployment and diagnose failure.

## Related Standards

- Image naming and tags:
  [Naming: Source Control and Artifacts](../naming/source-control-and-artifacts.md).
- Artifact build, publication and promotion:
  [CI/CD: Build and Artifacts](../ci-cd/build-and-artifacts.md) and
  [CI/CD: Deployments and Promotion](../ci-cd/deployments-and-promotion.md).
- Runtime hardening and supply chain:
  [Security: Containers and Supply Chain](../security/containers-and-supply-chain.md).
- Runtime topology and platform selection:
  [Architecture: Runtime and Platform Topology](../architecture/runtime-and-platform-topology.md).
