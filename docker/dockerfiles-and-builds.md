# Dockerfiles and Builds

A production Dockerfile should be predictable to review, efficient enough to
build repeatedly and narrow enough that its runtime image contains only what
the application needs to execute.

## Dockerfile Conventions

- Use a current Dockerfile syntax directive when BuildKit features are needed.
- Name meaningful build stages: `dependencies`, `build`, `test`, `runtime`,
  `debug`.
- Set an explicit `WORKDIR`.
- Copy dependency manifests before application source when this improves cache
  reuse without weakening correctness.
- Use `COPY` for local files unless `ADD` behavior is intentionally needed.
- Use exec-form `CMD` or `ENTRYPOINT` for the main process.
- Define an explicit non-root runtime `USER` where supported.
- Keep comments for constraints and non-obvious decisions, not narration.

## Reference Application Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

FROM node:22-alpine AS dependencies
WORKDIR /src
COPY package*.json ./
RUN npm ci

FROM dependencies AS build
COPY . .
RUN npm run build

FROM dependencies AS test
COPY . .
RUN npm test

FROM node:22-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production
COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force
COPY --from=build --chown=node:node /src/dist ./dist
USER node
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

Operational rationale:

- build tools and development dependencies do not define the final runtime
  stage;
- the runtime runs as the image-provided unprivileged user;
- dependency manifest copying permits effective layer reuse;
- the command is signal-friendly for controlled shutdown.

## Multi-Stage Build Strategy

Recommended stage responsibilities:

| Stage | Contains | Shipped to production? |
| --- | --- | --- |
| `dependencies` | Toolchain and restored dependencies | No unless it is also an intentionally lean runtime dependency stage |
| `build` | Source compilation and generated output | No |
| `test` | Build-time checks or test utilities | No |
| `runtime` | Required executable/output and runtime libraries | Yes |
| `debug` | Diagnostic tooling when needed | Never as normal production artifact |

Use `--target` to test or inspect a stage during development and CI, rather
than adding debug tools to the normal production image.

## Build Context and `.dockerignore`

Keep the context narrow. A large or sensitive context slows builds and makes
accidental inclusion more likely.

```dockerignore
.git
.github
.env
.env.*
!.env.example
node_modules
coverage
dist
*.pem
*.key
```

The build context exclusion is complementary to `.gitignore`; it protects
image builds even when local files are not tracked by Git.

```text
Good                                      Avoid
.dockerignore excludes .env and keys     COPY . . before filtering secrets
Explicit required source copy            Sending backup dumps to build context
```

## Dependency Separation

Build-time dependencies include compilers, package managers and development
libraries. Runtime dependencies are only what the executing process requires.

For compiled services, prefer copying the resulting binary/artifact into a
runtime stage. For interpreted runtimes, install only production dependencies
in the runtime stage and avoid carrying caches or credentials from builds.

Build secrets, such as a package-registry credential, MUST use a build secret
mount or equivalent secure mechanism, not `ARG` or `ENV` values that may
persist in image metadata or provenance.

```dockerfile
# syntax=docker/dockerfile:1
RUN --mount=type=secret,id=npmrc,target=/root/.npmrc npm ci
```

## Cache and Layer Design

Optimize stable expensive steps before frequently changing source:

```dockerfile
COPY package-lock.json package.json ./
RUN npm ci
COPY . .
RUN npm run build
```

Guidelines:

- combine package index refresh and package install in the same `RUN` layer;
- remove package-manager cache only when it will otherwise ship in runtime;
- do not distort an understandable Dockerfile for negligible size savings;
- treat cache as replaceable acceleration, never as proof of artifact
  identity;
- periodically rebuild with current base/dependency inputs according to patch
  policy.

## Reproducibility and Base Images

Requirements:

- use dependency lockfiles or equivalent controlled resolution;
- record source revision, Dockerfile and resulting digest in CI/CD;
- choose trusted supported base images;
- use a documented policy for base tags and/or digest pinning;
- rebuild for security updates instead of assuming immutable images stay
  secure indefinitely.

Tradeoff:

| Base reference | Benefit | Cost |
| --- | --- | --- |
| Version tag such as `node:22-alpine` | Receives changed upstream content on rebuild | Builds may change over time |
| Version plus digest | Exact build input and reviewable update | Requires deliberate digest refresh process |

Production-sensitive projects SHOULD prefer reviewed digest updates or
equivalent dependency automation that makes base-image changes visible.

## PHP-FPM Runtime Example

```dockerfile
# syntax=docker/dockerfile:1

FROM composer:2 AS dependencies
WORKDIR /app
COPY composer.json composer.lock ./
RUN composer install --no-dev --no-interaction --prefer-dist --no-scripts

FROM php:8.4-fpm-alpine AS runtime
WORKDIR /var/www/html
COPY --from=dependencies /app/vendor ./vendor
COPY --chown=www-data:www-data app/ ./app/
COPY --chown=www-data:www-data public/ ./public/
USER www-data
CMD ["php-fpm", "-F"]
```

The paired NGINX image should receive only its server configuration and public
static assets, not PHP secrets or application write access unless required by
the design.

## NGINX Static/Web Image Example

```dockerfile
# syntax=docker/dockerfile:1

FROM node:22-alpine AS assets
WORKDIR /src
COPY package*.json ./
RUN npm ci
COPY resources/ ./resources/
COPY public/ ./public/
RUN npm run build-assets

FROM nginx:1.27-alpine AS runtime
COPY docker/nginx/default.conf /etc/nginx/conf.d/default.conf
COPY --from=assets /src/public /usr/share/nginx/html
EXPOSE 8080
```

Keep dynamic application execution in the PHP-FPM image and route FastCGI
traffic deliberately through platform networking. If NGINX only serves
platform ingress and no app-specific assets, maintain its image independently
from the application release instead of coupling builds unnecessarily.
