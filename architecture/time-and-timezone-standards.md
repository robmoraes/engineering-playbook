# Time and Timezone Standards

Time handling is an architecture concern because it affects data correctness,
user trust, audit evidence, scheduling, integrations and incident response.
Global systems must distinguish an instant on the timeline from a local civil
date/time and from a user's display preference.

## Core Model

Use these concepts explicitly in code, schemas and API contracts:

| Concept | Meaning | Examples | Store as |
| --- | --- | --- | --- |
| Instant | One exact point on the global timeline | creation time, payment captured, log event | UTC timestamp / database instant type |
| Local date | Calendar date without time or timezone | birthday, due date, billing cycle date | date |
| Local time | Clock time without date or timezone | store opens at 09:00 | time |
| Zoned local date-time | Civil date/time governed by a named zone | meeting at 09:00 in Europe/Paris | local date-time + IANA timezone |
| Recurrence rule | Repeated civil schedule | every weekday at 08:00 in America/Sao_Paulo | rule + IANA timezone |
| Duration | Exact elapsed amount | retry after 30 seconds, token TTL | seconds/milliseconds or duration type |
| Calendar period | Human calendar amount | one month subscription, next business day | date arithmetic in target calendar/zone |

Do not collapse these concepts into one generic `datetime` field. Ambiguity is
the usual source of timezone defects.

## Non-Negotiable Defaults

- Persist instants in UTC using timezone-aware types. Do not store UTC values
  in timezone-naive fields.
- Use IANA timezone identifiers such as `America/Sao_Paulo`,
  `Europe/Lisbon` and `Asia/Tokyo` for user, tenant, venue or schedule zones.
- Do not use timezone abbreviations such as `EST`, `CST`, `BRT` or `IST` in
  persisted data or API contracts. They are ambiguous and change historically.
- API timestamps that represent instants MUST use RFC 3339 date-time strings
  with an explicit offset. Prefer UTC `Z` for generated system timestamps.
- Preserve the user's intended local date/time and IANA timezone for future or
  recurring events. A UTC instant alone is insufficient when timezone rules can
  change before the event occurs.
- Convert for display at the edge of the system using the viewer's selected
  timezone and locale. Do not let server, container or database session
  timezone silently define user-visible time.
- Keep application, database, container and CI default timezones at UTC unless
  a test or migration deliberately proves local-zone behavior.
- Update timezone data (`tzdata`, runtime images and language packages) as
  part of normal dependency maintenance.

## Layered Runtime Standard

For projects following this playbook, timezone flexibility belongs at the user
experience boundary. Servers, backend services, APIs, jobs, logs and storage
use UTC by default. The frontend may render and collect local civil time using
the user's selected timezone or, when appropriate, the browser-detected
timezone.

```text
User preference / browser timezone
              |
              v
+-------------------------------+
| Frontend / client UI          |
| - display in selected IANA TZ |
| - collect local intent + TZ   |
+---------------+---------------+
                |
                | API: instants as RFC 3339 UTC
                | API: local intent as date/time + IANA TZ
                v
+-------------------------------+
| Backend / APIs / jobs         |
| - default timezone: UTC       |
| - normalize instants to UTC   |
| - validate IANA TZ fields     |
| - compute schedules with TZ   |
+---------------+---------------+
                |
                | Persist UTC instants or explicit civil fields
                v
+-------------------------------+
| Database / logs / telemetry   |
| - instants stored as UTC      |
| - operational evidence in UTC |
+-------------------------------+
```

This rule prevents local machine settings from becoming hidden business
logic. A developer workstation, CI runner, container host or database session
may be in any local timezone; the system behavior must remain the same.

## Why This Standard

This playbook adopts "UTC in the system core, IANA timezone at the user
boundary" because it makes time behavior explicit, testable and portable
across regions.

