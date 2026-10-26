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
    "name_en": "Seungha Lee",
    "title": "Backend Engineer · Go / gRPC / Kafka / PostgreSQL",
    "links": {                # 값이 비어 있으면 숨김. 상단 바와 푸터에 표시
        "Email": "mailto:shalwxy@gmail.com",
        "GitHub": "https://github.com/shalwxy",
        "LinkedIn": "https://www.linkedin.com/in/seungha-lee-2aa442229",
        "Blog": "https://shalwxy.github.io/",
    },
    # (파일 stem, KR 라벨, EN 라벨, 사이드 목차 표시)
    "pages": [
        ("index", "Career", "Career", True),
        ("portfolio", "Portfolio", "Portfolio", True),
        ("architecture", "Architecture", "Architecture", True),
        ("decisions", "Design Decisions", "Design Decisions", True),
    ],
}

CSS = """
:root{--bg:#fff;--fg:#1f2328;--muted:#656d76;--line:#d0d7de;--accent:#0969da;--soft:#f6f8fa;--max:1100px;--col:760px}
@media(prefers-color-scheme:dark){:root{--bg:#0d1117;--fg:#e6edf3;--muted:#8d96a0;--line:#30363d;--accent:#4493f8;--soft:#161b22}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;scroll-padding-top:76px}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.7 -apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo",Pretendard,"Noto Sans KR","Segoe UI",Roboto,Helvetica,Arial,sans-serif;word-break:keep-all}
a{color:var(--accent)}
.topbar{position:sticky;top:0;z-index:20;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.topbar .in{max-width:var(--max);margin:0 auto;padding:10px 20px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.topbar .brand{font-weight:700;text-decoration:none;color:var(--fg)}
.topbar nav{display:flex;gap:4px;flex-wrap:wrap}
.topbar nav a{padding:6px 10px;border-radius:6px;text-decoration:none;color:var(--muted);font-size:.95rem}
.topbar nav a:hover{background:var(--soft);color:var(--fg)}
.topbar nav a.on{color:var(--fg);background:var(--soft);font-weight:600}
.topbar .ext{margin-left:auto;display:flex;gap:10px;align-items:center}
.topbar .ext a{font-size:.88rem;text-decoration:none}
.lang{display:inline-flex;border:1px solid var(--line);border-radius:999px;overflow:hidden;font-size:.78rem}
.lang a,.lang span{padding:3px 9px;text-decoration:none;color:var(--muted)}
.lang .on{background:var(--accent);color:#fff;font-weight:600}
.lang span.off{opacity:.45;cursor:not-allowed}
.toc-btn{display:none;position:fixed;right:16px;bottom:16px;z-index:30;width:46px;height:46px;border-radius:50%;border:1px solid var(--line);background:var(--bg);color:var(--fg);box-shadow:0 4px 14px rgba(0,0,0,.18);cursor:pointer;font-size:1.1rem}
.hero{border-bottom:1px solid var(--line);background:var(--soft)}
.hero .in{max-width:var(--max);margin:0 auto;padding:36px 20px 28px}
.hero h1{margin:0 0 4px;font-size:2rem;letter-spacing:-.01em}
.hero p{margin:0;color:var(--muted);font-size:1.05rem}
.wrap{max-width:var(--max);margin:0 auto;padding:24px 20px 56px;display:grid;grid-template-columns:minmax(0,var(--col)) 1fr;gap:40px}
.wrap.solo{grid-template-columns:minmax(0,var(--col))}
article>h1{font-size:1.55rem;margin:2em 0 .6em;padding-bottom:.3em;border-bottom:1px solid var(--line)}
article>h1:first-child{margin-top:.2em}
article h2{font-size:1.28rem;margin:1.9em 0 .5em;scroll-margin-top:76px}
article h3{font-size:1.06rem;margin:1.8em 0 .3em;color:var(--fg);display:flex;align-items:center;gap:10px;scroll-margin-top:76px}
article h4{font-size:1.02rem;margin:1.5em 0 .3em;color:var(--fg);display:flex;align-items:center;gap:10px;scroll-margin-top:76px}
article h4.sub,article h3+h4{color:var(--muted);font-size:.9rem;letter-spacing:.04em;text-transform:uppercase;margin-top:1.1em}
article p{margin:.5em 0}article hr{border:0;border-top:1px solid var(--line);margin:1.8em 0}
article ul,article ol{padding-left:1.4em;margin:.4em 0}article li{margin:.22em 0}article li>ul,article li>ol{margin:.15em 0 .3em}
article code{background:var(--soft);padding:.1em .35em;border-radius:4px;font-size:.92em}
article pre{background:var(--soft);padding:12px 14px;border-radius:8px;overflow:auto;font-size:.88em;line-height:1.5}
article pre code{background:none;padding:0}
article table{border-collapse:collapse;width:100%;margin:.8em 0;font-size:.95em;display:block;overflow-x:auto}
article th,article td{border:1px solid var(--line);padding:6px 10px;text-align:left;vertical-align:top}
article th{background:var(--soft)}
article table.certs{display:table;font-size:.93em}article table.certs td:last-child,article table.certs th:last-child{white-space:nowrap}
article blockquote{background:color-mix(in srgb,var(--accent) 8%,var(--soft));border-left:3px solid var(--accent);color:var(--fg);padding:.6em 1em;margin:1em 0;border-radius:0 6px 6px 0}
article .more{font-size:.9rem;color:var(--muted)}
article .tag{display:inline-block;font-size:.78rem;padding:1px 8px;border:1px solid var(--line);border-radius:999px;color:var(--muted);margin:0 6px 4px 0;vertical-align:middle}
article .meta{color:var(--muted);font-size:.95rem;margin:-.4em 0 1.2em;padding-bottom:1em;border-bottom:1px solid var(--line)}
article .period{color:var(--muted);font-size:.9rem;margin:-.1em 0 .4em}
article .period a{text-decoration:none;font-weight:500}article .period a:hover{text-decoration:underline}
article .phase{display:inline-flex;align-items:center;justify-content:center;width:26px;height:26px;border-radius:50%;background:var(--accent);color:#fff;font-size:.82rem;font-weight:700;flex-shrink:0}
article .stack{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:.8em 0;font-size:.95rem}
article .stack p{margin:.35em 0}
article .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:1.2em 0}
article .stats>div{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:14px 10px;text-align:center}
article .stats strong{display:block;font-size:1.4rem;color:var(--fg);line-height:1.1;margin-bottom:4px}
article .stats span{display:block;font-size:.78rem;color:var(--muted);line-height:1.3}
article .badges,article .chips{margin:1em 0 1.2em;line-height:2}
article .chips{margin:.1em 0 .6em}
article .b,article .chip{display:inline-block;padding:2px 10px;border-radius:999px;font-size:.8rem;border:1px solid var(--line);background:var(--soft);color:var(--fg);margin:0 2px 2px 0}
article .chip{font-size:.74rem;color:var(--muted);padding:1px 9px}
article .b-go{background:color-mix(in srgb,var(--accent) 15%,var(--soft));border-color:color-mix(in srgb,var(--accent) 40%,var(--line));color:var(--accent);font-weight:600}
article .impact{background:color-mix(in srgb,var(--accent) 7%,var(--bg));border:1px solid color-mix(in srgb,var(--accent) 30%,var(--line));border-radius:8px;padding:10px 14px;margin:.4em 0 1em;font-size:.92rem;line-height:1.6}
article .impact-k{display:inline-block;font-size:.7rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin-right:8px;vertical-align:middle}
article .cta{margin:1.4em 0 .6em;display:flex;gap:10px;flex-wrap:wrap}
article .btn{display:inline-flex;align-items:center;gap:8px;padding:9px 16px;border-radius:8px;background:var(--accent);color:#fff;text-decoration:none;font-size:.92rem;font-weight:500}
article .btn svg{flex-shrink:0}article .btn .arr{transition:transform .15s}article .btn:hover .arr{transform:translateX(3px)}
article .btn:hover{opacity:.92}
article .btn-ghost{background:transparent;color:var(--accent);border:1px solid var(--accent)}
article .diagram{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:1.2em 0}
article .dg-title{margin:0 0 10px;font-size:.85rem;font-weight:600;color:var(--muted);letter-spacing:.04em}
article .dg-flow{display:flex;align-items:stretch;gap:8px;flex-wrap:wrap}
article .dg-box{flex:1 1 120px;min-width:120px;background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:10px 12px;text-align:center;font-size:.85rem;line-height:1.35}
article .dg-box b{display:block;margin-bottom:4px}article .dg-box small{color:var(--muted);font-size:.76rem;display:block}
article .dg-accent{border-color:color-mix(in srgb,var(--accent) 45%,var(--line));background:color-mix(in srgb,var(--accent) 8%,var(--bg))}
article .dg-arrow{align-self:center;color:var(--muted);font-size:1.2rem}
article .dg-note{margin:10px 0 0;font-size:.8rem;color:var(--muted)}
aside.toc{position:sticky;top:76px;align-self:start;max-height:calc(100vh - 96px);overflow:auto;font-size:.86rem;border-left:1px solid var(--line);padding-left:16px}
aside.toc .t{font-weight:600;margin:0 0 8px;color:var(--muted);font-size:.78rem;letter-spacing:.06em;text-transform:uppercase}
aside.toc ul{list-style:none;margin:0;padding:0}aside.toc li{margin:4px 0}
aside.toc ul ul{padding-left:12px}aside.toc a{color:var(--muted);text-decoration:none}aside.toc a:hover,aside.toc a.cur{color:var(--fg);font-weight:600}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:.85rem}
footer .in{max-width:var(--max);margin:0 auto;padding:18px 20px 40px;display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center}
footer .links a{margin-right:14px}
@media(max-width:960px){.wrap{grid-template-columns:minmax(0,1fr)}
aside.toc{display:none;position:fixed;right:16px;bottom:72px;z-index:30;max-height:60vh;width:min(320px,calc(100vw - 32px));background:var(--bg);border:1px solid var(--line);border-radius:12px;padding:14px 16px;box-shadow:0 10px 30px rgba(0,0,0,.22)}
aside.toc.open{display:block}.toc-btn{display:block}}
@media(max-width:600px){article .stats{grid-template-columns:repeat(2,1fr)}article .cta{flex-direction:column}article .btn{justify-content:center}article .dg-flow{flex-direction:column}article .dg-arrow{transform:rotate(90deg)}}
@media print{:root{--bg:#fff;--fg:#000;--muted:#444;--line:#bbb;--accent:#000;--soft:#fff}
body{font-size:11pt;line-height:1.45}.topbar,aside.toc,.toc-btn,footer,.more,.cta{display:none}
.hero{background:none;border:0}.hero .in,.wrap{padding:0}.wrap{display:block}
article .impact,article .diagram{border:1px solid #bbb;background:#fff}
article>h1{margin-top:1.4em;page-break-after:avoid}article h2,article h3{page-break-after:avoid}article li,article p{page-break-inside:avoid}a{text-decoration:none}}
"""

