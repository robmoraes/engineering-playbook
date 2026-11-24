"""Poll the durable booking inbox, or submit and inspect synthetic messages."""

import argparse
import json
import sys
import time

import psycopg

from booking import connect, reserve, valid_id


def report(actor_id, slot_id, claim_id, outcome):
    print(json.dumps({
        "actor_id": actor_id, "slot_id": slot_id, "claim_id": claim_id, "outcome": outcome,
    }), flush=True)


def process_one(conn):
    with conn.transaction():
        job = conn.execute(
            """SELECT actor_id, slot_id, claim_id FROM booking_jobs
               WHERE outcome IS NULL ORDER BY received_at, actor_id, slot_id, claim_id
               LIMIT 1 FOR UPDATE SKIP LOCKED"""
        ).fetchone()
        if job is None:
            return False
        outcome = reserve(conn, *job)
        conn.execute(
            """UPDATE booking_jobs SET outcome = %s
               WHERE (actor_id, slot_id, claim_id) = (%s, %s, %s)""",
            (outcome, *job),
        )
    report(*job, outcome)
    return True


def run():
    failures = 0
    while True:
        try:
            with connect("booking-worker") as conn:
                while True:
                    processed = process_one(conn)
                    failures = 0
                    if not processed:
                        time.sleep(0.25)
        except psycopg.OperationalError as error:
            failures += 1
            print(f"Worker database error ({failures}/5): {type(error).__name__}",
                  file=sys.stderr, flush=True)
            if failures == 5:
                return 1
            time.sleep(failures)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("ready")
    for name in ("enqueue", "result"):
        command = commands.add_parser(name)
        command.add_argument("actor_id")
        command.add_argument("slot_id", type=int, choices=[42])
        command.add_argument("claim_id")
    args = parser.parse_args()
    if args.command is None:
        return run()

    with connect("booking-cli") as conn:
        if args.command == "ready":
            session = conn.execute(
                """SELECT 1 FROM pg_stat_activity WHERE datname = current_database()
                   AND usename = current_user AND application_name = 'booking-worker'"""
            ).fetchone()
            return 0 if session else 1

        if not valid_id(args.actor_id) or not valid_id(args.claim_id):
            parser.error("actor and claim IDs must match [A-Za-z0-9_-]{1,64}")
        job = (args.actor_id, args.slot_id, args.claim_id)
        if args.command == "enqueue":
            conn.execute(
                """INSERT INTO booking_jobs (actor_id, slot_id, claim_id) VALUES (%s, %s, %s)
                   ON CONFLICT (actor_id, slot_id, claim_id) DO NOTHING""", job
            )
        result = conn.execute(
            """SELECT outcome FROM booking_jobs
               WHERE (actor_id, slot_id, claim_id) = (%s, %s, %s)""", job
        ).fetchone()
    if result is None:
        report(*job, "Missing")
        return 1
    report(*job, result[0] or "Pending")
    return 0


if __name__ == "__main__":
    sys.exit(main())