| Practice | Failure mode | This standard |
| --- | --- | --- |
| Use server local timezone | Behavior changes when the app moves host, region, container image or CI runner | Server, backend, database and CI defaults stay UTC |
| Store local date-times as generic timestamps | The original user intent cannot be reconstructed reliably | Local intent is stored as date/time plus IANA timezone |
| Treat offset as timezone | `-03:00` cannot describe future daylight-saving or political rule changes | Future schedules use IANA identifiers |
| Convert everything to UTC and discard local context | Meetings, reminders, due dates and recurrences can shift from the user's intended civil time | Store both local intent and computed UTC instant when needed |
| Let each layer infer timezone independently | Frontend, backend, database and logs disagree during debugging and audits | Timezone conversion is explicit and owned by the boundary where it belongs |

The main benefits are:

- predictable behavior across laptops, CI, containers, cloud regions and
  database sessions;
- simpler ordering, comparison, auditing, logging and incident correlation
  because instants share UTC semantics;
- correct user-facing scheduling across daylight-saving transitions and
  future timezone rule changes;
- clearer API contracts because an instant, a local date and a scheduled civil
  time are not represented by the same ambiguous field;
- easier testing because code can inject a clock and choose explicit
  timezones instead of depending on the machine's wall clock.

The tradeoff is a little more schema and contract discipline. User-facing
events often need both a civil representation (`date`, `time`, `timezone_id`)
and, for querying or reminders, a computed UTC instant. That duplication is
intentional: one value preserves user intent; the other supports efficient
system operation.

## Server and Runtime Defaults

Servers, containers, CI runners and scheduled job runtimes SHOULD run with UTC
as the default timezone:

```text
TZ=UTC
```

Runtime images SHOULD include current timezone data when the application
parses or renders IANA timezone rules. Minimal images that omit `tzdata` are
acceptable only when the application never performs local-zone conversion
inside that image.

Do not use host local time as an application dependency. System clocks should
be synchronized through the platform's normal time synchronization mechanism,
but application behavior should not depend on the host's local timezone,
locale or daylight-saving configuration.

## Backend Application Rules

Backend services, workers and internal APIs SHOULD treat UTC as the common
time language:

- generate system timestamps as UTC instants;
- serialize instants as RFC 3339 with `Z` unless an integration requires a
  different explicit offset;
- reject offset-free date-time strings for instant fields;
- validate user, tenant, venue and schedule timezones as IANA identifiers;
- store user-facing future intent as local date/time plus IANA timezone;
- compute recurrences and reminders with timezone-aware calendar libraries;
- keep logs, audit events, metrics exemplars and deployment evidence in UTC;
- inject or freeze clocks in tests instead of reading uncontrolled wall time.

Backend code MUST NOT infer business timezone from server local time,
database session timezone, container image timezone or deployment region.
Region is an infrastructure placement concept; timezone is a user, tenant,
venue or schedule concept.

## Frontend and Client Rules

The frontend is the normal place for timezone flexibility because it is closest
to the user. It SHOULD:

- display instants in the user's selected IANA timezone when known;
- offer browser-detected timezone as a convenient default, not as an
  irreversible fact;
- allow explicit timezone selection when time affects deadlines, bookings,
  reminders, compliance, billing or coordination across regions;
- send local user intent as separate local date/time fields plus IANA timezone;
- send actual instants as RFC 3339 timestamps with explicit offset, preferably
  UTC `Z` when generated by backend data;
- avoid parsing offset-free date-time strings as instants;
- format display with locale-aware APIs while keeping locale separate from
  timezone preference.

The current browser offset is not enough for future scheduling. For example,
`-03:00` does not describe whether future daylight-saving or political rule
changes apply. Use `America/Sao_Paulo`, `Europe/Lisbon` or another IANA
timezone when the user's civil-time intent matters.

## Persistence

Choosing the database column type is part of the timezone contract. A field
named `datetime` is not precise enough in design review; the schema must state
what kind of time value is being stored.

For PostgreSQL, use this decision table:

| Value being stored | PostgreSQL type | Notes |
| --- | --- | --- |
| Instant on the timeline | `timestamptz` | Use for `created_at`, `updated_at`, audit events, job due instants and external event timestamps |
| Local calendar date | `date` | Use for birthdays, due dates, business dates and billing cycle dates |
| Local clock time | `time` | Use only with a separate date/timezone context, such as opening hours |
| Local civil date-time intent | `timestamp without time zone` plus IANA timezone column | Use for future appointments or schedules where the local civil value matters |
| Recurring schedule | recurrence rule plus IANA timezone | Do not model recurring civil schedules as a list of fixed UTC offsets |

