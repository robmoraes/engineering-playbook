"""Race two claims through the running HTTP API and the worker's durable inbox."""

import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from http.client import HTTPConnection
from pathlib import Path

from booking import connect


WAIT_SECONDS = 10


def submit_http_claim():
    client = HTTPConnection("127.0.0.1", 8080, timeout=30)
    try:
        client.request(
            "POST", "/slots/42/claims", json.dumps({"claim_id": "a1"}),
            {"Authorization": "Bearer lab-ana", "Content-Type": "application/json"},
        )
        response = client.getresponse()
        return response.status, json.loads(response.read())
    finally:
        client.close()


def wait_for_both_writers(observer, gate_pid, http_request):
    deadline = time.monotonic() + WAIT_SECONDS
    while True:
        blocked = observer.execute(
            """SELECT application_name, pid FROM pg_stat_activity
               WHERE datname = current_database()
                 AND application_name IN ('booking-api', 'booking-worker')
                 AND %s = ANY(pg_blocking_pids(pid))
               ORDER BY application_name""",
            (gate_pid,),
        ).fetchall()
        if {name for name, pid in blocked} == {"booking-api", "booking-worker"}:
            print(f"Both writers waiting on scenario PID {gate_pid}: {blocked}", flush=True)
            return
        if http_request.done():
            raise RuntimeError(f"API finished before overlap: {http_request.result()}")
        if time.monotonic() >= deadline:
            raise TimeoutError(f"Could not establish overlap; blockers of both writers "
                               f"must include {gate_pid}. Last blocked sessions: {blocked}")
        time.sleep(0.05)


def wait_for_worker(observer):
    deadline = time.monotonic() + WAIT_SECONDS
    while True:
        row = observer.execute(
            """SELECT outcome FROM booking_jobs
               WHERE actor_id = 'ben' AND slot_id = 42 AND claim_id = 'b1'"""
        ).fetchone()
        if row and row[0] is not None:
            return row[0]
        if time.monotonic() >= deadline:
            raise TimeoutError(f"No terminal worker outcome for ben/42/b1: {row}")
        time.sleep(0.05)


def run():
    with ThreadPoolExecutor(max_workers=1) as executor, connect("booking-observer") as observer:
        observer.autocommit = True
        fixture = observer.execute(
            """SELECT (SELECT array_agg(slot_id ORDER BY slot_id) FROM slots),
                      (SELECT count(*) FROM slot_claims), (SELECT count(*) FROM booking_jobs)"""
        ).fetchone()
        if fixture != ([42], 0, 0):
            raise RuntimeError(f"Expected slot 42 with no claims or jobs; found {fixture}. "
                               "Reset the disposable fixture before running the race.")

        with connect("booking-scenario") as gate, gate.transaction(force_rollback=True):
            gate.execute("SET LOCAL lock_timeout = '3s'")
            gate.execute(
                """INSERT INTO slot_claims (slot_id, actor_id, claim_id)
                   VALUES (42, 'scenario', 'uncommitted')"""
            )
            http_request = executor.submit(submit_http_claim)
            subprocess.run(
                [sys.executable, str(Path(__file__).with_name("worker.py")),
                 "enqueue", "ben", "42", "b1"],
                check=True, timeout=WAIT_SECONDS,
            )
            wait_for_both_writers(observer, gate.info.backend_pid, http_request)
        # Rolling back the provisional row releases both writers onto the same empty slot.
        status, reply = http_request.result(timeout=30)
        worker_outcome = wait_for_worker(observer)

    print(f"API ana/42/a1: HTTP {status} {reply}")
    print(f"Worker ben/42/b1: {worker_outcome}")
    observations = (status, reply.get("outcome"), worker_outcome)
    if reply.get("claim_id") != "a1":
        raise RuntimeError("API response did not identify the submitted claim a1")
    if observations == (201, "Confirmed", "SlotTaken"):
        winner = (42, "ana", "a1")
    elif observations == (409, "SlotTaken", "Confirmed"):
        winner = (42, "ben", "b1")
    else:
        raise RuntimeError(f"Expected one new confirmation and one rejection: {observations}")

    with connect("booking-verifier") as fresh:
        claims = fresh.execute("SELECT slot_id, actor_id, claim_id FROM slot_claims").fetchall()
    if claims != [winner]:
        raise RuntimeError(f"Expected exactly {winner} in PostgreSQL, found {claims}")
    print(f"PASS: one committed reservation {winner}")


if __name__ == "__main__":
    run()
