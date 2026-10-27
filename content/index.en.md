# Career Description

Hi, I'm Seungha Lee — a backend engineer who enjoys nothing more than the time spent solving problems.

**Three years of Go backend work** on payments, notifications, transaction history and data pipelines, mainly designing for **data consistency in distributed systems** (pre-emption, idempotency, recovery). I also work across the boundary of my services — **CI/CD, Kubernetes manifests, the gateway and DB DDL** — and I'm applying for both backend and DevOps roles.

---

# Work Experience

## NEXON UNIVERSE — MapleStory Universe

<p class="meta">Backend Developer · Platform Development Team · Nov 2023 – Nov 2026 (3 years)</p>

NEXON UNIVERSE (founded 2022, a Nexon affiliate) builds MapleStory Universe (MSU), a Web3 platform that brings blockchain to the MapleStory IP. I developed its backend on the platform development team. I started on the on-chain/off-chain synchronization layer and went on to work on transaction history, bookmarks, the marketplace BFF, account/payment, unified notifications, a policy service, a CDC data pipeline and an operations AI bot.

<div class="stats">
<div><strong>33</strong><span>repositories</span></div>
<div><strong>3,700+</strong><span>commits</span></div>
<div><strong>4</strong><span>services · domains · bots<br/>built new · joined early</span></div>
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

