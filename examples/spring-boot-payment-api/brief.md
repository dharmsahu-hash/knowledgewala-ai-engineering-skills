# Sample: Spring Boot payment API

## Business request
"Merchants need a REST API to accept card payments and refund them. It must never charge a customer twice. Use Spring Boot, MySQL and Redis. Card data must never be stored by us."

## Expected orchestrator behaviour
- Stage 1 yields FR (create payment, refund), NFR (idempotency, p95 latency target to confirm), questions on processor and PCI scope.
- Architecture: modular monolith ADR; payment adapter isolating the provider.
- LLD: payment and idempotency tables (additive), error contract, transaction boundaries with no processor call inside the DB transaction.
- Delegates to `spring-boot-engineering`, `database-engineering`, `java-engineering`, `test-engineering`, then `code-review`.
- Tests include concurrent same-key retries.

## Human gates
`requirements`, `architecture` (plus `security-sensitive` flag: payment flow), `plan`, `release`. No real processor credentials requested or stored.

## Acceptance for this sample
Idempotency proven by a test that was actually run; review finding on any remote call inside a transaction; no secrets in repo; closing report lists what was not verified. Score with `evals/rubrics/payment-api.json`.
