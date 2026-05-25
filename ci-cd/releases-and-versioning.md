# Releases and Versioning

A release is a traceable decision to make a tested artifact available for use,
not merely a Git tag or a generated changelog.

## Branch Strategy

Preferred default for small teams, portfolio projects and continuously
delivered services:

- `main` remains releasable and protected;
- work occurs on short-lived feature, fix or documentation branches;
- releases are identified by version tags from trusted history;
- use a release branch only when maintaining a release line or stabilizing
  independently of ongoing `main` work.

```text
main
feat/OPS-142-add-healthcheck
fix/image-promotion
release/v1.8
hotfix/v1.8.3-db-timeout
```

```text
Good                                      Avoid
Short-lived branch merged after CI       Long-lived integration branches nobody can release
Release branch for maintained v1 line    Release branch created for every routine deploy
```

The playbook adopts a trunk-oriented workflow for delivery speed and reduced
merge drift. It does not prohibit release branches where support or deployment
coordination justifies them.

Traditional Gitflow is the secondary strategy when a documented release model
requires a persistent `develop` integration line, planned stabilization on
`release/*` and promotion of completed releases into `main`. See
[GitHub: Branching Strategies](../github/branching-strategies.md) before
introducing long-lived branches.

## Versioning Strategy

Use Semantic Versioning when a project publishes a meaningful public API,
library contract or independently consumed image interface:

```text
MAJOR.MINOR.PATCH
1.8.2
```

| Change | Example version movement |
| --- | --- |
| Backward-compatible bug fix | `1.8.1` -> `1.8.2` |
| Backward-compatible feature | `1.8.2` -> `1.9.0` |
| Incompatible public contract change | `1.9.0` -> `2.0.0` |

For an internal deploy-only application without a published compatibility
contract, a date/release sequence or Git-SHA deployment identity can be
sufficient. Do not claim SemVer meaning where no public API has been defined.

## Git Tags and Image Tags

Use an annotated or otherwise protected release tag according to repository
workflow:

```text
Git tag:     v1.8.2
Image tag:   1.8.2
Image trace: sha-a13f2c91
Deploy ref:  sha256:<digest>
```

The `v` prefix makes Git references readable as release labels; container
image version tags omit it for compact artifact notation. This is an adopted
convention and should remain consistent per project.

Never move a published release tag to different source after consumers may
have used it. If release content changes, publish a new patch version.

## Release Workflow

Reference release sequence:

```text
1. Merge validated changes to main.
2. Build and publish immutable SHA-tagged image.
3. Verify candidate in stg where applicable.
4. Create release version/tag from the selected source revision.
5. Alias or publish the same digest with release version.
6. Promote selected digest to prod after authorization.
7. Verify production and publish release evidence.
```

Release record:

```text
version:        v1.8.2
source commit:  a13f2c91...
image digest:   sha256:...
stg result:     verified or not applicable with reason
prod deploy:    workflow run/link and timestamp
rollback ref:   prior known-good digest
notes:          user-visible or operational changes
```

## Hotfixes

A hotfix still requires traceability. For a production issue:

1. Branch from the release line or source revision currently requiring fix.
2. Validate the smallest corrective change.
3. Publish a new immutable artifact and patch version.
4. Deploy and verify through the fastest safe path appropriate to severity.
5. Merge or forward-port the fix into ongoing development history.

Do not overwrite a failing image tag with changed content under the same
release version. That destroys evidence and complicates incident review.

## Changelog and Release Notes

A project publishing versions for consumers or operators SHOULD keep a
root-level `CHANGELOG.md`. This playbook adopts
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) for that
file:

- record notable changes curated for people, not a commit-log dump;
- keep `## [Unreleased]` first and move its relevant entries into a release
  at publication time;
- order released versions newest first as
  `## [<version>] - YYYY-MM-DD`, using an ISO 8601 calendar date;
- group entries under applicable `Added`, `Changed`, `Deprecated`, `Removed`,
  `Fixed` and `Security` headings, omitting empty groups;
- define Markdown reference links so `Unreleased` compares the latest release
  with `HEAD`, released versions compare adjacent tags, and the initial
  release links to its tag or release page.

When the versioning criteria in this document justify SemVer, the changelog
MUST state that the project adheres to Semantic Versioning and version tags
use `v<MAJOR>.<MINOR>.<PATCH>`. A project using a different release identity
MUST name that policy instead of claiming SemVer compatibility.

Reference template for a SemVer project:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Pending notable capability.

## [1.8.2] - 2026-05-24

### Fixed

- Corrected observable behavior.

[Unreleased]: https://github.com/example/project/compare/v1.8.2...HEAD
[1.8.2]: https://github.com/example/project/compare/v1.8.1...v1.8.2
[1.8.1]: https://github.com/example/project/releases/tag/v1.8.1
```

Release notes, whether published in the changelog or a hosting platform
release record, SHOULD describe:

- user-visible behavior changes;
- operational actions such as migrations or configuration changes;
- security-relevant fixes when disclosure is safe;
- rollback constraints or required follow-up.

The repository changelog is the durable change history; a hosting platform
release may additionally carry artifact and deployment evidence. Neither
should include secrets, internal access details or raw vulnerability exploit
information before remediation is available.
