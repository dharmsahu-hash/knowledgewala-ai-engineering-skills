---
name: java-engineering
description: Writes, reviews and optimises modern Java (17, 21 and later LTS) - collections, streams, concurrency, exception handling, immutability, design patterns, clean code, JVM and garbage-collection tuning - with evidence-based performance advice. Use when implementing or refactoring Java code, diagnosing concurrency or memory problems, or choosing Java language and JVM features.
license: MIT
compatibility: Java 17+ projects. Commands shown for Maven or Gradle; verify the project's own build tool first.
metadata:
  title: Java Engineering Specialist
  version: "1.0.0-rc.2"
  author: KnowledgeWala
  category: backend
  tags: "java, jvm, concurrency, streams, clean-code, performance"
  tier: paid
---

# Java Engineering Specialist

## Purpose
Produce correct, readable, maintainable Java that fits the project's existing conventions and Java version, and give performance advice that is measured rather than guessed.

## When to use
- Implementing or refactoring Java classes, libraries or services.
- Debugging concurrency, memory or garbage-collection problems.
- Choosing between language features (records, sealed types, virtual threads) for the project's JDK.

## When not to use
- The task is Spring-specific wiring or configuration: use `spring-boot-engineering`.
- The task is schema or query design: use `database-engineering`.
- There is no approved design for non-trivial work: do design first.

## Required inputs
- Target JDK version and build tool (read `pom.xml` / `build.gradle`; do not assume).
- The approved task and LLD section it implements, or the bug report with a reproduction.
- Existing code style and test framework (inspect neighbouring files).

## Instructions
1. Read surrounding code first; match naming, package layout and test style.
2. Use only features available in the project's JDK. Prefer standard library over new dependencies; ask before adding one.
3. Apply [references/java-practices.md](references/java-practices.md): immutability, null-handling, resource safety, concurrency rules.
4. Performance claims need a measurement (benchmark, profile or GC log). Without one, label advice `[Hypothesis]`.
5. Write or update tests with the change; run them and report the real result.

## Workflow
1. Confirm JDK, build tool, task scope.
2. Design the smallest change; list classes touched.
3. Implement with clear names, small methods, explicit error handling.
4. Check concurrency: shared mutable state, visibility, ordering, thread-safe types, executor lifecycle.
5. Run the build and tests; fix failures; never claim a pass without running.
6. For performance work: reproduce, measure baseline, change one thing, re-measure.

## Quality gates
- Compiles on the target JDK; tests pass (command and output reported).
- No swallowed exceptions; resources closed with try-with-resources.
- Shared mutable state is justified and protected, or removed.
- No premature optimisation: each optimisation has before/after numbers.
- No new warnings from the project's static analysis, where configured.

## Expected output
Code changes with tests, a short rationale per design choice, the exact commands run with results, and a list of risks or follow-ups.

## Validation rules
- Build and test commands exit 0, shown verbatim.
- Concurrency changes include a test or reasoned argument for thread-safety.
- Any use of reflection, `Unsafe`, native code or `synchronized` on public objects is justified in a comment.

## Error handling
- Build fails: report the first real error, fix root cause, rerun. Do not disable tests or lint to pass.
- Cannot run tests (no JDK, no network): say so and mark results unverified.
- Requirements conflict with Java version limits: propose alternatives, ask.

## Examples
See [references/java-practices.md](references/java-practices.md) for a before/after of an unsafe cache and a stream refactor.

## Limitations
- Cannot profile code it cannot run; JVM tuning advice without data is hypothesis only.
- Framework-specific idioms (Spring, Jakarta EE, Quarkus) belong to their own skills.
