# References and Adoption Notes

The structure in this catalog is a local organization model for this playbook.
The external sources below inform artifact types and reusable-example
expectations; they do not prescribe this entire directory hierarchy.

## Adopted and Adapted Guidance

| Source | Source guidance used | Convention adopted here |
| --- | --- | --- |
| Docker Docs, *Samples overview*, *Multi-stage builds* and *Docker Compose* | Docker provides application/platform samples; Dockerfiles and Compose describe container images and multi-container applications; multi-stage builds separate build and final runtime contents. | Container examples are organized as reusable templates and integrated implementations, with dedicated space for Dockerfiles, Compose and runtime patterns. |
| Docker Docs, *Swarm mode* | Swarm is a production runtime option with services, discovery, networking, load balancing and rolling updates; Compose remains appropriate when Swarm is not the runtime. | Swarm deployment examples remain separate from local Compose examples and must document operating assumptions. |
| GitHub Docs, *Reusable workflows* and `actions/starter-workflows` | Workflow reuse and maintained templates reduce duplication and establish repeatable automation starting points. | GitHub Actions examples belong under reusable delivery templates with documented permissions, secrets and validation. |
| HashiCorp Terraform, *Standard Module Structure* | Terraform recommends documented module structures and an `examples/` directory for usages that consumers can understand and adapt. | Infrastructure-as-Code examples include README boundaries and distinguish modules/templates from complete topology references. |
| Kubernetes Documentation, *Configuration Best Practices* | Maintainable Kubernetes configurations favor explicit, debuggable and organized manifests using stable APIs. | Kubernetes is reserved as a future platform template area; added manifests must be minimal, documented and validation-oriented. |
| AWS Well-Architected Framework, *Operational Excellence - Use runbooks to perform procedures* | Operational procedures require inputs, tools, permissions, exception handling, escalation and validation, and may be automated where appropriate. | Operational scenarios include diagnostics, action safety and recovery verification rather than isolated shell fragments. |
| OpenTelemetry Demo | A reference implementation can demonstrate interconnected services and observability signals as a coherent system. | Complete examples may combine several playbook standards, but must state scope and operational tradeoffs. |

## Source Links

- Docker Docs, *Samples overview*: <https://docs.docker.com/en/latest/examples/>
- Docker Docs, *Multi-stage builds*:
  <https://docs.docker.com/build/building/multi-stage/>
- Docker Docs, *Docker Compose*: <https://docs.docker.com/compose/>
- Docker Docs, *Swarm mode*: <https://docs.docker.com/engine/swarm/>
- GitHub Docs, *Reusing workflow configurations*:
  <https://docs.github.com/en/actions/concepts/workflows-and-actions/reusing-workflow-configurations>
- GitHub, `actions/starter-workflows`:
  <https://github.com/actions/starter-workflows>
- HashiCorp Terraform, *Standard Module Structure*:
  <https://developer.hashicorp.com/terraform/language/modules/develop/structure>
- Kubernetes, *Configuration Best Practices*:
  <https://kubernetes.io/docs/concepts/configuration/overview/>
- AWS Well-Architected, *Use runbooks to perform procedures*:
  <https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_ready_to_support_use_runbooks.html>
- OpenTelemetry Demo:
  <https://opentelemetry.io/docs/demo/>

## Local Conventions

- `snippets/`, `templates/` and `reference-implementations/` distinguish
  explanatory depth and reuse intent; this classification is local.
- Domain directories match the standards already documented in this
  repository and should evolve with those standards.
- Empty catalog boundaries are documented intentionally so future additions
  can be scoped before executable files are introduced.
- No example is treated as deployable production configuration without explicit
  prerequisites, validation, security review and operating limitations.
