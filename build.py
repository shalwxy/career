#!/usr/bin/env python3
"""content/*.md → docs/*.html. 의존성: pip install markdown"""
import datetime
import html
import pathlib
import sys

try:
    import markdown
    from markdown.extensions.toc import TocExtension, slugify_unicode
except ImportError:
    sys.exit("python3 -m pip install --user markdown 를 먼저 실행하세요")

ROOT = pathlib.Path(__file__).parent
CONTENT = ROOT / "content"
OUT_DIR = ROOT / "docs"

CONFIG = {
    "name": "이승하",
    "title": "Backend Engineer · Go / gRPC / Kafka / PostgreSQL",
    "links": {                # 값이 비어 있으면 숨김
        "Email": "",          # "mailto:you@example.com"
        "GitHub": "",         # "https://github.com/your-id"
        "LinkedIn": "",
    },
    "lang": "ko",
    # 상단 내비 순서. (파일 stem, 라벨, 긴 페이지면 사이드 목차 표시)
    "pages": [
        ("index", "Career", False),
        ("portfolio", "Portfolio", True),
        ("decisions", "Design Decisions", True),
    ],
}

CSS = """
:root{--bg:#fff;--fg:#1f2328;--muted:#656d76;--line:#d0d7de;--accent:#0969da;--soft:#f6f8fa;--max:1100px;--col:760px}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#e6edf3;--muted:#8d96a0;--line:#30363d;--accent:#4493f8;--soft:#161b22}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;scroll-padding-top:72px}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.7 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo",Pretendard,"Noto Sans KR","Segoe UI",Roboto,Helvetica,Arial,sans-serif;word-break:keep-all}
a{color:var(--accent)}
.topbar{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.topbar .in{max-width:var(--max);margin:0 auto;padding:10px 20px;display:flex;align-items:center;gap:20px;flex-wrap:wrap}
.topbar .brand{font-weight:700;text-decoration:none;color:var(--fg)}
.topbar nav{display:flex;gap:4px;flex-wrap:wrap}
.topbar nav a{padding:6px 10px;border-radius:6px;text-decoration:none;color:var(--muted);font-size:.95rem}
.topbar nav a:hover{background:var(--soft);color:var(--fg)}
.topbar nav a.on{color:var(--fg);background:var(--soft);font-weight:600}
.topbar .ext{margin-left:auto;display:flex;gap:12px}
.topbar .ext a{font-size:.9rem;text-decoration:none}
.hero{border-bottom:1px solid var(--line);background:var(--soft)}
.hero .in{max-width:var(--max);margin:0 auto;padding:36px 20px 28px}
.hero h1{margin:0 0 4px;font-size:2rem;letter-spacing:-.01em}
.hero p{margin:0;color:var(--muted);font-size:1.05rem}
.wrap{max-width:var(--max);margin:0 auto;padding:24px 20px 56px;display:grid;grid-template-columns:minmax(0,var(--col)) 1fr;gap:40px}
.wrap.solo{grid-template-columns:minmax(0,var(--col))}
article>h1{font-size:1.55rem;margin:2em 0 .6em;padding-bottom:.3em;border-bottom:1px solid var(--line)}
article>h1:first-child{margin-top:.2em}
article h2{font-size:1.28rem;margin:1.9em 0 .5em;scroll-margin-top:72px}
article h3{font-size:1.02rem;margin:1.4em 0 .3em;color:var(--muted);letter-spacing:.02em}
article p{margin:.5em 0}article hr{border:0;border-top:1px solid var(--line);margin:1.6em 0}
article ul,article ol{padding-left:1.4em;margin:.4em 0}article li{margin:.18em 0}article li>ul,article li>ol{margin:.15em 0 .3em}
article code{background:var(--soft);padding:.1em .35em;border-radius:4px;font-size:.92em}
article pre{background:var(--soft);padding:12px 14px;border-radius:8px;overflow:auto;font-size:.88em;line-height:1.5}
article pre code{background:none;padding:0}
article table{border-collapse:collapse;width:100%;margin:.8em 0;font-size:.95em;display:block;overflow-x:auto}
article th,article td{border:1px solid var(--line);padding:6px 10px;text-align:left;vertical-align:top}
article th{background:var(--soft)}
article blockquote{margin:.8em 0;padding:.2em 1em;border-left:3px solid var(--line);color:var(--muted)}
article .more{font-size:.9rem;color:var(--muted)}
article .tag{display:inline-block;font-size:.78rem;padding:1px 8px;border:1px solid var(--line);border-radius:999px;color:var(--muted);margin-left:6px;vertical-align:middle}
aside.toc{position:sticky;top:72px;align-self:start;max-height:calc(100vh - 90px);overflow:auto;font-size:.88rem;border-left:1px solid var(--line);padding-left:16px}
aside.toc .t{font-weight:600;margin:0 0 8px;color:var(--muted);font-size:.8rem;letter-spacing:.06em;text-transform:uppercase}
aside.toc ul{list-style:none;margin:0;padding:0}aside.toc li{margin:4px 0}
aside.toc ul ul{padding-left:12px}aside.toc a{color:var(--muted);text-decoration:none}aside.toc a:hover{color:var(--fg)}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:.85rem}
footer .in{max-width:var(--max);margin:0 auto;padding:18px 20px 40px}
@media(max-width:960px){.wrap{grid-template-columns:minmax(0,1fr)}aside.toc{display:none}}
@media print{:root{--bg:#fff;--fg:#000;--muted:#444;--line:#bbb;--accent:#000;--soft:#fff}
body{font-size:11pt;line-height:1.45}.topbar,aside.toc,footer,.more{display:none}
.hero{background:none;border:0}.hero .in,.wrap{padding:0}.wrap{display:block}
article>h1{margin-top:1.4em;page-break-after:avoid}article h2,article h3{page-break-after:avoid}article li,article p{page-break-inside:avoid}a{text-decoration:none}}
"""

