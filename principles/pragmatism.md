# Pragmatism Without Negligence

## Build What The Problem Requires

Pragmatism means selecting an adequate solution for real constraints: user
need, risk, time, cost, skills and operating capacity. It does not mean
shipping whatever is fastest regardless of consequences.

A small library system that makes books findable can be more valuable than a
large platform solving an assumed problem. Scale, novelty and architectural
complexity are not proxies for usefulness.

## Simplicity Is A Discipline

Simple software is not careless software. A simple solution has fewer moving
parts because unnecessary ones were deliberately excluded while essential
responsibilities remained:

- validate important input;
- protect sensitive information;
- preserve or recover important state;
- report failure honestly;
- provide enough evidence to diagnose problems;
- document operation and known limits.

Simplicity reduces the number of ways a system can fail and the amount future
engineers must understand. It should be preferred until a measured limitation
justifies additional complexity.

## Proportionate Engineering

The right investment follows consequence, not fashion:

| Context | Appropriate posture |
| --- | --- |
| Disposable experiment with no sensitive data | Keep operation minimal; state assumptions clearly |
| Small persistent tool used by real people | Preserve data, secure access, test core workflows and document recovery |
| Internet-facing or business-dependent system | Automate delivery, observe behavior, prepare incidents and control changes |
| Critical or high-impact system | Define service objectives, isolate failures, test recovery and require stronger review |

Small does not mean unimportant. It means controls can be focused on the
actual risk instead of imitating a large organization.

## Tradeoffs And Debt

A deadline may require accepting debt. Treat it as a decision rather than an
accident:

- identify what was simplified or deferred;
- state the effect on users, operation or future change;
- choose a containment measure when risk is material;
- record when the decision should be revisited.

Debt that is visible can be prioritized. Debt hidden behind optimistic
language becomes a surprise borne by someone else.

## Resist Two Failures

Overengineering spends time, money and operating attention on complexity that
does not improve outcomes. Negligence avoids essential care by calling it
complexity. Professional pragmatism rejects both: do what is necessary,
explain what is not, and revise the decision when evidence changes.

For system-level tradeoffs, use [Architecture Standards](../architecture/README.md)
and its decision-record approach.
