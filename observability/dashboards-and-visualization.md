# Dashboards and Visualization

Dashboards should guide an operator from service impact to likely causes and
support routine capacity or release review. A wall of unrelated graphs slows
incident response.

## Dashboard Hierarchy

| Dashboard | Primary question |
| --- | --- |
| Service overview | Is user-facing behavior healthy? |
| Service detail | Which route, dependency, release or workload is affected? |
| Infrastructure/platform | Is node, cluster, network, storage or shared platform causing impact? |
| Deployment/release | Did a rollout correlate with behavior change? |
| SLO/reliability | Are objectives and error budget behavior acceptable? |

Alerts SHOULD link to the dashboard level appropriate for first diagnosis,
rather than forcing an operator to search.

## Grafana Organization

A practical folder model:

```text
Production/
  Service Overview/
    Orders API
  Platform/
    Edge and TLS
    Swarm Cluster
    Nodes and Capacity
    Telemetry Pipeline
  Reliability/
    SLO and Alert Review
Non-Production/
  Staging Validation
```

Use template variables for bounded dimensions such as `environment`,
`service`, `cluster` or `region` instead of copying a dashboard for every
node or deployment.

```text
Good                                      Avoid
One node dashboard with node variable    Copy of same dashboard per host
Version-controlled reviewed dashboard    Ad hoc edits lost after rebuild
Alert links to service overview          On-call browses folders during outage
```

## Service Overview Dashboard

For a request-serving service, begin with RED-oriented panels:

```text
Header: environment, service version, last deployment annotation, SLO state
Row 1: request rate, successful/error rate, latency percentiles
Row 2: top bounded routes/status classes, downstream error/latency
Row 3: runtime replicas, restarts, CPU/memory saturation
Links: logs, traces, runbook, deployment execution, platform dashboard
```

Keep application and infrastructure views connected. A slow API dashboard
should allow a pivot to database, ingress or node saturation without mixing
every low-level graph into the first view.

## Infrastructure Dashboards

USE-oriented dashboards commonly cover:

- host/node CPU, memory, disk and network saturation;
- container/task/Pod lifecycle and restart behavior;
- Swarm manager/worker or Kubernetes node/control-plane health;
- ingress/load balancer/TLS behavior;
- database/storage capacity and backup status;
- Prometheus/Loki/collector/Grafana health and ingestion failure.

Infrastructure panels explain causes and risk. Page primarily on
user-impacting symptoms or urgent recovery risks unless the infrastructure
component is itself the provided service.

## Dashboard Lifecycle

Dashboards SHOULD be maintained as reviewed configuration where operationally
important. Grafana supports provisioned/version-controlled dashboards; adopt
this when losing a dashboard or changing it unexpectedly would affect
production response.

Lifecycle rules:

- identify owner and intended use;
- annotate or display deployments where relevant;
- review unused/copied dashboards and remove sprawl;
- test changed queries against representative data;
- separate exploratory dashboards from trusted operational views;
- retire dashboards with their service or replace links in alerts/runbooks.

## Security and Sharing

Dashboard access may reveal internal service names, failure modes, traffic
volume, user behavior or log excerpts. For public portfolios:

- publish sanitized screenshots or curated metrics only;
- omit internal endpoints and identifiers;
- avoid public administrative dashboards;
- do not display log panels containing unsanitized data.
