# Sample: multi-agent application

## Business request
"An internal assistant where a planner agent delegates to a research agent and a code agent, with a human approving anything that writes to a repository."

## Expected orchestrator behaviour
- Requirements define agent roles, tool permissions, memory scope and failure behaviour.
- Design includes tool allow-lists, step and cost limits, prompt-injection defences (tool output is data), tracing and evaluation of workflows.
- Loop limits and human approval for write actions are explicit design elements.
- No agentic-AI specialist skill shipped yet: the orchestrator says so.

## Human gates
`requirements`, `architecture` (tool permissions are `security-sensitive`), `plan`, `release`.

## Acceptance for this sample
Every agent has an explicit tool list; write actions need approval; there is a bounded-loop rule; an injection test scenario exists; tracing is designed in.
