# Pipeline Principles

CI/CD should reduce manual uncertainty without granting automation unlimited
authority. A useful pipeline makes failures visible early, creates one
traceable artifact and makes production change deliberate and reversible.

## Principles

### Validate before privileged actions

Run formatting, linting, tests and build validation before publishing images or
requesting deployment credentials.

```text
Good                                      Avoid
PR test job with read-only permissions    PR build receiving production deploy key
Publish only after tests pass             Publish image before validation finishes
```

### Build once and promote

Build a deployable artifact once from trusted source, verify it, and promote
the same immutable artifact through environments:

```text
Source SHA a13f2c91
  -> ghcr.io/acme/orders-api:sha-a13f2c91
  -> verified in stg
  -> deployed to prod by digest sha256:<digest>
```

Rebuilding for each environment weakens traceability because source-equivalent
builds can still differ through changing dependencies, base images or build
inputs.

### Separate artifact creation from environment authorization

Building an image is not the same permission as deploying it. The build
pipeline should not need production secrets, and production deployment should
only select an already trusted artifact plus environment configuration.

### Keep pipeline behavior understandable

A delivery workflow is operational code. Prefer a visible sequence of jobs and
reusable components with clear contracts over layers of indirection that make
deployment hard to diagnose during an incident.

### Automate repeatable checks, preserve meaningful decisions

Automate deterministic validation, artifact creation, scanning, deployments
and verification. Retain a manual approval or explicit release action where
production impact, data migration or business timing needs human judgment.

## Reference Pipeline Shapes

### Pull Request Validation

```text
checkout -> dependency restore/cache -> lint -> unit tests
         -> build validation -> integration tests where justified
         -> security or image scan where relevant
```

No deploy or publication credential is available. Preview environments may be
created only with isolated credentials and data.

### Trusted Main Branch

```text
checkout trusted revision -> test -> build container -> scan
                          -> publish immutable SHA tag
                          -> store digest/build metadata
```

Publication from `main` produces deployable candidate artifacts. It need not
deploy production automatically.

### Release and Production Promotion

```text
select verified digest -> deploy stg -> smoke/health verification
                       -> manual approval when required
                       -> deploy prod -> verify -> record result
```

For low-risk personal services, `stg` may be omitted if a documented deploy and
rollback path exists. For production-critical systems, omission of meaningful
validation requires justification.

## Pipeline Stages

Use a stable vocabulary across repositories:

| Stage | Responsibility | Failure result |
| --- | --- | --- |
| `validate` | Format, lint and policy checks | Stop change |
| `test` | Automated correctness verification | Stop change |
| `build` | Produce artifact | No artifact published |
| `scan` | Dependency/image/security signal | Block or require documented exception by policy |
| `publish` | Store immutable artifact and metadata | No deployment candidate |
| `deploy` | Change target environment to selected artifact | Start recovery/rollback if unhealthy |
| `verify` | Health, smoke and observable behavior checks | Rollback or incident decision |
| `rollback` | Restore trusted prior version or recover service | Escalate if unsuccessful |

## Automation Boundaries

| Boundary | Pipeline may do | Pipeline should not silently do |
| --- | --- | --- |
| Source validation | Read source, run tests, create ephemeral outputs | Access production credentials |
| Artifact publishing | Push artifact to scoped registry repository | Modify production runtime |
| Non-production deploy | Deploy isolated test/staging configuration | Reuse production data or tokens |
| Production deploy | Deploy approved immutable artifact | Build new untested artifact |
| Database migration | Execute reviewed compatible migration | Run destructive change without recovery plan |

## Operational Tradeoffs

| Decision | Benefit | Cost or risk |
| --- | --- | --- |
| Single compact workflow | Easy to see in a small project | Repetition across repositories |
| Reusable workflow | Consistency and centralized fixes | Changes can affect multiple consumers; versioning required |
| Automatic production deploy from `main` | Fast delivery | Every merge becomes production authority |
| Approved production promotion | Better risk boundary | Slower delivery and reviewer availability |
| Extensive end-to-end suite | Broader behavioral validation | Execution time, flakiness and cost |

The correct pipeline is the smallest one that provides sufficient evidence and
control for its workload impact.

## Environment Boundaries

Use `dev`, `test`, `stg`, `prod` and `preview` consistently with the naming
standard. Environment values and secrets are deployment inputs; they must not
be baked into artifacts.

```text
Good                                      Avoid
Same image digest in stg and prod        prod-specific image rebuild
Preview with sandbox credentials         Pull request with prod database secret
```
