"""HTTP entry point for the local reservation service."""

import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import psycopg

import booking


LAB_ACTORS = {
    "Bearer lab-ana": "ana",
    "Bearer lab-ben": "ben",
    "Bearer lab-guest": "guest",
}
HTTP_OUTCOMES = {
    "Confirmed": (201, "Confirmed"),
    "Replayed": (200, "Confirmed"),
    "SlotTaken": (409, "SlotTaken"),
    "Forbidden": (403, "Forbidden"),
}


class ReservationHandler(BaseHTTPRequestHandler):
    timeout = 5

    def respond(self, status, **payload):
        body = (json.dumps(payload) + "\n").encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        if status == 401:
            self.send_header("WWW-Authenticate", 'Bearer realm="reservation-lab"')
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path != "/ready":
            self.respond(404, error="NotFound")
            return
        try:
            with booking.connect("booking-api-ready") as conn:
                slot = conn.execute("SELECT 1 FROM slots WHERE slot_id = 42").fetchone()
                ready = slot is not None
        except psycopg.Error:
            ready = False
        self.respond(200 if ready else 503, ready=ready)

    def read_claim_id(self):
        lengths = self.headers.get_all("Content-Length", [])
        if self.headers.get_content_type() != "application/json" or len(lengths) != 1:
            raise ValueError
        if not lengths[0].isascii() or not lengths[0].isdecimal():
            raise ValueError
        length = int(lengths[0])
        if not 0 < length <= 1024 or "Transfer-Encoding" in self.headers:
            raise ValueError
        body = self.rfile.read(length)
        if len(body) != length:
            raise ValueError
        data = json.loads(body.decode("utf-8"))
        if not isinstance(data, dict) or set(data) != {"claim_id"}:
            raise ValueError
        if not booking.valid_id(data["claim_id"]):
            raise ValueError
        return data["claim_id"]

    def do_POST(self):
        match = re.fullmatch(r"/slots/([1-9][0-9]{0,9})/claims", self.path)
        if match is None or int(match[1]) > 2_147_483_647:
            self.respond(404, error="NotFound")
            return
        slot_id = int(match[1])
        actor = LAB_ACTORS.get(self.headers.get("Authorization"))
        if actor is None:
            self.respond(401, error="Unauthenticated")
            return
        try:
            claim_id = self.read_claim_id()
        except (ValueError, RecursionError, TimeoutError):
            self.respond(400, error="InvalidClaim")
            return

        failure = "StoreUnavailable"
        try:
            with booking.connect("booking-api") as conn:
                result = booking.reserve(conn, actor, slot_id, claim_id)
                # Exiting this context commits. A lost reply here leaves the result unknown.
                failure = "CommitUnknown"
        except booking.SlotNotFound:
            self.respond(404, claim_id=claim_id, error="SlotNotFound")
            return
        except (psycopg.OperationalError, psycopg.InterfaceError):
            self.respond(503, claim_id=claim_id, error=failure)
            return
        except (psycopg.Error, RuntimeError) as error:
            self.log_error("claim %s: %s", claim_id, type(error).__name__)
            self.respond(500, claim_id=claim_id, error="InternalError")
            return
        status, outcome = HTTP_OUTCOMES[result]
        self.respond(status, claim_id=claim_id, outcome=outcome)


if __name__ == "__main__":
    with ThreadingHTTPServer(("0.0.0.0", 8080), ReservationHandler) as server:
        server.serve_forever()
