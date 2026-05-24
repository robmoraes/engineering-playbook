# Deployments and Promotion

Deployment automation changes a running environment. Its standard is therefore
higher than build automation: it must select a trusted artifact, use scoped
authority, verify result and support recovery.

## Promotion Model

Promote the same artifact across environments:

```text
sha256:trusted-digest
  -> deploy stg with stg configuration/secrets
  -> verify
  -> approve where required
  -> deploy prod with prod configuration/secrets
  -> verify and observe
```

Artifacts are shared; configuration, credentials and data boundaries are not.

```text
Good                                      Avoid
Same digest with separate env config     Rebuild image with production secrets
Prod deploy selects tested digest        Deploy whatever `latest` points to
```

## Approval Policy

| Context | Production approval |
| --- | --- |
| Personal/lab without live impact | Optional |
| Public portfolio service with users or credentials | Explicit manual trigger or protected environment recommended |
| Production workload | Protected environment and/or approval appropriate to impact |
| High-risk or enterprise workload | Separation of duties, auditable approval and controlled promotion policy where justified |

Approval is useful only if the reviewer can see what is being approved:
revision, image digest, test/scan outcome, migration impact and rollback
candidate.

## Deployment Safety Checks

Before deploying production:

- selected artifact exists and is immutable;
- required validation and scan policy has passed or a documented exception
  exists;
- configuration and secrets target the correct environment;
- database/schema migrations are compatible or have a recovery plan;
- current known-good version is recorded for rollback;
- change timing is appropriate for user impact and operator availability.

## Verification

Deployment success is not "command exited zero." Verify the running behavior.

Minimum verification for a service:

```text
- orchestrator reports intended image digest running;
- health endpoint passes through intended public/private path;
- smoke operation exercises critical behavior safely;
- logs and metrics show no immediate regression;
- dependent migrations or async workers are healthy where relevant.
```

Example shell-oriented verification contract:

```bash
curl --fail --silent --show-error https://api.example.com/health
```

For a more material API, use an authenticated or synthetic transaction that
confirms a critical path without modifying real customer data unexpectedly.

```text
Good                                      Avoid
Verify public route and running digest   Treat container start as user success
Check queue workers after migration      Ignore background processing until alerts
```

## Rollback and Recovery

Rollback restores the prior application artifact when the data/configuration
remains compatible. Recovery addresses situations where rollback alone is
insufficient, such as destructive migration, data corruption or credential
failure.

Every production deployment SHOULD record:

- deployed digest/version;
- prior known-good digest/version;
- configuration or migration compatibility notes;
- rollback command or workflow;
- recovery escalation when rollback is unsafe.

```text
Failure                                 Response
Application regression, compatible DB  Roll back to prior verified digest
Failed non-destructive migration       Fix-forward or roll back per migration plan
Destructive incompatible migration     Restore/recovery plan; image rollback may fail
Secret misconfiguration                Correct secret/config and redeploy safely
```

## Docker Swarm Deployment Pattern

For Swarm, use a versioned stack definition and deploy immutable image
references:

```yaml
services:
  api:
    image: ghcr.io/acme/orders-api@sha256:<digest>
    deploy:
      update_config:
        order: start-first
        failure_action: rollback
      rollback_config:
        order: stop-first
```

Practical pipeline:

```text
publish digest -> update deployment input -> docker stack deploy
               -> inspect service tasks/update status -> health verification
```

Operational considerations:

- `start-first` can reduce interruption but temporarily consumes extra capacity
  and may require both versions to run safely together;
- automatic task rollback does not undo database migrations;
- Swarm manager access is privileged and should be constrained as documented
  in the security standards.

## Kubernetes Deployment Considerations

For Kubernetes-based delivery:

- deploy immutable image digests;
- use readiness probes and rollout status for initial validation;
- configure rolling strategy appropriate to capacity and compatibility;
- keep configuration and secrets environment-scoped;
- define rollback or forward-fix behavior for schema changes;
- treat cluster credentials and namespace permissions as deployment authority.

A healthy Kubernetes rollout reports platform state; it does not replace
service-level smoke verification or telemetry review.

## GitOps Concepts

GitOps is appropriate when desired runtime state is declared, versioned,
automatically reconciled and continuously observed by an agent or platform.

```text
application build repository -> publishes image digest
environment configuration repository -> references approved digest
reconciler -> applies desired state and reports drift/health
```

Benefits:

- auditable deployment intent and drift correction;
- pull-based runtime credentials can reduce CI access to clusters;
- rollback may be represented as a configuration revert.

Costs:

- reconciler operation, repository boundaries and promotion mechanics;
- secret/configuration handling and reconciliation troubleshooting;
- need to distinguish application release from environment change.

A workflow that runs `kubectl apply` or `docker stack deploy` after a Git push
is automated deployment, not automatically GitOps. Adopt GitOps when
reconciliation and desired-state operation solve a real platform requirement.
