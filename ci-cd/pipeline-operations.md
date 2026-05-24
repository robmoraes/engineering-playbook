# Pipeline Operations

Delivery automation needs its own operations model: failures, duration,
resource consumption and dependency trust affect engineering throughput and
production risk.

## CI/CD Observability

Track enough pipeline information to answer:

- Which source and artifact were deployed?
- How often do validation, publication or deployment workflows fail?
- How long does change validation and production delivery take?
- Which environments currently run which image digest?
- How frequently are rollbacks or failed deployments occurring?

Useful indicators:

| Indicator | Operational use |
| --- | --- |
| Build/test failure rate | Identify flaky or degraded validation |
| Workflow duration by stage | Find slow feedback and cost hotspots |
| Deployment frequency | Understand delivery behavior, not performance alone |
| Deployment failure/rollback rate | Improve release safety |
| Time to recover failed deployment | Validate rollback/runbook quality |
| Current deployed digest per environment | Incident traceability |

Pipeline metrics should inform improvement, not encourage unsafe delivery speed
or punishment for necessary controls.

## Failure Handling

Fail early on deterministic problems:

- formatting or lint policy failure;
- unit/integration test failure;
- compilation/build error;
- invalid deployment manifest;
- unavailable required artifact.

For infrastructure or external dependency errors, distinguish transient
failures from defects before retrying.

```text
Good                                      Avoid
Retry registry push after timeout        Retry failing unit tests until green
Retain test reports on failure           Swallow failed deploy healthcheck
```

## Retry Strategy

Retries are appropriate for bounded transient operations such as registry
network requests, API rate responses with backoff or health stabilization.

Rules:

- do not retry deterministic validation failures automatically;
- bound attempts and use delay/backoff;
- preserve final failure evidence;
- make deployment operations idempotent or safely repeatable before retrying;
- never mask a failing verification by endlessly retrying.

Repeated flakiness is a defect in tests, environment or dependency management,
not a success achieved by retry count.

## Parallelization

Parallel jobs shorten feedback when they do not compete for scarce resources or
hide dependency order:

| Good candidate | Poor candidate |
| --- | --- |
| Independent lint and unit tests | Deploy and post-deploy verification |
| Matrix tests for supported runtimes | Multiple production deploys targeting same service |
| Independent images in a monorepo | Database migration racing application rollout |

Tradeoff: parallelism improves elapsed time but consumes more runner minutes,
external service quota and diagnosis effort when failures interleave.

## Caching

Use caching for replaceable build inputs, not for authoritative outputs or
secrets:

| Cache | Recommended key input | Concern |
| --- | --- | --- |
| Package dependencies | OS/runtime and lockfile hash | Stale or poisoned dependency state |
| Docker layers | Dockerfile and content-addressed layers | Cache trust across untrusted builds |
| Tool installation | Tool version | Unsupported/stale binary |

Measure before adding complicated cache flows. A small project with a
two-minute build may not benefit from cache maintenance complexity.

## Monorepo and Multirepo Pipelines

| Model | Delivery advantage | Operational challenge |
| --- | --- | --- |
| Monorepo | Coordinated change and shared workflow definitions | Avoid rebuilding/deploying unaffected services; define path ownership |
| Multirepo | Independent pipeline and release boundaries | Shared changes and platform standards require coordination/versioning |

For monorepos:

- map changes to affected deployable components;
- keep shared validation from skipping required integration checks;
- publish one artifact per independently deployed component.

For multiple repositories:

- version reusable workflows rather than silently changing every consumer;
- standardize artifact metadata and promotion rules;
- document dependency release order where services or libraries couple.

Choose based on ownership and change patterns, not CI fashion.

## Pipeline Cost and Runner Selection

Pipeline cost includes hosted runner minutes, self-hosted maintenance,
registry/storage retention, external test dependencies and engineer waiting
time.

Optimize in this order:

1. Remove unnecessary work and duplicate builds.
2. Run fast high-signal validation earlier.
3. Cache stable replaceable inputs.
4. Parallelize only useful independent work.
5. Select specialized/self-hosted runners only when their operating cost and
   security exposure are justified.

The cheapest runner is not cheaper if an unreliable or exposed build
environment consumes incident response time.

## Shared Workflow Governance

Shared workflows are platform products once multiple teams or projects depend
on them. Maintain:

- versioned releases or immutable references;
- documented inputs, outputs and required permissions;
- migration guidance for breaking changes;
- test coverage for representative consumers;
- ownership for security updates and runner compatibility.

In a personal repository collection, a copied short workflow may be more
maintainable than premature centralization. Centralize when repetition creates
meaningful inconsistency or maintenance burden.
