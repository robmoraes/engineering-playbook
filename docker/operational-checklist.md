# Docker Operational Checklist

Use this checklist when adding a containerized service, publishing an image or
reviewing a production deployment.

## Image and Dockerfile

- [ ] Image represents one independently deployed runtime responsibility.
- [ ] Dockerfile uses intentional stages and a lean supported runtime base.
- [ ] `.dockerignore` excludes secrets, credentials, local dependencies and
  irrelevant large files.
- [ ] Build and runtime dependencies are separated where practical.
- [ ] Dependency resolution and base-image update strategy are documented.
- [ ] No secrets are passed through persisted `ARG`/`ENV` or copied files.
- [ ] Runtime user is non-root unless an exception is recorded.
- [ ] Main process handles signals and exits correctly.

## Runtime Behavior

- [ ] Configuration is injected per environment, not baked into the image.
- [ ] Secret injection follows the security standard.
- [ ] Required writable paths and filesystem permissions are explicit.
- [ ] Healthcheck behavior is meaningful and does not leak data.
- [ ] Logs are emitted to standard streams and avoid sensitive values.
- [ ] Resource requests/limits or host capacity expectations are appropriate to
  the target environment.
- [ ] Graceful shutdown and interrupted work behavior are understood.

## Images and Registry

- [ ] Repository and tag names follow naming conventions.
- [ ] Published artifact is traceable to source revision and workflow run.
- [ ] Production deployment selects an immutable digest or approved immutable
  release identity.
- [ ] `latest` is not used as the sole production deployment reference.
- [ ] Registry credential is scoped for its automation purpose.
- [ ] Vulnerability scan result or documented exception exists for production
  artifacts.
- [ ] Provenance/SBOM is generated where workload exposure or consumer trust
  justifies it.
- [ ] Retention keeps deployed and rollback artifacts available.

## Networks and Storage

- [ ] Only intended ingress services publish public ports.
- [ ] Data services are isolated from public networks.
- [ ] Persistent data uses an explicit volume/storage design.
- [ ] Bind mounts are limited to intentional host coupling, normally
  development or controlled administration.
- [ ] Backup and restore behavior is documented for material state.
- [ ] Stateful scheduling and volume placement are understood for Swarm or
  other multi-node operation.

## Development and Production

- [ ] Local Compose values cannot access production systems.
- [ ] Development mounts/watch behavior is not required for the production
  image to function.
- [ ] Production configuration does not rely on developer host paths.
- [ ] Temporary or migration containers are controlled and removable.
- [ ] Debugging procedure does not require modifying a live production
  container as the deployed solution.

## Orchestration and Deployment

- [ ] Deployment automation uses a trusted published artifact.
- [ ] Swarm/Kubernetes secrets and permissions are scoped to the workload.
- [ ] Rollout and rollback/recovery behavior is defined.
- [ ] Deployment verification exercises health and relevant routed behavior.
- [ ] Migrations are coordinated explicitly and reviewed for rollback impact.
- [ ] Sidecars/init tasks are used only with an explicit lifecycle reason.

## Exception Record

```text
Control:
Workload/environment:
Reason:
Operational or security consequence:
Compensating measure:
Owner:
Review/removal date:
```
