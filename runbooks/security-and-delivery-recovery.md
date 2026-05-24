# Security and Delivery Recovery

Operational incidents frequently intersect with credentials, delivery
authority or artifact trust. Contain active security risk before optimizing
availability when a compromised path could continue causing harm.

## Suspected Secret or Credential Exposure

Symptoms:

- secret printed in logs, workflow output, terminal capture or repository;
- unauthorized registry, deploy, cloud or database operation;
- expired or invalid credential causing production outage;
- secret rotation deploy fails.

### Exposure Procedure

1. Identify the credential identifier, owner, scope and affected
   environments without redistributing its value.
2. Revoke or disable the exposed credential immediately when exposure is
   credible.
3. Preserve event times, audit activity, workflow/deployment evidence and
   accessible scope.
4. Issue a replacement identity/credential with equal or narrower privilege
   through protected storage.
5. Update authorized consumers and safely redeploy or reload.
6. Verify service behavior and investigate unauthorized use.
7. Correct the leak path and review related credentials/artifacts.

Availability may briefly degrade during immediate revocation; continued use of
a known exposed production credential is usually the larger risk.

## Credential Misconfiguration Without Exposure

If a secret reference is wrong or expired but not exposed:

1. confirm failure through authentication error classification;
2. identify the expected secret object/reference and affected consumer;
3. correct or rotate through the approved secret management route;
4. restart/redeploy only the required consumer;
5. verify authentication and user-facing function;
6. document why delivery or expiry monitoring failed.

Never troubleshoot by printing secret values or embedding them temporarily in
Compose files, workflow YAML or shell history.

## CI/CD Failure Recovery

| Failure | Diagnosis | Recovery |
| --- | --- | --- |
| Build/test failure | Workflow logs and source revision | Fix code/workflow; do not deploy unverified artifact |
| Image publish failure | Registry authentication/permission/quota | Repair scoped publisher identity or registry issue |
| Deploy failure before workload changes | Deploy authority/control plane/input | Restore deployment path and retry approved digest |
| Partial/bad deployment | Running digest, rollout/task state, service checks | Roll back or redeploy prior approved state where compatible |
| Untrusted workflow/artifact | Source/action change, digest and credential exposure | Stop promotion, rotate plausible credentials and deploy trusted digest |

Production delivery recovery must distinguish pipeline health from service
health. A green retry after a failed deploy does not prove that user-facing
behavior recovered.

## Suspicious Artifact Procedure

1. Pause promotion/deployment of the affected tag or digest.
2. Identify running production digests and known trusted build evidence.
3. Determine whether secrets or publish/deploy authority were available to the
   suspect build path.
4. Deploy a verified immutable digest if runtime trust is uncertain.
5. Rotate exposed or plausibly compromised credentials.
6. Verify service and registry state and preserve evidence.

See [Security Incident Response](../security/incident-response.md) and
[CI/CD Deployments and Promotion](../ci-cd/deployments-and-promotion.md).

## Emergency Access

Break-glass or elevated access may be necessary to recover production. It MUST
not become normal delivery practice.

Record:

```text
Reason for elevation:
Person/identity using access:
Start/end time:
Commands or changes performed:
Evidence retained:
Configuration reconciliation:
Access revocation/review:
```

## Validation

- compromised or failed credential is no longer the active path;
- only intended replacements are configured;
- trusted artifact/digest is deployed if artifact integrity was implicated;
- public/critical service checks pass;
- audit/log evidence is retained without secret values;
- scanning, workflow permission, expiry alert or procedure improvement is
  tracked where applicable.