JS = """
(function(){
  var btn=document.querySelector('.toc-btn'),toc=document.querySelector('aside.toc');
  if(btn&&toc){btn.addEventListener('click',function(){toc.classList.toggle('open')});
    toc.addEventListener('click',function(e){if(e.target.tagName==='A')toc.classList.remove('open')});}
  if(!toc)return;
  var links=[].slice.call(toc.querySelectorAll('a[href^="#"]'));
  var heads=links.map(function(a){return document.getElementById(decodeURIComponent(a.getAttribute('href').slice(1)))}).filter(Boolean);
  function cur(){var y=window.scrollY+90,i=-1;heads.forEach(function(h,k){if(h.offsetTop<=y)i=k});
    links.forEach(function(a,k){a.classList.toggle('cur',k===i)})}
  window.addEventListener('scroll',cur,{passive:true});cur();
})();
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
<a class="brand" href="{home}">{name}</a>
<nav>{nav}</nav>
<div class="ext">{links}<span class="lang">{lang_toggle}</span></div>
</div></div>
{hero}
<div class="wrap">
<article>
{body}
</article>
{toc}
</div>
<button class="toc-btn" aria-label="목차">☰</button>
<footer><div class="in"><span>Last updated {updated}</span><span class="links">{footer_links}</span><span>{footer_note}</span></div></footer>
<script>{js}</script>
</body>
</html>
"""

