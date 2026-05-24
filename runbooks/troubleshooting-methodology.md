# Troubleshooting Methodology

Troubleshooting is a controlled reduction of uncertainty. The goal is not to
try commands until the symptom disappears; it is to identify the affected
boundary and select a safe corrective action.

## Standard Workflow

1. State the symptom in user or operator terms.
2. Confirm whether it is current, historical, intermittent or already
   recovered.
3. Establish scope: environment, service, route, region/cluster, users and
   time window.
4. Identify recent change: deploy, config, secret rotation, infrastructure
   action or provider event.
5. Inspect observable behavior from outside in.
6. Test the most likely failure hypotheses with read-only evidence.
7. Choose mitigation or recovery with expected result and rollback risk.
8. Execute once, validate outcome and record evidence.

## Outside-In Diagnostic Layers

```text
User symptom / SLI / alert
  -> DNS and TLS
  -> public ingress / reverse proxy / load balancer
  -> service readiness and runtime instances
  -> container/Pod/task logs and version
  -> node CPU/memory/disk/network
  -> internal discovery and dependencies
  -> database/storage/queue
  -> control plane, credential or provider layer
```

Do not begin at the lowest layer simply because it has familiar commands.

## Hypothesis Record

For material incidents, keep investigation disciplined:

```text
Observation: 5xx began within two minutes of production rollout.
Hypothesis: new API image has incompatible database query.
Evidence to collect: running digest, error logs, dependency latency, migration record.
Action if confirmed: rollback compatible prior digest.
Validation: public checkout smoke plus error-rate recovery.
```

## Monitoring-Driven Investigation

| Signal | Question |
| --- | --- |
| External check or SLI | Are users currently affected? |
| Error/latency dashboard | Which service, route or period is affected? |
| Deployment annotation/version | Did change correlate with behavior? |
| Correlated logs/traces | Which failing operation or dependency explains it? |
| Infrastructure metrics | Is capacity, node, storage or network the cause? |
| Platform/control-plane status | Is recovery or scheduling itself impaired? |

See [Observability Diagnostics](../observability/diagnostics-and-incident-workflows.md).

## Resource Exhaustion Diagnostics

### CPU

Symptoms:

- sustained latency increase with high CPU saturation;
- throttling or task scheduling constraints;
- workers falling behind.

Check:

```bash
docker stats --no-stream
docker service ps <stack_service>
kubectl top pods -n <namespace>
kubectl top nodes
```

Interpret before acting: high CPU may be normal load, a bad release, retry
storm or slow dependency amplification. Scaling without removing a retry storm
may increase damage.

### Memory

Symptoms:

- restarts or OOM kill events;
- sudden unavailability during load;
- host pressure affecting several services.

Check runtime events/logs and current allocation; compare to deployment
changes and observed traffic. Recovery may require rollback, controlled
resource adjustment or workload isolation, not repeated restart.

### Disk and Storage

Symptoms:

- database write failures;
- log or telemetry ingestion failure;
- container/node disruption;
- failed backups.

Check:

```bash
df -h
df -i
docker system df
```

Do not delete unknown volumes, logs or database files during active diagnosis.
Identify retention, backup and ownership before cleanup.

## Dependency Verification

For each dependency, validate at the appropriate boundary:

| Dependency | Checks |
| --- | --- |
| Database | reachability, connection failure signals, query latency, storage health and migration state |
| Queue/worker | queue depth, failed jobs, consumer health and retry/dead-letter behavior |
| External provider | timeout/error classification, provider status and safe degraded behavior |
| Registry | image availability/pull authentication and expected digest |
| Secret store | retrieval/authorization status without printing values |

## Stop Conditions

Stop independent troubleshooting and escalate before:

- destructive database or storage action;
- forced cluster reconstruction or control-plane recovery;
- revoking authority without knowing affected recovery path, unless active
  exposure requires immediate containment;
- modifying multiple independent variables without evidence;
- continuing past operator fatigue or lack of required access.
