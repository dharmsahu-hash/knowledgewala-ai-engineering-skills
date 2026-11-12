# Sample: Angular frontend

## Business request
"A merchant dashboard in Angular showing payments with filters, a refund action, and login. It must be keyboard accessible and work on a phone."

## Expected orchestrator behaviour
- Requirements include accessibility (WCAG 2.2 AA target to confirm), responsive breakpoints and error states.
- Architecture notes state management choice with alternatives; auth token handling decision recorded.
- No specialist Angular skill is shipped yet: the orchestrator says so and applies generic guidance.
- Tests: component tests, an auth-guard test, an accessibility check scenario.

## Human gates
`requirements`, `architecture` (token storage is `security-sensitive`), `plan`, `release`.

## Acceptance for this sample
Token storage decision documented with risk; keyboard and screen-reader acceptance criteria exist and are mapped to tests; build and tests actually run or marked not run.
