# CG_TDD_TESTS_42 — Test Strategy for Automated Invoice Generation and Email Delivery (GitHub Issue #42)

Based on CG_TDD_42.md analysis. Stack: Next.js 14 (App Router), PostgreSQL, Prisma, BullMQ + Redis, S3/R2 storage, Stripe, Email provider (Resend/SendGrid), integrates with existing auth and time tracking.


## 1) Test Strategy Overview
- Goals
  - Validate accurate invoice creation from time entries, correct tax calculation, reliable PDF generation, and secure email delivery with robust status tracking (sent, opened/viewed, paid).
  - Ensure access control and security: signed links, webhook verification, idempotency, and audit trail.
  - Verify multi-template support and branding fidelity.
  - Establish performance and reliability expectations for rendering and delivery pipelines.
- Scope
  - API routes: /api/invoices, /api/invoices/[id]/render, /api/invoices/[id]/send, /api/invoices/[id]/download, /api/invoices/[id]/open-pixel (or /open), /api/webhooks/stripe, list/filter.
  - Services: InvoiceService, TaxService, PdfRenderer, EmailService, StorageService, Queue/Job workers, StripeWebhookHandler, SignedLinkService, Event logging.
  - Database: Prisma schema constraints, transactional integrity, idempotency patterns.
- Out of scope
  - Full client portal features beyond viewing an invoice via signed link; recurring invoices.
- Test levels
  - Unit tests (services, helpers)
  - Integration tests (API + DB + queues + storage mocked at boundaries)
  - End-to-end tests (browser flows with real API; external providers mocked)
  - Non-functional: performance for render, resilience/retry behavior


## 2) Unit Test Specifications (functions/methods to test)

- InvoiceService
  - createFromTimeEntries(userId, timeEntryIds, params):
    - Validates ownership; rejects non-owned or already-invoiced entries.
    - Aggregates items: quantity x unitPrice, subtotal, currency formatting.
    - Assigns invoice number atomically (per-user sequence).
  - computeTotals(invoice): subtotal, taxTotal, total; handles quantity decimals and rounding (half-up, 2 dp).
  - preventDoubleBilling(timeEntryIds): sets invoiceItemId on time entries in a transaction.

- TaxService
  - computeTaxLines(invoice, jurisdiction): applies TaxRule(s) including compound rules, multiple lines (e.g., VAT + regional), zero-rated, exemptions.
  - rounding behavior: verify 0.005 cases, totals across many lines.
  - snapshotting: TaxLine captures rate and name at time of computation.

- PdfRenderer (HTML -> PDF)
  - renderHtml(invoice, template, branding): variable substitution (client, items, totals, tax lines, invoice number, dates).
  - currency/locale formatting and typography application from branding.
  - renderPdf(html): returns bytes, checksum; time-budget awareness (timeout handling).
  - template variants: supports at least two HTML templates; missing variable detection.

- EmailService (with adapter abstraction)
  - composeInvoiceEmail(invoice, options): subject, from, to, reply-to; includes signed view link; attachment toggle.
  - send(message): provider adapter called with correct payload; error mapping and retryable vs non-retryable classification.
  - open-pixel url generation includes signed token (no sensitive data in clear).

- StorageService
  - put(buffer, key, metadata): returns url; sets content-type application/pdf; verifies checksum metadata.
  - getSignedUrl(key, ttl): short TTL; denies on missing key.

- SignedLinkService
  - sign(resourceId, purpose, ttl) and verify(token): correct HMAC, expiry handling, single-use option if enabled.

- Queue/Job orchestration
  - enqueueRender(invoiceId), enqueueEmail(invoiceId): proper job data, idempotent job keys, backoff settings.
  - worker handlers: update InvoiceEvent (rendered, sent, delivered) exactly once; retries do not duplicate events.

- StripeWebhookHandler
  - verifySignature(headers, payload): valid and invalid cases; clock skew tolerance.
  - handleEvent(payment_success, refund, failure): maps to invoice via metadata; idempotent updates; records InvoiceEvent paid/failed.

- Permissions/Access control
  - ensureUserOwnsInvoice(userId, invoiceId) and ensureTimeEntriesOwned: throws on cross-tenant access.
  - rate limiting hooks called for endpoints.

- Utilities
  - money math helpers (safe decimal operations), date formatting, invoice numbering (atomic increment per user).

- Prisma schema constraints (via unit-like repository tests)
  - Invoice.number uniqueness; foreign key integrity; not-null constraints; enum status transitions allowed.


## 3) Integration Test Requirements (API endpoints, database interactions)

