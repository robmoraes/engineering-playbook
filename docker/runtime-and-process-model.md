# Runtime and Process Model

A runtime image must behave predictably during startup, health checking,
termination, debugging and replacement. These properties matter more in
production than squeezing the final few megabytes from an image.

## Main Process

A container SHOULD have one primary workload process whose lifecycle determines
whether the container is running.

Use exec-form process commands:

```dockerfile
CMD ["node", "dist/server.js"]
```

```text
Good                                      Avoid
Main server as PID 1 with signal support Shell wrapper that loses SIGTERM
Separate worker service/container        Web server, scheduler and database managed by ad hoc script
```

A minimal init process MAY be used when the application cannot correctly reap
child processes or handle signal behavior itself.

## `CMD` Versus `ENTRYPOINT`

| Instruction | Use |
| --- | --- |
| `ENTRYPOINT` | Stable executable the container always represents |
| `CMD` | Default command or arguments that operators may reasonably override |

Application default:

```dockerfile
CMD ["node", "dist/server.js"]
```

Tool-style image:

```dockerfile
ENTRYPOINT ["terraform"]
CMD ["--help"]
```

Avoid entrypoint scripts that mutate the image filesystem unpredictably,
silently run schema changes or hide failures before launching the service.

## Entrypoint Scripts

Use a script only when startup requires small deterministic preparation such as
rendering non-secret configuration or fixing a known runtime path ownership
that cannot be handled at build time.

Rules:

- fail immediately on error;
- avoid logging secret values;
- use `exec` to replace the script with the main process;
- keep database migrations as an explicit deployment step unless their risk
  and concurrency behavior are deliberately controlled.

```sh
#!/bin/sh
set -eu

echo "Starting orders-api"
exec "$@"
```

## Environment Variables and Secrets

Use environment variables for non-secret deploy-varying configuration:

```text
APP_ENV=prod
LOG_LEVEL=info
HTTP_PORT=3000
```

For secrets:

- prefer runtime secret files or platform secret injection;
- read only the secrets required by the process;
- never copy `.env.production` into an image;
- avoid emitting configuration dumps to logs.

Swarm secret consumption example:

```text
/run/secrets/orders-api-db-password-prod
```

The application may support a `DATABASE_PASSWORD_FILE` input rather than
requiring a plaintext secret in its environment.

## Non-Root Runtime and Filesystem Permissions

Containers SHOULD execute as an unprivileged user. Build the filesystem so the
runtime user can access only required locations:

```dockerfile
WORKDIR /app
COPY --chown=node:node dist/ ./dist/
USER node
CMD ["node", "dist/server.js"]
```

Guidelines:

- write only to required runtime directories such as `/tmp` or an explicit
  application data mount;
- do not solve permission problems with broad `chmod 777`;
- do not require root to bind high ports when a reverse proxy can map external
  traffic to an unprivileged internal port;
- test runtime execution under the configured user.

Optional hardening for compatible production workloads:

- read-only root filesystem;
- dropped Linux capabilities;
- no privilege escalation;
- explicit writable temporary mounts.

## Healthchecks

Healthchecks answer operational questions and should not disclose internal
secrets or require expensive downstream operations.

Dockerfile example:

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://127.0.0.1:3000/health || exit 1
```

Compose example:

```yaml
healthcheck:
  test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://127.0.0.1:3000/health"]
  interval: 30s
  timeout: 3s
  retries: 3
  start_period: 20s
```

Tradeoffs:

| Check | Good use | Risk |
| --- | --- | --- |
| Liveness-style process check | Restart truly stuck process | Restart storms when dependency is degraded |
| Readiness/service check | Keep unavailable instance out of traffic | False failure if it tests non-critical dependency |
| Deep dependency check | Diagnostic endpoint or deployment smoke test | Too expensive or fragile for frequent local healthcheck |

Docker health status alone does not prove public traffic or critical user
behavior works. Deployment verification should also exercise the routed
service path.

## Logging

Application containers SHOULD write operational logs to `stdout` and `stderr`
in a structured, parseable form. The platform owns collection, transport and
retention.

```json
{"level":"info","event":"server_started","service":"orders-api","port":3000}
{"level":"error","event":"db_connection_failed","service":"orders-api","error_code":"timeout"}
```

Avoid:

- log files inside the container as the only record;
- credentials, headers or secret values in log output;
- multiline unstructured output where structured data is practical;
- relying on container filesystem logs for retention.

## Resource Constraints and Shutdown

Set realistic CPU/memory constraints or reservations in production platforms
after observing workload behavior. Unbounded containers can cause node-level
failure; limits set without measurement can create avoidable restarts.

Services MUST handle termination gracefully:

- stop accepting new work when shutting down where relevant;
- allow in-flight work a bounded completion period;
- exit on `SIGTERM`;
- ensure job processing is idempotent or recoverable if interrupted.
