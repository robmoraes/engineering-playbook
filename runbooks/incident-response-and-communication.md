# Incident Response and Communication

Incident response should minimize user impact while preserving enough
information to restore service safely and prevent repeat failure.

## Severity Model

Adapt thresholds to service impact. Keep classification simple enough to use
under pressure.

| Severity | Example impact | Response expectation |
| --- | --- | --- |
| `SEV-1` Critical | Broad production outage, active data loss/corruption, major security exposure or inability to recover critical service | Immediate coordination, mitigation, stakeholder communication and escalation |
| `SEV-2` High | Material degradation, partial outage, failed critical deployment or recovery risk with meaningful users affected | Prompt owner response, timeline and managed resolution |
| `SEV-3` Moderate | Limited degradation, non-critical production issue or recoverable operational failure | Track, investigate and resolve during appropriate support window |
| `SEV-4` Low | Lab/non-production issue or informational operational improvement | Normal backlog or maintenance workflow |

Do not under-classify an active secret leak or irreversible data risk merely
because user-visible outage has not yet appeared.

## First Response Workflow

1. **Acknowledge and classify.** Record initial symptom, environment, time,
   affected service and preliminary severity.
2. **Confirm impact.** Use user-facing check, SLI/dashboard or trustworthy
   evidence; distinguish suspected from confirmed scope.
3. **Assign ownership.** For material incidents, name an incident coordinator
   and technical responder; one person may perform both roles for a small
   service.
4. **Preserve evidence.** Record deploy/version, alerts, status, logs/events
   and known changes before mutating state where safe.
5. **Mitigate or contain.** Roll back, fail over, reduce traffic, revoke a
   credential or apply another documented control.
6. **Verify recovery.** Confirm actual service/security/data condition.
7. **Communicate resolution and follow-up.** Preserve timeline and create
   corrective work proportionate to impact.

## Roles by Scale

| Context | Roles |
| --- | --- |
| Personal/small system | One responder may coordinate, diagnose and communicate, but still keeps timeline and action notes |
| Team production incident | Incident coordinator, technical responder/operations lead and communication owner where user impact warrants it |
| Critical/enterprise incident | Dedicated command, operations, communications and subject matter roles according to organizational process |

Avoid multiple operators applying changes independently without a shared
timeline or decision owner.

## Escalation Criteria

Escalate when:

- the incident is or may become `SEV-1`;
- production data loss, corruption or confidentiality risk exists;
- recovery requires destructive state action or unknown compatibility;
- control plane, cloud account, DNS/TLS authority or secret store is impaired;
- mitigation fails or impact grows after first response;
- external provider/support or business communication is required;
- responder lacks authority, access or system knowledge to act safely.

## Timeline Record

Keep a plain, timestamped record in UTC or explicitly stated timezone:

```text
Incident: INC-2026-005-orders-api-errors
Severity: SEV-2
Status: investigating | mitigated | resolved | follow-up
Owner/Coordinator:
Affected environment/service:

2026-05-24T13:42:00Z Alert fired: elevated 5xx for orders-api prod.
2026-05-24T13:45:00Z Confirmed public checkout failures after digest sha256:...
2026-05-24T13:49:00Z Decision: rollback; migration compatibility confirmed.
2026-05-24T13:54:00Z Prior digest running; health and smoke checks pass.
2026-05-24T14:05:00Z Error rate recovered; incident resolved.
```

Record decisions and effects; do not paste secrets or uncontrolled sensitive
payloads.

## Operational Communication

| Audience | Communicate |
| --- | --- |
| Responders | Facts, current severity, decisions, ownership and next action |
| Service stakeholders/users | Impact, workaround if any, update cadence and restoration status |
| Security/platform owners | Exposure/authority affected and containment needs |
| Post-incident readers | Timeline, cause, mitigation and preventive actions |

For a personal portfolio service, communication may be a private incident note
plus an accurate public status statement where users were affected. Do not
publish internal access details or exploitable failure evidence.

## Temporary Mitigation and Resolution

A mitigation reduces impact but may leave risk:

```text
Mitigation: rollback application digest to restore API behavior.
Remaining issue: faulty release blocked; root cause unresolved.
Resolution: corrected release deployed and verified, with regression test added.
```

Mark an incident resolved only after:

- user or protected asset condition is verified;
- emergency access/change state is understood;
- remaining risk is assigned or explicitly accepted;
- follow-up owner exists for material corrective actions.

## Post-Incident Review

Conduct a postmortem for serious impact, repeated failure, data/security risk
or valuable operational learning. Focus on system improvement rather than
assigning blame:

- impact and detection;
- timeline and contributing factors;
- root and contributing causes;
- what worked and delayed recovery;
- temporary versus permanent fixes;
- action items with owner and priority;
- runbook, monitoring or readiness updates.

Use the template in [Templates and Checklists](./templates-and-checklists.md).
