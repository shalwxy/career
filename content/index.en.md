# Career Description

Hi, I'm Seungha Lee — a backend engineer who enjoys nothing more than the time spent solving problems.

---

# Work Experience

## NEXON UNIVERSE — MapleStory Universe

<p class="meta">Backend Developer · Platform Development Team · Nov 2023 – Nov 2026 (3 years)</p>

MapleStory Universe (MSU) is a Web3 platform built on the MapleStory IP. I started on the on-chain/off-chain synchronization layer and went on to be the main contributor for transaction history, bookmarks, the marketplace BFF, account/payment, unified notifications, a policy service, a CDC data pipeline, and an operations AI bot.

<div class="stats">
<div><strong>33</strong><span>repositories</span></div>
<div><strong>3,700+</strong><span>commits</span></div>
<div><strong>4</strong><span>services · domains · bots<br/>design to operation</span></div>
<div><strong>3 yrs</strong><span>tenure</span></div>
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

> My core role: keeping data consistent in distributed systems — **preemption · idempotency · outbox · CDC**.

<p class="cta">
<a class="btn" href="portfolio.html">Portfolio (KR) — problem · approach · result →</a>
<a class="btn btn-ghost" href="decisions.html">Design Decisions (KR) →</a>
</p>

### What I did

#### <span class="phase">1</span> On-chain / off-chain synchronization (Data Engine)
<p class="period">Nov 2023 – Apr 2024</p>
<p class="chips"><span class="chip">Go</span><span class="chip">Saga</span><span class="chip">Redis distributed lock</span><span class="chip">Helm</span></p>
<div class="impact"><span class="impact-k">Impact</span> Fixed nickname duplication at character mint with <strong>Redis-lock preemption</strong> · turned per-item NFT validation lookups into <strong>one list query</strong> · 186 commits across 4 repos</div>

