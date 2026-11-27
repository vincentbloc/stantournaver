# -*- coding: utf-8 -*-
"""국가 총정리(허브) 페이지 생성기.

내용은 src/hub_content.py 의 HUB_PAGES 에서 관리한다. 이 파일은 틀(HTML·CSS)만 담는다.

  python3 src/hub_pages.py                # site/<slug>/index.html 을 다시 만든다
  python3 src/build_site.py --no-images   # 글 목록 블록(related)을 채운다 (자동 글쓰기 빌드도 같은 일을 한다)

- 사실 정보는 data/posts/ 의 글에서 확인한 것만 쓴다. 글과 숫자가 어긋나면 글을 먼저 확인한다.
- 아이콘은 src/vendor/lucide (ISC 라이선스), 글꼴은 Pretendard(OFL, jsDelivr)로 메인 페이지와 같다.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
SITE = "https://stantournaver.com"
OUT = os.path.join(ROOT, "site")
NAVER = "4d59841bb5cc538afa936d117e03fb43bd11896e"
CAFE_GO = "/go/cafe/"          # 카페 가입 링크(클릭 수 집계용 경유 주소)
SITE_NAME = "중앙아시아 여행 가이드"
PRETENDARD = "https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css"
ICON_DIR = os.path.join(ROOT, "src", "vendor", "lucide")

esc = html.escape


def ic(name, size=22):
    """Lucide 아이콘을 인라인 SVG로."""
    raw = open(os.path.join(ICON_DIR, name + ".svg"), encoding="utf-8").read()
    inner = re.sub(r"\s+", " ", re.search(r"<svg[^>]*>(.*)</svg>", raw, re.S).group(1)).strip()
    return (f'<svg class="ic" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{inner}</svg>')


def mix(a, b, t):
    """두 색(#rrggbb)을 t 비율로 섞는다."""
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]; pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02x}" for x, y in zip(pa, pb))


# ───────────────────────────── 본문 부품
def links(items):
    """'더 자세히' 링크 줄. items = [(주소, 글자), …]"""
    return '<p class="more">자세한 내용: ' + " · ".join(f'<a href="{u}">{esc(t)}</a>' for u, t in items) + "</p>"


def info_table(rows):
    return ('<div class="tbl"><table class="info"><tbody>' +
            "".join(f"<tr><th scope=\"row\">{esc(k)}</th><td>{v}</td></tr>" for k, v in rows) + "</tbody></table></div>")


