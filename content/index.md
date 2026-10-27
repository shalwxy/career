# Career Description

안녕하세요. 이승하입니다.

백엔드 엔지니어로 일하고 문제를 해결하는 시간을 가장 좋아합니다.

---

# Work Experience

## NEXON UNIVERSE — Maplestory Universe

<p class="meta">Backend Developer · 넥슨유니버스 플랫폼개발팀 · 2023.11 ~ 2026.11 (3년)</p>

메이플스토리 IP를 기반으로 한 Web3 플랫폼 **메이플스토리 유니버스(MSU)** 를 개발합니다. 온체인 트랜잭션 동기화에서 시작해 트랜잭션 이력·북마크·거래소 BFF·계정/결제·통합 알림·정책 서비스·데이터 파이프라인·운영 AI까지 담당했습니다.

<div class="stats">
<div><strong>33</strong><span>저장소</span></div>
<div><strong>3,700+</strong><span>커밋</span></div>
<div><strong>4</strong><span>신규 서비스·도메인·봇<br/>신설 · 초기 참여</span></div>
<div><strong>3년</strong><span>재직</span></div>
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

> 분산 환경에서 데이터 정합성을 지키는 설계가 주 역할입니다 — **선점 · 멱등 · Outbox · CDC**.

<p class="cta">
<a class="btn" href="portfolio.html"><svg viewBox="0 0 16 16" width="15" height="15" aria-hidden="true"><path fill="currentColor" d="M2 2.5A1.5 1.5 0 0 1 3.5 1h5.8c.4 0 .8.16 1.06.44l2.7 2.7c.28.28.44.66.44 1.06v8.3A1.5 1.5 0 0 1 12 15H3.5A1.5 1.5 0 0 1 2 13.5v-11Zm1.5-.5a.5.5 0 0 0-.5.5v11c0 .28.22.5.5.5H12a.5.5 0 0 0 .5-.5V5.5H10a1 1 0 0 1-1-1V2H3.5Zm1 5.5h7v1h-7v-1Zm0 2.5h7v1h-7v-1Zm0 2.5h4.5v1h-4.5v-1Z"/></svg>Portfolio — 문제·접근·결과<svg class="arr" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path fill="currentColor" d="M8.3 3.3a1 1 0 0 1 1.4 0l4 4a1 1 0 0 1 0 1.4l-4 4a1 1 0 0 1-1.4-1.4L10.6 9H3a1 1 0 1 1 0-2h7.6L8.3 4.7a1 1 0 0 1 0-1.4Z"/></svg></a>
<a class="btn btn-ghost" href="decisions.html"><svg viewBox="0 0 16 16" width="15" height="15" aria-hidden="true"><path fill="currentColor" d="M8 1a7 7 0 1 1 0 14A7 7 0 0 1 8 1Zm0 1.5a5.5 5.5 0 1 0 0 11 5.5 5.5 0 0 0 0-11ZM8 4a1 1 0 0 1 1 1v2.6l1.7 1a1 1 0 1 1-1 1.7l-2.2-1.3A1 1 0 0 1 7 8V5a1 1 0 0 1 1-1Z"/></svg>Design Decisions — 선택의 이유<svg class="arr" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path fill="currentColor" d="M8.3 3.3a1 1 0 0 1 1.4 0l4 4a1 1 0 0 1 0 1.4l-4 4a1 1 0 0 1-1.4-1.4L10.6 9H3a1 1 0 1 1 0-2h7.6L8.3 4.7a1 1 0 0 1 0-1.4Z"/></svg></a>
</p>

### What did I do

#### <span class="phase">1</span> 온체인-오프체인 동기화 (DE)
<p class="period">2023.11 ~ 2024.04 · <a href="portfolio.html#de">자세히 보기 →</a></p>
<p class="chips"><span class="chip">Go</span><span class="chip">Saga</span><span class="chip">Redis 분산 락</span><span class="chip">Helm</span></p>
<div class="impact"><span class="impact-k">Impact</span> 캐릭터 민트 시 <strong>닉네임 중복 생성 이슈를 Redis 락 선점으로 수정</strong> · NFT 아이템 유효성 검사의 건별 반복 조회를 <strong>목록 조회 1회</strong>로 개선 · DE 리포 4개에 186 커밋</div>

