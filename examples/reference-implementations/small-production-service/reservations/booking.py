"""The booking decision shared by the HTTP API and the queue worker."""

import re

import psycopg


class SlotNotFound(Exception):
    """The requested slot has no parent row."""


def connect(application_name):
    conn = psycopg.connect(
        application_name=application_name,
        client_encoding="UTF8",
        connect_timeout=3,
        options="-c statement_timeout=30000",
    )
    conn.isolation_level = psycopg.IsolationLevel.READ_COMMITTED
    return conn


def valid_id(value):
    return isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9_-]{1,64}", value) is not None


def reserve(conn, actor_id, slot_id, claim_id):
    """Decide inside the caller's transaction. Publish the outcome after commit."""
    if actor_id not in ("ana", "ben"):
        return "Forbidden"

    try:
        inserted = conn.execute(
            """INSERT INTO slot_claims (slot_id, actor_id, claim_id)
               VALUES (%s, %s, %s) ON CONFLICT (slot_id) DO NOTHING
               RETURNING claim_id""",
            (slot_id, actor_id, claim_id),
        ).fetchone()
    except psycopg.errors.ForeignKeyViolation as error:
        if (error.diag.table_name, error.diag.constraint_name) == (
            "slot_claims", "slot_claims_slot_id_fkey"
        ):
            raise SlotNotFound(slot_id) from error
        raise
    if inserted is not None:
        return "Confirmed"

    # Read Committed gives this statement a fresh view of the winning claim.
    owner = conn.execute(
        "SELECT actor_id, claim_id FROM slot_claims WHERE slot_id = %s",
        (slot_id,),
    ).fetchone()
    if owner is None:
        raise RuntimeError("Conflicting claim disappeared during booking")
    if owner == (actor_id, claim_id):
        return "Replayed"
    return "SlotTaken"
