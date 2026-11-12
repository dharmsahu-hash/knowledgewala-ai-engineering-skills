# Test cases: hld-generator

| ID | Input | Expected behaviour |
|---|---|---|
| HLD-1 | Approved payment requirements + ADRs | HLD with failure-path flow per use case; security architecture present |
| HLD-2 | Requirement set with an NFR the design cannot meet | NFR listed as unaddressed with reason |
| HLD-3 | Request that contradicts an approved ADR | Stops and raises conflict |
| HLD-4 | Existing repo supplied | Current-state claims cite inspected files; unverified claims labelled |
| HLD-5 | Any output | Mermaid parses; every FR/NFR referenced |
