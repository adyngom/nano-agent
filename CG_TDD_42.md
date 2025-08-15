Title: CG_TDD_42 — Automated Invoice Generation and Email Delivery (GitHub Issue #42)

1) Issue summary and analysis
- Summary: Build an automated system to generate branded PDF invoices from selected time entries and deliver them to clients via email, while tracking status (sent, viewed, paid), supporting multiple templates, and applying tax calculations by jurisdiction. Tech stack: Next.js 14 (App Router), PostgreSQL, Prisma, Stripe. Integrate with existing authentication and time tracking.
- Scope decomposition:
  - Data modeling: Invoices, invoice items, templates, taxes, delivery and view events, and payment status.
  - PDF generation: Server-side render of invoice with branding and template selection.
  - Email delivery: Send with PDF attachment and/or signed download link; handle bounces.
  - Status tracking: sent (email queued/sent), viewed (open pixel + client portal view), paid (Stripe webhooks).
  - Template management: Multiple templates per user with default selection and branding.
  - Tax computation: Jurisdiction-aware tax lines; extensible for future integrations (TaxJar/Avalara).
  - Ops: Background jobs/queue for PDF build and email dispatch; storage for generated PDFs.
- Out of scope (for issue #42 unless explicitly expanded): Client portal build-out beyond invoice view, recurring invoices, multi-currency edge cases, advanced AI insights.

2) System impact assessment
- Backend services:
  - Add invoice generation service (HTML->PDF) and email service abstraction. Introduces a background worker (Bull/Redis or compatible) to avoid long-running serverless requests.
  - Extend Stripe integration to map payments to invoices and update status via webhook.
- Database & schema (Prisma):
  - New/extended models (high-level): Invoice, InvoiceItem, InvoiceTemplate, InvoiceEvent, EmailQueue, TaxRule (jurisdiction), TaxLine. Indexes on (userId, status, clientId, issueDate), and foreign keys for events.
- Storage:
  - Persist generated PDFs to S3/R2 with signed URLs. Optional caching and versioning per revision.
- API surface (Next.js route handlers):
  - POST /api/invoices (create from time entries)
  - POST /api/invoices/[id]/render (generate PDF)
  - POST /api/invoices/[id]/send (enqueue email send)
  - GET /api/invoices/[id]/download (signed URL; records view)
  - POST /api/webhooks/stripe (paid/failed/refund events)
  - GET /api/invoices (list with filters)
- Frontend:
  - UI to select time entries, choose template, preview invoice, send email, and display status timeline.
- Observability:
  - Audit logs for creation/sending/viewing/payment; metrics for generation latency, email delivery success, and webhook throughput.

3) Architecture decisions and rationale
- PDF generation approach: HTML-to-PDF using headless Chromium (Puppeteer or @sparticuz/chromium for serverless) over React-PDF.
  - Rationale: Highest template fidelity, matches UX strategy for PDF-accurate preview, supports brand typography and complex layouts. React-PDF is fine but less WYSIWYG vs HTML/CSS.
- Email provider abstraction: Implement EmailService with Resend or SendGrid adapter.
  - Rationale: PRD lists Resend/SendGrid; abstraction allows swapping and A/B of deliverability.
- Attachment vs link: Send signed link by default, optionally attach PDF when user opts in.
  - Rationale: Smaller emails, updated copies on re-render, better security and analytics; attachment opt-in for client expectations.
- Status tracking pattern: Immutable InvoiceEvent table for sent/viewed/paid/failed; denormalize latest status on Invoice for fast queries.
  - Rationale: Event sourcing lite improves auditability and analytics while keeping reads fast.
- Background jobs: Use BullMQ + Redis for rendering and emailing.
  - Rationale: Decouple long-running work from API, resiliency with retries and backoff. If Vercel only, run worker on separate Node process or AWS Lambda queues; alternative is Vercel queues.
- Tax calculation strategy: Rule-engine first (TaxRule + TaxLine), adapter interface for TaxJar/Avalara later.
  - Rationale: Start simple, enable compliance-grade integration without redesign.
- Security-first links: All public invoice links are signed, short-lived or single-use magic links. Email open tracked via 1x1 pixel with signed token tied to invoice.
  - Rationale: Prevent enumeration and unauthorized access; meets privacy requirements.

4) Security considerations
- Access control:
  - Only the freelancer (owner/team with permission) can create/send invoices; clients access via signed link or authenticated client portal.
  - Validate that all time entries belong to the requesting user and have not already been invoiced.
