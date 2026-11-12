# Requirement quality rules

A requirement is acceptable when it is: **atomic** (one thing), **testable** (a pass/fail check exists), **unambiguous**, **traceable** (source or quote), **necessary**, **feasible**.

## Acceptance criteria
- Use Given/When/Then. One behaviour per criterion.
- For every happy path add at least one negative path (invalid input, unauthorised user, dependency down).
- Include boundary values for numbers, dates and sizes.

## Non-functional requirements need numbers
| Weak | Strong |
|---|---|
| "Fast" | p95 API latency under 300 ms at 200 requests/second |
| "Secure" | All endpoints require authentication; no secrets in logs; OWASP Top 10 review passed |
| "Highly available" | 99.9% monthly availability; RPO 5 min, RTO 30 min |

If the source gives no number, write the NFR as a question, or as `[Inference]` with a proposed value awaiting approval.

## Edge-case prompts
Empty, null, huge, duplicate, concurrent, retried, out-of-order, timezone, currency, locale, partial failure, permission change mid-flow.

## Security / compliance triggers
Payments, credentials, personal or children's data, health or financial data, cross-border transfer, audit trails, data deletion rights, third-party integrations.
