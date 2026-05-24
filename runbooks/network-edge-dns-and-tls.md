# Network, Edge, DNS and TLS

Use this runbook when a service is healthy internally but unreachable, fails
TLS validation or cannot communicate through expected network paths.

## External Route Assessment

Start from the route users consume:

```bash
curl --fail --silent --show-error --verbose https://api.example.com/health
curl --head --silent --show-error https://api.example.com/
```

Record:

- DNS name and environment;
- error type: resolution, TCP timeout/refusal, TLS, HTTP status or backend
  application behavior;
- whether impact is global or limited to a route/network;
- recent DNS, certificate, proxy, load-balancer or deployment change.

## DNS Diagnostics

Symptoms:

- name does not resolve;
- old target remains in use;
- only some networks/regions fail;
- certificate is valid for another host due to incorrect route.

Checks:

```bash
dig +short api.example.com
dig api.example.com
getent hosts api.example.com
```

Investigate:

- expected record and target;
- record TTL and propagation expectations;
- provider health/alias/load-balancer target;
- whether staging and production hostnames were confused;
- internal cluster/service DNS separately from public DNS.

Do not change DNS blindly during an outage. A wrong record plus cached TTL can
extend impact and complicate rollback.

## TLS and Certificate Diagnostics

Symptoms:

- browser/client certificate expiry or hostname mismatch;
- failed TLS handshake;
- ingress route works only over HTTP;
- certificate renewal alert.

Checks:

```bash
openssl s_client -connect api.example.com:443 -servername api.example.com </dev/null
curl --verbose https://api.example.com/health
```

Verify:

- certificate subject/SAN matches hostname;
- expiry and renewal ownership;
- expected certificate is presented at the actual ingress;
- proxy/load-balancer configuration selects intended certificate;
- backend TLS requirements where encryption continues internally.

Recovery may require renewing/replacing certificate configuration and
reloading/redeploying ingress. Validate externally after change and monitor
renewal to avoid recurrence.

## Reverse Proxy and Ingress Diagnostics

| Observation | Next check |
| --- | --- |
| TLS succeeds, HTTP `502`/`503` | backend health, service discovery, proxy route and network attachment |
| Correct backend works privately, public route fails | ingress config, load balancer target and edge network |
| One host/path fails | routing configuration and certificate/hostname mapping |
| All edge routes fail | shared proxy/load balancer capacity, certificate, DNS or node failure |

Check proxy logs and metrics without exposing headers or credentials. Confirm
whether the proxy is a shared failure domain before applying restart or
configuration change.

## Internal Connectivity and Service Discovery

For Docker Swarm:

- confirm source and destination services share only required overlay
  networks;
- inspect service/task placement and overlay health symptoms;
- verify firewall changes affecting node-to-node paths;
- distinguish published routing-mesh behavior from direct host-mode routing.

For Kubernetes:

- verify `Service` selectors/endpoints and affected Pods;
- check cluster DNS behavior from an authorized diagnostic Pod where needed;
- review network policy or ingress/gateway changes.

Example Kubernetes read-only checks:

```bash
kubectl get service,endpoints -n <namespace>
kubectl describe service <service> -n <namespace>
kubectl get ingress -n <namespace>
```

## Validation

- intended public DNS resolves to the expected ingress path;
- TLS certificate validates for intended hostname;
- public route returns expected health/smoke response;
- internal service-to-dependency route works only where required;
- proxy/error metrics and logs show recovery;
- any emergency edge or DNS change is recorded and reconciled in managed
  configuration.
