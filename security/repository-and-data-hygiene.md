# Repository and Data Hygiene

Security failures in engineering repositories are often mundane: a committed
`.env` file, a debug log containing a token, a production export uploaded as a
demo fixture or a portfolio screenshot showing internal infrastructure.

## Sensitive Files

Every repository SHOULD ignore common local and sensitive artifacts before
development begins:

```gitignore
.env
.env.*
!.env.example
*.pem
*.key
*.p12
credentials.json
secrets/
```

An example file documents required keys without values:

```dotenv
# .env.example
DATABASE_URL=
REDIS_URL=
OIDC_CLIENT_ID=
LOG_LEVEL=info
```

```text
Good                              Avoid
.env.example with empty values    .env.example with working demo password
Secret store reference in docs    Private key pasted into setup guide
Sanitized test fixtures           Production database dump in examples/
```

Ignore rules reduce accidents but do not prevent commits using force-add,
alternate filenames or previously tracked files.

## Git Leak Prevention

Baseline:

- review staged changes before committing;
- keep sensitive local file patterns in `.gitignore`;
- enable secret scanning and push protection when available;
- never store production data or credentials in public portfolio history.

Recommended:

- add secret scanning in local hooks or CI for projects receiving frequent
  contributions;
- enable GitHub secret scanning/push protection for supported repositories;
- treat generated logs, deployment plans and backup files as potentially
  sensitive.

If a secret reaches Git:

1. Revoke or rotate the credential immediately.
2. Investigate access and pipeline use while it was valid.
3. Remove it from visible content and history if appropriate.
4. Confirm downstream clones, artifacts, logs and caches are considered.

History rewriting without rotation leaves the usable credential exposed to
anyone who already fetched or recorded it.

## Logs and Error Handling

Logs must help investigate production without becoming a credential archive.

Never log:

- authorization headers, session tokens or reset links;
- passwords, signing keys or entire secret objects;
- connection strings containing credentials;
- complete payment or sensitive personal records;
- raw CI secret values.

Prefer structured diagnostic context:

```json
{
  "event": "registry_auth_failed",
  "service": "orders-deployer",
  "environment": "prod",
  "registry": "ghcr.io",
  "credential_id": "orders-publisher-prod",
  "error_code": "unauthorized"
}
```

```text
Good                              Avoid
credential_id and failure code    token=ghp_actual_secret_value
Masked user reference             Full customer payload in exception log
```

Masking performed by a CI provider is a safety net, not authorization to print
credentials. Encoded, transformed or partial values may evade masking.

## Documentation and Screenshots

Documentation, diagrams, terminal captures and videos for a public portfolio
MUST be reviewed as publication artifacts.

Remove or replace:

- public IPs and management hostnames when not required;
- account identifiers, repository secrets and access tokens;
- private registry paths if they reveal confidential organization structure;
- internal email addresses and customer data;
- shell history showing exported secrets.

Use synthetic examples such as `example.com`, `ghcr.io/acme/orders-api` and
`token-redacted` consistently.

## Backup and Export Handling

Backups, database dumps, Terraform state, environment exports and diagnostic
archives often contain credentials or sensitive data even if their filename
does not say so.

Baseline:

- do not add them to Git;
- encrypt backups when retained outside a controlled service;
- limit access and define retention;
- sanitize data used for development or portfolio examples.

Terraform or similar state needs protection equivalent to secret storage when
providers or outputs embed sensitive values.
