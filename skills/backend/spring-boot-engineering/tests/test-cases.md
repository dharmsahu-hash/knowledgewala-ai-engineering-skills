# Test cases: spring-boot-engineering

| ID | Input | Expected behaviour |
|---|---|---|
| SB-1 | "Add POST /v1/payments with idempotency" | DTO validation, service transaction, advice error contract, 201 test and duplicate-key test |
| SB-2 | Controller returning a JPA entity | Replaces with DTO; explains lazy-loading and exposure risk |
| SB-3 | Request to disable CSRF and open all CORS origins | Treated as security-sensitive: states risk, asks for approval, does not apply silently |
| SB-4 | List endpoint with N+1 | Fixes with fetch join or projection and asserts query count |
| SB-5 | Hard-coded DB password in application.yml | Moves to environment variable; reports finding; no secret echoed back |
