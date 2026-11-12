---
name: hld-generator
description: Produces a High-Level Design from approved requirements and architecture decisions - system architecture, major components, data flow, integration points, API boundaries, infrastructure, security architecture and scalability strategy. Use when architecture is decided and a reviewable system-level design document is needed before low-level design or implementation planning.
license: MIT
compatibility: Works in any Agent Skills capable assistant. Diagrams use Mermaid.
metadata:
  title: High-Level Design Generator
  version: "1.0.0-rc.2"
  author: KnowledgeWala
  category: architecture
  tags: "hld, high-level-design, architecture, data-flow, security-architecture"
  tier: paid
---

# High-Level Design Generator

## Purpose
Produce the system-level design that engineers, security and operations can review before detailed design starts.

## When to use
- Requirements and key architecture decisions (ADRs) are approved.
- A reviewable design document is required for a feature, service or system.

## When not to use
- No approved requirements: use `requirement-analysis`.
- Architecture options are still open: use `solution-architecture`.
- You need class diagrams, schemas or method contracts: use `lld-generator`.

## Required inputs
- Approved requirements (FR/NFR ids) and ADRs.
- Existing system context if this is a change: repos, services, data stores. Inspect the code before asserting how it works.

## Instructions
1. Every design element must trace to an FR/NFR or ADR; cite the id.
2. Follow [templates/hld.md](templates/hld.md). Keep to system level; push detail to LLD.
3. Describe only what exists when documenting current state, and what is proposed when designing. Label each clearly.
4. Security architecture is mandatory: trust boundaries, authN/authZ, data classification, secrets handling, encryption in transit and at rest.

## Workflow
1. Scope, assumptions, constraints, glossary.
2. System context diagram and major components with responsibilities.
3. Data flow for each primary use case, including failure paths.
4. Integration points and API boundaries (contract-level only).
5. Data architecture: stores, ownership, retention.
6. Infrastructure and deployment topology; environments.
7. Security architecture and threat considerations.
8. Scalability, availability, observability and DR strategy.
9. Risks, open questions, traceability to requirements.

## Quality gates
- Every component has a stated responsibility and an owner of its data.
- Each primary use case has a happy-path and failure-path flow.
- Every NFR has a design response or is listed as unaddressed.
- Trust boundaries are drawn and each crossing has authentication stated.
- Approval requested for security-sensitive and infrastructure-cost-significant elements.

## Expected output
HLD document with sections: Overview, Context Diagram, Components, Data Flow, Integration and API Boundaries, Data Architecture, Infrastructure, Security Architecture, Scalability and Resilience, Observability, Risks, Traceability.

## Validation rules
- Mermaid blocks parse; every component in prose appears in a diagram and vice versa.
- No orphan requirement: each FR/NFR is referenced at least once.
- No secrets, real hostnames or credentials in the document.

## Error handling
- Missing requirement detail: add an open question and a clearly labelled assumption.
- Contradiction with an approved ADR: stop and raise it; do not override the ADR.
- Code inspection impossible: mark current-state claims as unverified.

## Examples
See [references/hld-example.md](references/hld-example.md).

## Limitations
- Not a substitute for threat modelling workshops or capacity testing.
- Describes design intent; it does not verify the implementation matches.
