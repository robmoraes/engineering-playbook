# Observability Checklist

Use this checklist for a new deployed service, a monitoring stack change or a
production readiness review.

## Identity and Scope

- [ ] Service, component, environment and running release are identifiable
  across telemetry.
- [ ] Owner and operator response route are known.
- [ ] Application, platform, infrastructure and delivery visibility
  responsibilities are clear.
- [ ] Telemetry uses canonical naming and environment mapping.

## Logs and Correlation

- [ ] Production events are structured or consistently parseable.
- [ ] Material failures use stable event/error classifications.
- [ ] Request, job or trace correlation exists where workflow boundaries need
  investigation.
- [ ] Logs do not expose credentials, secrets or unnecessary sensitive data.
- [ ] Aggregation and retention fit incident need and access risk.
- [ ] Loki/indexed labels, if used, are bounded and intentionally selected.

## Metrics and SLOs

- [ ] User-relevant outcomes and latency/completion behavior are measured.
- [ ] Important dependencies, queues and saturation signals are available.
- [ ] Prometheus-style names use stable quantities and base units.
- [ ] Metric labels avoid unbounded values and cardinality growth is reviewed.
- [ ] Production-critical behavior has a defined SLI/SLO or documented reason
  it does not yet require one.

## Alerts and Dashboards

- [ ] Paging alerts represent actionable user impact or recovery risk.
- [ ] Alert labels identify service, environment and severity.
- [ ] Alerts link to a dashboard/query and runbook or first response.
- [ ] Grouping, inhibition or silencing strategy avoids alert floods.
- [ ] Dashboard hierarchy supports symptom-to-cause drill-down.
- [ ] Trusted operational dashboards are maintained and not uncontrolled
  copies.

## Runtime and Platform

- [ ] Healthchecks distinguish local liveness, readiness and external service
  behavior as applicable.
- [ ] Container/host/node capacity and runtime failure are observable.
- [ ] Swarm quorum/service state or Kubernetes workload/cluster concerns are
  covered where applicable.
- [ ] Shared ingress, registry, secrets, backup and telemetry infrastructure
  expose relevant operating signals.
- [ ] Deployment evidence can be correlated with behavior changes.

## Pipeline, Cost and Security

- [ ] Collection endpoints and credentials are not unnecessarily public or
  broadly privileged.
- [ ] Collector/exporter failure and telemetry loss can be detected.
- [ ] Metrics, logs and trace retention are intentional.
- [ ] Sampling, scrape rate, log volume and cardinality have cost controls
  proportional to scale.
- [ ] Public screenshots or dashboards are sanitized.

## Diagnostics and Lifecycle

- [ ] Operators can follow a standard troubleshooting workflow.
- [ ] Material alerts have current runbooks and recovery verification.
- [ ] Incident review captures useful telemetry gaps or alert noise.
- [ ] Retired services remove obsolete alerts, dashboards, collectors and
  storage cost safely.

## Exception Record

```text
Service/platform:
Standard not applied:
Reason and tradeoff:
Operational/security/cost impact:
Interim control:
Owner:
Review date or trigger:
```
