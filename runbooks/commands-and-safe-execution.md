# Commands and Safe Execution

Commands in runbooks are examples that must be adapted to the known
environment, ownership boundary and access policy. Begin with read-only
inspection; mark mutating actions explicitly in incident notes.

## Safety Rules

- Confirm environment, service and authority before any mutating command.
- Prefer scoped accounts and platform APIs over unrestricted root/admin shell.
- Avoid commands that print secret values or unrestricted configuration.
- Record production changes, expected outcome and validation.
- Stop before deletion, restore, force removal or cluster reconstruction unless
  the documented recovery owner has approved the action.

## HTTP, DNS and TLS

Read-only diagnostics:

```bash
curl --fail --silent --show-error https://api.example.com/health
curl --verbose https://api.example.com/health
dig +short api.example.com
openssl s_client -connect api.example.com:443 -servername api.example.com </dev/null
```

Use to distinguish routing, DNS, certificate and application failures. Avoid
including authentication tokens in copied command output.

## Linux Host Capacity

Read-only diagnostics:

```bash
uptime
free -h
df -h
df -i
ss -lnt
journalctl --since "30 minutes ago" --no-pager
```

System logs may contain sensitive material. Limit retrieval to the relevant
time/service and retain them in an access-controlled incident location.

## Docker Container Diagnostics

```bash
docker ps
docker inspect <container>
docker logs --tail 100 <container>
docker stats --no-stream
docker system df
```

Avoid `docker exec` modifications as recovery. When an interactive diagnostic
session is necessary, record its purpose and do not expose mounted secrets.

## Docker Swarm Diagnostics

Read-only:

```bash
docker node ls
docker service ls
docker service ps <stack_service>
docker service inspect <stack_service> --pretty
docker service logs --tail 100 <stack_service>
docker stack services <stack>
```

Mutating, use only after approval and compatibility review:

```bash
docker service rollback <stack_service>
docker service update --image <image>@sha256:<digest> <stack_service>
docker stack deploy -c <approved-stack-file> <stack>
```

These operations require Swarm manager authority. Do not force-remove a
manager or rebuild a swarm as a generic service troubleshooting step.

## Kubernetes Diagnostics

Read-only:

```bash
kubectl get deployment,pods,service -n <namespace>
kubectl describe deployment/<service> -n <namespace>
kubectl describe pod <pod> -n <namespace>
kubectl logs <pod> -n <namespace> --tail=100
kubectl get events -n <namespace> --sort-by=.metadata.creationTimestamp
kubectl get nodes
kubectl rollout history deployment/<service> -n <namespace>
kubectl rollout status deployment/<service> -n <namespace>
```

Mutating, use only after approval and compatibility review:

```bash
kubectl rollout undo deployment/<service> -n <namespace>
kubectl cordon <node>
kubectl drain <node> --ignore-daemonsets
```

Drain and rollback change production scheduling/runtime state. Validate
capacity, stateful volumes and application compatibility first.

## Observability Queries

Examples of investigation intent:

```promql
sum(rate(orders_http_requests_total{environment="prod",status_code=~"5.."}[5m]))
/
sum(rate(orders_http_requests_total{environment="prod"}[5m]))
```

```logql
{service_name="orders-api", environment="prod"} |= "checkout_failed"
```

Correlate query time range with deployment and timeline. Do not copy
unredacted log payloads into public notes.

## Command Recording

For a production-changing action, record:

```text
Time:
Operator:
Environment/resource:
Command or workflow invoked:
Reason/evidence:
Expected outcome:
Actual outcome:
Validation:
Rollback/escalation:
```
