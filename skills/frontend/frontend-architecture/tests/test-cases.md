# Test cases: frontend-architecture

Manual scenarios; record results in `evals/results/`, never mark a case passed unless it was run.

| ID | Input | Expected behaviour |
|---|---|---|
| FA-1 | New dashboard UI | State ownership table, design tokens, data-access conventions, numeric budgets |
| FA-2 | No accessibility target given | Proposes WCAG 2.2 AA as an inference and asks to confirm |
| FA-3 | Feature importing another feature's internals | Flags dependency direction violation with fix |
| FA-4 | Raw server error shown to users | Replaced by mapped message with correlation id |
