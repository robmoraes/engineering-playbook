# Principles and Boundaries

Repository boundaries influence who can change a system, how it is released,
what it exposes publicly and how easily an operator can discover the relevant
documentation during a problem.

## Principles

### Organize around a coherent responsibility

A repository should answer a clear question:

```text
What system, reusable capability, platform concern or body of documentation
does this repository own?
```

```text
Good                                      Avoid
orders-api owns ordering API runtime     backend-things contains unrelated experiments
platform-observability owns telemetry    scripts-new holds unowned production automation
engineering-playbook owns standards      portfolio-final mixes every old project
```

### Match repository boundaries to change boundaries

Keep components together when a normal change needs one coordinated review,
version and deployment. Split when components have different owners, release
cadences, security/visibility boundaries or independent operating lifecycles.

### Prefer discoverability over clever taxonomy

A new maintainer should be able to identify repository purpose through its
name, description, README, topics and ownership information without knowing
private shorthand.

### Keep operational dependencies visible

A code repository may depend on image registries, deployment repositories,
shared workflows, infrastructure modules, secrets or runtime platforms. Those
relationships should be discoverable from README or maintained documentation.

### Treat repositories as living assets

Creating a repository creates maintenance responsibility: dependency updates,
security handling, workflow upkeep, visibility decisions and eventual
retirement.

## Boundary Decision Questions

Before creating or splitting a repository, ask:

| Question | Separate repository signal | Same repository signal |
| --- | --- | --- |
| Ownership | Different accountable owner/team | One owner reviews and operates together |
| Access/visibility | Different confidentiality or contributor boundary | Same access and publication posture |
| Release/deploy | Independent artifact or production deployment | Released and deployed as one unit |
| Data/security | Distinct privileged surface or sensitive boundary | Shared runtime/security boundary |
| Change coupling | Rare coordinated change and stable interface | Frequent atomic cross-component change |
| Lifecycle | Can be retired/versioned independently | Lifecycle is inseparable |
| Tooling cost | Separation improves governance enough to justify CI/docs/version work | Extra repository would only add maintenance |

A service being separately deployable is a strong signal, but not an automatic
rule: a small system may keep closely related deployables in one monorepo while
publishing separate images.

## Repository Boundaries Versus Architecture Boundaries

Repository layout and runtime architecture are related but not identical:

```text
One repository can contain:
  app/api/       -> orders-api image
  app/worker/    -> orders-worker image

Several repositories can participate in:
  one platform deployment
```

Do not create a microservice merely because a repository was split. Do not
assume a monorepo means a monolithic runtime. Record runtime boundaries in
architecture documentation and delivery boundaries in CI/CD documentation.

## Cross-Repository Dependencies

When a repository consumes another repository's output, use a clear contract:

| Dependency type | Preferred contract |
| --- | --- |
| Shared library | Versioned package/module artifact |
| Containerized service | API/event contract and versioned image |
| Infrastructure module | Versioned module reference and upgrade notes |
| Reusable workflow | Versioned/immutable workflow reference |
| GitOps environment configuration | Approved image digest/version input |
| Standards/playbook | Linked adopted standard plus documented exceptions |

```text
Good                                      Avoid
@acme/http-client@1.4.2                 Copy/pasted library folder between repos
workflow reference pinned/versioned      Calling mutable shared delivery behavior silently
```

Git submodules or copied directories MAY be justified for specific vendor or
documentation needs, but they should not be the accidental default for internal
dependency management.

## Repository Creation Decision

Create a repository only when its purpose can be stated in one paragraph and
its lifecycle has an owner:

```text
Name:
Purpose:
Owner:
Visibility:
Artifact/deployment output:
Key dependencies:
Documentation entry point:
Retirement condition:
```

For a personal portfolio, the owner may be one person. The discipline still
prevents unfinished or ambiguous repositories from obscuring credible work.
