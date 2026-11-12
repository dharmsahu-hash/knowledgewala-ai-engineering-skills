---
name: test-engineering
description: Designs and writes automated tests - unit, integration, API, contract, end-to-end, boundary, negative and performance-scenario tests - mapped to acceptance criteria, runs them, and reports real results and coverage gaps. Use when code needs tests, when acceptance criteria must be turned into executable checks, or when test quality and coverage must be assessed.
license: MIT
compatibility: Framework-neutral. Uses the project's existing test framework (for example JUnit 5, pytest, Jest, Playwright); inspect before choosing.
metadata:
  title: Test Engineering Specialist
  version: "1.0.0-rc.2"
  author: KnowledgeWala
  category: quality
  tags: "testing, unit-tests, integration-tests, contract-tests, e2e, coverage"
  tier: free
---

# Test Engineering Specialist

## Purpose
Prove behaviour against requirements with executable tests, and report honestly what is and is not covered.

## When to use
- Implementation is done or in progress and needs tests.
- Acceptance criteria need to become automated checks.
- Coverage or test quality is in question.

## When not to use
- Judging code quality overall: `code-review`.
- Load testing at scale: this skill defines scenarios; running them needs dedicated tooling and an approved environment.

## Required inputs
- Requirements/acceptance criteria and the code under test.
- The project's test framework, conventions and how to run tests (inspect repo and docs).

## Instructions
1. Derive tests from acceptance criteria first, then from code paths; keep a map AC -> test.
2. Use the existing framework and style. Add a dependency only with approval.
3. Follow [references/test-strategy.md](references/test-strategy.md) for levels, naming and what each test type must cover.
4. Tests must be deterministic: no sleeps for sync, no reliance on order, clock/randomness injected.
5. Run the tests. Report the exact command and the real outcome. Never write "tests pass" without running them.
6. Never weaken or delete a failing test to make a run green; fix the cause or report it.

## Workflow
1. Build the AC-to-test map and identify gaps.
2. Unit tests for logic including boundaries and negatives.
3. Integration tests for persistence and wiring (real engine where practical).
4. API/contract tests for each endpoint: success, validation failure, unauthorised, forbidden, not found, conflict, idempotent retry.
5. End-to-end tests for critical journeys only.
6. Performance scenarios: workload, data size, success thresholds (defined, not run unless approved).
7. Run, record results, list uncovered criteria and flaky risks.

## Quality gates
- Every acceptance criterion maps to at least one test or is listed as uncovered.
- Each feature has negative and boundary tests, not only happy paths.
- Tests run green locally with the shown command, or failures are reported verbatim.
- No test depends on real external services, secrets or production data.
- Test names state the behaviour.

## Expected output
Test files, the AC-to-test traceability table, the run command and real results, coverage gaps, and performance test scenarios.

## Validation rules
- Test run exit code and summary are quoted from the actual run.
- Coverage numbers, if given, come from a coverage tool run, with the tool named.
- Mutation of a test to pass is prohibited.

## Error handling
- Cannot run tests (missing runtime or services): state it; deliver tests marked "not executed".
- Flaky test: isolate the cause (time, order, shared state); do not add retries as a first fix.
- Code is untestable: report the design obstacle and propose the smallest refactor, ask before applying.

## Examples
See [references/test-strategy.md](references/test-strategy.md) for an AC-to-test mapping and an idempotency test outline.

## Limitations
- Passing tests show absence of the tested failures only.
- Generated test data is synthetic; it cannot reveal production data quirks.
- Does not execute load or security tests without explicit approval and an approved environment.
