# DevOps Checklist

Use this checklist when starting a maintained service, reviewing a delivery
system or selecting the next DevOps improvement. It is a compass, not a score:
record context and improve the most consequential constraint first.

## Purpose And Context

- [ ] The user or organizational outcome is stated.
- [ ] The service/system boundary and operating context are known.
- [ ] Risk, data value and production consequences are understood.
- [ ] Success evidence includes an outcome, not only completed technical work.
- [ ] Complexity and controls are proportional to real impact.

## Ownership And Collaboration

- [ ] Service, repository, platform and operational owners are identifiable.
- [ ] Development, security, quality and operation responsibilities are clear.
- [ ] Production feedback reaches people able to change priorities and the
  service.
- [ ] Handoffs have explicit input, owner, completion and feedback conditions.
- [ ] Important knowledge and privileged procedures do not depend on one
  undocumented person.
- [ ] Support, escalation and availability expectations fit actual capacity.

## Flow And Work In Progress

- [ ] The real path from need to production feedback is understood.
- [ ] Waiting, rework, queues and specialist dependencies are visible.
- [ ] Active work is limited enough to finish important changes.
- [ ] Changes are small, coherent and independently verifiable where practical.
- [ ] Branches are short-lived and integrated frequently.
- [ ] The current improvement targets an end-to-end constraint rather than a
  convenient local optimization.

## Validation And Delivery

- [ ] Consequential changes receive automated feedback before privileged work.
- [ ] Security and operability are reviewed during delivery, not only after it.
- [ ] The deployable artifact is attributable to source and validation.
- [ ] Production deployment uses controlled, minimal authority.
- [ ] Deployment verifies the real intended service path.
- [ ] Rollback, containment or recovery behavior exists for production change.
- [ ] Emergency delivery remains traceable and is reconciled afterward.

Apply the detailed [CI/CD Delivery Checklist](../ci-cd/delivery-checklist.md),
[Security Baseline Checklist](../security/baseline-checklist.md) and
[Testing Standards](../testing/README.md) where relevant.

## Operation And Recovery

- [ ] The running version and material configuration can be identified.
- [ ] User-affecting failure can be detected and investigated.
- [ ] Alerts route to an owner with authority or an escalation path.
- [ ] Production procedures state safety, access, verification and recovery.
- [ ] Valuable state has an explicit backup or reproducibility decision.
- [ ] Material incidents produce owned corrective or learning actions.
- [ ] Retired services remove access, automation, telemetry and cost safely.

Apply the detailed [Observability Checklist](../observability/observability-checklist.md),
[Infrastructure Checklist](../infrastructure/infrastructure-checklist.md) and
[Runbook Standards](../runbooks/README.md).

## Automation And Platform

- [ ] Automation has a defined user, outcome, owner and failure path.
- [ ] Privileged automation has minimal identity, useful evidence and a
  controlled change lifecycle.
- [ ] Human approval represents a meaningful decision with stated criteria.
- [ ] Repeated tickets or manual actions are reviewed for a safe self-service
  capability.
- [ ] A shared platform has real consumers and a maintained product contract.
- [ ] Supported paths provide secure and observable defaults.
- [ ] Exceptions and escape paths are explicit, owned and reviewable.
- [ ] Capability outcomes justify maintenance cost and shared blast radius.

## Measurement And Improvement

- [ ] Delivery measures use stable local definitions and service context.
- [ ] Throughput and instability are considered together.
- [ ] Metrics are used for improvement, not individual ranking or punishment.
- [ ] Delivery data is reviewed with user, reliability, security and
  sustainability evidence.
- [ ] The team can surface bad news, uncertainty and operational overload.
- [ ] Improvement work states a baseline, expected effect and review point.
- [ ] Retrospective and incident actions have owners and are followed through.
- [ ] Measurement effort is proportional to the decision it supports.

## SRE Adoption Trigger

Evaluate a dedicated SRE practice when one or more apply:

- [ ] User or business impact requires an explicit reliability objective.
- [ ] Availability, latency or correctness must be balanced against change
  velocity.
- [ ] On-call load or repeated operational work needs a sustainable policy.
- [ ] Capacity, overload or dependency risk requires continuous engineering.
- [ ] Several services need a consistent reliability review or support model.

Until a dedicated SRE standard exists, use the reliability guidance in
[Observability](../observability/README.md),
[Infrastructure](../infrastructure/README.md) and
[Runbooks](../runbooks/README.md).

## Improvement Record

```text
System/service:
Operating context:
Outcome to improve:
Observed constraint or risk:
Baseline and known limitations:
Selected change:
Expected effect and guardrails:
Owner:
Review date or trigger:
Result and next decision:
```

## Exception Record

```text
Standard not applied:
System/service and environment:
Reason and constraint:
User/delivery/operational consequence:
Compensating measure:
Owner:
Review or removal date:
```
