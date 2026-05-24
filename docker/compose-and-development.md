# Compose and Local Development

Docker Compose is an effective way to express local multi-container
dependencies and small deployments. Its value is consistency, not forcing
production topology to be identical to a laptop.

## Compose File Conventions

Prefer a clear base file plus intentional development overrides:

```text
compose.yaml              shared service model
compose.override.yaml     local developer defaults, when appropriate
compose.prod.yaml         production-specific declarations only when Compose-based production is deliberate
.env.example              documented non-secret keys
```

Rules:

- use explicit service, network and volume names consistent with naming rules;
- define images for deployment-oriented files; use `build` where local build
  is intentional;
- avoid plaintext secrets in versioned Compose files;
- keep public port mappings limited to services developers must reach;
- add healthchecks for dependencies whose startup order affects usability.

## Development Example

```yaml
services:
  api:
    build:
      context: .
      target: runtime
    environment:
      APP_ENV: dev
      DATABASE_URL: postgres://orders:orders@db:5432/orders
    ports:
      - "3000:3000"
    depends_on:
      db:
        condition: service_healthy
    networks: [app]

  db:
    image: postgres:17-alpine
    environment:
      POSTGRES_DB: orders
      POSTGRES_USER: orders
      POSTGRES_PASSWORD: orders
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U orders -d orders"]
      interval: 5s
      timeout: 3s
      retries: 10
    networks: [app]

networks:
  app:

volumes:
  db_data:
```

Static local credentials in a development-only Compose example are acceptable
only when they cannot access shared or production systems. Never copy this
pattern into production.

## Source Mounts and Watch Workflows

For fast development feedback, choose deliberately between:

| Approach | Use when | Tradeoff |
| --- | --- | --- |
| Bind mount source | Runtime executes source directly and host/container permission behavior is understood | May mask image contents and differ from production |
| Compose Watch sync | Controlled files can update without full rebuild | Requires current Compose and clear synchronization rules |
| Rebuild container on change | Compiled/native dependencies or production-like verification matter | Slower feedback |

The production image must still be built and tested without development mounts.
A container that works only because a source mount overlays missing files is
not deployable.

## One-Off and Temporary Containers

Use ephemeral Compose runs for explicit development tasks:

```bash
docker build --target test -t orders-api:test .
docker compose run --rm api node dist/migrate.js
```

The `test` build target should include test dependencies and test execution;
the normal runtime image remains free of that tooling. For production
migrations, run through a controlled deployment procedure, not an undocumented
local command against production credentials.

Temporary containers SHOULD:

- be removable with `--rm` when their output is external or disposable;
- avoid privileged mounts unless the task explicitly requires them;
- use the same trusted image or toolchain expected by the project.

## Debugging Locally

Useful commands:

```bash
docker compose ps
docker compose logs --tail=100 api
docker compose exec api sh
docker compose config
docker inspect <container>
```

Debug shells and additional tools are acceptable in local/development targets.
Do not inflate production images only to preserve an interactive shell if a
separate debug image or platform debugging method is adequate.

## Compose in Production

Compose-based production can be legitimate for a carefully operated
single-host service or low-complexity deployment. It must still provide:

- immutable image selection;
- externalized secrets;
- durable backup strategy for state;
- restart/recovery behavior;
- monitoring and logs;
- controlled deployment and rollback.

When multi-node scheduling, rolling update orchestration, workload policy or
availability requirements exceed that model, move to a suitable platform
rather than stretching local-development conventions into production.
