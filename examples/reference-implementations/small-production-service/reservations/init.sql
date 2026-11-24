\set ON_ERROR_STOP on
\getenv app_password RESERVATION_APP_PASSWORD
BEGIN;
CREATE ROLE reservation_app LOGIN PASSWORD :'app_password';

CREATE TABLE slots (slot_id integer PRIMARY KEY);
INSERT INTO slots (slot_id) VALUES (42);

CREATE TABLE slot_claims (
    slot_id integer PRIMARY KEY REFERENCES slots (slot_id),
    actor_id text NOT NULL,
    claim_id text NOT NULL
);

CREATE TABLE booking_jobs (
    actor_id text NOT NULL,
    slot_id integer NOT NULL REFERENCES slots (slot_id),
    claim_id text NOT NULL,
    received_at timestamptz NOT NULL DEFAULT now(),
    outcome text CHECK (outcome IN ('Confirmed', 'Replayed', 'SlotTaken', 'Forbidden')),
    PRIMARY KEY (actor_id, slot_id, claim_id)
);

GRANT SELECT ON slots TO reservation_app;
GRANT SELECT, INSERT ON slot_claims TO reservation_app;
GRANT SELECT, INSERT (actor_id, slot_id, claim_id), UPDATE (outcome)
    ON booking_jobs TO reservation_app;
COMMIT;
