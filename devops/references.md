# References And Adoption Notes

This section uses established delivery, organizational, platform, security and
reliability guidance. The sources describe capabilities and evidence; this
playbook converts them into a proportional personal operating standard rather
than a certification model or a mandatory organization design.

## External Guidance And Adoption

| Source | Relevant external guidance | Adoption in this playbook |
| --- | --- | --- |
| Agile Manifesto, *Principles behind the Agile Manifesto* | Deliver valuable working software early and frequently, collaborate across roles, sustain the work and regularly adapt the process. | DevOps work begins with outcomes, uses incremental change and includes regular evidence-based improvement. |
| DORA, *Software delivery performance metrics* | The current model evaluates throughput and instability with five service-context metrics; it warns against targets, inappropriate comparison and siloed ownership. | Change lead time, deployment frequency, failed deployment recovery time, change fail rate and deployment rework rate are used together for service improvement, never individual ranking. |
| DORA, *Value stream mapping for software delivery* | Visualizing work, wait time, handoffs and recovery flow helps teams find constraints and improve outcomes iteratively. | Map the real end-to-end path only to the detail needed to select one material improvement. |
| DORA, *Continuous integration*, *Continuous delivery* and *Trunk-based development* | Frequent mainline integration, short-lived branches, fast automated validation and deployable software support delivery speed and stability. | Small frequent integration is the default; continuous production deployment remains an explicit context-dependent choice. |
| DORA, *Working in small batches* and *Work in process limits* | Small batches and bounded WIP reduce feedback delay, expose constraints and support flow. | Split work by coherent verifiable behavior, limit active work and address blocked flow instead of starting more work. |
| DORA, *Generative organizational culture* | High-trust cultures emphasize information flow, cooperation, shared risk, inquiry after failure and safe experimentation. | Surface bad news early, use blameless technical inquiry and share lifecycle risks without making ownership anonymous. |
| CNCF TAG App Delivery, *Platforms White Paper* and *Platform Engineering Maturity Model* | Platforms curate capabilities around internal-user needs, support self-service, reduce cognitive load and require product thinking and intentional maturity. | Introduce paved paths and shared capabilities only for verified consumers, with secure defaults, ownership, feedback and escape paths. |
| NIST SP 800-218, *Secure Software Development Framework (SSDF) Version 1.1* | Secure development practices should be integrated into each SDLC implementation to reduce vulnerabilities, impact and recurrence. | Security is part of design, validation, delivery and learning rather than a final downstream gate. |
| Google, *How SRE Relates to DevOps* | DevOps is a broad whole-lifecycle collaboration philosophy; SRE supplies more opinionated service-operation practices and reliability mechanisms. | DevOps is the baseline operating model; the SRE section owns detailed reliability policy without duplicating this section. |
| Google SRE, *Postmortem Culture: Learning from Failure* | Blameless postmortems examine contributing conditions and produce preventive action rather than scapegoating. | Material failures receive technically specific review and owned follow-up through the runbook standard. |

## Source Links

- Agile Manifesto, *Principles behind the Agile Manifesto*:
  <https://agilemanifesto.org/principles.html>
- DORA, *Software delivery performance metrics*:
  <https://dora.dev/guides/dora-metrics/>
- DORA, *Value stream mapping for software delivery*:
  <https://dora.dev/guides/value-stream-management/>
- DORA, *Continuous integration*:
  <https://dora.dev/capabilities/continuous-integration/>
- DORA, *Continuous delivery*:
  <https://dora.dev/capabilities/continuous-delivery/>
- DORA, *Trunk-based development*:
  <https://dora.dev/capabilities/trunk-based-development/>
- DORA, *Working in small batches*:
  <https://dora.dev/capabilities/working-in-small-batches/>
- DORA, *Work in process limits*:
  <https://dora.dev/capabilities/wip-limits/>
- DORA, *Generative organizational culture*:
  <https://dora.dev/capabilities/generative-organizational-culture/>
- CNCF TAG App Delivery, *Platforms White Paper*:
  <https://tag-app-delivery.cncf.io/whitepapers/platforms/>
- CNCF TAG App Delivery, *Platform Engineering Maturity Model*:
  <https://tag-app-delivery.cncf.io/whitepapers/platform-eng-maturity-model/>
- NIST SP 800-218, *Secure Software Development Framework (SSDF) Version 1.1*:
  <https://csrc.nist.gov/pubs/sp/800/218/final>
- Google, *How SRE Relates to DevOps*:
  <https://sre.google/workbook/how-sre-relates/>
- Google SRE, *Postmortem Culture: Learning from Failure*:
  <https://sre.google/sre-book/postmortem-culture/>

## Local Conventions

- DevOps is an operating model, not a product selection, job title or
  mandatory separate team.
- The DevOps Engineer is an enabling role and does not inherit sole ownership
  of application behavior or every production incident.
- Continuous delivery is the general baseline for maintained deployed systems;
  continuous deployment is selected only when automated controls and service
  context justify it.
- DORA's current five-metric model is adopted as reviewed in September 2026.
  Definitions are revisited when DORA changes the model or the local delivery
  boundary changes.
- Metrics are interpreted per application or service and against its own
  context. They are not individual performance measures or cross-team league
  tables.
- Platform engineering is introduced for verified consumer needs; this
  playbook does not require an internal developer platform for small projects.
- NIST SSDF 1.1 is referenced because it is the current final SSDF publication
  at this review; draft revisions do not silently change the local baseline.
- SRE is adjacent to and compatible with DevOps; detailed controls are defined
  in [SRE Standards](../sre/README.md).

## Using References Responsibly

External guidance cannot select a local tradeoff by itself. When applying a
practice, record:

- the user, service and operating context;
- the observed constraint or risk;
- the practice being adopted and its intended effect;
- cost, authority and sustainability consequences;
- evidence and review trigger;
- any deliberate local exception.
