"""이미지 생성 + SEO 강화 빌드 (중앙아시아 여행 가이드)"""
import os, json, re, sys
import build as B  # 공용 템플릿·게시판·피드
from build import SITE, OUT, CAFE, DATE, DATE_DOT, NAVER, CAT, HUBS, POSTS, esc, thumb_url, CTA_TEXT, item_title
from scenes import SCENES
import infographics as IG

HUB_SCENE = {}
MANIFEST = os.path.join(B.ROOT, "data", "img_manifest.json")

for p in POSTS:
    p["stitle"] = p["x"]["stitle"]

# ───────────────────────────── 썸네일 (좌측 글자 + 우측 컬러 일러스트)
def thumb_html(line1, line2, chip, accent, dark, scene_svg, main=False, collage=None):
    n = len(line1.replace("<br>", ""))
    size = 88 if main else (80 if n <= 6 else 66 if n <= 8 else 58 if n <= 10 else 52)
    right = f'<svg class="scene" viewBox="0 0 600 630" preserveAspectRatio="xMidYMid slice">{scene_svg}</svg>'
    if collage:
        right = '<div class="col">' + "".join(f'<svg viewBox="0 0 600 630" preserveAspectRatio="xMidYMid slice">{s}</svg>' for s in collage) + "</div>"
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1200px;height:630px;overflow:hidden;font-family:'Noto Sans CJK KR','Noto Color Emoji',sans-serif;color:#fff;background:linear-gradient(90deg,{dark} 0px,{accent} 600px,{accent} 1200px);position:relative;word-break:keep-all}}
.scene{{position:absolute;right:0;top:0;width:600px;height:630px}}
.col{{position:absolute;right:0;top:0;width:600px;height:630px;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:6px;background:{dark}}}
.col svg{{width:100%;height:100%}}
.fade{{position:absolute;left:600px;top:0;width:190px;height:630px;background:linear-gradient(90deg,{accent},rgba(0,0,0,0))}}
.grain{{position:absolute;left:0;top:0;width:640px;height:630px;background-image:radial-gradient(rgba(255,255,255,.08) 1.5px,transparent 1.5px);background-size:24px 24px}}
.wrap{{position:absolute;left:64px;top:0;bottom:70px;width:530px;display:flex;flex-direction:column;justify-content:center}}
.chip{{align-self:flex-start;font-size:28px;font-weight:800;padding:8px 22px;border-radius:99px;background:#fff;color:{dark};margin-bottom:24px}}
h1{{max-width:520px;white-space:normal;font-size:{size}px;font-weight:900;line-height:1.14;letter-spacing:-.02em;text-shadow:0 4px 18px rgba(0,0,0,.25)}}
h2{{font-size:36px;font-weight:700;margin-top:18px;color:#ffe27a;line-height:1.3}}
.bar{{display:flex;gap:8px;margin-top:22px}}.bar i{{width:44px;height:8px;border-radius:4px}}
.brand{{position:absolute;left:70px;bottom:40px;font-size:23px;font-weight:700;opacity:.92}}
</style></head><body>{right}<div class="fade"></div><div class="grain"></div>
<div class="wrap"><span class="chip">{chip}</span><h1>{line1}</h1><h2>{line2}</h2>
<div class="bar"><i style="background:#ff6b6b"></i><i style="background:#ffd23f"></i><i style="background:#20c997"></i><i style="background:#4d96ff"></i><i style="background:#9b5de5"></i></div></div>
<div class="brand">stantournaver.com · 중앙아시아 여행 가이드</div></body></html>"""

LOGO = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>*{margin:0}body{width:512px;height:512px;overflow:hidden;font-family:'Noto Sans CJK KR',sans-serif}
.b{width:512px;height:512px;border-radius:110px;background:linear-gradient(135deg,#15336b,#1b9d96);position:relative;overflow:hidden}
.m{position:absolute;right:70px;top:70px;width:150px;height:150px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#fff7dc,#f3c96a 70%)}
svg{position:absolute;left:0;bottom:0;width:512px;height:220px}
.t{position:absolute;left:56px;top:180px;color:#fff;font-weight:900;font-size:76px;line-height:1.12;letter-spacing:-.03em}</style></head>
<body><div class="b"><div class="m"></div><svg viewBox="0 0 512 220" preserveAspectRatio="none"><path d="M0 220 L0 120 L80 60 L150 110 L240 30 L330 100 L420 50 L512 110 L512 220Z" fill="rgba(0,0,0,.25)"/></svg><div class="t">중앙아시아<br>여행</div></div></body></html>"""

def jpg(pg, png, out, sel=None):
    from PIL import Image
    (pg.query_selector(sel).screenshot(path=png) if sel else pg.screenshot(path=png))
    im = Image.open(png).convert("RGB"); im.save(out, quality=84, optimize=True, progressive=True)
    return im.size

def render_all_images(full=False):
    """새 글(또는 --all)만 이미지 생성. 기존 이미지는 그대로 재사용."""
    from playwright.sync_api import sync_playwright
    tdir = os.path.join(OUT, "assets", "thumb"); idir = os.path.join(OUT, "assets", "img")
    os.makedirs(tdir, exist_ok=True); os.makedirs(idir, exist_ok=True)
    man = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}
    def exists(p): return os.path.exists(p)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 630})
        if full or not exists(os.path.join(tdir, "og-main.jpg")):
            pg.set_content(thumb_html("중앙아시아 여행<br>가이드", "비자·직항·코스·경비 총정리", "무비자 · 2026", "#1f4d9e", "#15336b", "",
                                      main=True, collage=[SCENES[k] for k in ["dome_city", "mountain_lake", "yurt_steppe", "canyon"]]))
            pg.wait_for_timeout(80); jpg(pg, "/tmp/_t.png", os.path.join(tdir, "og-main.jpg"))
        for h in HUBS:
            out = os.path.join(tdir, f"{h['slug']}.jpg")
            if full or not exists(out):
                pg.set_content(thumb_html(h["thumb"][0], h["thumb"][1], h["city"], *h["accent"], SCENES[HUB_SCENE[h["slug"]]]))
                pg.wait_for_timeout(60); jpg(pg, "/tmp/_t.png", out)
        for p in POSTS:
            out = os.path.join(tdir, f"{p['slug']}.jpg")
            if full or not exists(out):
                pg.set_content(thumb_html(p["thumb"][0], p["thumb"][1], p["city"], *p["accent"], SCENES[p["x"]["scene"]]))
                pg.wait_for_timeout(60); jpg(pg, "/tmp/_t.png", out)
        if full or not exists(os.path.join(OUT, "assets", "logo.png")):
            lp = b.new_page(viewport={"width": 512, "height": 512}); lp.set_content(LOGO); lp.wait_for_timeout(60)
            lp.screenshot(path=os.path.join(OUT, "assets", "logo.png"), omit_background=True)
        ip = b.new_page(viewport={"width": 1200, "height": 800})
        for p in POSTS:
            x = p["x"]
            specs = [(x["facts"], IG.facts(x["facts"]))]
            for s in x["imgs"]: specs.append((s, IG.RENDER[s["type"]](s)))
            specs.append((x["tips"], IG.tips(x["tips"], x["tips"]["h2"])))
            files = [f"{p['slug']}-{s['kw']}.jpg" for s, _ in specs]
            if not full and p["slug"] in man and all(exists(os.path.join(idir, f)) for f in files):
                continue
            lst = []
            for (s, doc), fn in zip(specs, files):
                ip.set_content(doc); ip.wait_for_timeout(80)
                w, h = jpg(ip, "/tmp/_i.png", os.path.join(idir, fn), "#cap")
                lst.append(dict(file=fn, w=w, h=h, kw=s["kw"]))
            man[p["slug"]] = lst
            print("  images:", p["slug"])
        b.close()
    json.dump(man, open(MANIFEST, "w"), ensure_ascii=False, indent=1)

# ───────────────────────────── 추가 CSS
EXTRA_CSS = r"""
figure.ig{margin:22px 0 8px;border-radius:18px;overflow:hidden;box-shadow:0 6px 24px rgba(30,40,80,.08);background:#fff}
figure.ig img{display:block;width:100%;height:auto}
figure.ig figcaption{font-size:14px;color:var(--soft);padding:10px 16px;background:var(--alt)}
.toc{margin:26px 0 8px;border:2px solid var(--line);border-radius:16px;padding:18px 22px;background:#fff}
.toc b{display:block;font-size:16px;margin-bottom:6px}
.toc ol{padding-left:22px;font-size:15.5px;columns:2;column-gap:28px}
.toc li{margin:3px 0;break-inside:avoid}
.toc a{color:var(--ink);text-decoration:none}.toc a:hover{color:var(--ac);text-decoration:underline}
.kfacts{list-style:none;display:grid;grid-template-columns:1fr 1fr;gap:6px 18px;margin:10px 0 0;font-size:15.5px}
.kfacts li{padding:6px 0;border-bottom:1px dashed var(--line)}
.kfacts li b{color:var(--ac);margin-right:6px}
article h2{scroll-margin-top:12px}
@media (max-width:640px){.toc ol{columns:1}.kfacts{grid-template-columns:1fr}}
.ask{margin:26px 0;border-radius:16px;padding:18px 20px;background:linear-gradient(135deg,#eafaf1,#f7fcf9);border:1px solid #bfe9d0;display:flex;gap:14px;align-items:center;justify-content:space-between;flex-wrap:wrap}
.ask div{flex:1 1 260px}
.ask strong{display:block;font-size:17px;line-height:1.45;margin-bottom:4px}
.ask p{margin:0;color:var(--soft);font-size:15px;line-height:1.55}
.ask a{flex:0 0 auto;display:inline-flex;align-items:center;gap:8px;background:#03c75a;color:#fff;font-weight:700;text-decoration:none;padding:11px 18px;border-radius:12px;font-size:15.5px}
.ask a .n{background:#fff;color:#03c75a;border-radius:5px;width:22px;height:22px;display:inline-flex;align-items:center;justify-content:center;font-size:13px;font-weight:900}
.more3{margin:18px 0 6px;border:1px solid var(--line);border-radius:16px;padding:14px 16px;background:#fff}
.more3 b{display:block;font-size:15px;margin-bottom:8px}
.more3 a{display:flex;gap:12px;align-items:center;text-decoration:none;color:var(--ink);padding:7px 0;border-top:1px dashed var(--line)}
.more3 a:first-of-type{border-top:0}
.more3 img{width:96px;height:auto;border-radius:8px;flex:0 0 96px}
.more3 span{font-size:15px;font-weight:700;line-height:1.45}
.more3 a:hover span{color:var(--ac);text-decoration:underline}
@media (max-width:640px){.ask a{width:100%;justify-content:center}.more3 img{width:80px;flex-basis:80px}}
"""

# 많이 보는 글(방문 통계 기준, data/popular.json에서 관리)
POPULAR_FILE = os.path.join(B.ROOT, "data", "popular.json")
POPULAR = json.load(open(POPULAR_FILE, encoding="utf-8")) if os.path.exists(POPULAR_FILE) else []
ASK_DEFAULT = {
    "prep": ("{t}, 막히면 카페에 바로 물어보세요", "환전·교통·입국 문제, 먼저 다녀온 회원들이 빠르게 답해 드립니다."),
    "city": ("{c} 여행 준비 중이라면 카페에서 함께해요", "항공·숙소 특가, 현지 최신 소식, 동행 모집까지 카페에서 나눕니다."),
    "spot": ("{t} 가기 전, 카페에서 최신 후기 확인", "투어 가격·예약 소식과 실제 소요 시간 후기가 카페에 올라옵니다."),
    "nature": ("{c} 날씨·현지 상황, 카페에서 확인하세요", "시즌마다 바뀌는 현지 정보와 회원들의 생생한 후기를 공유합니다."),
}

def ask_box(p):
    c = p["x"].get("cta")
    if c and len(c) >= 2:
        t, d = c[0], c[1]
    else:
        t, d = ASK_DEFAULT.get(p["cat"], ASK_DEFAULT["city"])
        t = t.format(t=p["thumb"][0], c=p["city"])
    return f'<aside class="ask"><div><strong>{esc(t)}</strong><p>{esc(d)}</p></div><a href="{CAFE}" target="_blank" rel="noopener"><span class="n">N</span>카페에서 물어보기</a></aside>'

def hub_of(p):
    for h in HUBS:
        if p["slug"].startswith(h["slug"] + "-") or p["city"].startswith(h["city"]): return h
    return None

def more_box(p):
    by = {x["slug"]: x for x in POSTS}
    pick, seen = [], {p["slug"]}
    rel = B.related_for(p)
    h = hub_of(p)
    same = [x for x in POSTS if h and hub_of(x) is h]
    for x in same[:1] + rel[:1] + [by[s] for s in POPULAR if s in by] + rel[1:]:
        if x["slug"] in seen or not x["path"].startswith("/travel/"): continue
        seen.add(x["slug"]); pick.append(x)
        if len(pick) == 3: break
    if not pick: return ""
    return '<nav class="more3" aria-label="많이 보는 글"><b>이 글과 함께 많이 보는 글</b>' + "".join(
        f'<a href="{x["path"]}"><img src="/assets/thumb/{x["slug"]}.jpg" alt="{esc(item_title(x))}" width="1200" height="630" loading="lazy" decoding="async"><span>{esc(item_title(x))}</span></a>' for x in pick) + "</nav>"

def fig(slug, item, alt, cap):
    return (f'<figure class="ig"><img src="/assets/img/{item["file"]}" alt="{esc(alt)}" width="{item["w"]}" height="{item["h"]}" loading="lazy" decoding="async">'
            f'<figcaption>{esc(cap)}</figcaption></figure>')

def build_body(p, man):
    x = p["x"]; imgs = {m["kw"]: m for m in man[p["slug"]]}
    body = p["body"]
    for old, new in x.get("h2", {}).items():
        body = body.replace(f"<h2>{old}</h2>", f"<h2>{new}</h2>", 1)
    # 본문 인포그래픽을 해당 h2 뒤에
    parts = re.split(r"(<h2>.*?</h2>)", body)
    h2i = -1; out = []; toc = []
    for part in parts:
        m = re.match(r"<h2>(.*?)</h2>", part)
        if m:
            h2i += 1; sid = f"s{h2i+1}"; toc.append((sid, re.sub("<[^>]+>", "", m.group(1))))
            out.append(f'<h2 id="{sid}">{m.group(1)}</h2>')
            for s in x["imgs"]:
                if s["after"] == h2i:
                    out.append(fig(p["slug"], imgs[s["kw"]], s["alt"], s["title"]))
        else:
            out.append(part)
    body = "".join(out)
    # 첫 소제목 섹션이 끝나는 곳(두 번째 h2 앞)에 주제 맞춤 카페 안내
    hs = [m.start() for m in re.finditer(r'<h2 id="s', body)]
    ask = ask_box(p)
    body = body[:hs[1]] + ask + body[hs[1]:] if len(hs) > 1 else body + ask
    # 꿀팁 섹션
    t = x["tips"]; tid = f"s{len(toc)+1}"; toc.append((tid, t["h2"]))
    tips_html = (f'<h2 id="{tid}">{esc(t["h2"])}</h2>' + fig(p["slug"], imgs[t["kw"]], t["alt"], t["h2"]) +
                 '<ul class="check">' + "".join(f"<li><b>{esc(h)}</b> – {esc(d)}</li>" for _, h, d in t["items"]) + "</ul>")
    toc.append(("faq", "자주 묻는 질문"))
    f = x["facts"]
    facts_html = fig(p["slug"], imgs[f["kw"]], f["alt"], f["title"]) + '<ul class="kfacts">' + "".join(f"<li><b>{esc(l)}</b>{esc(v)}</li>" for _, l, v in f["items"]) + "</ul>"
    toc_html = '<nav class="toc" aria-label="목차"><b>목차</b><ol>' + "".join(f'<li><a href="#{i}">{esc(tx)}</a></li>' for i, tx in toc) + "</ol></nav>"
    return facts_html + toc_html + more_box(p) + body + tips_html

def render_post(p, man):
    ac, dark = p["accent"]; url = SITE + p["path"]
    images = [thumb_url(p["slug"])] + [f"{SITE}/assets/img/{m['file']}" for m in man[p["slug"]]]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "Article", "headline": p["h1"], "description": p["desc"], "image": images, "keywords": p["kw"],
         "articleSection": CAT[p["cat"]], "inLanguage": "ko-KR", "datePublished": p["date"] + "T09:00:00+09:00", "dateModified": p["date"] + "T09:00:00+09:00",
         "mainEntityOfPage": {"@type": "WebPage", "@id": url},
         "author": {"@type": "Organization", "name": "중앙아시아 여행 가이드", "url": SITE + "/"},
         "publisher": {"@type": "Organization", "name": "중앙아시아 여행 가이드", "url": SITE + "/", "logo": {"@type": "ImageObject", "url": SITE + "/assets/logo.png", "width": 512, "height": 512}}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "중앙아시아 여행 가이드", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": CAT[p["cat"]], "item": SITE + "/travel/#" + p["cat"]},
            {"@type": "ListItem", "position": 3, "name": item_title(p), "item": url}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}]}
    faq_html = "\n".join(f"<details{' open' if i == 0 else ''}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for i, (q, a) in enumerate(p["faq"]))
    rel = "\n".join(f'<a href="{r["path"]}"><img src="/assets/thumb/{r["slug"]}.jpg" alt="{esc(item_title(r))}" loading="lazy" decoding="async" width="1200" height="630"><span>{esc(item_title(r))}</span></a>' for r in B.related_for(p))
    cta_t, cta_p = CTA_TEXT[p["cat"]]
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(p['stitle'])}</title>
<meta name="description" content="{esc(p['desc'])}">
<meta name="keywords" content="{esc(p['kw'])}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{url}">
<link rel="alternate" type="application/rss+xml" title="중앙아시아 여행 가이드" href="{SITE}/rss.xml">
<link rel="icon" href="/assets/logo.png">
<link rel="preload" as="image" href="/assets/thumb/{p['slug']}.jpg">
<meta name="naver-site-verification" content="{NAVER}">
<meta property="og:type" content="article">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="중앙아시아 여행 가이드">
<meta property="og:title" content="{esc(p['stitle'])}">
<meta property="og:description" content="{esc(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{thumb_url(p['slug'])}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(p['h1'])}">
<meta property="article:published_time" content="{p['date']}T09:00:00+09:00">
<meta property="article:modified_time" content="{p['date']}T09:00:00+09:00">
<meta property="article:section" content="{CAT[p['cat']]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(p['stitle'])}">
<meta name="twitter:image" content="{thumb_url(p['slug'])}">
<link rel="stylesheet" href="/assets/post.css">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body style="--ac:{ac}">
<div class="topbar"><div class="wrap"><a class="logo" href="/">중앙아시아<span>여행</span>가이드</a><a class="top-cta" href="{CAFE}" target="_blank" rel="noopener">카페 가입</a></div></div>
<main class="wrap">
<nav class="crumb" aria-label="현재 위치"><a href="/">중앙아시아 여행 가이드</a> › <a href="/travel/#{p['cat']}">{CAT[p['cat']]}</a> › {(f'<a href="{hub_of(p)["path"]}">{esc(hub_of(p)["city"])} 여행 총정리</a>' if hub_of(p) else esc(p['city']))}</nav>
<header class="head">
<div class="badges"><span>{esc(p['city'])}</span><span class="o">{CAT[p['cat']]}</span></div>
<h1>{esc(p['h1'])}</h1>
<div class="date"><time datetime="{p['date']}">{p['date_dot']}</time> 작성 · 중앙아시아 여행 가이드</div>
<p class="lead">{esc(p['lead'])}</p>
</header>
<figure class="cover"><img src="/assets/thumb/{p['slug']}.jpg" alt="{esc(p['h1'])}" width="1200" height="630" fetchpriority="high"></figure>
<article>
{build_body(p, man)}
</article>
<div class="cta"><strong>{cta_t}</strong><p>{cta_p}</p><a class="btn" href="{CAFE}" target="_blank" rel="noopener"><span class="n">N</span>네이버 카페 무료 가입</a></div>
<section><h2 id="faq" style="font-size:24px;margin:48px 0 6px">{esc(p['city'])} 자주 묻는 질문</h2><div class="faq">
{faq_html}
</div></section>
<section><h2 style="font-size:24px;margin:48px 0 6px">함께 보면 좋은 글</h2><div class="related">
{rel}
</div></section>
</main>
<footer><div class="wrap"><p>이 글은 {p['date_dot']} 기준으로 작성되었습니다. 요금, 운영 시간, 예약 방식, 비자 정책은 바뀔 수 있으니 방문 전 공식 안내를 확인하세요.</p><p><a href="/travel/">전체 글 보기</a> · 최신 중앙아시아 여행 정보: <a href="{CAFE}" target="_blank" rel="noopener">cafe.naver.com/snowiii</a></p></div></footer>
<div class="sticky"><a class="btn" href="{CAFE}" target="_blank" rel="noopener"><span class="n">N</span>중앙아시아 여행 카페 가입하기</a></div>
</body>
</html>
"""

def write_sitemap(man):
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
    def entry(u, imgs, d=None):
        return f"  <url><loc>{SITE}{u}</loc><lastmod>{d or B.LATEST}</lastmod>" + "".join(f"<image:image><image:loc>{i}</image:loc></image:image>" for i in imgs) + "</url>\n"
    sm += entry("/", [thumb_url("og-main")])
    sm += entry("/travel/", [thumb_url("og-main")])
    for h in HUBS: sm += entry(h["path"], [thumb_url(h["slug"])])
    for p in POSTS: sm += entry(p["path"], [thumb_url(p["slug"])] + [f"{SITE}/assets/img/{m['file']}" for m in man[p["slug"]]], p["date"])
    sm += "</urlset>\n"
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(sm)

def route_cafe_links():
    """카페 가입 링크를 /go/cafe/ 로 보내 방문자 통계에서 클릭 수를 셀 수 있게 한다."""
    import glob as _g
    n = 0
    for f in _g.glob(os.path.join(OUT, "**", "index.html"), recursive=True):
        if os.sep + "go" + os.sep in f: continue
        h = open(f, encoding="utf-8").read()
        h2 = h.replace('href="https://cafe.naver.com/snowiii"', 'href="/go/cafe/"')
        if h2 != h:
            open(f, "w", encoding="utf-8").write(h2); n += 1
    return n

if __name__ == "__main__":
    if "--no-images" not in sys.argv: render_all_images(full="--all" in sys.argv)
    man = json.load(open(MANIFEST)) if os.path.exists(MANIFEST) else {}
    os.makedirs(os.path.join(OUT, "assets"), exist_ok=True)
    open(os.path.join(OUT, "assets", "post.css"), "w", encoding="utf-8").write(B.POST_CSS.strip() + "\n" + EXTRA_CSS.strip() + "\n")
    for p in POSTS:
        p["title"] = p["stitle"]  # 게시판·RSS에도 짧은 SEO 제목 사용
        d = os.path.join(OUT, "travel", p["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(render_post(p, man))
    os.makedirs(os.path.join(OUT, "travel"), exist_ok=True)
    open(os.path.join(OUT, "travel", "index.html"), "w", encoding="utf-8").write(B.render_index())
    B.patch_landing(); B.write_feeds(); write_sitemap(man)
    route_cafe_links()
    print("ok", sum(len(v) for v in man.values()), "body images")
