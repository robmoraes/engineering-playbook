# Security Standards

Practical controls for protecting source code, delivery pipelines, credentials
and containerized workloads without turning small engineering projects into a
compliance program.

## Security Position

Security controls in this playbook protect four recurring boundaries:

1. Source repositories must not become a secret store.
2. Automation must receive only the access required for one job and
   environment.
3. Production credentials, data and deployment authority must remain isolated
   from development and preview workflows.
4. Built artifacts must be attributable to trusted source and pipeline
   execution before deployment.

## Control Levels

| Level | Use | Examples |
| --- | --- | --- |
| **Baseline** | Required for any public or deployed project | Ignore sensitive files, scan for leaked secrets, scoped tokens, non-root containers, immutable production image reference |
| **Recommended** | Default for persistent or internet-facing workloads | OIDC federation, approval gates for production, vulnerability scanning, protected environments, documented rotation and incident response |
| **Advanced** | Higher-risk production, teams or regulated environments | Central vault with dynamic secrets, signed provenance verification, centralized identity, admission policy and audited break-glass workflow |
| **Lab exception** | Local experiments with no sensitive data or live access | Simpler local secret injection is acceptable if nothing is committed and tokens cannot reach production |

The baseline is intentionally achievable by one engineer. Additional controls
should follow actual exposure, access scope and recovery cost.

## Navigation

| Document | Covers |
| --- | --- |
| [Secrets and Credentials](./secrets-and-credentials.md) | Secret handling, encrypted storage, naming, generation and rotation |
| [Identity and Access](./identity-and-access.md) | Least privilege, SSH, service accounts, access segmentation and environments |
| [CI/CD and Automation](./ci-cd-and-automation.md) | GitHub Actions, Docker Hub tokens, deployment credentials and OIDC |
| [Containers and Supply Chain](./containers-and-supply-chain.md) | Container runtime baseline, images, provenance and dependency trust |
| [Repository and Data Hygiene](./repository-and-data-hygiene.md) | Git leaks, sensitive files, logging and portfolio publication |
| [Incident Response](./incident-response.md) | Practical secret exposure and access incident procedure |
| [Baseline Checklist](./baseline-checklist.md) | Review checklist for projects and releases |
| [References](./references.md) | External guidance and adopted conventions |

## Non-Negotiable Defaults

- Secrets MUST NOT be committed, placed in image layers or printed in CI logs.
- Human and machine access MUST be separate and scoped to the minimum
  environment and operation required.
- Production deployments MUST use a traceable image tag or digest, never only
  `latest`.
- Production secrets MUST NOT be shared with development, test or preview
  environments.
- Suspected leaked credentials MUST be revoked or rotated before repository
  cleanup is treated as complete.

## Applying the Standard

Start with [Baseline Checklist](./baseline-checklist.md) for a repository or
deployment. Use the domain documents when implementing a control or recording
an exception. An exception should state the affected asset, risk, temporary
mitigation, owner and removal date.
