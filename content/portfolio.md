# Portfolio

> Web3 게임 플랫폼(메이플스토리 유니버스)에서 2023년 11월부터 담당한 프로젝트를 **문제 → 접근 → 결과** 순으로 정리했습니다. 공개용으로 정제한 요약이며, 각 항목 끝의 "관련 설계 결정" 링크에서 선택의 이유와 되돌린 결정까지 볼 수 있습니다.

## 한눈에 보기 {#overview}

| 시기 | 영역 | 핵심 |
|---|---|---|
| 2023-11 ~ 2024-04 | 온체인-오프체인 동기화(DE) | 유효성 검사 추가·보완, 닉네임 중복 생성 수정(Redis 락 선점), Helm 배포 운영 |
| 2024-06 ~ 2025-09 | 트랜잭션 이력 · 북마크 · 거래소 BFF | 트랜잭션 이력 서비스 구조 개선·확장, 북마크 서비스 개발(서버와 BFF 양쪽), Swap & Warp 도메인 추가 |
| 2025-07 ~ 2026-08 | 계정 · 결제 · 통합 알림 | Worldpay 신용카드 인증, USDT 출금 한도 선차감·롤백, SSE 알림, KYC 벤더 변경 데이터 이관 |
| 2026-01 ~ | 정책 서비스 · 데이터 파이프라인 · 운영 AI | 정책 서비스(rate limit·ACL 등) 신설, PostgreSQL CDC → Snowflake, LLM 에러 분석 봇 |

작업 철학은 네 가지입니다. **실패 경로부터 설계한다**(롤백·재시도·멱등이 본체), **확인 대신 선점한다**(존재 확인 후 생성은 경합 창이 있다), **서비스는 데이터 파이프라인에 직접 쓰지 않는다**(CDC), **정책은 코드 분기가 아니라 설정/enum 으로 받는다**.

---

## 1. 온체인-오프체인 동기화 — 유효성 검사와 닉네임 선점 {#de}

<span class="tag">2023-11 ~ 2024-04</span> <span class="tag">Go · gRPC · Redis · Saga</span>

