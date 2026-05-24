# Snippets

Focused fragments that illustrate one engineering decision without presenting
themselves as deployable solutions.

## Use This Area For

- a single Dockerfile instruction pattern;
- a healthcheck expression;
- a structured log event shape;
- a Prometheus alert expression fragment;
- a bounded network or configuration pattern;
- a diagnostic command example with safety note.

## Do Not Use This Area For

- complete Compose or Swarm applications;
- copy-ready CI/CD workflows;
- multi-service platform stacks;
- production recovery procedures.

Those belong in [Templates](../templates/) or
[Operational Scenarios](../operational-scenarios/).

## Planned Domains

| Folder | Intended content |
| --- | --- |
| [containers](./containers/) | Single-purpose Docker/runtime fragments |
| [delivery](./delivery/) | Small workflow and validation patterns |
| [observability](./observability/) | Metric, log, query and alert fragments |
| [operations](./operations/) | Read-only diagnostic command patterns |

## Addition Standard

Each snippet directory must state its teaching purpose, source standard,
assumptions, unsafe copy-paste risks and expected validation if adopted into a
real system.
