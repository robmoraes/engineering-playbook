# Service-Level Management

Service-level management turns reliability from a vague expectation into a
measurable product and engineering decision. Start with a small number of
user-relevant objectives and improve them from production evidence.

## Core Terms

| Term | Meaning in this playbook |
| --- | --- |
| Service level indicator (SLI) | A measured proportion or distribution representing user/dependent behavior |
| Service level objective (SLO) | The target for an SLI over a stated evaluation window |
| Error budget | The permitted amount of behavior outside an SLO target during its window |
| Burn rate | How quickly error budget is being consumed relative to the sustainable rate |
| Service level agreement (SLA) | An external or contractual commitment with stated consequences; not created by an internal SLO alone |

An SLO is an internal decision tool. Do not publish or imply an SLA without
the business, legal, support and measurement authority to make that
commitment.

## Start With The Journey

For each selected critical journey, ask:

```text
Who depends on the behavior?
Where does the journey begin and end?
What result is good enough to count as success?
Which latency, freshness, durability or correctness boundary matters?
What failure is visible to the user/dependent?
Can the behavior be measured at or near that perspective?
```

Prefer a few objectives that change decisions. Do not assign an SLO to every
component, metric or endpoint.

## Define The SLI

Ratio-style SLIs use consistent good and eligible event definitions:

```text
SLI = good eligible events / total eligible events
```

Examples:

| Workload | Eligible event | Good event |
| --- | --- | --- |
| HTTP service | Valid request reaching the service boundary | Correct non-server-error response within threshold |
| Background job | Job accepted for processing | Completed correctly within expected delay |
| Data pipeline | Scheduled output expected | Complete and fresh output available by deadline |
| Storage/recovery | Required recovery validation | Data restored within integrity and time expectations |
| Internal platform | Supported provision request | Usable capability delivered within promised time |

Every SLI MUST define:

- specification: the behavior that matters independent of tooling;
- implementation: query or measurement source;
- numerator and denominator, or distribution and threshold;
- eligibility and documented exclusions;
- aggregation dimensions and evaluation cadence;
- missing, delayed and partial-data behavior;
- owner and validation method.

```text
Good                                      Avoid
Checkout completed within 2 seconds      Pod CPU below 80%
Job output fresh before business cutoff  Worker process is running
Eligible 5xx and timeout behavior stated Count only failures that reached one backend
```

Infrastructure signals explain causes and imminent risk. They rarely replace
the journey SLI.

## Choose Target And Window

An SLO definition includes:

```text
Service and journey:
SLI specification:
SLI implementation/source:
Target:
Window: rolling | calendar
Window duration:
Exclusions:
Owner and stakeholders:
Error-budget policy:
Review trigger/date:
```

Choose the target from user need, dependency behavior, support capacity, cost
and acceptable risk. Do not copy `99.9%` because it is familiar, derive a
target solely from current performance or silently promise `100%`.

Prefer a rolling window for ongoing operational decisions. Use a calendar
window when it aligns with an explicit reporting or contractual cycle. The
window must be long enough to represent real use and short enough to change a
decision.

## Calculate Error Budget

For a ratio SLO:

```text
Allowed bad-event ratio = 1 - SLO target
Allowed bad events       = eligible events * allowed bad-event ratio
Budget consumed          = observed bad events / allowed bad events
Burn rate                 = observed bad-event ratio / allowed bad-event ratio
```

Example:

```text
SLO: 99.5% successful eligible checkout requests over 30 rolling days
Eligible requests: 200,000
Allowed bad-event ratio: 0.5%
Allowed bad events: 1,000
Observed bad events: 250
Budget consumed: 25%
Budget remaining: 75%
Burn rate over this observation range: 0.25x
```

Time-based availability tables can help communicate outage equivalents, but
event-based objectives often represent partial failure and user distribution
more accurately.

## Error-Budget Policy

The policy is agreed before the budget is under pressure:

| State | Default decision |
| --- | --- |
| Healthy consumption | Continue normal controlled delivery and reliability work |
| Abnormal burn | Investigate the cause, validate measurement and protect the remaining budget |
| At risk of exhaustion | Reduce risky change, prioritize the dominant reliability work and increase verification |
| Exhausted or SLO missed | Pause nonessential risk-increasing change until exit criteria are met or an authorized exception is recorded |
| Measurement unreliable | Repair the measurement; use conservative risk controls without pretending the budget is healthy |

Security remediation, active incident mitigation and changes that reduce known
reliability risk may proceed while a budget is exhausted. The policy must say
who decides, how emergency work is verified and which exit criteria restore
normal delivery.

An error budget is not:

- permission to cause avoidable failures;
- a target to consume recklessly;
- a performance score for an individual;
- a substitute for incident judgment;
- a reason to hide valid exclusions or missing telemetry;
- automatically a total release freeze.

## Alert On Budget Risk

For sufficient traffic, prefer burn-rate alerts that detect material fast and
slow consumption of the error budget. Use multiple windows where that improves
precision, recall, detection time and reset behavior.

A burn rate of `1x` consumes budget at the maximum sustainable rate across the
SLO window. A rate above `1x` consumes it faster; paging thresholds should
represent enough projected consumption to require prompt intervention.

Practical routing:

| Condition | Response |
| --- | --- |
| Fast material burn threatening the window | Page with SLO, dashboard and runbook context |
| Slow persistent burn that allows planned action | Ticket or owned reliability work |
| Budget trend without actionable condition | Dashboard/review signal |
| Telemetry failure invalidating SLO decisions | Alert according to the risk of blindness |

Thresholds and windows MUST be derived from the SLO and response capability,
not copied unchanged from an example. Alert implementation follows
[Observability: Metrics, SLOs and Alerts](../observability/metrics-slos-and-alerts.md).

## Low-Volume And Batch Services

One failure can create an extreme rate in a low-volume service. Consider:

- longer evaluation windows;
- explicit bad-event counts alongside ratios;
- synthetic critical-journey checks;
- deadline/freshness objectives for batch work;
- grouping services only when users and failure modes are meaningfully shared;
- a lower target when prompt response would not change user impact.

Do not page on a mathematically large burn rate when no responder can take a
useful immediate action.

## SLO Example

```text
Service: orders-api
Journey: submit checkout
SLI specification: proportion of eligible checkouts completed correctly
  within 2 seconds
SLI implementation: edge request outcomes joined to application completion
  metric; requests rejected for invalid client input are ineligible
Target/window: 99.5% over 30 rolling days
Owner: orders service owner
Known gap: client abandonment before edge receipt is not measured
Policy: fast material burn pages; slow burn creates reliability work;
  exhausted budget restricts nonessential risk-increasing releases
Review: quarterly or after a material checkout/telemetry change
```

## Review And Retirement

Review an SLO when the journey, traffic, architecture, support model,
measurement source or user expectation changes. At each review, ask:

- Did the SLO change a delivery or reliability decision?
- Are exclusions still legitimate and observable?
- Does the target represent user need rather than current accident?
- Are alerts actionable and proportionate?
- Is measurement trustworthy during partial and total failure?
- Should the SLO be revised, replaced or retired?

An unused SLO creates false confidence. Remove it deliberately along with its
alerts and dashboards when the journey or service retires.
