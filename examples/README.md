# Sample projects

Six realistic briefs for exercising the `ai-sdlc-orchestrator` end to end. Each brief states the business request, what the orchestrator must do, where humans must approve, and how to judge a run.

| Sample | Focus |
|---|---|
| [spring-boot-payment-api](spring-boot-payment-api/brief.md) | Java/Spring Boot REST, idempotency, security gate |
| [angular-frontend](angular-frontend/brief.md) | Angular UI, accessibility, auth |
| [mysql-database-design](mysql-database-design/brief.md) | Schema, indexes, destructive-change gate |
| [aws-deployment](aws-deployment/brief.md) | AWS architecture, production-deploy gate |
| [rag-application](rag-application/brief.md) | RAG design, evaluation, data privacy |
| [multi-agent-application](multi-agent-application/brief.md) | Multi-agent orchestration, guardrails |

**Status:** briefs are ready. Running them against a live assistant and scoring the outputs (`kw-skills eval score`) has **not** been done yet; results go in `evals/results/`.
Note: specialist skills for Angular, AWS, RAG and agentic design are on the roadmap and not yet shipped; for those samples the orchestrator must say that it applied generic guidance without a specialist skill.
