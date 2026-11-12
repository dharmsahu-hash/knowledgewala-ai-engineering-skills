# Agent design checklists

## Workflow shapes (simplest first)
1. Fixed pipeline (prompt chain) 2. Router to specialised prompts 3. Planner-executor with a bounded plan 4. Multi-agent with a supervisor. Move down the list only when the simpler shape fails a stated requirement.

## Tool specification template
| Field | Example |
|---|---|
| Name and purpose | `create_refund`: issue a refund |
| Input schema | JSON schema with required fields and limits |
| Permission | write, needs human approval |
| Idempotency | required `request_id` |
| Failure behaviour | return typed error; agent must not retry blindly more than 2 times |
| Rate and cost limit | 5 calls per run |

## Guardrails
Input: length, type and policy checks. Retrieval and tool output: treated as untrusted data, never executed as instructions; strip or quarantine instruction-like text. Output: schema validation, policy and PII checks. Limits: max steps, tokens, wall time and spend per run; circuit breaker on repeated tool errors. Secrets never enter prompts.

## Memory and context
Short-term (conversation window with trimming/summarisation), long-term (explicit store with scope, owner, retention and deletion), no cross-user leakage, memory writes validated.

## Observability
Trace id per run; log prompt version, tool calls, latency, tokens, cost, decision points; redact PII; sample for human review; alert on cost and error spikes.

## Evaluation (before release)
Task success rate on a fixed test set, tool-use correctness, injection scenarios, refusal behaviour, cost and latency per task, regression suite per prompt or model change.

## Multi-agent notes
Clear roles, typed hand-offs, a single owner of final output, shared state minimal and versioned, loop and deadlock limits.
