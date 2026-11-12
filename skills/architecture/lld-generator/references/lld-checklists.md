# LLD checklists

## Idempotent payment table (MySQL, additive)
```sql
CREATE TABLE payment (
  id            BIGINT AUTO_INCREMENT PRIMARY KEY,
  merchant_id   BIGINT NOT NULL,
  reference     VARCHAR(64) NOT NULL,
  amount_minor  BIGINT NOT NULL CHECK (amount_minor > 0),
  currency      CHAR(3) NOT NULL,
  status        VARCHAR(16) NOT NULL,
  version       INT NOT NULL DEFAULT 0,          -- optimistic locking
  created_at    TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  UNIQUE KEY uq_payment_merchant_ref (merchant_id, reference)
);
CREATE TABLE idempotency_key (
  merchant_id  BIGINT NOT NULL,
  idem_key     VARCHAR(64) NOT NULL,
  request_hash CHAR(64) NOT NULL,                -- same key + different body => 422
  response     JSON NULL,
  created_at   TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  PRIMARY KEY (merchant_id, idem_key)
);
```
Money is stored in minor units as integers, never floating point.

## Transaction checklist
Smallest possible scope; no remote calls inside a DB transaction; state transitions validated (`PENDING -> CAPTURED|FAILED`); isolation level stated; retry only on idempotent steps.

## Concurrency checklist
Unique constraints for dedupe; optimistic locking where read-modify-write; lock ordering to avoid deadlock; visible timeouts; thread-safety of shared objects stated.

## Error contract
Stable machine code, human message, correlation id, no internal detail; 4xx for caller errors, 5xx for server errors, 409/422 for idempotency conflicts.
