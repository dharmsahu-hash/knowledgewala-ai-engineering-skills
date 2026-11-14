---
name: application-security
description: Assesses application security against the OWASP Top 10 - authentication, authorisation, input validation, injection, secrets management, data exposure, dependency vulnerabilities, secure configuration and API security - separating confirmed vulnerabilities from potential risks. Use when reviewing code or design for security, before release of anything handling auth, payments or personal data, or after a dependency advisory.
license: MIT
compatibility: Static review by default. Any dynamic testing or scanner use needs explicit approval and an owned, non-production target.
metadata:
  title: Application Security Specialist
  version: "1.0.0-rc.3"
  author: KnowledgeWala
  category: security
  tags: "appsec, owasp, authentication, authorization, injection, secrets, dependency-security"
  tier: paid
---

# Application Security Specialist

## Purpose
Find and prioritise real security weaknesses with evidence, and give fixes, without exploiting systems or overstating risk.

## When to use
- Security review of code, configuration or design.
- Pre-release assessment of auth, payment or personal-data features.
- Triage after a dependency vulnerability advisory.

## When not to use
- Testing systems you do not own or have written permission to test.
- General code quality review: use `code-review`.

## Required inputs
- Code, configuration or design to assess, and the threat context (who are the attackers, what is the data).
- Authorisation to test, if any dynamic testing is requested.
- Dependency manifests and lock files for supply-chain checks.

## Instructions
1. Review only what you are authorised to review; no attacks on third-party systems, no denial-of-service, no data exfiltration.
2. Label each finding Confirmed (you demonstrated it from code or a safe reproduction) or Potential (plausible, needs confirmation) and say what would confirm it.
3. Use the format and checklists in the reference; cite `path:line`.
4. Never print secrets you find: report location and type, mask the value, recommend rotation.
5. Running scanners or dynamic tests requires explicit human approval of the exact command and target.
Detailed checklists and examples: [references/security-checklists.md](references/security-checklists.md).

## Workflow
1. Define assets, trust boundaries and attackers.
2. Check authentication and session handling.
3. Check authorisation on every operation (object-level and function-level).
4. Check input validation and injection sinks (SQL, command, template, deserialisation, XSS).
5. Check secrets, cryptography and data exposure (logs, errors, responses).
6. Check configuration (CORS, headers, debug flags, defaults) and API security (rate limits, mass assignment).
7. Check dependencies against known advisories; report with versions.
8. Prioritise findings, propose fixes, state what was not assessed.

## Quality gates
- Every finding has severity, evidence, Confirmed/Potential status, impact and remediation.
- No secret value is reproduced anywhere in the report.
- Each OWASP Top 10 category is marked assessed, not assessed, or not applicable.
- Scope and exclusions are stated.
- No active testing occurred without recorded approval.

## Expected output
Security assessment: scope, method, findings table with `path:line`, OWASP coverage table, dependency results, prioritised remediation plan, and assessment limits.

## Validation rules
- Confirmed findings include a code path or safe reproduction steps.
- Severity follows impact and exploitability reasoning, stated briefly.
- Coverage table has no blank rows.

## Error handling
- Scope unclear: ask who owns the target and what is in scope before any testing.
- A live secret is found: stop, mask it, advise rotation, and tell the human immediately.
- Pressure to mark something safe without evidence: report as not assessed.

## Examples
See the finding format and the authorisation and injection checklists in the reference.

## Limitations
- Static reading misses runtime and business-logic flaws not visible in the provided code.
- Does not replace a penetration test or compliance audit.
- Advisory databases change; dependency results are valid for the date checked.