PAGE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page_title} — {name}</title>
<meta name="description" content="{name} · {title}">
<style>{css}</style>
</head>
<body>
<div class="topbar"><div class="in">
<a class="brand" href="index.html">{name}</a>
<nav>{nav}</nav>
<div class="ext">{links}</div>
</div></div>
{hero}
<div class="wrap{solo}">
<article>
{body}
</article>
{toc}
</div>
<footer><div class="in">Last updated {updated} · 이 페이지는 공개용으로 정제된 요약이며, 사내 식별자·운영 정보는 포함하지 않습니다.</div></footer>
</body>
</html>
"""


def nav_html(current: str) -> str:
    return "".join(
        f'<a href="{stem}.html"{" class=on" if stem == current else ""}>{html.escape(label)}</a>'
        for stem, label, _ in CONFIG["pages"]
    )


def links_html() -> str:
    return "".join(
        f'<a href="{html.escape(href)}" rel="me noopener">{html.escape(label)}</a>'
        for label, href in CONFIG["links"].items() if href
    )


def toc_html(tokens, depth=2) -> str:
    def walk(items, level):
        if not items or level > depth:
            return ""
        lis = []
        for it in items:
            sub = walk(it.get("children", []), level + 1)
            lis.append(f'<li><a href="#{it["id"]}">{html.escape(it["name"])}</a>{sub}</li>')
        return "<ul>" + "".join(lis) + "</ul>"
    return walk(tokens, 1)


def build_page(stem: str, label: str, with_toc: bool) -> None:
    src = CONTENT / f"{stem}.md"
    md = markdown.Markdown(
        extensions=["extra", "sane_lists", "smarty", "attr_list",
                    TocExtension(slugify=slugify_unicode, toc_depth="1-3", permalink=False)],
        output_format="html5",
    )
    body = md.convert(src.read_text(encoding="utf-8"))
    toc = ""
    if with_toc:
        toc = f'<aside class="toc"><p class="t">On this page</p>{toc_html(md.toc_tokens, depth=2)}</aside>'
    hero = ""
    if stem == "index":
        hero = (f'<div class="hero"><div class="in"><h1>{html.escape(CONFIG["name"])}</h1>'
                f'<p>{html.escape(CONFIG["title"])}</p></div></div>')
    page = PAGE.format(
        lang=CONFIG["lang"], name=html.escape(CONFIG["name"]), title=html.escape(CONFIG["title"]),
        page_title=html.escape(label), css=CSS, nav=nav_html(stem), links=links_html(),
        hero=hero, solo="" if with_toc else " solo", body=body, toc=toc,
        updated=datetime.date.today().isoformat(),
    )
    out = OUT_DIR / f"{stem}.html"
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(page.encode()):,} bytes)")


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / ".nojekyll").touch()
    for stem, label, with_toc in CONFIG["pages"]:
        build_page(stem, label, with_toc)


if __name__ == "__main__":
    main()
