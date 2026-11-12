# Review format

## Severity
- **Critical**: exploitable security flaw, data loss or corruption, outage on a main path.
- **High**: incorrect behaviour on a realistic path, serious security weakness, missing required error handling.
- **Medium**: maintainability or performance problem with real cost, missing important tests.
- **Low**: style, naming, minor clarity.

## Finding template
```
### F-1 [High] src/main/java/com/acme/PaymentService.java:88
- **Status:** Confirmed | Potential
- **Evidence:** what you saw (quote the line or describe the control flow)
- **Explanation:** why it is wrong
- **Impact:** business or technical consequence
- **Remediation:** concrete fix
```

## Example
```
### F-1 [High] src/main/java/com/acme/PaymentService.java:88
- **Status:** Confirmed
- **Evidence:** `chargeProcessor(req)` is called inside the `@Transactional` method before `repo.save(payment)`.
- **Explanation:** A processor timeout after a successful charge rolls back the local row, so the charge exists without a record.
- **Impact:** Customer charged with no payment record; retry may charge again.
- **Remediation:** Save PENDING first, commit, then call the processor, then update; reconcile on timeout.
```

## Verdict line
`**Verdict: BLOCKED**` (or `APPROVED`, `APPROVED WITH SUGGESTIONS`). BLOCKED is required if any Critical or High finding is Confirmed.

## Review limits section
List files not reviewed, tests not run, and assumptions.
