# Database Snippets

## Test the last available slot

The [reservation contention test](./reservation-contention.py) automates the
[two-session exercise](../../../databases/reservation-schema.md) for local
and pull request validation. It runs the example's claim SQL and interprets
the result for two synthetic customers. The HTTP and queue entry points
have their own [test boundaries](../../../testing/choosing-automated-tests.md).

### Run locally or in CI

Use Python 3.11 or later, Psycopg 3 and a disposable PostgreSQL database.
The example was exercised on PostgreSQL 17.11.
All connections use the same role. It needs permission to connect and
create schemas in that database. For a local PostgreSQL installation with
`createdb` privileges, create the lab database once with
`createdb reservation_lab`. In CI, use the database provided by the job's
PostgreSQL service. Supply its connection settings through the usual libpq
variables, such as `PGHOST`, `PGPORT`, `PGUSER` and `PGDATABASE`.

From the repository root, install the driver in an active virtual
environment and run the test. This example uses the local lab database
and pins the driver so CI can reproduce the same client behavior.

```bash
python -m pip install 'psycopg[binary]==3.3.9'
export PGDATABASE=reservation_lab
python examples/snippets/databases/reservation-contention.py --timeout 10
```

Use the same Python command as a required CI step with the job's connection
settings. Each invocation creates its own schema, seeds one unclaimed slot
and drops the schema after success or failure. Independent runs can share
the lab database. Supply credentials through the runner's PostgreSQL
credential store or CI secrets.

### What a pass proves

1. Ana inserts claim `a1` for slot 42 and leaves her transaction open.
2. Ben attempts claim `b1` on a separate connection. The test checks that
   PostgreSQL lists Ana's backend PID among Ben's blockers before allowing
   Ana to commit. A sequential run cannot satisfy this check.
3. Ana receives confirmation after commit. Ben's insert returns no row.
   A subsequent read at Read Committed finds Ana's claim, so Ben receives
   `SlotTaken`.
4. A fresh connection reads exactly one committed claim, `(42, ana, a1)`,
   and counts zero available slots. The JSON report should contain
   `A.outcome = Confirmed(a1)`, `B.outcome = SlotTaken` and
   `remaining_available = 0`. Exit status zero requires both callers'
   outcomes and the final state to agree.

### Reproduce a failure

For an intermittent failure, keep the database and driver versions, timeout
and failing output from CI. Repeat the contested write with the same settings.
This shell loop stops on the first failure and preserves its exit status.

```bash
for run in 1 2 3 4 5; do
  echo "Reservation contention run $run"
  python examples/snippets/databases/reservation-contention.py --timeout 10 || exit 1
done
```

To reproduce a timeout deliberately, run the following command on the lab
database. It holds Ana's transaction open after PostgreSQL has confirmed
the wait. Expect exit status 1 and a JSON report on standard error.

```bash
python examples/snippets/databases/reservation-contention.py --timeout 2 --reproduce-timeout
```

On this failure, `lock_wait.blockers` contains Ana's PID, A is holding its
commit, and B is inserting. Both outcomes are still null. If the timeout
expires before that evidence appears, use the reported stages to locate the
delay. Increase `--timeout` on a slow runner to allow setup and lock
observation to finish.

PostgreSQL defines the blocking and visibility behavior used by the test.
The playbook maps a competing committed claim to `SlotTaken`.
See the [database adoption notes](../../../databases/references.md#reservation-schema)
and [Psycopg installation instructions](https://www.psycopg.org/psycopg3/docs/basic/install.html).

## Evaluate a reservation index

The [reservation index experiment](./reservation-index.sql) is an illustrative
`psql` script for a disposable PostgreSQL database. Each invocation creates
one schema, seeds synthetic slots and claims, prints the customer lookup and
its plan, then times a batch of 10,000 inserts.

Use a role that can create schemas in the lab database. Set `lab_schema` to
a fresh schema name and `with_index` to `on` or `off`. Reusing a schema
name stops the script at creation. Both arms retain the slot key and foreign
key. The output includes the ordered ten-row result, the insert time, the
final claim count and the candidate index size in bytes.

See [Evaluating a reservation index](../../../databases/reservation-index.md)
for the commands, measured results, assumptions and PostgreSQL references.
The script leaves the synthetic data available for inspection. Discard the
lab database after completing the comparison.
