# Security Templates

Adaptable examples that expose safe interfaces for configuration, secrets and
container/runtime security without including credentials.

## Planned Template Families

| Directory | Purpose |
| --- | --- |
| `environment-configuration/` | `.env.example` and environment contract patterns |
| `secret-delivery/` | References to runtime secret objects and rotation-safe consumption |
| `container-hardening/` | Non-root, filesystem/capability and image trust patterns |

Examples MUST use placeholders and document the real secret store or identity
integration expected from a consuming project. Security response procedures
belong under [Operational Scenarios](../../operational-scenarios/).
