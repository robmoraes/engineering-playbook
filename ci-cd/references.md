# References and Adoption Notes

The sources below describe platform capabilities or established delivery
practices. This playbook converts them into an opinionated but proportional
standard: build once, publish an immutable artifact, promote with environment
isolation, verify deployments and add governance only where project impact
requires it.

## External Guidance and Adoption

| Source | Original guidance or platform behavior | Adoption in this playbook |
| --- | --- | --- |
| GitHub Docs, *Workflow syntax for GitHub Actions* | Defines workflows, jobs, events, permissions, environments and concurrency behavior. | Workflows have explicit roles, minimal permissions, protected production jobs and controlled concurrency. |
| GitHub Docs, *Reusing workflow configurations* | Reusable workflows expose caller-defined inputs and secrets through `workflow_call`. | Reuse standard build/deploy contracts only once interfaces and ownership are stable. |
| GitHub Docs, *Dependency caching reference* | Dependency caches speed jobs but have scope and trust considerations. | Cache replaceable build inputs and avoid trusting untrusted cache outputs in privileged work. |
| GitHub Docs, *Security hardening for GitHub Actions* | Recommends least privilege, protecting secrets, pinning actions to full SHAs and OIDC for cloud authentication. | Privileged workflows are treated as production code and receive narrow, reviewed authority. |
| GitHub Docs, *Secure use reference: self-hosted runners* | Self-hosted runners can be persistently compromised by untrusted workflow code and require careful isolation. | GitHub-hosted runners are the default for public repos; production-connected self-hosted runners never run arbitrary fork code. |
| Docker Docs, *Multi-stage builds* and *Build cache* | Multi-stage Dockerfiles separate build/runtime content; cache can reuse unchanged work. | Use multi-stage container builds and measured, trust-aware cache optimization. |
| Docker Docs, *GitHub Actions* and *Build attestations* | Docker documents image build/push automation and SBOM/provenance attestations. | Publish immutable tagged images and generate provenance where useful for deployment trust. |
| Docker Docs, *Personal access tokens* and *Deploy a stack to a swarm* | Tokens replace passwords for automation; Swarm stacks are deployed from Compose-form descriptions through manager authority. | Docker Hub publication uses scoped tokens and Swarm deployments are treated as privileged environment changes. |
| Kubernetes Docs, *Deployments* | Deployments expose rollout status and revision-based rollback operations for application workloads. | Kubernetes rollout checks are initial deployment verification, supplemented by service behavior checks. |
| Keep a Changelog 1.1.0 | Changelogs are curated for people, group notable changes by version and type, retain an `Unreleased` section and use linkable dated versions. | Versioned projects with consumer or operator impact maintain a root `CHANGELOG.md` in this structure and connect versions to tags or comparisons. |
| Semantic Versioning 2.0.0 | Version semantics apply to software declaring a public API. | Use SemVer for published contracts; do not imply SemVer guarantees for undocumented internal deploys. |
| OpenGitOps, *Principles* | GitOps systems are declarative, versioned and immutable, pulled automatically and continuously reconciled. | Reserve the term GitOps for reconciled desired-state delivery, not any Git-triggered script deployment. |
| The Twelve-Factor App, *Build, release, run* and *Dev/prod parity* | Separate build/release/run stages and keep material environment behavior aligned. | Separate artifacts from environment config and promote the same build through relevant environments. |
| Google SRE, *Release Engineering* | Reliable release engineering emphasizes consistency, repeatability, automation and auditable artifact provenance. | Release records capture source, artifact, deployment result and rollback reference. |
| Trunk Based Development, *Introduction* | Developers collaborate on a single trunk using short-lived branches; release branches may be created when needed. | `main` with short-lived branches is the practical default; release branches are justified by maintenance/stabilization needs. |

## Source Links

- GitHub Docs, *Workflow syntax for GitHub Actions*:
  <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax>
- GitHub Docs, *Reusing workflow configurations*:
  <https://docs.github.com/en/actions/concepts/workflows-and-actions/reusing-workflow-configurations>
- GitHub Docs, *Dependency caching reference*:
  <https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching>
- GitHub Docs, *Security hardening for GitHub Actions*:
  <https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions>
- GitHub Docs, *Secure use reference - Self-hosted runners*:
  <https://docs.github.com/en/actions/reference/security/secure-use>
- Docker Docs, *Multi-stage builds*:
  <https://docs.docker.com/build/building/multi-stage/>
- Docker Docs, *Build cache*:
  <https://docs.docker.com/build/cache/>
- Docker Docs, *GitHub Actions*:
  <https://docs.docker.com/build/ci/github-actions/>
- Docker Docs, *Build attestations*:
  <https://docs.docker.com/build/metadata/attestations/>
- Docker Docs, *Personal access tokens*:
  <https://docs.docker.com/security/for-developers/access-tokens/>
- Docker Docs, *Deploy a stack to a swarm*:
  <https://docs.docker.com/engine/swarm/stack-deploy/>
- Docker Docs, *Deploy services to a swarm*:
  <https://docs.docker.com/engine/swarm/services/>
- Kubernetes Docs, *Deployments*:
  <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/>
- Keep a Changelog 1.1.0:
  <https://keepachangelog.com/en/1.1.0/>
- Semantic Versioning 2.0.0:
  <https://semver.org/>
- OpenGitOps, *Principles*:
  <https://opengitops.dev/>
- The Twelve-Factor App, *Build, release, run*:
  <https://12factor.net/build-release-run>
- The Twelve-Factor App, *Dev/prod parity*:
  <https://12factor.net/dev-prod-parity>
- Google SRE, *Release Engineering*:
  <https://sre.google/sre-book/release-engineering/>
- Trunk Based Development, *Introduction*:
  <https://trunkbaseddevelopment.com/>

## Local Conventions

The following are deliberately adopted playbook rules rather than universal
requirements of a referenced tool:

- trusted `main` publishes SHA-addressable candidate images;
- production selects immutable digests and retains a prior rollback reference;
- `stg` may be omitted for low-impact workloads only with an explicit safe
  deploy and recovery rationale;
- reusable workflows are introduced when stable reuse exists, not as a default
  abstraction for every small repository;
- CI-driven deployment and GitOps are distinct operating models.
