-- Run once per fresh schema in a disposable database using psql -X.
\set ON_ERROR_STOP on
\set AUTOCOMMIT on
\timing off
SELECT :'with_index'::boolean AS build_candidate \gset
CREATE SCHEMA :"lab_schema";
SET search_path TO :"lab_schema";

CREATE TABLE slots (
    slot_id integer PRIMARY KEY
);
CREATE TABLE slot_claims (
    slot_id  integer PRIMARY KEY REFERENCES slots (slot_id),
    actor_id text NOT NULL,
    claim_id text NOT NULL
);

-- Reserve the last 10,000 parent slots for the measured insert.
INSERT INTO slots SELECT n FROM generate_series(1, 110000) AS s(n);
INSERT INTO slot_claims (slot_id, actor_id, claim_id)
SELECT n, 'actor-' || (n % 10000), 'claim-' || n
FROM generate_series(1, 100000) AS s(n);

\if :build_candidate
CREATE INDEX slot_claims_actor_idx ON slot_claims (actor_id);
\endif
ANALYZE slots;
ANALYZE slot_claims;

PREPARE customer_bookings AS
    SELECT slot_id, claim_id
    FROM slot_claims
    WHERE actor_id = 'actor-42'
    ORDER BY slot_id;

-- Print the ordered result as a correctness check and warm up the lookup.
EXECUTE customer_bookings;
EXPLAIN (ANALYZE, BUFFERS) EXECUTE customer_bookings;
SELECT coalesce(pg_relation_size(to_regclass('slot_claims_actor_idx')), 0)
    AS candidate_bytes_before_batch;

-- psql reports the time for this one autocommitted statement.
\timing on
INSERT INTO slot_claims (slot_id, actor_id, claim_id)
SELECT n, 'actor-' || (n % 10000), 'claim-' || n
FROM generate_series(100001, 110000) AS s(n);
\timing off

SELECT count(*) AS final_claims FROM slot_claims;
SELECT coalesce(pg_relation_size(to_regclass('slot_claims_actor_idx')), 0)
    AS candidate_bytes_after_batch;