- Happy path: Create → Render → Send → Open → Pay
  - POST /api/invoices with owned timeEntryIds returns DRAFT invoice with items, computed taxes; events: created.
  - POST /api/invoices/[id]/render queues job; worker stores pdf in S3 (mock), sets pdfUrl/checksum, status RENDERED; event: rendered.
  - POST /api/invoices/[id]/send queues email; worker sends via provider (mock), sets status SENT; event: sent.
  - GET /api/invoices/[id]/open-pixel?token=... records OPENED (debounced) without leaking token.
  - GET /api/invoices/[id]/download?token=... returns PDF (mock url), event: viewed; denies on expired/invalid token.
  - POST /api/webhooks/stripe with payment_intent.succeeded updates status PAID; idempotent on replay.

- Database interactions
  - Transactional creation: invoice + items + timeEntry linkage must succeed or roll back as a unit.
  - InvoiceEvent immutability; latest status denormalized to Invoice.status remains consistent.
  - Concurrency: two parallel sends do not create duplicate SENT events or duplicate emails.

- Error and retry flows
  - Render failure (Chromium error) triggers retry with backoff, marks failed after max attempts; records failed event.
  - Email provider temporary failure -> retries; permanent failure -> bounced/failed event.
  - Webhook signature invalid -> 400; valid but unknown invoice -> 200 with no-op and audit note.

- Filters and listing
  - GET /api/invoices?status=SENT&clientId=... returns correct filtered results with indexes used (observable via explain in dev or reasonable latency thresholds).

- Security
  - Auth required for all protected endpoints; time entry ownership enforced; no PII leaks in logs or URLs.


## 4) End-to-End Test Scenarios (user workflows)

- Freelancer creates and sends an invoice
  - Login → select time entries → choose template → preview (WYSIWYG) → click Generate PDF → Send email (link-only by default) → UI shows status timeline moving from Draft → Rendered → Sent.

- Client receives and views invoice
  - Open email (simulated inbox) → click secure link → invoice page loads without auth → PDF available to download → system records Viewed and Opened events.

- Payment status reflected
  - Simulate Stripe checkout completion → webhook processed → UI updates to Paid and shows event in timeline.

- Multiple templates and branding
  - Switch templates and brand colors/logo → preview updates → generated PDF reflects selected template and branding.

- Access control and link security
  - Expired link cannot download; regenerating link from UI works; unauthorized user cannot access another user’s invoice.

- Large invoice performance
  - Invoice with 100+ items renders within target time; UI remains responsive (uses skeletons/throttling).


## 5) Mock and Test Data Strategy

- Providers and infrastructure mocks
  - Email provider: adapter mock capturing payload and simulating delivered/bounced states.
  - Stripe: webhook event fixtures (succeeded, failed, refund) with signature verification using test secret.
  - S3/R2: in-memory storage mock providing put/getSignedUrl and storing metadata.
  - Puppeteer/Chromium: mock renderPdf returning deterministic PDF bytes and checksum; separate integration test with real headless run in CI nightly.
  - Redis/BullMQ: use ioredis-mock or local Redis in CI; verify job enqueue, backoff, retries, and idempotent job keys.

- Test data factories (e.g., @faker-js/faker + factory helpers)
  - User, Client (with PII fields), TimeEntry (owned by user; rates, durations), InvoiceTemplate (two variants), TaxRule (e.g., US-CA 7.25%, EU-DE 19%, compound example), Invoice entities, Event entities.

- Determinism and time control
  - Freeze time with fake timers for predictable timestamps and status transitions.
  - Fixed rounding mode: half-up to 2 decimals for currency totals; assert formatted strings where required.

- Security tokens and secrets
  - Use test env secrets for HMAC signing; ensure tokens never logged in plaintext; sanitize logs in tests.


## 6) Coverage Requirements and Success Criteria

- Coverage thresholds (Jest)
  - Core services (TaxService, InvoiceService, PdfRenderer, EmailService, SignedLinkService, StripeWebhookHandler): 90% statements, 90% branches, 95% lines.
  - Access control, idempotency, and signature verification code: 100% branch coverage.
  - Overall repository: ≥ 85% statements/branches.

- Success criteria
  - All happy-path and critical edge-case tests pass.
  - Rendering P95 < 2s in integration/perf test with 50 item invoice (measured with real Chromium once per CI pipeline or nightly); failures flagged but may be non-blocking on PR runs.
  - No duplicate events for retries/replays; idempotency verified under concurrent requests.
  - Security checks (auth, signed links, webhook verification) behave correctly.


## 7) TDD Implementation Order (tests first, then code)

1) Data and access foundations
  - Write tests: Prisma models constraints (invoice number unique, event fk); ensureUserOwnsInvoice and ensureTimeEntriesOwned.
  - Implement minimal Prisma schema/migrations and access helpers.

