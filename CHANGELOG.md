# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This documentation repository publishes numbered playbook editions using
`vMAJOR.MINOR.PATCH` tags; these versions identify document revisions rather
than a software API compatibility contract.

## [Unreleased]

### Changed

- Clarified that release-tag workflows promote the SHA-addressed candidate
  produced from `main` rather than rebuilding it.
- Added controls for pinning and recording external build-time content inputs.

### Added

- Added architecture standards for timezone-safe software design, including
  UTC server/backend defaults, frontend timezone selection, IANA timezone
  identifiers, RFC 3339 API contracts, PostgreSQL column-type selection,
  persistence, scheduling, display and testing guidance.

## [0.2.0] - 2026-05-25

### Added

- Adopted Keep a Changelog 1.1.0 as the standard for projects publishing
  versioned changes for consumers or operators.
- Added a reference changelog template and release checklist control for
  dated, linkable release entries.
- Established this repository changelog for numbered playbook editions.

## [0.1.0] - 2026-05-24

### Added

- Initial engineering playbook covering principles, architecture, CI/CD,
  containers, GitHub, infrastructure, naming, observability, repositories,
  runbooks and security.
- Examples catalog for future reusable templates, snippets, reference
  implementations and operational scenarios.
- Repository guidance for contribution practices and trunk-based delivery,
  with documented criteria for Gitflow where release needs justify it.

[Unreleased]: https://github.com/robmoraes/engineering-playbook/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/robmoraes/engineering-playbook/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/robmoraes/engineering-playbook/releases/tag/v0.1.0
