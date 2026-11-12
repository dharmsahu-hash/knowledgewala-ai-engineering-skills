# Security checklists

## Finding format
```
### S-1 [High] src/.../OrderController.java:57
- **Status:** Confirmed | Potential
- **Category:** A01 Broken Access Control
- **Evidence:** the handler loads the order by id and never compares owner to the caller.
- **Impact:** any authenticated user can read another customer's order.
- **Remediation:** enforce ownership in the service layer; add a test for cross-user access.
```

## OWASP Top 10 (2021) coverage prompts
A01 access control, A02 cryptographic failures, A03 injection, A04 insecure design, A05 misconfiguration, A06 vulnerable components, A07 authentication failures, A08 integrity failures (deserialisation, CI/CD), A09 logging and monitoring failures, A10 SSRF. Mark each assessed / not assessed / not applicable.

## Authorisation
Check object-level (IDOR) and function-level access on every endpoint; default deny; do not rely on client-side checks; test cross-tenant access.

## Injection
Parameterised queries only; no string-built SQL, shell or template input; validate type, length and format at the boundary; encode output by context.

## Secrets
None in source, config committed to version control, logs or error messages; use a secret store; rotate anything exposed; scan history if a secret was committed.

## Data exposure
Minimise fields in responses, mask sensitive values in logs, avoid stack traces to clients, encrypt in transit and at rest, define retention.

## API security
Authentication on every operation, rate limiting, schema validation, mass-assignment protection (explicit allow-lists), safe pagination limits, CORS restricted to known origins.

## Dependencies
Record name, version, advisory id and fixed version; distinguish reachable from unreachable use where evidence allows; pin and verify integrity.

## Severity guide
Critical: remote, unauthenticated, high-impact. High: authenticated exploit with significant data or control impact. Medium: limited impact or needs unusual conditions. Low: hardening.
