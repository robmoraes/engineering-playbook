# Service Reliability Record - SERVICE_NAME

> Copy this file to `docs/operations/service-reliability.md`. Replace
> placeholders with evidence, use `Not applicable` only with a reason and link
> authoritative implementation artifacts instead of duplicating them.

## Identity And Purpose

- **Service:** SERVICE_NAME
- **Repository:** REPOSITORY_LINK
- **Runtime/environment:** RUNTIME_AND_ENVIRONMENT
- **Lifecycle:** experimental | maintained | production | retiring
- **Reliability context:** learning/lab | maintained | production | critical |
  shared platform
- **Purpose and users/dependents:** PURPOSE_AND_CONSUMERS
- **Critical journey(s):** ENTRY_POINT, SUCCESS_OUTCOME_AND_FAILURE_BOUNDARY

## Ownership And Support

- **Service owner:** OWNER
- **Technical escalation:** ESCALATION_ROUTE
- **Support window:** best effort | BUSINESS_HOURS_AND_TIMEZONE | 24x7
- **Alert destination:** ALERT_ROUTE_OR_NOT_APPLICABLE_REASON
- **Change authority:** ROLE_OR_APPROVAL_PATH
- **Last reviewed:** YYYY-MM-DD

Do not select 24x7 unless a staffed, trained and sustainable response model
exists.

## Service-Level Management

### SLO: JOURNEY_NAME

- **SLI:** GOOD_EVENTS / ELIGIBLE_EVENTS at MEASUREMENT_BOUNDARY
- **Good event:** GOOD_EVENT_DEFINITION
- **Eligible event:** ELIGIBLE_EVENT_DEFINITION
- **Exclusions:** EXCLUSIONS_AND_REASON
- **Target/window:** TARGET over WINDOW
- **Data source:** QUERY_DASHBOARD_OR_RECORDING_RULE
- **Owner:** OWNER
- **Known measurement gaps:** GAPS_OR_NONE_KNOWN

### Error-Budget Policy

| State | Evidence | Change/response decision |
| --- | --- | --- |
| Healthy | LOCAL_CONDITION | NORMAL_RISK_POLICY |
| At risk | LOCAL_CONDITION | TIGHTER_VERIFICATION_AND_RELIABILITY_WORK |
| Exhausted | LOCAL_CONDITION | RESTRICT_NONESSENTIAL_RISK_INCREASING_CHANGE |

If no numerical SLO is justified, record the user consequence, available
health evidence, reason for the exception and review trigger.

## Architecture And Dependencies

- **Entry point:** ENTRY_POINT
- **Critical dependencies and owners:** DEPENDENCIES_AND_OWNERS
- **Persistent state and owner:** STATE_AND_DATA_OWNER
- **Failure/degradation behavior:** FAILURE_BOUNDARIES_AND_USER_BEHAVIOR
- **Capacity or quota limit:** LIMITING_RESOURCE_AND_CURRENT_HEADROOM

For each critical dependency, capture behavior used, timeout/retry boundary,
failure or degradation, quota/capacity limit, detection and escalation.

## Delivery And Configuration

- **Artifact/configuration identity:** VERSION_DIGEST_AND_CONFIG_REFERENCE
- **Deployment and verification:** WORKFLOW_AND_CRITICAL_JOURNEY_CHECK
- **Rollback/containment/recovery:** TESTED_PATH_AND_LIMITATIONS
- **Feature flag or migration constraints:** CONSTRAINTS_OR_NOT_APPLICABLE_REASON

## Operations

- **Service dashboard:** DASHBOARD_LINK
- **Alerts:** ALERT_LINKS_OR_NOT_APPLICABLE_REASON
- **Runbooks:** RUNBOOK_LINKS
- **Incident coordination route:** INCIDENT_ROUTE

## Data And Disaster Recovery

- **Backup/reproducibility decision:** DECISION_AND_SCOPE
- **RPO/RTO or accepted limitation:** RPO_AND_RTO
- **Restore/recovery procedure:** PROCEDURE_LINK
- **Last validation and result:** DATE_EVIDENCE_AND_OBSERVED_BOUNDS
- **Next validation:** DATE_OR_CHANGE_TRIGGER

## Capacity And Reliability Validation

- **Demand unit, peak and growth:** DEMAND_MODEL
- **Tested safe capacity and limiting resource:** CAPACITY_EVIDENCE
- **Failure/maintenance reserve:** NAMED_SCENARIO_AND_HEADROOM
- **Reliability scenarios exercised:** SCENARIO_EVIDENCE
- **Next exercise:** DATE_OR_CHANGE_TRIGGER

## Toil And Sustainability

- **Recurring operational work:** TASK_FREQUENCY_AND_HANDS_ON_TIME
- **Accepted operations-work bound:** LOCAL_BOUND_AND_REVIEW_WINDOW
- **Dominant reduction candidate:** ELIMINATE_SIMPLIFY_OR_AUTOMATE_ACTION
- **Paging/support sustainability:** EVIDENCE_AND_LIMITATION

## Risks, Exceptions And Review

| Risk or unmet control | Consequence | Compensating control | Owner | Review/removal trigger |
| --- | --- | --- | --- | --- |
| RISK | CONSEQUENCE | CONTROL | OWNER | DATE_OR_TRIGGER |

- **Next record review:** DATE_OR_CHANGE_TRIGGER
- **Approval/acknowledgement:** ACCOUNTABLE_OWNER_AND_DATE
