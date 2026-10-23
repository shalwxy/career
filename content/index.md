# Career Description

안녕하세요. 이승하입니다.

백엔드 엔지니어로 일하고 개발하는 시간을 가장 좋아합니다.

---

# Work Experience

---

## NEXON UNIVERSE

Backend Developer

2023. 11 ~

(재직 중, 2년 11개월 — 2026-10 기준)

## **Maplestory Universe**

넥슨유니버스 플랫폼개발팀

2023-11 ~

### Description

메이플스토리 IP를 기반으로 한 Web3 플랫폼인 메이플스토리 유니버스(MSU) 플랫폼을 개발합니다.

온체인 트랜잭션을 오프체인 상태와 동기화하는 DE(Data Engine) 서비스에서 시작해, 트랜잭션 이력·북마크·거래소 BFF·계정/결제·통합 알림·정책 서비스·데이터 파이프라인·운영 AI까지 33개 저장소(Go/Java/Helm/SQL)에 3,700여 건의 커밋을 기여했습니다. 신규 서비스를 바닥부터 설계해 라이브까지 올린 경험(api-bookmark, Swap&Warp, api-sentinel, 에러시로봇)과 분산 환경에서 데이터 정합성을 지키는 설계(선점·멱등·Outbox·CDC)가 주된 역할입니다.

각 시기의 프로젝트는 [Portfolio](portfolio.html)에서 문제 → 접근 → 결과로, 선택의 이유와 되돌린 결정은 [Design Decisions](decisions.html)에서 볼 수 있습니다.

### What did I do

