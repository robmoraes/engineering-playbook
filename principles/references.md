# References and Adoption Notes

This section begins with a personal mission: build software that creates a
useful bridge between people and their everyday goals. The positions in these
documents are this playbook's own. The external sources below provide
professional and operational guidance that strengthens particular duties and
practices; they are not presented as authors of the personal mission.

## External Guidance And Adoption

| Source | Relevant external guidance | Adoption in this section |
| --- | --- | --- |
| ACM, *Code of Ethics and Professional Conduct* (2018) | Computing work should contribute to human well-being, avoid harm, respect privacy and pursue high quality and careful evaluation of impact. | User impact, honest risk discussion, privacy and quality are treated as engineering responsibilities rather than optional refinements. |
| IEEE-CS/ACM Joint Task Force, *Software Engineering Code of Ethics and Professional Practice* | Software engineers have obligations to the public, clients and employers, product quality, independent judgment, colleagues and lifelong professional competence. | Serving users is held alongside honest responsibility toward employers, clients, colleagues and professional judgment. |
| Google, *Site Reliability Engineering* | Service level indicators and monitoring should connect operational decisions to meaningful service behavior and response. | Reliability and observability are framed as accountability for user-visible outcomes and recovery, with investment proportionate to consequence. |
| Adam Wiggins, *The Twelve-Factor App* | Explicit dependencies and configuration, separated build/release/run stages, disposability, parity and logs support manageable deployed applications. | Operational clarity, automation and replaceable runtime practices are valued because maintainers must safely change and diagnose systems. |

## Source Links

- Association for Computing Machinery, *ACM Code of Ethics and Professional
  Conduct* (adopted June 22, 2018):
  <https://www.acm.org/code-of-ethics>
- IEEE Computer Society and ACM, *Software Engineering Code of Ethics and
  Professional Practice*:
  <https://www.computer.org/education/code-of-ethics>
- Google, *Site Reliability Engineering - Service Level Objectives*:
  <https://sre.google/sre-book/service-level-objectives/>
- Google, *Site Reliability Engineering - Monitoring Distributed Systems*:
  <https://sre.google/sre-book/monitoring-distributed-systems/>
- Adam Wiggins, *The Twelve-Factor App*:
  <https://12factor.net/>

## Relationship To Other Works

Some established books discuss adjacent subjects, including software
craftsmanship, delivery performance and organizational boundaries. They are
useful reading, but this section does not attribute its principles to works it
does not directly rely upon. When a future revision adopts specific guidance
from another work, that guidance and the local adaptation should be recorded
here explicitly.

## Using References Responsibly

A code of ethics or industry book cannot decide a local tradeoff by itself.
When invoking external guidance, record:

- the affected people or workflow;
- the actual technical and organizational constraint;
- the risk, benefit or evidence relevant to the decision;
- the local practice adopted and any intentional limit or exception.
