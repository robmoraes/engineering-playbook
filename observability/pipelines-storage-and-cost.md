# Pipelines, Storage and Cost

An observability pipeline is production infrastructure. If it fails silently,
operators may lose evidence at the same time a workload fails.

## Reference Small Production Topology

```text
Applications/containers -> structured stdout logs -> collector/agent -> Loki
Applications/exporters  -> metrics endpoints ------> Prometheus
Applications/SDKs       -> spans -------------------> OTel Collector -> trace backend
Blackbox probes         -> endpoint signals --------> Prometheus

Prometheus/Loki/traces -> Grafana dashboards
Prometheus rules       -> Alertmanager -> operator route
Deploy events          -> dashboard annotations and incident correlation
```

Tracing may be omitted initially for a simple service. Central logs, endpoint
visibility, deployment correlation and core metrics usually provide more
immediate operating value.

## Multi-Environment Strategy

| Context | Practical separation |
| --- | --- |
| Lab | Local or disposable stack; no production data |
| Portfolio service | Production telemetry protected from public access; sanitized material only for presentation |
| Small production | Environment label plus restricted production data source/access; separate alerts/routing |
| Higher-impact platform | Separate tenants/projects/stores or stronger access boundary where telemetry sensitivity or blast radius warrants it |

Production and non-production signals may share tooling where access,
retention and query behavior remain safe. They must remain distinguishable and
non-production must not generate false production pages.

## Collection and Service Discovery

Prometheus targets, log collectors and trace exporters need controlled
discovery:

- use runtime/orchestrator discovery where appropriate and constrain it to
  intended scrape/collection targets;
- apply stable service/environment identity at collection or instrumentation;
- do not expose metrics endpoints publicly by convenience;
- monitor collection target failure and collector/exporter health;
- document how ephemeral containers or Pods map to stable services.

Example Prometheus scrape configuration for a controlled Docker network:

```yaml
scrape_configs:
  - job_name: orders-api
    static_configs:
      - targets: ["orders-api:9090"]
        labels:
          service: orders-api
          environment: prod
```

For dynamic platforms, prefer supported service discovery rather than manually
maintaining rapidly changing instance lists.

## Storage and Retention

| Signal | Retention strategy consideration |
| --- | --- |
| High-resolution metrics | Useful for recent diagnosis; downsample or shorten when long-term precision has low value |
| SLO/recording-rule metrics | Longer retention may support reliability trend review |
| Error/operation logs | Retain for incident and release analysis subject to sensitivity |
| Verbose/debug logs | Short-lived or sampled; expensive and frequently unnecessary |
| Traces | Sample and retain according to distributed diagnosis need |
| Audit/security signals | Access-controlled retention according to investigation need |

Loki retention is not an assumption: configure retention intentionally and
coordinate it with underlying storage lifecycle behavior. A default indefinite
store can become both a cost issue and an exposure liability.

## Cardinality and Cost Controls

Primary telemetry cost drivers include:

- metric series cardinality and scrape frequency;
- Loki stream cardinality and log volume;
- trace volume, attributes and sampling rate;
- dashboard queries over broad/high-resolution windows;
- retention and replication/storage policy;
- telemetry egress or cross-zone movement.

Controls:

- reject or review unbounded labels/attributes before production;
- reduce debug log volume and unnecessary payload logging;
- choose scrape interval by operational need;
- create recording rules only for stable useful queries;
- sample traces deliberately;
- monitor the monitoring platform's resource/cost usage.

## Performance and Failure Handling

Instrumentation must not destabilize the workload it observes:

- exporters and SDKs SHOULD fail open for normal application traffic unless a
  stronger audit requirement explicitly demands otherwise;
- collectors need queue/buffer/drop behavior understood and monitored;
- avoid synchronous high-latency log or trace export in critical request paths;
- define what happens during telemetry backend outage;
- alert when observability loss prevents confident operation.

```text
Good                                      Avoid
App continues while collector reports loss Application blocks on Loki outage
Dropped telemetry measured                Silent exporter failures
```

## Tooling Complexity

Prometheus, Loki and Grafana can form a practical stack for small platforms.
OpenTelemetry can standardize correlation and exporter routing as distributed
needs grow. Avoid deploying every telemetry backend before there is an
operational question it answers.
