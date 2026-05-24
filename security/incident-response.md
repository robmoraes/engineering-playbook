# Security Incident Response

This procedure is intentionally lightweight. It is meant to make the first
hour of a likely credential or access incident predictable for small and
mid-sized engineering workloads.

## What Qualifies as an Incident

Treat the following as security incidents until assessed:

- a token, private key or password committed or published;
- unexpected use of a deployment, registry or cloud credential;
- an untrusted workflow run with access to secrets;
- a container image published from an untrusted source or workflow;
- production access granted to the wrong identity;
- logs or artifacts exposing sensitive information.

## Immediate Response

1. **Contain access.** Revoke or rotate exposed credentials, disable affected
   machine identities or pause a compromised deployment path.
2. **Preserve facts.** Record times, affected repositories, workflow runs,
   image digests, audit entries and actions taken. Do not retain secret values
   in the incident record.
3. **Assess reach.** Identify environments, resources and data accessible to
   the credential or artifact.
4. **Restore safely.** Issue replacement credentials with minimal scope,
   rebuild or redeploy trusted artifacts if required and verify service health.
5. **Prevent recurrence.** Add the smallest durable control that would have
   prevented or detected the incident sooner.

## Leaked Secret Runbook

```text
Example: Docker Hub publish token appears in a public workflow log
```

| Step | Action |
| --- | --- |
| Contain | Revoke the token in Docker Hub immediately |
| Investigate | Review registry pushes and GitHub workflow runs since issuance |
| Recover | Create a new repository-scoped publish token and update protected CI secret |
| Verify | Confirm authorized image digests; mark or remove untrusted image tags |
| Improve | Ensure workflow no longer echoes auth output and limits token scope |

Do not wait to remove the log before revoking the token. Exposure duration is
the meaningful risk.

## Suspicious Image or Supply-Chain Event

If a published image may not correspond to trusted source:

1. Stop promoting or deploying the tag.
2. Identify all deployed digests and compare them to known trusted builds.
3. Roll back or redeploy a verified immutable digest.
4. Review workflow modifications, action dependencies and registry activity.
5. Rotate credentials available to the affected build context when exposure is
   plausible.

## Communication and Records

A small project still benefits from a concise incident note:

```text
Date/time:
Reported by:
Affected asset:
Exposure or symptom:
Credential/artifact revoked or contained:
Evidence reviewed:
Recovery action:
Preventive follow-up:
```

Avoid recording live secret material in tickets, commits or public issue
threads. Public portfolio repositories may document the lesson after
sanitization without disclosing exploitable detail.

## Control Depth

**Personal/lab:** revoke, verify there was no production access, clean the
public artifact and record the fix.

**Production workload:** preserve audit evidence, determine impact, verify
artifacts and data exposure, and track corrective controls.

**Larger platform or regulated environment:** follow the organization's
incident process, legal/reporting obligations and evidence handling controls in
addition to this operational first response.
