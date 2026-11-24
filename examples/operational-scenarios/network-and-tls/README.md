# Network and TLS Scenarios

This family covers DNS, certificates, reverse proxy routing and internal
connectivity. Use synthetic endpoints and confirm recovery through the
same route that first showed the symptom.

| Symptom | Exercise |
| --- | --- |
| NGINX returns HTTP 502 for a backend request | [Distinguish a stopped backend from one listening on the wrong port](./reverse-proxy-502/README.md) |
