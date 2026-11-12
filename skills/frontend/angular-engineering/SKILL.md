---
name: angular-engineering
description: Builds and reviews Angular 16+ applications - standalone components, services and dependency injection, RxJS, signals, state management, routing and guards, reactive forms, HTTP interceptors, authentication, accessibility and performance. Use when implementing or changing an Angular frontend, diagnosing change-detection or RxJS problems, or reviewing Angular code.
license: MIT
compatibility: Angular 16+ with TypeScript. Verify the project's actual Angular version in package.json before applying advice.
metadata:
  title: Angular Engineering Specialist
  version: "1.0.0-rc.2"
  author: KnowledgeWala
  category: frontend
  tags: "angular, typescript, rxjs, forms, accessibility, performance"
  tier: paid
---

# Angular Engineering Specialist

## Purpose
Deliver maintainable, accessible, performant Angular code that matches the project's version and conventions.

## When to use
- Implementing or changing Angular components, services, routes or forms.
- Diagnosing change-detection, memory-leak or RxJS issues.
- Reviewing Angular code for accessibility and performance.

## When not to use
- General UI architecture and design systems: use `frontend-architecture`.
- Backend or API contract work: use `api-design-integration`.

## Required inputs
- Angular and TypeScript versions, build tool, existing project structure (inspect).
- Approved requirements and API contract the UI consumes.
- Accessibility target (for example WCAG 2.2 AA) if known.

## Instructions
1. Inspect package.json, angular.json, tsconfig and a neighbouring feature to match conventions.
2. Follow the reference for components, RxJS, forms, auth and performance.
3. Authentication token storage and similar security choices need human approval before applying.
4. Run lint, unit tests and a production build; report the real output.
Detailed checklists and examples: [references/angular-practices.md](references/angular-practices.md).

## Workflow
1. Confirm versions and scope.
2. Write tests for the behaviour first where practical.
3. Implement standalone, OnPush components with typed forms and services.
4. Handle loading, empty and error states explicitly.
5. Add guards and interceptors for auth and error handling.
6. Check keyboard access, labels, focus order and contrast.
7. Run `ng lint`, `ng test`, `ng build --configuration production`.

## Quality gates
- Strict TypeScript compiles with no `any` in new code.
- Subscriptions are managed (async pipe, `takeUntilDestroyed`).
- Every interactive element is keyboard operable and labelled.
- No tokens in logs or URLs; storage choice documented.
- Tests and production build ran, with results quoted.

## Expected output
Source and tests, notes on accessibility and performance decisions, the commands run with real results, and open risks.

## Validation rules
- Lint, tests and production build exit 0, commands shown verbatim.
- No unmanaged subscriptions or DOM-bypassing `innerHTML` without sanitisation.
- Accessibility acceptance criteria map to tests or a manual checklist.

## Error handling
- Build fails: fix the first real error; do not weaken strictness flags.
- Cannot run the toolchain: say so and mark results unverified.
- Version-specific API unclear: check the installed version, not memory.

## Examples
See the component, RxJS and interceptor patterns in the reference.

## Limitations
- Cannot verify visual rendering or screen-reader behaviour without a browser run.
- NgRx and other state libraries covered at pattern level only.
- AngularJS and pre-16 projects are out of scope.
