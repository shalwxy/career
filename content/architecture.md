# Architecture

> 제가 일한 플랫폼의 전체 구조와, 그 안에서 제가 담당한 영역입니다. 내부 문서(워크플로우 총람 3종)를 바탕으로 **공개 가능한 수준으로 정제**했습니다 — 서비스 이름과 데이터 흐름만 있고, 호스트·포트·테이블·토픽명·저장소 경로는 없습니다.

## 전체 지형 {#landscape}

플랫폼은 세 그룹으로 나뉩니다. **DE(Data Engine)** 가 온체인 트랜잭션을 오프체인 상태와 동기화하고, **거래소 도메인**이 그 상태 위에서 거래·검색·게임데이터를 제공하며, **portal 플랫폼**이 계정·결제·알림·정책·트랜잭션 이력을 담당합니다. 외부 개발자용 **Synergy** 는 portal 의 계정·OAuth 를 사용합니다.

<div class="diagram">
<p class="dg-title">그룹 간 연결 — 굵은 테두리가 제가 담당한 서비스</p>
<div class="dg-flow">
<div class="dg-box"><b>DE — 온체인 동기화</b><small>business-provider (gRPC 파사드)<br/>saga-provider (Saga 실행) ★<br/>event-service (상태 저장) ★<br/>analyzer 워커들</small></div>
<span class="dg-arrow">→</span>
<div class="dg-box"><b>거래소 도메인</b><small>exchange (거래)<br/>api-gamedata (게임데이터)<br/>api-search · api-avatar<br/>bff-marketplace ★ · bff-navigator ★</small></div>
<span class="dg-arrow">→</span>
<div class="dg-box dg-accent"><b>portal 플랫폼</b><small>api-account ★ · api-activity ★<br/>api-bookmark ★ · api-notification ★<br/>api-sentinel ★ · api-blockchain-supporter ★<br/>BFF 3종 ★ · marina 게이트웨이 ★</small></div>
<span class="dg-arrow">→</span>
<div class="dg-box"><b>Synergy (외부 개발자)</b><small>devcenter<br/>msu-arcade</small></div>
</div>
<p class="dg-note">★ = 제가 메인 담당 또는 과반 기여한 서비스. 모든 외부 요청은 marina(Envoy) 를 지나며 JWT 검증 후 지갑 주소 헤더가 주입됩니다 — 모든 BFF 와 Synergy 가 이 헤더를 신뢰합니다.</p>
</div>

## 데이터 흐름 — 트랜잭션 한 건의 여정 {#flow}

사용자가 거래소에서 아이템을 구매하면 아래 순서로 세 그룹을 지나갑니다. 제가 만든 부분은 ③~⑤입니다.

<div class="diagram">
<p class="dg-title">거래 체결 → 이력 · 알림 · 검색 · 분석</p>
<div class="dg-flow">
<div class="dg-box"><b>① exchange</b><small>주문 검증 → 선차감<br/>DE 에 Lock 요청</small></div>
<span class="dg-arrow">→</span>
<div class="dg-box"><b>② 블록체인</b><small>트랜잭션 제출<br/>결과 이벤트</small></div>
<span class="dg-arrow">→</span>
<div class="dg-box"><b>DE analyzer</b><small>체인 결과를 도메인 이벤트로 정규화<br/>Saga 로 상태 반영</small></div>
<span class="dg-arrow">→</span>
<div class="dg-box dg-accent"><b>③ api-activity ★</b><small>거래 이벤트 소비 → 이력 적재<br/>NX + advisory lock 으로 중복 차단</small></div>
<span class="dg-arrow">→</span>
<div class="dg-box dg-accent"><b>④ api-notification ★</b><small>결과 확정 이벤트 → 알림 생성<br/>SSE 로 실시간 푸시</small></div>
</div>
<p class="dg-note">같은 거래 이벤트를 api-search(검색 인덱스)·분석 적재 컨슈머(⑤, Java)도 각자 소비합니다 — 한 토픽, 네 소비자. api-bookmark ★ 는 북마크/조회수 이벤트를 발행하고, portal DB 변경은 CDC ★ 로 분석 저장소에 실시간 반영됩니다.</p>
</div>

## 제가 담당한 portal 서비스 간 의존 {#portal}

