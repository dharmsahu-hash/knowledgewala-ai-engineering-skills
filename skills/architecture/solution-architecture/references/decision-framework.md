# Decision framework

## Scoring
Score each option 1-5 against weighted drivers (weights sum to 100). Record the table and the reasoning, not only the totals.

| Driver | Weight | Modular monolith | Microservices |
|---|---|---|---|
| Time to first release (team of 4) | 25 | 5 | 2 |
| Independent scaling of one hot component | 15 | 2 | 5 |
| Operational simplicity | 25 | 5 | 2 |
| Fault isolation | 15 | 2 | 4 |
| Team autonomy | 10 | 3 | 5 |
| Data consistency simplicity | 10 | 5 | 2 |
| **Weighted total** | | **4.05** | **2.95** |

Outcome: modular monolith with enforced module boundaries; extract a service only when a driver (for example separate scaling of the payments module) demonstrably needs it. Record this as an ADR with a review trigger.

## Distribution is justified only by
Independent scaling, independent deployment cadence across teams, fault isolation of a critical path, different technology needs, or regulatory isolation.

## Resilience checklist
Timeouts on every remote call, bounded retries with jitter, idempotency for retried writes, circuit breakers, bulkheads, graceful degradation, backpressure on queues, dead-letter handling, health checks, tested restore.

## Event-driven checklist
Ordering needs, at-least-once delivery (consumers idempotent), schema versioning, outbox pattern for DB+event atomicity, replay, observability of lag.
