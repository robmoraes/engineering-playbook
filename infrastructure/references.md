# References

This section uses official platform and reliability guidance to ground
operational behavior. The specific topology tiers, checklist structure and
small-platform recommendations are local standards adapted for this
playbook, not mandates from the cited sources.

## Adopted and Adapted Guidance

| Source | Source guidance used | Convention adopted here |
| --- | --- | --- |
| Docker Docs, *Swarm mode*, *Deploy services to a swarm*, *Manage swarm service networks* and *Administer and maintain a swarm of Docker Engines* | Swarm uses declarative services, managers reconcile desired state, overlay networking supports service communication, and manager quorum/control-state recovery require operational care. | Swarm guidance addresses manager quorum, overlay segmentation, immutable deployments and cluster recovery for small platforms that choose Swarm. |
| Kubernetes Docs, *Cluster Architecture*, *Nodes*, *Services* and *Production environment* | Kubernetes operates workloads through a control plane and nodes; production use commonly requires multiple control-plane/nodes and deliberate resilience planning; Services provide stable network exposure for Pods. | Kubernetes is documented as a platform choice with control-plane, policy, storage and operational costs, not a universal default. |
| AWS Well-Architected Framework, *Reliability Pillar* | Reliability practices include fault isolation, monitoring, immutable changes, automated/protected backups, recovery testing and stated recovery objectives. | Infrastructure HA/DR decisions must state addressed failure domains, backups, restore validation and accepted cost. |
| AWS Well-Architected Framework, *Cost Optimization - data transfer* | Network placement and cross-Availability Zone traffic can affect operating cost and should be measured and selected intentionally. | Multi-zone reliability and traffic cost are evaluated together rather than optimized in isolation. |
| Google, *Site Reliability Engineering - Monitoring Distributed Systems* and *Practical Alerting from Time-Series Data* | Monitoring supports operational decisions; alerts should be actionable for human response and tied to service behavior. | Infrastructure monitoring covers user-impacting routes, capacity, state, control-plane behavior and recovery actions without paging on every event. |
| HashiCorp Terraform Docs, *State* | Terraform state maps configuration to real infrastructure objects and must be stored/handled appropriately for shared operation. | Production IaC state is treated as protected control data and is not committed to repositories. |
| The Twelve-Factor App, *Config* and *Backing Services* | Configuration varies between deployments and backing services should be attached resources. | Runtime configuration/secrets remain outside immutable artifacts and stateful dependencies are documented infrastructure resources. |

## Source Links

- Docker Docs, *Swarm mode*: <https://docs.docker.com/engine/swarm/>
- Docker Docs, *Deploy services to a swarm*:
  <https://docs.docker.com/engine/swarm/services/>
- Docker Docs, *Manage swarm service networks*:
  <https://docs.docker.com/engine/swarm/networking/>
- Docker Docs, *Administer and maintain a swarm of Docker Engines*:
  <https://docs.docker.com/engine/swarm/admin_guide/>
- Kubernetes Docs, *Cluster Architecture*:
  <https://kubernetes.io/docs/concepts/architecture/>
- Kubernetes Docs, *Nodes*: <https://kubernetes.io/docs/concepts/architecture/nodes/>
- Kubernetes Docs, *Service*:
  <https://kubernetes.io/docs/concepts/services-networking/service/>
- Kubernetes Docs, *Production environment*:
  <https://kubernetes.io/docs/setup/production-environment/>
- AWS Well-Architected Framework, *Reliability Pillar*:
  <https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html>
- AWS Well-Architected Framework, *COST08-BP02 Select components to optimize data transfer cost*:
  <https://docs.aws.amazon.com/wellarchitected/latest/framework/cost_data_transfer_optimized_components.html>
- Google, *Site Reliability Engineering - Monitoring Distributed Systems*:
  <https://sre.google/sre-book/monitoring-distributed-systems/>
- Google, *Site Reliability Engineering - Practical Alerting from Time-Series Data*:
  <https://sre.google/sre-book/practical-alerting/>
- HashiCorp Terraform Docs, *State*:
  <https://developer.hashicorp.com/terraform/language/state>
- The Twelve-Factor App, *Config*: <https://12factor.net/config>
- The Twelve-Factor App, *Backing Services*: <https://12factor.net/backing-services>

## Local Conventions

- The maturity model is a local tool for proportional infrastructure rigor; it
  is not a certification or external SRE standard.
- A simple single-host production design is permitted when its limitations,
  recovery path and data handling are explicit.
- Shared platform services are introduced only with ownership and consumer
  impact documented.
- Cost and reliability are reviewed together; redundancy without an operated
  failure/recovery model is not considered maturity.
