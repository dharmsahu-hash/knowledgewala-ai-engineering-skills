# Worked example: payment processing API

**Input (business request):** "Merchants need an API to accept card payments and refund them. It must never charge a customer twice."

## Extract (abridged)
- **FR-1** The API accepts a payment request with amount, currency and merchant reference. (source: "accept card payments")
- **FR-2** A payment can be fully or partially refunded. (source: "refund them")
- **NFR-1** Idempotency: repeating a request with the same idempotency key returns the original result and creates no second charge. (source: "never charge a customer twice")
- **NFR-2** [Inference] p95 latency under 500 ms excluding the card network. Awaiting approval.

## Stories
- **US-1** As a merchant, I want to submit a payment, so that the customer is charged once.
  - **AC-1** Given a valid request, when submitted, then a payment is created with status `PENDING` or `CAPTURED`.
  - **AC-2** Given the same idempotency key, when resubmitted, then the original response is returned and no new charge exists.
  - **AC-3** (negative) Given amount <= 0, when submitted, then 400 with a machine-readable error.

## Clarification questions
- **Q-1** Which payment processor and card-data scope (PCI DSS SAQ level)? Blocks FR-1.
- **Q-2** Are partial refunds cumulative up to the original amount? Blocks FR-2.

## Flags
Payment flow: requires human approval of the security design (orchestrator gate).