1. 온체인-오프체인 동기화, DE(Data Engine) 서비스 — 2023-11 ~ 2024-04 · [자세히 →](portfolio.html#de)
    - 신규 코어 서비스(dapp-chunk) 연동 파사드 개발: 파사드 단 유효성 검사, converter 및 단위 테스트, gRPC 에러 래핑으로 코어 서비스 오염 차단
    - Saga v2 validator 체계 구축: 재화(neso/currency)·캐릭터·NFT 아이템 도메인별 검증기, 단건 반복 조회를 목록 조회로 전환해 호출 수 절감
    - 캐릭터 민트 시 닉네임 중복 생성 경합 해결: "존재 확인 후 생성" 대신 Redis 분산 락 기반 선점으로 전환하고 민트 성공 시에만 해제 — 이후 작업 전반의 "확인 대신 선점" 원칙
    - Helm 기반 배포 운영: 신규 서비스 롤아웃, DocumentDB 장애 재현용 임시 배포/롤백, test/qa 승격 전 dev 선행 배포 패턴 정립
2. 트랜잭션 이력·북마크 서비스 신설 및 거래소 연동 — 2024-06 ~ 2025-09 · [자세히 →](portfolio.html#activity)
    - 대용량 블록체인 트랜잭션 이력(원장) 적재/조회 서비스(api-activity)
        - 레이어 분리·서버/컨슈머 분리 등 구조 개선을 먼저 수행해, 이후 거래·민팅·전송·Swap/Warp·브릿지 인(Bridge-In)·USDT 스키마를 구조 변경 없이 추가하여 개발 기간 단축
        - transaction_hash 유니크 키 승격, 비정상 이벤트는 DB 적재 대신 DLQ, Kafka 순서 비보장 대응(nullable 설계), Redis NX + PostgreSQL advisory lock 으로 동시 적재 정합성 보장
        - DBA와의 긴밀한 협업을 통한 쿼리 튜닝(OR → UNION ALL), 커서 기반 무한 스크롤 전환, 조건부 캐싱(팀 공통 라이브러리 직접 개발 및 반영)으로 조회 성능 개선
        - 트랜잭션 결과 확정 시 외부에 공유하는 알림 이벤트 발행 구조 추가, Snowflake 적재를 Kafka 발행에서 CDC 로 전환해 유실 경로 제거
    - 북마크/조회수 서비스(api-bookmark) 신규 설계: 멱등 처리(중복 요청 성공, DB 저장 성공 시에만 카운트), Redis 카운트 캐시 → Kafka 이벤트 기반 집계 전환, 일일/총량 제한, 회원 탈퇴 연동
    - 거래소 웹 BFF(bff-marketplace): 북마크/액티비티 서비스 마이그레이션, 인벤토리 서비스 신설, 조회수 비동기화·캐릭터 이미지 렌더 병렬화. 원인 불명의 간헐적 pod 재시작 이슈를 로그 추적으로 비동기 루프 내 gRPC 자원 점유로 규명하고 timeout·chunk 호출로 근본 해결
    - 전사 proto 저장소(grpc) 도메인별 모듈화 및 공통 라이브러리(platform-lib) 마이그레이션을 플랫폼·거래소 서비스에 동시 적용
    - Swap & Warp(크로스체인 전송) 신규 도메인 설계: 데이터 모델·Kafka 컨슈머·실패 이벤트 처리·조회 BFF(bff-swapnwarp)
    - 확률 고지 서비스의 요구사항 분석, 버저닝 체계 설계 및 데이터 적재 완료
    - Java/Spring Kafka 컨슈머(sync-market-event)에 북마크 이벤트 적재 추가, 런칭 전 거래소 BFF 버그 픽스 집중 대응
    - 운영 효율화를 위한 백오피스 서비스 내 아이템/토큰 제재 기능(단건, 일괄, 대량 제재) 및 제재 이력 관리 시스템 구축
3. 계정·결제·통합 알림 서비스 — 2025-07 ~ 2026-08 · [자세히 →](portfolio.html#creditcard)
    - 월드페이(FraudSight 3DS) 신용카드 인증(0원 결제) 및 재인증 기능 개발: 벤더 응답 분기(400대는 outcome 코드, 500대는 에러), 일일 3회 제한을 Redis Lua 스크립트로 원자 처리, PCI 암호화·서킷 브레이커 도입, OTP 리셋용 재인증(신규 카드/기존 카드) 설계
    - 스테이블 코인(USDT) 도입: 온체인에 데이터가 기록되기 전 발생 가능한 리스크를 방지하기 위해 오프체인 단에서 선차감 및 롤백이 가능한 블록체인 지원 서비스(api-blockchain-supporter)를 재설계하고 롤백 토픽을 결과 확정 토픽으로 통합
    - MSU 통합 알림 서비스(SSE 기반): 계정 서비스에 위임하던 JWT 검증을 자체 흡수해 의존 제거, 서버 안정화를 위한 동시 구독 커넥션 수 제한, 알림 URL/타이틀 백엔드 생성, 백오피스 대량 수신자 처리를 gRPC streaming RPC(500건 청크·5만 건 상한)로 분리
    - Envoy 게이트웨이에 대한 gRPC 의존성을 제거하고 HTTP 통신 방식으로 전환하여 서비스 간 강한 결합도와 아키텍처적 종속성 제거
    - 글로벌 규제 대응을 위한 KYC 업체 변경(Argos → Sumsub)에 따른 대용량 데이터 마이그레이션 파이프라인 구축 (일정 준수를 위해 병렬 호출·재진입 가능한 커서·rate limiter 구조로 설계)
    - 게임 내 유저 데이터(무릉도원 층수)에 따른 디스코드 자동 뱃지 지급 봇 및 커뮤니티 공지 크롤링 봇 개발, 외부 side effect 는 Outbox(TxEvent) 재시도로 설계
    - 이메일 변경 후 보안 설정 변경 잠금(3차 보안): Redis TTL 방식에서 DB 컬럼 영속화로 전환, Primary 조회로 복제 지연 창 제거
4. 정책 서비스·데이터 파이프라인·운영 자동화 — 2026-01 ~ · [자세히 →](portfolio.html#sentinel)
    - 대용량 트래픽 제어 및 보안을 위한 비즈니스 정책 서비스(api-sentinel) 신설: 여러 서비스에 흩어져 있던 제어 로직을 단일 서비스로 통합
        - ACL: 지갑/IP 화이트·블랙리스트 통합 구현
        - Rate Limit: Sliding Window 및 Fixed Window 방식을 모두 도입하여 트래픽 제어의 유연성 확보, jitter 로 refresh 스파이크 완화
        - Lockout: 추후 타 서비스 확장성을 고려하여 실패 횟수의 보존/초기화 정책을 유연하게 설계
        - Feature Flag: 정책 활성화 플래그를 두어 런타임 중에도 실시간으로 정책 변경이 가능하도록 구현
    - PostgreSQL CDC → Kafka → Snowflake 데이터 파이프라인 구축: Debezium 커넥터, Stream/Task, replication slot keepalive 배치, 데이터가 있을 때만 실행되는 조건부 task 로 비용 최적화
    - 운영 AI "에러시로봇": Slack 에러 알림을 LLM 으로 1차 분석(GitLab 커밋 대조·OpenSearch 히스토리·escalation), LLM 모델 폐기 장애를 모델 교체·재시도/백오프·세마포어로 3일 내 대응
    - 운영 콘솔: 디스코드 메시지 재전송, SNS 권한 도메인 분리, 지갑주소↔SNS ID 조회 기능 추가

### Tech Stack

1. Golang (Uber FX, gRPC-Gateway, Watermill)
2. gRPC (unary / streaming, buf)
3. PostgreSQL (advisory lock, cursor pagination, CDC)
4. NoSQL (MongoDB, AWS DocumentDB)
5. Redis (분산 락, Lua, NX dedup)
6. Kafka (consumer group, DLQ, Debezium Connect)
7. Snowflake (Stream / Task)
8. Envoy (gRPC-JSON transcoding gateway)
9. Java / Spring Kafka
10. Gitlab CI, ArgoCD, HelmChart, Rundeck, Jenkins
11. AWS Cloud (EKS, MSK, KMS, S3)
12. Datadog, Jaeger
13. Vertex AI (LLM), OpenSearch

---

## UCLICK

AI Engineering R&D

2021. 01 ~
2023. 10

(1년 10개월)

## **NVIDIA Omniverse R&D**

유클릭 AI사업본부 AI서비스1팀

2022-06 ~ 2023-10

### Description

NVIDIA의 메타버스 제작 및 시뮬레이션 플랫폼인 Omniverse를 조사하고 Omniverse 애플리케이션에서 개발 및 프로젝트, PoC를 수행합니다.

NVIDIA의 Metaverse(Industrial Digital Twin) Solution인 Omniverse 플랫폼에서 Python을 이용해서 협동 로봇 프로젝트를 수행합니다.

### What did I do

1. NVIDIA Omniverse IsaacSim Application에서 로봇 조립 및 시뮬레이션
    
    — 과정에서 ROS 메시지 통신(Python) 이용
    
2. NVIDIA Omniverse CreateXR Application에서 VR 장비 연동 및 탐색
    
    — 과정에서 UnrealEngine4 기반의 VR 싱글 플레이 예제(C++) 개발
    

### Tech Stack

1. ROS
2. Python
3. NVIDIA Omniverse IsaacSim API
4. Communication
5. Presentation

---

## GC-GPU **솔루션 장애에 대한 원인 진단 및 해결**

유클릭 AI사업본부 AI서비스1팀

2022-04 ~ 2022-05

### Description

GPU를 이용한 학습 및 추론 솔루션(GPU를 여러 개로 분할해서 교육기관 내 다수의 학생이 각자의 계정과 이미지로 AI 학습 및 추론을 할 수 있도록 하는 플랫폼으로, 계정 관리 및 GPU를 포함한 자원을 모니터링하는 관리자 화면이 포함된 솔루션)에 대해 솔루션 소스를 보유하여 장애 발생 시 원인을 진단하고 해결합니다.

### What did I do

1. GC-GPU 솔루션 사용 서버의 커널 패닉 발생 관련 로그 분석
2. GC-GPU 솔루션 장애에 대해 환경과 소스 단에서 분석해서 해결

### Tech Stack

1. PHP (솔루션 소스 파일 분석)
2. Shell Script
3. Linux System

---

## **NVDIA GPU MIG 기능 지원**

유클릭 AI사업본부 AI서비스1팀

2022-03 ~ 2022-04

### Description

NVIDIA GPU를 분할해서 사용 가능한 MIG 기능을 지원합니다.

### What did I do

1. 신한 DS 개발 서버 및 운영 서버에 NVIDIA GPU MIG 기능을 현장 지원
2. 시스템 재부팅 후 MIG 프로필을 생성하는 Shell Script 제작 및 제공

### Tech Stack

1. **신한DS 개발 서버 및 운영 서버에 NVIDIA GPU MIG 기능 적용 지원**
2. **시스템 재부팅 후 MIG 프로필을 생성할 수 있도록 MIG 프로필 생성 쉘 스크립트 제작해서 제공**
1. NVIDIA GPU MIG
2. Shell Script
3. Kubernetes

---

## **NVIDIA deepops 기반 GPU 모니터링 솔루션 재구성**

유클릭 AI사업본부 AI서비스1팀

2022-01 ~ 2022-02

### Description

NVIDIA GPU를 사용하는 Kubernetes 및 Slurm 클러스터 용도 인프라 자동화 도구인 NVIDIA deepops(오픈소스)를 이용해서 GPU 모니터링 환경을 자동으로 구축하고, 폐쇄망 환경에서도 구축 가능하도록 패키지를 재구성합니다.

### What did I do

— 프로젝트 전체 담당

1. NVIDIA deepops 기반으로 한 GPU 모니터링 환경으로 Prometheus, Grafana를 Ansible을 이용해서 설치하고 가이드로 정리
2. 폐쇄망 환경에서 GPU 모니터링 환경을 구성하도록 Ansible 파일 분석을 통해 Shell Script를 만들고 이미지를 묶어서 패키지로 재구성

### Tech Stack

1. **NVIDIA 오픈 소스 deepops 기반으로 GPU 모니터링 테스트 및 가이드 정리**
2. **GPU 모니터링 시스템을 폐쇄망 상황에서도 구성 가능하도록 쉘 스크립트 및 패키지로 재구성**
1. Ansible
2. Shell Script
3. Prometheus
4. Grafana

---

## UCLICK

Backend Developer

2019. 11 ~

2021. 12

(2년)

## **UNO-GATEWAY**

유클릭 기술연구소 연구2실

2020-09 ~ 2021-12

### Description

동적 API를 생성, 수정 및 서비스할 수 있는 OPEN API 플랫폼입니다. 메시지 검증 및 변환, 인가/인증, 유량제어, 라우팅 등의 기능을 제공합니다.

### What did I do

1. 웹 소켓 기능 및 성능 현황 구현
2. Database 연계
    - Oracle Database
    - Mysql / MariaDB
    - Mssql
    - Tibero
    - PostgreSql
    - Db2
    - H2
3. 외부 시스템 연계
    - Elasticsearch
    - Hazelcast
    - Redis
4. 로드밸런싱 테스트
    - Ribbon
    - with Eureka / without Eureka
5. 통합 테스트 및 패키지 배포

### Tech Stack

1. Java
2. Spring Boot
3. Spring JPA
4. Ribbon with Eureka / without Eureka
5. Oracle Database
6. Mysql / MariaDB
7. Mssql
8. PostgreSql
9. Db2
10. Kafka
11. Elasticsearch / Kibana
12. Hazelcast
13. Redis

---

## **UNO-GATEWAY 신한금융투자 MDB 프로젝트**

유클릭 기술연구소 연구2실

2021-09 ~ 2021-10

### Description

개발자가 UNO-GATEWAY에 API 요청 시 해당 요청을 전문 데이터로 변환해 신한금융투자의 서버에 TCP 요청 후 신한금융투자에서 TCP 응답으로 주어지는 전문 데이터에 대해 다시 JSON 템플릿으로 변환해서 API 호출에 응답하는 프로젝트입니다.

### What did I do

— 프로젝트 전체 담당

1. 샘플 데이터 분석 및 요구 사항 명료화
2. 사용자 JSON과 MDB 서버의 전문 상호 변환 프로젝트 담당
3. 추가 요구 사항 수용: 관리 포인트를 EXCEL에서 QRY 파일 형식으로 변경

### Tech Stack

1. Java
2. Spring Boot

---

## **UNO-MSP**

유클릭 기술연구소 연구2실

2021-11 ~ 2021-12 (4차 고도화)

2021-02 ~ 2021-08 (3차 고도화)

2020-11 ~ 2021-01 (2차 고도화)

2020-02 ~ 2020-07 (1차 개발)

### Description

Oracle Cloud Infrastructure를 이용하는 고객사, 고객사 관리자를 대상으로 클라우드 자원과 정보, 자원 간 관계를 보여주는 대시보드와, 관리자가 직접 자원을 생성, 수정, 관리하는 페이지를 보유한 MSP(Managed Service Provider) 플랫폼입니다.

### What did I do

— 프로젝트 메인 개발

1. UNO-MSP 4차 고도화 (2021-11 ~ 2021-12)
    - Agent 및 UI 서버 이중화 구현
    - 리소스 이력 수집 기능 구현
    - ZENDESK 연동 및 티켓 발생 현황 기능 구현
    - JDBC를 이용한 DB 성능 모니터링 기능 구현
2. UNO-MSP 3차 고도화 (2021-02 ~ 2021-08)
    - 주어진 양식으로 SLACK, MAIL에 알림 전송 기능 구현
    - 주어진 양식으로 클라우드 월간 리포트 자동화 기능 구현
    - OCI 설정(알람, 규칙, 모니터)에 대한 OCI와 MSP 실시간 동기화 기능 구현
3. UNO-MSP 2차 고도화 (2020-11 ~ 2021-01)
    - MSP 자체 임계값 설정 및 알림(메일, 슬랙, 웹페이지 내 토스트) 구현
    - OCI 설정(알람, 규칙, 모니터)에 대한 MSP에서 생성/수정/삭제 구현
    - OCI 청구서 데이터 무결성 확인 및 보장
4. UNO-MSP 1차 개발 (2020-02 ~ 2020-07)
    - Oracle Cloud Infrastructure API 호출 통한 실시간 정보 수집
    - 대시보드(CPU, Memory, Disk, Network I/O 실시간 및 통계 정보)
    - 리소스 간 포함 관계를 데이터로 저장 후 Treemap 데이터로 표현
    - 클라우드 인스턴스에 대한 상태 검사(Health Check)
    - 클라우드 리소스별 청구 금액 표현 및 엑셀 다운로드

### Tech Stack

1. Java
2. Spring Boot
3. Spring JPA
4. MyBatis
5. PostgreSql
6. Hazelcast
7. Oracle Cloud Infrastructure API

---

## **LISTEN2ME-SURVEY**

유클릭 기술연구소 연구2실

2020.09 ~ 2020.10

### Description

규격 엑셀 시트를 설문조사 페이지로 변환하여 설문 URL링크를 제공하고, 관리자 화면에서는 설문조사 결과에 대한 통계를 대시보드로 보여주는 웹 애플리케이션입니다.

### What did I do

1. 백엔드와 프론트엔드 간 데이터 교환 형식 정의
2. 설문 결과 및 통계를 효과적으로 보여주는 대시보드 데이터 구성

### Tech Stack

1. Java
2. Spring Boot
3. Spring JPA
4. Oracle Database

---

# Other Experiences

---

## 한국방송통신대학교 컴퓨터과학과

2021.03 ~ 2024.02

좋은 개발자가 되기 위해서는 지식 및 소통 측면에서 컴퓨터 과학에 대한 이해가 필요하다고 생각해 입학했습니다. 컴퓨터과학과 전공 과목만 수강하였으며, 전산 기초인 디지털논리회로, 컴퓨터구조, 운영체제, 컴파일러구성, 자료구조, 알고리즘, 데이터베이스 과목과 프로그래밍 언어인 C프로그래밍, C++프로그래밍, Java 프로그래밍, 모바일앱프로그래밍, JSP프로그래밍 과목과 그 외에도 개발에 필요한 과목인 컴퓨터보안, 클라우드컴퓨팅, 시뮬레이션 등을 수강했고, 언급한 과목들 모두 A+을 취득했습니다.

그 외에도 학습한 것을 연계해서 학교 시험 뿐 아니라 자격 시험에 응시하는 것도 피드백이 된다고 생각해서 실천한 결과로, 정보처리기사, 정보보안기사, 리눅스마스터 1/2급, 네트워크관리사 1/2급, SQLD를 취득했습니다.

---

## 한국폴리텍대학교 융합기술교육원 데이터융합 소프트웨어학과

2019.03 ~ 2019.11

Java, Spring Framework, Python, R, Linux, Database, 웹 프로그래밍 등을 실무 중심으로 배웠습니다. Python TensorFlow를 이용해서 공부 시간과 시험 성적에 대한 데이터를 학습시키고, 새 데이터의 시험 성적을 추측했습니다. Oracle SQL 및 ODBC를 활용해서 대용량의 고객 데이터를 관찰하여 의미 있는 마케팅 정보(신규회원의 유입 통계)를 추출하는 SQL(그룹화 및 조건 적용하는 SQL)을 작성하고, Oracle 데이터베이스와 R, Excel을 연동하여 시각화했습니다. JSP와 Open API를 이용해서 Data Parsing(날씨 정보는 xml, 환율 정보는 json으로 수행)해서 페이지로 제시했는데, 이때 날씨 조회의 경우 csv 파일을 이용하여 특정 지역 날씨 조회 기능을 추가했고, 환율 정보의 경우 chart.js을 통해서 그래프로 제시한 바 있습니다. JSP를 이용해서 달력 형태의 예약 페이지를 만들고, 관리자로 로그인하는 경우 세션에 로그인 확인 여부를 저장하고, 예약 상황을 수정 및 삭제 가능하도록 구현했습니다. Java를 이용해 MVC에 기반한 클래스(DAO, Domain, DTO, Service, UI)를 생성하고 Database와 연결하여 CRUD를 구현했으며 정산 결과 및 소비 패턴을 분석하고 통계 내서 사용자에게 보여주는 가계부를 구현했습니다. 끝으로, Linux Ubuntu 환경에서 서버의 CPU, MEMORY, DISK 상황을 실시간 조회하고 결과를 HTML에 삽입하여 실시간으로 새로고침하는 모니터링 웹페이지를 구현했습니다.

---

## 이화여자대학교 수학교육과

2011.03 ~ 2016.02

전공수학으로 미분적분학, 선형대수학, 기하학, 확률과 통계, 해석학, 위상수학, 정수론, 현대대수학 등을 학습했습니다. 구체적으로는, 미분을 이용해서 n 차원의 주어진 범위 내에서 함수의 최솟값과 최댓값을 구했고, 선형대수학을 활용해서 빠른 연산이 가능하도록 기저를 변환하여 효과적인 행렬 연산을 수행했습니다. 기하학을 사용해서는 도형과 그 성질들 간 상호 관계를 체계적으로 정리했고, 해석학을 통해서 실함수를 분석했습니다. 위상수학으로 형태는 달라도 구조가 같은 기하학적 성질을 다루었고, 정수론을 이용해서 정수 조건의 문제를 빠르게 해결했습니다. 현대대수학에서는 구조를 최대한 추상화해서 수학의 영역을 확장했습니다.

---

# Skills

---

## Backend Development

- **Golang 기반 개발과 리팩토링:** Go 언어의 고루틴과 채널을 활용한 동시성 처리에 능숙합니다. 복잡한 코드를 그대로 두지 않고, 인터페이스를 활용해 기능을 작은 단위로 쪼개고 결합도를 낮추는 리팩토링을 꾸준히 해왔습니다.
- **데이터 설계 및 최적화:** 대용량 트래픽이나 동시 요청 상황에서도 데이터가 꼬이지 않도록 PostgreSQL advisory lock, Redis 분산 락·Lua 원자 처리, 멱등 설계를 활용한 설계와 최적화에 적극적입니다.
- **실패 경로 우선 설계:** 선차감·롤백, Outbox(TxEvent) 재시도, DLQ, CDC 처럼 "잘못됐을 때 어떻게 복구할지"를 먼저 설계합니다. 큰 기능이 기획 변경으로 롤백되어도, 그 과정에서 발견한 결함 수정은 남겨 가치를 보존합니다.
- **유연한 API 설계:** 새로운 가이드나 외부 API 문서를 분석해 서비스에 녹이는 것을 좋아하며, 나중에 다른 시스템(로봇이나 외부 서비스)이 붙더라도 유연하게 확장할 수 있는 구조를 고민하며 개발합니다.

## Logging / Debugging

- **의미 있는 로그 남기기:** 장애가 터졌을 때만 로그를 보는 게 아니라, 개발·운영 단계에서 필요한 위치에 로그를 꼼꼼히 남기고 주기적으로 모니터링합니다.
- **가설 기반의 빠른 디버깅:** 문제가 발생하면 무작정 코드부터 보지 않고, 에러가 발생한 환경과 맥락을 먼저 파악합니다. 원인을 추측하고 범위를 좁혀가며 근본적인 문제를 빠르게 잡아냅니다.

## Communication

- **요구사항 명료화:** 모호한 기획이나 요구사항을 개발자 관점에서 명확하게 정리하는 것을 좋아합니다. 풀고자 하는 문제를 확실히 정의하고 구현에 들어갑니다.
- **시각화를 통한 수평적 소통:** 제 생각을 글이나 그림(다이어그램)으로 정리해서 공유합니다. 동료들과 의견을 주고받을 때 고집 부리지 않고 더 좋은 방향이 있다면 능동적으로 수용합니다.
- **선제적인 리스크 관리:** 이슈가 생길 만한 부분을 미리 예측하고 방어적인 코드를 짜거나 대비책을 세워둡니다. 필요할 때 바로바로 대응할 수 있는 상태를 유지하는 것을 선호합니다.
- **리뷰 지적을 원칙으로:** 결제·보안 기능은 리뷰 2회차까지 돌리고, 지적받은 내용("외부 호출은 log-and-swallow 금지", "설정은 부팅 시 주입")은 팀 원칙으로 문서화해 다음 작업에 반영합니다.

---