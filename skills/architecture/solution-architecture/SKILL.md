---
name: solution-architecture
description: Designs scalable, maintainable solution architecture - pattern selection, monolith versus microservices assessment, service boundaries, integration and event-driven design, resilience, cost and operations - and records decisions as ADRs with Mermaid diagrams. Use when approved requirements exist and a technology or structural decision must be made before detailed design or coding.
license: MIT
compatibility: Works in any Agent Skills capable assistant. Diagrams use Mermaid.
metadata:
  title: Solution Architecture Designer
  version: "1.0.0-rc.2"
  author: KnowledgeWala
  category: architecture
  tags: "architecture, adr, microservices, monolith, mermaid, resilience"
  tier: paid
---

# Solution Architecture Designer

## Purpose
Choose an architecture that fits the requirements, team and budget, and make every significant decision explicit, reasoned and reversible where possible.

## When to use
- Requirements are approved (see `requirement-analysis`) and the system shape is undecided.
- A monolith-versus-services, sync-versus-async, or build-versus-buy decision is pending.
- An existing architecture must be assessed for scale, resilience or cost.

## When not to use
- Requirements are not yet approved: do `requirement-analysis` first.
- Only class-level or schema-level detail is needed: use `lld-generator`.
- The change fits inside an existing, documented architecture with no new decision.

## Required inputs
- Approved requirements, especially NFRs (load, availability, data sensitivity, compliance).
- Constraints: team size and skills, budget, hosting, existing systems, deadlines.
- If NFR numbers are missing, ask. Do not size a system on invented traffic.

## Instructions
1. Start from the simplest design that meets the NFRs. Default to a modular monolith; justify each step toward distribution with a requirement it satisfies.
2. Evaluate at least two options per significant decision using [references/decision-framework.md](references/decision-framework.md). State the trade-offs and the option you recommend, then stop for approval on major decisions.
3. Write each decision as an ADR using [templates/adr.md](templates/adr.md).
4. Mark every cost, latency or capacity figure as `[Estimate]` with its assumption.

## Workflow
1. Restate drivers: top NFRs, constraints, risks.
2. Identify bounded contexts and candidate service boundaries (data ownership first).
3. Generate options (e.g. modular monolith, services, serverless) and score against drivers.
4. Define integration style (REST, messaging, events), API gateway need, and failure behaviour (timeouts, retries, circuit breaking, idempotency).
5. Define data stores per context and consistency model.
6. Draft system context, component and deployment diagrams (Mermaid).
7. List technology recommendations with alternatives and operational cost.
8. Record ADRs; list open risks; request approval.

## Quality gates
- Each decision has two or more evaluated options and a stated reason.
- Every NFR maps to a mechanism or an explicit "not addressed".
- Single points of failure and data-loss scenarios are named.
- Operational burden (monitoring, on-call, deployment) is stated for the team size.
- Human approval is recorded for major decisions before HLD begins.

## Expected output
Architecture decision document: Context and Drivers, Options Considered, Recommended Architecture, Diagrams (context, component, deployment), Technology Recommendations, Resilience and Scalability, Cost and Operations, Risks, ADR list.

## Validation rules
- Diagrams must parse as Mermaid and show every component named in the text.
- No technology is recommended without a reason tied to a driver.
- Numeric claims carry `[Estimate]` and an assumption, or a source.

## Error handling
- Conflicting NFRs (e.g. strict consistency and global low latency): present the trade-off and ask the owner to prioritise.
- Missing constraints: list them as open questions; give conditional recommendations.
- User insists on a pattern that conflicts with the NFRs: record the risk in an ADR and continue.

## Examples
See [references/decision-framework.md](references/decision-framework.md) for a worked monolith-versus-services scoring.

## Limitations
- Does not benchmark or load-test; capacity statements are reasoned estimates.
- Cloud pricing changes; verify costs against current provider calculators.
- Vendor-specific depth (for example AWS) is outside this skill's core.