def grid_table(head, rows):
    """3열 표. 좁은 화면에서는 CSS가 행을 카드처럼 쌓는다(칸 이름은 data-label)."""
    return ('<div class="tbl"><table class="grid"><thead><tr>' + "".join(f"<th scope=\"col\">{esc(h)}</th>" for h in head) +
            "</tr></thead><tbody>" + "".join("<tr>" + "".join(f'<td data-label="{esc(head[i])}">{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows) + "</tbody></table></div>")


def spots(items):
    """items = [(구분, 이름, 설명, 주소), …]"""
    return ('<ul class="spots">' + "".join(
        f'<li><a href="{u}"><span class="tag">{esc(tag)}</span><b>{esc(name)}</b><span class="d">{desc}</span></a></li>'
        for tag, name, desc, u in items) + "</ul>")


def days(items):
    """items = [(날짜 표시, 제목, 설명), …]"""
    return ('<ol class="days">' + "".join(
        f'<li><span class="n">{esc(n)}</span><div><b>{esc(t)}</b><p>{d}</p></div></li>' for n, t, d in items) + "</ol>")


def styles(items):
    """items = [(아이콘, 제목, 설명, 주소, 링크 글자), …]"""
    return ('<div class="styles">' + "".join(
        f'<div>{ic(i)}<b>{esc(t)}</b><p>{d}</p><a href="{u}">{esc(lt)}</a></div>' for i, t, d, u, lt in items) + "</div>")


def check(items):
    return '<ul class="check">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"


def food(items):
    return '<dl class="food">' + "".join(f"<div><dt>{esc(k)}</dt><dd>{v}</dd></div>" for k, v in items) + "</dl>"


def cafe_box(title, text, btn):
    return (f'<aside class="cafe-box"><h2>{esc(title)}</h2><p>{esc(text)}</p>'
            f'<a class="btn-n" href="{CAFE_GO}" target="_blank" rel="noopener"><span class="n" aria-hidden="true">N</span>{esc(btn)}</a></aside>')


CSS = r"""
:root{--ink:#232a3f;--soft:#4e5670;--paper:#faf6ec;--card:#fff;--line:#e7dfcd;--naver:#03c75a;--gold:#ffd98a;--ac:%(ac)s;--dark:%(dark)s;--mid:%(mid)s;--tint:%(tint)s}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%%}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
body{font-family:'Pretendard Variable',Pretendard,-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Noto Sans KR','Malgun Gothic',sans-serif;background:var(--paper);color:var(--ink);line-height:1.75;font-size:17px;word-break:keep-all;padding-bottom:78px}
a{color:var(--dark);text-underline-offset:3px}
a:focus-visible,summary:focus-visible{outline:3px solid #e29a2f;outline-offset:2px;border-radius:4px}
.wrap{max-width:820px;margin:0 auto;padding:0 20px}
.ic{flex:none;vertical-align:middle}
.topbar{background:var(--dark);padding:11px 0;font-size:.95rem}
.topbar .wrap{display:flex;justify-content:space-between;align-items:center;gap:12px}
.topbar a{color:#fff;font-weight:800;text-decoration:none}
.topbar .cta{background:var(--naver);font-size:.86rem;font-weight:700;padding:6px 13px;border-radius:8px}
.hero{position:relative;color:#fff;background:linear-gradient(152deg,var(--dark) 0%%,var(--mid) 58%%,var(--ac) 125%%);overflow:hidden}
.hero svg.tiles{position:absolute;inset:0;width:100%%;height:100%%;opacity:.13}
.hero .wrap{position:relative;padding-top:44px;padding-bottom:78px}
.crumb{font-size:.86rem;color:rgba(255,255,255,.85);margin-bottom:18px}
.crumb a{color:#fff}
h1{font-size:clamp(1.95rem,6.4vw,2.9rem);font-weight:800;letter-spacing:-.03em;line-height:1.22}
h1 span{display:block;font-size:.5em;font-weight:600;letter-spacing:-.01em;line-height:1.5;margin-top:10px;color:var(--gold)}
.lede{max-width:640px;margin:18px 0 26px;color:rgba(255,255,255,.93);font-size:1.02rem}
.hero .btn-n{display:none}
.btn-n{display:inline-flex;align-items:center;gap:9px;background:var(--naver);color:#fff;font-weight:800;text-decoration:none;padding:13px 22px;border-radius:12px;font-size:1rem;line-height:1.3}
.btn-n .n{background:#fff;color:var(--naver);border-radius:5px;width:22px;height:22px;display:inline-flex;align-items:center;justify-content:center;font-size:13px;font-weight:900;flex:none}
.btn-n:hover{background:#02b351}
.quick{position:relative;margin-top:-44px;background:var(--card);border:1px solid var(--line);border-radius:16px;display:grid;grid-template-columns:1fr 1fr;box-shadow:0 10px 30px rgba(35,42,63,.08)}
.quick div{padding:15px 16px;display:grid;grid-template-columns:auto 1fr;column-gap:11px;align-items:center;border-top:1px solid var(--line)}
.quick div:nth-child(-n+2){border-top:0}
.quick div:nth-child(even){border-left:1px solid var(--line)}
.quick .ic{grid-row:1/3;color:var(--ac)}
.quick dt{font-size:.82rem;color:var(--soft);line-height:1.3}
.quick dd{font-weight:800;font-size:.98rem;line-height:1.35}
.toc{margin:26px 0 0}
.toc b{display:block;font-size:.88rem;color:var(--soft);margin-bottom:9px}
.toc ol{display:flex;flex-wrap:wrap;gap:8px;list-style:none}
.toc a{display:inline-block;border:1.5px solid var(--line);border-radius:999px;padding:5px 14px;font-size:.92rem;font-weight:600;color:var(--dark);background:var(--card);text-decoration:none}
.toc a:hover{border-color:var(--ac);background:var(--tint)}
main section{margin:54px 0}
main h2{font-size:clamp(1.38rem,4.3vw,1.72rem);font-weight:800;letter-spacing:-.02em;line-height:1.38;margin-bottom:14px;display:flex;align-items:flex-start;gap:11px;scroll-margin-top:14px}
main h2::before{content:"";width:22px;height:22px;flex:none;border-radius:6px;background:var(--ac);margin-top:.28em}
main p{margin-bottom:14px}
main h3{font-size:1.1rem;font-weight:800;margin:26px 0 10px;letter-spacing:-.01em}
.note{background:var(--tint);border-radius:12px;padding:14px 18px;font-size:.95rem;margin:14px 0}
.more{font-size:.94rem;color:var(--soft);margin-top:12px}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:14px;background:var(--card);margin:14px 0}
table{width:100%%;border-collapse:collapse;font-size:.95rem}
.info th{width:7.2em;background:var(--tint);color:var(--dark);font-weight:800;text-align:left;padding:12px 14px;vertical-align:top;border-top:1px solid var(--line)}
.info td{padding:12px 14px;border-top:1px solid var(--line);vertical-align:top}
.info tr:first-child th,.info tr:first-child td{border-top:0}
.grid thead{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.grid tr{display:block;padding:13px 16px;border-top:1px solid var(--line)}
.grid tbody tr:first-child{border-top:0}
.grid td{display:block}
.grid td:first-child{font-weight:800;color:var(--dark);font-size:1rem;margin-bottom:2px}
.grid td:not(:first-child){padding-left:5.4em;position:relative;color:var(--ink)}
.grid td:not(:first-child)::before{content:attr(data-label);position:absolute;left:0;top:0;font-size:.84em;font-weight:700;color:var(--soft);line-height:2.05}
.spots{list-style:none;display:grid;grid-template-columns:1fr;gap:10px}
.spots a{display:block;height:100%%;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 18px;color:var(--ink);text-decoration:none}
.spots a:hover{border-color:var(--ac)}
.spots .tag{display:inline-block;font-size:.78rem;font-weight:700;color:var(--dark);background:var(--tint);border-radius:6px;padding:2px 9px;margin-bottom:7px}
.spots b{display:block;font-size:1.08rem;letter-spacing:-.01em;margin-bottom:3px}
.spots .d{display:block;font-size:.95rem;color:var(--soft);line-height:1.65}
.days{list-style:none;margin:14px 0;border-left:3px solid var(--line);margin-left:6px}
.days li{position:relative;padding:0 0 20px 22px}
.days li::before{content:"";position:absolute;left:-9px;top:6px;width:15px;height:15px;border-radius:50%%;background:var(--card);border:4px solid var(--ac)}
.days .n{display:block;font-size:.86rem;font-weight:800;color:var(--dark)}
.days b{display:block;font-size:1.04rem}
.days p{margin:2px 0 0;font-size:.96rem;color:var(--soft)}
.cafe-box{margin:54px 0;background:#eefaf2;border:1px solid #bfe9d0;border-radius:16px;padding:24px 22px}
.cafe-box h2{font-size:1.22rem;margin-bottom:8px;display:block}
.cafe-box h2::before{display:none}
.cafe-box p{color:var(--soft);margin-bottom:16px;font-size:.98rem}
.food div{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin-bottom:8px}
.food dt{font-weight:800;color:var(--dark)}
.food dd{font-size:.96rem;color:var(--soft)}
.styles{display:grid;grid-template-columns:1fr;gap:10px}
.styles div{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}
.styles .ic{color:var(--ac);margin-bottom:8px;display:block}
.styles b{display:block;font-size:1.05rem;margin-bottom:4px}
.styles p{font-size:.95rem;color:var(--soft);margin-bottom:8px}
.styles a{font-size:.93rem;font-weight:700}
.check{list-style:none;margin:12px 0}
.check li{position:relative;padding:7px 0 7px 32px;border-bottom:1px dashed var(--line)}
.check li::before{content:"";position:absolute;left:2px;top:14px;width:17px;height:17px;border-radius:5px;border:2px solid var(--ac)}
.check li::after{content:"";position:absolute;left:8px;top:16px;width:5px;height:9px;border:solid var(--ac);border-width:0 2px 2px 0;transform:rotate(45deg)}
details{background:var(--card);border:1px solid var(--line);border-radius:12px;margin-bottom:10px}
summary{cursor:pointer;padding:15px 18px;font-weight:700;list-style:none;display:flex;justify-content:space-between;gap:12px}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";font-size:1.3rem;line-height:1.2;color:var(--ac);font-weight:600;flex:none}
details[open] summary::after{content:"−"}
details p{padding:0 18px 16px;margin:0}
.kw{display:flex;flex-wrap:wrap;gap:8px;list-style:none}
.kw a{display:inline-block;background:var(--card);border:1px solid var(--line);border-radius:999px;padding:6px 14px;font-size:.92rem;font-weight:600;text-decoration:none}
.kw a:hover{border-color:var(--ac);background:var(--tint)}
#posts h2{margin-bottom:16px}
.cafe-band{background:linear-gradient(135deg,var(--dark),var(--mid));color:#fff;border-radius:16px;padding:30px 24px;margin:54px 0 0;text-align:center}
.cafe-band h2{color:#fff;display:block;font-size:1.3rem;margin-bottom:8px}
.cafe-band h2::before{display:none}
.cafe-band p{color:rgba(255,255,255,.9);max-width:540px;margin:0 auto 18px}
footer{margin-top:56px;background:var(--dark);color:rgba(255,255,255,.85);padding:28px 0 34px;font-size:.9rem}
footer p{margin-bottom:6px}
footer a{color:var(--gold);font-weight:700}
.sticky{position:fixed;left:0;right:0;bottom:0;background:rgba(255,255,255,.96);border-top:1px solid var(--line);padding:10px 16px calc(10px + env(safe-area-inset-bottom));display:flex;justify-content:center;z-index:5}
.sticky .btn-n{width:100%%;max-width:460px;justify-content:center;padding:12px 18px}
@media (min-width:640px){
 .hero .wrap{padding-top:58px;padding-bottom:92px}
 .quick{grid-template-columns:repeat(4,1fr)}
 .quick div{border-top:0;border-left:1px solid var(--line)}
 .quick div:first-child{border-left:0}
 .grid thead{position:static;width:auto;height:auto;overflow:visible;clip:auto}
 .grid tr{display:table-row;padding:0;border:0}
 .grid td{display:table-cell;padding:11px 14px;border-top:1px solid var(--line);vertical-align:top}
 .grid thead th{background:var(--dark);color:#fff;font-weight:700;text-align:left;padding:11px 14px;white-space:nowrap}
 .grid td:first-child{font-size:inherit;white-space:nowrap;margin:0}
 .grid td:not(:first-child){padding-left:14px}
 .grid td:not(:first-child)::before{content:none}
 .hero .btn-n{display:inline-flex}
 .spots{grid-template-columns:1fr 1fr}
 .styles{grid-template-columns:1fr 1fr}
 .cafe-box{padding:28px 30px}
}
"""

TILES = """<svg class="tiles" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="girih" width="88" height="88" patternUnits="userSpaceOnUse"><path d="M44 6 L52 36 L82 44 L52 52 L44 82 L36 52 L6 44 L36 36 Z" fill="none" stroke="#ffffff" stroke-width="1.6"/><circle cx="44" cy="44" r="7" fill="none" stroke="#ffffff" stroke-width="1.2"/><circle cx="0" cy="0" r="10" fill="none" stroke="#ffffff" stroke-width="1"/><circle cx="88" cy="0" r="10" fill="none" stroke="#ffffff" stroke-width="1"/><circle cx="0" cy="88" r="10" fill="none" stroke="#ffffff" stroke-width="1"/><circle cx="88" cy="88" r="10" fill="none" stroke="#ffffff" stroke-width="1"/></pattern></defs><rect width="100%" height="100%" fill="url(#girih)"/></svg>"""


def render(h):
    url = f"{SITE}/{h['slug']}/"
    thumb = f"{SITE}/assets/thumb/{h['slug']}.jpg"
    ac, dark = h["accent"]
    css = CSS % dict(ac=ac, dark=dark, mid=mix(dark, ac, .42), tint=mix("#ffffff", ac, .11))
    toc, body = [], []
    for s in h["sections"]:
        if s.get("raw"):
            body.append(s["raw"]); continue
        toc.append((s["id"], s.get("toc") or s["h2"]))
        body.append(f'<section id="{s["id"]}">\n<h2>{esc(s["h2"])}</h2>\n{s["html"]}\n</section>')
    faq_html = "\n".join(f"<details{' open' if i == 0 else ''}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for i, (q, a) in enumerate(h["faq"]))
    toc.append(("faq", "자주 묻는 질문"))
    kw_html = '<ul class="kw">' + "".join(f'<li><a href="{u}">{esc(t)}</a></li>' for t, u in h["chips"]) + "</ul>"
    quick = '<dl class="quick">' + "".join(f"<div>{ic(i)}<dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for i, k, v in h["quick"]) + "</dl>"
    toc_html = '<nav class="toc" aria-label="목차"><b>이 페이지에서 볼 수 있는 것</b><ol>' + "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc) + "</ol></nav>"
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "@id": url + "#article", "headline": h["headline"], "description": h["desc"], "image": [thumb],
         "inLanguage": "ko-KR", "datePublished": h["published"] + "T09:00:00+09:00", "dateModified": h["modified"] + "T09:00:00+09:00",
         "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "about": {"@type": "TouristDestination", "name": h["name"]},
         "author": {"@type": "Organization", "name": SITE_NAME, "url": SITE + "/"},
         "publisher": {"@type": "Organization", "name": SITE_NAME, "url": SITE + "/", "logo": {"@type": "ImageObject", "url": SITE + "/assets/logo.png", "width": 512, "height": 512}}},
        {"@type": "TouristDestination", "name": h["name"], "description": h["desc"], "url": url, "image": thumb},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": SITE_NAME, "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": h["name"] + " 여행 총정리", "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in h["faq"]]}]}
    y, m, d = h["modified"].split("-")
    others = " · ".join(f'<a href="/{s}/">{esc(n)} 여행</a>' for s, n in h["others"])
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(h['title'])}</title>
<meta name="description" content="{esc(h['desc'])}">
<meta name="keywords" content="{esc(h['keywords'])}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url}">
<link rel="alternate" type="application/rss+xml" title="{SITE_NAME}" href="{SITE}/rss.xml">
<link rel="icon" href="/assets/logo.png">
<meta name="naver-site-verification" content="{NAVER}">
<meta property="og:type" content="article">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{esc(h['headline'])}">
<meta property="og:description" content="{esc(h['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{thumb}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="article:modified_time" content="{h['modified']}T09:00:00+09:00">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{thumb}">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preload" as="style" href="{PRETENDARD}" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="{PRETENDARD}"></noscript>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>{css.strip()}</style>
</head>
<body>
<div class="topbar"><div class="wrap"><a href="/">{SITE_NAME}</a><a class="cta" href="{CAFE_GO}" target="_blank" rel="noopener">카페 가입</a></div></div>
<header class="hero">{TILES}<div class="wrap">
<nav class="crumb" aria-label="현재 위치"><a href="/">{SITE_NAME}</a> › {esc(h['name'])}</nav>
<h1>{esc(h['name'])} 여행 총정리<span>{esc(h['h1_sub'])}</span></h1>
<p class="lede">{esc(h['lede'])}</p>
<a class="btn-n" href="{CAFE_GO}" target="_blank" rel="noopener"><span class="n" aria-hidden="true">N</span>{esc(h['name'])} 여행 카페 가입하기</a>
</div></header>
<div class="wrap">
{quick}
{toc_html}
</div>
<main class="wrap">
{chr(10).join(body)}

