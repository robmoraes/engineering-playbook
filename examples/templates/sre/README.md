# SRE Operational Record Templates

## Purpose

Copyable Markdown records for applying the SRE standards while preparing or
reviewing a maintained service.

## Status

Template.

## Operating Context

Maintained, production and critical services. Learning environments may use a
reduced record when they explicitly state that no production reliability or
support commitment exists.

## Standards Demonstrated

- [SRE Standards](../../../sre/README.md)
- [Service Reliability Record](../../../sre/service-reliability-record.md)
- [Production Readiness and Change](../../../sre/production-readiness-and-change.md)

## Configuration Inputs

Replace all uppercase placeholder values with service-specific evidence. Do
not invent owners, targets, recovery claims or support commitments. Link to
the authoritative dashboard, runbook, workflow or catalog record instead of
copying details that would drift.

## Secret And Data Handling

Do not include credentials, live secret values, private keys, customer data or
unsafe production commands. Use approved secret-object names and controlled
internal links when operational material cannot be public.

## Validation

- confirm every referenced local or external artifact exists;
- search for unresolved uppercase placeholders and `TBD` values;
- have the accountable service owner review reliability and risk decisions;
- verify technical claims through the implementation path described by the
  record;
- apply the [SRE Checklist](../../../sre/sre-checklist.md).

## Operational Limitations

Completing a template is not production evidence. A reliability claim is valid
only when its implementation, observed behavior and responsible owner support
it. Adapt depth to consequence without omitting an applicable stop condition.

## Files

| File | Use |
| --- | --- |
| [Service Reliability Record](./service-reliability-record.md) | Canonical service context, objectives, ownership, operation and recovery record |
| [Production Readiness Review](./production-readiness-review.md) | Evidence-based launch or material-transition decision |

## References

See [SRE References And Adoption Notes](../../../sre/references.md).