- Added input validation, a proto ↔ domain converter with unit tests, and gRPC error wrapping while wiring a new core service into the facade
- Added currency/character validators for the [Saga v2](#dg:saga) migration and reworked NFT item validation from per-item state lookups to a single list query
- Fixed nickname duplication at character mint: dropped the existence check, **preempted with a Redis lock**, released only on successful mint — a small fix, but a pattern I kept reusing
- Ran Helm rollouts for new services, reproduced a DocumentDB incident with throwaway deploys, and established dev-first deployment before test/qa promotion

#### <span class="phase">2</span> Transaction history · bookmarks · marketplace BFF
<p class="period">Jun 2024 – Sep 2025</p>
<p class="chips"><span class="chip">gRPC</span><span class="chip">Kafka</span><span class="chip">PostgreSQL advisory lock</span><span class="chip">Redis NX</span><span class="chip">CDC</span><span class="chip">Snowflake</span></p>
<div class="impact"><span class="impact-k">Impact</span> Restructured and extended transaction history (<strong>907 commits</strong>) and carried bookmarks from its early stage to production (<strong>550 commits</strong>, majority of the repo) · blocked duplicate writes under concurrent ingestion with Redis NX + advisory locks · narrowed intermittent BFF pod restarts to a cause and fixed them</div>

- **High-volume transaction ledger ([api-activity](#dg:activity))** — inherited the early codebase, restructured layers and split the query server from the Kafka consumer, then extended it to trades, mints, transfers, Swap & Warp, bridge-in and USDT. Promoted the transaction hash to a unique key, routed malformed events to a DLQ, and protected [concurrent ingestion](#dg:activity-lock) with Redis NX + PostgreSQL advisory locks
- **Query performance** — OR → UNION ALL rewrite with the DBA, cursor-based infinite scroll, conditional caching contributed to the shared library
- Emitted notification events on transaction finalization; moved Snowflake ingestion from Kafka publishes to **CDC**, removing the publish-failure loss path
- **Bookmark / view-count service ([api-bookmark](#dg:bookmark))** — joined right after the initial scaffold and owned the core features (majority of commits): idempotent writes, Redis counters moved to Kafka-driven aggregation, daily/total limits, account-deletion hook
- **Marketplace web BFF** — migrated bookmark/activity calls, built the inventory service, parallelized rendering. Traced intermittent pod restarts to gRPC calls inside async loops holding resources and fixed them with timeouts and chunked calls
- [Swap & Warp](#dg:swapwarp) (cross-chain) domain, domain-split proto repository, shared-library migration across platform and marketplace services
- Probability-disclosure service: requirements, versioning, data ingestion
- Back-office item/token sanctions (single, batch, bulk) and sanction history

#### <span class="phase">3</span> Account · payment · unified notifications
<p class="period">Jul 2025 – Aug 2026</p>
<p class="chips"><span class="chip">Worldpay</span><span class="chip">Redis Lua</span><span class="chip">SSE</span><span class="chip">gRPC streaming</span><span class="chip">MongoDB</span><span class="chip">Outbox</span></p>
<div class="impact"><span class="impact-k">Impact</span> Shipped credit-card verification and re-verification through <strong>two review rounds</strong> · enforced the daily limit atomically with <strong>Lua</strong> · bulk recipients moved to <strong>500-row streaming chunks</strong> · full-user KYC migration completed in production</div>

- **Worldpay (FraudSight 3DS) [card verification & re-verification](#dg:creditcard)** — mapped vendor 4xx to 200 + outcome codes and 5xx to errors, enforced the daily limit atomically with a Redis Lua script, encrypted payment-instrument data and added a circuit breaker, designed re-verification for OTP reset
- **[Stablecoin (USDT) launch](#dg:usdt)** — redesigned the off-chain pre-deduction/rollback service and collapsed the rollback topic into a single result-confirmation topic
- **[Unified notifications (SSE)](#dg:notification)** — absorbed JWT verification to drop the account-service dependency, capped concurrent subscriptions, generated URLs server-side, and split bulk recipients into a **gRPC streaming RPC** (500-row chunks, 50,000 cap)
- Replaced the gateway's gRPC dependency with HTTP to reduce coupling
- **KYC vendor migration (Argos → Sumsub)** — parallel calls, resumable cursor, rate limiter
- Discord auto-badge bot, role-sync batch and community-notice crawler — external side effects retried through an **outbox**
- Security-settings lock after e-mail change — moved from Redis TTL to a persisted column, primary reads to close the replication-lag window

#### <span class="phase">4</span> Policy service · data pipeline · ops automation
<p class="period">Jan 2026 – Nov 2026</p>
<p class="chips"><span class="chip">Debezium</span><span class="chip">Snowflake Stream/Task</span><span class="chip">Vertex AI</span><span class="chip">OpenSearch</span><span class="chip">Slack API</span></p>
<div class="impact"><span class="impact-k">Impact</span> Consolidated scattered control logic into <strong>one policy service</strong> used by four callers · replaced batch sync jobs with a <strong>CDC pipeline</strong> · automated first-pass error triage and shipped the first fix for a vendor model-deprecation outage <strong>within 3 days</strong> (re-swapped on recurrence)</div>

- **Policy service ([api-sentinel](#dg:sentinel))** — ACL (wallet/IP allow & deny lists), rate limiting (sliding + fixed window with jitter), lockout with flexible failure-count policies, runtime feature flags
- **[PostgreSQL CDC → Snowflake](#dg:cdc)** — Debezium connectors, Stream/Task, a replication-slot keepalive job, conditional tasks to cut cost
- **[Error-triage bot](#dg:errorbot)** — LLM first-pass analysis of Slack alerts with GitLab commit diffing, OpenSearch history and escalation; handled a vendor model deprecation with model swap, retry/backoff and a semaphore
- Operations console — Discord message re-send, permission-domain split, wallet ↔ SNS lookups

### Tech Stack

<div class="stack" markdown="1">

**Language** &nbsp;·&nbsp; Go · Java (Spring)

**Communication** &nbsp;·&nbsp; gRPC (unary / streaming, buf) · HTTP · Envoy · SSE

**Data** &nbsp;·&nbsp; PostgreSQL · MongoDB · AWS DocumentDB · Redis · Snowflake

**Messaging** &nbsp;·&nbsp; Kafka (Watermill · Debezium Connect · Spring Kafka)

**Infra / DevOps** &nbsp;·&nbsp; AWS EKS · Helm · ArgoCD · Rundeck · Jenkins · GitLab CI

**Observability** &nbsp;·&nbsp; Datadog · Jaeger · OpenSearch

**AI** &nbsp;·&nbsp; Vertex AI (LLM)

</div>

---

## UCLICK — AI Engineering R&D

<p class="meta">AI Engineering R&D · AI Service Team 1 · Jan 2021 – Oct 2023 (1 yr 10 mo)</p>

- **NVIDIA Omniverse R&D (Jun 2022 – Oct 2023)** — robot assembly and simulation in IsaacSim with ROS messaging (Python); VR device integration in CreateXR with an UnrealEngine4 single-player sample (C++)
- **GC-GPU solution incident diagnosis (Apr – May 2022)** — kernel-panic log analysis and root-cause fixes at the environment and source level
- **NVIDIA GPU MIG support (Mar – Apr 2022)** — on-site MIG enablement for a financial client's dev/prod servers; shell script that recreates MIG profiles after reboot
- **GPU monitoring with NVIDIA deepops (Jan – Feb 2022, sole owner)** — Prometheus/Grafana via Ansible; repackaged as scripts and images for air-gapped networks

## UCLICK — Backend Developer

<p class="meta">Backend Developer · R&D Lab 2 · Nov 2019 – Dec 2021 (2 years)</p>

- **UNO-GATEWAY (Sep 2020 – Dec 2021)** — dynamic OPEN API platform (validation, transformation, auth, rate limiting, routing); WebSocket + performance view, connectors for 7 databases and Elasticsearch/Hazelcast/Redis, Ribbon load-balancing tests, packaging
- **UNO-GATEWAY MDB project for a securities firm (Sep – Oct 2021, sole owner)** — JSON ↔ fixed-format message conversion over TCP
- **UNO-MSP (Feb 2020 – Dec 2021, lead developer)** — Oracle Cloud MSP platform across four releases: real-time resource collection, dashboards, billing integrity, OCI alarm/rule sync, Slack/mail alerts, monthly reports, HA agents, Zendesk integration, JDBC DB monitoring
- **LISTEN2ME-SURVEY (Sep – Oct 2020)** — spreadsheet-to-survey web app; API contract and statistics dashboard data

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
<tr><td>Linux Master Level 2</td><td>KAIT</td><td>Jul 2020</td></tr>
<tr><td>Network Administrator Level 2</td><td>ICQA</td><td>Jul 2020</td></tr>
</tbody>
</table>

## Korea National Open University — Computer Science

<p class="meta">Mar 2021 – Feb 2024 · A+ in every major course</p>

Enrolled to ground my engineering in computer science fundamentals: digital logic, computer architecture, operating systems, compilers, data structures, algorithms, databases, plus C/C++/Java, security, cloud computing and simulation.

## Korea Polytechnic — Data Convergence Software

<p class="meta">Mar 2019 – Nov 2019</p>

Hands-on Java/Spring, Python, R, Linux and database training, including TensorFlow regression, large-scale customer SQL analysis with Oracle, and JSP/Open-API web apps.

## Ewha Womans University — Mathematics Education

<p class="meta">Mar 2011 – Feb 2016</p>

Calculus, linear algebra, geometry, probability and statistics, analysis, topology, number theory and abstract algebra.

---

# Skills

## Backend Development

- **Go and refactoring** — comfortable with goroutine/channel concurrency; I keep splitting complex code into small, loosely coupled units behind interfaces.
- **Data design under concurrency** — PostgreSQL advisory locks, Redis distributed locks and Lua atomics, idempotent writes; I design the schema, the application layer and the database layer together so out-of-order messages never create duplicates.
- **Failure paths first** — pre-deduction/rollback, outbox retries, DLQs and CDC. When a large feature is rolled back, the defect fixes discovered along the way stay.
- **Flexible APIs** — policies come in as enums/config rather than code branches, so policy changes don't become commits.

## Architecture & Operations

- **New services and domains to production** — the policy service from its first commit, bookmarks and Swap & Warp joined early and carried to production with the majority of commits, and an error-triage bot added to an existing service. Splitting layers and server/consumer early is what lets features land without structural change later.
- **Pipelines outside the service** — batch → publish removal → CDC with Debezium and Snowflake Stream/Task, including slot keepalive and conditional tasks.
- **Infra & deployment** — Helm, ArgoCD, Rundeck, Jenkins, GitLab CI; dev-first promotion and reproducible incident deploys.

## Logging / Debugging

- **Meaningful logs and correlation keys** so a request can be traced end to end across Datadog, Jaeger and OpenSearch.
- **Hypothesis-driven debugging** — context and environment first, then narrow the scope; hidden causes like async-loop resource exhaustion get found and fixed at the root.
- **Closing incidents on recurrence conditions**, not on the first fix — retries, backoff, semaphores and table tests ship together.

## Communication

- **Clarifying requirements** and separating "current assumptions" from "needs verification" when working with DBAs, data engineering, security and product.
- **Visual, horizontal communication** — diagrams and written proposals; I change direction when a better one appears.
- **Proactive risk management** and turning review feedback into team principles ("no log-and-swallow on external calls", "inject config at boot").
