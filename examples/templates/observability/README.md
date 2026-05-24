# Observability Templates

Reusable telemetry stack and signal configuration applying
[Observability Standards](../../../observability/README.md).

## Planned Template Families

| Directory | Purpose |
| --- | --- |
| `prometheus/` | Scrape configuration, recording rules, alert rules and exporters |
| `loki/` | Low-cardinality log collection and retention examples |
| `grafana/` | Provisioned dashboards and data source layouts |
| `opentelemetry/` | Collector and service correlation patterns |
| `structured-logging/` | Application log schema and pipeline handling |
| `slo-and-alerting/` | SLIs, SLOs, burn-rate or actionable alert examples |

Templates must state expected cardinality, retention, access and sensitive-data
assumptions. Telemetry configuration that cannot be operated or queried safely
is not a reference template.
