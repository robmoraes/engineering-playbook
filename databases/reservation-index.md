# Evaluating a Reservation Index

A customer wants to list their bookings. The primary key on `slot_id`
protects the [one-claim-per-slot rule](./reservation-schema.md). The lookup
filters on `actor_id`. Does a second index save enough work on that lookup
to justify maintaining it on every booking?

## Workload and candidate

Assume 100 customer lookups per batch of 10,000 new claims. This ratio is
an input to the decision. The lab seeds 110,000 existing slots and claims
the first 100,000. Each of 10,000 synthetic customers owns exactly ten
claims, interleaved by slot ID. The measured insert adds one more claim
per customer against the remaining slots. Both arms use the same primary
key, foreign key, column types and non-null constraints.

```sql
SELECT slot_id, claim_id
FROM slot_claims
WHERE actor_id = 'actor-42'
ORDER BY slot_id;

CREATE INDEX slot_claims_actor_idx ON slot_claims (actor_id);
```

The candidate is a non-unique B-tree. Equality on its leading column locates
the customer's rows. PostgreSQL still needs the table for the returned
columns and sorts the matches by slot ID.

## Reproduce the comparison

From the repository root, use `psql` and an empty disposable PostgreSQL
database. The example below creates one named `reservation_index_lab`.
The [experiment script](../examples/snippets/databases/reservation-index.sql)
creates a fresh schema per run so every timed insert starts with the same
100,000 committed claims. Use one server with the same settings throughout.

```bash
createdb reservation_index_lab

run_arm() {
  psql -X -d reservation_index_lab -v lab_schema="$1" -v with_index="$2" \
    -f examples/snippets/databases/reservation-index.sql
}

run_arm pair1_base off
run_arm pair1_idx on
run_arm pair2_idx on
run_arm pair2_base off
run_arm pair3_base off
run_arm pair3_idx on
```

Each run refreshes planner statistics with `ANALYZE`, prints the ordered
result once to warm the lookup, then measures that same prepared query with
`EXPLAIN (ANALYZE, BUFFERS)`. Compare the actual pairs across arms. For
customer 42, slot IDs must be `42, 10042, 20042, …, 90042`, each paired with
`claim-<slot_id>`. After the timed insert, expect `INSERT 0 10000` and
110,000 total claims in every schema.

## Read the plans

These plans came from the first pair on PostgreSQL 17.11. Both runs used
8 KiB blocks, 128 MiB of shared buffers and 4 MiB of work memory. Data was
on tmpfs, with `fsync` and `synchronous_commit` enabled.

**Baseline, slot primary key only**

```text
Sort  (cost=1985.17..1985.19 rows=10 width=15) (actual time=8.030..8.032 rows=10 loops=1)
  Sort Key: slot_id
  Sort Method: quicksort  Memory: 25kB
  Buffers: shared hit=735
  ->  Seq Scan on slot_claims  (cost=0.00..1985.00 rows=10 width=15) (actual time=0.015..8.008 rows=10 loops=1)
        Filter: (actor_id = 'actor-42'::text)
        Rows Removed by Filter: 99990
        Buffers: shared hit=735
Planning Time: 0.002 ms
Execution Time: 8.070 ms
```

**With the customer index**

```text
Sort  (cost=41.16..41.19 rows=10 width=15) (actual time=0.032..0.033 rows=10 loops=1)
  Sort Key: slot_id
  Sort Method: quicksort  Memory: 25kB
  Buffers: shared hit=12
  ->  Bitmap Heap Scan on slot_claims  (cost=4.37..41.00 rows=10 width=15) (actual time=0.018..0.025 rows=10 loops=1)
        Recheck Cond: (actor_id = 'actor-42'::text)
        Heap Blocks: exact=10
        Buffers: shared hit=12
        ->  Bitmap Index Scan on slot_claims_actor_idx  (cost=0.00..4.37 rows=10 width=0) (actual time=0.014..0.014 rows=10 loops=1)
              Index Cond: (actor_id = 'actor-42'::text)
              Buffers: shared hit=2
Planning Time: 0.001 ms
Execution Time: 0.068 ms
```

The estimate of ten matches agreed with the actual ten in both plans. The
sequential scan discarded 99,990 rows. The bitmap index scan found the ten
matches using two buffer hits, then the heap scan fetched ten table pages.
Both sorted the same ten rows in memory. Compare buffer counts at the root
because a parent's count includes its children. All 735 baseline accesses
and all 12 indexed accesses were shared-buffer hits in this pair.

## Measure the write cost

Each row below is one pair of fresh schemas. Lookup time is the server's
reported execution time. Batch time is the elapsed time reported by `psql`
for one autocommitted insert of 10,000 new rows, including the primary key,
foreign key checks and commit. Fixture generation and index creation finish
before the timed statement.

| Pair and run order | Baseline lookup (ms) | Indexed lookup (ms) | Baseline batch (ms) | Indexed batch (ms) |
| --- | ---: | ---: | ---: | ---: |
| 1, baseline first | 8.070 | 0.068 | 276.436 | 289.803 |
| 2, indexed first | 8.221 | 0.073 | 274.236 | 305.455 |
| 3, baseline first | 7.530 | 0.075 | 309.011 | 326.964 |

All six runs returned the same ten ordered pairs before the batch and
finished with 110,000 claims. The secondary index's main fork occupied
1,040,384 bytes (1,016 KiB) both before and after the batch. The baseline
had zero bytes attributable to that index. An unchanged allocated size
still leaves index entries to maintain during inserts.

The indexed batch took 13–31 ms longer within each pair. Alternating the
order helps expose timing variation. The read measurements describe a warm
lookup and the writes use a single client on memory-backed storage. For a
deployment decision, repeat the paired runs on representative storage with
the observed customer distribution, cache pressure and write concurrency.

## Decide for this workload

**Keep the customer index** for the assumed 100 lookups per 10,000 inserted
claims. The median lookup fell from 8.070 ms to 0.073 ms. At that frequency,
the measured difference amounts to roughly 800 ms of query execution per
batch of bookings, against 13–31 ms of additional batch elapsed time and
about 1 MiB of index space. This calculation compares the scale of the two
costs in this lab. It cannot predict end-user latency under concurrent load.

Revisit the choice if the customer listing becomes rare. One such lookup
per batch would save about 8 ms on these measurements, less than the extra
write time in any pair. The primary key on `slot_id` still protects every
reservation whichever decision is made about the customer index.

See the [PostgreSQL sources and adoption notes](./references.md#evaluating-an-index).
