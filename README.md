# career

Career Description · Portfolio · Design Decisions 를 정적 HTML 로 발행하는 저장소.

```
content/index.md      Career Description (원고)
content/portfolio.md  프로젝트별 상세 (공개용 정제본)
content/decisions.md  설계 결정 기록 (공개용 정제본)
content/diagrams/*.mmd 본문 용어 클릭 시 모달로 뜨는 mermaid 도식 (내가 만든 부분만)
build.py              content/*.md → docs/*.html
docs/                 발행 결과물 (GitHub Pages 가 서빙)
```

## 수정 → 발행

```bash
# 최초 1회
python3 -m pip install --user markdown

# 1. 원고 수정 (content/*.md)
# 2. 빌드
python3 build.py
# 3. 로컬 확인
open docs/index.html
# 4. 커밋 · 푸시
git add content docs
git commit -m "update resume"
git push
```

이름 · 직함 · 상단 링크(Email/GitHub/LinkedIn) 는 `build.py` 의 `CONFIG` 에서 바꾼다. 빈 값은 표시하지 않는다.
페이지 추가는 `content/<name>.md` 를 만들고 `CONFIG["pages"]` 에 등록한다. 제목에 `{#id}` 를 붙이면 다른 페이지에서 `page.html#id` 로 링크할 수 있다.
도식은 `content/diagrams/<id>.mmd` 를 만들고 본문에서 `[용어](#dg:<id>)` 로 걸면 클릭 시 모달에 그려진다(mermaid 는 첫 클릭 때 CDN 에서 지연 로드). `page.html#dg:<id>` 로 열면 바로 뜬다.

## GitHub Pages (최초 1회)

1. GitHub 에 **public** 저장소 `career` 생성 (README 없이 빈 저장소)
2. 로컬에서 `git remote add origin git@github.com:<id>/career.git && git push -u origin main`
3. 저장소 Settings → Pages → Source **Deploy from a branch** → Branch **main**, 폴더 **/docs** → Save
4. 1~2분 뒤 `https://<id>.github.io/career/`

## 공개 전 체크

- 커밋 author 는 개인 이메일: `git config user.email "<개인 이메일>"` (이 저장소에만 적용)
- `content/` 에 사내 호스트명·IP·테이블명·티켓 번호·시크릿 위치 같은 내부 식별자가 없는지 확인
- 워크플로우 총람·인수인계서 류 내부 문서는 이 저장소에 넣지 않는다