<section id="faq">
<h2>{esc(h['name'])} 여행 자주 묻는 질문</h2>
{faq_html}
</section>

<section id="keywords">
<h2>함께 많이 찾는 {esc(h['name'])} 여행 정보</h2>
{kw_html}
</section>

<!-- related-start -->
<!-- related-end -->

<section class="cafe-band">
<h2>{esc(h['name'])} 여행, 혼자 준비하지 마세요</h2>
<p>항공 특가, 최신 현지 소식, 먼저 다녀온 회원들의 답변까지 네이버 카페에서 나눕니다.</p>
<a class="btn-n" href="{CAFE_GO}" target="_blank" rel="noopener"><span class="n" aria-hidden="true">N</span>네이버 카페 가입하기</a>
</section>
</main>
<footer><div class="wrap">
<p>이 페이지는 {y}년 {int(m)}월 {int(d)}일 기준으로 정리했습니다. 요금, 운행 시간, 비자 정책은 바뀔 수 있으니 출발 전 공식 안내를 확인하세요.</p>
<p>다른 여행지: {others} · <a href="/">중앙아시아 전체 가이드</a> · <a href="/travel/">전체 여행 글</a></p>
</div></footer>
<div class="sticky"><a class="btn-n" href="{CAFE_GO}" target="_blank" rel="noopener"><span class="n" aria-hidden="true">N</span>{esc(h['name'])} 여행 카페 가입하기</a></div>
</body>
</html>
"""


def check_links(h, page):
    """내부 링크가 실제 있는 글·페이지인지 확인."""
    bad = []
    for l in set(re.findall(r'href="(/[^"#]*)"', page)):
        p = l.lstrip("/")
        t = os.path.join(OUT, p, "index.html") if (p.endswith("/") or not p) else os.path.join(OUT, p)
        if p.startswith("travel/"):
            slug = p.strip("/").split("/")[-1]
            import glob as _g
            if p != "travel/" and not _g.glob(os.path.join(ROOT, "data", "posts", f"*-{slug}.json")): bad.append(l)
        elif not os.path.exists(t) and l != CAFE_GO: bad.append(l)
    return bad


if __name__ == "__main__":
    from hub_content import HUB_PAGES
    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    for h in HUB_PAGES:
        if only and h["slug"] not in only: continue
        page = render(h)
        bad = check_links(h, page)
        if bad:
            print("깨진 링크:", h["slug"], bad); sys.exit(1)
        d = os.path.join(OUT, h["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page)
        text = re.sub(r"<[^>]+>", "", re.sub(r"<(script|style)[^>]*>.*?</\1>", "", page, flags=re.S))
        print("ok", h["slug"], "본문 글자 수", len(re.sub(r"\s+", "", text)), "제목", len(h["title"]), "자, 설명", len(h["desc"]), "자")
