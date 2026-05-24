# References and Adoption Notes

The sources below supply authoritative platform behavior or widely used
security guidance. This playbook adapts them into a practical baseline for
containerized projects, automation pipelines and public portfolio workloads.
Its control levels, naming examples and recommended minimum implementation are
local conventions, not certification claims.

## External Guidance and Adoption

| Source | Original guidance used | Adoption in this playbook |
| --- | --- | --- |
| GitHub Docs, *Security hardening for GitHub Actions* | Limit token permissions, protect secrets, consider OIDC and pin actions to full-length SHAs. | Explicit workflow permissions, protected production secrets, OIDC recommendation and immutable pinning for privileged workflows. |
| GitHub Docs, *About push protection* | Detect and block supported secrets during pushes in supported scenarios. | Enable secret scanning/push protection where available; still rotate any exposed credential. |
| Docker Docs, *Access tokens* | Use personal access tokens for CLI/authentication and manage token permissions and lifecycle. | Use tokens rather than passwords for CI registry access; split publish and pull authority where feasible. |
| Docker Docs, *Build secrets* | Pass build secrets through secret mounts rather than `ARG` or `ENV`, which persist in images or metadata. | Never bake secrets into images; use runtime or build secret delivery mechanisms. |
| Kubernetes Docs, *Good practices for Kubernetes Secrets* | Restrict Secret access, consider encryption at rest and avoid exposing secrets through workloads and manifests. | Treat platform secrets as restricted runtime inputs and apply stronger stores/encryption for production. |
| Kubernetes Docs, *Pod Security Standards* | Defines baseline and restricted security profiles for pods. | Prefer non-root and restricted workload settings when operating Kubernetes workloads. |
| OWASP, *Secrets Management Cheat Sheet* | Centralize, scope, rotate, audit and protect secrets through their lifecycle. | Lifecycle record, rotation guidance and vaulting maturity options. |
| OWASP, *Logging Cheat Sheet* | Exclude credentials and sensitive data from logs; retain security-relevant events safely. | Structured logs include diagnostic identifiers, not live secret values. |
| OWASP, *Docker Security Cheat Sheet* | Use trusted images, non-root users, least privileges and avoid secrets in images. | Container baseline and optional runtime hardening rules. |
| NIST SP 800-61 Rev. 3, *Incident Response Recommendations and Considerations for Cybersecurity Risk Management* | Integrates incident response preparation, detection, response and recovery considerations into cybersecurity risk management. | Lightweight contain, assess, recover and improve sequence for credential and artifact incidents. |
| SLSA Specification, *Supply-chain Levels for Software Artifacts* | Defines supply-chain integrity levels and attestation formats, including provenance. | Provenance/signature verification is recommended as impact and artifact consumers grow. |
| The Twelve-Factor App, *Config* | Keep deploy-varying configuration outside code in the environment. | Stable environment variable interfaces and no committed deployment secrets. |

## Source Links

- GitHub Docs, *Security hardening for GitHub Actions*:
  <https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions>
- GitHub Docs, *About push protection*:
  <https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection>
- Docker Docs, *Personal access tokens*:
  <https://docs.docker.com/security/for-developers/access-tokens/>
- Docker Docs, *Organization access tokens*:
  <https://docs.docker.com/security/for-admins/access-tokens/>
- Docker Docs, *Build secrets*:
  <https://docs.docker.com/build/building/secrets/>
- Kubernetes Docs, *Good practices for Kubernetes Secrets*:
  <https://kubernetes.io/docs/concepts/security/secrets-good-practices/>
- Kubernetes Docs, *Pod Security Standards*:
  <https://kubernetes.io/docs/concepts/security/pod-security-standards/>
- OWASP, *Secrets Management Cheat Sheet*:
  <https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html>
- OWASP, *Logging Cheat Sheet*:
  <https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html>
- OWASP, *Docker Security Cheat Sheet*:
  <https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html>
- NIST SP 800-61 Rev. 3, *Incident Response Recommendations and Considerations
  for Cybersecurity Risk Management*:
  <https://csrc.nist.gov/pubs/sp/800/61/r3/final>
- SLSA, *SLSA Specification*:
  <https://slsa.dev/spec/>
- The Twelve-Factor App, *Config*:
  <https://12factor.net/config>

## Extending the Standard

Before adding a control:

1. Identify the concrete asset or failure mode it protects.
2. Link authoritative platform behavior or security guidance where applicable.
3. State whether it is baseline, recommended or advanced.
4. Describe its operational cost, ownership and recovery path.
5. Provide a smaller practical control if the advanced option is unsuitable
   for a personal or lab environment.
