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
