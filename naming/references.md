# References and Adoption Notes

This playbook deliberately applies a conservative shared naming subset across
systems. External documents below provide platform constraints or established
semantic vocabulary. Rules such as the single environment vocabulary,
`<system>-<component>` ordering and Docker tag promotion policy are local
standards adopted here for operational consistency; they are not claimed as
requirements of those external projects.

## External Constraints and Recommendations

| Source | Relevant external guidance | Adoption in this playbook |
| --- | --- | --- |
| Kubernetes, *Object Names and IDs* | Most object names use DNS subdomain syntax; some use DNS label restrictions. | Default runtime slugs are lowercase DNS-safe and start with a letter; operational segments target 63 characters or fewer. |
| Kubernetes, *Labels and Selectors* | Label keys support an optional DNS prefix and constrained name/value segments. | Kubernetes-facing metadata uses DNS-prefixed custom labels and stable selector values. |
| Kubernetes, *Recommended Labels* | Defines shared `app.kubernetes.io/*` labels for application metadata. | These labels are used as the default Kubernetes-compatible workload identity vocabulary. |
| Docker Docs, *docker image tag* | Image references are structured as `[HOST[:PORT]/]NAMESPACE/REPOSITORY[:TAG]`. | Registry, namespace, image repository and tag are treated as distinct naming decisions. |
| Docker Docs, *Deploy a stack to a swarm* | Swarm prefixes network, volume and service names with the stack name. | Stack name includes application and environment; nested service names remain concise. |
| GitHub Docs, *Workflow syntax for GitHub Actions* | Workflow files live in `.github/workflows`; `name`, `run-name` and job IDs have separate roles and job-ID syntax limits. | Files are kebab-case, UI text is readable and job IDs are snake_case. |
| GitHub Docs, *Dealing with special characters in branch and tag names* | Simple branch/tag characters reduce shell escaping; `/` can provide structure. | Branches use one type prefix and a safe, readable description. |
| The Twelve-Factor App, *Config* | Deploy-varying configuration should be stored in environment variables rather than committed code. | Environment variable keys are stable across environments; deployments provide values. |
| Prometheus, *Metric and label naming* | Metrics should describe one quantity, use base-unit suffixes and avoid high-cardinality labels. | Metric identifiers and label rules follow Prometheus-compatible snake_case and bounded dimensions. |
| OpenTelemetry Semantic Conventions, *Service* | Defines `service.name`, `service.namespace`, `service.version` and service instance identity. | Logs and traces separate stable service, version and instance identity. |
| OpenTelemetry Semantic Conventions, *Deployment* | Defines `deployment.environment.name` and well-known values including `development`, `staging`, `production` and `test`. | Telemetry maps short owned environment slugs such as `prod`/`stg` to `production`/`staging`. |
| RFC 1123, *Requirements for Internet Hosts - Application and Support* | Defines host-related DNS naming foundations used by modern platforms. | DNS-safe lowercase labels form the portability baseline for runtime names. |

## Source Links

- Kubernetes, *Object Names and IDs*: <https://kubernetes.io/docs/concepts/overview/working-with-objects/names/>
- Kubernetes, *Labels and Selectors*: <https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/>
- Kubernetes, *Recommended Labels*: <https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/>
- Docker Docs, *docker image tag*: <https://docs.docker.com/reference/cli/docker/image/tag/>
- Docker Docs, *Deploy a stack to a swarm*: <https://docs.docker.com/engine/swarm/stack-deploy/>
- GitHub Docs, *Workflow syntax for GitHub Actions*: <https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax>
- GitHub Docs, *Dealing with special characters in branch and tag names*: <https://docs.github.com/en/get-started/using-git/dealing-with-special-characters-in-branch-and-tag-names>
- The Twelve-Factor App, *Config*: <https://12factor.net/config>
- Prometheus, *Metric and label naming*: <https://prometheus.io/docs/practices/naming/>
- OpenTelemetry Semantic Conventions, *Service*: <https://opentelemetry.io/docs/specs/semconv/resource/service/>
- OpenTelemetry Semantic Conventions, *Deployment*: <https://opentelemetry.io/docs/specs/semconv/registry/entities/deployment/>
- RFC Editor, *RFC 1123*: <https://www.rfc-editor.org/info/rfc1123>

## How to Extend This Standard

When a new platform is introduced:

1. Record its official identifier restrictions in this file.
2. Reuse the core slug unless the platform requires a different syntax.
3. Document any translation at the boundary rather than creating competing
   names for all existing resources.
4. Add positive and negative examples that can be checked during review.
