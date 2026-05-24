# Engineering Examples Catalog

Reusable examples and reference implementations that apply the standards in
this playbook to inspectable engineering artifacts.

## Purpose

This directory is not a snippet dump. It is a catalog for examples that
demonstrate a clear engineering concern, identify their operating assumptions
and remain safe to adapt for real projects.

Every added example should answer:

- Which standard does it apply?
- Is it explanatory, reusable as a starting point or an integrated reference
  implementation?
- Which environment is it intended for: local, lab, staging or production?
- What must be changed before use?
- How is it validated?
- What security, data, access or cost assumptions apply?

## Catalog Layers

| Layer | Purpose | Expected depth |
| --- | --- | --- |
| [Snippets](./snippets/) | Small focused patterns used to explain one concern | Minimal artifact plus concise rationale and cautions |
| [Templates](./templates/) | Starting points intended to be copied and adapted | Documented inputs, validation, security assumptions and lifecycle |
| [Reference Implementations](./reference-implementations/) | Integrated examples showing several standards working together | Architecture, delivery, operations, tradeoffs and recovery notes |
| [Decision Examples](./decision-examples/) | Sample ADRs and rationale-first decisions | Context, alternatives, consequences and adoption boundary |
| [Operational Scenarios](./operational-scenarios/) | Rehearsable troubleshooting and recovery examples | Symptoms, diagnostics, safe action and verification |

Use the smallest layer that communicates the intended pattern. A single
healthcheck should not be disguised as a complete production system; an
integrated deployment should not be fragmented into unexplained snippets.

## Domain Navigation

| Domain | Primary catalog location | Planned examples |
| --- | --- | --- |
| Containers and local runtime | [Templates: Containers](./templates/containers/) | Dockerfiles, multi-stage builds, PHP-FPM/NGINX split, Compose and healthchecks |
| Delivery automation | [Templates: Delivery](./templates/delivery/) | GitHub Actions, image publishing, deployment and rollback workflows |
| Runtime platform | [Templates: Platform](./templates/platform/) | Swarm stacks, reverse proxy, Traefik, networking, storage and future Kubernetes |
| Telemetry | [Templates: Observability](./templates/observability/) | Prometheus, Loki, Grafana, structured logging and SLO/alerts |
| Security and configuration | [Templates: Security](./templates/security/) | Environment configuration, secrets interfaces and hardening controls |
| Provisioning | [Templates: Infrastructure as Code](./templates/infrastructure-as-code/) | Infrastructure modules, environment topology and cloud foundations |
| Integrated systems | [Reference Implementations](./reference-implementations/) | Local lab, small production and platform capability examples |
| Operations | [Operational Scenarios](./operational-scenarios/) | Deployment failure, routing/TLS, data recovery and incident response |
| Architecture rationale | [Decision Examples](./decision-examples/) | ADR examples for boundaries, storage and orchestration choices |

## Required Example Metadata

Every executable or copyable example MUST include a `README.md` in its
directory with:

```text
Purpose:
Status: illustrative | template | reference implementation
Operating context: local | lab | staging | production-oriented
Standards demonstrated:
Prerequisites:
Configuration inputs:
Secret/data handling:
Validation:
Operational limitations:
Files:
References:
```

Start new entries from
[Example README Template](./example-readme-template.md) and remove sections
that are genuinely not applicable rather than leaving unclear placeholders.

Integrated reference implementations additionally SHOULD include:

- architecture or topology diagram;
- build/deploy flow;
- health and telemetry behavior;
- rollback or recovery route;
- known tradeoffs and cost/complexity assumptions;
- linked ADRs where a significant choice is demonstrated.

## Safety and Publication Rules

- Examples MUST NOT contain real credentials, private keys, production state,
  internal hostnames or unsanitized user/client data.
- Use synthetic identities such as `example.com`,
  `ghcr.io/acme/orders-api` and placeholder secret object names.
- Production-oriented means design discipline and documented tradeoffs; it
  does not mean an example can be deployed unchanged.
- Templates MUST identify values, permissions and dependencies that consumers
  must replace.
- Example outputs, screenshots, logs and diagnostics MUST follow
  [Security: Repository and Data Hygiene](../security/repository-and-data-hygiene.md).

## Naming and Structure Rules

- Directory and human-readable artifact names use lowercase kebab-case:
  `php-fpm-nginx`, `publish-image`, `small-production-service`.
- Preserve ecosystem-native filenames when required:
  `Dockerfile`, `compose.yaml`, `.env.example`, `prometheus.yml`.
- Do not create `misc/`, `tmp/`, `old/` or `final/` buckets. New material
  belongs to a named domain or should not be added.
- Each folder should remain focused enough that a maintainer can describe its
  purpose in one sentence.

See [Naming Standards](../naming/README.md) for delimiter and runtime naming
rules.

## Contribution Workflow

1. Choose the catalog layer and owning domain before creating files.
2. Link the standard the example demonstrates.
3. Add only enough artifacts to make the example coherent.
4. Provide validation and safe adaptation instructions.
5. Review for credentials, sensitive identifiers, excessive permissions and
   unsupported production claims.
6. Update the appropriate domain index when adding, superseding or retiring
   an example.

## References

External guidance and the conventions adapted for this catalog are listed in
[References](./references.md).
