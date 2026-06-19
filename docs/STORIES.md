# STORIES.md
**Project:** `revenue-recovery`  
**Product Vision:** A revenue‑recovery platform that uses intelligent retry timing, personalized dunning emails, and real‑time webhook error detection to minimize failed payments and maximize MRR for SaaS companies.  

---  

## Epics & Backlog

| Epic | Description | Priority (MVP → Full) |
|------|-------------|-----------------------|
| **E1 – Intelligent Retry Engine** | Core service that determines optimal retry schedules per failed transaction based on risk signals, payment‑method constraints, and historical success rates. | 1 |
| **E2 – Personalized Dunning Automation** | Generate and send targeted dunning emails/SMS with dynamic content, A/B testing, and escalation paths. | 2 |
| **E3 – Real‑Time Webhook Error Detection** | Capture, classify, and surface webhook failures from payment providers; expose alerts & dashboards. | 1 |
| **E4 – Dashboard & Reporting** | UI for finance & ops teams to monitor recovery KPIs, drill‑down by customer, plan, and retry stage. | 3 |
| **E5 – Integration SDKs** | Language‑specific client libraries (Node, Python, Go) to embed the platform into existing SaaS billing stacks. | 4 |
| **E6 – Compliance & Data Governance** | Ensure GDPR/CCPA consent handling, audit logs, and secure storage of payment‑retry metadata. | 3 |
| **E7 – Admin & Role‑Based Access Control** | Granular permissions for finance, support, and engineering users. | 4 |
| **E8 – Extensibility Hooks** | Public webhook & plugin system for custom retry strategies or third‑party analytics. | 5 |

---  

## User Stories

### **Epic E1 – Intelligent Retry Engine**

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E1‑01** | **As a** Finance Ops analyst, **I want** the system to automatically schedule the next retry for a failed payment, **so that** we reduce manual intervention and increase successful recoveries. | 1. On receipt of a `payment_failed` event, the engine creates a retry schedule (1st, 2nd, 3rd attempts) based on configurable rules.<br>2. Schedule respects provider‑specific limits (e.g., max 3 retries, 24‑hour minimum gap).<br>3. The schedule is persisted and can be queried via API. |
| **E1‑02** | **As a** Platform Engineer, **I want** the retry algorithm to consider risk signals (card‑type, past success rate, country), **so that** high‑risk retries are delayed or omitted. | 1. Risk model receives inputs: card brand, BIN, historical success %, IP geolocation.<br>2. Engine outputs a “retry score” and adjusts the next‑retry timestamp accordingly.<br>3. Scores and decisions are logged for audit. |
| **E1‑03** | **As a** Billing System, **I want** a webhook (`/retry/schedule`) that returns the next retry timestamp for a given transaction ID, **so that** we can display the expected recovery date to the customer. | 1. Endpoint returns `{ transaction_id, next_retry_at, attempt_number }` in JSON.<br>2. Returns 404 if transaction not found or already settled.<br>3. Response time < 150 ms under load (10 k RPS). |
| **E1‑04** | **As a** Product Manager, **I want** A/B testing of different retry intervals, **so that** we can empirically discover the most effective schedule. | 1. UI toggle to assign a transaction to “control” or “variant” bucket.<br>2. Engine uses bucket‑specific interval config.<br>3. Metrics (recovery rate, time‑to‑recovery) are captured per bucket. |

### **Epic E2 – Personalized Dunning Automation**

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E2‑01** | **As a** Customer Success rep, **I want** the system to send a personalized dunning email after the first failed payment, **so that** the tone matches the customer’s plan tier. | 1. Email template selection based on `plan_tier` (Free, Pro, Enterprise).<br>2. Email includes dynamic fields: customer name, amount, last 4 digits, next retry date.<br>3. Sent within 5 minutes of failure event. |
| **E2‑02** | **As a** Marketing lead, **I want** to run A/B tests on subject lines and call‑to‑action buttons, **so that** we can improve open and conversion rates. | 1. UI to create variants with separate subject/CTA.<br>2. Random assignment of recipients to variants (even split).<br>3. Dashboard shows open‑rate, click‑through, and recovered‑payment % per variant. |
| **E2‑03** | **As a** Support agent, **I want** escalation emails (second, third attempts) to include a direct support link, **so that** customers can resolve issues quickly. | 1. Escalation templates add a “Contact Support” button linking to a pre‑filled ticket form.<br>2. Button appears only after the second failed retry.<br>3. Email delivery success ≥ 98 %. |
| **E2‑04** | **As a** System, **I want** to respect customer communication preferences (email vs SMS), **so that** we stay compliant with consent regulations. | 1. Preference stored per customer (`email_opt_in`, `sms_opt_in`).<br>2. Engine selects channel based on preference hierarchy.<br>3. If no opt‑in, no dunning message is sent and a compliance log entry is created. |

### **Epic E3 – Real‑Time Webhook Error Detection**

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E3‑01** | **As a** DevOps engineer, **I want** the platform to capture any webhook delivery failure from payment providers, **so that** we can alert the team instantly. | 1. All inbound webhook payloads are validated (signature, schema).<br>2. Failures (invalid signature, timeout, 5xx) are logged with error code.<br>3. Slack/PagerDuty alert triggered for > 5 failures in 1 min. |
| **E3‑02** | **As a** Finance Ops analyst, **I want** a dashboard view of webhook health (success rate, latency), **so that** we can spot provider‑level issues. | 1. Dashboard shows % success, avg latency, error breakdown per provider.<br>2. Data refreshed every 30 seconds.<br>3. Ability to filter by date range (last 24 h, 7 d). |
| **E3‑03** | **As a** Platform, **I want** to retry failed webhook deliveries with exponential back‑off up to 3 attempts, **so that** transient network issues don’t cause data loss. | 1. Retry schedule: 1 min, 5 min, 15 min.<br>2. After final failure, event is persisted to a dead‑letter queue and flagged for manual review.<br>3. Each attempt logged with timestamp and response status. |