For PostgreSQL, prefer `timestamptz` for instants such as `created_at`,
`updated_at`, `deleted_at`, `published_at`, audit entries and operational
events. `timestamptz` represents a point on the timeline; PostgreSQL stores it
internally as UTC and does not retain the original timezone name or offset.

Use `date` for date-only business facts and `time` only for clock-time facts
that are intentionally independent of a date. Use `timestamp without time
zone` only for a local civil date-time that is always interpreted together with
a separate IANA timezone column.

```sql
-- Instant that already happened or is due at one absolute moment.
created_at timestamptz not null default now()

-- Future user intent. Keep the civil time and governing timezone.
starts_on date not null
starts_at time not null
timezone_id text not null
```

Avoid patterns such as:

```sql
-- Ambiguous: the database cannot know this naive value is UTC.
created_at timestamp not null default (now() at time zone 'utc')

-- Ambiguous: this may mean different zones depending on context.
timezone text not null default 'EST'
```

The risky failure mode is storing a local backend value in a timezone-naive
column and later treating it as UTC:

```text
Backend timezone: America/Sao_Paulo
Actual instant:   2026-05-24T13:42:08Z
Local value:      2026-05-24 10:42:08

Bad schema:       created_at timestamp without time zone
Stored value:     2026-05-24 10:42:08
Later read as:    2026-05-24T10:42:08Z
Error:            instant shifted three hours earlier
```

This happens because `timestamp without time zone` stores a calendar date and
clock time without any offset or timezone identity. Once the literal is stored,
the database cannot know whether `10:42:08` meant UTC, `America/Sao_Paulo`,
`Europe/Lisbon` or another zone. Backend and database drivers may also apply
session timezone rules differently when binding, reading or formatting values.

For instants, the safe pattern is:

```sql
created_at timestamptz not null default now()
```

and the backend should bind a timezone-aware instant, not a formatted local
string.

Where the database supports constraints or domain types, validate timezone IDs
against the platform's IANA timezone list at the application boundary or with
a controlled reference table. Do not accept arbitrary strings and silently
fall back to UTC.

## API and Event Contracts

Use different wire formats for different meanings:

| Meaning | Format | Example |
| --- | --- | --- |
| Instant | RFC 3339 date-time with offset | `2026-05-24T13:42:08Z` |
| Local date | RFC 3339 full-date | `2026-05-24` |
| Local time | explicit clock time | `09:30:00` |
| User/schedule timezone | IANA timezone ID | `America/Sao_Paulo` |
| Duration | explicit unit or ISO 8601 duration when supported | `900` seconds or `PT15M` |

Generated service timestamps SHOULD be serialized in UTC with `Z`. Incoming
timestamps MAY include non-UTC offsets, but the system MUST normalize instants
before persistence and MUST reject offset-free date-time strings when an
instant is required.

RFC 9557 defines an extended RFC 3339 form that can attach additional
information such as an IANA timezone to a timestamp. Use that form only when
all producers, consumers, validators and query tools explicitly support it.
For ordinary JSON/OpenAPI contracts, prefer separate fields for the instant
and the timezone.

OpenAPI schemas SHOULD make the distinction visible:

```yaml
created_at:
  type: string
  format: date-time
  example: "2026-05-24T13:42:08Z"
timezone_id:
  type: string
  example: "America/Sao_Paulo"
starts_on:
  type: string
  format: date
  example: "2026-05-24"
starts_at:
  type: string
  pattern: "^([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$"
  example: "09:30:00"
```

## User Experience

Display time in the user's chosen timezone when available. If the user has not
chosen one, use a clearly defined product default, tenant default or browser
detected timezone, and allow correction when time affects commitments,
deadlines, bookings or compliance.

