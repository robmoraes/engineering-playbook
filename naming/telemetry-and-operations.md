# Telemetry and Operations

A resource name is only useful if it remains recognizable in metrics, logs,
traces and alerts. Telemetry SHOULD preserve the same system and component
vocabulary used by deployments.

## Service Identity

For OpenTelemetry resource attributes, use the stable logical service identity:

| Attribute | Value example | Purpose |
| --- | --- | --- |
| `service.namespace` | `orders` | Application or product grouping |
| `service.name` | `api` | Logical component, stable across replicas |
| `service.version` | `1.8.2` | Running release |
| `deployment.environment.name` | `production` | Deployment environment |

Alternatively, a small system may use `service.name=orders-api` without a
namespace. Pick one model across all services and dashboards; do not mix both
for the same application.

```text
Good                              Avoid
service.name=api                  service.name=api-prod-pod-7fd8b
service.version=1.8.2             service.name=api-v1-8-2
deployment.environment.name=production
                                  deployment.environment.name=prod
```

Instance IDs are useful for debugging, but they are not service names and
should not be primary dashboard groupings.

The playbook uses short resource suffixes such as `prod` and `stg`.
OpenTelemetry defines well-known values `production` and `staging` for
`deployment.environment.name`. This is a deliberate integration-boundary
mapping, not competing names for runtime resources.

## Kubernetes-Compatible Labels

Where Kubernetes labels are used or anticipated, adopt its recommended
application vocabulary:

```yaml
labels:
  app.kubernetes.io/name: api
  app.kubernetes.io/instance: orders-prod
  app.kubernetes.io/component: backend
  app.kubernetes.io/part-of: orders
  app.kubernetes.io/version: 1.8.2
  app.kubernetes.io/managed-by: helm
```

Use organization-specific keys with a DNS prefix:

```yaml
platform.example.com/environment: prod
platform.example.com/owner: platform
```

Labels used for selection MUST describe stable workload identity. Do not place
commit SHAs, request IDs or timestamps in selectors.

## Prometheus Metric and Label Names

Metric names and label keys use lowercase snake case:

```text
orders_http_requests_total
orders_checkout_duration_seconds
build_info{service="orders-api", environment="prod", version="1.8.2"}
```

Rules:

- Prefix application-specific metrics with a stable system name.
- Include base-unit suffixes such as `_seconds` or `_bytes`.
- Use `_total` for counters.
- Keep label keys bounded and reusable: `service`, `environment`, `method`,
  `status_code`.
- Never use unbounded values such as `request_id`, email address, raw URL or
  user ID as metric labels.

```text
Good                              Avoid
http_request_duration_seconds     http_request_duration_ms
environment="prod"                env="production-us-east-new"
status_code="500"                 request_id="<unique-id>"
```

The anti-cardinality rule is operational: an apparently convenient identifier
can turn one metric into an expensive and slow-to-query time-series set.

## Log Field Identifiers

Structured logs MUST use consistent field keys. Prefer established semantic
fields where the logging pipeline supports them:

```json
{
  "service.name": "api",
  "service.namespace": "orders",
  "deployment.environment.name": "production",
  "service.version": "1.8.2",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "request_id": "req-8fe1c4",
  "event": "checkout_failed"
}
```

Use `snake_case` for local event fields and retain dotted OpenTelemetry
resource keys where they are integrated with tracing. A logging backend that
does not support dotted keys MAY map them centrally, for example
`service_name`, but the mapping must be consistent across applications.

Do not encode dynamic context into the logger name:

```text
Good                              Avoid
event=checkout_failed             logger=orders-api-prod-user-2391-failed
request_id=req-8fe1c4            metric label request_id=req-8fe1c4
```

## Alerts and Dashboards

Operator-facing display text may be readable title case, but alert labels and
dashboard variables should use the canonical values:

```text
Display title: Orders API - Elevated Error Rate
Labels:        service=orders-api environment=prod severity=critical
```

This lets an operator pivot from an alert to logs, metrics and deployment
inventory. Where OpenTelemetry resource attributes are queried, the documented
boundary mapping from `prod` to `production` applies consistently.
