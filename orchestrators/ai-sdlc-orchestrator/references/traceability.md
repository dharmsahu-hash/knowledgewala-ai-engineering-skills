# Traceability

Maintain one matrix in `docs/sdlc/traceability.md`, extended at each stage.

| Req | Story/AC | Design (HLD/LLD ref) | Code (path) | Test (name) | Status |
|---|---|---|---|---|---|
| FR-1 | US-1 / AC-1 | HLD 3.1, LLD 4 | src/.../PaymentController.java | createPayment_valid_returns201 | verified (run 2026-..) |

Rules:
- Add the design column at stages 4-5, code at 9, test at 10-11, status at 13-15.
- `verified` means the test ran and passed in this project with evidence. Otherwise `designed`, `implemented`, `tested-not-run`, or `gap`.
- A requirement with no code or test at release readiness is listed as an open risk.
- Changed requirements get a new row version and a `scope-change` flag if significant.
