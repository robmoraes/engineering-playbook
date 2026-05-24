# Secrets and Credentials

Secrets include API tokens, passwords, private keys, signing keys, connection
strings containing credentials, webhook secrets and cloud access material.
Their operational value is access, so they require lifecycle management rather
than careful file naming alone.

## Baseline Rules

- Secrets MUST NOT be stored in Git history, Dockerfiles, Compose files,
  public documentation, screenshots, issue comments or workflow logs.
- Each credential MUST identify an owner, consumer, environment and rotation
  or revocation route.
- Production credentials MUST be separate from non-production credentials.
- Credentials SHOULD be scoped and short-lived where the provider supports it.
- A suspected exposure MUST trigger revocation or rotation; deleting a string
  from the latest commit is not remediation.

## Classification

| Kind | Examples | Handling |
| --- | --- | --- |
| Public configuration | Domain name, public image repository | May be committed |
| Sensitive configuration | Internal hostname, account identifier | Avoid public exposure; store with deployment configuration where justified |
| Secret | Password, access token, private key, signing secret | Store in a secret manager or approved encrypted mechanism only |
| High-impact secret | Production deploy token, root cloud key, TLS private key | Strongly restrict, monitor and rotate with a tested process |

## Secret Naming

Name the secret object so operators can identify its consumer and scope; never
put secret values or personal identifiers in the name. Follow the naming
standard in [Runtime and Infrastructure Resources](../naming/runtime-and-infrastructure.md).

```text
<system>-<consumer>-<credential>[-<environment>]

orders-api-db-password-prod
edge-proxy-dns-token-prod
portfolio-web-oauth-client-secret-stg
```

```text
Good                              Avoid
orders-api-db-password-prod       password-final-new
edge-proxy-dns-token-prod         carlos-cloud-key
portfolio-web-session-key-stg     token-AKIA...
```

Within an application, expose concise variable names:

```text
Secret object: orders-api-db-password-prod
Runtime variable: DATABASE_PASSWORD
```

## Storage Strategies

| Context | Acceptable approach | Tradeoff |
| --- | --- | --- |
| Local development | Untracked `.env` file containing non-production values, or local password-manager injection | Simple, but each developer must prevent accidental commit and local backup leakage |
| Public portfolio demo | Repository secrets or hosting-provider secrets with demo-only scope | Practical, but still requires token rotation and log hygiene |
| Persistent production | Managed secrets store or deployment platform secret mechanism with restricted access | Better access controls and operations; introduces platform dependency |
| Larger production platform | Vault/KMS-backed store with policy, audit and optional dynamic credentials | Stronger lifecycle controls; requires operational ownership and recovery procedures |

Encrypted files MAY be committed only when the decryption key is managed
separately and access-controlled. Encryption is not useful if the ciphertext
and key are available through the same repository or workflow permissions.

```text
Acceptable                        Unsafe
Encrypted config in Git           Plaintext .env.production in Git
Key held in cloud KMS             Key committed beside encrypted file
```

## Generation and Distribution

- Generate secrets using a cryptographically secure source supplied by the
  platform or secret manager.
- Prefer tokens created for a named automation consumer over a personal token.
- Transfer secrets through the secret store or provider UI/API, not chat,
  email or issue trackers.
- Supply secrets at runtime or deployment time. Do not bake them into images.

Example lifecycle record:

| Field | Example |
| --- | --- |
| Secret | `orders-api-db-password-prod` |
| Consumer | `orders-api` deployment |
| Owner | Platform operations |
| Scope | Database login for `orders_prod` only |
| Stored in | Production secret manager |
| Rotation trigger | 90-day review or suspected exposure |
| Revocation test | Application re-authenticates after rolling deploy |

## Rotation and Revocation

Rotation frequency should follow credential impact and provider capability, not
an arbitrary ritual. Short-lived federated credentials reduce the need for
calendar rotation. Long-lived production tokens need a documented review and
replacement procedure.

For a rotatable application secret:

1. Create a replacement credential with equal or narrower privileges.
2. Store it in the target environment without exposing its value.
3. Deploy or reload consumers and verify authentication.
4. Revoke the old credential.
5. Record the rotation date and any follow-up action.

Prefer overlapping rotation when the provider supports two valid credentials.
Immediate revoke-first rotation is appropriate for suspected leaks, accepting
possible service interruption to stop unauthorized use.

## Vaulting Approaches

**Baseline:** hosting platform or GitHub environment secrets for scoped
automation, and untracked non-production local configuration.

**Recommended:** cloud secret manager or orchestrator-managed secrets for
persistent deployed workloads; use workload identity instead of static cloud
keys where available.

**Advanced:** centralized Vault/KMS solution with dynamic database or cloud
credentials, audited access, recovery documentation and policy-as-code.

A vault is not a security improvement if it is deployed without backup,
unseal/recovery ownership, access policy or a method for applications to
authenticate safely.
