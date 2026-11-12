---
name: lld-generator
description: Produces a Low-Level Design from an approved HLD - class and sequence diagrams, database schema, API specifications, interface definitions, design patterns, error-handling strategy, transaction boundaries and concurrency considerations. Use when an HLD is approved and engineers need implementable detail before coding starts.
license: MIT
compatibility: Works in any Agent Skills capable assistant. Diagrams use Mermaid; API specs use OpenAPI 3.x snippets.
metadata:
  title: Low-Level Design Generator
  version: "1.0.0-rc.2"
  author: KnowledgeWala
  category: architecture
  tags: "lld, low-level-design, uml, sequence-diagram, schema, openapi"
  tier: paid
---

# Low-Level Design Generator

## Purpose
Turn an approved HLD into component-level detail precise enough to implement and test without further design decisions.

## When to use
- An HLD is approved and implementation is next.
- A module needs documented contracts, schema or concurrency rules before coding.

## When not to use
- HLD is missing or unapproved: use `hld-generator`.
- The work is a trivial change inside existing, understood code.

## Required inputs
- Approved HLD and its requirement ids.
- Language/framework and conventions in use (inspect the repo; do not assume).
- Existing schema or API definitions if this is a change.

## Instructions
1. Design only what the HLD scopes. New cross-cutting decisions go back to `solution-architecture` as ADRs.
2. Follow [templates/lld.md](templates/lld.md) and consult [references/lld-checklists.md](references/lld-checklists.md).
3. Schema changes must be expressed as additive migrations. Any destructive change (drop, rename, type narrowing, data rewrite) is flagged for human approval.
4. Name the test approach for each component so `test-engineering` can proceed.

## Workflow
1. Module and package structure.
2. Class/interface design with responsibilities (Mermaid class diagram).
3. Sequence diagrams for each primary flow plus one failure flow.
4. Database schema: tables, keys, constraints, indexes with the query each index serves.
5. API specification: paths, methods, request/response schemas, error contract, auth, idempotency.
6. Error-handling strategy: exception taxonomy, mapping to error codes, retries.
7. Transaction boundaries and isolation; concurrency and locking rules.
8. Patterns used and why; traceability to FR/NFR; test approach.

## Quality gates
- Each public method or endpoint has inputs, outputs, errors and preconditions.
- Every index justifies itself by a named query; every FK has a deletion rule.
- Each transaction lists what is inside it and what happens on failure.
- Concurrent access to shared state has an explicit rule (optimistic lock, unique constraint, etc.).
- Destructive schema changes are flagged `NEEDS APPROVAL`.

## Expected output
LLD document: Module Structure, Class Diagram, Sequence Diagrams, Database Schema (DDL), API Specification, Error Handling, Transactions and Concurrency, Patterns, Test Approach, Traceability.

## Validation rules
- DDL is syntactically valid for the stated database; OpenAPI snippets are valid YAML.
- Names are consistent across class diagram, sequence diagrams and API spec.
- No credentials or real data in examples.

## Error handling
- HLD ambiguity: record an assumption and ask; do not guess silently.
- Conflict between HLD and existing code: report with file references; do not change either unasked.
- Unknown database engine: ask; avoid engine-specific DDL until known.

## Examples
See [references/lld-checklists.md](references/lld-checklists.md) for the idempotent-payment schema and checklist.

## Limitations
- DDL is not executed against a real database by this skill.
- Performance of indexes is reasoned, not measured.