- Data protection:
  - Store client PII (name, email, address, taxId) encrypted at rest; avoid storing full tax IDs unencrypted. Mask display in UI/logs.
  - Signed URLs for PDF with short TTL; rotate salts/keys. Avoid permanent public URLs.
- Email security:
  - Configure SPF/DKIM/DMARC for domain; prefer provider-managed sending identities.
  - Avoid sensitive data in subject lines; do not include raw tokens in query params without HMAC; use opaque IDs.
- Webhooks:
  - Verify Stripe signatures; idempotency keys for state updates. Log all webhook attempts and replays.
- Injection/hardening:
  - Sanitize rich text (notes) in invoices; strictly validate template variables. Use server-side type validation (Zod) on APIs.
- Auditing:
  - Immutable InvoiceEvent rows with actor, IP (when appropriate), user agent for view/open events, and reason codes.
- Compliance path:
  - GDPR/CCPA data rights support (delete/anonymize). PCI scope limited to Stripe.

5) Performance implications
- Rendering:
  - Target <2s PDF generation P95. Pre-warm Chromium or pool workers; cache rendered PDFs per invoice revision to avoid re-render.
- Database:
  - Index frequent filters; use computed columns or materialized views for dashboard KPIs if necessary. Keep InvoiceEvent lightweight.
- Email throughput:
  - Use queue with exponential backoff; batch sending where possible; monitor provider rate limits.
- Webhooks:
  - Handle asynchronously; acknowledge 200 quickly and offload processing to jobs.
- Frontend:
  - Lazy-load preview and template assets; use skeletons; throttle live preview re-renders.

6) Recommended implementation approach
- Milestone 0: Foundations (1-2 days)
  - Add Prisma models and migrations.
  - Create service interfaces: PdfRenderer, EmailService, TaxService.
  - Introduce BullMQ worker and Redis configuration; feature flag for queue vs inline for local dev.
- Milestone 1: Invoice creation from time entries (3-4 days)
  - API: POST /api/invoices to build invoice draft from selected TimeEntry IDs.
  - Validate ownership and rates; compute subtotal and provisional taxes via TaxService.
  - UI: Invoice builder with client selector, items, tax panel, template picker.
- Milestone 2: PDF render & storage (2-3 days)
  - Implement HTML templates (at least 2 variants) and theming from FreelancerProfile branding.
  - Server job to render to PDF and upload to S3/R2; persist file metadata (url, checksum, bytes, revision).
  - API: POST /api/invoices/[id]/render; write InvoiceEvent: rendered.
- Milestone 3: Email sending & tracking (3-4 days)
  - API: POST /api/invoices/[id]/send -> enqueue email. Compose email with summary, signed view link, optional attachment.
  - Add tracking pixel endpoint /api/invoices/[id]/open?t=... to register viewed (email open). Debounce to avoid noise.
  - Record events: sent, delivered (if provider supports), opened.
- Milestone 4: Payment status wiring (2 days)
  - Stripe webhook handler to map payment to invoice by metadata (invoiceId or number). Update status to paid and append InvoiceEvent.
  - UI updates for status timeline.
- Milestone 5: Hardening & tests (2-3 days)
  - TDD coverage: tax calc, template rendering variables, access control, event recording idempotency, webhook signature.
  - Load test PDF service; alerting and dashboards (Sentry for errors, Datadog/PostHog for metrics).

7) Integration points with existing code
- Authentication (NextAuth):
  - Enforce session on all invoice APIs; add role checks consistent with PRD RBAC extensions.
- Time tracking:
  - Convert TimeEntry -> InvoiceItem with references; prevent double-billing by setting invoiceItemId on time entries when invoiced.
- Stripe:
  - Reuse configured Stripe client; add metadata { invoiceId, invoiceNumber } on PaymentIntent/Checkout.
- UI design system:
  - Reuse shadcn/ui components per UX strategy; InvoiceBuilder, TemplateSelector, PreviewPanel; status badges and timeline components.
- Rate limiting:
  - Apply existing middleware to invoice routes as per PRD rateLimits example.
- Storage:
  - Use existing S3/R2 abstraction if present; otherwise introduce a minimal StorageService with put/getSignedUrl.

8) Technical debt considerations
- Serverless PDF rendering:
  - Puppeteer in serverless can be fragile. Mitigation: isolate rendering to a dedicated worker (Lambda with chromium layer or containerized worker). Track cold start latency and failures.
- Template system maturity:
  - Start with HTML+Handlebars-like tokens. Plan a versioned template engine with migration tools and per-user overrides later.
