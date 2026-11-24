"""Deploy a tested image and measure booking recovery in a disposable Compose lab."""

import argparse
import json
import math
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from http.client import HTTPConnection
from pathlib import Path
from queue import Empty, Queue
from threading import Event, Thread
from uuid import uuid4


HERE = Path(__file__).resolve().parent
SERVICE = HERE.parents[2] / "reference-implementations/small-production-service/reservations"
PERIOD = 2
MAX_TICKS = 30
FIRST_SLOT = 1001
CAN_INSERT = "SELECT has_table_privilege('reservation_app', 'slot_claims', 'INSERT')"


def utc():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def command(*args, timeout=30):
    result = subprocess.run(args, text=True, capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f"{args[0]} failed ({result.returncode}): {result.stderr.strip()}")
    return result.stdout.strip()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def request(port, method, path, claim=None):
    conn = HTTPConnection("127.0.0.1", port, timeout=5)
    headers = {"Authorization": "Bearer lab-ana", "Content-Type": "application/json"}
    try:
        body = json.dumps({"claim_id": claim}) if claim else None
        conn.request(method, path, body, headers)
        response = conn.getresponse()
        return response.status, json.loads(response.read())
    finally:
        conn.close()


def book(port, slot, claim):
    started = utc()
    status, body = request(port, "POST", f"/slots/{slot}/claims", claim)
    return {
        "started_utc": started, "completed_utc": utc(), "slot_id": slot,
        "claim_id": claim, "http_status": status, "response": body,
    }


def sample(port, stop, events, probes):
    """Use a new slot at each scheduled tick. Skip missed ticks instead of catching up."""
    origin = time.monotonic()
    tick = 0
    try:
        while tick < MAX_TICKS:
            if stop.wait(max(0, origin + tick * PERIOD - time.monotonic())):
                return
            slot = FIRST_SLOT + tick
            probe = book(port, slot, f"probe-{slot}")
            probe["tick"] = tick
            probes.append(probe)
            events.put(probe)
            tick = max(tick + 1, math.ceil((time.monotonic() - origin) / PERIOD))
        raise TimeoutError("Exhausted the fresh probe slots")
    except Exception as error:
        events.put(error)


def next_probe(events):
    try:
        event = events.get(timeout=PERIOD + 8)
    except Empty as error:
        raise TimeoutError("No booking probe result before its deadline") from error
    if isinstance(event, Exception):
        raise event
    expected = {
        201: {"claim_id": event["claim_id"], "outcome": "Confirmed"},
        500: {"claim_id": event["claim_id"], "error": "InternalError"},
    }
    require(event["http_status"] in expected and event["response"] == expected[event["http_status"]],
            f"Unexpected booking response: {event}")
    return event


