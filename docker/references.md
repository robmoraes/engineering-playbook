# References and Adoption Notes

These sources define Docker platform behavior or established operating
guidance. This playbook adapts them to practical portfolio and production
systems. Its decisions to prefer one runtime image per independently deployed
capability, use digest-based production promotion and avoid unnecessary
orchestration complexity are local conventions rather than requirements of
Docker or Kubernetes.

## External Guidance and Adoption

| Source | Original guidance or platform behavior | Adoption in this playbook |
| --- | --- | --- |
| Docker Docs, *Building best practices* | Recommends multi-stage builds, trusted/minimal base images, `.dockerignore`, ephemeral containers, CI builds, cache awareness and regular rebuilds. | Dockerfiles separate runtime from build concerns, exclude sensitive context and treat running containers as replaceable. |
| Docker Docs, *Multi-stage builds* | Build stages can use different bases and selectively copy artifacts into a final stage. | Production examples ship runtime output rather than compiler/debug tooling. |
| Dockerfile Reference | Defines `CMD`, `ENTRYPOINT`, `USER`, `HEALTHCHECK`, `COPY` and BuildKit secret mounts. | Main process, runtime user, health behavior and secure build-secret patterns follow native Docker capabilities. |
| Docker Docs, *Build attestations* | Docker Build can attach provenance and SBOM attestations to pushed images. | Provenance/SBOM are recommended when public distribution or production trust justifies them. |
| Docker Docs, *Personal access tokens* | PATs are intended for automation and avoid exposing Docker Hub passwords. | Publishing uses scoped automation tokens rather than account passwords. |
| Docker Docs, *Compose* and *Compose Develop Specification* | Compose defines multi-container applications and supports development synchronization/watch behavior. | Compose is the local development baseline; development mounts/watch are kept out of production assumptions. |
| Docker Docs, *Deploy services to a swarm* and *Manage sensitive data with Docker secrets* | Swarm services define desired state, update/rollback behavior, placement/resources and secret mounts. | Swarm examples use immutable images, runtime secrets, resources and explicit rollout consequences. |
| Kubernetes Docs, *Probes*, *Resource Management* and *Sidecar Containers* | Kubernetes distinguishes startup/readiness/liveness probes, resources and sidecar lifecycle semantics. | Portable images expose health and shutdown behavior; Kubernetes-specific probes/sidecars are adopted only where deployed. |
| The Twelve-Factor App, *Processes*, *Config* and *Logs* | Processes are stateless, configuration is external and logs are event streams. | Runtime state, environment configuration and logging conventions are externalized from images. |
| OWASP, *Docker Security Cheat Sheet* | Recommends least privilege, trusted images, non-root operation and protection of secrets. | Container runtime baseline aligns security controls with delivery and operations. |
| Open Container Initiative, *Image Format Specification* | Defines the interoperable OCI image format and descriptors used by container tooling. | Image artifacts are treated as portable registry-stored deployment inputs; no platform-specific claim is made beyond supported tooling. |

## Source Links

- Docker Docs, *Building best practices*:
  <https://docs.docker.com/build/building/best-practices/>
- Docker Docs, *Multi-stage builds*:
  <https://docs.docker.com/build/building/multi-stage/>
- Docker Docs, *Dockerfile reference*:
  <https://docs.docker.com/reference/dockerfile/>
- Docker Docs, *Build attestations*:
  <https://docs.docker.com/build/metadata/attestations/>
- Docker Docs, *Personal access tokens*:
  <https://docs.docker.com/security/for-developers/access-tokens/>
- Docker Docs, *Docker Compose*:
  <https://docs.docker.com/compose/>
- Docker Docs, *Compose Develop Specification*:
  <https://docs.docker.com/reference/compose-file/develop/>
- Docker Docs, *Deploy services to a swarm*:
  <https://docs.docker.com/engine/swarm/services/>
- Docker Docs, *Manage sensitive data with Docker secrets*:
  <https://docs.docker.com/engine/swarm/secrets/>
- Kubernetes Docs, *Liveness, Readiness, and Startup Probes*:
  <https://kubernetes.io/docs/concepts/workloads/pods/probes/>
- Kubernetes Docs, *Resource Management for Pods and Containers*:
  <https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/>
- Kubernetes Docs, *Sidecar Containers*:
  <https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/>
- The Twelve-Factor App, *Processes*:
  <https://12factor.net/processes>
- The Twelve-Factor App, *Config*:
  <https://12factor.net/config>
- The Twelve-Factor App, *Logs*:
  <https://12factor.net/logs>
- OWASP, *Docker Security Cheat Sheet*:
  <https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html>
- Open Container Initiative, *Image Format Specification*:
  <https://github.com/opencontainers/image-spec>

## Local Conventions

- Separate application and web images only when runtime ownership, scaling or
  security boundaries justify the operational overhead.
- Use Compose for consistent development and explicitly simple deployments;
  introduce an orchestrator only when deployment requirements demand it.
- Retain debugging capability through telemetry or debug tooling rather than
  bloating every production image.
- Treat all production state, rollback and credential lifecycle concerns as
  system responsibilities outside the image itself.
