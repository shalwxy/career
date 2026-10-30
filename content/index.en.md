# Career Description

Hi, I'm Seungha Lee — a backend engineer who enjoys nothing more than the time spent solving problems.

**Seven years in software and engineering** — Java backend (2 years) → AI/GPU infrastructure R&D (about 2 years) → **Go backend (3 years)**.

In my current role I work on payments, notifications, transaction history and data pipelines, mainly designing for **data consistency in distributed systems** (pre-emption, idempotency, recovery), and I also handle **CI/CD, Kubernetes manifests, the gateway and DB DDL** for my services. I design the failure path first and turn review feedback into written team principles. I'm applying for both backend and DevOps roles.

---

# Skills

::: skills
Languages | Go:3, Java (Spring):3, SQL:3, Python:2, Shell:2
Communication | gRPC:3, HTTP / REST:3, SSE:3, Kafka:3, Envoy:2, Debezium (CDC):2, Watermill:2
Data | PostgreSQL:3, Redis:3, MongoDB:2, DocumentDB:2, Snowflake:2
Infrastructure | Docker:3, Kubernetes (EKS):3, Helm:3, GitLab CI:3, ArgoCD:2, Rundeck:2, Ansible:2
Observability | Datadog:3, Jaeger:2, OpenSearch:2, Prometheus·Grafana:2
AI | Vertex AI (LLM):2, Omniverse·IsaacSim:1
:::

---

# Work Experience

## NEXON UNIVERSE — MapleStory Universe

<p class="meta">Backend Developer · Platform Development Team · Nov 2023 – Nov 2026 (3 years)</p>

NEXON UNIVERSE (founded 2022, a Nexon affiliate) builds MapleStory Universe (MSU), a Web3 platform that brings blockchain to the MapleStory IP. I developed its backend on the platform development team.

I started on the on-chain/off-chain synchronization layer and went on to work on transaction history, bookmarks, the marketplace BFF, account/payment, unified notifications, a policy service, a CDC data pipeline and an operations AI bot.

<div class="stats">
<div><strong>3 yrs</strong><span>at the company<br/>Nov 2023 – Nov 2026</span></div>
<div><strong>6</strong><span>main Go services<br/>built and operated</span></div>
<div><strong>4</strong><span>services · domains · bots<br/>built new · joined early</span></div>
<div><strong>5</strong><span>deployment environments<br/>dev · test · qa · stage · live</span></div>
</div>

<p class="badges">
<span class="b b-go">Go</span>
<span class="b">gRPC</span>
<span class="b">Kafka</span>
<span class="b">PostgreSQL</span>
<span class="b">Redis</span>
<span class="b">MongoDB</span>
<span class="b">Snowflake</span>
<span class="b">AWS EKS</span>
<span class="b">Helm</span>
<span class="b">Vertex AI</span>
</p>

> My core role: keeping data consistent in distributed systems — **preemption · idempotency · CDC**.

<p class="cta">
<a class="btn" href="portfolio.html">Portfolio (KR) — problem · approach · result →</a>
<a class="btn btn-ghost" href="decisions.html">Design Decisions (KR) →</a>
</p>

### What I did

#### <span class="phase">1</span> On-chain / off-chain synchronization (Data Engine)
<p class="period">Main work Nov 2023 – Apr 2024</p>
<p class="chips"><span class="chip">Go</span><span class="chip">Saga</span><span class="chip">Redis distributed lock</span></p>
<div class="impact"><span class="impact-k">Impact</span> Fixed nickname duplication at character mint with <strong>Redis-lock preemption</strong> · turned per-item NFT validation lookups into <strong>one list query</strong></div>

