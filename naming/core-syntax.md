# Core Naming Syntax

This document defines the shared vocabulary. Domain-specific documents may
tighten these rules when a platform imposes additional syntax.

## Normative Language

- **MUST** identifies a rule required for interoperability or operational safety.
- **SHOULD** identifies the default; exceptions need a recorded reason.
- **MAY** identifies an intentional option.

## Canonical Resource Slug

Use this shape for repositories, images, deployable services, networks,
infrastructure resources and host aliases whenever the platform supports it:

```regex
^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$
```

```text
Good                              Avoid
payments-api                      Payments_API
observability-grafana             observability.grafana
br-sp1-swarm-worker-01            swarm_worker_BR_01
```

Requirements:

- Use lowercase ASCII.
- Separate human-readable words with `-`.
- Start with a letter for compatibility with conservative DNS and Kubernetes
  label constraints.
- End with a letter or digit.
- Use stable words rather than deployment-specific details.
- Keep a DNS-facing label at 63 characters or fewer. Shorter names are easier
  to scan in dashboards and command output.

## Delimiters

| Delimiter | Use for | Example | Do not use for |
| --- | --- | --- | --- |
| `-` | Resource slugs and readable filenames | `catalog-worker`, `build-and-test.yml` | Environment variable word separation |
| `_` | Environment variables, Prometheus names, CI job identifiers | `DATABASE_URL`, `http_requests_total`, `publish_image` | DNS names, image repositories, Kubernetes object names |
| `.` | DNS hierarchy, file extensions, semantic versions and semantic telemetry keys | `api.stg.example.com`, `1.4.2`, `service.name` | Generic service word separation |
| `/` | Registry namespace, branch classification and qualified label prefix | `ghcr.io/acme/orders-api`, `feat/OPS-142-healthcheck`, `app.kubernetes.io/name` | Runtime resource slugs |
| `:` | Docker image tag separator and Prometheus recording rule syntax | `orders-api:1.4.2`, `job:http_requests:rate5m` | General identifiers |

The goal is not to force one punctuation mark everywhere. It is to give each
separator one predictable operational meaning.

## Vocabulary and Ordering

Use terms in the order that most quickly identifies ownership and purpose:

```text
<system>-<component>[-<purpose>][-<environment>]
orders-api
orders-db-backup-prod
edge-public-stg
```

Recommended terms:

| Concept | Values |
| --- | --- |
| Component | `api`, `web`, `worker`, `scheduler`, `db`, `cache`, `proxy` |
| Environment | `dev`, `test`, `stg`, `prod`, `sandbox`, `preview` |
| Network purpose | `public`, `private`, `data`, `monitoring`, `ingress` |
| Node role | `manager`, `worker`, `runner`, `gateway`, `monitoring` |

Choose one term and keep it: do not mix `production`, `prd` and `prod`, or
`backend`, `server` and `api` for the same capability.

## Abbreviations and Length

Well-understood technical abbreviations such as `api`, `db`, `ci`, `cdn`,
`tls` and region codes are acceptable. Avoid local abbreviations that require
tribal knowledge:

```text
Good                              Avoid
payments-api-prod                 pym-api-p
observability-loki                obs-lk
```

If a platform forces a length reduction, document the approved vocabulary in
the owning project and retain the full name in labels or descriptions.

## Scope and Uniqueness

A name needs to be unique in its actual namespace, not globally verbose.
Prefer `api` as a service inside stack `orders-prod`, because Docker Swarm
materializes it as `orders-prod_api`. Prefer `orders-api` when the service is
listed without a stack or namespace context.

Do not add the environment merely as decoration. Include it when two
environments may collide in the same account, cluster namespace, DNS zone,
secret store or dashboard.

## Operational Readability

Names appear during failures in narrow terminal columns, alerts and audit
logs. A useful name tells an operator what it belongs to and what it does,
without requiring a lookup:

```text
Good                              Avoid
catalog-worker-prod               app-03-prod-new
edge-public-prod                  network-final
```

Resource names are not inventories. Put owner, cost center, region, version
and lifecycle detail in labels or metadata unless they are required to
distinguish the resource.
