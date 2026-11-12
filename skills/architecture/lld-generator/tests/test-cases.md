# Test cases: lld-generator

| ID | Input | Expected behaviour |
|---|---|---|
| LLD-1 | Approved payment HLD | Schema with unique constraint on (merchant, reference), idempotency table, error table |
| LLD-2 | Change that renames a column | Flagged `NEEDS APPROVAL` as destructive; additive alternative offered |
| LLD-3 | HLD without DB engine | Asks which engine before emitting engine-specific DDL |
| LLD-4 | Transaction involving a remote call | Remote call moved outside the DB transaction, failure path described |
| LLD-5 | Any output | Names consistent across diagrams and API spec |
