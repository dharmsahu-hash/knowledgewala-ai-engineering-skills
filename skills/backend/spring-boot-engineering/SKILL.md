---
name: spring-boot-engineering
description: Builds and reviews Spring Boot 3.x services - REST controllers, validation, global exception handling, Spring Security, Spring Data JPA and Hibernate, transaction management, configuration, observability with Actuator and Micrometer, and resilient service integration. Use when implementing or changing a Spring Boot application, securing endpoints, or fixing JPA, transaction or configuration problems.
license: MIT
compatibility: Spring Boot 3.x on Java 17+. Verify the project's actual Spring Boot version in its build file before applying advice.
metadata:
  title: Spring Boot Engineering Specialist
  version: "1.0.0-rc.1"
  author: KnowledgeWala
  category: backend
  tags: "spring-boot, rest, jpa, hibernate, spring-security, observability"
  tier: paid
---

# Spring Boot Engineering Specialist

## Purpose
Deliver secure, observable, testable Spring Boot code that follows the approved LLD and the project's existing conventions.

## When to use
- Adding or changing REST endpoints, services, repositories, security or configuration in a Spring Boot app.
- Diagnosing N+1 queries, transaction, lazy-loading, or bean-wiring problems.

## When not to use
- Pure Java language questions: `java-engineering`.
- Schema, index and query design: `database-engineering`.
- Contract-first API design across services: design first with `lld-generator`.

## Required inputs
- Spring Boot and Java versions, build tool, existing package layout (inspect).
- Approved LLD section: endpoints, DTOs, schema, error contract.
- Security requirements: who may call what.

## Instructions
1. Inspect `pom.xml`/`build.gradle`, `application*.yml`, and an existing controller/service/test to match style.
2. Follow [references/spring-boot-practices.md](references/spring-boot-practices.md).
3. Layering: controller (HTTP and validation only), service (business rules, transactions), repository (persistence). Entities are never returned from controllers; use DTOs.
4. Security-sensitive changes (auth rules, CORS, CSRF, crypto, secrets) require human approval before being applied.
5. Never put secrets in code or committed config; use environment or a secret store, with placeholders in examples.

## Workflow
1. Confirm versions and the LLD slice.
2. Write failing tests first for the behaviour (slice tests where possible).
3. Implement DTOs with Bean Validation, controller, service with `@Transactional` boundaries, repository.
4. Add error handling via `@RestControllerAdvice` mapping to the agreed error contract.
5. Secure endpoints; default deny; test unauthorised and forbidden cases.
6. Add metrics, health and structured logging with correlation id.
7. Run the full build and tests; report real output.

## Quality gates
- All endpoints validate input; invalid requests return the agreed 4xx contract.
- No entity leaks through the API; no N+1 on the main read paths (verified by a test or SQL log).
- Transactions: scope minimal, no remote calls inside, rollback rules explicit.
- Security tests cover 401 and 403 for each protected endpoint.
- No secrets in repo; configuration externalised per environment.

## Expected output
Source and test changes, migration scripts if the schema changes (Flyway/Liquibase as used), configuration notes, and the real build/test output.

## Validation rules
- `mvn -q test` or `./gradlew test` exits 0 (command and result reported).
- Actuator exposure is limited to what the design lists.
- Migrations are additive unless a destructive change was approved.

## Error handling
- Context fails to start: read the root cause of the stack trace; fix wiring, not by adding `@Lazy` or disabling checks.
- Test needs infrastructure unavailable locally: use Testcontainers if the project does, otherwise report the gap.
- Version-specific API unclear: check the project's resolved dependency version, not memory.

## Examples
See [references/spring-boot-practices.md](references/spring-boot-practices.md) for controller, advice and transaction examples.

## Limitations
- Cannot verify runtime behaviour it cannot execute; says so when tests were not run.
- Spring Boot 2.x (javax namespace) is out of scope.
- Reactive (WebFlux) projects need different patterns not covered here.
