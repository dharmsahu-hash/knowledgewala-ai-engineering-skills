# Database practices

## Modelling
Third normal form by default; denormalise only for a measured read need and document the write-path cost. Natural uniqueness enforced by constraints, not application code. Store time in UTC. Money as integer minor units or `DECIMAL(p,s)`.

## Indexing (MySQL/PostgreSQL)
- Composite index order: equality columns first, then range, then sort.
- A leading-column mismatch makes the index unusable for that query.
- Covering indexes avoid table lookups but cost writes and space.
- Verify with `EXPLAIN` (`EXPLAIN ANALYZE` on PostgreSQL, in a non-production environment).

Example: query `WHERE merchant_id = ? AND status = 'PENDING' ORDER BY created_at LIMIT 50`
```sql
CREATE INDEX ix_payment_merchant_status_created ON payment (merchant_id, status, created_at);
```
Expected plan change: full scan with filesort -> index range scan with no sort. Confirm with real plans before and after.

## Expand and contract migration
1. Expand: add new nullable column / table (backward compatible).
2. Deploy code writing both old and new.
3. Backfill in small batches with a throttle; verify counts.
4. Switch reads; keep writing both for one release.
5. Contract: drop the old column in a later release **(NEEDS APPROVAL; backup verified)**.
Each step lists a verification query and a rollback.

## Transactions
Short transactions; consistent lock order; retry on deadlock/serialisation failure for idempotent work; state the isolation level (MySQL InnoDB default REPEATABLE READ, PostgreSQL READ COMMITTED).

## Connection pooling
Pool size is bounded by DB max connections divided by app instances, not by thread count. Start small (for example 10 per instance) and tune with measured wait times.

## Caching (Redis)
Cache-aside by default; key includes version/tenant; TTL with jitter; protect against stampede (single-flight or lock); invalidate on write; the system must still be correct when Redis is unavailable.

## DynamoDB
Design from access patterns first; partition key for even distribution; avoid scans; GSIs per query; idempotent writes with conditional expressions.
