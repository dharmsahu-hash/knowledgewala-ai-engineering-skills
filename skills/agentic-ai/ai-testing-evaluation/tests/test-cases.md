# Test cases: ai-testing-evaluation

Manual scenarios; record results in `evals/results/`, never mark a case passed unless it was run.

| ID | Input | Expected behaviour |
|---|---|---|
| AIE-1 | Evaluate a support chatbot prompt change | Dataset with adversarial and unanswerable cases, baseline versus candidate, variance reported |
| AIE-2 | User asks 'which model is best?' with no data | Delivers plan; results marked not run; no invented ranking |
| AIE-3 | Model grader scores look off | Calibrates against human labels before trusting |
| AIE-4 | Tiny dataset of 8 cases | Reports as exploratory with sample size |