<div class="diagram">
<p class="dg-title">호출 관계 — 화살표 방향이 호출</p>
<div class="dg-flow">
<div class="dg-box"><b>BFF (msu-web · swapnwarp · marketplace · navigator)</b><small>프론트별 조합 레이어<br/>DB 직결 없음</small></div>
<span class="dg-arrow">→</span>
<div class="dg-box dg-accent"><b>api-account</b><small>허브 — 13개 호출자<br/>JWT · KYC · 신용카드 · 제재 · MFA</small></div>
<span class="dg-arrow">→</span>
<div class="dg-box dg-accent"><b>api-sentinel</b><small>리프 — 아무것도 호출 안 함<br/>rate limit · ACL · flag · lockout</small></div>
</div>
<div class="dg-flow" style="margin-top:8px">
<div class="dg-box"><b>api-blockchain-supporter</b><small>출금/전송 가드레일<br/>→ account · sentinel</small></div>
<span class="dg-arrow">·</span>
<div class="dg-box"><b>api-activity · api-bookmark</b><small>이력 · 북마크<br/>→ gamedata</small></div>
<span class="dg-arrow">·</span>
<div class="dg-box"><b>api-notification</b><small>알림<br/>→ account · bookmark · exchange</small></div>
</div>
<p class="dg-note">설계 원칙: 정책은 sentinel 이 단일 소유자(다른 서비스는 조회만) · 외부 side effect 는 Outbox 로 재시도 · 데이터 파이프라인에는 서비스가 직접 쓰지 않음(CDC) · 조회 서버와 Kafka 컨슈머는 별도 바이너리.</p>
</div>

## 공통 패턴 {#patterns}

세 그룹에 걸쳐 제가 만들거나 지킨 패턴입니다. 자세한 이유는 [Design Decisions](decisions.html) 에.

| 패턴 | 적용한 곳 | 왜 |
|---|---|---|
| **확인 대신 선점** | DE 닉네임 Redis 락 → api-activity Redis NX → 신용카드 일일 한도 Lua | "존재 확인 후 생성" 은 확인과 생성 사이에 경합 창이 있다 |
| **요청/결과 동시 적재 잠금** | api-activity Swap & Warp (PostgreSQL advisory lock, 키 2개) | Kafka 메시지 순서 비보장 + 재시도 |
| **선차감 → 결과 확정 토픽** | api-blockchain-supporter (USDT 도입) | 롤백 토픽을 따로 두면 순서·중복 처리가 두 배 |
| **Outbox 재시도** | api-account (디스코드 역할 부여 등 외부 호출) | "배치가 나중에 주워 담는다" 는 복구 설계가 아니다 |
| **서비스 밖으로 적재** | 배치 → publish 제거 → CDC (Debezium → Snowflake) | 커밋 후 publish 실패 유실 경로 제거 |
| **정책은 enum/설정** | 출금 자격 검사 check_type · 토큰 종류 · 시간 정책 | 정책은 바뀐다 — 왕복이 커밋이 되면 안 된다 |
| **큰 응답은 스트리밍 + 수신 규약** | api-notification 대량 수신자 (500건 청크) | 쪼개는 것보다 수신측 조립 규약이 핵심 |

## 같은 이름, 다른 것 (문서화해 둔 함정) {#traps}

인수인계 문서에 남긴 것 중 공개해도 되는 항목입니다 — 팀에 들어온 사람이 처음 헷갈리는 지점을 미리 적어 두는 습관의 예시입니다.

- **whale** — DE 에서는 ① Kafka 워커 유형 ② 공통 라이브러리의 헬스체커 ③ FlowEngine 저장소 이름, 세 가지 다른 뜻으로 쓰입니다.
- **settlement** — DE 의 수불부 서비스와 리액터 보상 정산 워커는 다른 것입니다.
- **synergy 폴더** — 로컬 폴더 이름과 GitLab 그룹이 일치하지 않아, 7개 저장소는 실제로는 portal 과 같은 그룹입니다.
- **이벤트 producer 이중 경로** — 같은 이벤트 토픽 설정이 신형(saga emit)과 구형(FlowEngine) 양쪽에 남아 있어 이중 발행 여부를 운영에서 확인해야 합니다.
