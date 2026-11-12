# API design rules

## Resources and verbs
Plural nouns (`/payments`), no verbs in paths; actions that are not CRUD use a sub-resource (`POST /payments/{id}/refunds`). Use `GET` safe, `PUT` idempotent replace, `PATCH` partial, `DELETE` idempotent.

## Status codes
200 OK, 201 Created (+`Location`), 202 Accepted (async), 204 No Content, 400 malformed/validation, 401 unauthenticated, 403 forbidden, 404 missing, 409 conflict, 422 semantic error, 429 rate limited (+`Retry-After`), 5xx server.

## Error contract
```json
{ "code": "PAYMENT_DUPLICATE_KEY", "message": "Idempotency key reused with a different body", "correlationId": "c0ffee", "details": [] }
```
Stable machine `code`; no stack traces or SQL.

## Idempotency
Require an `Idempotency-Key` header on unsafe, retried operations. Same key and body returns the original response; same key with a different body returns 422. Keys expire after a documented window.

## Pagination
Prefer cursor pagination for large or changing sets (`?limit=50&cursor=...`); state the maximum limit; return `nextCursor`. Offset pagination only for small stable data.

## Versioning and compatibility
Compatible: add optional fields, add endpoints, loosen validation. Breaking: remove or rename fields, change types, tighten validation, change semantics. Version in the path (`/v1`) or a header, one policy only. Deprecate with `Deprecation`/`Sunset` headers and a documented window.

## Security
Authenticate every operation, scope per operation, rate limit per client, validate schemas strictly, never echo secrets, enable CORS only for known origins.

## Performance
Field selection or sparse responses for heavy resources, ETag/conditional GET where useful, bounded payloads, avoid chatty sequences by offering a purpose-built read model.
