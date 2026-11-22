# References and Adoption Notes

## Reservation schema

- PostgreSQL defines primary keys as unique, non-null row identifiers and
  foreign keys as references to existing keys. The example uses both on
  the claim's slot ID. Modeling one slot as one bookable place is a decision
  about appointments. [Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html)
- PostgreSQL checks a unique index against concurrent inserts. If the other
  transaction is still open, its commit or rollback can change the outcome.
  The exercise observes this wait using the blocking session's process ID.
  [Index uniqueness checks](https://www.postgresql.org/docs/current/index-unique-checks.html)
  and [session information functions](https://www.postgresql.org/docs/current/functions-info.html).
- PostgreSQL supports a conflict target and returns rows affected by an
  insert. At Read Committed, a conflicting row can prevent insertion before
  it is visible to that statement's snapshot. The example reads the owner
  in the next statement. Treating a matching attempt as a replay and a
  different claim as `SlotTaken` is the application's policy.
  [INSERT](https://www.postgresql.org/docs/current/sql-insert.html) and
  [transaction isolation](https://www.postgresql.org/docs/current/transaction-iso.html).

## Evaluating an index

- PostgreSQL uses statistics to estimate how many rows a predicate will
  match. The lab refreshes statistics in both schemas before comparing
  estimates with actual rows. [ANALYZE](https://www.postgresql.org/docs/17/sql-analyze.html).
- A measured plan reports actual rows, loops, execution time and buffer
  accesses. In this exercise we compare the top node's buffers across plans
  and use child nodes to locate the work.
  [Using EXPLAIN](https://www.postgresql.org/docs/17/using-explain.html).
- Each additional index must stay synchronized with writes. We time a
  committed insert batch and use `pg_relation_size` to report the candidate
  index's main fork in bytes. Workload frequency and the decision to keep it
  are local judgments.
  [Index introduction](https://www.postgresql.org/docs/17/indexes-intro.html)
  and [object size functions](https://www.postgresql.org/docs/17/functions-admin.html#FUNCTIONS-ADMIN-DBSIZE).

## Schema migrations

- A row-level `BEFORE INSERT` trigger can change the row before PostgreSQL
  checks constraints. The exercise uses one to copy a booking identity
  supplied by either client into the other column.
  [CREATE TRIGGER](https://www.postgresql.org/docs/17/sql-createtrigger.html).
- Adding a check with `NOT VALID` enforces it on subsequent inserts and
  updates. Validating it later scans existing rows with a weaker lock than
  the one used to add it. The exercise commits validation before requesting
  the stronger cutover lock.
  [ALTER TABLE](https://www.postgresql.org/docs/17/sql-altertable.html).
- PostgreSQL can replace a view's defining query while preserving its
  existing output columns. The v2 client keeps the same read interface as
  its data source changes from both columns to `booked_by_id` alone.
  [CREATE VIEW](https://www.postgresql.org/docs/17/sql-createview.html).
- PostgreSQL exposes connected sessions and their application names.
  Before retiring v1, the playbook checks those observations against API
  and worker revisions, job schedules and retry lifetimes.
  [Activity statistics](https://www.postgresql.org/docs/17/monitoring-stats.html#MONITORING-PG-STAT-ACTIVITY-VIEW).
