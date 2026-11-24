# Diagnose a service that can answer requests but cannot write a file

A receipt service passes `GET /health`, yet a customer gets an error when
creating a receipt. Trace the failed `POST` to the service's Linux identity,
locate the missing permission, then repeat the operation with a fresh name.

## Start the lab

Use Bash and Docker on a disposable Linux host. From the repository root,
start an isolated container and copy in the [receipt service](./receipt-service.py).
The HTTP client and server both run on the container's loopback interface.
All files and numeric identities used below belong to this lab.

```bash
lab=$(docker run --rm -d --network none python:3.13-slim-bookworm sleep infinity)
docker cp examples/operational-scenarios/runtime-and-platform/service-write-permission/receipt-service.py "$lab:/tmp/receipt-service.py"
docker exec -it "$lab" bash
```

Run the following commands **inside that same container shell** until cleanup.
The shell has authority to prepare the fixture and change its permissions.
The directory owner (UID 20001) and the service (UID 10001, GID 10001) are
distinct. Record the original numeric owners, groups and modes before
starting the service.

```bash
umask 077
labdir=/srv/receipt-lab
outbox=$labdir/outbox
install -d -o 20001 -g 10001 -m 0710 "$labdir"
install -d -o 20001 -g 10001 -m 0770 "$outbox"
chmod 0444 /tmp/receipt-service.py
record_modes() { stat -c '%n %u:%g %a' "$labdir" "$outbox"; }
record_modes | tee /tmp/receipt-modes.before

setpriv --reuid=10001 --regid=10001 --clear-groups --no-new-privs \
  python /tmp/receipt-service.py "$outbox" >/tmp/receipt-service.log 2>&1 &
service_pid=$!
```

Expect `20001:10001 710` for the parent and `20001:10001 770` for the
outbox. The service group can traverse the parent and create files in the
outbox. Other users have no access to either directory.

## Establish the user-visible baseline

Define a small client that prints both status and response body. Use it for
all three receipt requests. Each name is synthetic and may be created once.

```bash
request() {
  python - "$@" <<'PY'
import sys
from http.client import HTTPConnection

method, path = sys.argv[1:]
client = HTTPConnection("127.0.0.1", 18083, timeout=3)
client.request(method, path)
response = client.getresponse()
print(f"HTTP {response.status} {response.read().decode().strip()}")
client.close()
PY
}
wait_ready() {
  local attempt
  for attempt in {1..30}; do
    if [[ "$(request GET /health 2>/dev/null)" == 'HTTP 200 ready' ]]; then
      echo 'HTTP 200 ready'
      return 0
    fi
    sleep 0.1
  done
  echo 'Readiness check timed out' >&2
  cat /tmp/receipt-service.log >&2
  return 1
}
```

Gate the first write on the health response. If startup times out, inspect
the service log before proceeding.

```bash
wait_ready &&
  request POST /receipts/baseline.txt &&
  stat -c '%u:%g %a %n' "$outbox/baseline.txt" &&
  cat "$outbox/baseline.txt"
```

Before changing permissions, confirm `HTTP 201 created baseline.txt` and
a file owned by `10001:10001` with mode `600` and content
`receipt baseline.txt`.

## Reproduce the failure and identify the missing permission

As the lab operator, remove the **group write bit on the outbox**. Send the
same kind of request with a new name. Read the service log for this specific
request and path, and check whether a file appeared.

```bash
chmod g-w "$outbox"
request POST /receipts/denied.txt
request GET /health
grep -F "POST /receipts/denied.txt path=$outbox/denied.txt" /tmp/receipt-service.log
test ! -e "$outbox/denied.txt" && echo 'denied.txt is absent'
```

Expect `HTTP 500 write failed`, `HTTP 200 ready` and no new file. The
matching log line identifies the path the service tried to create.

```text
POST /receipts/denied.txt path=/srv/receipt-lab/outbox/denied.txt error=Permission denied
```

Collect the following evidence **before repairing** the directory.

```bash
grep -E '^(Name|State|Uid|Gid|Groups|CapEff):' "/proc/$service_pid/status"
namei -l "$outbox"
record_modes
setpriv --reuid=20001 --regid=20001 --clear-groups test -w "$outbox" &&
  echo 'The directory owner still has write access'
```

- The original PID still exists. The second and fourth entries of `Uid`
  and `Gid` are the effective and filesystem IDs. Both are 10001 here.
  `Groups` is empty (no supplementary groups), and `CapEff` is zero.
- `namei -l` shows search permission (`x`) on each directory in the path.
  `/` and `/srv` allow traversal, and group 10001 has `x` on
  `receipt-lab` and `outbox`.
- The outbox is still `20001:10001`, now mode `750`. UID 20001 can still
  write as its owner. The service matches the group, whose permissions are
  now `r-x`. Creating the new entry requires both `w` and `x` on that
  directory. The missing bit is `g+w` on the outbox.

## Restore access and prove recovery

Restore that one bit, compare the directory metadata with the baseline,
then submit a fresh receipt through the running service.

```bash
chmod g+w "$outbox"
record_modes | diff -u /tmp/receipt-modes.before -
request POST /receipts/recovered.txt
stat -c '%u:%g %a %n' "$outbox/recovered.txt"
cat "$outbox/recovered.txt"
grep -E '^(Uid|Gid|Groups|CapEff):' "/proc/$service_pid/status"
```

An empty diff confirms the original owners, groups and modes. Expect
`HTTP 201 created recovered.txt` and a new file containing
`receipt recovered.txt`, owned by `10001:10001` with mode `600`. The
same service PID still has its original credentials. This correction gives
the service group the required write access and keeps other users excluded.

If the actual path, credentials or mode differ, preserve the request, log
and process evidence for the storage owner. Check mount options, ACLs or
security policy before changing any further permissions. See
[Storage, Backup and Recovery](../../../../infrastructure/storage-backup-and-recovery.md)
and the [container troubleshooting runbook](../../../../runbooks/containers-and-orchestration.md).

## Clean up

Run `exit` to leave the container shell. In the **original host shell**,
stop the lab container. Docker removes the container and its synthetic
files because it was started with `--rm`.

```bash
docker stop "$lab"
```

The Linux manuals describe credential fields, directory search permission,
and file creation failures.
[proc_pid_status(5)](https://man7.org/linux/man-pages/man5/proc_pid_status.5.html),
[path_resolution(7)](https://man7.org/linux/man-pages/man7/path_resolution.7.html)
and [open(2)](https://man7.org/linux/man-pages/man2/open.2.html).