- Added input validation, request/response conversion with unit tests, and gRPC error handling while wiring a new core service into the game-facing gRPC service (business-provider)
- Added currency/character validators for the [Saga v2](#dg:saga) migration and reworked NFT item validation from per-item state lookups to a single list query
- Fixed nickname duplication at character mint: dropped the existence check, **preempted with a Redis lock**, released only on successful mint — a small fix, but a pattern I kept reusing
- Ran Helm rollouts for new services, reproduced an incident with throwaway deploys and rollbacks, and deployed to dev first before test/qa promotion

#### <span class="phase">2</span> Transaction history · bookmarks · marketplace BFF
<p class="period">Jun 2024 – Sep 2025</p>
<p class="chips"><span class="chip">gRPC</span><span class="chip">Kafka</span><span class="chip">PostgreSQL advisory lock</span><span class="chip">Redis NX</span><span class="chip">CDC</span><span class="chip">Snowflake</span></p>
<div class="impact"><span class="impact-k">Impact</span> Restructured and extended transaction history (<strong>907 commits</strong>) and carried bookmarks to production (<strong>550 commits</strong>, majority of the repo) · blocked duplicate writes under concurrent ingestion with Redis NX + advisory locks · narrowed intermittent BFF pod restarts to a cause and fixed them</div>

- **High-volume transaction ledger ([api-activity](#dg:activity))** — reorganized layers, generalized the consumer and moved to message format v2, then extended it to trades, mints, transfers, Swap & Warp, bridge-in and USDT. Promoted the transaction hash to a unique key, routed malformed events to a DLQ, and protected [concurrent ingestion](#dg:activity-lock) with Redis NX + PostgreSQL advisory locks
- **Query performance** — OR → UNION ALL rewrite with the DBA, cursor-based infinite scroll, a conditional-caching option added to the shared cache decorator
- Emitted notification events when a transaction result is finalized; moved Snowflake ingestion from Kafka publishes to **CDC**, removing the publish-failure loss path
- **Bookmark / view-count service ([api-bookmark](#dg:bookmark))** — core features (majority of commits): idempotent writes, Redis counters moved to Kafka-driven aggregation, daily/total limits, account-deletion hook
- **Marketplace web BFF** — moved bookmark/activity calls to the new services, implemented bookmark and on-sale listings in the inventory service, parallelized rendering. Traced intermittent pod restarts to gRPC calls inside async loops holding resources and fixed them with timeouts and chunked calls
- [Swap & Warp](#dg:swapwarp) cross-chain transfer history and queries (incl. bff-swapnwarp); domain-split proto repository
- Item-probability disclosure service: data storage and versioning
- Back-office item/token sanctions (single, batch, bulk) and a sanction-history view

#### <span class="phase">3</span> Account · payment · unified notifications
<p class="period">Jul 2025 – Aug 2026</p>
<p class="chips"><span class="chip">Worldpay</span><span class="chip">Redis Lua</span><span class="chip">SSE</span><span class="chip">gRPC streaming</span><span class="chip">MongoDB</span><span class="chip">Outbox</span></p>
<div class="impact"><span class="impact-k">Impact</span> Completed credit-card verification and added the <strong>card path to account re-verification</strong> · daily attempt counter's <strong>increment + expiry made atomic with Lua</strong> · bulk recipients moved to <strong>500-row streaming chunks</strong> · full-user KYC migration completed in production</div>

- **Worldpay (FraudSight 3DS) [card verification & re-verification](#dg:creditcard)** — mapped vendor 4xx to 200 + outcome codes and 5xx to errors, made the daily attempt counter atomic with a Redis Lua script, encrypted part of the card data, added blocking of abnormal attempts per payment-method combination, and a re-verification path that confirms identity by card when OTP is reset
- **[Stablecoin (USDT) launch](#dg:usdt)** — extended the off-chain pre-deduction/rollback service for USDT (per-token limit tables, pre-deduction and row locking generalized per token) and replaced the rollback topic with a dependency on transaction result topics
- **[Unified notifications (SSE)](#dg:notification)** — absorbed JWT verification to drop the account-service dependency, generated URLs server-side, and split bulk recipients into a **gRPC streaming RPC** (500-row chunks, 50,000 cap)
- Moved routing/port settings of my services (notifications, blockchain supporter) as part of the team-wide gateway gRPC → HTTP switch
- **Full-user data migration batch for the KYC vendor change (Argos → Sumsub)** — range-partitioned parallel runs, resumable cursor, call-quota management; completed in production
- Discord auto-badge and role-sync batch; extended the community-notice crawler with new boards and resumable failures — role-grant failures retried through an **outbox** (in review)
- 24-hour lock on security-option changes after an e-mail change — moved from Redis TTL to a persisted column, with primary reads to close the replication-lag window

#### <span class="phase">4</span> Policy service · data pipeline · ops automation
<p class="period">Jan 2026 – Nov 2026</p>
<p class="chips"><span class="chip">Debezium</span><span class="chip">Snowflake Stream/Task</span><span class="chip">Vertex AI</span><span class="chip">OpenSearch</span><span class="chip">GitLab CI</span><span class="chip">Helm · EKS</span></p>
<div class="impact"><span class="impact-k">Impact</span> Consolidated scattered control logic into <strong>one policy service</strong> used by four callers · replaced batch sync jobs with a <strong>CDC pipeline</strong> · automated first-pass error triage and shipped the first fix for a vendor model-deprecation outage <strong>within 3 days</strong> (re-swapped on recurrence)</div>

- **Policy service ([api-sentinel](#dg:sentinel))** — ACL (wallet/IP allow & deny lists), rate limiting (sliding + fixed window with jitter), lockout after repeated OTP failures (keep/reset failure counts by configurable policy), runtime feature flags
- **[PostgreSQL CDC → Snowflake](#dg:cdc)** — Debezium connectors, Stream/Task, a replication-slot keepalive job, conditional tasks to cut cost
- **[Error-triage bot](#dg:errorbot)** — replies in-thread to Slack error alerts with an LLM first-pass analysis with GitLab commit diffing, OpenSearch history and escalation; handled a vendor model deprecation with model swap, retry/backoff and a semaphore
- Operations console — Discord message re-send, permission-domain split, wallet ↔ SNS lookups
- Reviewed all externally exposed APIs (Swap & Warp, notifications, BFF) and added authentication (team of three); added wallet-address validation
- **[CI/CD & infrastructure](#dg:cicd)** (throughout) — used the team's existing pipeline and manifest patterns to maintain GitLab CI, Dockerfiles, Helm/K8s manifests, Envoy routes and DDL for the services I owned; new services shipped with their full deployment set by copying those patterns

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

<p class="meta">Mar 2021 – Feb 2024</p>

Enrolled to ground my engineering in computer science fundamentals: digital logic, computer architecture, operating systems, compilers, data structures, algorithms, databases, plus C/C++/Java, security, cloud computing and simulation — A+ in each of these courses.

## Korea Polytechnic — Data Convergence Software

<p class="meta">Mar 2019 – Nov 2019</p>

Hands-on Java/Spring, Python, R, Linux and database training, including TensorFlow regression, large-scale customer SQL analysis with Oracle, and JSP/Open-API web apps.

## Ewha Womans University — Mathematics Education

<p class="meta">Mar 2011 – Feb 2016</p>

Calculus, linear algebra, geometry, probability and statistics, analysis, topology, number theory and abstract algebra.

---

# Skills

## Backend (Go)

- **Go services and restructuring** — gRPC (unary/streaming), Kafka consumers and PostgreSQL/Redis/MongoDB, built in clear layers. Over three years I developed and restructured several Go services (api-activity, api-bookmark, api-sentinel, api-account, api-notification, api-blockchain-supporter) and split complex code behind interfaces to keep coupling low.
- **Concurrency and consistency** — PostgreSQL advisory locks, Redis NX/distributed locks/Lua, idempotency keys and unique keys, chosen per event type: look-up-then-create/update for messages that may arrive out of order, Redis NX for single-message events. I also re-check where atomicity actually ends — in a daily-limit counter I found the check sat outside the Lua script and wrote that up as a retrospective.
- **Failure paths first** — pre-deduction/rollback, DLQ and retries, CDC: decide how to recover before implementing. From a rolled-back feature (withdrawal delay) I learned to merge defect fixes separately from the feature so they survive a rollback.
- **API and policy design** — policies come in as enums/config rather than code branches, so policy changes don't become commits.

## Data & Messaging

- **Kafka** — consumer handlers, retry queues and DLQs; recovering failed external calls through an outbox (in review).
- **CDC and pipelines** — Debezium → Kafka → Snowflake Stream/Task. Took part in moving batch jobs and direct publishing to CDC under a "services don't write outward themselves" rule, and manage cost with a slot-keepalive batch, conditional tasks and a stateful/history table split.
- **DB design and query tuning** — DDL managed through DBA review (103 commits in portal-ops); improved reads with OR → UNION ALL and cursor pagination.

## Infrastructure & DevOps

- **Using and maintaining CI/CD** — the team's GitLab CI (test → build → deploy → release), multi-stage Dockerfiles and Rundeck deploy jobs; I didn't design them. I fixed broken builds (semantic-release, runtime upgrades) and wired new services into the [pipeline](#dg:cicd) by following existing patterns. Deployment differs per environment (dev: K8s API / test·qa·stage: Rundeck / live: Rundeck outside CI) and I operate with that distinction.
- **Kubernetes manifests** — wrote and operated Helm templates and per-environment Deployment · HPA · Service; tuned probes, resources and ports for cost and stability (e.g. reducing test/qa/stage resources).
- **Deploy and ops routine** — dev-first deployment before promotion, post-deploy monitoring on live, and scheduled-maintenance support as part of regular work.
- **Gateway** — operate Envoy gRPC → REST routes (82 commits) and auth settings; took part in the team's review of externally exposed APIs and adding authentication.

## Observability & Debugging

- **Observability** — correlation keys so a request can be traced across Datadog, Jaeger and OpenSearch; logs where they're needed; monitoring after each deploy.
- **Hypothesis-driven debugging** — context and environment first, then narrow the scope. Intermittent BFF pod restarts were traced to gRPC calls inside async loops holding resources and fixed with timeouts and chunked calls.
- **Operational automation** — built an error-triage bot that gives LLM first-pass analysis of Slack alerts, and hardened it after a vendor model deprecation with retries, backoff and a semaphore. After the replacement model was itself deprecated, "check vendor availability first" became part of the closing criteria.

## Collaboration

- **Clarifying requirements** — turn vague specs into developer terms and separate "current assumptions" from "needs verification" with DBA, data engineering, security, product, front-end and blockchain teams.
- **Visual communication and documentation** — diagrams and written proposals, open to a better direction; documentation and handover notes are how I close work.
- **Reviews as principles** — payment/security features go through two review rounds; feedback ("no log-and-swallow on external calls", "inject config at boot") is written down as team principles.
