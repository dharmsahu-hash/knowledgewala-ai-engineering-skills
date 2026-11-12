# Performance playbook

## Experiment log
| # | Hypothesis | Change | Metric before | Metric after | Noise | Keep? |
|---|---|---|---|---|---|---|

## Where time goes
| Symptom | Look at | Typical causes |
|---|---|---|
| High p95, low CPU | traces, waits | blocking I/O, slow queries, lock contention, pool exhaustion |
| High CPU | CPU profile | hot loops, serialisation, regex, excess logging |
| Growing memory | heap dump, GC logs | leaks, unbounded caches, large result sets |
| Throughput plateau | thread/connection metrics | small pools, synchronised sections, downstream limits |
| Fast median, bad tail | latency histogram | GC pauses, retries, cold caches, queueing |

## Database
Check query count per request (N+1), plans for the slowest queries, missing or unused indexes, connection pool wait time, transaction length. Hand deep SQL tuning to `database-engineering`.

## Caching
Cache the expensive and repeatable; define key, TTL, invalidation and stampede protection; measure hit ratio; the system must stay correct when the cache is cold or down.

## Concurrency
Bound pools and queues, avoid blocking calls on event-loop threads, reduce lock scope, apply backpressure, test under realistic concurrency.

## Load test scenario format
Workload model (users, arrival rate, think time), data volume, environment, duration and ramp, pass thresholds (for example p95 and error rate), and who approved running it.

## Reporting
Percentiles (p50/p95/p99), throughput, error rate, saturation of CPU/memory/connections; compare against the requirement, not against the previous state alone.
