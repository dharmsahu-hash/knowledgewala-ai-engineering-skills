# Java practices

## Language (check JDK first)
- 17+: records for data carriers, sealed types for closed hierarchies, switch expressions, text blocks.
- 21+: pattern matching for switch, virtual threads (good for blocking I/O; not for CPU-bound work), sequenced collections.
- Do not use preview features in production code without explicit approval.

## Correctness
- Prefer immutable objects; make fields `final`; copy defensive collections at boundaries (`List.copyOf`).
- Avoid null returns for collections; use `Optional` only as a return type, never as a field or parameter.
- Money: `BigDecimal` with explicit scale and rounding, or integer minor units. Never `double`.
- Always specify charset and `Locale` for text/format operations; use `java.time`, not `Date`.
- `equals`/`hashCode` together; records give both.

## Exceptions
Catch the narrowest type; never swallow; wrap with cause; do not use exceptions for flow control; do not log and rethrow the same error.

## Concurrency rules
1. Prefer no shared mutable state. 2. Use `java.util.concurrent` types over manual `wait/notify`. 3. Bound every pool and queue. 4. Shut executors down. 5. Do not call unknown code while holding a lock. 6. `ConcurrentHashMap.compute*` for atomic updates, never check-then-act on a plain map.

```java
// Unsafe: check-then-act race
if (!cache.containsKey(k)) cache.put(k, load(k));
// Safe
cache.computeIfAbsent(k, this::load);   // load must be quick and must not modify the map
```

## Streams
Use for transformation, not side effects. Keep pipelines short. Avoid streams in hot inner loops without measuring. `parallelStream()` only with a measured gain and thread-safe operations.

## JVM and GC (hypotheses until measured)
Start with defaults (G1). Collect GC logs (`-Xlog:gc*`), heap dumps for leaks, and flight recordings for CPU. Change one flag at a time and compare.
