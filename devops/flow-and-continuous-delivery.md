# Flow And Continuous Delivery

Flow is the movement of a useful change from an identified need through
implementation, validation and production feedback. Improve the whole path,
including recovery, rather than making one stage faster while work accumulates
elsewhere.

## Make The Value Stream Visible

For an important service, sketch the actual path rather than the intended
process:

```text
need -> ready work -> implementation -> review -> validation
     -> artifact -> approval -> deployment -> verification -> feedback
```

Record enough evidence to expose constraints:

```text
Step:
Active work time:
Wait time:
Queue or WIP:
Owner:
Entry/completion condition:
Failure/rework route:
```

Include waiting, approval, environment provisioning, security review and
recovery work. Excluding another team's queue produces a local view, not an
end-to-end value stream.

Use value-stream mapping when the delivery path is unclear or materially slow.
Do not require a detailed map for every small repository when the constraint is
already visible and the team can act on it.

## Work In Small Batches

Prefer the smallest change that can produce useful evidence or safely move a
larger outcome forward. Small batches normally:

- reduce review and integration complexity;
- shorten the time before feedback;
- limit the scope of failure;
- make rollback or correction easier;
- reduce the amount of unvalidated work;
- allow priorities to change with less discarded effort.

A small diff is not automatically a safe batch. Database migrations, protocol
changes and security-boundary changes may need compatibility stages even when
few lines change. Split by independently verifiable behavior and recovery
boundary, not by arbitrary file or ticket counts.

```text
Good                                      Avoid
Add compatible field before using it     One release changes schema and every consumer
Merge an inactive code path safely       Long-lived branch hiding weeks of integration
Review one coherent behavior             Tiny commits with no independently useful intent
```

## Limit Work In Progress

Starting more work does not guarantee more completed value. Make active and
waiting work visible, set a WIP limit appropriate to available capacity and
help remove the current constraint before opening more parallel work.

WIP limits are diagnostic. When work blocks:

1. Keep the blocked state visible.
2. Identify the missing decision, environment, evidence or capability.
3. Collaborate across the constraint where possible.
4. Improve the process that caused the wait.
5. Adjust the limit only when capacity or workflow has actually changed.

Do not use WIP limits to conceal urgent security, incident or support work.
Account for that demand when evaluating delivery capacity.

## Integrate Continuously

Continuous integration is a working practice, not merely a CI server. The
default is:

- one shared mainline representing an integrated working state;
- small changes merged frequently through short-lived branches;
- automated validation on every consequential change;
- fast feedback for deterministic failures;
- repair of a broken mainline before unrelated delivery continues.

Feature flags or compatible intermediate states may keep incomplete behavior
inactive while code remains integrated. Flags need an owner and removal
condition; permanent flag accumulation is deferred complexity.

Branching and workflow implementation are defined in
[GitHub Branching Strategies](../github/branching-strategies.md) and
[CI/CD Standards](../ci-cd/README.md).

## Distinguish Integration, Delivery And Deployment

| Practice | Working expectation |
| --- | --- |
| Continuous integration | Changes join the shared mainline frequently and receive automated feedback |
| Continuous delivery | The integrated system remains in a releasable state and can be deployed through a repeatable path on demand |
| Continuous deployment | Every change satisfying the defined controls proceeds automatically to production |

Continuous deployment is optional. Continuous delivery is the stronger
general baseline because it preserves a deployable state while allowing
explicit approval where user impact, migration risk, regulation or business
timing requires judgment.

The detailed delivery path must follow
[Pipeline Principles](../ci-cd/pipeline-principles.md): validate before
privileged action, build once, promote the same immutable artifact, verify the
real service path and retain recovery behavior.

## Treat Security And Quality As Flow

Security and quality controls belong in the delivery system, with feedback as
early as practical:

| Control | Early feedback | Later or continuous feedback |
| --- | --- | --- |
| Correctness | Local tests, review, CI validation | Smoke, synthetic and user behavior |
| Security | Dependency/secret checks, threat-aware design | Artifact/runtime scanning and incident signals |
| Operability | Health, telemetry and runbook review | Deployment verification and production diagnosis |
| Architecture | Compatibility and decision review | Runtime evidence and evolutionary review |

Moving a control earlier does not mean running every expensive or privileged
check on a developer workstation or untrusted pull request. Place it at the
earliest stage with the necessary fidelity and safe authority.

## Include The Recovery Stream

The normal delivery stream and the recovery stream use many of the same
capabilities:

```text
signal -> assess -> corrective change or rollback -> validate
       -> deploy/execute -> verify recovery -> learn
```

If urgent recovery bypasses source history, validation, artifact trust or
deployment controls, the delivery system is incomplete. Emergency paths may
use different approvals, but they still need narrow authority, traceability
and post-action reconciliation.

Recovery procedures are defined in [Operational Runbooks](../runbooks/README.md).

## Improve The Constraint

Prefer one measurable improvement to a broad transformation program:

1. State the outcome that is being delayed or placed at risk.
2. Observe the current value stream and find its material constraint.
3. Establish a lightweight baseline.
4. Change one controllable part of the system.
5. Verify flow, quality and operational consequences.
6. Keep, revise or reverse the change from evidence.
7. Repeat with the next important constraint.

Automation that makes a non-constraint faster may add maintenance cost without
improving delivery. Optimize where work actually waits, fails or requires
rework.

## Flow Review Questions

- Can one ordinary change reach production without undocumented intervention?
- How much elapsed time is active work versus waiting?
- Where are approvals, environments or specialist knowledge scarce?
- Is work split into independently reviewable and recoverable increments?
- Does urgent recovery use a trusted and practiced delivery path?
- Are security, quality and operations producing actionable feedback early?
- Did the last process improvement change the end-to-end outcome?
