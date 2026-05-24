# Deployment Rollback and Service Recovery

Use this runbook when a service degrades after a deployment or when a known
good artifact can restore behavior. Rollback reverses application release
state; it does not automatically reverse data migrations or infrastructure
changes.

## Summary

```text
Goal: restore a failing service to a verified known-good artifact safely.
Applies to: deployment-related failure in staging or production.
Owner: service delivery/operations owner.
Required access: read access to deployment evidence and scoped deploy/rollback authority.
```

## Symptoms

- errors or latency begin after a release;
- readiness/health failures during rollout;
- new tasks/Pods cannot become healthy;
- background workers fail after new artifact promotion;
- monitoring identifies behavior correlated with `service.version` or image
  digest.

## Safety Checks

Before rollback:

- confirm target environment and affected service;
- record current and prior known-good image digest/version;
- identify database schema, configuration or secret changes in the release;
- confirm prior artifact is compatible with current state;
- capture alert, logs and rollout status;
- identify validation steps after rollback.

```text
Safe rollback                              Escalate/recovery analysis required
Code regression with compatible DB         Destructive/incompatible migration applied
Bad runtime config with prior config known Data corruption or lost state
Readiness regression in new image          Secret compromise or unknown artifact trust
```

## Diagnostics

Read-only examples:

```bash
curl --fail --silent --show-error https://api.example.com/health
docker service ls
docker service ps <stack_service>
docker service logs --tail 100 <stack_service>
kubectl rollout status deployment/<service> -n <namespace>
kubectl describe deployment/<service> -n <namespace>
kubectl logs deployment/<service> -n <namespace> --tail=100
```

Use only the commands applicable to the deployed runtime and authorized
context. Avoid printing configuration or secret contents.

## Docker Swarm Rollback

Docker Swarm service changes are performed from a manager and require
privileged authority.

1. Confirm failing service and tasks:

   ```bash
   docker service ps <stack_service>
   docker service inspect <stack_service> --pretty
   ```

2. Confirm rollback is compatible with data and configuration changes.
3. Execute the approved rollback:

   ```bash
   docker service rollback <stack_service>
   ```

4. Watch tasks reach expected state and inspect failures:

   ```bash
   docker service ps <stack_service>
   docker service logs --tail 100 <stack_service>
   ```

5. Perform external health/smoke validation and observe error/latency metrics.

For stack-wide deployment state driven by versioned configuration, prefer
redeploying the approved prior configuration/digest through the controlled
delivery path instead of accumulating manual drift.

## Kubernetes Rollback Consideration

Where Kubernetes is the selected runtime:

```bash
kubectl rollout history deployment/<service> -n <namespace>
kubectl rollout status deployment/<service> -n <namespace>
kubectl rollout undo deployment/<service> -n <namespace>
kubectl rollout status deployment/<service> -n <namespace>
```

`kubectl rollout undo` changes workload revision; it does not restore database
content, external configuration or secret history. Verify those compatibility
boundaries before invoking it in production.

## Configuration or Secret Correction

If artifact code is healthy but runtime configuration is wrong:

1. determine the incorrect configuration/secret reference without exposing
   its value;
2. restore the intended environment-scoped reference through controlled
   configuration/secrets management;
3. redeploy or reload the service safely;
4. verify authentication/dependency behavior and user path;
5. record whether the failed release procedure needs a guardrail.

For suspected credential exposure, use
[Security and Delivery Recovery](./security-and-delivery-recovery.md) rather
than treating it as configuration rollback only.

## Validation

- expected image digest/version is running;
- service readiness is healthy;
- external health and a safe critical-path smoke test pass;
- error rate and latency recover in telemetry;
- asynchronous workers/queues and dependencies are healthy where relevant;
- no new permission, secret or state failures appear.

## Follow-Up

- preserve incident/deployment timeline and rollback reason;
- block or correct failed artifact/configuration;
- add or improve pre-deployment verification where it would have prevented
  recurrence;
- update this runbook when actual recovery differed from documented behavior.
