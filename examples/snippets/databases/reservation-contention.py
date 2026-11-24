"""Exercise the last-slot booking rule with two independent PostgreSQL callers."""

import argparse
import asyncio
import json
import sys
import traceback
from dataclasses import asdict, dataclass
from uuid import uuid4

import psycopg
from psycopg import sql


@dataclass
class Caller:
    actor: str
    claim_id: str
    pid: int | None = None
    stage: str = "not started"
    outcome: str | None = None


AVAILABLE = """
    SELECT count(*) FROM slots AS s
    WHERE NOT EXISTS (SELECT FROM slot_claims AS c WHERE c.slot_id = s.slot_id)
"""


async def reserve(db, caller, hold=None):
    async with db.transaction():
        await db.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")
        caller.stage = "inserting claim"
        cursor = await db.execute(
            """INSERT INTO slot_claims (slot_id, actor_id, claim_id)
               VALUES (42, %s, %s) ON CONFLICT (slot_id) DO NOTHING
               RETURNING claim_id""",
            (caller.actor, caller.claim_id),
        )
        inserted = await cursor.fetchone()
        if inserted:
            outcome = f"Confirmed({inserted[0]})"
        else:
            caller.stage = "reading committed owner"
            cursor = await db.execute(
                "SELECT actor_id, claim_id FROM slot_claims WHERE slot_id = 42"
            )
            owner = await cursor.fetchone()
            if owner is None:
                raise AssertionError("Conflicting insert returned no committed owner")
            outcome = "SlotTaken"
            if owner == (caller.actor, caller.claim_id):
                outcome = f"Confirmed({caller.claim_id})"

        if hold is not None:
            inserted_first, allow_commit = hold
            caller.stage = "holding transaction before commit"
            inserted_first.set()
            await allow_commit.wait()
        caller.stage = "committing"
    caller.stage = "committed"
    caller.outcome = outcome


async def wait_for_blocker(observer, first, second, competitor, evidence):
    while True:
        cursor = await observer.execute(
            """SELECT pg_blocking_pids(pid), wait_event_type, wait_event
               FROM pg_stat_activity WHERE pid = %s""",
            (second.pid,),
        )
        row = await cursor.fetchone()
        if row:
            blockers, kind, event = row
            evidence["lock_wait"] = {"blockers": blockers, "type": kind, "event": event}
            if first.pid in blockers:
                return
        if competitor.done():
            raise AssertionError("Second caller finished before the observed wait")
        await asyncio.sleep(0.05)


async def run(args, evidence, first, second):
    schema = evidence["schema"]
    identifier = sql.Identifier(schema)
    statement_timeout_ms = (args.timeout + 5) * 1000

    def connect():
        return psycopg.AsyncConnection.connect(
            autocommit=True,
            client_encoding="UTF8",
            connect_timeout=args.timeout,
            options=f"-c search_path={schema} -c statement_timeout={statement_timeout_ms}",
        )

    async with await connect() as observer:
        await observer.execute(sql.SQL("CREATE SCHEMA {}").format(identifier))
        try:
            async with asyncio.timeout(args.timeout):
                await observer.execute("CREATE TABLE slots (slot_id integer PRIMARY KEY)")
                await observer.execute("""
                    CREATE TABLE slot_claims (
                        slot_id integer PRIMARY KEY REFERENCES slots (slot_id),
                        actor_id text NOT NULL,
                        claim_id text NOT NULL
                    )
                """)
                await observer.execute("INSERT INTO slots (slot_id) VALUES (42)")
                cursor = await observer.execute(AVAILABLE)
                evidence["initial_available"] = (await cursor.fetchone())[0]
                if evidence["initial_available"] != 1:
                    raise AssertionError("Expected one initially available slot")

                evidence["stage"] = "connecting booking sessions"
                async with await connect() as a, await connect() as b:
                    first.pid = a.info.backend_pid
                    second.pid = b.info.backend_pid
                    inserted_first = asyncio.Event()
                    allow_commit = asyncio.Event()
                    evidence["stage"] = "waiting for first insert"
                    async with asyncio.TaskGroup() as group:
                        group.create_task(reserve(a, first, (inserted_first, allow_commit)))
                        await inserted_first.wait()
                        competitor = group.create_task(reserve(b, second))
                        evidence["stage"] = "observing contention"
                        await wait_for_blocker(observer, first, second, competitor, evidence)
                        if args.reproduce_timeout:
                            evidence["stage"] = "holding first commit to reproduce timeout"
                        else:
                            evidence["stage"] = "waiting for both commits"
                            allow_commit.set()

                evidence["stage"] = "verifying committed claims"
                async with await connect() as fresh:
                    cursor = await fresh.execute(
                        "SELECT slot_id, actor_id, claim_id FROM slot_claims ORDER BY slot_id"
                    )
                    claims = await cursor.fetchall()
                    cursor = await fresh.execute(AVAILABLE)
                    available = (await cursor.fetchone())[0]
                evidence.update(committed_claims=claims, remaining_available=available)
                if (first.outcome, second.outcome) != ("Confirmed(a1)", "SlotTaken"):
                    raise AssertionError("Expected Ana's confirmation and Ben's SlotTaken")
                if claims != [(42, "ana", "a1")] or available != 0:
                    raise AssertionError("Expected only Ana's claim and zero available slots")
        finally:
            await observer.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(identifier))
            evidence["schema_removed"] = True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=int, default=10, help="exercise deadline in seconds")
    parser.add_argument(
        "--reproduce-timeout", action="store_true",
        help="withhold the first commit after observing the conflicting write",
    )
    args = parser.parse_args()
    if args.timeout < 1:
        parser.error("--timeout must be a positive number of seconds")

    first = Caller("ana", "a1")
    second = Caller("ben", "b1")
    evidence = {
        "schema": f"reservation_contention_{uuid4().hex}",
        "stage": "setting up fixture",
        "lock_wait": None,
        "schema_removed": False,
    }
    try:
        asyncio.run(run(args, evidence, first, second))
    except Exception as error:
        traceback.print_exception(error)
        status = "FAIL"
    else:
        status = "PASS"
    evidence.update(result=status, timeout_seconds=args.timeout, A=asdict(first), B=asdict(second))
    print(json.dumps(evidence), file=sys.stdout if status == "PASS" else sys.stderr)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