def exercise(compose, data):
    def sql(statement):
        return compose("exec", "-T", "db", "psql", "-XqAt", "-v", "ON_ERROR_STOP=1",
                       "-U", "postgres", "-d", "reservations", "-c", statement)

    def stored():
        return json.loads(sql("""SELECT coalesce(json_agg(json_build_array(
            slot_id, actor_id, claim_id) ORDER BY slot_id), '[]') FROM slot_claims"""))

    def policy(action, statement, expected):
        issued = utc()
        value = sql(f"{statement}; {CAN_INSERT}")
        require(value == expected, f"Unexpected effective INSERT privilege after {action}: {value}")
        data["policy_changes"].append({
            "action": action, "issued_utc": issued, "verified_utc": utc(),
            "sql": statement, "can_insert": value == "t",
        })

    def images():
        return {service: command("docker", "inspect", "--format", "{{.Image}}", compose("ps", "-q", service))
                for service in ("api", "worker")}

    data["deployed_images"] = images()
    data["deployment_verified_utc"] = utc()
    require(all(image == data["image_id"] for image in data["deployed_images"].values()),
            "The running containers do not use the tested image")
    host, port_text = compose("port", "api", "8080").rsplit(":", 1)
    require(host == "127.0.0.1", f"Expected loopback API publication, found {host}")
    port = int(port_text)
    data["public_endpoint"] = f"http://{host}:{port}"
    require(stored() == [] and sql(CAN_INSERT) == "t", "Expected an empty, writable fixture")
    sql(f"INSERT INTO slots SELECT generate_series({FIRST_SLOT}, {FIRST_SLOT + MAX_TICKS - 1})")
    data["baseline"] = book(port, 42, "control-42")
    control = [42, "ana", "control-42"]
    data["baseline_rows"] = stored()
    require(data["baseline"]["http_status"] == 201 and data["baseline"]["response"] ==
            {"claim_id": "control-42", "outcome": "Confirmed"} and data["baseline_rows"] == [control],
            "The control booking did not match its committed row")

    stop, events = Event(), Queue()
    monitor = Thread(target=sample, args=(port, stop, events, data["probes"]))
    monitor.start()
    try:
        require(next_probe(events)["http_status"] == 201, "First scheduled booking must succeed")
        policy("deploy fault", "REVOKE INSERT ON slot_claims FROM reservation_app", "f")
        failed = next_probe(events)
        while failed["http_status"] == 201:
            failed = next_probe(events)
        data["first_failed_utc"] = failed["completed_utc"]
        require(next_probe(events)["http_status"] == 500, "Expected a second consecutive failure")
        status, body = request(port, "GET", "/ready")
        data["readiness_during_fault"] = {"http_status": status, "response": body}
        require((status, body) == (200, {"ready": True}), "API readiness changed during the fault")
        logs = compose("logs", "--timestamps", "--no-log-prefix", "--no-color", "--tail", "200", "api")
        signal = f"claim {failed['claim_id']}: InsufficientPrivilege"
        data["operator_signal"] = next((line for line in logs.splitlines() if signal in line), None)
        require(data["operator_signal"], f"Missing API error log for {failed['claim_id']}")
        data["rows_during_fault"] = stored()
        require(control in data["rows_during_fault"], "Control disappeared during the fault")

        policy("restore policy", "GRANT INSERT ON slot_claims TO reservation_app", "t")
        recovered = next_probe(events)
        while recovered["http_status"] == 500:
            recovered = next_probe(events)
        data["first_recovered_utc"] = recovered["completed_utc"]
    finally:
        stop.set()
        monitor.join()

    data["final_rows"] = stored()
    expected_rows = [control] + [[p["slot_id"], "ana", p["claim_id"]] for p in data["probes"]
                                 if p["http_status"] == 201]
    require(data["final_rows"] == expected_rows,
            "Stored rows disagree with confirmed bookings or a failed booking left a claim")
    data["restored_images"] = images()
    require(data["deployed_images"] == data["restored_images"], "Image changed during the drill")
    start = datetime.fromisoformat(failed["completed_utc"].replace("Z", "+00:00"))
    end = datetime.fromisoformat(recovered["completed_utc"].replace("Z", "+00:00"))
    require(end >= start, "UTC clock moved backwards; interval is invalid")
    data["observed_recovery_seconds"] = (end - start).total_seconds()
    data["missed_ticks"] = data["probes"][-1]["tick"] + 1 - len(data["probes"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="new evidence JSON file")
    args = parser.parse_args()
    image = os.environ.get("RESERVATION_IMAGE")
    image_id = os.environ.get("EXPECTED_IMAGE_ID", "")
    revision = os.environ.get("SOURCE_REVISION", "")
    if not image or not re.fullmatch(r"sha256:[0-9a-f]{64}", image_id) or not re.fullmatch(r"[0-9a-f]{40}", revision):
        parser.error("Set RESERVATION_IMAGE, EXPECTED_IMAGE_ID and the full SOURCE_REVISION")
    metadata = command("docker", "image", "inspect", "--format",
                       '{{.Id}} {{index .Config.Labels "org.opencontainers.image.revision"}}', image)
    require(metadata == f"{image_id} {revision}", "Candidate image ID or source revision label differs")
    project = f"booking-drill-{uuid4().hex}"
    os.environ["RESERVATION_PORT"] = "0"

    def compose(*args, timeout=30):
        return command("docker", "compose", "-p", project, "-f", str(SERVICE / "compose.yaml"),
                       "-f", str(HERE / "tested-image.yaml"), *args, timeout=timeout)

    data = {
        "project": project, "source_revision": revision, "image_ref": image, "image_id": image_id,
        "pipeline_url": os.environ.get("PIPELINE_URL"), "probe_interval_seconds": PERIOD,
        "policy_changes": [], "probes": [], "result": "failed",
    }
    args.output.parent.mkdir(exist_ok=True, parents=True)
    with args.output.open("x", encoding="utf-8") as evidence:
        try:
            compose("up", "--no-build", "--wait", "--wait-timeout", "90", timeout=150)
            exercise(compose, data)
            data["result"] = "passed"
        finally:
            try:
                compose("down", "--volumes", timeout=90)
            except Exception:
                data["result"] = "failed"
                raise
            finally:
                json.dump(data, evidence, indent=2)
                evidence.write("\n")
    print(f"PASS: {data['observed_recovery_seconds']} seconds; evidence: {args.output}")


if __name__ == "__main__":
    sys.exit(main())
