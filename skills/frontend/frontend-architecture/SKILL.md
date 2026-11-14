---
name: frontend-architecture
description: Designs framework-neutral frontend architecture - component architecture, reusable design systems, responsive layout, accessibility, state management, API integration, error handling, performance, security and testing. Use when planning a new UI codebase, standardising components, or reviewing a frontend for structure, accessibility and resilience.
license: MIT
compatibility: Works in any Agent Skills capable assistant; framework-neutral. Pair with `angular-engineering` for Angular specifics.
metadata:
  title: Frontend Architecture and UI Engineering
  version: "1.0.0-rc.3"
  author: KnowledgeWala
  category: frontend
  tags: "frontend, architecture, design-system, accessibility, state-management, web-performance"
  tier: paid
---

# Frontend Architecture and UI Engineering

## Purpose
Give frontends a structure that scales across teams: clear component boundaries, one design system, predictable state and resilient data access.

## When to use
- Planning a new frontend or a major restructure.
- Defining a shared component library or design tokens.
- Reviewing a UI codebase for accessibility, security and performance.

## When not to use
- Framework-specific implementation details: use the framework skill (for Angular, `angular-engineering`).
- Backend design: use `solution-architecture`.

## Required inputs
- Approved requirements including accessibility and device targets.
- Chosen framework and constraints, or the decision still to make.
- API contracts the UI will consume.

## Instructions
1. Decide structure before components: feature boundaries, shared kit, data-access layer.
2. Apply the reference checklists for state, errors, accessibility, security and performance.
3. Record significant choices as ADRs through `solution-architecture`.
4. Never trust the client for authorisation or validation.
Detailed checklists and examples: [references/frontend-architecture-checklists.md](references/frontend-architecture-checklists.md).

## Workflow
1. Capture user journeys and device/accessibility targets.
2. Define feature modules and the shared design system (tokens, components).
3. Choose a state strategy per kind of state (server, UI, form, URL).
4. Define the data-access layer, error and loading conventions.
5. Set security rules (CSP, sanitisation, token handling).
6. Define the testing pyramid and performance budgets.
7. Document decisions and open risks.

## Quality gates
- Each kind of state has one owner and one mechanism.
- Design tokens exist for colour, spacing and type; components consume tokens only.
- Accessibility target is stated and mapped to tests.
- Every network failure has a user-visible state.
- Performance budgets are numeric.

## Expected output
Frontend architecture document: structure, design-system plan, state strategy, data-access conventions, security rules, testing and performance plan, ADR list.

## Validation rules
- Diagrams (Mermaid) parse and match the text.
- Budgets and targets are numbers, not adjectives.
- No secrets or real user data in examples.

## Error handling
- Framework undecided: present options with trade-offs and ask.
- Missing accessibility target: propose WCAG 2.2 AA as `[Inference]` and ask to confirm.
- Conflicting device targets: list the conflict and ask for priorities.

## Examples
See the state-ownership table and budget template in the reference.

## Limitations
- No visual design; produces structure and rules, not mock-ups.
- Cannot measure performance without running the app.
- Framework specifics are delegated.
