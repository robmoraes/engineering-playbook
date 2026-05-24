# Container Principles

Containers make an application portable only when their boundaries are clear:
what is in the image, what is supplied at runtime, what is persisted and what
must be operated outside the container.

## Principles

### Package runtime behavior, not environment state

An image contains application runtime code and required runtime dependencies.
It does not contain production secrets, mutable data or environment-specific
decisions.

```text
Good                                      Avoid
Same image deployed to stg and prod      Production URL and secret baked into image
Configuration injected by deployment     Editing files inside running container
```

### Treat containers as replaceable

A running container may be restarted, rescheduled or replaced during normal
delivery and recovery. Durable data belongs in a database, object store,
durable volume design or another explicitly owned backing service.

### Build for the runtime actually operated

A minimal image is valuable when it reduces attack surface, transfer cost and
patch burden. It is harmful when it removes the observability or diagnostics
needed to operate the workload without an alternative debug process.

### Separate deployable responsibilities

One image should represent one independently deployed runtime capability:

```text
orders-api       HTTP/API process
orders-worker    asynchronous processing
portfolio-web    static or frontend delivery runtime
edge-proxy       ingress/reverse proxy
```

Do not combine unrelated services into one container merely because they run
on the same host.

### Align container design with platform behavior

The same image may run through Compose, Swarm or Kubernetes if it:

- uses runtime configuration rather than host-specific mutation;
- exits cleanly and responds to termination signals;
- emits logs to standard streams;
- exposes meaningful health behavior;
- makes state and privilege requirements explicit.

## Application and Web Image Split

A split between application runtime and web/edge runtime is reasonable when the
process responsibilities or scaling boundaries differ.

### PHP-FPM and NGINX Pattern

For a PHP application served through NGINX:

```text
edge/public traffic -> nginx image -> php-fpm app image -> datastore
```

Use separate containers when:

- NGINX owns TLS/static delivery/proxy policy independently of PHP execution;
- PHP-FPM and NGINX may scale or update independently;
- network and filesystem sharing are deliberate and maintainable.

Possible build approach:

```text
builder stage -> application artifacts
php-fpm runtime image <- application code/runtime dependencies
nginx runtime image   <- public assets and NGINX configuration
```

Tradeoff: two images and services require routing, shared asset strategy and
coordinated releases. For a low-traffic application where one supported image
already embeds a suitable serving model, splitting solely for pattern purity
can add work without operational benefit.

```text
Good                                      Avoid
NGINX serves static assets, PHP-FPM runs Combining database, web server and cron
application code with explicit contract  in one container without lifecycle ownership
```

## Immutable Infrastructure Meaning

Immutable operation means changing a containerized service by replacing it
with a newly built, traceable artifact rather than modifying a running
container manually.

It does not mean:

- data cannot change;
- configuration cannot differ by environment;
- images never need rebuilds for base-image patches.

```text
Good                                      Avoid
Deploy new digest for application fix    docker exec and edit production code
Rebuild image for patched base image     Patch container in place without image record
```

## When Containers Are Not Enough

Containers do not provide by themselves:

- database backup or recovery;
- reliable secret lifecycle management;
- multi-node storage guarantees;
- service-level availability;
- deployment approval, rollback safety or artifact trust;
- secure network exposure.

These remain platform and application responsibilities. Containerization makes
them explicit; it does not eliminate them.
