"""Serve synthetic receipt requests for the Linux write-permission lab."""

import argparse
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


RECEIPTS = {
    f"/receipts/{name}": name for name in ("baseline.txt", "denied.txt", "recovered.txt")
}


class ReceiptHandler(BaseHTTPRequestHandler):
    def reply(self, status, message):
        body = f"{message}\n".encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self.reply(200, "ready")
        else:
            self.reply(404, "not found")

    def do_POST(self):
        name = RECEIPTS.get(self.path)
        if name is None:
            self.reply(404, "not found")
            return

        target = self.server.receipt_dir / name
        try:
            with target.open("x", encoding="utf-8") as receipt:
                receipt.write(f"receipt {name}\n")
        except FileExistsError:
            self.reply(409, "already exists")
        except OSError as error:
            print(f"{self.command} {self.path} path={target} error={error.strerror}",
                  file=sys.stderr, flush=True)
            self.reply(500, "write failed")
        else:
            self.reply(201, f"created {name}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="absolute path to the receipt directory")
    args = parser.parse_args()
    if os.geteuid() == 0:
        parser.error("start the service as an unprivileged user")
    if not args.directory.is_absolute() or not args.directory.is_dir():
        parser.error("supply an existing directory by its absolute path")

    with HTTPServer(("127.0.0.1", 18083), ReceiptHandler) as server:
        server.receipt_dir = args.directory
        server.serve_forever()


if __name__ == "__main__":
    main()
