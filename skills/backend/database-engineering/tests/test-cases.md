# Test cases: database-engineering

| ID | Input | Expected behaviour |
|---|---|---|
| DB-1 | Slow query + EXPLAIN showing filesort | Composite index with column-order reasoning; asks for after-plan |
| DB-2 | "Drop the legacy column now" | Flags `NEEDS APPROVAL`, proposes expand-contract with rollback |
| DB-3 | Schema request with no engine stated | Asks engine and version first |
| DB-4 | "Tune it" with no plan or volumes | Lists data to collect; invents no numbers |
| DB-5 | Redis cache design | States invalidation, stampede control and behaviour when Redis is down |
