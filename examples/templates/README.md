# Templates

Reusable starting points intended to be copied into a project and adapted.
Templates demonstrate a maintained default, but they are not production
deployments without project-specific configuration, access controls and
verification.

## Template Contract

Each template MUST document:

- intended operating context;
- included files and extension points;
- values and credentials that must be supplied externally;
- validation commands or checks;
- production limitations and recovery implications;
- source standards and external references where applicable.

## Domains

| Folder | Template scope |
| --- | --- |
| [containers](./containers/) | Dockerfiles, Compose applications, healthchecks and app/web runtime split |
| [delivery](./delivery/) | GitHub Actions, image publishing, deployment and rollback workflows |
| [platform](./platform/) | Swarm, reverse proxy, Traefik, networks, storage and future Kubernetes |
| [observability](./observability/) | Telemetry stack, dashboards, alerts, logging pipeline and SLO material |
| [security](./security/) | Secret/configuration boundaries and runtime hardening |
| [infrastructure-as-code](./infrastructure-as-code/) | Provisioning modules and environment definitions |

## Template Lifecycle

A template should have an owner, review trigger and retirement/supersession
notice when assumptions change. Stale templates create repeatable mistakes.
