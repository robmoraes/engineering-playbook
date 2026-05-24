# Diagnostics and Incident Workflows

Observability proves its value during change, degradation and incidents.
Diagnostics should direct investigation from symptom to cause without random
production mutation.

## Standard Investigation Flow

1. Confirm the reported symptom from a user-relevant route or SLI.
2. Establish scope: service, environment, region/cluster and time window.
3. Check recent deployments, configuration or infrastructure changes.
4. Inspect RED behavior: rate, errors and latency.
5. Pivot using request/trace correlation into representative failures.
6. Inspect dependencies and USE/resource signals for likely causes.
7. Apply a documented recovery or mitigation action.
8. Verify user-facing behavior and retain incident evidence.

```text
Good                                      Avoid
Confirm outage through external route    Restart services on first error log
Compare errors with deployed version     Diagnose from one uncorrelated screenshot
Preserve evidence before mutation        Delete/recreate before collecting state
```

## Example: API Errors After Deployment

```text
Symptom: Orders API error-rate page fires after production rollout.

Investigation:
1. Open alert-linked service overview dashboard.
2. Confirm elevated 5xx on external route and identify start time.
3. Compare deployment annotation and service.version.
4. Query logs for event/error_type in affected version.
5. Inspect traces for downstream or database timeout concentration.
6. Check runtime readiness, resource saturation and dependency availability.
7. Roll back verified artifact if regression and data compatibility permit.
8. Verify SLI recovery; capture root cause and telemetry gaps.
```

## Example: Latency Without Errors

```text
Symptom: Requests succeed but p99 latency breaches objective.

Investigation:
1. Confirm rate and p50/p95/p99 behavior, not averages only.
2. Segment by bounded route and release.
3. Use traces or dependency metrics to locate delayed boundary.
4. Check node/container saturation and storage/network conditions.
5. Confirm whether load increase, provider latency or deploy caused shift.
6. Mitigate through safe scaling, rollback or dependency action.
```

## Example: Missing Telemetry

Loss of visibility is itself an operational issue:

```text
Symptoms:
- Prometheus target down or stale metrics
- Collector export failures
- Loki ingestion/query failure
- Dashboard empty while service traffic continues

Response:
- confirm service behavior through independent blackbox checks;
- inspect collector/storage/platform health;
- avoid concluding that absent errors mean healthy service;
- restore visibility and identify any diagnostic gap during the interval.
```

## Runbook Integration

Every page-level alert SHOULD link to a runbook containing:

```text
Alert/symptom:
Service and owner:
User impact:
Dashboard and direct query:
Related logs/traces:
Common causes:
Safe initial checks:
Mitigation/rollback/recovery:
Escalation:
Post-recovery verification:
```

Keep runbooks aligned with actual dashboard names, metric queries and access
routes. A runbook that points to retired telemetry adds delay during an
incident.

## Failure Analysis and Improvement

For material incidents or repeated alert noise, review:

- whether the user symptom was detected quickly;
- whether alert routing and severity were correct;
- whether telemetry identified the cause or produced ambiguity;
- missing correlation, labels, log events or dashboards;
- excessive noise, cardinality or retention cost;
- runbook effectiveness and recovery verification.

Follow-up work should prioritize telemetry that changes future diagnosis or
reliability decisions over broad instrumentation added without a use case.
