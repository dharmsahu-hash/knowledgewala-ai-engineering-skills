# Test strategy

## Levels
| Level | Scope | Speed | Use for |
|---|---|---|---|
| Unit | One class/function, collaborators faked | ms | Logic, boundaries, error paths |
| Integration | Component + real DB/queue | s | Mapping, queries, transactions |
| API / contract | HTTP surface against spec | s | Status codes, schemas, auth, idempotency |
| End-to-end | Full stack, few journeys | s-min | Critical user paths only |
| Performance | Workload against thresholds | min | NFR latency/throughput (approved env) |

## Case matrix per endpoint
Success; each validation rule failing; missing/invalid credentials (401); insufficient rights (403); missing resource (404); conflict/duplicate (409); idempotent retry returns the original; dependency failure; boundary values (0, 1, max, max+1).

## AC-to-test map (example)
| AC | Test |
|---|---|
| AC-1 valid payment created | `createPayment_validRequest_returns201AndPending` |
| AC-2 same key returns original | `createPayment_sameKey_returnsOriginalNoSecondCharge` |
| AC-3 amount <= 0 rejected | `createPayment_nonPositiveAmount_returns400` |

## Idempotency test outline
1. POST with key K -> 201, record body.
2. POST same body with K -> same body/status, exactly one row and one processor call.
3. POST different body with K -> 422/409.
4. Concurrent POSTs with K -> exactly one charge.

## Determinism rules
Inject clocks and random sources; wait on conditions, not time; isolate data per test; no shared mutable fixtures; clean up.

## Performance scenario format
Workload (users, rate, duration), data volume, environment, pass thresholds (for example p95 < 300 ms, error rate < 0.1%), what is measured, who approves running it.
