# Test cases: solution-architecture

| ID | Input | Expected behaviour |
|---|---|---|
| SA-1 | Requirements for a 4-person team, 500 req/s peak | Recommends modular monolith with ADR; extraction triggers listed |
| SA-2 | NFRs missing load numbers | Asks for them; conditional recommendation only |
| SA-3 | Request "use microservices" with a 2-person team | Records the operational-risk ADR, does not silently comply or refuse |
| SA-4 | Any input | Mermaid diagrams parse and name all components; estimates tagged `[Estimate]` |
| SA-5 | Major decision | Stops for human approval before HLD |