NOTE = {
    "ko": "공개용으로 정제된 요약이며 사내 식별자·운영 정보는 포함하지 않습니다.",
    "en": "Public summary. Internal identifiers and operational details are intentionally omitted.",
}


def nav_html(current: str, lang: str) -> str:
    out = []
    for stem, ko, en, _ in CONFIG["pages"]:
        label = en if lang == "en" else ko
        href = f"{stem}.en.html" if lang == "en" and (CONTENT / f"{stem}.en.md").exists() else f"{stem}.html"
        out.append(f'<a href="{href}"{" class=on" if stem == current else ""}>{html.escape(label)}</a>')
    return "".join(out)


def links_html() -> str:
    return "".join(
        f'<a href="{html.escape(href)}" rel="me noopener">{html.escape(label)}</a>'
        for label, href in CONFIG["links"].items() if href
    )


def lang_toggle(stem: str, lang: str) -> str:
    has_en = (CONTENT / f"{stem}.en.md").exists()
    if lang == "en":
        return f'<a href="{stem}.html">KR</a><span class="on">EN</span>'
    if has_en:
        return f'<span class="on">KR</span><a href="{stem}.en.html">EN</a>'
    return f'<span class="on">KR</span><span class="off" title="English version: Career page only">EN</span>'


def toc_html(tokens, depth=2) -> str:
    def walk(items, level):
        if not items or level > depth:
            return ""
        lis = []
        for it in items:
            sub = walk(it.get("children", []), level + 1)
            # toc 토큰의 name 은 이미 HTML 이스케이프된 상태 — 한 번 풀고 다시 이스케이프해 이중 이스케이프 방지
            lis.append(f'<li><a href="#{it["id"]}">{html.escape(html.unescape(it["name"]))}</a>{sub}</li>')
        return "<ul>" + "".join(lis) + "</ul>"
    return walk(tokens, 1)


