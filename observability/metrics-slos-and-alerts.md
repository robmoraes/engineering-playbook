# Metrics, SLOs and Alerts

Metrics are best for rates, trends, saturation and objective evaluation.
Alerts should be derived from conditions where an operator can reduce impact
or prevent an imminent failure.

## Prometheus Metric Standard

Metrics and label keys use lowercase snake case and base units:

```text
orders_http_requests_total{method="GET", status_code="200"}
orders_http_request_duration_seconds_bucket{route="/checkout", le="0.5"}
orders_queue_depth{queue="payments"}
process_cpu_seconds_total
```

Rules:

- metrics SHOULD represent one quantity with a stable meaning;
- use `_total` for counters;
- use base-unit suffixes such as `_seconds` and `_bytes`;
- label dimensions MUST be bounded and useful for aggregation;
- initialize known expected series where absence would make alerting
  ambiguous;
- do not generate metric names dynamically per tenant, route ID or error text.

```text
Good                                      Avoid
status_code="500"                        user_id="109482"
route="/orders/{id}"                     path="/orders/109482"
duration_seconds                         latency_ms
```

## Cardinality Budget

Every label combination creates a distinct time series. Cardinality affects
memory, storage, query behavior and alert reliability.

Prefer bounded labels:

```text
service, environment, method, status_code, region, queue
```

Keep in logs or traces:

```text
request_id, trace_id, user_id, email, raw URL, container ID
```

For a new metric, ask:

```text
How many distinct series exist today?
How does it grow with users, requests, instances or routes?
Will an operator aggregate by this dimension?
Can detail live in logs/traces instead?
```

## Service Level Indicators and Objectives

An SLI measures behavior a user or dependent system cares about. An SLO states
the acceptable target and evaluation window.

| Workload | Example SLI | Example SLO direction |
| --- | --- | --- |
| Public HTTP API | successful eligible requests / eligible requests | availability over rolling period |
| Interactive endpoint | successful request latency distribution | proportion below latency threshold |
| Worker pipeline | jobs completed within expected delay | timely completion over period |
| Backup service | successful verified restores | restoration validation expectation |

Example working SLO:

```text
Service: orders-api production checkout endpoint
SLI: eligible checkout requests returning non-server-error response
Target: 99.5% successful over 30 days
Exclusions: documented synthetic and client-aborted requests only
Source: Prometheus request metric plus route definition
Response: error-budget burn alert and investigation runbook
```

Do not define SLOs solely from easy infrastructure metrics such as CPU use.
CPU can explain risk; it rarely describes whether users completed an order.

## RED and USE Views

| Method | Use for | Signals |
| --- | --- | --- |
| RED | Request-serving services and user symptoms | Rate, errors, duration |
| USE | Resources and infrastructure causes | Utilization, saturation, errors |

RED commonly drives service health and paging. USE commonly supports diagnosis
and capacity decisions. Apply them as practical lenses, not mandatory
dashboard branding.

## Alerting Philosophy

Page when prompt human action is necessary for material user impact or
recovery risk. Create a ticket or dashboard signal for conditions that should
be investigated but do not justify interruption.

```text
Page                                      Ticket/dashboard
Sustained critical API error rate        Gradual disk growth with weeks remaining
Production public route unreachable      One transient task restart
Backup failure threatening recovery      Low-volume debug log anomaly
```

Every paging alert SHOULD include:

- service and environment;
- symptom and severity;
- current value and condition;
- relevant dashboard or query;
- runbook or first response;
- owner/routing destination.

## Prometheus Alert Example

```yaml
groups:
  - name: orders-api-slo
    rules:
      - alert: OrdersApiHighErrorRate
        expr: |
          sum(rate(orders_http_requests_total{environment="prod",status_code=~"5.."}[5m]))
          /
          sum(rate(orders_http_requests_total{environment="prod"}[5m]))
          > 0.05
        for: 10m
        labels:
          service: orders-api
          environment: prod
          severity: page
        annotations:
          summary: Orders API elevated production error rate
          runbook_url: https://docs.example.com/runbooks/orders-api-errors
```

Thresholds and windows are examples only; adopt values from user impact,
traffic characteristics and SLO decisions.

## Noise Reduction and Alertmanager

Use Alertmanager routing, grouping, inhibition and silences to reduce
notification noise without hiding real user impact:

- group many replica alerts beneath a service/cluster-level symptom;
- inhibit secondary component symptoms during a known broader outage;
- use time-bounded silences for controlled maintenance;
- review recurring alerts that operators routinely dismiss.

Alert fatigue is usually a signal of weak alert design or unresolved
reliability debt, not a reason to train operators to ignore pages.
