# HLD example (excerpt): payment API

**Components:** API service (validates, enforces idempotency, orchestrates), Payment processor adapter (isolates the external provider), MySQL (payments, refunds, idempotency keys; owned by API service), Redis (short-lived idempotency lock, rate limiting).

**Flow 1: create payment**
1. Client sends `POST /payments` with `Idempotency-Key`.
2. API checks Redis lock, then the idempotency table. If found, returns the stored response (NFR-1).
3. API writes `PENDING` payment in one transaction, calls the processor adapter with a timeout.
4. On success updates to `CAPTURED` and stores the response against the key.
5. **Failure path:** processor timeout leaves `PENDING`; a reconciliation job queries the processor by reference before any retry, so a customer is never charged twice.

**Security:** TLS everywhere; API keys hashed at rest; card data never stored (tokenised by the processor); trust boundary at the API gateway; audit log for every state change. Payment flow = approval gate for the security design.

**Traceability:** FR-1 -> API service, FR-2 -> refund endpoint, NFR-1 -> idempotency table and Redis lock.
