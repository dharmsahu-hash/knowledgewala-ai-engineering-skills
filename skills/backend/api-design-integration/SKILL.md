---
name: api-design-integration
description: Designs and reviews REST APIs and integrations - resource modelling, OpenAPI specifications, versioning, authentication and authorisation, rate limiting, idempotency, pagination, error contracts and backward compatibility. Use when defining a new API, changing a published one, or reviewing an API contract for consistency, safety and performance.
license: MIT
compatibility: Works in any Agent Skills capable assistant. OpenAPI 3.x snippets in YAML.
metadata:
  title: API Design and Integration
  version: "1.0.0-rc.3"
  author: KnowledgeWala
  category: backend
  tags: "api, rest, openapi, versioning, idempotency, pagination"
  tier: paid
---

# API Design and Integration

## Purpose
Produce API contracts that are consistent, safe to evolve and easy to consume, before any implementation starts.

## When to use
- A new API or integration contract must be defined.
- A published API changes and compatibility must be assessed.
- An OpenAPI document needs review.

## When not to use
- Internal implementation details of a controller: use `spring-boot-engineering`.
- Message-broker or event schema design beyond HTTP: use `solution-architecture` first.

## Required inputs
- Approved requirements and consumer list (who calls this and how).
- Existing API specs or clients if this is a change.
- Auth model and data sensitivity.

## Instructions
1. Design contract-first: write the OpenAPI before code.
2. Apply the rules in the reference for resources, status codes, pagination, idempotency and errors.
3. Classify every change to a published API as compatible or breaking; breaking changes need a new version and human approval.
4. Never put secrets or real data in examples.
Detailed checklists and examples: [references/api-design-rules.md](references/api-design-rules.md).

## Workflow
1. List consumers and use cases.
2. Model resources and relationships; name by noun.
3. Define operations, schemas, status codes and the error contract.
4. Add auth scopes, rate limits, idempotency and pagination rules.
5. Write the OpenAPI document and examples.
6. Run the compatibility checklist against the previous version.
7. Record versioning and deprecation policy.

## Quality gates
- Every operation lists success and error responses.
- Writes that can be retried specify idempotency behaviour.
- Every list endpoint is paginated with a stated maximum page size.
- Breaking changes are flagged and approved.
- Auth requirement is explicit per operation.

## Expected output
OpenAPI 3.x document, error-contract definition, versioning and deprecation notes, compatibility assessment, and list of open questions.

## Validation rules
- OpenAPI snippets are valid YAML and internally consistent ($ref targets exist).
- Status codes match semantics (201 on create, 409/422 on idempotency conflict).
- Examples contain no real credentials or personal data.

## Error handling
- Consumers unknown: ask; do not assume a single client.
- Ambiguous compatibility: treat as breaking until shown otherwise.
- Requirement conflicts with REST conventions: explain the trade-off and ask.

## Examples
See the error contract, pagination and idempotency examples in the reference.

## Limitations
- Does not run contract tests or load tests.
- GraphQL and gRPC are out of scope.
- Rate-limit values are proposals until measured.