- 신규 코어 서비스 연동 시 **BP 단 유효성 검사·converter·gRPC 에러 래핑** 추가
- [Saga v2](#dg:saga) 전환에 맞춰 **재화(neso/currency)·캐릭터 유효성 검사기 추가**, NFT 아이템 검사는 단건 반복 조회 → 목록 조회로 보완
- 캐릭터 민트 **닉네임 중복 생성 이슈 수정** — 존재 확인 대신 Redis 락으로 선점, 민트 성공 시에만 해제
- Helm 배포 운영 — 신규 서비스 롤아웃, 장애 재현용 임시 배포/롤백, test/qa 전 dev 선행 배포

#### <span class="phase">2</span> 트랜잭션 이력 · 북마크 · 거래소 BFF
<p class="period">2024.06 ~ 2025.09 · <a href="portfolio.html#activity">자세히 보기 →</a></p>
<p class="chips"><span class="chip">gRPC</span><span class="chip">Kafka</span><span class="chip">PostgreSQL advisory lock</span><span class="chip">Redis NX</span><span class="chip">CDC</span><span class="chip">Snowflake</span></p>
<div class="impact"><span class="impact-k">Impact</span> api-activity 구조 개선 후 확장(<strong>907 커밋</strong>) · api-bookmark 과반 커밋(<strong>550 커밋</strong>) 모두 라이브 승격 · Redis NX + advisory lock 으로 동시 적재 중복 차단 · 간헐적 pod 재시작 원인 규명·해결</div>

- **대용량 트랜잭션 이력 서비스([api-activity](#dg:activity))** — 레이어 재정비·컨슈머 일반화·메시지 포맷 v2 후 거래/민팅/전송/Swap&Warp/USDT 를 차례로 확장. 트랜잭션 해시 유니크 승격, Redis NX + PostgreSQL advisory lock 으로 [동시 적재 정합성](#dg:activity-lock), 비정상 이벤트는 DLQ
- **쿼리 튜닝·성능 개선** — DBA 와 협업한 OR → UNION ALL 전환, 커서 기반 무한 스크롤, 조건부 캐싱(공통 라이브러리 직접 개발)
- **알림 이벤트 발행 구조**, Snowflake 적재를 Kafka 발행 → **CDC 로 전환**해 유실 경로 제거
- **북마크/조회수 서비스([api-bookmark](#dg:bookmark))** 신규 설계 — 멱등 처리, Redis 카운트 캐시 → Kafka 이벤트 집계, 하루/총량 제한, 회원 탈퇴 연동
- **거래소 웹 BFF(bff-marketplace)** — 북마크/액티비티 마이그레이션, 인벤토리 서비스의 북마크·판매중 목록 조회 구현. 간헐적 pod 재시작을 로그 추적으로 비동기 루프 내 gRPC 호출 자원 점유로 좁혀 timeout·chunk 호출로 해결
- [Swap & Warp](#dg:swapwarp) 신규 도메인(bff-swapnwarp 포함) · 전사 proto 저장소 도메인별 모듈화 주도(저장소 165 커밋) · 공통 라이브러리 마이그레이션을 플랫폼·거래소 서비스 6곳에 2주 내 연속 적용 · Envoy 게이트웨이 route 운영 · Java/Spring Kafka 컨슈머에 북마크 이벤트 적재 추가 · 런칭 전 거래소 BFF·게임데이터 버그 픽스
- 확률 고지 서비스 요구사항 분석·버저닝·데이터 적재
- 백오피스 아이템/토큰 제재(단건·일괄·대량) 기능과 제재 이력 조회 화면

#### <span class="phase">3</span> 계정 · 결제 · 통합 알림
<p class="period">2025.07 ~ 2026.08 · <a href="portfolio.html#creditcard">자세히 보기 →</a></p>
<p class="chips"><span class="chip">Worldpay</span><span class="chip">Redis Lua</span><span class="chip">SSE</span><span class="chip">gRPC streaming</span><span class="chip">MongoDB</span><span class="chip">Outbox</span></p>
<div class="impact"><span class="impact-k">Impact</span> 신용카드 인증을 완성하고 계정 재인증에 <strong>신용카드 수단</strong>을 붙여 라이브 승격 · 일일 시도 카운트의 <strong>증가+만료를 Lua 로 원자 처리</strong> · 대량 수신자 응답을 <strong>500건 청크 스트리밍</strong>으로 분리 · KYC 전 사용자 마이그레이션 live 완료</div>

- **월드페이(FraudSight 3DS) [신용카드 인증 · 재인증](#dg:creditcard)** — 벤더 응답 분기(400대는 outcome, 500대는 에러), Redis Lua 로 일일 3회 카운트 **증가+만료 원자 처리**, 카드 정보 일부 암호화, 결제수단 조합별 이상 시도 차단, OTP 리셋용 재인증
- **[스테이블 코인(USDT) 도입](#dg:usdt)** — 오프체인 선차감·롤백 서비스를 USDT 에 맞춰 확장(토큰 단위 한도 테이블 재설계, 선차감·행 잠금 로직을 토큰별로 일반화), 별도 롤백 토픽 대신 트랜잭션 결과 토픽을 구독해 실패 시만 되돌리도록 단순화
- **[MSU 통합 알림(SSE)](#dg:notification)** — JWT 검증 자체 흡수로 의존 제거, 백엔드 URL 생성, 대량 수신자를 **gRPC streaming RPC**(500건 청크·5만 건 상한)로 분리
- 팀 단위 게이트웨이 gRPC → HTTP 전환에 맞춰 담당 서비스(통합 알림·블록체인 서포터)의 라우팅·포트 설정 이전
- **KYC 업체 변경(Argos → Sumsub)에 따른 전 사용자 데이터 이관 배치** — 구간 분할 병렬 실행·재진입 가능한 커서·호출 한도 관리, live 이관 완료
- 디스코드 자동 뱃지·역할 동기화 배치 개발, 공지 크롤링 봇에 게시판 추가·실패 지점 재개 확장 — 역할 부여 실패는 **Outbox 재시도**로(리뷰 중)
- 이메일 변경 후 보안 설정 잠금 — Redis TTL → DB 컬럼 영속화, Primary 조회로 복제 지연 창 제거

#### <span class="phase">4</span> 정책 서비스 · 데이터 파이프라인 · 운영 자동화
<p class="period">2026.01 ~ 2026.11 · <a href="portfolio.html#sentinel">자세히 보기 →</a></p>
<p class="chips"><span class="chip">Debezium</span><span class="chip">Snowflake Stream/Task</span><span class="chip">Vertex AI</span><span class="chip">OpenSearch</span><span class="chip">GitLab CI</span><span class="chip">Helm · EKS</span></p>
<div class="impact"><span class="impact-k">Impact</span> 흩어진 제어 로직을 <strong>정책 서비스 1개로 통합</strong>(4개 서비스가 단일 진입점 사용) · 배치 동기화 잡을 <strong>CDC 파이프라인</strong>으로 대체 · 운영 에러 1차 분석 자동화, 벤더 모델 폐기 장애 <strong>3일 내 1차 대응</strong>(재발 시 재교체)</div>

- **비즈니스 정책 서비스([api-sentinel](#dg:sentinel)) 신설** — 여러 서비스에 흩어져 있던 제어 로직을 단일 서비스로 통합
    - **ACL** (지갑/IP 화이트·블랙리스트), **Rate Limit** (Sliding/Fixed Window + jitter), **Lockout** (실패 횟수 보존/초기화 유연 설계), **Feature Flag** (런타임 변경)
- **[PostgreSQL CDC → Snowflake 파이프라인](#dg:cdc)** — Debezium 커넥터, Stream/Task, replication slot keepalive 배치, 조건부 task 로 비용 최적화
- **[에러시로봇(운영 AI)](#dg:errorbot)** — Slack 에러 알림을 LLM 으로 1차 분석(GitLab 커밋 대조·OpenSearch 히스토리·escalation), 벤더 모델 폐기 장애를 모델 교체·재시도/백오프·세마포어로 3일 내 대응
- 운영 콘솔 — 디스코드 메시지 재전송, SNS 권한 도메인 분리, 지갑↔SNS ID 조회
- **[CI/CD · 인프라 운영](#dg:cicd)** (전 기간) — 팀의 기존 파이프라인·매니페스트 패턴을 가져다 쓰며 담당 서비스의 GitLab CI · Dockerfile · Helm/K8s 매니페스트 · Envoy route · DDL 을 보수, 신설 서비스는 배포 세트까지 복제 · <a href="portfolio.html#infra">자세히 →</a>

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

<p class="meta">AI Engineering R&D · 유클릭 AI사업본부 AI서비스1팀 · 2021.01 ~ 2023.10 (1년 10개월)</p>

<div class="stats">
<div><strong>4</strong><span>프로젝트</span></div>
<div><strong>Metaverse</strong><span>Digital Twin</span></div>
<div><strong>GPU</strong><span>MIG · deepops</span></div>
<div><strong>1년 10개월</strong><span>재직</span></div>
</div>

<p class="badges">
<span class="b">Python</span>
<span class="b">ROS</span>
<span class="b">NVIDIA Omniverse</span>
<span class="b">UnrealEngine4</span>
<span class="b">Ansible</span>
<span class="b">Prometheus</span>
<span class="b">Grafana</span>
<span class="b">Shell Script</span>
<span class="b">Linux</span>
</p>

### <span class="phase">1</span> NVIDIA Omniverse R&D
<p class="period">2022.06 ~ 2023.10</p>
<p class="chips"><span class="chip">Python</span><span class="chip">ROS</span><span class="chip">IsaacSim</span><span class="chip">UnrealEngine4 (VR)</span></p>

#### Description

NVIDIA의 메타버스 제작 및 시뮬레이션 플랫폼인 Omniverse를 조사하고 Omniverse 애플리케이션에서 개발 및 프로젝트, PoC를 수행합니다.

NVIDIA의 Metaverse(Industrial Digital Twin) Solution인 Omniverse 플랫폼에서 Python을 이용해서 협동 로봇 프로젝트를 수행합니다.

#### What did I do

- **NVIDIA Omniverse IsaacSim** 에서 로봇 조립 및 시뮬레이션 — ROS 메시지 통신(Python) 이용
- **NVIDIA Omniverse CreateXR** 에서 VR 장비 연동 및 탐색 — UnrealEngine4 기반 VR 싱글 플레이 예제(C++) 개발

### <span class="phase">2</span> GC-GPU 솔루션 장애에 대한 원인 진단 및 해결
<p class="period">2022.04 ~ 2022.05</p>
<p class="chips"><span class="chip">PHP</span><span class="chip">Shell Script</span><span class="chip">Linux</span></p>

#### Description

GPU를 이용한 학습 및 추론 솔루션(GPU를 여러 개로 분할해서 교육기관 내 다수의 학생이 각자의 계정과 이미지로 AI 학습 및 추론을 할 수 있도록 하는 플랫폼으로, 계정 관리 및 GPU 자원을 모니터링하는 관리자 화면이 포함된 솔루션)에 대해 솔루션 소스를 보유하여 장애 발생 시 원인을 진단하고 해결합니다.

#### What did I do

- 커널 패닉 발생 관련 로그 분석
- 환경과 솔루션 소스 단에서 분석해 장애 해결

### <span class="phase">3</span> NVIDIA GPU MIG 기능 지원
<p class="period">2022.03 ~ 2022.04</p>
<p class="chips"><span class="chip">NVIDIA GPU MIG</span><span class="chip">Shell Script</span><span class="chip">Kubernetes</span></p>

#### Description

NVIDIA GPU를 분할해서 사용 가능한 MIG 기능을 지원합니다.

#### What did I do

- 신한 DS 개발·운영 서버에 NVIDIA GPU MIG 기능 **현장 지원**
- 시스템 재부팅 후 MIG 프로필을 생성하는 **Shell Script 제작·제공**

### <span class="phase">4</span> NVIDIA deepops 기반 GPU 모니터링 솔루션 재구성
<p class="period">2022.01 ~ 2022.02 · 프로젝트 전체 담당</p>
<p class="chips"><span class="chip">Ansible</span><span class="chip">Prometheus</span><span class="chip">Grafana</span><span class="chip">Shell Script</span></p>

#### Description

NVIDIA GPU를 사용하는 Kubernetes 및 Slurm 클러스터 용도 인프라 자동화 도구인 NVIDIA deepops(오픈소스)를 이용해서 GPU 모니터링 환경을 자동으로 구축하고, 폐쇄망 환경에서도 구축 가능하도록 패키지를 재구성합니다.

#### What did I do

- NVIDIA deepops 기반 GPU 모니터링 환경(**Prometheus, Grafana**)을 Ansible 로 설치하고 가이드로 정리
- **폐쇄망 환경**에서도 구성 가능하도록 Ansible 파일 분석 → Shell Script 작성 + 이미지 패키징으로 재구성

---

## UCLICK — Backend Developer

<p class="meta">Backend Developer · 유클릭 기술연구소 연구2실 · 2019.11 ~ 2021.12 (2년)</p>

<div class="stats">
<div><strong>4</strong><span>프로젝트</span></div>
<div><strong>UNO Platform</strong><span>Gateway · MSP</span></div>
<div><strong>OPEN API</strong><span>동적 API · 라우팅</span></div>
<div><strong>2년</strong><span>재직</span></div>
</div>

<p class="badges">
<span class="b">Java</span>
<span class="b">Spring Boot</span>
<span class="b">Spring JPA</span>
<span class="b">MyBatis</span>
<span class="b">Oracle</span>
<span class="b">PostgreSQL</span>
<span class="b">MySQL / MariaDB</span>
<span class="b">Kafka</span>
<span class="b">Elasticsearch</span>
<span class="b">Redis</span>
<span class="b">Hazelcast</span>
<span class="b">OCI</span>
</p>

### <span class="phase">1</span> UNO-GATEWAY
<p class="period">2020.09 ~ 2021.12</p>
<p class="chips"><span class="chip">Java</span><span class="chip">Spring Boot</span><span class="chip">Multi-DB</span><span class="chip">Ribbon · Eureka</span><span class="chip">Kafka</span><span class="chip">Elasticsearch</span></p>

#### Description

동적 API를 생성·수정·서비스할 수 있는 OPEN API 플랫폼입니다. 메시지 검증 및 변환, 인가/인증, 유량 제어, 라우팅 등의 기능을 제공합니다.

#### What did I do

- 웹 소켓 기능 및 **성능 현황 구현**
- **다중 Database 연계** — Oracle · MySQL/MariaDB · MSSQL · Tibero · PostgreSQL · Db2 · H2
- **외부 시스템 연계** — Elasticsearch · Hazelcast · Redis
- **로드밸런싱 테스트** — Ribbon with/without Eureka
- 통합 테스트 및 패키지 배포

### <span class="phase">2</span> UNO-GATEWAY 신한금융투자 MDB 프로젝트
<p class="period">2021.09 ~ 2021.10 · 프로젝트 전체 담당</p>
<p class="chips"><span class="chip">Java</span><span class="chip">Spring Boot</span><span class="chip">TCP</span><span class="chip">전문 변환</span></p>

#### Description

개발자가 UNO-GATEWAY에 API 요청 시 요청을 전문 데이터로 변환해 신한금융투자 서버에 TCP 요청하고, TCP 응답으로 받은 전문 데이터를 다시 JSON 템플릿으로 변환해서 API 호출에 응답하는 프로젝트입니다.

#### What did I do

- 샘플 데이터 분석 및 요구사항 명료화
- 사용자 JSON과 MDB 서버 전문 **상호 변환 로직** 담당
- 추가 요구사항 수용 — 관리 포인트를 EXCEL에서 QRY 파일 형식으로 변경

### <span class="phase">3</span> UNO-MSP
<p class="period">2020.02 ~ 2021.12 (1~4차 고도화) · 프로젝트 메인 개발</p>
<p class="chips"><span class="chip">Java</span><span class="chip">Spring Boot</span><span class="chip">Spring JPA</span><span class="chip">MyBatis</span><span class="chip">PostgreSQL</span><span class="chip">Hazelcast</span><span class="chip">Oracle Cloud (OCI)</span></p>

#### Description

Oracle Cloud Infrastructure를 이용하는 고객사·관리자를 대상으로 클라우드 자원·정보·자원 간 관계를 보여주는 대시보드와, 관리자가 직접 자원을 생성/수정/관리하는 페이지를 보유한 MSP(Managed Service Provider) 플랫폼입니다.

#### What did I do

- **4차 고도화 (2021.11 ~ 2021.12)** — Agent·UI 서버 이중화, 리소스 이력 수집, ZENDESK 연동 및 티켓 현황, JDBC 기반 DB 성능 모니터링
- **3차 고도화 (2021.02 ~ 2021.08)** — SLACK/MAIL 알림 전송 자동화, 클라우드 월간 리포트 자동화, OCI 설정(알람·규칙·모니터) 실시간 동기화
- **2차 고도화 (2020.11 ~ 2021.01)** — MSP 자체 임계값 설정·알림(메일·슬랙·웹 토스트), OCI 설정 CRUD, OCI 청구서 데이터 무결성 보장
- **1차 개발 (2020.02 ~ 2020.07)** — OCI API 실시간 정보 수집, 대시보드(CPU/Memory/Disk/Network I/O), 리소스 포함 관계 Treemap, Health Check, 리소스별 청구 금액 및 Excel 다운로드

### <span class="phase">4</span> LISTEN2ME-SURVEY
<p class="period">2020.09 ~ 2020.10</p>
<p class="chips"><span class="chip">Java</span><span class="chip">Spring Boot</span><span class="chip">Spring JPA</span><span class="chip">Oracle</span></p>

#### Description

규격 엑셀 시트를 설문조사 페이지로 변환하여 설문 URL 링크를 제공하고, 관리자 화면에서는 설문 결과 통계를 대시보드로 보여주는 웹 애플리케이션입니다.

#### What did I do

- 백엔드와 프론트엔드 간 **데이터 교환 형식** 정의
- 설문 결과 및 통계를 효과적으로 보여주는 **대시보드 데이터 구성**

---

# Other Experiences

## 자격증

<table class="certs">
<thead><tr><th>자격명</th><th>발급 기관</th><th>취득일</th></tr></thead>
<tbody>
<tr><td><strong>정보처리기사</strong></td><td>과학기술정보통신부</td><td>2019.08</td></tr>
<tr><td><strong>SQL개발자 (SQLD)</strong></td><td>한국데이터산업진흥원</td><td>2019.09</td></tr>
<tr><td><strong>정보보안기사</strong></td><td>과학기술정보통신부</td><td>2023.05</td></tr>
<tr><td><strong>리눅스마스터 1급</strong></td><td>한국정보통신진흥협회</td><td>2021.05</td></tr>
<tr><td><strong>네트워크관리사 1급</strong></td><td>한국정보통신자격협회</td><td>2023.05</td></tr>
<tr><td>리눅스마스터 2급</td><td>한국정보통신진흥협회</td><td>2020.07</td></tr>
<tr><td>네트워크관리사 2급</td><td>한국정보통신자격협회</td><td>2020.07</td></tr>
</tbody>
</table>

## 한국방송통신대학교 컴퓨터과학과

<p class="meta">2021.03 ~ 2024.02</p>

좋은 개발자가 되기 위해서는 지식 및 소통 측면에서 컴퓨터 과학에 대한 이해가 필요하다고 생각해 입학했습니다. 컴퓨터과학과 전공 과목만 수강하였으며, 전산 기초인 디지털논리회로, 컴퓨터구조, 운영체제, 컴파일러구성, 자료구조, 알고리즘, 데이터베이스 과목과 프로그래밍 언어인 C프로그래밍, C++프로그래밍, Java 프로그래밍, 모바일앱프로그래밍, JSP프로그래밍 과목과 그 외에도 개발에 필요한 과목인 컴퓨터보안, 클라우드컴퓨팅, 시뮬레이션 등을 수강했고, 언급한 과목들 모두 A+을 취득했습니다.

---

## 한국폴리텍대학교 융합기술교육원 데이터융합 소프트웨어학과

<p class="meta">2019.03 ~ 2019.11</p>

개발자로 전향하기 위해 Java·Spring, Python·R, Linux, Database, 웹 프로그래밍을 실무 중심으로 배운 9개월 과정입니다. 과정 중 만든 것은 네 가지입니다 — Oracle SQL로 대용량 고객 데이터에서 신규 회원 유입 통계를 뽑아 R·Excel로 시각화, JSP와 Open API(날씨 XML·환율 JSON)를 파싱해 chart.js로 보여주는 웹 페이지, MVC(DAO·Service·UI) 기반으로 DB CRUD와 소비 패턴 통계까지 구현한 가계부, 그리고 Ubuntu 서버의 CPU·메모리·디스크를 실시간으로 갱신해 보여주는 모니터링 페이지. TensorFlow로 공부 시간 → 시험 성적 회귀 예측도 해 봤습니다.

---

## 이화여자대학교 수학교육과

<p class="meta">2011.03 ~ 2016.02</p>

전공수학으로 미분적분학, 선형대수학, 기하학, 확률과 통계, 해석학, 위상수학, 정수론, 현대대수학 등을 학습했습니다. 구체적으로는, 미분을 이용해서 n 차원의 주어진 범위 내에서 함수의 최솟값과 최댓값을 구했고, 선형대수학을 활용해서 빠른 연산이 가능하도록 기저를 변환하여 효과적인 행렬 연산을 수행했습니다. 기하학을 사용해서는 도형과 그 성질들 간 상호 관계를 체계적으로 정리했고, 해석학을 통해서 실함수를 분석했습니다. 위상수학으로 형태는 달라도 구조가 같은 기하학적 성질을 다루었고, 정수론을 이용해서 정수 조건의 문제를 빠르게 해결했습니다. 현대대수학에서는 구조를 최대한 추상화해서 수학의 영역을 확장했습니다.

---

# Skills

## Backend Development

- **Golang 기반 개발과 리팩토링:** Go 언어의 고루틴과 채널을 활용한 동시성 처리에 능숙합니다. 복잡한 코드를 그대로 두지 않고, 인터페이스를 활용해 기능을 작은 단위로 쪼개고 결합도를 낮추는 리팩토링을 꾸준히 해왔습니다.
- **데이터 설계 및 최적화:** 대용량 트래픽이나 동시 요청 상황에서도 데이터가 꼬이지 않도록 PostgreSQL advisory lock, Redis 분산 락·Lua 원자 처리, 멱등 설계를 활용한 설계와 최적화에 적극적입니다. 요청/결과 메시지가 순서 없이 들어오는 환경에서도 중복 저장이 발생하지 않도록 스키마·애플리케이션·DB 세 층에서 함께 설계합니다.
- **실패 경로 우선 설계:** 선차감·롤백, Outbox(TxEvent) 활용, DLQ, CDC 처럼 "잘못됐을 때 어떻게 복구할지"를 먼저 설계합니다. 큰 기능이 기획 변경으로 롤백되어도, 그 과정에서 발견한 결함 수정은 남겨 가치를 보존합니다.
- **유연한 API 설계:** 새로운 가이드나 외부 API 문서를 분석해 서비스에 녹이는 것을 좋아하며, 나중에 다른 시스템(로봇이나 외부 서비스)이 붙더라도 유연하게 확장할 수 있는 구조를 고민하며 개발합니다. 정책은 코드 분기가 아니라 enum/설정으로 받아, 정책이 바뀔 때 커밋이 아니라 설정이 바뀌도록 합니다.

## Architecture & Operations

- **신규 서비스·도메인을 라이브까지:** api-sentinel 은 초기 커밋부터 신설, api-bookmark 와 Swap&Warp 는 과반 커밋으로 라이브 승격, portal-ai 에는 에러시로봇 기능을 신설했습니다. 레이어를 처음부터 나눠 두면, 이후 기능 추가가 구조 변경 없이 들어온다는 걸 반복해서 경험했습니다.
- **데이터 파이프라인 분리:** "서비스가 직접 외부에 쓰지 않는다"는 원칙으로, 배치 → publish 제거 → CDC(Debezium + Snowflake Stream/Task)로 이동시켰습니다. 상태성/이력성 테이블 구분, replication slot keepalive, 조건부 task 처럼 운영 비용과 유실 경로를 함께 고려합니다.

## Infrastructure & CI/CD

- **파이프라인 사용·보수:** 팀에 갖춰진 GitLab CI(test → build → deploy → release) · multi-stage Dockerfile · Rundeck 배포 job 을 가져다 썼습니다. 설계한 것은 없고, 깨진 빌드(semantic-release · 런타임 버전)를 고치고 신설 서비스를 기존 패턴대로 [파이프라인](#dg:cicd)에 태웠으며, 운영 대역 승격 전 dev 선행 배포 패턴을 지켰습니다.
- **Kubernetes 매니페스트:** Helm 템플릿과 환경별 Deployment · HPA · Service 를 작성·운영했습니다. probe · 리소스 · 포트 같은 운영 설정을 비용과 안정성 기준으로 조정합니다.
- **게이트웨이 · 데이터 인프라:** Envoy gRPC → REST route, Debezium/Kafka Connect · Snowflake 설정, DBA 검토 흐름의 DDL 관리까지 애플리케이션 경계 밖도 함께 봅니다.

## Logging / Debugging

- **의미 있는 로그 남기기:** 장애가 터졌을 때만 로그를 보는 게 아니라, 개발·운영 단계에서 필요한 위치에 로그를 꼼꼼히 남기고 주기적으로 모니터링합니다. Datadog · Jaeger · OpenSearch 를 사용해 요청 흐름을 끝까지 추적할 수 있도록 상관관계 키를 설계합니다.
- **가설 기반의 빠른 디버깅:** 문제가 발생하면 무작정 코드부터 보지 않고, 에러가 발생한 환경과 맥락을 먼저 파악합니다. 원인을 추측하고 범위를 좁혀가며 근본적인 문제를 빠르게 잡아냅니다. BFF 의 간헐적 pod 재시작처럼 원인이 숨은 이슈도 로그 추적으로 근본 원인(비동기 루프 내 자원 점유)까지 짚고 해결했습니다.
- **장애 재발 방지:** 모델 교체 같은 1차 조치에 재시도·백오프·세마포어·테이블 테스트를 함께 넣고, 교체한 모델이 다시 폐기된 재발을 겪은 뒤 **"가용 모델 사전 확인"** 을 종결 기준에 추가했습니다.

## Communication

- **요구사항 명료화:** 모호한 기획이나 요구사항을 개발자 관점에서 명확하게 정리하는 것을 좋아합니다. 풀고자 하는 문제를 확실히 정의하고 구현에 들어갑니다. DBA·DE·보안·기획과의 협업에서 "현재 가정"과 "검증이 필요한 지점"을 분리해 공유합니다.
- **시각화를 통한 수평적 소통:** 제 생각을 글이나 그림(다이어그램)으로 정리해서 공유합니다. 동료들과 의견을 주고받을 때 고집 부리지 않고 더 좋은 방향이 있다면 능동적으로 수용합니다.
- **선제적인 리스크 관리:** 이슈가 생길 만한 부분을 미리 예측하고 방어적인 코드를 짜거나 대비책을 세워둡니다. 필요할 때 바로바로 대응할 수 있는 상태를 유지하는 것을 선호합니다.
- **리뷰 지적을 원칙으로:** 결제·보안 기능은 리뷰 2회차까지 돌리고, 지적받은 내용("외부 호출은 log-and-swallow 금지", "설정은 부팅 시 주입")은 팀 원칙으로 문서화해 다음 작업에 반영합니다.

---