# Diagnose an HTTP 502 from a reverse proxy

A client requests `GET /health` from NGINX and receives `502 Bad Gateway`.
In this lab the intended path is **client → 127.0.0.1:18080 (NGINX) →
127.0.0.1:18081 (backend)**. The exercise reproduces two causes of the same
upstream connection error. Use the backend process and its listening socket
to choose the repair.

## Set up a local Linux lab

Use three Bash terminals on the same Linux machine, as the same regular user
in the same network and PID namespaces. The **observer** runs all diagnostics.
The **proxy** and **backend** terminals each own one foreground service.
Use NGINX with the standard HTTP modules and the `-e` option, Python 3.7+
with `http.server`, curl, `ss` (iproute2) and `ps` (procps). All three
ports bind to loopback. The backend serves one synthetic file.

In the **observer** terminal, check the ports before starting. Expect no
rows. If a port already has a listener, use another lab environment.

```bash
ss -H -ltn '( sport = :18080 or sport = :18081 or sport = :18082 )'
```

From the repository root in the **observer** terminal, create a private
directory for this run. Copy the printed `cd` command into the **proxy**
and **backend** terminals.

```bash
lab=$(mktemp -d)
cp examples/operational-scenarios/network-and-tls/reverse-proxy-502/nginx.conf "$lab/"
mkdir "$lab/site"
printf 'booking-backend-ok\n' > "$lab/site/health"
printf 'cd %q\n' "$lab"
```

In the **proxy** terminal, after changing directory, validate and start
the supplied [NGINX configuration](./nginx.conf). Its PID, logs and temporary
files are relative to this lab prefix. Leave it running for both faults.

```bash
nginx -e stderr -p "$PWD/" -c nginx.conf -t &&
  nginx -e stderr -p "$PWD/" -c nginx.conf
```

In the **backend** terminal, after changing directory, define the following
function and start the server. The subshell records its PID, then `exec`
starts Python under that same PID. Wait for its serving message before each
probe. Ctrl+C in this terminal stops just this foreground service.

```bash
serve() (
  printf '%s\n' "$BASHPID" > backend.pid
  exec python3 -m http.server "$1" --bind 127.0.0.1 --directory "$PWD/site"
)
serve 18081
```

## Record a healthy request

In the **observer** terminal, define the client request once. It prints
the HTTP status and body even for a 502. Use this same request after each
repair. Confirm the destination in the config used to launch the proxy.

```bash
probe() {
  curl --noproxy '*' --silent --show-error --max-time 3 \
    --output "$lab/response" --write-out 'HTTP %{http_code}\n' \
    http://127.0.0.1:18080/health && cat "$lab/response"
}
grep 'proxy_pass' "$lab/nginx.conf"
probe
```

Expect `proxy_pass http://127.0.0.1:18081;` and the following response.
Start fault injection only after both the status and body match.

```text
HTTP 200
booking-backend-ok
```

## Collect evidence for each 502

Define this function in the **observer** terminal. It takes a log position
before the request so the second fault cannot reuse the first fault's
error line. The PID file holds the identity of the last launched backend.
Compare it with the command in `ps` and the PID in the socket's `users:`
field. An empty `ss` result means neither backend port has a TCP listener.

```bash
inspect_fault() {
  local previous_lines backend_pid
  previous_lines=$(wc -l < "$lab/error.log")
  probe
  tail -n "+$((previous_lines + 1))" "$lab/error.log"
  backend_pid=$(cat "$lab/backend.pid")
  printf 'Recorded backend PID %s\n' "$backend_pid"
  ps -p "$backend_pid" -o pid=,stat=,args= || echo 'No process at recorded PID'
  ss -H -ltnp '( sport = :18081 or sport = :18082 )'
}
```

### Fault 1 — the backend stopped

1. Press Ctrl+C in the **backend** terminal and wait for its shell prompt.
2. Run `inspect_fault` in the **observer** terminal. Expect `HTTP 502` and
   an NGINX error page. The fresh error log should contain
   `connect() failed (111: Connection refused) while connecting to upstream`
   and `upstream: "http://127.0.0.1:18081/health"`. The recorded PID is
   gone and the socket query returns no rows.
3. In the **backend** terminal, run `serve 18081`. In the **observer**
   terminal, repeat `probe`. Record `HTTP 200` and `booking-backend-ok`
   before starting the second fault.

### Fault 2 — the backend is listening on the wrong port

1. Press Ctrl+C in the **backend** terminal. Run `serve 18082` and wait
   for its serving message.
2. Run `inspect_fault` in the **observer** terminal. Expect the same 502
   and a new connection refusal for `127.0.0.1:18081/health`. This time
   `ps` shows a live `python3 -m http.server 18082`. The `ss` line for
   `127.0.0.1:18082` shows that process's PID. There is no listener on
   the configured upstream port, `18081`.
3. Correct the backend launch port. Press Ctrl+C in the **backend**
   terminal and run `serve 18081`. In the **observer** terminal, repeat
   `probe` and record `HTTP 200` and `booking-backend-ok`.

In a rehearsal on Ubuntu 24.04 with NGINX 1.24.0, the following
observations distinguished the two failures. PIDs vary by run.

| Observation | Backend stopped | Backend on the wrong port |
| --- | --- | --- |
| NGINX error for this request | Connection refused on `127.0.0.1:18081` | Connection refused on `127.0.0.1:18081` |
| `ps` for the recorded backend | PID `1179696` absent | PID `1179713` running `http.server 18082` |
| `ss` for the two backend ports | No listener | PID `1179713` listening on `127.0.0.1:18082` |
| `GET /health` through the proxy after repair | `200`, `booking-backend-ok` | `200`, `booking-backend-ok` |

If the process, socket and fresh error line disagree, preserve those
observations and the client response before making another change. On a
shared service, hand them to the proxy and backend owners. In a
containerized deployment, inspect the listener in the backend's namespace
and test reachability from the proxy's namespace. Each has its own loopback
address when the two use separate network namespaces.

## Clean up

Press Ctrl+C in the **backend** and **proxy** terminals and wait for both
shell prompts. In the **observer** terminal, run the socket check again.
After confirming it returns no rows, remove the private directory created
for this run.

```bash
ss -H -ltn '( sport = :18080 or sport = :18081 or sport = :18082 )'
rm -r -- "$lab"
```

For the operating standards, see [Networking and Edge](../../../../infrastructure/networking-and-edge.md)
and the [network incident runbook](../../../../runbooks/network-edge-dns-and-tls.md).
NGINX documents how it forwards the request to the selected upstream, and
the Linux socket tool documents how it displays the owning process.
[NGINX proxy_pass](https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass)
and [ss(8)](https://man7.org/linux/man-pages/man8/ss.8.html).
