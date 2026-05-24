# Repository Guidelines

## Project Structure & Module Organization

This repository is a documentation-first engineering playbook. Root-level
books organize guidance by domain: `architecture/`, `ci-cd/`, `docker/`,
`github/`, `infrastructure/`, `naming/`, `observability/`, `principles/`,
`repositories/`, `runbooks/`, and `security/`. Each book uses `README.md` as
its entry point and keeps focused topics in sibling Markdown files. Reusable
reference material belongs under `examples/`. Update the root `README.md` and
`OVERVIEW.md` when introducing a new top-level section.

There is no application source tree, compiled output, test suite, or asset
pipeline in this repository.

## Development & Validation Commands

No build or local runtime is required. Review documentation changes with:

```bash
git diff --check
git diff --stat
rg -n '\]\(' README.md OVERVIEW.md principles/
git status --short
```

`git diff --check` detects whitespace errors. `rg` is useful when reviewing
new or changed relative links; confirm their targets exist before committing.

## Writing Style & Naming Conventions

Write clear professional English in Markdown. Prefer short sections, direct
explanations, practical examples, and explicit tradeoffs. Avoid promotional
language and unnecessary abstraction. Follow the existing book pattern:
`README.md` for navigation, lower-case hyphenated topic files such as
`long-term-responsibility.md`, and `references.md` when external guidance is
used.

Keep lines readable, tables compact, and relative links local to the
repository. When incorporating external sources, distinguish the source's
guidance from this playbook's adopted practice and include links.

## Review Guidelines

Treat review as documentation verification: check technical accuracy, internal
link paths, consistency with related books, and whether operational or
security claims are appropriately qualified. New guidance should connect
principles to actionable engineering behavior.

## Commit & Pull Request Guidelines

Recent history predominantly uses concise, scoped documentation commits, for
example `docs: add production observability standards`. Prefer
`docs: <imperative summary>` for documentation work and keep each commit
focused on one coherent addition or correction.

Pull requests should explain scope, affected sections, substantive decisions,
and any newly cited external sources. Link issues where applicable. Screenshots
are only needed when rendered Markdown layout or diagrams are material to the
review.
