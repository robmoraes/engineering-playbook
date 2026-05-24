# Principles and Signal Model

Observability should help answer: what is failing, who is affected, what
changed, why it is happening and which recovery action is safe.

## Monitoring Versus Observability

| Practice | Primary purpose |
| --- | --- |
| Monitoring | Continuously evaluate known conditions, health and objectives |
| Observability | Use emitted telemetry and context to investigate system behavior, including unexpected failure |

Monitoring is part of observability. A production platform still needs
explicit alerts and health checks; it cannot rely on an operator manually
exploring traces after users report an outage.

## Signal Model

| Signal | Strong use | Poor substitute for |
| --- | --- | --- |
| Metrics | Trends, rates, SLO evaluation, saturation and alert conditions | Detailed per-request explanation |
| Logs | Discrete events, errors, change evidence and detailed diagnosis | Cheap unbounded analytics or SLO calculation by default |
| Traces | Request path, cross-service latency and partial failure | Complete application event history |
| Events/deploy evidence | Change correlation and runtime lifecycle | User-visible service measurement |
| Synthetic/blackbox checks | External reachability and critical route behavior | Internal dependency diagnosis |

Start with logs, health and a small number of useful metrics. Add tracing or
more complex pipelines when network boundaries, latency diagnosis or support
load justify the operational cost.

## Visibility Principles

### Begin with User Symptoms

For user-facing services, visibility begins with availability, errors and
latency through the route users depend on. Internal CPU or restart counts may
explain symptoms; they should not replace user-oriented signals.

```text
Good                                      Avoid
Alert on elevated API failure rate       Page because one replica restarted
Dashboard public latency and errors      Dashboard only host CPU graphs
```

### Preserve Operational Context

An operator must be able to pivot across signals using stable context:

```text
service.name=api
service.namespace=orders
deployment.environment.name=production
service.version=1.8.2
trace_id=<execution-context>
```

Do not hide release, environment or service identity in dashboard titles only.
It belongs in the telemetry model.

### Use Whitebox and Blackbox Together

| View | Reveals | Example |
| --- | --- | --- |
| Blackbox | Externally visible behavior | HTTPS probe against `api.example.com/health` |
| Whitebox | Internal reason or warning | Database pool saturation or queue backlog |

Blackbox monitoring catches broken user paths that internal checks miss.
Whitebox telemetry makes diagnosis and capacity planning possible.

### Prefer Actionable Data

Each signal should serve at least one purpose:

- trigger a defined response;
- confirm user impact;
- isolate a dependency or failure domain;
- verify a deployment or architecture decision;
- support capacity, retention or cost planning.

Collecting everything indefinitely increases exposure and cost while making
urgent investigation harder.

## Telemetry Boundaries

| Boundary | Expected visibility |
| --- | --- |
| Application | request outcomes, latency, domain-critical failures, background work |
| Runtime/container | process health, restarts, CPU/memory and image/version identity |
| Infrastructure | nodes, ingress, network, storage, control plane, backups and changes |
| Delivery | deployed artifact, rollout outcome, verification and rollback evidence |
| Security | authentication/access outcomes without secret material |

The owner of a service remains responsible for useful application telemetry.
A platform team can provide collection and dashboards, but cannot infer every
business-critical failure from container metrics.

## Maturity by Context

| Context | Reasonable baseline | Add when needed |
| --- | --- | --- |
| Lab | Local logs and a health check | Metrics/dashboard for learning |
| Portfolio deployment | Structured centralized logs, uptime/health and deploy visibility | Public-safe dashboard evidence |
| Small production | Central logs, Prometheus-style metrics, alerts, runbooks and infrastructure visibility | Traces for distributed diagnosis |
| High scale/platform | SLOs, governed telemetry pipeline, reusable dashboards/rules, sampling and cost controls | Dedicated platform operation and long-term analysis tiers |
