# Branching Strategies

Branching strategy is an engineering and release-management decision. Choose
the simplest model that supports release, maintenance and audit requirements
without introducing unnecessary integration delay.

## Decision Order

Use the following order of preference:

1. Prefer **Trunk-Based Development** whenever the product can integrate
   frequently into `main` and release from trusted history.
2. Use **Traditional Gitflow** only when separate integration and production
   histories solve a documented release or support need.

```text
Need continuous integration, frequent releases or simple delivery?
  -> Trunk-Based Development

Need planned versioned releases with a shared next-release integration line,
parallel release stabilization or multiple supported versions?
  -> Traditional Gitflow, with the reason documented
```

Do not adopt Gitflow only because a project has pull requests, environments or
release tags. Those controls work with trunk-based development.

## Preferred Model: Trunk-Based Development

The default strategy keeps `main` releasable and integrates small changes
through short-lived branches:

```text
main
  <- feat/OPS-142-add-healthcheck
  <- fix/image-promotion
  <- docs/github-standards
  <- release/v1.8            only when stabilization or maintenance requires it
  <- hotfix/v1.8.3-timeout   only for a supported release line
```

Use trunk-based development when:

- changes can be integrated in small reviewable units;
- CI validates changes before or immediately after merge;
- incomplete behavior can be controlled through design, configuration or
  feature flags where needed;
- production artifacts can be traced to `main` commits or release tags;
- release branches, if any, are exceptions rather than the integration model.

This is the playbook default because it reduces merge drift and supports
continuous integration and delivery without a permanent intermediary branch.

## Secondary Model: Traditional Gitflow

Traditional Gitflow retains two long-lived branches and several supporting
branch types. The original model names the production branch `master`; this
playbook uses `main` instead and applies its existing `<type>/<description>`
branch naming convention while preserving the Gitflow branch roles.

```text
main                 production-ready history; release tags originate here
develop              long-lived integration history for the next release
feat/<description>   feature work branched from and merged into develop
release/v<version>   release stabilization branched from develop
hotfix/v<version>-*  urgent production fix branched from main
```

The branch flow is:

```text
feature:  develop -> feat/* -> develop
release:  develop -> release/* -> main + develop; tag on main
hotfix:   main -> hotfix/* -> main + develop; tag on main
```

### When Gitflow Is Appropriate

Gitflow MAY be selected when one or more of these needs are real and
documented:

- releases are explicitly versioned and scheduled rather than continuously
  selected from `main`;
- a stabilization period must proceed while the team integrates work intended
  for a later release;
- multiple released versions must receive fixes in parallel;
- product, regulatory or external-distribution constraints require a durable
  distinction between next-release integration and production-ready history.

Gitflow is usually a poor fit for continuously delivered services where one
current production version is supported and small changes can be released from
`main`.

### Gitflow Branch Rules

| Branch | Lifetime | Branches from | Merges into | Purpose |
| --- | --- | --- | --- | --- |
| `main` | Permanent | N/A | N/A | Production-ready release history and tags |
| `develop` | Permanent | `main` initially | N/A | Integration state for the next planned release |
| `feat/*` | Temporary | `develop` | `develop` | Reviewable feature or planned change |
| `release/*` | Temporary | `develop` | `main` and `develop` | Stabilization, release metadata and approved fixes only |
| `hotfix/*` | Temporary | `main` or a supported release revision | `main` and `develop` | Urgent correction to released production behavior |

Do not add new features to `release/*` or `hotfix/*`. A correction applied to
production history MUST also reach `develop`, whether by merge or an explicitly
recorded forward-port.

### Gitflow Release Sequence

```text
1. Integrate intended release work into develop.
2. Create release/v1.8 from develop when scope is fixed.
3. Apply only stabilization fixes and release metadata on release/v1.8.
4. Validate the release candidate and merge it into main.
5. Create the immutable release tag, such as v1.8.0, from main.
6. Merge release/v1.8 corrections back into develop.
7. Delete the completed temporary release branch when retention is not needed.
```

For an urgent correction:

```text
1. Create hotfix/v1.8.1-timeout from main or the affected supported tag.
2. Validate and merge the correction into main.
3. Tag the patched release from main.
4. Merge or forward-port the correction into develop and any affected
   maintained release line.
```

## Selection Record

A repository using the default trunk-based strategy needs no exception record.
A repository selecting Gitflow SHOULD state the decision in its README or ADR:

```text
Branching strategy: Traditional Gitflow
Reason: Planned versioned releases require stabilization while next-version
        integration continues on develop.
Protected branches: main, develop, release/*
Release source and tagging: main with immutable v<version> tags
Re-evaluation trigger: Continuous delivery adoption or end of parallel support
```

Reassess Gitflow if its `develop` or release branches create regular merge
conflicts, delayed feedback or fixes that are not consistently propagated
between supported histories.

## Related Standards

- Branch names, protection, pull requests and review:
  [Branches, Commits and Pull Requests](./branches-commits-and-pull-requests.md).
- Version tags, immutable artifacts and release evidence:
  [CI/CD: Releases and Versioning](../ci-cd/releases-and-versioning.md).
- Branch and tag naming:
  [Naming: Source Control and Artifacts](../naming/source-control-and-artifacts.md).
- External sources and adopted conventions:
  [References](./references.md).
