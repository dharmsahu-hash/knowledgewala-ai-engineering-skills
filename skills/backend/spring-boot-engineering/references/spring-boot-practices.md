# Spring Boot practices (3.x, `jakarta.*` namespace)

## Controller and DTO
```java
public record CreatePaymentRequest(
    @NotBlank @Size(max = 64) String reference,
    @Positive long amountMinor,
    @Pattern(regexp = "[A-Z]{3}") String currency) {}

@RestController @RequestMapping("/v1/payments") @Validated
class PaymentController {
  private final PaymentService service;
  PaymentController(PaymentService service) { this.service = service; }   // constructor injection

  @PostMapping
  ResponseEntity<PaymentResponse> create(@RequestHeader("Idempotency-Key") String key,
                                         @Valid @RequestBody CreatePaymentRequest req) {
    return ResponseEntity.status(201).body(service.create(key, req));
  }
}
```

## Errors
One `@RestControllerAdvice` maps exceptions to a stable body `{code, message, correlationId}`. Never expose stack traces or SQL.

## Transactions
`@Transactional` on service methods, not controllers or repositories. Keep remote calls outside. Read-only paths: `@Transactional(readOnly = true)`. Self-invocation bypasses the proxy: call through another bean. Checked exceptions do not roll back by default; declare `rollbackFor` when needed.

## JPA
- Default `LAZY` associations; use `JOIN FETCH`, entity graphs or DTO projections for list endpoints (N+1).
- Enable SQL logging in tests to assert query counts on hot paths.
- `ddl-auto=validate` (or `none`) outside throwaway environments; schema via Flyway/Liquibase.
- `open-in-view=false`.

## Security (Spring Security 6)
Default deny with `SecurityFilterChain`; method security for fine rules; password hashing with `DelegatingPasswordEncoder`/bcrypt-argon2; CSRF stays on for browser sessions and may be disabled only for stateless token APIs, with the reason documented; restrictive CORS origins; validate JWT issuer, audience and expiry.

## Configuration
Typed `@ConfigurationProperties` with validation; profiles for environment differences; secrets from environment or a vault; no defaults for secrets.

## Observability
Actuator health/readiness, Micrometer metrics with low-cardinality tags, trace/correlation id in logs, no PII in logs.

## Testing
`@WebMvcTest` for controllers, `@DataJpaTest` for repositories (with the real engine via Testcontainers when available), `@SpringBootTest` sparingly, security tests with `spring-security-test`.
