# Issues, Projects and Releases

GitHub planning features should improve discoverability and release
traceability, not create duplicate administration for small projects.

## Issues

Use issues for work that benefits from an explicit problem statement,
discussion or follow-up. A small documentation fix can be submitted directly
as a pull request without creating an issue first.

Issue content SHOULD capture:

```markdown
## Problem

## Expected Outcome

## Constraints or Context

## Acceptance Notes
```

For incidents or security findings, avoid posting active secret values or
sensitive exploit detail in public issues.

## Labels

Use a small predictable label taxonomy:

| Category | Labels | Purpose |
| --- | --- | --- |
| Type | `type:feature`, `type:bug`, `type:docs`, `type:security`, `type:maintenance` | Nature of work |
| Area | `area:ci-cd`, `area:docker`, `area:infrastructure`, `area:security` | Affected domain |
| Priority | `priority:critical`, `priority:high`, `priority:normal`, `priority:low` | Triage ordering |
| Status | `status:blocked`, `status:needs-decision` | Exceptional workflow state |
| Contribution | `good first issue`, `help wanted` | Public contributor discoverability |

```text
Good                                      Avoid
type:bug + area:ci-cd                    bug2, urgent-new, fix-soon
```

Do not encode every workflow state as a label if a project board field already
owns that state.

## Milestones

Milestones are useful when a repository needs to group issues and pull
requests for a release or meaningful delivery objective:

```text
v1.8.0
portfolio-publication
production-hardening-q3
```

Do not create milestones for routine continuous delivery unless they answer a
real tracking or release question.

## Projects and Boards

Use GitHub Projects when work spans multiple repositories, needs prioritization
or has enough parallel items that a board improves coordination.

| Context | Recommendation |
| --- | --- |
| Personal small project | Issues and a milestone may be enough |
| Portfolio roadmap | Lightweight project board can communicate planned work |
| Team platform work | Shared project with priority, owner and status fields |
| Enterprise program | Organization-level project/reporting only when it reduces coordination burden |

The repository remains the technical source of truth for code, decisions and
release evidence. A board should not replace ADRs, runbooks or issue context.

## Discussions

Enable GitHub Discussions where a public project benefits from questions,
ideas or usage help that should not become actionable defect tickets.

Use:

- issues for accepted work, bugs and tracked tasks;
- discussions for questions, proposals before commitment and community help;
- private channels for active security disclosures unless public disclosure is
  intended and safe.

## Tags and GitHub Releases

Use Git tags and GitHub Releases for published versions or meaningful delivery
milestones:

```text
Git tag:        v1.8.2
GitHub Release: v1.8.2
Container tag:  1.8.2
Artifact trace: sha256:<digest>
```

Release notes SHOULD identify:

- outcome and user-visible changes;
- operational changes such as migration or configuration requirements;
- source/tag and artifact reference when deployed;
- known rollback constraints;
- security fixes at an appropriate disclosure level.

GitHub-generated release notes can provide a useful draft from merged pull
requests and contributors. Review and edit them before publication when
operational impact needs to be clear.

## Release Workflow Example

```text
PR validated and merged to main
  -> trusted workflow builds/publishes SHA artifact
  -> selected revision tagged v1.8.2
  -> GitHub Release documents changes and artifact digest
  -> deployment workflow promotes digest
  -> release notes link deployment/rollback evidence where appropriate
```

Do not move a published version tag to new content. Create a new release if
the artifact or source changes.

## ADR and Release Integration

Link significant technical decisions from issues or pull requests and note
relevant ADRs in release notes when they alter operating behavior:

```text
ADR-0003: adopt managed object storage
Release impact: uploads now depend on managed storage service; migration
procedure linked in deployment notes.
```

This keeps rationale, implementation and operational rollout connected without
forcing all discussion into one document.
