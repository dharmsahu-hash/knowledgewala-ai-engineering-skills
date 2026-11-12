# Test cases: api-design-integration

Manual scenarios; record results in `evals/results/`, never mark a case passed unless it was run.

| ID | Input | Expected behaviour |
|---|---|---|
| API-1 | Payment API requirements | OpenAPI with idempotency header, 201/409/422 semantics, paginated list |
| API-2 | Request to rename a response field on a live v1 | Flagged breaking; proposes additive field or v2; asks approval |
| API-3 | List endpoint without limit | Adds pagination with a maximum page size |
| API-4 | Error responses with stack traces | Replaced by stable error contract |
