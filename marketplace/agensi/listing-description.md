# AI SDLC Orchestrator (flagship listing draft)

> Draft for owner review. Not published. Claims below are limited to what is implemented and tested in this repository.

**Skill id:** `ai-sdlc-orchestrator` · **Version:** 1.0.0-rc.1 · **License:** MIT · **Category:** Orchestration / Software engineering
**Tags:** sdlc, orchestration, governance, approval-gates, traceability, requirements, architecture, code-review

## Short description
Run any software project through requirements, architecture, design, code, tests, review and release with script-enforced order, evidence and human approval gates.

## Detailed description
Most AI coding sessions jump straight to code. The AI SDLC Orchestrator makes the assistant follow a 16-stage lifecycle instead:

1. Requirement analysis and approval
2. Architecture, HLD, LLD
3. Implementation planning and task decomposition
4. Specialist delegation, code generation
5. Unit and integration tests
6. Security assessment, code review, defect resolution (bounded to 3 rounds)
7. Release readiness and documentation

A small Python gate tool records stage evidence and refuses to advance if a stage is skipped, evidence is missing, or a human approval is pending. Six situations always stop for a human: major architecture decisions, destructive database changes, security-sensitive changes, secrets, production deployment, scope changes. The assistant cannot approve for you.

Includes a requirements-to-test traceability matrix, delegation briefs for nine companion KnowledgeWala skills, and six sample projects (Spring Boot payments, Angular, MySQL, AWS, RAG, multi-agent).

## What it is not
Not a deployment tool, not a guarantee of correct software, and not a replacement for engineers. It makes AI-assisted development more disciplined and auditable.

## Requirements
An assistant that supports the Agent Skills format and can run commands. Python 3.10+ for gate enforcement (without it, enforcement falls back to instructions). Works best with the companion skills installed.

## Installation
See [installation-instructions.md](installation-instructions.md).

## Usage example
"Use ai-sdlc-orchestrator for this project: merchants need an API to accept and refund card payments and never charge twice."
Expected: clarification questions, a requirements document for your approval, then architecture with a security-sensitive flag for the payment design, and so on, with evidence recorded at each stage.

## Limitations
- Gate enforcement validates process, not truth: it cannot verify that evidence is genuine or that an approval came from a human.
- Not yet evaluated end to end with scored real-assistant runs; platform discovery not live-tested.
- Specialist skills for Angular, AWS, RAG, agentic design and security are on the roadmap; the orchestrator says so when it works without them.

## Changelog
See repository CHANGELOG.md (1.0.0-rc.1: initial release candidate).

## Pricing
Proposal only, see [pricing-recommendation.md](pricing-recommendation.md). Final price set by the owner.
