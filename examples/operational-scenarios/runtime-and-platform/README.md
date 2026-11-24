# Runtime and Platform Scenarios

Use these exercises to investigate workload health, filesystem access,
scheduling, capacity and shared platform dependencies.

Each scenario must distinguish a read-only diagnosis from an action requiring
runtime or cluster authority.

| Symptom | Exercise |
| --- | --- |
| A service passes its health check but fails to create a file | [Trace a failed write to the service's Linux permissions](./service-write-permission/README.md) |
