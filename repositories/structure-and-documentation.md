# Structure and Documentation

Repository structure should help a maintainer find code, delivery controls,
decisions and operations without learning a unique layout for every project.

## Universal Baseline

Use only the files relevant to the repository, but keep their roles
predictable:

```text
README.md
.gitignore
.github/
  workflows/
  PULL_REQUEST_TEMPLATE.md      # when useful
  CODEOWNERS                    # when ownership requires it
docs/                           # deeper documentation, optional
architecture/                   # topology/ADRs, optional
examples/                       # safe reusable examples, optional
scripts/                        # maintained automation, optional
```

Public reusable software may additionally need `LICENSE`, `CONTRIBUTING.md`
and `SECURITY.md`. Do not create empty files solely to appear complete.

## Application Repository Example

```text
orders-api/
├── README.md
├── .github/
│   └── workflows/
│       ├── build-and-test.yml
│       └── publish-image.yml
├── Dockerfile
├── compose.yaml
├── .env.example
├── src/
├── tests/
├── architecture/
│   └── decision-records/
├── docs/
│   └── deployment.md
└── scripts/
    └── verify-deployment.sh
```

Operational implication: source, image definition, validation, decisions and
verification are discoverable within the application responsibility boundary.

## Infrastructure Repository Example

```text
platform-infrastructure/
├── README.md
├── .github/
│   ├── CODEOWNERS
│   └── workflows/
│       ├── validate.yml
│       └── apply-prod.yml
├── modules/
│   ├── network/
│   └── compute/
├── environments/
│   ├── stg/
│   └── prod/
├── docs/
│   ├── state-management.md
│   └── recovery.md
└── architecture/
    └── decision-records/
```

Production apply authority should be protected separately from validation.
Do not commit backend credentials or sensitive state outputs.

## Platform Repository Example

```text
platform-observability/
├── README.md
├── docs/
│   ├── onboarding.md
│   ├── tenancy.md
│   └── operations.md
├── dashboards/
├── alerts/
├── deploy/
├── examples/
└── architecture/
    └── decision-records/
```

A platform repository requires consumer onboarding and operational impact
documentation because its failures or breaking changes affect multiple teams
or services.

## Documentation-First Repository Example

```text
engineering-playbook/
├── README.md                  # quick navigation
├── OVERVIEW.md                # scope and philosophy
├── architecture/
├── ci-cd/
├── docker/
├── github/
├── naming/
├── repositories/
├── security/
└── examples/
```

Use topic modules rather than a single oversized README. A reader should be
able to navigate from a standard to its implementation examples and sources.

## README Standard

A repository README SHOULD answer:

| Question | Section example |
| --- | --- |
| What is this? | Purpose and scope |
| Why does it exist? | Problem/capability demonstrated |
| How do I inspect or run it? | Quickstart or navigation |
| How is it delivered/operated? | Build/deployment or docs link |
| Where are decisions documented? | Architecture/ADR link |
| What is its maintenance/public status? | Status/license/security statement |

Example compact landing page:

```markdown
# Orders API

Order management API deployed as a containerized service.

## Navigation

- [Architecture](./architecture/)
- [Local Development](./docs/local-development.md)
- [Delivery](./docs/deployment.md)

## Quick Start

...

## Status

Maintained reference service for portfolio deployment practices.
```

Keep project charters and long engineering rationale in linked documents where
they do not bury navigation.

## ADR Organization

Use ADRs where a repository owns significant choices:

```text
architecture/
└── decision-records/
    ├── README.md
    ├── template.md
    └── 0001-use-managed-postgresql.md
```

ADRs are appropriate for changes to datastore, orchestration, public/security
boundaries, deployment authority, high availability or repository model.
Reference the shared ADR standard in
[Architecture Decision Records](../architecture/decision-records/README.md).

## Examples and Templates

Examples MUST be safe to publish and easy to adapt:

```text
examples/
├── compose.yaml
├── Dockerfile
└── build-and-test.yml
```

Never include:

- real tokens or credentials;
- client/customer data;
- internal endpoint names unless intentional and safe;
- production Terraform state or exports.

Templates reduce setup time when they remain current. A template repository or
shared starter structure should have an owner and a review/update cadence.
