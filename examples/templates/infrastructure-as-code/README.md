# Infrastructure-as-Code Templates

Provisioning templates and module usage examples that apply
[Infrastructure Standards](../../../infrastructure/README.md).

## Planned Template Families

| Directory | Purpose |
| --- | --- |
| `modules/` | Reusable infrastructure module boundaries and documented inputs/outputs |
| `environments/` | Development, staging and production-oriented composition patterns |
| `topologies/` | Provisioning examples tied to an explicit runtime topology |

Infrastructure templates must state provider assumptions, state/backend
handling, credentials required, cost implications, teardown/recovery behavior
and whether they are illustrative or intended as a reusable module baseline.

Terraform-specific additions should follow documented module and `examples/`
structure expectations from HashiCorp where that tool is chosen.
