# Angular practices (16+)

## Components
Standalone components, `ChangeDetectionStrategy.OnPush`, small templates, inputs typed (`@Input({ required: true })`), signals for local state where the version supports them. Smart (container) vs presentational split.

```ts
@Component({ standalone: true, selector: 'kw-payment-list', changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [AsyncPipe, NgFor], templateUrl: './payment-list.component.html' })
export class PaymentListComponent {
  private readonly api = inject(PaymentApi);
  readonly payments$ = this.api.list();            // async pipe unsubscribes automatically
}
```

## RxJS
Prefer `async` pipe; otherwise `takeUntilDestroyed()`. Use `switchMap` for latest-wins (search), `concatMap` for ordered writes, `exhaustMap` for ignoring duplicate clicks. Handle errors with `catchError` and a user-visible state; never leave a stream silently dead.

## Forms
Typed reactive forms; validators in one place; show errors after touch; disable submit while pending; map server validation errors back to controls.

## Auth and interceptors
Interceptor adds the token and handles 401 by a single refresh-and-retry. Prefer HttpOnly secure cookies over web storage where the backend allows (XSS exposure). Route guards improve UX only; the server enforces authorisation. Token storage choice = security-sensitive decision requiring approval.

## Accessibility
Native elements first; labels and `aria-*` only where native semantics are insufficient; visible focus; logical tab order; error text linked to inputs; contrast checked; announcements for async changes (`aria-live`).

## Performance
Lazy-loaded routes, `trackBy`/`track`, avoid function calls in templates, virtual scroll for long lists, image optimisation, bundle budgets in `angular.json`, measure with the production build and Lighthouse before tuning.