**맥락.** 게임 자산(아이템·캐릭터·재화·닉네임)의 오프체인 상태와 온체인 트랜잭션을 Saga 로 동기화하는 조직에서 첫 업무를 시작했습니다. 게임 서버가 호출하는 gRPC 파사드(business-provider)와 Saga 실행기([saga-provider](#dg:saga)), 이벤트 저장소(event-service)를 다뤘습니다. 입사 첫 5개월의 작업이라 규모는 작지만, 이후 작업 방식의 출발점이 된 것들입니다.

**유효성 검사 추가·보완.** 신규 코어 서비스 연동 코드를 BP(파사드)에 만들면서 입력 유효성 검사, proto ↔ 도메인 변환기(단위 테스트 포함), gRPC 에러 래핑을 추가했습니다. 이어 Saga v2 전환 브랜치에서 재화(neso/currency)·캐릭터 유효성 검사기를 추가하고, NFT 아이템 검사가 건마다 상태 서비스를 호출하던 것을 **목록 조회 1회**로 바꿨습니다.

**닉네임 중복 생성 수정.** 캐릭터 민트 시 "닉네임이 존재하는지 확인한 뒤 생성"하던 방식은 확인과 생성 사이에 틈이 있어 같은 닉네임이 두 번 만들어졌습니다. 존재 확인을 없애고 **Redis 락으로 닉네임을 먼저 선점**, 해제는 민트 성공 시에만 하도록 고쳤고 캐릭터 생성에도 같은 방식을 적용했습니다. 작은 수정이지만 "확인 대신 선점" 은 이후 작업에서 계속 쓴 방식입니다.

**운영.** Helm 으로 신규 서비스를 롤아웃하면서, 장애 재현을 위한 임시 배포/롤백을 커밋으로 남기고 **test/qa 승격 전 dev 선행 배포**를 관행으로 정립했습니다.

<p class="more">관련 설계 결정: <a href="decisions.html#d-preempt">확인 대신 선점</a> · <a href="decisions.html#d-validator">검증은 목록 조회로</a></p>

---

## 2. 트랜잭션 이력 플랫폼 — 구조 개선부터 CDC 전환까지 {#activity}

<span class="tag">2024-06 ~ 2026-11</span> <span class="tag">Go · Kafka · PostgreSQL · Redis · Snowflake</span>

**맥락.** 플랫폼의 블록체인 트랜잭션(거래·민팅·전송·크로스체인 전송·스테이블 코인)을 [수집·조회·알림 발행하는 서비스](#dg:activity). 2024년 6월부터 2년 반, 가장 오래 담당했습니다.

**단계별 진화.**

| 시기 | 변화 |
|---|---|
| 2024-06 | 레이어 재정비, 거래 결과 전용이던 컨슈머를 범용 이벤트 컨슈머로 일반화, 불필요 기능 제거, 메시지 포맷 v2 — 이후 모든 확장의 토대 |
| 2024-11 | 트랜잭션 해시를 유니크 키로 승격해 중복 저장 차단, 비정상 이벤트는 DB 대신 DLQ 로 |
| 2025 Q1 | 크로스체인([Swap & Warp](#dg:swapwarp)) 도메인 추가, OR 조회 → UNION ALL, 커서 기반 무한 스크롤 |
| 2025 Q2~Q3 | Redis NX(거래·자산·Swap) + PostgreSQL advisory lock(Warp) 으로 동시 적재 정합성, 결과 적재 시 알림 이벤트 발행, 브릿지-인 확장 |
| 2026 Q1 | Snowflake 적재를 Kafka 발행에서 **CDC 로 전환** — 발행 실패 유실 경로 제거 |
| 2026 Q3 | 출금 지연 피처 구현 중 기존 결함(DB 에러 삼킴·커밋 전 알림 발행·갱신 조건) 발견·수정 → 피처 전체 롤백에 함께 되돌아감, 재적용 과제로 인수인계 |

**Deep dive — [Kafka 순서 비보장과 동시 적재](#dg:activity-lock).** 크로스체인 전송은 "요청 정보"와 "결과" 메시지가 역순으로 올 수 있고 재시도도 발생합니다. 단순 "exists → insert" 로는 중복이 생겼습니다.
→ 이벤트 종류별로 방어를 달리했습니다. 거래·자산·Swap 처럼 단건으로 끝나는 이벤트는 Redis SET NX 로 "먼저 잡은 쪽만 처리"(TTL, 처리 후 해제). 요청/결과가 뒤집혀 올 수 있는 Warp 는 스키마를 nullable 로 설계하고, 트랜잭션 범위 advisory lock(네임스페이스 키 + 해시 버킷 키, 버킷 상한 설정) 아래에서 선조회 후 생성/수정 — 먼저 온 쪽을 PENDING·NO_CONTENT 상태로 적재해 두고 나중에 온 쪽이 채웁니다. 2026년 워프 지연 작업 때 락 시드와 조회 키를 다시 맞추는 보완을 넣었으나 피처 롤백에 함께 되돌아갔습니다.

**Deep dive — 롤백된 피처에서 배운 것.** 2026 Q3 에 보안 요건으로 "출금 지연" 피처를 7개 저장소(서비스 4 · proto · DDL · 게이트웨이)에 걸쳐 구현했으나 기획 변경으로 전체 롤백됐습니다. 구현 중에 기존 결함 — DB 에러를 삼켜 "commit unexpectedly resulted in rollback" 을 내던 경로, 알림 발행이 커밋 전에 일어나는 경로, 갱신 조건이 식별자가 아닌 문제 — 을 찾아 고쳤지만 피처 커밋 흐름에 섞여 있어 **롤백에 함께 되돌아갔습니다**. 결함 수정은 피처와 분리해 먼저 머지해야 한다는 것을 배웠고, 되돌아간 수정은 분석 기록과 함께 재적용 과제로 인수인계했습니다.

<p class="more">관련 설계 결정: <a href="decisions.html#d-unique">유니크 키 승격</a> · <a href="decisions.html#d-lock">동시 적재 정합성</a> · <a href="decisions.html#d-cdc">publish 대신 CDC</a> · <a href="decisions.html#d-rollback">롤백에서 배운 것</a></p>

---

## 3. 북마크 · 조회수 서비스 신설과 거래소 BFF {#bookmark}

<span class="tag">2024-06 ~ 2025-09</span> <span class="tag">Go · gRPC · Kafka · Redis</span>

**[북마크 서비스](#dg:bookmark)(서버).** 초기부터 참여해 proto 설계부터 라이브까지 담당했습니다. 북마크는 더블클릭·재시도가 흔해 **멱등**이 기본이어야 했습니다 — 중복 요청은 성공 반환, 카운트는 DB 저장 성공 시에만 증가, 0 이하면 캐시 키 제거. 카운트 갱신은 요청 경로의 동기 처리에서 **Kafka 이벤트 기반**으로 옮겨 레이턴시와 정합성을 함께 잡았고, 하루/총량 제한과 회원 탈퇴 연동을 더했습니다.

**거래소 BFF(소비자).** 같은 서비스를 소비하는 거래소 웹 BFF 도 직접 마이그레이션해, 서버 proto 변경이 BFF 에 어떻게 닿는지 양쪽에서 확인했습니다. 인벤토리 서비스의 북마크·판매중 목록 조회 구현, 조회수 증가 비동기화, 캐릭터 이미지 렌더 병렬화·bulk 호출, 외부 조회 chunk 분할.

**장애 — 간헐적 pod 재시작.** 원인 불명으로 BFF pod 가 재시작되던 문제를 로그 추적으로 **비동기 반복문 안의 gRPC 호출이 자원을 점유**하는 것으로 좁히고, timeout 과 chunk 호출로 해결했습니다.

**캐시의 교훈.** BFF 북마크 캐시를 "변경 시 무효화" 로 설계했다가 비동기 무효화 실패·context 취소 문제로 timeout 을 늘려가던 끝에 **3초 TTL, 무효화 없음** 으로 단순화했습니다. 무효화보다 짧은 TTL 이 낫다는 걸 체감한 사례입니다.

**같은 시기.** 전사 proto 저장소를 도메인별 모듈로 재구성했습니다. Java/Spring Kafka 컨슈머에 북마크 이벤트 적재를 추가했고(이후 요구 변경으로 제거), 확률 정보 고지 서비스의 데이터 저장·버전 관리, 백오피스 제재 기능(단건·일괄·대량)과 제재 이력 화면을 공동 구축했습니다.

<p class="more">관련 설계 결정: <a href="decisions.html#d-idempotent">북마크 멱등성</a> · <a href="decisions.html#d-ttl">무효화 대신 TTL</a> · <a href="decisions.html#d-proto">proto 모듈화</a></p>

---

## 4. 신용카드 인증 · 재인증 — Worldpay 3DS {#creditcard}

<span class="tag">2025-08 ~ 2026-07</span> <span class="tag">Go · Redis Lua · 결제 보안</span>

**맥락.** 사용자가 등록한 신용카드를 [0원 결제(3DS)로 검증](#dg:creditcard)하고 토큰화해, 이후 OTP 리셋·보안 설정 변경의 재인증 수단으로 쓰는 기능. 결제 보안의 가장 민감한 영역이라 리뷰를 2회차까지 돌리며 완성했습니다.

**설계가 복잡했던 지점.**

- **벤더 응답 분기**
    - 벤더가 실패를 400대와 500대에 섞어서 돌려줍니다. 400대 대부분은 사용자가 고칠 수 있는 실패이고, 500대는 벤더 장애입니다.
    - 400대는 **200 + outcome 코드**로 바꿔 프론트가 안내를 분기하게 하고, 500대만 에러로 올려 재시도를 유도했습니다.
- **일일 3회 제한의 카운터**
    - "증가 + 첫 증가 시 만료 설정"을 **Redis Lua 스크립트**로 묶어 키 생성과 TTL 설정 사이의 틈을 없앴습니다.
    - 키에서 날짜를 빼고, UTC 자정까지의 만료 시각으로 리셋을 관리했습니다.
- **암호화와 이상 시도 차단**
    - 결제수단·발급사 정보를 암호화하고, 카드 소유자 정보 비교를 해시 기반으로 전환했습니다.
    - 같은 결제수단 조합으로 짧은 시간에 시도가 몰리면 일정 시간 차단하는 장치를 도입했습니다(이후 정책 서비스로 이관·고도화).
- **OTP 리셋용 재인증**
    - "새 카드 인증 / 기존 카드 재사용" 두 타입을 설계했습니다.
    - 일일 한도는 합산해서 적용하고, 벤더 오류는 횟수에서 차감하지 않았습니다.

**결과.** 2025 Q4 라이브 승격 후 재인증·OTP 리셋 재인증으로 확장되며 운영 중. 기획 변경(소유자명 검사 제거 등)에 따라 네이밍과 정책을 세 차례 조정하며 "컬럼 이름에 용도를 넣지 말 것" 이라는 교훈을 얻었습니다.

<p class="more">관련 설계 결정: <a href="decisions.html#d-worldpay">벤더 응답 분기</a> · <a href="decisions.html#d-lua">Lua 원자 처리</a> · <a href="decisions.html#d-naming">네이밍 교훈</a></p>

---

## 5. 스테이블 코인 도입과 선차감·롤백 {#usdt}

<span class="tag">2025-10 ~ 2025-12</span> <span class="tag">Go · Kafka · 블록체인</span>

온체인에 기록되기 전 발생할 수 있는 리스크(한도 초과, 중복 출금)를 막기 위해 **[오프체인에서 먼저 차감하고 결과에 따라 롤백](#dg:usdt)**하는 서비스를 스테이블 코인(USDT) 도입에 맞춰 확장·수정했습니다. 별도 롤백 토픽을 두는 대신 **트랜잭션 결과 토픽**에서 성공/실패/드랍을 받아 실패일 때만 선차감을 되돌리도록(선차감이 곧 확정) 순서·중복 처리를 단순화했고, 같은 nonce 로 여러 트랜잭션이 들어오는 케이스의 보정이 3건 이상에서 빠지던 것을 고쳤습니다. 토큰 추가 시 enum 만 늘리면 되도록 테이블을 재설계했습니다.

<p class="more">관련 설계 결정: <a href="decisions.html#d-settle">롤백 토픽 → 결과 토픽</a></p>

---

## 6. 통합 알림 서비스 — SSE 와 streaming RPC {#notification}

<span class="tag">2025-07 ~ 2026-11</span> <span class="tag">Go · SSE · gRPC streaming · MongoDB</span>

- 계정 서비스를 호출해 하던 JWT 검증을 알림 서비스가 **자체 흡수**해, SSE 연결마다 계정 서비스를 때리던 비용과 의존을 제거했습니다.
- "모든 사용자에게 통합 알림" 기능은 기획과 합의해 **제거** — 대량 fan-out 은 알림 서비스가 지지 않습니다.
- 알림 URL·타이틀·본문을 백엔드에서 생성해 프론트별 조립 중복을 없앴습니다(URL 생성과 payload 다수 담당).
- 백오피스 알림의 수신자 목록(수만 건)이 상세 조회 응답에 통째로 실리던 것을 **[gRPC streaming RPC](#dg:notification)**(500건 청크, 상한 명시)로 분리하고, 수신 규약("대상은 chunk 프레임으로만")을 수신 측 코드에 명시했습니다. 큰 응답을 쪼개는 것보다 **수신측이 어떻게 조립하는지**를 정하는 게 설계의 핵심이었습니다.
- 팀 단위 게이트웨이 gRPC → HTTP 전환에 맞춰 알림 서비스의 라우팅·포트 설정을 옮겼습니다.

<p class="more">관련 설계 결정: <a href="decisions.html#d-notify">통합 알림 3가지 결정</a> · <a href="decisions.html#d-stream">recipients 스트리밍</a></p>

---

## 7. 정책 서비스 신설 — rate limit · ACL · feature flag · lockout {#sentinel}

<span class="tag">2026-01 ~ 2026-11</span> <span class="tag">Go · Redis · PostgreSQL</span>

**문제.** 서킷 브레이커는 공통 라이브러리에, rate limit 은 계정 서비스에, 화이트리스트는 블록체인 서비스에 — 제어 로직이 흩어져 중복과 운영 혼란의 원인이었습니다.

**접근.** 1단계로 계정 서비스·공통 라이브러리에 있던 rate limit·서킷 브레이커·feature flag·ACL 을 포털 서비스로 모은 뒤, 콘텐츠 도메인과 섞이지 않도록 **[정책 전용 서비스](#dg:sentinel)**를 신설했습니다. rate limit 정책 refresh 를 각 서비스가 전체 정책을 메모리에 올리던 방식에서 **정책 서비스가 단일 소유자**가 되는 구조로 옮겨 메모리 이슈를 해결했고, sliding/fixed window 를 모두 지원하되 refresh 스파이크를 jitter 로 완화했습니다(ticker 대신 매 회차 랜덤 timer). 이어 OTP 반복 실패 잠금(lockout) 을 실패 횟수 보존/초기화 정책을 유연하게 설계해 추가하고, 블록체인 서비스의 화이트리스트까지 이전해 **통합을 완료**했습니다.

**결과.** 로그인 rate limit, 출금 화이트리스트, 백오피스 lockout 의 단일 진입점.

<p class="more">관련 설계 결정: <a href="decisions.html#d-sentinel">정책 전용 서비스 분리</a> · <a href="decisions.html#d-jitter">jitter 와 timer</a> · <a href="decisions.html#d-enum">정책은 enum 으로</a></p>

---

## 8. PostgreSQL CDC → Snowflake 파이프라인 {#cdc}

<span class="tag">2026-06 ~ 2026-11</span> <span class="tag">Debezium · Kafka Connect · Snowflake</span>

데이터 팀이 운영 DB 변경을 더 빠르게 조회하길 원했고, 기존 배치 동기화 잡은 지연과 잡별 코드 유지 비용이 있었습니다. Debezium 으로 변경 이벤트를 Kafka 로 흘리고 Snowflake Stream/Task 로 적재하는 [파이프라인](#dg:cdc)을 dev 에서 qa/live 로 확장하고, 계정 DB CDC 와 운영 설정(상태성/이력성 구분 · slot keepalive · 조건부 task)을 맡았습니다.

- **상태성/이력성 테이블 구분** — 현재 상태 테이블은 upsert, 이력 테이블은 insert 만, delete 이벤트는 적재 제외. publication 레벨에서 제어.
- **replication slot keepalive 배치** — 변경이 뜸한 테이블의 slot 이 밀려 WAL 디스크가 차는 것을 방지.
- **조건부 task** — stream 에 데이터가 있을 때만 task 를 실행해 실행 횟수 과금을 최적화.
- 커넥터 계정 교체 및 publication 대상 테이블 추가.

<p class="more">관련 설계 결정: <a href="decisions.html#d-cdc">publish 대신 CDC</a></p>

---

## 9. LLM 에러 분석 봇과 모델 폐기 장애 대응 {#ai}

<span class="tag">2026-07 ~ 2026-11</span> <span class="tag">Go · Vertex AI · Slack API · OpenSearch · GitLab API</span>

**문제.** 운영 에러가 Slack 에 들어오면 담당자가 매번 "어느 코드인지", "전에도 봤는지"를 수동 검색. 밤·주말 대응이 느렸습니다.

**솔루션.** [봇](#dg:errorbot)이 스택트레이스에서 파일을 추출해 **각 파일의 최근 커밋을 GitLab API 로 조회**해 회귀 후보를 프롬프트에 주입하고, 과거 분석을 OpenSearch 에 signature 키로 저장해 재사용·dedupe·escalation. 최초 감지 시각과 스레드 영구 링크를 함께 응답합니다. Slack 긴 메시지의 preview 잘림을 감지해 원문을 재조회하는 방어, 에러 폭주 시 LLM 동시 실행을 세마포어로 제한하는 보호를 넣었습니다.

**장애.** LLM 벤더가 사용 중 모델을 폐기(404)해 봇 전체가 멈췄습니다. 모델 교체에 그치지 않고 429/5xx 재시도(Retry-After 우선, 지수 백오프 + 지터), 에러 메시지 타입 분기, 테이블 테스트까지 3일 내 랜드했습니다. 나흘 뒤 교체한 모델마저 폐기돼 재교체하며 **"교체 전에 벤더 카탈로그에서 가용 모델을 확인했어야"** 한다는 교훈을 남겼습니다.


---

## 10. 인프라 · CI/CD — 배포 파이프라인과 운영 저장소 {#infra}
<p class="chips"><span class="chip">전 기간</span><span class="chip">GitLab CI · Docker · Helm · ArgoCD · Rundeck · EKS · Envoy · Kafka Connect</span></p>

**맥락.** 담당 서비스의 CI/CD 설정(GitLab CI → Rundeck → EKS, Helm, Envoy)은 백엔드 개발자가 직접 관리하는 구조였습니다. [파이프라인](#dg:cicd)으로 배포하면서 깨진 빌드를 고치고 신설 서비스를 연결했습니다. 대역별로 흐름이 달랐습니다 — dev 는 CI 가 K8s API 로 재시작, test·qa·stage 는 CI 가 Rundeck 을 호출, live 는 CI 가 이미지 빌드까지만 하고 배포는 CI 밖에서 Rundeck 으로.

**제가 한 일.**

- **CI 파이프라인 운영** — 담당 서비스 3개의 `.gitlab-ci.yml`·Dockerfile: 누락된 go test 단계 보완, Go 1.23 → 1.26 · Docker · Node 런타임 업그레이드, semantic-release 빌드 깨짐 수정(버전 고정), 신설 서비스의 배포 job 연결.
- **신설 서비스의 배포 세트** — api-sentinel 신설 때 Helm 템플릿(dev) · 4개 환경 매니페스트(Deployment · HPA · Service) · Envoy route · CI 배포 job 을 코드와 같은 주에 한 세트로 추가. 레지스트리 deploy token 만료 시 dockerconfigjson 교체.
- **Kubernetes 매니페스트 운영** (gotohelm · deploy-scripts) — liveness/readiness probe 보정, 서비스 포트 추가, 서비스명 변경, test/qa/stage pod 리소스 감축(비용 절감 요청 건), live 로그 레벨 정리, DE 서비스 초기 배포.
- **Envoy 게이트웨이** (marina) — 서비스가 늘어날 때마다 gRPC → REST 연결 규칙(route)을 추가·정리, 인증 적용·skip 설정, 미사용 cluster 제거, live 에서 특정 인증 호출 차단.
- **운영 저장소** (portal-ops) — PostgreSQL DDL 을 DBA 검토 흐름으로 관리, Debezium/Kafka Connect · Snowflake Stream/Task 설정([CDC](#dg:cdc)), MongoDB TTL 정책.
- **공용 Go 라이브러리** (platform-lib) — PostgreSQL 드라이버 `target_session_attrs`(읽기 복제본 라우팅), 캐시 데코레이터에 조건부 캐싱 옵션 추가.

**결과.** 서비스 신설·확장 시 애플리케이션 코드와 배포 설정을 같은 사람이 같은 MR 흐름에서 끝낼 수 있었습니다. 파이프라인 자체를 만들거나 바꾼 경험은 없고, 구조를 읽고 그 위에서 운영한 경험입니다.

<p class="more">관련 설계 결정: <a href="decisions.html#d-deployset">서비스 신설은 배포 세트까지</a> · <a href="decisions.html#d-devfirst">test/qa 승격 전 dev 선행 배포</a> · <a href="decisions.html#d-cdc">publish 대신 CDC</a></p>

---

## 11. 그 외 {#etc}

- **KYC 벤더 변경 데이터 이관 배치** — 글로벌 규제 대응으로 전 사용자 KYC 데이터를 신규 벤더로 이관하는 배치를 전담. 일련번호 구간을 나눠 여러 인스턴스로 병렬 실행, 재진입 가능한 커서, 벤더 호출 한도 관리로 live 이관 완료.
- **디스코드 자동 뱃지·역할 동기화** — 게임 내 달성도에 따라 역할을 자동 부여. 비동기 → 동기 전환으로 누락 방지, 연결 해제 시 식별 정보는 보존.
- **이메일 변경 후 보안 설정 잠금** — Redis TTL 에서 DB 컬럼 영속화로 전환, 선검사 API 대신 응답 필드 하나로 UX 통합, Primary 조회로 복제 지연 창 제거.
- **운영 콘솔** — 디스코드 메시지 재전송(rate limit·변경 감지), 권한 도메인 분리, 지갑↔SNS 조회.
- **그 밖의 기여** — 외부 노출 API(스왑워프·통합알림·BFF) 영향성 전수 조사와 인증 추가(팀 3인), 블록체인 서포터·BFF 지갑주소 유효성 검사 추가, 액티비티 로그 제거, PostgreSQL 메이저 버전 업그레이드에 따른 QA 대역 CDC 작업, 커뮤니티 공지 → 디스코드 크롤러에 게시판 추가·실패 지점 재개, 거래소 런칭 전 네비게이터·게임데이터 버그 픽스.

<p class="more">관련 설계 결정: <a href="decisions.html#d-lock-email">잠금은 Redis 가 아니라 컬럼</a></p>
