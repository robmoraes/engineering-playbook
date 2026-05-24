# Container Templates

Copyable container-building and local-runtime patterns that apply
[Docker Standards](../../../docker/README.md).

## Planned Template Families

| Directory | Purpose |
| --- | --- |
| `dockerfiles/` | Production-oriented Dockerfiles and multi-stage build patterns |
| `php-fpm-nginx/` | Separate application runtime and web/edge process model |
| `compose/` | Development and deliberately operated Compose topologies |
| `healthchecks/` | Runtime health behavior paired with validation guidance |
| `networking-and-storage/` | Intentional networks, volumes and state boundaries |

## Boundaries

- Place small teaching fragments in [Container Snippets](../../snippets/containers/).
- Place a complete deployed platform example in
  [Reference Implementations](../../reference-implementations/).
- Do not commit runtime secrets or claim that a Compose template alone
  provides production availability or backup.
