# Databases for Applications

Use this book when application behavior depends on a database guarantee.
Start by stating what must remain true after commit. Identify the key,
constraint or transaction that enforces it across independent writers, then
check the result from another connection.

| When you need to… | Read |
| --- | --- |
| Model a bookable slot and decide which reservation can commit | [A reservation schema under contention](./reservation-schema.md) |
| Decide whether a customer lookup earns the cost of an index | [Evaluating a reservation index](./reservation-index.md) |
| Decide where the API and worker interpret the result | [Business rule placement](../software-design/business-rule-placement.md) |
| Check how PostgreSQL implements the guarantee | [References and adoption notes](./references.md) |
