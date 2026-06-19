# TECH_SPEC.md  

**Project:** revenue-recovery  
**Owner:** Axentx – Product/Engineering Lead  
**Status:** Draft – ready for review & implementation  

---  

## Table of Contents
1. [Overview](#1-overview)  
2. [Architecture Diagram](#2-architecture-diagram)  
3. [Core Components](#3-core-components)  
4. [Data Model](#4-data-model)  
5. [Key APIs & Interfaces](#5-key-apis--interfaces)  
6. [Technology Stack](#6-technology-stack)  
7. [External Dependencies](#7-external-dependencies)  
8. [Deployment & Operations](#8-deployment--operations)  
9. [Security & Compliance](#9-security--compliance)  
10. [Scalability & Performance](#10-scalability--performance)  
11. [Observability](#11-observability)  
12. [Glossary](#12-glossary)  

---  

## 1. Overview
**Revenue‑Recovery** is a SaaS‑focused platform that reduces churn caused by failed payments. It combines three intelligence layers:

1. **Intelligent Retry Timing** – ML‑driven schedule for payment retries based on historical success patterns, card network rules, and customer behavior.  
2. **Personalized Dunning Emails** – Dynamic, context‑aware email templates rendered per‑customer, with A/B testing and optimal send‑time selection.  
3. **Real‑Time Webhook Error Detection** – Event‑driven monitoring of payment‑gateway webhooks; immediate classification of transient vs permanent failures and trigger of the appropriate recovery flow.

The system is built as a set of loosely‑coupled micro‑services that communicate via **Kafka** (event bus) and expose **REST/GraphQL** APIs for integration with SaaS billing back‑ends (Stripe, Braintree, Paddle, etc.). All services are containerised and orchestrated by **Kubernetes** (GKE/EKS).  

---  

## 2. Architecture Diagram
```
+-------------------+        +-------------------+        +-------------------+
|   SaaS Billing    |  ---> |  Ingestion Service|  --->  |   Event Bus (Kafka) |
|   (Stripe, …)    |        |  (Webhook Receiver)      |                     |
+-------------------+        +-------------------+        +-------------------+
                                                               |
                 +-------------------+   +-------------------+   +-------------------+
                 | Retry Scheduler   |   | Dunning Engine    |   | Analytics Service |
                 | Service           |   | Service           |   | (Reporting)       |
                 +-------------------+   +-------------------+   +-------------------+
                         |                       |                       |
                +-------------------+   +-------------------+   +-------------------+
                |  Payment Gateway  |   |  Email Provider   |   |  Data Warehouse   |
                |  (Stripe, Braintree) | | (SendGrid, SES)  |   | (BigQuery/Redshift)|
                +-------------------+   +-------------------+   +-------------------+
```

*All services are stateless; state is persisted in PostgreSQL and Redis.*  

---  

## 3. Core Components  

| Service | Responsibility | Key Libraries |
|---------|----------------|----------------|
| **Ingestion Service** | Accepts payment‑gateway webhooks, validates signatures, normalises events, publishes to Kafka. | FastAPI, pydantic, kafka‑python |
| **Retry Scheduler** | Calculates next retry timestamp using a lightweight ML model (gradient‑boosted trees) and enqueues retry jobs. | vLLM (inference), scikit‑learn, Redis Queue (RQ) |
| **Dunning Engine** | Generates personalized email content, selects optimal send time, tracks delivery & engagement. | Jinja2, SGLang (structured generation), Celery, SendGrid SDK |
| **Analytics Service** | Aggregates events, produces dashboards, feeds data back to model training pipeline. | dbt, SQLAlchemy, Apache Superset |
| **Admin API** | CRUD for customers, payment methods, dunning templates, model configuration. | GraphQL (Ariadne), OAuth2, FastAPI |
| **Model Training Pipeline** (offline) | Periodic retraining of retry‑timing model using collected pairs (≈144M pairs/7d). | PyTorch, vLLM, Airflow, PGVector for embeddings |
| **Observability Agent** | Metrics, logs, traces export to Prometheus/Grafana & Loki. | OpenTelemetry, Prometheus client |

---  

## 4. Data Model  

### 4.1 Relational Schema (PostgreSQL)

| Table | Primary Key | Important Columns |
|-------|-------------|-------------------|
| `customers` | `customer_id` (UUID) | `email`, `name`, `created_at`, `status` |
| `payment_methods` | `pm_id` (UUID) | `customer_id`, `gateway`, `last4`, `exp_month`, `exp_year`, `status` |
| `payment_events` | `event_id` (UUID) | `customer_id`, `pm_id`, `gateway`, `event_type`, `amount_cents`, `currency`, `timestamp`, `raw_payload` |
| `retry_jobs` | `job_id` (UUID) | `customer_id`, `pm_id`, `scheduled_at`, `attempt_number`, `status` |
| `dunning_emails` | `email_id` (UUID) | `customer_id`, `template_id`, `sent_at`, `opened_at`, `clicked_at`, `delivery_status` |
| `templates` | `template_id` (UUID) | `name`, `subject`, `body_jinja`, `created_at`, `active` |
| `model_versions` | `model_id` (UUID) | `version`, `trained_at`, `metrics_json` |

### 4.2 Event Schema (Kafka Topics)

| Topic | Message Type | Schema (JSON) |
|-------|--------------|---------------|
| `payment.webhook.raw` | Raw webhook payload | `{gateway, event_type, payload, received_at}` |
| `payment.processed` | Normalised event | `{event_id, customer_id, pm_id, status, amount_cents, timestamp}` |
| `retry.schedule` | Retry job request | `{customer_id, pm_id, next_attempt_at, model_version}` |
| `dunning.send` | Email send request | `{customer_id, template_id, send_at, personalization}` |
| `analytics.ingest` | Unified event for reporting | `{event_type, customer_id, timestamp, metadata}` |

---  

## 5. Key APIs & Interfaces  

### 5.1 Public REST API (Admin / Integration)

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/v1/customers` | `POST` | OAuth2 (client‑credentials) | Register a new customer |
| `/api/v1/customers/{id}` | `GET` | OAuth2 | Retrieve customer profile |
| `/api/v1/payment-methods` | `POST` | OAuth2 | Add/Update payment method |
| `/api/v1/webhooks/stripe` | `POST` | Signature verification | Stripe webhook endpoint |
| `/api/v1/webhooks/braintree` | `POST` | Signature verification | Braintree webhook endpoint |
| `/api/v1/dunning/templates` | `GET/POST/PUT` | OAuth2 | Manage email templates |
| `/api/v1/metrics` | `GET` | OAuth2 | Export health & usage metrics (JSON) |

### 5.2 GraphQL API (Analytics)

```graphql
type Query {
  revenueRecoveryStats(dateFrom: Date!, dateTo: Date!): RecoveryStats
  customerRecovery(customerId: ID!): CustomerRecovery
}
type RecoveryStats {
  totalFailedPayments: Int
  totalRecovered: Int
  mrrRecoveredCents: Int
  avgRetryDelayHours: Float
}
type CustomerRecovery {
  customerId: ID!
  attempts: [RetryAttempt!]!
  dunningEmails: [DunningEmail!]!
}
```

### 5.3 Internal Event Bus (Kafka)

* Producers:* Ingestion Service, Retry Scheduler, Dunning Engine, Analytics Service.  
* Consumers:* Retry Scheduler, Dunning Engine, Analytics Service, Model Trainer.  

---  

## 6. Technology Stack  

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **API Framework** | FastAPI (Python 3.11) | High performance, async, OpenAPI auto‑gen |
| **ML Inference** | vLLM (GPU‑accelerated) | Scalable inference for the retry‑timing model |
| **Structured Generation** | SGLang | Enables token‑level control for email personalization |
| **Message Bus** | Apache Kafka (Confluent Cloud) | Durable, ordered event streaming |
| **Task Queue** | Redis Queue (RQ) + Celery (fallback) | Simple, reliable retry semantics |
| **Database** | PostgreSQL 15 + PGVector extension | Relational integrity + vector similarity for template retrieval |
| **Cache** | Redis 7 (cluster) | Session data, rate‑limit counters |
| **Container Runtime** | Docker (Slim‑Python) | Small footprint, reproducible builds |
| **Orchestration** | Kubernetes (GKE/EKS) | Autoscaling, rolling updates |
| **CI/CD** | GitHub Actions + ArgoCD | Automated testing, canary deployments |
| **Observability** | Prometheus + Grafana, Loki, OpenTelemetry | Full‑stack metrics & logs |
| **Infrastructure as Code** | Terraform (Google Cloud / AWS) | Reproducible environments |
| **Testing** | PyTest, Locust (load), Pact (contract) | Unit, integration, performance, contract testing |

---  

## 7. External Dependencies  

| Dependency | Version | License |
|------------|---------|---------|
| Stripe SDK | 5.4.0 | MIT |
| Braintree SDK | 4.12.0 | MIT |
| SendGrid SDK | 6.10.0 | MIT |
| vLLM | latest (git) | Apache‑2.0 |
| SGLang | latest (git) | Apache‑2.0 |
| PostgreSQL | 15 | PostgreSQL |
| Redis | 7 | BSD‑3 |
| Kafka | 3.5 | Apache‑2.0 |
| Terraform | 1.6 | MPL‑2.0 |

All third‑party libraries are vetted for security (dependabot, Snyk) and are compatible with Axentx’s open‑source policy.

---  

## 8. Deployment & Operations  

### 8.1 Container Images  
- Base: `python:3.11-slim`  
- Build pipeline: multi‑stage Dockerfile, static analysis (bandit, mypy), and SBOM generation (Syft).  

### 8.2 Kubernetes Manifests (Helm Chart)  
- **Namespace:** `revenue-recovery`  
- **Deployments:** `ingestion`, `retry-scheduler`, `dunning-engine`, `admin-api`, `analytics`.  
- **StatefulSets:** `postgres`, `redis`, `kafka`.  
- **ConfigMaps & Secrets:** API keys, webhook secrets, DB credentials (encrypted via KMS).  

### 8.3 Autoscaling  
- **Horizontal Pod Autoscaler (HPA)** based on CPU (target 60%) and custom metric `kafka_consumer_lag`.  
- **Cluster Autoscaler** enabled for node‑pool scaling.  

### 8.4 CI/CD Flow  
1. **PR validation:** unit tests, lint, type check, security scan.  
2. **Staging deploy:** Helm upgrade with `--dry-run`, integration tests via test harness.  
3. **Canary release:** 5 % traffic to new version, monitor `error_rate` & `latency`.  
4. **Full promotion** on success, automatic rollback on threshold breach.  

---  

## 9. Security & Compliance  

| Area | Controls |
|------|----------|
| **Authentication** | OAuth2 client‑credentials for API; JWT signed with RS256. |
| **Authorization** | RBAC at API gateway (Kong/Envoy). |
| **Data Protection** | At‑rest encryption (PostgreSQL Transparent Data Encryption, Redis TLS). In‑flight TLS 1.3 everywhere. |
| **PCI‑DSS** | No card data stored; only tokenised identifiers from gateways. |
| **Secret Management** | Google Secret Manager / AWS Secrets Manager, accessed via IAM roles. |
| **Audit Logging** | Immutable audit trail in Cloud Audit Logs; retained 2 years. |
| **Vulnerability Management** | Weekly dependabot PRs, quarterly Snyk scans, CVE alerts. |
| **GDPR/CCPA** | Ability to delete all personal data per `customer_id` via API; data‑subject request workflow. |

---  

## 10. Scalability & Performance  

- **Throughput Goal:** 10 k webhook events/sec (peak) → Kafka partitioning (≥50 partitions) and consumer groups sized accordingly.  
- **Latency SLA:** End‑to‑end retry decision ≤ 200 ms; email send request ≤ 100 ms.  
- **Model Inference:** vLLM serving with GPU autoscaling; batch size 32, inference latency ~30 ms per request.  
- **Cache Warm‑up:** Recent customer profiles cached in Redis (TTL 15 min).  

Load testing (Locust) will be performed on a staging cluster with 5× production traffic to validate scaling rules.

---  

## 11. Observability  

| Metric | Source | Export |
|--------|--------|--------|
| `webhook_ingest_rate` | Ingestion Service | Prometheus |
| `retry_job_queue_depth` | Redis Queue | Prometheus |
| `email_delivery_success` | Dunning Engine | Prometheus |
| `model_inference_latency` | vLLM server | Prometheus |
| `error_rate` (5xx) | API Gateway | Prometheus |
| `kafka_consumer_lag` | Kafka Exporter | Prometheus |
| **Logs** | All services | Loki (structured JSON) |
| **Traces** | End‑to‑end request flow | Jaeger (OpenTelemetry) |
| **Dashboards** | Grafana (pre‑built panels for MRR recovery, churn reduction) | — |

Alerting thresholds are defined in Alertmanager (e.g., `retry_job_queue_depth > 10k` for >5 min).

---  

## 12. Glossary  

- **MRR** – Monthly Recurring Revenue.  
- **Dunning** – Communication to collect overdue payments.  
- **Webhook** – HTTP callback from payment gateway notifying of events.  
- **Retry Scheduler** – Service that decides when to attempt another charge.  
- **vLLM** – High‑throughput inference engine for large language models.  
- **SGLang** – Structured generation language for token‑level control.  

---  

*Prepared by:* Senior Product/Engineering Lead – Axentx  
*Date:* 2026‑06‑19  

---
