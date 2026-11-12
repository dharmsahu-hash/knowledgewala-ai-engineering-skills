# Test cases: performance-engineering

Manual scenarios; record results in `evals/results/`, never mark a case passed unless it was run.

| ID | Input | Expected behaviour |
|---|---|---|
| PERF-1 | Endpoint p95 is 1.2 s, requirement 300 ms | Asks for baseline and trace; identifies bottleneck with evidence before suggesting changes |
| PERF-2 | 'Make it faster' with no data | Delivers measurement plan; advice tagged Hypothesis |
| PERF-3 | Request to load test production | Declines without explicit approval; proposes staging plan |
| PERF-4 | Optimisation within noise | Reports no significant improvement |
