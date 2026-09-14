# Feedback, Measurement And Learning

Feedback is useful when it reaches someone who can change the outcome while
the context is still available. Measurement supports judgment; it does not
replace user understanding, technical investigation or accountable decisions.

## Design Feedback Loops

Use several loops because no single signal describes the delivery system:

| Loop | Expected timing | Question answered |
| --- | --- | --- |
| Change | Minutes | Is the change internally consistent and safe to integrate? |
| Delivery | Each candidate/deployment | Was the intended artifact delivered and verified? |
| Operation | Continuous or risk-based | Is the service behaving safely for users and operators? |
| Product/user | Appropriate usage cadence | Did the change improve the intended outcome? |
| Team/process | Regular and event-driven | What is slowing, harming or repeatedly surprising the work? |

Fast incorrect feedback is not useful. Keep each loop trustworthy, actionable
and proportionate to the decision it informs.

## Software Delivery Performance

This playbook adopts DORA's current five-metric model as a high-level view of
software delivery throughput and instability:

| Factor | Metric | Local interpretation | Improvement use |
| --- | --- | --- | --- |
| Throughput | Change lead time | Elapsed time from change committed to successful production deployment | Expose queues, slow validation and oversized changes |
| Throughput | Deployment frequency | How often the service is successfully deployed in a period | Understand batch and release behavior |
| Throughput | Failed deployment recovery time | Time to restore acceptable service after a deployment requires intervention | Evaluate detection, rollback and corrective delivery |
| Instability | Change fail rate | Proportion of deployments requiring immediate remediation, rollback or hotfix | Improve change safety and verification |
| Instability | Deployment rework rate | Proportion of deployments that are unplanned responses to production incidents | Expose delivery capacity consumed by instability |

Definitions must be recorded with the measurement because deployment and
failure semantics vary. Use the application or service as the primary context,
compare it with its own history and review the current DORA reference before
changing the model.

Failed deployment recovery time measures recovery from a failed change. It is
not a substitute for measuring recovery from infrastructure, dependency,
security or other incidents. Detailed service reliability measurement belongs
to [SRE: Service-Level Management](../sre/service-level-management.md).

## Measurement Guardrails

- Use the metrics together; optimizing one can damage the system.
- Do not set an arbitrary deployment-frequency target without an outcome.
- Do not compare unrelated services, teams or technology contexts as a league
  table.
- Do not attribute a team-level system measure to individual performance.
- Do not sacrifice security, validation or recovery to improve a number.
- Prefer a useful approximate baseline to an expensive measurement platform
  that delays improvement.
- Automate collection when its decision value justifies implementation and
  maintenance cost.
- Review definitions when tools, deployment models or service boundaries
  change.

```text
Good                                      Avoid
Compare one service before/after change  Rank engineers by deployment count
Review throughput with instability       Optimize lead time while failures rise
Record known data limitations            Present false precision from incomplete events
```

## Balance Delivery With Outcomes

Delivery metrics describe the change process, not whether the product is
valuable or the service is reliable. Review them alongside evidence such as:

- user success, failure and support signals;
- test effectiveness and escaped defects;
- security findings and exposure;
- service behavior and reliability objectives;
- operational load and repeated manual work;
- cost and resource consumption;
- team sustainability and ability to learn.

A faster delivery process that increases user harm, unplanned work or operator
load is not an improvement.

## Build A Learning Culture

A learning culture makes important information safe to surface and useful to
act upon:

- seek bad news early;
- share risks across the lifecycle;
- treat failure as a reason for inquiry, not automatic blame;
- document uncertainty and conflicting evidence;
- allow reversible experiments within explicit safety boundaries;
- convert recurring friction into owned improvement work;
- share learning through code, documentation, reviews and automation.

Blameless does not mean consequence-free or technically vague. Reviews should
identify decisions, conditions, missing defenses and corrective actions while
distinguishing honest error from reckless or malicious behavior.

Material incident review follows the
[Runbook Post-Incident Standard](../runbooks/incident-response-and-communication.md).

## Run Improvement As An Experiment

Use a small evidence loop:

```text
Outcome:
Observed constraint or risk:
Baseline and limitations:
Proposed change:
Expected effect and guardrails:
Owner and review date:
Result:
Decision: keep / revise / reverse
```

Suggested sequence:

1. Choose one user, delivery or operational outcome.
2. Map enough of the system to identify the material constraint.
3. Establish a lightweight baseline.
4. Implement one bounded improvement.
5. Observe intended and unintended effects.
6. Standardize successful learning or reverse the change.
7. Select the next constraint.

Retrospectives without owned action become ceremony. Metrics without a
decision become inventory. Each review should conclude with an accepted state
or a small number of prioritized actions.

## Suggested Review Cadence

| Trigger | Review |
| --- | --- |
| Each production change | Deployment result, verification and immediate regression |
| Repeated or material failure | Incident learning, defenses and recovery path |
| Regular team interval | Flow constraints, WIP, delivery measures and improvement actions |
| Material delivery/platform change | Baseline, consumer effect, access and recovery consequences |
| Service lifecycle change | Ownership, operating expectation, telemetry and retirement work |

Cadence is proportional. A personal lab may review after a meaningful change;
a production team may review flow and operations weekly. The important control
is that evidence reaches a decision and decisions reach owned work.

## Feedback Review Questions

- Which feedback can stop or correct a risky change earliest?
- Can the service owner connect a production symptom to the deployed change?
- Are metrics exposing a constraint or merely reporting activity?
- What improvement decision changed because of this measurement?
- Are people safe to surface failure, uncertainty and operational overload?
- Did a previous incident or retrospective action actually close?
