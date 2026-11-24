# One slot, two booking paths

Two customers want slot 42. Ana books through an HTTP API. Ben's booking
arrives as a message for a worker. Both call the same Python operation,
and PostgreSQL enforces one committed claim per slot. This local reference
implementation lets you see the result each caller receives and compare it
with the stored reservation.

```text
HTTP client  -> API                    -> reserve() -> slot_claims
producer CLI -> booking_jobs -> worker -> reserve() -> slot_claims
                                worker -> booking_jobs.outcome (same transaction)
```

The [API](./api.py) maps its synthetic bearer token to an actor. The
[worker and its CLI](./worker.py) use a PostgreSQL table as a durable inbox.
The worker locks a pending message, calls the [shared booking operation](./booking.py)
and records the outcome in the same transaction as the claim. The queue key
is the actor, slot and claim ID. Repeating a delivery with that identity
returns the existing job. The [schema](./init.sql) separately enforces a
primary key on the slot in the claims table.

## Start and check readiness

Use Docker with Compose supporting `up --wait`, and curl for the manual HTTP
requests. The first build needs access to the base images and Python package
index. From the repository root, run the following commands in the same shell.

```bash
cd examples/reference-implementations/small-production-service/reservations
docker compose up --build --wait --wait-timeout 90
```

```bash
docker compose ps
api="http://127.0.0.1:${RESERVATION_PORT:-18084}"
curl --noproxy '*' --fail --silent --show-error "$api/ready"
```

Expect three healthy services and `{"ready": true}`. The API reads slot 42
from PostgreSQL. The worker health check looks for its polling session in
the same database. The contention scenario below verifies actual message
processing. Only the API publishes a host port, bound to loopback.

## Race the API against the worker

Start with an empty fixture and no other senders. Run the
[contention scenario](./scenario.py) from the API container so it can use
both the HTTP route and the trusted queue producer.

```bash
docker compose exec -T api python scenario.py
```

The coordinator inserts a provisional claim for slot 42 inside an open
transaction. It sends Ana's HTTP request (`a1`) and enqueues Ben's worker
message (`b1`). Once PostgreSQL reports **both** application sessions
waiting on the coordinator, the coordinator rolls back its claim. The API
and worker now compete for the same available slot. The scenario fails if
it cannot observe the overlap, if the two outcomes disagree with the
contract, or if the row read on a fresh connection disagrees with the winner.

| Winner | HTTP response to Ana, claim `a1` | Worker result for Ben, claim `b1` | Only row in `slot_claims` |
| --- | --- | --- | --- |
| Ana | `201 Confirmed` | `SlotTaken` | `42, ana, a1` |
| Ben | `409 SlotTaken` | `Confirmed` | `42, ben, b1` |

Inspect the durable worker outcome by its original identity and query the
database independently. The result should match one row of the table above.

```bash
docker compose exec -T worker python worker.py result ben 42 b1
docker compose exec -T db psql -X -U postgres -d reservations \
  -c 'SELECT slot_id, actor_id, claim_id FROM slot_claims ORDER BY slot_id;'
```

## Reset the fixture and submit the two claims by hand

After all in-flight requests finish, run this reset **in the disposable lab**.
It empties the inbox, its outcomes and the claims in one transaction. It
keeps the single parent slot. The scenario checks for an empty fixture at
the beginning so a previous run's bookings are visible until you reset them.

```bash
docker compose exec -T db psql -X -v ON_ERROR_STOP=1 -U postgres -d reservations \
  -c 'TRUNCATE booking_jobs, slot_claims;'
```

Submit Ana's claim first. Expect HTTP `201` and a JSON response identifying
`a1` as `Confirmed`. Repeating this exact request returns HTTP `200` with the
same confirmation. An unauthenticated caller gets `401`. The authenticated
lab guest (`Bearer lab-guest`) lacks booking permission and gets `403`.

```bash
curl --noproxy '*' --silent --show-error --write-out 'HTTP %{http_code}\n' \
  -H 'Authorization: Bearer lab-ana' -H 'Content-Type: application/json' \
  --data '{"claim_id":"a1"}' "$api/slots/42/claims"
```

Deliver Ben's message and look up its outcome. `Pending` means it is in
the inbox. Repeat the read until the worker reports `SlotTaken` for `b1`.
The worker also logs each terminal result after commit. In this ordering
the SQL query above must return precisely `42, ana, a1`.

```bash
docker compose exec -T worker python worker.py enqueue ben 42 b1
docker compose exec -T worker python worker.py result ben 42 b1
```

## Configuration, persistence and recovery

- The [Compose file](./compose.yaml) runs one database, one API and one
  worker. Both application processes use the same [Dockerfile](./Dockerfile)
  and a restricted database role. The host operator can administer the lab
  via Compose. The fixed bearer tokens and default database passwords are
  public synthetic values for this local exercise.
- Before startup you can export `RESERVATION_PORT` to change the host port.
  Docker allocates the project subnet by default. If its address pool is
  exhausted, set `RESERVATION_SUBNET` to an unused private CIDR that does
  not overlap your Docker networks, host routes or VPN.
- PostgreSQL initializes the role, tables and slot 42 on the first start
  with an empty named volume. To override the lab passwords, set
  `RESERVATION_APP_PASSWORD` and `RESERVATION_ADMIN_PASSWORD` before this
  first start. Changing the environment later does not rotate a stored
  PostgreSQL password.
- If the worker exits before commit, its booking and inbox update roll
  back together. Pending jobs survive in the database. An API client that
  loses its response can retry with the same identity. Inspect
  `docker compose logs worker` after a processing failure. Once the database
  issue is resolved, `docker compose up -d worker` resumes polling.
- A single database backs both booking paths and the queue. Loss of its
  volume loses both reservations and outcomes. The example has no replica
  or backup and runs on one Docker host. Ingress, production identity,
  backup/restore and timed deployment recovery need separate controls.

Use `docker compose down` to stop the project and retain the named volume.
To discard all synthetic reservations and remove the lab containers,
network and volume, run the following command from this directory.

```bash
docker compose down --volumes
```

The [booking contract](../../../../software-design/business-rule-placement.md),
[reservation schema](../../../../databases/reservation-schema.md) and
[two-session integration test](../../../snippets/databases/README.md#test-the-last-available-slot)
give the underlying rule, storage guarantee and database-level exercise.
PostgreSQL documents how locking reads can select pending work for a queue
and how Read Committed handles conflicting inserts.
[Locking clauses](https://www.postgresql.org/docs/17/sql-select.html#SQL-FOR-UPDATE-SHARE)
and [transaction isolation](https://www.postgresql.org/docs/17/transaction-iso.html#XACT-READ-COMMITTED).
