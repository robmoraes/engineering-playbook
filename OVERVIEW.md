# Engineering Playbook

Personal engineering standards, conventions and operational practices used across my professional projects, labs and public portfolio.

This repository consolidates the technical patterns I use for:

- Backend engineering
- Containerization
- CI/CD
- DevOps operating model
- Site Reliability Engineering
- Software testing
- Infrastructure
- Docker Swarm
- Observability
- Security
- Documentation
- Repository organization
- Deployment workflows
- Professional principles and engineering ethics

The goal is to maintain a consistent and professional engineering approach across all projects and environments.

---

# Purpose

This repository exists as:

- a personal engineering reference;
- a living technical playbook;
- a standards guide for future projects;
- a public demonstration of engineering practices and operational maturity.

Instead of treating infrastructure and delivery as isolated scripts or ad-hoc decisions, this repository documents the rationale and conventions behind the ecosystem I build and maintain.

---

# Topics Covered

The repository is intended to document standards and conventions related to:

- Repository naming
- DevOps ownership, flow, feedback and improvement
- Service-level objectives, error budgets and production readiness
- Docker image naming
- GitHub Actions
- Software testing and Test Case standards
- Secrets management
- CI/CD pipelines
- Environment variable conventions
- Docker Swarm deployments
- Reverse proxy patterns
- Observability
- Logging
- Infrastructure decisions
- Internationalization and localization standards
- Spec-driven development standards
- Production deployment practices
- Operational troubleshooting
- Architecture rationale
- Human impact and long-term stewardship of software

---

# Initial Structure

```text
engineering-playbook/
├── README.md
├── OVERVIEW.md
├── principles/
├── devops/
├── sre/
├── repositories/
├── docker/
├── github/
├── ci-cd/
├── naming/
├── observability/
├── infrastructure/
├── security/
├── testing/
├── architecture/
├── runbooks/
└── examples/
```

---

# Planned Sections

## principles/

Professional principles grounded in the human purpose and consequences of
software engineering.

Examples:

- personal mission and user-first responsibility;
- practical engineering ethics;
- craftsmanship, maintainability and documentation;
- pragmatic decision making and long-term stewardship.

---

## devops/

Shared operating standards for delivering, operating and improving software.

Examples:

- whole-lifecycle ownership and cross-functional collaboration;
- visible value streams, small batches and limited work in progress;
- continuous integration and delivery as working practices;
- delivery feedback, DORA metrics and continuous learning;
- product-oriented platforms, self-service and controlled automation;
- relationship between DevOps and SRE standards.

---

## sre/

Practical service-reliability standards for production operation and change.

Examples:

- critical user journeys, SLIs, SLOs and error-budget policy;
- service reliability records and production readiness reviews;
- actionable paging, support models, incidents and postmortems;
- operational toil, capacity, overload and graceful degradation;
- reliability testing, game days, backup restore and recovery evidence.

---

## repositories/

Repository organization standards.

Examples:

- repository naming conventions;
- mono-repo vs multi-repo decisions;
- public vs private repository criteria;
- portfolio repository organization.

---

## docker/

Containerization standards and image publishing practices.

Examples:

- multi-stage builds;
- app/web image split;
- tagging strategy;
- Docker Hub publishing;
- image security;
- healthchecks;
- non-root containers;
- volume conventions.

---

## github/

GitHub-specific conventions and repository standards.

Examples:

- repository templates;
- labels;
- branch protection;
- issue templates;
- pull request patterns;
- repository secrets naming.

---

## ci-cd/

Continuous Integration and Delivery practices.

Examples:

- GitHub Actions workflows;
- Docker image publishing;
- deployment pipelines;
- semantic versioning;
- release automation.

---

## naming/

Naming conventions used across infrastructure and software.

Examples:

- repositories;
- Docker images;
- stacks;
- services;
- networks;
- secrets;
- environment variables;
- domains;
- CI/CD pipelines.

---

## testing/

Software testing and reusable Test Case standards.

Examples:

- risk-focused Test Case design;
- behavior-oriented scenarios;
- test data and preconditions;
- requirement and risk traceability;
- execution records and evidence;
- automation and test maintenance.

---

## observability/

Operational visibility and monitoring standards.

Examples:

- structured logging;
- Loki conventions;
- Prometheus metrics;
- Grafana dashboards;
- alerting philosophy;
- correlation IDs;
- operational diagnostics.

---

## infrastructure/

Infrastructure and platform engineering decisions.

Examples:

- Docker Swarm patterns;
- reverse proxy architecture;
- high availability tradeoffs;
- internationalization and localization contracts;
- spec-driven development workflow;
- storage strategies;
- cost optimization decisions;
- infrastructure layout rationale.

---

## security/

Security-oriented operational standards.

Examples:

- secrets handling;
- token management;
- least privilege practices;
- access segmentation;
- CI/CD credential usage.

---

## architecture/

Architectural rationale and engineering philosophy.

Examples:

- why certain technologies were chosen;
- tradeoffs between simplicity and scalability;
- operational priorities;
- infrastructure evolution patterns.

---

## runbooks/

Operational procedures and troubleshooting documentation.

Examples:

- incident handling;
- deployment rollback;
- troubleshooting guides;
- recovery procedures.

---

## examples/

Reference implementations and reusable templates.

Examples:

- Dockerfiles;
- GitHub Actions workflows;
- stack files;
- compose files;
- deployment scripts.

---

# Philosophy

The focus of this repository is not theoretical perfection.

The objective is to document practical engineering decisions that prioritize:

- maintainability;
- operational clarity;
- consistency;
- shared ownership and continuous improvement;
- measurable reliability and sustainable operations;
- simplicity when possible;
- scalability when necessary;
- production-oriented thinking.

---

# Notes

This repository is continuously evolving alongside my personal studies, professional work and infrastructure experiments.

Some practices documented here may intentionally favor operational pragmatism over enterprise complexity, especially in small or personal environments.

---

# License

This repository is intended primarily as a public engineering reference and learning resource.
