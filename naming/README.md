# Naming Standards

Consistent names reduce mistakes in deployment, incident response and automation. This
section defines stable naming rules for repositories, delivery artifacts, runtime
resources and operational telemetry.

## Standard

The default resource identifier is a lowercase, hyphen-separated slug:

```text
<system>-<component>[-<qualifier>]
orders-api
orders-worker
edge-public-prod
```

Names that may cross into DNS, Docker Swarm or Kubernetes contexts should be
portable by default: ASCII lowercase letters, digits and hyphens; start with a
letter; end with a letter or digit; keep each operational segment at 63
characters or fewer.

This is an adopted playbook convention, stricter than every individual
platform requires. It avoids translation rules as resources move between CI,
container registries, DNS and orchestration platforms.

## Navigation

| Document | Covers |
| --- | --- |
| [Core Syntax](./core-syntax.md) | Grammar, casing, delimiters, abbreviations and readability |
| [Source Control and Artifacts](./source-control-and-artifacts.md) | Repositories, branches, packages, files, Docker images and tags |
| [Automation and Environments](./automation-and-environments.md) | GitHub Actions, pipelines, environments and temporary resources |
| [Runtime and Infrastructure](./runtime-and-infrastructure.md) | Projects, stacks, services, networks, secrets, nodes and domains |
| [Telemetry and Operations](./telemetry-and-operations.md) | Monitoring labels, metrics and logging identifiers |
| [References](./references.md) | Official sources, external constraints and adopted decisions |

## Decision Rules

1. Name the durable capability, not its current implementation: use
   `orders-api`, not `orders-node-express`.
2. Put environment in the name only where resources from multiple
   environments share a namespace, account, registry view or DNS zone.
3. Keep version, build SHA and runtime instance identity in tags or metadata,
   not in stable service names.
4. Prefer names that can be read aloud during an incident and searched in logs,
   dashboards and the deployment platform.
5. Do not encode secrets, personal names, IP addresses or changeable topology
   in a resource name.

## Change Control

Naming changes can alter DNS records, monitoring continuity, secret mounts and
deployment targets. New rules should be added here before adoption in
templates. Existing production identifiers should be renamed only with a
documented migration and rollback plan.
