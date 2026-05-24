# Templates and Checklists

These templates are intentionally concise. Extend them for a specific service
when state, compliance, user communication or platform complexity requires it.

## Runbook Template

````markdown
# <Procedure Name>

## Summary

Goal:
Applies to:
Owner:
Last validated:

## Symptoms

- <symptom or trigger>

## Safety and Required Access

- Environment(s):
- Required role/tooling:
- Risk of action:
- Stop/escalation condition:

## Initial Assessment

1. <initial read-only verification>

## Diagnostics

```bash
# Read-only commands first
```

## Root Cause or Decision Point

Evidence required before mitigation:

## Mitigation or Recovery

1. <approved action>

## Validation

- [ ] User/operational path recovered.
- [ ] Expected runtime/configuration state confirmed.
- [ ] Alerts/telemetry stabilized.

## Rollback or Escalation

- <rollback or escalation condition>

## Permanent Fix and Prevention

- <corrective action>

## Useful Commands

```bash
```

## References

- <reference or linked standard>
````

## Incident Record Template

```markdown
# INC-YYYY-NNN - <Short Symptom>

Severity:
Status:
Coordinator/owner:
Affected services/environments:
Start time/timezone:
Detection source:
User impact:

## Current Assessment

## Timeline

| Time | Observation, decision or action | Owner |
| --- | --- | --- |
| | | |

## Mitigation and Validation

## Communications

## Evidence Links

## Follow-Up Required
```

## Postmortem Template

```markdown
# Postmortem - <Incident>

## Summary

## Impact

## Detection

## Timeline

## Root Cause and Contributing Factors

## Resolution and Recovery Validation

## What Worked

## What Delayed Recovery

## Corrective Actions

| Action | Type: prevention/detection/mitigation/process | Owner | Priority/target |
| --- | --- | --- | --- |
| | | | |

## Runbook and Monitoring Updates

## References/Evidence
```

Postmortems SHOULD be blameless and technically specific. Identify systemic
conditions and controls that change future outcomes rather than attributing
failure to an individual performing normal work in a weak process.

## Production Recovery Verification Checklist

- [ ] Impacted route or SLI has recovered, not just process status.
- [ ] Expected release/configuration/secret reference is active.
- [ ] Dependent jobs, queues, storage or database state is healthy where
  relevant.
- [ ] Error/latency/resource telemetry shows stabilization.
- [ ] Temporary mitigation and residual risk are recorded.
- [ ] Emergency access or manual change is reconciled/reviewed.
- [ ] Follow-up owner exists for permanent correction.

## Operational Readiness Checklist

- [ ] Service owner and escalation route are documented.
- [ ] Deployment rollback/recovery and artifact identity are known.
- [ ] Public route, health, key telemetry and alerts are validated.
- [ ] Critical alerts link to useful runbooks.
- [ ] Data backup/restore ownership exists for durable state.
- [ ] Credentials can be revoked/rotated without copying values into docs.
- [ ] DNS/TLS/ingress and runtime/platform failure paths are understood.
- [ ] Procedures were reviewed or exercised after major topology change.

## Maintenance Checklist

- [ ] Runbook owner and last validation date remain current.
- [ ] Commands, service names, endpoints, dashboards and links still resolve.
- [ ] Access permissions and secret references still reflect current controls.
- [ ] Incidents or exercises have been incorporated.
- [ ] Obsolete procedures are archived or point to successors.