### **Epic E4 – Dashboard & Reporting**

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E4‑01** | **As a** Finance VP, **I want** a high‑level KPI card showing “Recovered MRR %” and “Avg. Time to Recovery”, **so that** I can gauge the platform’s impact. | 1. KPI cards update in near‑real‑time (≤ 1 min lag).<br>2. Calculations use only settled payments within the selected window.<br>3. Exportable as CSV. |
| **E4‑02** | **As a** Analyst, **I want** to drill down by customer segment (plan, geography) and see retry success rates, **so that** we can target improvement efforts. | 1. Table with columns: segment, attempts, successes, recovery %.<br>2. Clickable rows open a detailed transaction list.<br>3. Filters for date range, provider, and retry stage. |
| **E4‑03** | **As a** Support manager, **I want** to receive a daily summary email of all unrecoverable payments, **so that** the team can follow up manually. | 1. Email generated at 08:00 UTC with a table of failed‑after‑max‑retries transactions.<br>2. Includes customer contact info and last retry attempt details.<br>3. Unsubscribe link respects user preferences. |

### **Epic E5 – Integration SDKs**

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E5‑01** | **As a** Backend Engineer (Node.js), **I want** an npm package that abstracts webhook verification and retry schedule queries, **so that** integration takes < 2 hours. | 1. Package `@axentx/revenue-recovery` published to npm.<br>2. Provides `verifyWebhook(payload, signature)` and `getNextRetry(txId)` functions.<br>3. Includes TypeScript typings and unit tests ≥ 80 % coverage. |
| **E5‑02** | **As a** Python developer, **I want** a pip‑installable client that can trigger manual retries, **so that** we can handle edge cases programmatically. | 1. Package `axentx-revenue-recovery` on PyPI.<br>2. Exposes `retry_transaction(tx_id, reason)` method.<br>3. Documentation with example scripts. |
| **E5‑03** | **As a** Go services team, **I want** a Go module that streams real‑time webhook events via gRPC, **so that** we can react instantly in our microservices. | 1. Module `github.com/axentx/revenue-recovery/go` implements `SubscribeEvents` RPC.<br>2. Supports TLS and token‑based auth.<br>3. Sample consumer app included. |

### **Epic E6 – Compliance & Data Governance**

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E6‑01** | **As a** Data Protection Officer, **I want** all personal data to be encrypted at rest and in transit, **so that** we meet GDPR requirements. | 1. AES‑256 encryption for stored retry metadata.<br>2. TLS 1.3 for all API endpoints.<br>3. Encryption keys rotated quarterly; rotation process logged. |
| **E6‑02** | **As a** Customer, **I want** the ability to request deletion of my payment‑retry data, **so that** I can exercise my right to be forgotten. | 1. API endpoint `DELETE /customers/{id}/recovery-data`.<br>2. Upon request, all related records are permanently erased within 24 h.<br>3. Confirmation email sent to the requester. |
| **E6‑03** | **As an** Auditor, **I want** immutable audit logs for every retry decision and dunning email sent, **so that** we can provide evidence of compliance. | 1. Logs written to append‑only storage (e.g., CloudWatch Logs with retention policy).<br>2. Each log entry includes timestamp, actor, action, and hash of payload.<br>3. Logs are tamper‑evident (signed). |

### **Epic E7 – Admin & Role‑Based Access Control**

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E7‑01** | **As a** System Admin, **I want** to create roles (Finance, Support, Engineer) with granular permissions, **so that** users only see data they need. | 1. RBAC UI to define permissions per API endpoint and UI component.<br>2. Permissions enforced at middleware layer.<br>3. Unauthorized access returns HTTP 403. |
| **E7‑02** | **As a** Support agent, **I want** read‑only access to customer payment status but not to modify retry schedules, **so that** we maintain data integrity. | 1. Role “Support” can GET `/transactions/*` but cannot POST/PUT/PATCH retry endpoints.<br>2. UI hides edit controls for restricted actions. |

### **Epic E8 – Extensibility Hooks**

| # | User Story | Acceptance Criteria |
|---|------------|----------------------|
| **E8‑01** | **As a** Partner SaaS, **I want** a webhook (`/plugins/custom-retry`) that receives each failed payment event, **so that** we can apply our own retry logic. | 1. Platform sends POST with full event payload to registered URL.<br>2. Partner can respond with `{ defer: true, next_attempt_at: ISO8601 }` to override default schedule.<br>3. Failure to respond within 2 s falls back to built‑in engine. |
| **E8‑02** | **As a** Data Scientist, **I want** a bulk export of anonymized retry outcomes, **so that** I can train custom ML models. | 1. Export job can be scheduled via UI or API.<br>2. Data includes: risk features, retry timestamps, outcome (recovered/failed).<br>3. Export delivered as encrypted CSV to S3 bucket. |

---  

## MVP Scope (First Release)

| Epic | Stories Included |
|------|-------------------|
| **E1** | E1‑01, E1‑02, E1‑03 |
| **E2** | E2‑01, E2‑02 |
| **E3** | E3‑01, E3‑03 |
| **E4** | E4‑01 |
| **E5** | E5‑01 |
| **E6** | E6‑01 |
| **E7** | E7‑01 |
| **E8** | – (deferred to post‑MVP) |

All MVP stories are **shippable**, have clear acceptance criteria, and are ordered to deliver a functional revenue‑recovery service that can be trialed with a pilot SaaS customer within 8 weeks.  

---  

*Prepared by the Senior Product/Engineering Lead – Axentx*
