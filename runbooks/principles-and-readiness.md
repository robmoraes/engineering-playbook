# Principles and Readiness

Runbooks are operating code written for a human or an automation system. A
procedure that is unclear, unsafe or obsolete during failure increases outage
duration and can create a second incident.

## Runbook Versus Playbook

| Document | Use |
| --- | --- |
| Runbook | Repeatable procedure for a known outcome, such as rollback a service or rotate an expired certificate |
| Investigation playbook | Guided diagnosis for ambiguous symptoms, such as elevated latency with several possible dependencies |

Both must identify ownership, access needs, safe checks, escalation and
verification. This repository uses `runbook` broadly for both forms, while
preserving the distinction when choosing automation depth.

## Operating Principles

### Stabilize Before Optimizing

During active impact, restore acceptable service or contain risk before
performing broad refactoring or speculative tuning.

```text
Good                                      Avoid
Roll back confirmed bad image            Tune unrelated database parameters mid-incident
Disable exposed credential promptly      Delay revocation for a perfect investigation
```

### Gather Evidence Before Mutation

Before restart, rollback, deletion, failover or restore, capture when feasible:

- symptom, time and affected environment;
- active release or infrastructure change;
- alert/dashboard snapshot or query result;
- relevant task/Pod/node status and logs;
- dependency and capacity state;
- action chosen and why.

Immediate containment can override evidence collection when ongoing security
exposure or data corruption risk is material. Record the reason afterward.

### Verify from the Intended Path

A successful command confirms only that the command ran. Validate recovery
through the actual route and operation at issue:

```text
Good                                      Avoid
External HTTPS health plus safe smoke    `docker ps` alone after rollback
Restore validation against test query    Backup job status alone
```

### Keep Changes Reversible Where Possible

Prefer actions with a known return path:

- restore prior immutable artifact;
- remove a bad instance from routing before deleting it;
- rotate credentials through overlapping replacement when no active leak is
  suspected;
- preserve backups before destructive repair.

## Runbook Minimum Structure

Every production procedure SHOULD include:

```markdown
# Summary
# Scope and Owner
# Symptoms
# Safety and Required Access
# Initial Assessment
# Diagnostics
# Mitigation or Recovery
# Validation
# Rollback or Escalation
# Evidence and Communication
# Prevention or Follow-Up
# Useful Commands
# References
```

Use a shorter structure for low-impact lab tasks only when the omitted
sections truly do not apply.

## Human Action Versus Automation

| Procedure | Automate first? | Reason |
| --- | --- | --- |
| Read-only health/status collection | Yes, where reliable | Reduces toil and preserves consistent evidence |
| Standard deployment verification | Yes | Repeatability improves release safety |
| Known safe rollback of compatible artifact | Often | Reduces recovery time if guards and validation exist |
| Secret revocation after confirmed exposure | Provider workflow/script useful; human decision may remain | Speed matters, but scope/impact must be known |
| Data restore or destructive failover | Carefully, with controls | Wrong target or version can increase loss |
| Ambiguous incident diagnosis | Assist, do not blindly automate | Requires interpretation of incomplete evidence |

Automation MUST expose its authority, input, outcome and failure behavior.
Automating an unsafe procedure only makes unsafe actions faster.

## Operational Readiness

Before a production service launches or changes materially, confirm:

- owners and escalation route exist;
- critical alerts lead to maintained runbooks;
- deployment and rollback path is known;
- secrets/credentials can be rotated or revoked;
- state has a recovery decision and restore steps where applicable;
- topology failures such as ingress, node or dependency loss can be
  distinguished;
- required production access is available through a protected path;
- at least one other maintainer, or a deliberate self-review for a personal
  system, has walked through critical steps.

## Runbook Lifecycle

| Event | Required update |
| --- | --- |
| Platform/service architecture change | Review commands, endpoints, dependencies and recovery path |
| New alert | Link a procedure or first-response path |
| Incident or failed exercise | Correct unclear or missing steps and track improvements |
| Credential/access model change | Replace authority requirements and secure access notes |
| Service retirement | Remove alert links, archive procedure or document successor |
