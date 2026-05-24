# References

This section uses primary operational and tool documentation for signal,
query, correlation and alerting behavior. The particular document split,
baseline stack examples and maturity decisions are local playbook conventions,
not mandatory external frameworks.

## Adopted and Adapted Guidance

| Source | Source guidance used | Convention adopted here |
| --- | --- | --- |
| Google, *Site Reliability Engineering - Monitoring Distributed Systems* | Monitoring distinguishes symptoms and causes, combines blackbox and whitebox signals, and focuses on latency, traffic, errors and saturation for user-facing systems. | Service dashboards and diagnosis begin with user symptoms, then drill into infrastructure and dependencies. |
| Google, *Site Reliability Engineering - Service Level Objectives* and *Practical Alerting from Time-Series Data* | SLIs/SLOs should represent behavior users care about; alerts should support high-level service objectives and remain actionable. | Production-critical services define meaningful SLIs/SLOs and page for impact or recovery risk rather than routine component events. |
| Prometheus, *Metric and label naming* and *Instrumentation* | Metrics represent one quantity, use base units and bounded labels; high cardinality harms operational cost/performance. | Metric syntax and cardinality rules follow Prometheus-compatible conventions already established in naming standards. |
| Prometheus, *Alerting rules* and *Alertmanager* | Rules evaluate alert conditions; Alertmanager provides grouping, routing, inhibition and silencing. | Alerts carry owner/runbook context and use notification controls to reduce floods. |
| Prometheus, *Monitoring Docker container metrics using cAdvisor* and node exporter project | Container and host exporters provide infrastructure/resource signals for Prometheus collection. | cAdvisor and node exporter are optional runtime visibility tools with protected metric exposure. |
| OpenTelemetry, *Semantic Conventions* and *Logging* | Common resource attributes standardize signals; trace and span context can correlate logs with distributed traces. | Service/environment/version attributes and log-trace correlation use OpenTelemetry semantics where adopted. |
| Grafana, *Dashboard best practices* and *Provision Grafana* | Dashboards benefit from hierarchy, links, variables and managed/provisioned configuration. | Operational dashboards are organized for drill-down and version-controlled where loss or drift affects response. |
| Grafana Loki, *Understand labels*, *Structured metadata* and *Log retention* | Loki labels should be low cardinality; structured metadata supports high-cardinality query context; retention requires explicit configuration. | Indexed labels remain bounded, correlation detail is not promoted to streams, and retention is a deliberate cost/security decision. |
| OWASP, *Logging Cheat Sheet* | Logs should not include credentials or inappropriate sensitive content and need controlled handling. | Secret and payload exclusion is a logging baseline even when storage access is restricted. |

## Source Links

- Google SRE, *Monitoring Distributed Systems*:
  <https://sre.google/sre-book/monitoring-distributed-systems/>
- Google SRE, *Service Level Objectives*:
  <https://sre.google/sre-book/service-level-objectives/>
- Google SRE, *Practical Alerting from Time-Series Data*:
  <https://sre.google/sre-book/practical-alerting/>
- Prometheus, *Metric and label naming*:
  <https://prometheus.io/docs/practices/naming/>
- Prometheus, *Instrumentation*:
  <https://prometheus.io/docs/practices/instrumentation/>
- Prometheus, *Alerting rules*:
  <https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/>
- Prometheus, *Alertmanager*:
  <https://prometheus.io/docs/alerting/latest/alertmanager/>
- Prometheus, *Monitoring Docker container metrics using cAdvisor*:
  <https://prometheus.io/docs/guides/cadvisor/>
- Prometheus node exporter:
  <https://github.com/prometheus/node_exporter>
- OpenTelemetry, *Semantic Conventions*:
  <https://opentelemetry.io/docs/specs/semconv/>
- OpenTelemetry, *Logging*:
  <https://opentelemetry.io/docs/specs/otel/logs/>
- Grafana, *Dashboard best practices*:
  <https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/>
- Grafana, *Provision Grafana*:
  <https://grafana.com/docs/grafana/latest/administration/provisioning/>
- Grafana Loki, *Understand labels*:
  <https://grafana.com/docs/loki/latest/get-started/labels/>
- Grafana Loki, *Structured metadata*:
  <https://grafana.com/docs/loki/latest/get-started/labels/structured-metadata/>
- Grafana Loki, *Log retention*:
  <https://grafana.com/docs/loki/latest/operations/storage/retention/>
- OWASP, *Logging Cheat Sheet*:
  <https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html>

## Local Conventions

- Prometheus, Loki and Grafana form a practical reference stack, not a
  mandatory product selection.
- OpenTelemetry is introduced where correlation or backend portability solves
  a real operating need; it is not required for a simple lab.
- The observability maturity described here is proportional guidance rather
  than an external certification model.
- A smaller set of trustworthy signals and runbooks is preferred to a complex
  telemetry system no maintainer can operate.
