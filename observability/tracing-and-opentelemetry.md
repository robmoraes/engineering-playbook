# Tracing and OpenTelemetry

Tracing is valuable when a request crosses service, queue or provider
boundaries and operators need to understand where time or failure is spent.
It is not automatically required for a small single-service workload.

## When to Add Tracing

| Situation | Recommendation |
| --- | --- |
| One service with clear logs/metrics | Tracing optional |
| API calling database and one external provider | Add when latency/failure diagnosis is recurring |
| Several internal services or asynchronous workflow | Tracing strongly useful if context is propagated correctly |
| High-volume distributed platform | Use governed instrumentation, sampling and storage controls |

## OpenTelemetry Position

OpenTelemetry provides vendor-neutral APIs, SDKs, Collector capability and
semantic conventions across telemetry signals. Use its resource and
correlation model where instrumentation is introduced so that logs, traces
and metrics identify the same deployed service.

Recommended resource attributes:

```text
service.namespace=orders
service.name=api
service.version=1.8.2
deployment.environment.name=production
```

The repository naming standard defines how local `prod`/`stg` runtime slugs
map to OpenTelemetry `production`/`staging` resource values.

## Trace and Log Correlation

When tracing is enabled, include trace context in structured logs:

```json
{
  "event": "payment_provider_timeout",
  "service.name": "api",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7"
}
```

An operator should be able to:

1. observe a latency/error symptom in a dashboard;
2. locate representative traces for the affected service/release;
3. pivot from a trace span to correlated logs;
4. confirm whether the issue is application, downstream dependency, network
   or deployment related.

## Span Design

Instrument meaningful boundaries:

- inbound HTTP/RPC handling;
- outbound dependency calls;
- queue publish/consume and background job execution;
- datastore operations at useful semantic scope;
- significant business operation where it aids diagnosis.

Avoid:

- spans for every trivial local function;
- raw secret or personal data in span attributes;
- unbounded payload capture;
- high sampling/storage spend without an investigation use.

```text
Good                                      Avoid
Span external payment request            Span every JSON field conversion
Record provider outcome and latency      Attach full customer payload
```

## Context Propagation

Distributed tracing only works if context follows the work:

- propagate trace context across supported HTTP/RPC calls;
- pass or link context for asynchronous messaging where feasible;
- retain a safe business/job correlation identifier for support workflows;
- document where external dependencies break propagation.

Correlation IDs are still useful without full tracing, especially for jobs and
support cases. Do not delay structured logging while waiting to deploy a trace
backend.

## Sampling and Performance

Tracing adds CPU, network and storage overhead. Use a sampling policy
appropriate to volume and investigative need:

| Context | Practical approach |
| --- | --- |
| Lab/small low-volume production | Full or high sampling may be acceptable |
| Moderate production traffic | Sample normal requests; preserve errors/slow paths where supported |
| High-scale platform | Defined sampling policy, cost limits and validation of diagnostic coverage |

Sampling decisions must not silently eliminate the only evidence for a
critical failure path.

## Collector and Pipeline Boundaries

An OpenTelemetry Collector or equivalent gateway can standardize export,
resource enrichment, filtering and backend routing. It also becomes part of
the telemetry failure path.

Document:

- whether applications fail open if export is unavailable;
- resource attribute enrichment/mapping;
- redaction or dropping of unsafe attributes;
- queue/buffer and loss behavior;
- access credentials and backend destinations;
- monitoring of collector health and dropped telemetry.