def build_page(stem: str, label: str, with_toc: bool, lang: str) -> None:
    src = CONTENT / (f"{stem}.en.md" if lang == "en" else f"{stem}.md")
    if not src.exists():
        return
    md = markdown.Markdown(
        extensions=["extra", "sane_lists", "smarty", "attr_list",
                    TocExtension(slugify=slugify_unicode, toc_depth="1-3", permalink=False)],
        output_format="html5",
    )
    body = md.convert(src.read_text(encoding="utf-8"))
    toc = ""
    if with_toc:
        title = "Contents" if lang == "en" else "목차"
        toc = f'<aside class="toc"><p class="t">{title}</p>{toc_html(md.toc_tokens, depth=2)}</aside>'
    name = CONFIG["name_en"] if lang == "en" else CONFIG["name"]
    hero = ""
    if stem == "index":
        hero = (f'<div class="hero"><div class="in"><h1>{html.escape(name)}</h1>'
                f'<p>{html.escape(CONFIG["title"])}</p></div></div>')
    page = PAGE.format(
        lang=lang, name=html.escape(name), title=html.escape(CONFIG["title"]),
        page_title=html.escape(label), css=CSS, js=JS,
        home="index.en.html" if lang == "en" else "index.html",
        nav=nav_html(stem, lang), links=links_html(), lang_toggle=lang_toggle(stem, lang),
        hero=hero, body=body, toc=toc, footer_links=links_html(), footer_note=NOTE[lang],
        updated=datetime.date.today().isoformat(),
    )
    out = OUT_DIR / (f"{stem}.en.html" if lang == "en" else f"{stem}.html")
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({len(page.encode()):,} bytes)")


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / ".nojekyll").touch()
    for stem, ko, en, with_toc in CONFIG["pages"]:
        build_page(stem, ko, with_toc, "ko")
        build_page(stem, en, with_toc, "en")


if __name__ == "__main__":
    main()