Use locale-aware formatting for display, but do not confuse locale with
timezone. A Portuguese-speaking user may need `Europe/London`; a US-English
browser may be used while traveling in Japan. Persist timezone preference
separately from language/locale preference.

For critical workflows, show enough context to prevent mistakes:

```text
Good                                      Avoid
24 May 2026, 09:30 America/Sao_Paulo     24/05/2026 09:30
Due today in your timezone               Due today
```

## Scheduling and Recurrence

Scheduling is not just timestamp storage.

For a one-time future event tied to local user intent, store:

- local date;
- local time;
- IANA timezone;
- optional precomputed UTC instant for querying and reminders;
- the timezone database version when the runtime exposes it and the risk
  justifies auditing recalculation.

For recurring events, store the recurrence rule and IANA timezone. Compute
each occurrence using timezone-aware calendar logic. Do not add fixed
durations such as `24 hours` or `7 * 24 hours` to model local daily/weekly
recurrence; daylight-saving transitions can create skipped, repeated or
shifted local times.

When local time is invalid or ambiguous because of daylight-saving transitions,
the product must define a policy. Examples:

- reject the invalid time and ask for another local time;
- move to the next valid local time;
- choose earlier or later offset for repeated times and record the choice.

The policy must be documented for user-facing scheduling domains.

## Time Arithmetic

Use duration arithmetic for elapsed time and deadlines measured from an
instant:

```text
token expires 900 seconds after issue
retry after 30 seconds
page if error rate persists for 10 minutes
```

Use calendar arithmetic for human periods:

```text
renew on the same local day next month
run every business day at 08:00 in the account timezone
close submissions at local midnight
```

Do not mix the two without naming the intended behavior.

## Testing Requirements

Time-sensitive code SHOULD include tests for:

- UTC and at least two non-UTC IANA timezones;
- positive and negative offsets;
- daylight-saving spring-forward and fall-back transitions where applicable;
- zones without daylight saving;
- half-hour or quarter-hour offsets such as `Asia/Kolkata` or
  `Australia/Adelaide`;
- date-only values crossing UTC day boundaries;
- future schedule recalculation after timezone data changes when the domain
  depends on future local civil time.

Tests MUST control the clock through an injectable clock, test clock or
runtime-supported time-freezing mechanism. Do not make correctness depend on
the machine's current local timezone.

## Logs, Metrics and Incidents

Operational evidence SHOULD use UTC timestamps. Logs, trace events, deployment
records and incident timelines should use RFC 3339 UTC timestamps unless a
local timezone is explicitly required for the investigation and clearly named.

Metrics should use the monitoring system's timestamp model and avoid timestamp
values as high-cardinality labels. Dashboards may render local time for
operators, but queries and incident records should remain unambiguous.

## Reference Basis

This standard adopts external guidance as follows:

- RFC 3339 defines interoperable Internet timestamps with explicit
  relationship to UTC.
- RFC 9557 extends RFC 3339 for timestamps with additional information,
  including named timezones, but this playbook still prefers separate fields
  unless both sides support the extended syntax.
- IANA tz database is the source for named timezone identifiers and civil-time
  rule changes.
- W3C timezone guidance motivates the distinction between instants, local
  civil times and future scheduled events.
- PostgreSQL documentation and wiki guidance inform the `timestamptz` default
  for persisted instants.
- OpenAPI date and date-time formats align API schema conventions with RFC
  3339.

See [Architecture References](./references.md) for source links and adoption
notes.

## Review Checklist

- [ ] Does each temporal field state whether it is an instant, date, local
      time, zoned local date-time, recurrence, duration or calendar period?
- [ ] Are instants persisted with timezone-aware UTC semantics?
- [ ] Are future and recurring local events stored with an IANA timezone?
- [ ] Do API contracts reject offset-free date-times for instants?
- [ ] Are timezone abbreviations excluded from persisted data and contracts?
- [ ] Is display conversion performed explicitly from user/tenant/product
      timezone?
- [ ] Are DST gaps/repeated times handled by a documented policy?
- [ ] Are tests independent of machine timezone and current wall clock?
- [ ] Is timezone data updated through normal dependency/runtime maintenance?
