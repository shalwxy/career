# Seungha Lee (이승하) — Backend / DevOps Engineer

**🔗 https://shalwxy.github.io/resume/**

Go 백엔드 3년 — 결제·알림·트랜잭션 이력·데이터 파이프라인, 분산 환경에서의 데이터 정합성. 담당 서비스의 CI/CD·Kubernetes 매니페스트·게이트웨이·DB DDL 운영까지 다뤘습니다.

| 페이지 | 내용 |
|---|---|
| [Career](https://shalwxy.github.io/resume/) | 경력기술서 (KR / [EN](https://shalwxy.github.io/resume/index.en.html)) |
| [Portfolio](https://shalwxy.github.io/resume/portfolio.html) | 프로젝트별 문제 → 접근 → 결과 |
| [Design Decisions](https://shalwxy.github.io/resume/decisions.html) | 선택의 이유와 되돌린 결정 |

본문의 밑줄 친 용어를 누르면 흐름 도식(mermaid)이 창으로 열립니다.

연락: [Email](mailto:shalwxy@gmail.com) · [LinkedIn](https://www.linkedin.com/in/seungha-lee-2aa442229) · [Blog](https://shalwxy.github.io/)

공개용으로 정제한 요약이며 사내 식별자와 운영 정보는 포함하지 않습니다.

---

<details>
<summary>이 사이트의 구성과 발행 방법</summary>

```
content/index.md, index.en.md   Career Description (KR / EN)
content/portfolio.md            프로젝트별 상세
content/decisions.md            설계 결정 기록
content/diagrams/*.mmd          본문 용어 클릭 시 모달로 뜨는 mermaid 도식 (*.en.mmd 는 영문)
build.py                        content/*.md → docs/*.html
docs/                           발행 결과물 (GitHub Pages 가 서빙)
```

```bash
python3 -m pip install --user markdown   # 최초 1회
python3 build.py                         # 빌드
open docs/index.html                     # 로컬 확인
git add content docs && git commit -m "update" && git push
```

- 이름·직함·상단 링크는 `build.py` 의 `CONFIG` 에서 바꿉니다.
- 도식은 `content/diagrams/<id>.mmd` 를 만들고 본문에서 `[용어](#dg:<id>)` 로 겁니다. mermaid 는 첫 클릭 때 CDN 에서 불러옵니다.
- Pages: Settings → Pages → Deploy from a branch → `main` / `/docs`.

</details>
