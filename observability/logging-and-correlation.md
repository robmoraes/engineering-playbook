# Logging and Correlation

Logs should preserve evidence needed for diagnosis without becoming an
uncontrolled copy of application data or credentials.

## Structured Logging Baseline

Production applications SHOULD emit structured events, preferably as JSON to
standard output in containerized runtimes:

```json
{
  "timestamp": "2026-05-24T13:42:08Z",
  "severity": "error",
  "event": "checkout_failed",
  "service.name": "api",
  "service.namespace": "orders",
  "service.version": "1.8.2",
  "deployment.environment.name": "production",
  "request_id": "req-8fe1c4",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "error_type": "payment_provider_timeout"
}
```

Required fields depend on the system, but production event logs SHOULD expose:

- timestamp and severity;
- stable service and environment identity;
- release/version where failures may be deployment-related;
- concise event or error classification;
- correlation identifier where requests or jobs span components.

Use the identifier conventions in
[Telemetry and Operations](../naming/telemetry-and-operations.md).
Timestamps SHOULD follow
[Architecture: Time and Timezone Standards](../architecture/time-and-timezone-standards.md):
use RFC 3339 UTC values for operational events unless a different timezone is
explicitly required and named.

## Levels and Events

| Level | Use when | Avoid |
| --- | --- | --- |
| `debug` | Temporary or sampled diagnostic detail | Default high-volume production logging |
| `info` | Expected lifecycle or material business/operation event | One line for every irrelevant internal step |
| `warn` | Recoverable abnormal condition worth investigation | Treating normal validation failures as incidents |
| `error` | Operation failed or user-impacting processing was not completed | Repeated stack traces without classification |

Prefer stable event names:

```text
Good                                      Avoid
event=registry_auth_failed               message="Something went wrong!!!!"
event=payment_provider_timeout           event=error2
```

## Correlation IDs and Trace Context

Use:

- `request_id` for an application-visible request identifier useful in
  support or HTTP response diagnostics;
- `trace_id` and `span_id` for distributed trace correlation where tracing is
  enabled;
- `job_id` or equivalent for asynchronous workflow diagnosis when safe to log.

Propagate identifiers across internal request or job boundaries. Do not use
request IDs, trace IDs or user IDs as Prometheus labels or Loki indexed labels;
they are high-cardinality data intended for detail lookup.

```text
Good                                      Avoid
Find log by request_id field             Label every Loki stream by request_id
Link log entry to trace_id               Aggregate a metric by trace_id
```

## Sensitive Data and Security

Never log:

- passwords, API tokens, authorization/cookie headers or private keys;
- complete connection strings containing credentials;
- reset/invite links or session material;
- full payment or sensitive personal payloads;
- raw secrets received from CI/CD or infrastructure providers.

Prefer safe diagnostic context:

```json
{
  "event": "database_auth_failed",
  "credential_id": "orders-api-db-password-prod",
  "error_code": "invalid_credentials"
}
```

Security redaction is an application and pipeline responsibility. Access
control to Loki or another log store is not permission to ingest secrets.

## Centralized Logging and Loki

Loki is a practical log backend when the operating model favors low-cardinality
stream labels with query-time search through log content or structured
metadata.

Recommended stream labels:

```text
service_name="orders-api"
environment="prod"
cluster="platform-prod"
namespace="orders"
```

These backend labels are a controlled query mapping of canonical telemetry
identity. Where OpenTelemetry resource fields are retained directly, prefer
`service.name` and `deployment.environment.name` consistently instead of
inventing different service identities in each backend.

Do not index values that grow per request, container instance or user:

```text
Avoid as labels
request_id, trace_id, user_id, raw_url, container_id, timestamp
```

Where supported and justified, use structured metadata for queryable
high-cardinality fields such as trace or ephemeral instance identity instead
of indexed Loki labels.

## Aggregation and Retention

| Log class | Retention consideration |
| --- | --- |
| Debug/high-volume routine events | Short retention or disabled by default in production |
| Application errors and operational events | Retain long enough for incident and release analysis |
| Access/security-relevant events | Retain according to investigation need and sensitivity |
| Audit/change evidence | Protect access and retention according to impact |

Retention is a cost and security decision. Longer storage may support
investigation but increases storage expense and the duration of sensitive data
exposure.