2) Invoice creation from time entries
  - Write tests for InvoiceService.createFromTimeEntries: ownership, aggregation, atomic invoice numbering, timeEntry linkage, computeTotals.
  - Implement service and POST /api/invoices handler with Zod validation.

3) Tax calculation engine
  - Write tests for TaxService.computeTaxLines: various jurisdictions, compound taxes, rounding.
  - Implement TaxService and integration in invoice creation.

4) PDF rendering and storage
  - Write tests: PdfRenderer.renderHtml variable substitution and formatting; renderPdf timeout behavior; StorageService.put metadata and signed url.
  - Implement templates (2 variants), renderer, storage; POST /api/invoices/[id]/render job enqueue + worker handler.

5) Email composition and sending
  - Write tests: EmailService.compose includes signed link; attachment toggle; provider adapter invoked; open-pixel link generation.
  - Implement EmailService, adapter, POST /api/invoices/[id]/send job enqueue + worker handler.

6) Status tracking and signed links
  - Write tests: SignedLinkService sign/verify expiry; download and open-pixel endpoints record events; debounce open events.
  - Implement GET /api/invoices/[id]/download and /open-pixel handlers and event recording.

7) Stripe webhooks and payment mapping
  - Write tests: signature verification, idempotency on replay, mapping metadata to invoice, status update to PAID.
  - Implement /api/webhooks/stripe handler and event updates.

8) List/filter and UI integration smoke tests
  - Write tests: GET /api/invoices filters; E2E flow from selection to send; template switching in preview.
  - Implement remaining UI glue and ensure status timeline updates.

9) Hardening
  - Write tests: retry/backoff behaviors, concurrency (parallel sends, double renders), PII not in logs/urls, sanitization of rich text.
  - Implement backoff strategies, debouncing, and sanitization.


## 8) Edge Cases and Error Scenarios to Test

- Ownership and integrity
  - Time entries from multiple users; some already invoiced; mixed valid/invalid IDs.
  - Attempt to access another user’s invoice by id; attempts to modify after PAID.

- Tax and money
  - Zero tax jurisdiction; multiple tax lines; compound vs non-compound; very small fractional amounts; rounding at item-level vs invoice-level.
  - Currency formatting for large totals; negative adjustments/credits line item (if allowed) guarded or computed correctly.

- PDF/template
  - Missing template variables; invalid HTML; extremely long notes field (sanitized); logo missing or oversized; right-to-left or unicode characters.
  - Large invoice (100–500 items) within resource constraints; renderer timeout and recovery.

- Email
  - Attachment enabled with large PDF near provider limit; provider rate-limit errors; bounced address; invalid recipient email.

- Links and security
  - Expired/invalid tokens; single-use link accessed twice; token replay from different IP/UA (if policy enforced); no leakage of raw identifiers.

- Queue and retries
  - Redis outage (enqueue fails); worker restart mid-job; duplicate jobs deduped by key; backoff escalation.

- Webhooks
  - Out-of-order events; refund after paid; signature invalid; unknown event type ignored gracefully.

- Observability
  - Event log contains actor, IP (when appropriate), user agent; correlation IDs propagated; PII masked in logs.


## 9) Tooling and Environment

- Test runner: Jest + ts-jest; assertions: @testing-library for UI, supertest for route handlers.
- DB: Test Postgres (Docker) or Prisma + sqlite for unit/integration; transactions with rollback per test.
- Browser E2E: Playwright (preferred) or Cypress; mock email inbox via MailHog/Mailslurper or provider adapter capture.
- Mocks: nock/MSW for HTTP; ioredis-mock or Redis container; puppeteer real run in nightly.
- CI: Parallelize unit/integration and E2E; artifacts: sample PDFs, coverage reports; thresholds enforced.


## 10) Test Case Catalog (high level names)

- Unit
  - TaxService computes multiple tax lines with compound rule
  - InvoiceService creates draft and links time entries atomically
  - PdfRenderer substitutes variables and formats currency per locale
  - EmailService composes message with signed link and optional attachment
  - SignedLinkService rejects expired token
  - StripeWebhookHandler is idempotent on replayed events

- Integration
  - Create → Render → Send → Open → Pay updates status and events exactly once
  - Render failure retries with backoff and final failure event
  - Concurrent send requests do not duplicate emails or events

- E2E
  - Freelancer builds and sends invoice; timeline updates
  - Client opens link and downloads PDF; view event recorded
  - Payment webhook updates timeline to Paid


## 11) Notes and Assumptions

- Rounding mode is half-up to 2 decimals unless PRD specifies otherwise.
- Email default is link-only; attachments behind feature flag.
- All public invoice links are signed and short-lived; download link may be regenerated on demand.
- Stripe metadata includes { invoiceId, invoiceNumber } to associate payments.