- Tax engine simplification:
  - Initial flat-rate per jurisdiction likely insufficient (compound taxes, exemptions). Encapsulate in TaxService and persist TaxLines to allow future replaced computations without data loss.
- Event model growth:
  - InvoiceEvent may evolve into a generic Activity/Event bus. Keep scope narrow but design schema to be extensible (type, payload JSONB, actor).
- Email deliverability:
  - Warm-up domains and monitor reputation. Consider provider fallback or round-robin in EmailService.
- Observability:
  - Add structured logging and correlation IDs early to ease production debugging.

Proposed Prisma schema additions (illustrative)
- Note: Align field names with existing code conventions before migration.

model Invoice {
  id           String       @id @default(cuid())
  number       String       @unique
  userId       String
  clientId     String
  status       InvoiceStatus @default(DRAFT)
  issueDate    DateTime     @default(now())
  dueDate      DateTime
  currency     String       @default("USD")
  subtotal     Decimal      @default(0)
  taxTotal     Decimal      @default(0)
  total        Decimal      @default(0)
  pdfUrl       String?
  pdfChecksum  String?
  templateId   String?
  revision     Int          @default(1)
  items        InvoiceItem[]
  taxLines     TaxLine[]
  events       InvoiceEvent[]
  createdAt    DateTime     @default(now())
  updatedAt    DateTime     @updatedAt
}

enum InvoiceStatus {
  DRAFT
  RENDERED
  SENT
  VIEWED
  PAID
  OVERDUE
  CANCELLED
}

model InvoiceItem {
  id          String   @id @default(cuid())
  invoiceId   String
  description String
  quantity    Decimal  @default(1)
  unitPrice   Decimal  @default(0)
  amount      Decimal  @default(0)
  timeEntryId String?
}

model InvoiceTemplate {
  id        String   @id @default(cuid())
  userId    String
  name      String
  version   Int      @default(1)
  engine    String   @default("html") // html, react-pdf
  markup    String   // HTML/Handlebars or JSX source
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model TaxRule {
  id            String   @id @default(cuid())
  jurisdiction  String   // e.g., US-CA, EU-DE
  rate          Decimal  // 0.00-1.00
  name          String   // VAT, GST, State Tax
  compound      Boolean  @default(false)
  active        Boolean  @default(true)
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt
}

model TaxLine {
  id         String   @id @default(cuid())
  invoiceId  String
  ruleId     String?
  name       String
  rate       Decimal  // snapshot at computation time
  amount     Decimal
}

model InvoiceEvent {
  id         String   @id @default(cuid())
  invoiceId  String
  type       String   // sent, opened, viewed, paid, rendered, failed, bounced
  actorId    String?
  ip         String?
  userAgent  String?
  payload    Json?
  createdAt  DateTime @default(now())
}

API outline (alignment with PRD)
- POST /api/invoices: create invoice draft from time entries
- GET /api/invoices/:id: fetch details incl. events
- POST /api/invoices/:id/render: queue render => updates pdfUrl
- POST /api/invoices/:id/send: queue email send, records SENT
- GET /api/invoices/:id/download?token=...: serve PDF, record VIEWED
- GET /api/invoices/:id/open-pixel?token=...: 1x1 gif, record OPENED
- POST /api/webhooks/stripe: update to PAID on successful intent/charge

Test strategy (TDD highlights)
- Unit tests:
  - TaxService: jurisdiction rules, rounding, multiple tax lines.
  - PdfRenderer: variable substitution, branding, currency formatting.
  - EmailService: payload construction, signed link generation, attachment toggle.
  - Permissions: ensure only owner/team can act on invoice/time entries.
- Integration tests:
  - Create -> Render -> Send -> Open -> Pay happy path.
  - Idempotent webhook handling and job retries.
- E2E (Playwright/Cypress):
  - Select time entries, preview, send, and verify client view.
  - Status timeline reflects events.

Rollout & migration
- Backfill: none required. Introduce schema via safe migrations.
- Feature flags: enable per cohort; start with link-only emails before enabling attachments.
- Observability: add SLOs for render latency and email delivery success; dashboards and alerts.

Open questions
- Do we enforce invoice numbering sequences per user (prefix + incremental)? PRD suggests FreelancerProfile.nextInvoiceNumber — implement atomic increment during creation.
- Which email provider to standardize on initially? Recommend Resend for developer velocity; keep adapter for SendGrid.
- Where to run rendering/queue workers in current infra (Vercel + AWS)? Suggest dedicated worker on AWS (Lambda or container) with Redis, or Vercel Queues if available.
