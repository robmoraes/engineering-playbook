# On-Call, Incidents And Learning

Human response is a constrained reliability control. Use it only when timely
judgment can materially reduce impact, and design it so that responders can
act safely without relying on heroics.

## Declare The Support Model

Every production service MUST state one support model:

| Model | Expectation |
| --- | --- |
| Best effort | No guaranteed response time; alerts may be reviewed when a maintainer is available |
| Business hours | Owned response during stated hours and timezone; outside-hours impact is an accepted limitation or uses another provider |
| 24x7 on-call | A staffed rotation acknowledges and responds at all times under a sustainable policy |
| Provider/platform supported | A provider owns part of response; application escalation and shared boundaries remain explicit |

A notification channel does not create 24x7 support. Do not route urgent pages
to a person who has not accepted a shift or cannot access the response path.

## Preconditions For 24x7 On-Call

Before claiming 24x7 response, define:

- primary and backup coverage with no silent gaps;
- shift length, handoff and escalation;
- acknowledgement and response expectations derived from service need;
- compensation or organizational treatment of out-of-hours work;
- trained responders with safe production access;
- current dashboards, runbooks and communication channels;
- workload measurement and a threshold for operational overload;
- illness, leave and rotation-change coverage;
- time for incident follow-up and reliability engineering.

A single maintainer cannot provide a sustainable 24x7 rotation. Choose an
honest support window, reduce service commitments, use supported managed
capabilities or add staffed coverage.

Google's staffing ratios and operational-work limits are useful evidence from
its context, not universal numeric mandates for this playbook.

## Page Only For Action

Use the least disruptive route that matches urgency:

| Signal | Route |
| --- | --- |
| Immediate human action can prevent or reduce material impact | Page |
| Action is needed within a planned period | Ticket/owned work |
| Evidence is useful only when investigating another signal | Log, metric, trace or event |
| No action or decision follows | Remove or redesign the signal |

Prefer symptom- or SLO-based paging. Component alerts may page when they
predict imminent irreversible harm, such as capacity exhaustion or loss of the
last safe replica.

Every page SHOULD include:

```text
Service/environment and owner:
User/dependent symptom:
Severity or budget risk:
Current value and alert condition:
Dashboard/query:
Runbook or safe first action:
Recent change evidence:
Escalation route:
```

An alert that routinely requires no action is a defect. Repeated paging for
the same cause is reliability debt and operational toil.

Alert implementation follows
[Observability: Metrics, SLOs and Alerts](../observability/metrics-slos-and-alerts.md).

## Responder Readiness

Before joining a response rotation, an engineer SHOULD be able to:

- explain the critical journey and major dependencies;
- locate current service/release and SLO state;
- use read-only diagnosis before mutation;
- execute or escalate the common mitigations;
- distinguish rollback, containment, failover and permanent repair;
- obtain emergency authority through the approved path;
- declare an incident and communicate status;
- identify when personal uncertainty or fatigue requires help.

Use shadow shifts and rehearsed scenarios before unsupported primary duty. An
access grant without service knowledge is not readiness.

## Declare And Structure Incidents

Declare an incident when impact, coordination or uncertainty exceeds routine
single-owner handling. Early declaration is reversible; delayed coordination
can increase harm.

Scale roles to the incident:

| Role | Responsibility |
| --- | --- |
| Incident commander | Maintains high-level state, priorities, roles and escalation |
| Operations lead | Coordinates controlled diagnosis and service changes |
| Communications lead | Provides regular stakeholder/user updates |
| Scribe/planning | Maintains timeline, decisions, actions, handoff and divergence from normal state |
| Subject expert | Investigates a delegated service or failure domain and reports evidence |

One person may hold several roles in a small incident. Make the active owner
and next update visible even when no formal response team exists.

Severity, communication and detailed records follow
[Runbooks: Incident Response and Communication](../runbooks/incident-response-and-communication.md).

## Incident Survival Workflow

```text
1. Acknowledge and assume or assign ownership.
2. Confirm the user, data or operational impact.
3. Identify current release/configuration and recent material changes.
4. Declare severity and coordination roles when needed.
5. Preserve enough evidence before mutation where safe.
6. Stop uncontrolled concurrent change.
7. Choose the safest known mitigation or containment.
8. Verify the affected journey and remaining risk.
9. Communicate status, decisions and next update.
10. Reconcile emergency state and assign follow-up.
```

During active impact, stabilize before speculative optimization. If the last
change is a plausible cause and rollback is compatible, a tested rollback is
often safer than debugging while users remain affected.

Security exposure, active data corruption or safety impact may require
immediate containment before full evidence collection. Record what was lost
and why.

## Control Changes During Response

- Use one operations lead to coordinate production mutation.
- Announce action, expected effect and stop condition before execution where
  time permits.
- Prefer reversible actions and narrow blast radius.
- Record commands/workflows and results in the incident timeline.
- Do not combine unrelated cleanup or optimization with mitigation.
- Verify through the impacted path after each material action.
- Preserve or document temporary divergence from versioned state.
- Require explicit handoff when the executing owner changes.

Detailed diagnostic and safe-execution procedures are in
[Operational Runbooks](../runbooks/README.md).

## Communication Minimum

An incident update states:

```text
Time and severity:
Observed impact:
Current state:
Mitigation performed or in progress:
What is not yet known:
Next decision/update time:
Incident owner/contact:
```

Separate confirmed fact from hypothesis. Do not publish sensitive data,
credentials, exploitable detail or unsupported resolution estimates.

## Resolution And Handoff

Resolve an incident only when:

- the user/dependent or protected asset condition is verified;
- temporary changes and emergency access are understood;
- remaining risk is accepted or assigned;
- follow-up ownership exists for material work;
- monitoring is stable enough to detect recurrence.

Mitigation restores acceptable behavior. Resolution completes necessary
reconciliation and ownership. Root cause and permanent repair may follow when
they cannot be established safely during response.

## Learn From Failure

Perform a postmortem for serious impact, repeated failure, unexpected error
budget consumption, data/security risk, difficult recovery or valuable new
learning.

A useful postmortem identifies:

- user and service impact;
- detection and response timeline;
- technical and organizational contributing conditions;
- what limited or amplified impact;
- what helped or delayed diagnosis and recovery;
- temporary and permanent corrective actions;
- owners, priority and completion evidence;
- runbook, alert, test and readiness updates.

Blameless review rejects scapegoating; it does not conceal decisions or remove
accountability for corrective action. Address systemic defenses and distinguish
honest error from reckless or malicious behavior.

Use the existing
[Postmortem Template](../runbooks/templates-and-checklists.md#postmortem-template).

## Practice And Sustainability

- Rehearse common incidents and role transitions.
- Validate paging, access and escalation periodically.
- Review pages per shift, sleep interruption, tickets and follow-up load.
- Protect engineering time to remove recurring causes.
- Reduce commitments or add capacity when response is not sustainable.
- Rotate knowledge without forcing unsafe unsupported duty.

Do not rank responders by incident count or recovery speed without context.
Incident measures evaluate the response system and user impact, not personal
worth.