- Added input validation, request/response conversion with unit tests, and gRPC error handling while wiring a new core service into the game-facing gRPC service (business-provider)
- Added currency/character validators for the [Saga v2](#dg:saga) migration and reworked NFT item validation from per-item state lookups to a single list query
- Fixed nickname duplication at character mint: dropped the existence check, **preempted with a Redis lock**, released only on successful mint — a small fix, but a pattern I kept reusing

#### <span class="phase">2</span> Transaction history · bookmarks · marketplace BFF
<p class="period">Main work Jun 2024 – Sep 2025 · maintained afterwards</p>
<p class="chips"><span class="chip">gRPC</span><span class="chip">Kafka</span><span class="chip">PostgreSQL advisory lock</span><span class="chip">Redis NX</span><span class="chip">CDC</span><span class="chip">Snowflake</span></p>
<div class="impact"><span class="impact-k">Impact</span> Restructured and extended transaction history and built bookmarks, both <strong>through to production</strong> · <strong>per-event-type defence</strong> against concurrent duplicate writes (Redis NX · advisory locks) · narrowed intermittent BFF pod restarts to a cause and fixed them</div>

- **High-volume transaction ledger ([api-activity](#dg:activity))**
    - Reorganized layers, generalized the consumer and moved to message format v2, then extended it to trades, mints, transfers, Swap & Warp, bridge-in and USDT
    - Promoted the transaction hash to a unique key and routed malformed events to a DLQ
    - Protected [concurrent ingestion](#dg:activity-lock) with Redis NX + PostgreSQL advisory locks
- **Query performance** — OR → UNION ALL rewrite with the DBA, cursor-based infinite scroll, a conditional-caching option added to the shared cache decorator
- Emitted notification events when a transaction result is finalized; moved Snowflake ingestion from Kafka publishes to **CDC**, removing the publish-failure loss path
- **Bookmark / view-count service ([api-bookmark](#dg:bookmark))** — core features: idempotent writes, Redis counters moved to Kafka-driven aggregation, daily/total limits, account-deletion hook
- **Marketplace web BFF** — moved bookmark/activity calls to the new services, implemented bookmark and on-sale listings in the inventory service, parallelized rendering
- [Swap & Warp](#dg:swapwarp) cross-chain transfer history and queries (incl. bff-swapnwarp)

#### <span class="phase">3</span> Account · payment · unified notifications
<p class="period">Main work Jul 2025 – Aug 2026</p>
<p class="chips"><span class="chip">Worldpay</span><span class="chip">Redis Lua</span><span class="chip">SSE</span><span class="chip">gRPC streaming</span><span class="chip">MongoDB</span></p>
<div class="impact"><span class="impact-k">Impact</span> Completed credit-card verification and added the <strong>card path to account re-verification</strong> · daily attempt counter's <strong>increment + expiry made atomic with Lua</strong> · bulk recipients moved to <strong>500-row streaming chunks</strong> · full-user KYC migration completed in production</div>

- **Worldpay (FraudSight 3DS) [card verification & re-verification](#dg:creditcard)**
    - Mapped vendor 4xx to 200 + outcome codes and 5xx to errors
    - Made the daily attempt counter atomic with a Redis Lua script
    - Encrypted part of the card data and added blocking of abnormal attempts per payment-method combination
    - Added a re-verification path that confirms identity by card when OTP is reset
- **[Stablecoin (USDT) launch](#dg:usdt)** — extended the off-chain pre-deduction/rollback service for USDT (per-token limit tables, pre-deduction and row locking generalized per token), replaced the rollback topic with a dependency on transaction result topics, and added wallet-address validation to the blockchain supporter and BFF
- **[Unified notifications (SSE)](#dg:notification)** — absorbed JWT verification to drop the account-service dependency, generated URLs server-side, and split bulk recipients into a **gRPC streaming RPC** (500-row chunks, 50,000 cap)
- **Full-user data migration batch for the KYC vendor change (Argos → Sumsub)** — range-partitioned parallel runs, resumable cursor, call-quota management; completed in production
- Discord auto-badge and role-sync batch — cut run time from about 2 hours to 20 minutes

#### <span class="phase">4</span> Policy service · data pipeline · ops automation
<p class="period">Main work Jan 2026 – Nov 2026</p>
<p class="chips"><span class="chip">Debezium</span><span class="chip">Snowflake Stream/Task</span><span class="chip">Vertex AI</span><span class="chip">OpenSearch</span></p>
<div class="impact"><span class="impact-k">Impact</span> Consolidated scattered control logic into <strong>one policy service</strong> used by four callers · replaced batch sync jobs with a <strong>CDC pipeline</strong> · <strong>automated first-pass error triage</strong></div>

- **Policy service ([api-sentinel](#dg:sentinel))** — ACL (wallet/IP allow & deny lists), rate limiting (sliding + fixed window with jitter), lockout after repeated OTP failures (keep/reset failure counts by configurable policy), runtime feature flags
- **[PostgreSQL CDC → Snowflake](#dg:cdc)** — Debezium connectors, Stream/Task, a replication-slot keepalive job, conditional tasks to cut cost
- **[Error-triage bot](#dg:errorbot)** — replies in-thread to Slack error alerts with an LLM first-pass analysis (GitLab commit diffing, OpenSearch history, escalation). Guardrails — daily/monthly cost caps, PII masking, dedupe, a circuit breaker — run as independent components outside the service logic, and prompt rules are promoted from failure modes seen in real use

#### <span class="phase">5</span> Infrastructure · CI/CD · gateway
<p class="period">Throughout</p>
<p class="chips"><span class="chip">GitLab CI</span><span class="chip">Docker</span><span class="chip">Helm · EKS</span><span class="chip">Rundeck</span><span class="chip">Envoy</span></p>
<div class="impact"><span class="impact-k">Impact</span> New services shipped with their <strong>full deployment set</strong> · five deployment environments operated (dev · test · qa · stage · live) · gateway routes and auth tidied</div>

- **[CI/CD & infrastructure](#dg:cicd)** — operated GitLab CI, Dockerfiles, Helm/K8s manifests and DDL for the services I owned; new services shipped with their full deployment set
- **Envoy gateway** — added and tidied gRPC → REST routes and auth settings whenever services were added; moved routing/port settings of my services (notifications, blockchain supporter) as part of the team-wide gateway gRPC → HTTP switch
- Reviewed all externally exposed APIs (Swap & Warp, notifications, BFF) and added authentication (team of three)
- Led the split of the company-wide proto repository into domain modules

#### <span class="phase">6</span> Back office · operations tools · other
<p class="period">Mar 2025 – Oct 2026</p>

- Back-office item/token sanctions (single, batch, bulk) and a sanction-history view
- Operations console — Discord message re-send, permission-domain split, wallet ↔ SNS lookups

### Tech Stack

<div class="stack" markdown="1">

**Language** &nbsp;·&nbsp; Go · Java (Spring)

**Communication** &nbsp;·&nbsp; gRPC (unary / streaming, buf) · HTTP · Envoy · SSE

**Data** &nbsp;·&nbsp; PostgreSQL · MongoDB · AWS DocumentDB · Redis · Snowflake

**Messaging** &nbsp;·&nbsp; Kafka (Watermill · Debezium Connect · Spring Kafka)

**Infra / DevOps** &nbsp;·&nbsp; AWS EKS · Kubernetes · Docker · Helm · ArgoCD · Rundeck · Jenkins · GitLab CI · Envoy

**Observability** &nbsp;·&nbsp; Datadog · Jaeger · OpenSearch

**AI** &nbsp;·&nbsp; Vertex AI (LLM)

</div>

---

## UCLICK — AI Engineering R&D

<p class="meta">AI Engineering R&D · AI Service Team 1 · Jan 2022 – Oct 2023 (1 yr 10 mo)</p>

- **NVIDIA Omniverse R&D (Jun 2022 – Oct 2023)** — robot assembly and simulation in IsaacSim with ROS messaging (Python); VR device integration in CreateXR with an UnrealEngine4 single-player sample (C++)
- **GC-GPU solution incident diagnosis (Apr – May 2022)** — kernel-panic log analysis and root-cause fixes at the environment and source level
- **NVIDIA GPU MIG support (Mar – Apr 2022)** — on-site MIG enablement for a Korean financial client's dev/prod servers; shell script that recreates MIG profiles after reboot
- **GPU monitoring with NVIDIA deepops (Jan – Feb 2022, sole owner)** — Prometheus/Grafana via Ansible; repackaged as scripts and images for air-gapped networks

## UCLICK — Backend Developer

<p class="meta">Backend Developer · R&D Lab 2 · Nov 2019 – Dec 2021 (2 years)</p>

- **UNO-GATEWAY (Sep 2020 – Dec 2021)** — dynamic OPEN API platform (validation, transformation, auth, rate limiting, routing); WebSocket + performance view, connectors for 7 databases and Elasticsearch/Hazelcast/Redis, Ribbon load-balancing tests, packaging
- **UNO-GATEWAY MDB project for a Korean securities client (Sep – Oct 2021, sole owner)** — JSON ↔ fixed-format message conversion over TCP
- **UNO-MSP (Feb 2020 – Dec 2021, lead developer)** — Oracle Cloud MSP platform across four releases: real-time resource collection, dashboards, billing integrity, OCI alarm/rule sync, Slack/mail alerts, monthly reports, HA agents, Zendesk integration, JDBC DB monitoring
- **LISTEN2ME-SURVEY (Sep – Oct 2020)** — spreadsheet-to-survey web app; API contract and statistics dashboard data

---

# How I Work

## Design

- **Failure paths first.** Pre-deduction/rollback, DLQ and retries, CDC — I decide how to recover before I implement. Defect fixes are merged separately from the feature, so they survive if the feature is rolled back.
- **Locks and idempotency chosen per event type.** Requests and results that arrive out of order get look-up-then-create/update under an advisory lock; single-message events get Redis NX; unique keys are the last line of defence underneath.
- **Policy as configuration, not code branches.** A policy change should change a setting, not a commit — and settings are injected at boot, never read on the request path.
- **Services don't write outward themselves.** Analytics and downstream loads flow through CDC, which removes "the app failed to publish" as a loss path altogether.

## Operations

- **Deploys, manifests and DDL for my services are my job.** GitLab CI → Helm/Kubernetes → Rundeck, a different deploy path per environment, and DDL that goes through DBA review — one person sees it through. New services get wired into the [pipeline](#dg:cicd) by me.
- **A single request must be traceable end to end.** I design the correlation keys first, then verify after each deploy that Datadog, Jaeger and OpenSearch actually follow the request.

## Collaboration

- **Separate "current assumptions" from "needs verification"** when working with DBA, data engineering, security, product, front-end and blockchain teams.
- **Write down design intent and the reasons behind decisions.** Diagrams first, open to a better direction; the [Design Decisions](decisions.html) page on this site is that record.
- **Review feedback becomes team principle.** Rules like "no log-and-swallow on external calls" are documented and carried into the next piece of work.

---

# Other Experiences

## Certifications

<table class="certs">
<thead><tr><th>Certification</th><th>Issuer</th><th>Date</th></tr></thead>
<tbody>
<tr><td><strong>Engineer Information Processing</strong></td><td>Ministry of Science and ICT</td><td>Aug 2019</td></tr>
<tr><td><strong>SQL Developer (SQLD)</strong></td><td>Korea Data Agency</td><td>Sep 2019</td></tr>
<tr><td><strong>Information Security Engineer</strong></td><td>Ministry of Science and ICT</td><td>May 2023</td></tr>
<tr><td><strong>Linux Master Level 1</strong></td><td>KAIT</td><td>May 2021</td></tr>
<tr><td><strong>Network Administrator Level 1</strong></td><td>ICQA</td><td>May 2023</td></tr>
</tbody>
</table>

## Korea National Open University — Computer Science

<p class="meta">Mar 2021 – Feb 2024</p>

Enrolled to ground my engineering in computer science fundamentals and took major courses only — operating systems, compilers, data structures, algorithms, databases, C/C++/Java, security and cloud computing — with A+ in each of these courses.

## Korea Polytechnic — Data Convergence Software

<p class="meta">Mar 2019 – Nov 2019</p>

Hands-on Java/Spring, Python, R, Linux and database training, including TensorFlow regression, large-scale customer SQL analysis with Oracle, and JSP/Open-API web apps.

## Ewha Womans University — Mathematics Education

<p class="meta">Mar 2011 – Feb 2016</p>

Mathematics major (calculus, linear algebra, geometry, probability and statistics, analysis, topology, number theory, abstract algebra) — trained to solve problems through definitions and proofs.
