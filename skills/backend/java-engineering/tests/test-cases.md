# Test cases: java-engineering

| ID | Input | Expected behaviour |
|---|---|---|
| J-1 | Cache using check-then-put on `HashMap` shared across threads | Identifies race; fixes with `computeIfAbsent` on `ConcurrentHashMap`; adds a test |
| J-2 | Money calculation with `double` | Switches to `BigDecimal` or minor units |
| J-3 | "Make it faster" with no data | Asks for or collects a baseline; advice labelled `[Hypothesis]` until measured |
| J-4 | Project on JDK 17 asked to use virtual threads | Notes JDK 21 requirement; offers alternative or upgrade path |
| J-5 | Failing build | Fixes root cause; does not disable tests; reports real command output |
