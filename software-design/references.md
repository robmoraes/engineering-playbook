# References and Adoption Notes

## Business rule placement

- Alistair Cockburn describes adapters that let different clients drive the
  same application behavior. Here the HTTP handler and queue worker each
  translate a request and call the booking operation.
  [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture)
- Martin Fowler describes organizing a business transaction as a procedure.
  This playbook starts a small use case with a named function. More elaborate
  domain objects become useful when several operations share behavior.
  [Transaction Script](https://martinfowler.com/eaaCatalog/transactionScript.html)
- PostgreSQL documents how a primary key enforces uniqueness, how an insert
  handles a conflict on a chosen key, and how Read Committed gives each
  statement its own snapshot. The example adopts those database semantics.
  The lifetime of a claim, the replay identity and the caller responses are
  decisions specific to the example.
  [Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html),
  [INSERT](https://www.postgresql.org/docs/current/sql-insert.html) and
  [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html).
- PostgreSQL's `pg_blocking_pids` identifies sessions blocking another
  session. The two-session exercise uses it to observe actual contention
  before allowing the first reservation to commit.
  [Session Information Functions](https://www.postgresql.org/docs/current/functions-info.html#FUNCTIONS-INFO-SESSION).

## Module boundaries and failures

- Cockburn describes application ports and technology-specific adapters.
  Here booking owns the operations used by its callers and storage adapter.
  The application wires a function or interface to a concrete implementation.
  [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture)
- AWS describes caller-provided request identifiers for recognizing a retry
  after a lost response. Here retries carry the original actor, slot and
  claim ID so the service can recover the stored confirmation.
  [Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)
- RFC 9110 defines HTTP status semantics. The booking example chooses
  `409` for a competing claim and `503` for a temporary inability to
  confirm a result. The claim ID and retry policy belong to the application.
  [HTTP Semantics, status codes](https://www.rfc-editor.org/rfc/rfc9110.html#section-15)
- RabbitMQ describes consumer acknowledgements, redelivery and the cost of
  immediate requeue loops. Here the worker acknowledges terminal outcomes
  after recording them and uses bounded retries for transient failures.
  [Consumer Acknowledgements and Publisher Confirms](https://www.rabbitmq.com/docs/confirms)

## Safe refactoring

- Michael Feathers describes characterization tests as a way to discover
  and record existing behavior. Here the tests observe the HTTP response,
  worker acknowledgement and stored reservation before the first edit.
  [Characterization Testing](https://michaelfeathers.silvrback.com/characterization-testing)
- Martin Fowler describes refactoring in small steps that preserve observable
  behavior. His Extract Function example names a piece of existing logic
  and replaces it with a call. Here we use that move to share the booking
  decision and verify each caller as it switches over.
  [Refactoring](https://refactoring.com/) and
  [Extract Function](https://refactoring.com/catalog/extractFunction.html).
