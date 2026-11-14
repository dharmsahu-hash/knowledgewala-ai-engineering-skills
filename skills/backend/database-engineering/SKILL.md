---
name: database-engineering
description: Designs and optimises databases - relational modelling for MySQL, PostgreSQL and Aurora, indexing, query analysis with EXPLAIN, transactions and isolation, connection pooling, caching with Redis, DynamoDB access patterns, and safe, reversible migrations. Use when designing a schema, tuning slow queries, planning a data migration, or choosing a caching or datastore strategy.
license: MIT
compatibility: Engine-specific advice requires the engine and version to be stated. Scripts and SQL are produced for review; this skill never runs them against a database.
metadata:
  title: Database Architecture and Optimization
  version: "1.0.0-rc.3"
  author: KnowledgeWala
  category: backend
  tags: "mysql, postgresql, aurora, redis, dynamodb, indexing, migrations"
  tier: paid
---

# Database Architecture and Optimization

## Purpose
Produce correct schemas, justified indexes and safe migrations, and tune performance from evidence (query plans and measurements).

## When to use
- Designing or reviewing a schema, ER model or data-access pattern.
- A query or endpoint is slow and needs analysis.
- Planning a migration, backfill or cache layer.

## When not to use
- Application code issues unrelated to data access: `java-engineering` or `spring-boot-engineering`.
- Whole-system storage choices still open: start with `solution-architecture`.

## Required inputs
- Database engine and version; workload shape (read/write ratio, volumes, latency goals).
- Current schema/DDL and, for tuning, the slow query plus `EXPLAIN` output and row counts.
- For migrations: table sizes, downtime tolerance, rollback expectation.

## Instructions
1. Never run SQL against a real database unless the human explicitly approves the exact statement and environment. Produce scripts for review.
2. Destructive changes (drop, truncate, rename, narrowing a type, data rewrite, mass update/delete) are flagged `NEEDS APPROVAL` and need a rollback plan.
3. Every index states the query it serves and its write cost. Prove tuning with plans, not intuition; follow [references/db-practices.md](references/db-practices.md).
4. Use expand-and-contract migrations so old and new application versions both work.

## Workflow
1. Clarify engine, version, workload, constraints.
2. Model entities, keys, constraints, normalisation level and deliberate denormalisation (with reason).
3. Derive indexes from the real query list; check column order and selectivity.
4. For slow queries: read the plan, find scans/sorts/temp tables, propose the change, predict the new plan, and ask for measured before/after.
5. Define transaction boundaries, isolation, locking and deadlock handling.
6. Size the connection pool from DB limits and app concurrency.
7. Choose cache strategy: what, key design, TTL, invalidation, stampede protection.
8. Write the migration plan: steps, order, verification query per step, rollback.

## Quality gates
- Every table has a primary key and explicit constraints; money uses exact types.
- Every FK has a documented delete rule; every index is justified by a query.
- Migrations are additive or approved; each has a rollback or a stated reason it cannot.
- Cache design names its invalidation and failure behaviour (cache down must not mean data loss).
- Performance claims cite a plan or measurement; otherwise `[Hypothesis]`.

## Expected output
ER diagram (Mermaid), DDL, index recommendations with rationale, query optimisation report (before plan, change, expected after), migration plan with rollback, caching design, performance considerations.

## Validation rules
- SQL is syntactically valid for the stated engine and version.
- Migration steps are ordered and each has a verification statement.
- No credentials or real personal data appear in examples.

## Error handling
- Engine unknown: ask; do not emit engine-specific features.
- No plan or volumes provided: give a checklist of what to collect; no invented numbers.
- Request to run a destructive statement: stop and request explicit approval naming environment and statement.

## Examples
See [references/db-practices.md](references/db-practices.md) for an index-tuning and expand-contract example.

## Limitations
- Cannot see production data distribution; index advice is validated only by the user's measurements.
- Engine behaviour differs between versions; verify against the version's documentation.
- Redis and DynamoDB guidance is design-level; capacity and cost need provider tooling.
