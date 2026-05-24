# Delivery Templates

Reusable automation baselines that apply [CI/CD Standards](../../../ci-cd/README.md)
and [GitHub Standards](../../../github/README.md).

## Planned Template Families

| Directory | Purpose |
| --- | --- |
| `github-actions/` | Build, test, publish and reusable workflow templates |
| `image-publishing/` | Registry authentication, tagging and immutable digest publication |
| `deployments/` | Environment promotion and controlled deployment paths |
| `rollback/` | Recovery workflows paired with verification and data-compatibility notes |

Each workflow template must document required secrets/identity, workflow
permissions, environment protection, artifact identity and safe validation.
