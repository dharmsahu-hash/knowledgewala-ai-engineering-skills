# Sample: multi-agent application

## Business request
"An internal assistant where a planner agent delegates to a research agent and a code agent, with a human approving anything that writes to a repository."

## Expected orchestrator behaviour
- Requirements define agent roles, tool permissions, memory scope and failure behaviour.
- Delegates to `agentic-ai-architect` and `ai-testing-evaluation`; `application-security` reviews tool permissions.
- Design includes tool allow-lists, step and cost limits, prompt-injection defences (tool output is data), tracing and evaluation of workflows.
- Loop limits and human approval for write actions are explicit design elements.

## Human gates
`requirements`, `architecture` (tool permissions are `security-sensitive`), `plan`, `release`.

## Acceptance for this sample
Every agent has an explicit tool list; write actions need approval; there is a bounded-loop rule; an injection test scenario exists; tracing is designed in.
