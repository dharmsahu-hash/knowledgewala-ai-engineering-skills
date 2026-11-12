# Pricing recommendation (proposal, requires owner approval)

This is a packaging strategy, not confirmed Agensi pricing and not demand data. No price has been set anywhere. Agensi's homepage says creators set prices, one-time or subscription, with a 30% platform fee (creators keep 70%) and a money-back guarantee if a skill does not do what its listing promises; confirm terms in the creator dashboard before deciding.

| Tier | Skills | Proposal | Rationale |
|---|---|---|---|
| Free | `requirement-analysis`, `code-review`, `test-engineering` | Free | Adoption and feedback; they showcase output-checker scripts and honesty rules |
| Paid | `solution-architecture`, `hld-generator`, `lld-generator`, `java-engineering`, `spring-boot-engineering`, `database-engineering`, `api-design-integration`, `angular-engineering`, `frontend-architecture`, `rag-engineering`, `ai-testing-evaluation`, `application-security`, `performance-engineering`, `aws-cloud-architecture`, `cicd-release-engineering` | One-time, price TBD | Deep reference material and templates |
| Premium | `ai-sdlc-orchestrator`, `agentic-ai-architect` | One-time or subscription, price TBD | Flagship; gate tooling and traceability |
| Bundle | All twenty | Discount versus individual | Natural workflow set |
| Enterprise | Customisation, private skills, training | Contact KnowledgeWala | Outside the marketplace |

Guidance for the owner:
- Start low or free to collect reviews; the refund guarantee means vague claims are costly, so the listings avoid unmeasured promises.
- Because the real-world evaluation has not been run, avoid premium pricing until at least three scored runs exist (see docs/QUALITY_MODEL.md).
- Tiers are stored per skill as `metadata.tier` and drive the generated listings; change them there.
