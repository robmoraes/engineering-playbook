# Infrastructure Checklist

Use this checklist when creating, reviewing, promoting or materially changing
infrastructure. Apply depth proportional to user impact and data value.

## Purpose and Boundaries

- [ ] Purpose, owner and operating context are stated.
- [ ] Edge, runtime, data, platform and management responsibilities are clear.
- [ ] Environment and access boundaries are deliberate.
- [ ] Known dependencies and shared-service blast radius are documented.
- [ ] A significant topology decision is recorded through an ADR where needed.

## Topology and Networking

- [ ] Diagram or topology description identifies public and private paths.
- [ ] Only required endpoints and ports are exposed.
- [ ] Data and management paths are not incidentally internet-accessible.
- [ ] Network segmentation reflects communication need.
- [ ] DNS, TLS, ingress/load balancing and discovery ownership are identified.
- [ ] Cross-zone/external traffic cost is understood where material.

## Runtime and Clusters

- [ ] Orchestrator choice is justified against simpler alternatives.
- [ ] Node/control-plane failure implications are known.
- [ ] Swarm manager quorum/backup or Kubernetes control-plane responsibility is
  documented where applicable.
- [ ] Scheduling, capacity, maintenance and upgrade procedures exist for
  multi-node infrastructure.
- [ ] Deployment uses identifiable artifacts and scoped authority.

## State and Recovery

- [ ] Stateful dependencies and data owners are identified.
- [ ] Storage choice matches concurrency, portability and durability needs.
- [ ] Valuable production data has protected automated backup or an explicit
  reproducibility decision.
- [ ] RPO/RTO or accepted recovery limitation is stated.
- [ ] Restore/recovery is documented and verified at an appropriate cadence.
- [ ] HA and backup are not confused as the same control.

## Provisioning and Security

- [ ] Repeatable production infrastructure is declared through maintained IaC
  or an explicit provider-controlled equivalent.
- [ ] IaC state, credentials and production change authority are protected.
- [ ] Production identities and secrets are isolated from non-production.
- [ ] Administrative access is restricted, attributable and recoverable.
- [ ] Manual emergency changes have a reconciliation path.

## Operability

- [ ] Health, capacity, ingress, state/backup and material control-plane
  behavior are observable.
- [ ] Alerts represent actionable operational impact or risk.
- [ ] Runbooks exist for failures requiring privileged action or judgment.
- [ ] Logs and telemetry avoid exposing secrets or sensitive topology
  unnecessarily.
- [ ] Troubleshooting and incident follow-up paths are understood.

## Cost and Lifecycle

- [ ] Availability/redundancy decisions identify protected failure domains and
  cost.
- [ ] Resource sizing, storage retention and data transfer cost have review
  signals where material.
- [ ] Patching, upgrade and deprecation ownership are known.
- [ ] Retirement removes resources, access and unnecessary spend safely.
- [ ] Public diagrams/examples are sanitized and do not overstate production
  capability.

## Exception Record

When a baseline does not apply, record:

```text
Infrastructure/system:
Standard not applied:
Reason and tradeoff:
Operational or security impact:
Interim control:
Owner:
Review date or retirement condition:
```
