# Platform Templates

Reusable runtime and shared-platform definitions for containerized delivery
and infrastructure-aware service operation.

## Planned Template Families

| Directory | Purpose |
| --- | --- |
| `swarm/` | Stack definitions, service constraints, secrets and rolling update patterns |
| `reverse-proxy/` | Generic edge routing and TLS termination layouts |
| `traefik/` | Traefik-specific dynamic/static configuration examples |
| `networks-and-storage/` | Runtime segmentation and persistent storage attachment patterns |
| `kubernetes/` | Optional future manifests when a Kubernetes use case is documented |

Swarm and Kubernetes content must remain separate because their control-plane,
networking, secrets and recovery behaviors differ. Local development Compose
content belongs in [Container Templates](../containers/), not here.
