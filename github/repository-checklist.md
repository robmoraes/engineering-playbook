# GitHub Repository Checklist

Use this checklist for a new repository, a public portfolio review or a
repository that now controls production delivery.

## Identity and Presentation

- [ ] Repository name follows lowercase kebab-case naming standard.
- [ ] Description communicates purpose in one concise statement.
- [ ] Topics reflect stable technologies or engineering concerns.
- [ ] Visibility is intentional and publication rights are understood.
- [ ] README provides navigation, purpose, setup or inspection path and
  maintenance status.
- [ ] License or usage intent is explicit for public repositories.
- [ ] Public screenshots, logs, examples and diagrams are sanitized.

## Repository Structure

- [ ] `.gitignore` excludes sensitive local artifacts and generated noise.
- [ ] `.env.example` or equivalent contains safe placeholders only when
  configuration is required.
- [ ] Contribution/security files exist only when their process is supported.
- [ ] Architecture decisions or project-specific operating docs are linked
  where material.
- [ ] Issue and PR templates request information reviewers will actually use.

## Branches and Collaboration

- [ ] `main` is the default trusted branch.
- [ ] Branch naming follows the shared convention.
- [ ] Required CI checks run before production-relevant merges.
- [ ] Direct pushes, force pushes and branch deletion are restricted according
  to repository impact.
- [ ] CODEOWNERS covers sensitive areas when real reviewer ownership exists.
- [ ] PR descriptions include verification and operational impact for material
  changes.
- [ ] Commit or merge-message convention is clear where release automation
  depends on it.

## Work Tracking and Releases

- [ ] Labels are small, consistent and useful for triage.
- [ ] Milestones/projects are used only when they improve coordination.
- [ ] Issues and Discussions have distinct purposes where both are enabled.
- [ ] Version/tag strategy is documented for released software.
- [ ] GitHub Releases include meaningful change and operational notes.
- [ ] Published tags/releases are not silently rewritten.

## Actions and Delivery

- [ ] Workflows have descriptive filenames and names.
- [ ] Workflow permissions are explicit and minimal.
- [ ] Pull request jobs do not receive publish or production credentials.
- [ ] Deployment environments separate `stg` and `prod` authority where
  applicable.
- [ ] Image/package publication preserves source and artifact traceability.
- [ ] Reusable workflows are versioned and owned when shared.
- [ ] Self-hosted runners do not expose trusted systems to untrusted code.

## Access and Security

- [ ] MFA is enabled for human identities with meaningful access where
  available.
- [ ] Collaborators/teams receive minimum practical permission.
- [ ] Automation uses `GITHUB_TOKEN`, OIDC, apps or scoped tokens rather than
  broad personal credentials where possible.
- [ ] Secrets are stored at the narrowest applicable repository,
  environment or organization scope.
- [ ] Secret scanning/push protection is enabled where available for public or
  production-sensitive code.
- [ ] Dependabot and code scanning decisions are documented and alerts have an
  owner where enabled.
- [ ] Credentials have a revocation route and are removed when no longer used.

## Lifecycle

- [ ] Repository maintenance status is clear.
- [ ] GitHub Pages content and deployment, if used, are public-safe and
  maintained.
- [ ] Archived repositories remove unnecessary automation and credentials.
- [ ] Replacement or successor repositories are linked when applicable.

## Exception Record

```text
Control:
Repository/context:
Reason:
Operational/security consequence:
Compensating measure:
Owner:
Review/removal date:
```
