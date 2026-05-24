# Observability Standards

Standards for producing, collecting and using telemetry to operate software
and infrastructure safely in production.

## Observability Position

Observability exists to shorten the path from a user-visible symptom to a
correct operational decision. It is not measured by the number of agents,
dashboards or stored log lines.

Default position:

1. Measure user-relevant behavior and the dependencies needed to diagnose it.
2. Alert on actionable impact or imminent risk, not routine component noise.
3. Keep service, environment and release identity consistent across logs,
   metrics, traces, dashboards and deployment evidence.
4. Control sensitive data, cardinality, retention and telemetry cost from the
   start.
5. Add instrumentation depth as operating impact and distributed complexity
   justify it.

## Operating Contexts

| Context | Practical observability expectation |
| --- | --- |
| **Personal lab** | Useful logs, basic health/metrics and enough visibility to learn; no unsupported reliability claim |
| **Hosted portfolio service** | Structured logs, endpoint health, deploy correlation and safe public evidence of operation |
| **Small production environment** | Centralized logs, service and infrastructure metrics, actionable alerts, dashboards and recovery runbooks |
| **High-scale telemetry environment** | Governed schemas, SLO-driven alerting, retention/cardinality controls, tracing strategy and platform ownership |
| **Enterprise platform** | Shared telemetry pipelines, access isolation, reusable dashboards/rules, cost governance and lifecycle controls |

## Navigation

| Document | Covers |
| --- | --- |
| [Principles and Signal Model](./principles-and-signal-model.md) | Monitoring versus observability, signals, visibility boundaries and maturity |
| [Logging and Correlation](./logging-and-correlation.md) | Structured events, aggregation, correlation IDs, Loki and sensitive data |
| [Metrics, SLOs and Alerts](./metrics-slos-and-alerts.md) | Prometheus conventions, SLIs/SLOs, alert quality and Alertmanager patterns |
| [Tracing and OpenTelemetry](./tracing-and-opentelemetry.md) | Distributed tracing, resources, context propagation and adoption tradeoffs |
| [Dashboards and Visualization](./dashboards-and-visualization.md) | Grafana organization, RED/USE views, drill-downs and dashboard lifecycle |
| [Platform and Runtime Monitoring](./platform-and-runtime-monitoring.md) | Applications, infrastructure, containers, Swarm, Kubernetes and healthchecks |
| [Pipelines, Storage and Cost](./pipelines-storage-and-cost.md) | Collection topology, service discovery, retention, access, performance and cost |
| [Diagnostics and Incident Workflows](./diagnostics-and-incident-workflows.md) | Troubleshooting paths, runbooks and failure analysis |
| [Observability Checklist](./observability-checklist.md) | Instrumentation, production readiness and operational review |
| [References](./references.md) | External sources and conventions adapted here |

## Non-Negotiable Defaults

- Telemetry identity and identifiers MUST follow
  [Naming: Telemetry and Operations](../naming/telemetry-and-operations.md).
- Production services MUST expose enough telemetry to identify environment,
  version, critical-path health and material dependency failure.
- Logs MUST NOT contain secrets, authentication material or unnecessary
  sensitive payloads.
- Metrics and indexed log labels MUST avoid unbounded cardinality.
- A paging alert MUST identify impact, owner, dashboard/query and runbook or
  first response.
- Observability storage and administration MUST follow the same access and
  lifecycle discipline as other production data services.

## Related Standards

- Runtime topology and operational access:
  [Infrastructure Standards](../infrastructure/README.md).
- Reliability and architecture decisions:
  [Architecture Standards](../architecture/README.md).
- Runtime logging and health behavior: [Docker Standards](../docker/README.md).
- Security of logs and diagnostics: [Security Standards](../security/README.md).
- Deployment evidence and verification: [CI/CD Standards](../ci-cd/README.md).
