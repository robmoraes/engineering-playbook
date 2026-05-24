# Identity and Access

Access design should make normal work easy while making broad or unexplained
access unusual. A useful least-privilege policy answers who or what needs
access, to which environment, for which action and for how long.

## Identity Principles

- Human identities MUST be individual and protected with multi-factor
  authentication where the platform supports it.
- Automated workloads MUST use service accounts, deploy keys or workload
  identity, not a maintainer's personal credential.
- Production write access MUST be restricted more heavily than read-only or
  non-production access.
- Shared administrator credentials SHOULD NOT be used for routine operations.
- Access that is no longer needed MUST be removed promptly.

```text
Good                              Avoid
orders-deployer-prod service acct Personal token used by deployment pipeline
Named maintainer SSH identity     Shared team SSH private key
Read-only monitoring credential   Admin token for dashboard reads
```

## Access Matrix

Each deployed project SHOULD maintain a small access matrix:

| Principal | Environment | Allowed operation | Credential form |
| --- | --- | --- | --- |
| Developer | `dev`, `stg` | Deploy and troubleshoot | Individual identity |
| Release workflow | `prod` | Deploy approved image only | Environment-scoped service identity |
| Application service | `prod` | Read its own secret and database schema | Workload/service identity |
| Monitoring agent | `prod` | Read metrics and logs | Read-only service identity |
| Break-glass operator | `prod` | Emergency administrative action | Audited elevated identity |

For a personal portfolio, the principal may be one person, but human login,
deployment automation and application runtime credentials still need separate
scopes.

## Environment Isolation

Production and non-production SHOULD be separated through the strongest
practical boundary available:

| Maturity | Minimum boundary |
| --- | --- |
| Local or lab | Separate credentials and no production data |
| Hosted portfolio workload | Separate secrets and protected production deployment environment |
| Production service | Separate accounts/projects, networks or clusters when feasible; restricted data and deployment access |
| Higher-risk platform | Separate administrative boundaries, audited access and explicit cross-environment promotion |

Rules:

- Non-production workloads MUST NOT hold production write credentials.
- Preview deployments MUST NOT use production secrets or unsanitized
  production data.
- Artifacts may be promoted across environments; credentials and configuration
  must not be promoted with them.

## Service Accounts and Machine Users

Create a machine identity for a defined purpose and environment:

```text
orders-ci-publisher
orders-deployer-stg
orders-deployer-prod
observability-reader-prod
```

Use separate identities when privileges or blast radius differ. One token that
can publish any image, deploy any service and change production secrets is
convenient initially but difficult to audit and dangerous to leak.

For each machine identity, document:

- owner and purpose;
- environments and resources permitted;
- token issuance and storage location;
- expiry or review date;
- revocation and replacement steps.

## SSH Access

SSH remains reasonable for small host-based or Swarm environments when tightly
managed.

Baseline:

- Use key-based access; disable password authentication where safely possible.
- Use individual public keys, not one shared private key across maintainers.
- Store private keys outside repositories and CI logs.
- Limit users permitted to administer production hosts.
- Remove keys when no longer required.

Recommended:

- Use a bastion, VPN or restricted network path for management endpoints.
- Separate automation keys from interactive user keys.
- Restrict automation commands or target hosts where feasible.
- Log administrative access and retain enough detail for investigation.

Advanced environments SHOULD prefer short-lived SSH certificates or managed
session access instead of long-lived authorized keys.

```text
Good                              Avoid
Dedicated deploy key scoped host  Root private key stored as repository secret
Named operator public key         Shared id_rsa copied between machines
```

## Privileged and Break-Glass Access

An emergency administrative path MAY exist, but it should not be the daily
delivery mechanism. Document where it is stored, who may invoke it, how its
use is recorded and when access is reviewed afterward.

For small projects, this can be a protected owner account with MFA and a
written recovery procedure. For a platform team, it should generally include
approval, audit and time-limited elevation.
