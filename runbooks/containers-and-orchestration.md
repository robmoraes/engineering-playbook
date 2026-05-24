# Containers and Orchestration

Use this runbook when workload failure appears at container, node or
orchestrator level. Diagnose user impact and deployment state before
restarting or rescheduling processes.

## Container Troubleshooting

### Symptoms

- service unhealthy or repeatedly restarting;
- application logs unavailable or show startup failure;
- resource limit or filesystem permission issue;
- image/configuration mismatch.

### Initial Assessment

```bash
docker ps
docker inspect <container>
docker logs --tail 100 <container>
docker stats --no-stream
```

Check:

- running image reference/version;
- exit state and health status;
- mounted volumes/secrets by identifier only;
- resource pressure;
- network attachment and exposed ports.

Avoid mutating the live container to make it work temporarily. Diagnose,
correct the defined artifact/configuration and redeploy a recorded version.

## Docker Swarm Service Troubleshooting

### Scope

Swarm commands that manage services or nodes require manager authority. Begin
with status collection and do not remove nodes or recreate the swarm during
routine service diagnosis.

### Procedure

1. Confirm application symptom through monitoring or external route.
2. Inspect nodes and service task distribution:

   ```bash
   docker node ls
   docker service ls
   docker service ps <stack_service>
   ```

3. Inspect service configuration and recent task failure:

   ```bash
   docker service inspect <stack_service> --pretty
   docker service logs --tail 100 <stack_service>
   ```

4. Determine likely boundary:

   | Observation | Investigate next |
   | --- | --- |
   | New tasks reject image pull | Registry credentials, image digest/tag and node reachability |
   | Tasks rejected for placement/resources | Node labels, constraints and available capacity |
   | Tasks start but routed service fails | Application logs, overlay/ingress and dependencies |
   | Manager commands fail or nodes unavailable | Manager quorum/control-plane recovery procedure |
   | Stateful task unavailable on another node | Volume/storage placement and recovery design |

5. Apply the narrow approved recovery: artifact rollback, corrected
   configuration, restored node capacity or control-plane escalation.
6. Verify routed service and task convergence.

### Swarm Quorum or Manager Failure

Manager quorum loss is not a routine application restart. Existing workloads
may continue while management operations fail.

- preserve manager/node status and known failure event;
- stop unrelated deployment attempts;
- engage infrastructure owner;
- follow backed-up Swarm recovery procedure appropriate to the topology;
- verify services and control plane after recovery.

See [Infrastructure: Clusters and Orchestration](../infrastructure/clusters-and-orchestration.md).

## Kubernetes Troubleshooting Considerations

For a Kubernetes-operated workload, use an outside-in progression:

```bash
kubectl get deployment,pods,service -n <namespace>
kubectl rollout status deployment/<service> -n <namespace>
kubectl describe pod <pod> -n <namespace>
kubectl logs <pod> -n <namespace> --tail=100
kubectl get events -n <namespace> --sort-by=.metadata.creationTimestamp
kubectl get nodes
```

| Observation | Investigate |
| --- | --- |
| Pod cannot start | image pull, secrets/config, scheduling, volumes and security settings |
| Pod ready but Service fails | endpoints, service selector, DNS/network policy and ingress |
| Node `NotReady` | node events, capacity/runtime/network and platform owner |
| Rollout regression | revision compatibility and controlled rollback |

Use temporary debug containers or `kubectl exec` only under appropriate
authority, with awareness that production diagnostics can expose sensitive
network or configuration data.

## Resource Exhaustion Recovery

If container or node pressure is confirmed:

1. identify which workload/resource is saturated and whether it caused user
   impact;
2. correlate with release, load or dependency behavior;
3. select rollback, controlled scale, resource adjustment or capacity repair;
4. avoid broad cleanup or restart that removes evidence;
5. verify both service recovery and resource stabilization.

```text
Good                                      Avoid
Rollback memory-leaking new release      Restart all tasks repeatedly
Scale validated stateless service        Delete volumes to free unknown disk usage
```
