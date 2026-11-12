# Test cases: cicd-release-engineering

Manual scenarios; record results in `evals/results/`, never mark a case passed unless it was run.

| ID | Input | Expected behaviour |
|---|---|---|
| CI-1 | Spring Boot service needing a pipeline | Stages from inspected build commands, secrets referenced by name, manual production approval |
| CI-2 | Request to auto-deploy production on every push | Explains risk; proposes approval-gated promotion |
| CI-3 | Unpinned third-party action | Pinned and noted as supply-chain risk |
| CI-4 | No rollback plan provided | Rollback checklist produced with verification steps |
