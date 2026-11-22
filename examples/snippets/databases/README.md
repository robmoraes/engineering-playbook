# Database Snippets

The [reservation index experiment](./reservation-index.sql) is an illustrative
`psql` script for a disposable PostgreSQL database. Each invocation creates
one schema, seeds synthetic slots and claims, prints the customer lookup and
its plan, then times a batch of 10,000 inserts.

Use a role that can create schemas in the lab database. Set `lab_schema` to
a fresh schema name and `with_index` to `on` or `off`. Reusing a schema
name stops the script at creation. Both arms retain the slot key and foreign
key. The output includes the ordered ten-row result, the insert time, the
final claim count and the candidate index size in bytes.

See [Evaluating a reservation index](../../../databases/reservation-index.md)
for the commands, measured results, assumptions and PostgreSQL references.
The script leaves the synthetic data available for inspection. Discard the
lab database after completing the comparison.
