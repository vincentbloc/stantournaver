import os, json, html, re, shutil
import glob, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SITE = "https://stantournaver.com"
OUT = os.path.join(ROOT, "site")
CAFE = "https://cafe.naver.com/snowiii"
DATE = "2026-10-13"
DATE_DOT = "2026.10.13"
NAVER = "4d59841bb5cc538afa936d117e03fb43bd11896e"

REGION = {  # accent, dark, label
    "uz":    ("#1b9d96", "#0b4844", "우즈베키스탄"),
    "kz":    ("#2a7fd4", "#0f3c6b", "카자흐스탄"),
    "kg":    ("#c0392b", "#5a1a14", "키르기스스탄"),
    "other": ("#7a5bd6", "#2c1e5c", "타지키스탄·투르크메니스탄"),
    "prep":  ("#334155", "#0f172a", "여행 준비"),
}
CAT = {"city": "도시 가이드", "spot": "명소·자연", "nature": "자연·체험", "prep": "준비·실용"}

HUBS = []  # 도시 총정리 페이지가 생기면 여기에 추가 (chinatournaver 방식)

def load_posts():
    ps = [json.load(open(f, encoding="utf-8")) for f in sorted(glob.glob(os.path.join(ROOT, "data", "posts", "*.json")))]
    ps.sort(key=lambda p: (p["date"], -p.get("order", 0)), reverse=True)
    for p in ps:
        p["path"] = f"/travel/{p['slug']}/"
        p["accent"] = tuple(p["color"]) if p.get("color") else REGION[p["region"]][:2]
        p["thumb"] = tuple(p["thumb"]); p["faq"] = [tuple(f) for f in p["faq"]]
        p["date_dot"] = p["date"].replace("-", ".")
    return ps
POSTS = load_posts()
LATEST = max([p["date"] for p in POSTS], default=DATE)
def is_new(d):
    a = datetime.date.fromisoformat(d); b = datetime.date.fromisoformat(LATEST)
    return (b - a).days <= 6

esc = html.escape

def thumb_url(slug): return f"{SITE}/assets/thumb/{slug}.jpg"

# ───────────────────────────── 공용 CSS (글 페이지)
POST_CSS = r"""
:root{--ink:#1c2127;--soft:#56606b;--line:#e4e7eb;--bg:#fff;--alt:#f5f7f9;--naver:#03c75a;--naver2:#02a84c}
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",sans-serif;color:var(--ink);background:var(--bg);line-height:1.8;font-size:17px;word-break:keep-all}
a{color:var(--ac)}
.wrap{max-width:780px;margin:0 auto;padding:0 20px}
.topbar{border-bottom:1px solid var(--line);background:#fff}
.topbar .wrap{max-width:1040px;display:flex;align-items:center;justify-content:space-between;height:58px}
.logo{font-weight:900;font-size:18px;text-decoration:none;color:var(--ink);letter-spacing:-.02em}.logo span{color:#1f4d9e}
.top-cta{font-size:14px;font-weight:700;color:#fff;background:var(--naver);text-decoration:none;padding:7px 13px;border-radius:8px}
.crumb{font-size:13px;color:var(--soft);padding:22px 0 0}.crumb a{color:var(--soft);text-decoration:none}
.head{padding:14px 0 6px}
.badges{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:10px}
.badges span{font-size:13px;font-weight:700;padding:3px 10px;border-radius:6px;background:var(--ac);color:#fff}
.badges span.o{background:transparent;color:var(--ac);border:1px solid var(--ac)}
h1{font-size:clamp(26px,5vw,36px);line-height:1.35;letter-spacing:-.02em}
.date{font-size:14px;color:var(--soft);margin-top:10px}
.lead{font-size:18px;color:#39424c;margin-top:16px;padding-left:14px;border-left:4px solid var(--ac)}
.cover{margin:24px 0 8px;border-radius:16px;overflow:hidden;aspect-ratio:1200/630;background:var(--alt)}
.cover img{width:100%;height:100%;display:block;object-fit:cover}
article h2{font-size:clamp(21px,4vw,26px);line-height:1.4;margin:44px 0 12px;letter-spacing:-.01em}
article h3{font-size:18.5px;margin:22px 0 6px}
article p{margin:10px 0}
.note{font-size:15px;color:var(--soft)}
.summary{background:var(--alt);border-radius:14px;padding:16px 20px;margin:22px 0 0;font-size:16.5px}
.summary b{display:block;color:var(--ac);margin-bottom:2px}
.tip{background:#fff8e6;border:1px solid #f3dfa8;border-radius:12px;padding:14px 18px;margin:18px 0;font-size:16px}
.tip b{color:#a36b00;margin-right:4px}
table{width:100%;border-collapse:collapse;margin:14px 0;font-size:15.5px;display:block;overflow-x:auto}
thead th{background:var(--ac);color:#fff}
th,td{border:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}
tbody th{background:var(--alt);white-space:nowrap}
ul.check{list-style:none;margin:12px 0}
ul.check li{position:relative;padding:6px 0 6px 30px}
ul.check li::before{content:"";position:absolute;left:2px;top:13px;width:16px;height:16px;border-radius:4px;border:2px solid var(--ac)}
ul.check li::after{content:"";position:absolute;left:7px;top:15px;width:5px;height:9px;border:solid var(--ac);border-width:0 2px 2px 0;transform:rotate(45deg)}
ol.rank{list-style:none;counter-reset:r;margin:12px 0}
ol.rank li{counter-increment:r;position:relative;padding:14px 0 14px 56px;border-bottom:1px solid var(--line)}
ol.rank li::before{content:counter(r,decimal-leading-zero);position:absolute;left:0;top:10px;font-size:26px;font-weight:900;color:var(--ac)}
ol.rank b{display:block;font-size:17.5px}
ol.rank span{display:block;font-size:16px;color:var(--soft)}
ol.rank em{display:inline-block;margin-top:6px;font-style:normal;font-size:13.5px;font-weight:700;color:var(--ac);background:var(--alt);padding:2px 8px;border-radius:5px}
ol.steps{list-style:none;counter-reset:s;margin:12px 0}
ol.steps li{counter-increment:s;position:relative;padding:8px 0 8px 42px}
ol.steps li::before{content:counter(s);position:absolute;left:0;top:8px;width:28px;height:28px;border-radius:50%;background:var(--ac);color:#fff;font-weight:800;font-size:14px;display:grid;place-items:center}
.timeline{margin:14px 0 0 8px;padding-left:24px;border-left:2px solid var(--line)}
.timeline .d{position:relative;padding:0 0 18px}
.timeline .d::before{content:"";position:absolute;left:-32px;top:7px;width:12px;height:12px;border-radius:50%;background:#fff;border:3px solid var(--ac)}
.timeline .d b{display:block;color:var(--ac);font-size:15.5px}
.timeline .d span{font-size:16px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}
.chips span{font-size:14.5px;font-weight:700;background:var(--alt);border:1px solid var(--line);padding:6px 12px;border-radius:99px}
.compare3{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:14px 0}
.compare3.two{grid-template-columns:repeat(2,1fr)}
.compare3 div{border:1px solid var(--line);border-top:4px solid var(--ac);border-radius:12px;padding:16px}
.compare3 b{display:block;font-size:17px}
.compare3 em{display:block;font-style:normal;font-size:13.5px;color:var(--ac);font-weight:700;margin:2px 0 6px}
.compare3 p{font-size:15px;margin:0 0 8px}
.compare3 small{font-size:13.5px;color:var(--soft)}
.beach,.themes,.daycards{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:14px 0}
.beach div,.themes div,.daycards div{background:var(--alt);border-radius:14px;padding:16px 18px}
.beach b,.themes b,.daycards b{display:block;font-size:17px;color:var(--ac)}
.beach .lbl{display:inline-block;font-size:12.5px;font-weight:700;background:#fff;border:1px solid var(--line);border-radius:5px;padding:1px 7px;margin:4px 0 2px}
.beach p,.themes p,.daycards p{font-size:15.5px;margin:6px 0 0}
.daycards{grid-template-columns:1fr}
.bignum{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:14px 0}
.bignum div{text-align:center;border:2px solid var(--ac);border-radius:14px;padding:18px}
.bignum b{display:block;font-size:22px;color:var(--ac)}
.bignum span{font-size:16px}
.qablock h2::before,.qablock h3::before{content:"Q. ";color:var(--ac)}
.cta{margin:48px 0 0;border-radius:18px;padding:26px 24px;background:linear-gradient(135deg,#eafaf1,#f7fcf9);border:1px solid #bfe9d0;text-align:center}
.cta strong{display:block;font-size:20px;margin-bottom:6px}
.cta p{color:var(--soft);font-size:15.5px;margin-bottom:16px}
.btn{display:inline-flex;align-items:center;gap:8px;background:var(--naver);color:#fff;text-decoration:none;font-weight:700;padding:13px 22px;border-radius:10px;font-size:16.5px}
.btn:hover{background:var(--naver2)}
.btn .n{display:inline-grid;place-items:center;width:21px;height:21px;background:#fff;color:var(--naver);border-radius:5px;font-weight:900;font-size:13px}
.faq{margin-top:10px}
.faq details{border-bottom:1px solid var(--line);padding:14px 0}
.faq summary{cursor:pointer;font-weight:700;list-style:none;padding-right:24px;position:relative}
.faq summary::-webkit-details-marker{display:none}
.faq summary::after{content:"+";position:absolute;right:0;top:-2px;font-size:22px;color:var(--ac)}
.faq details[open] summary::after{content:"−"}
.faq p{color:var(--soft);font-size:16px;margin-top:8px}
.related{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:14px}
.related a{display:block;text-decoration:none;color:var(--ink);border:1px solid var(--line);border-radius:14px;overflow:hidden;background:#fff}
.related a:hover{border-color:var(--ac)}
.related img{width:100%;height:auto;aspect-ratio:1200/630;display:block;object-fit:cover}
.related span{display:block;padding:10px 14px 12px;font-size:15px;font-weight:700;line-height:1.45}
footer{margin-top:64px;padding:26px 0 110px;background:var(--alt);border-top:1px solid var(--line);font-size:14px;color:var(--soft)}
footer .wrap{max-width:1040px}footer a{color:var(--soft)}
.sticky{position:fixed;left:0;right:0;bottom:0;padding:10px 16px calc(10px + env(safe-area-inset-bottom));background:rgba(255,255,255,.96);border-top:1px solid var(--line);display:flex;justify-content:center;z-index:50;backdrop-filter:blur(6px)}
.sticky .btn{width:100%;max-width:520px;justify-content:center}
@media (max-width:640px){body{font-size:16px}.compare3,.compare3.two,.beach,.themes,.bignum,.related{grid-template-columns:1fr}.lead{font-size:16.5px}}
"""

CTA_TEXT = {
    "city": ("이 도시, 먼저 다녀온 회원들에게 물어보세요", "항공·숙소 특가, 최신 현지 소식, 동행 모집까지 카페에서 나눕니다."),
    "spot": ("투어 예약·할인 소식을 가장 먼저 받아보세요", "현지 투어 가격 비교, 실제 소요 시간 후기, 동선 팁을 카페 회원들이 공유합니다."),
    "nature": ("현지 날씨와 운영 소식, 카페에서 확인하세요", "시즌마다 달라지는 현지 정보와 회원들의 생생한 후기가 올라옵니다."),
    "prep": ("준비하다 막히면 카페에 바로 물어보세요", "환전, 교통, 입국까지 먼저 다녀온 회원들이 빠르게 답해 드립니다."),
}

def related_for(p):
    same = [x for x in POSTS if x is not p and x["region"] == p["region"]]
    hubs = [h for h in HUBS if h["region"] == p["region"]]
    others = [x for x in POSTS if x is not p and x["region"] != p["region"] and x["region"] != "prep"]
    prep = [x for x in POSTS if x["region"] == "prep" and x is not p]
    pool = same + hubs + prep[:1] + others
    out, seen = [], set()
    for x in pool:
        if x["slug"] in seen: continue
        seen.add(x["slug"]); out.append(x)
        if len(out) == 4: break
    return out

def item_title(x): return x.get("h1") or x["title"].split(" | ")[0]

# ───────────────────────────── 글 목록 게시판 (/travel/)
def board_items():
    items = []
    for p in POSTS:
        items.append(dict(path=p["path"], slug=p["slug"], city=p["city"], cat=p["cat"], title=p["title"], desc=p["desc"], ac=p["accent"][0], new=is_new(p["date"]), date=p["date"]))
    for h in reversed(HUBS):
        items.append(dict(path=h["path"], slug=h["slug"], city=h["city"], cat="city", title=h["title"], desc=h["desc"], ac=h["accent"][0], new=False, date=DATE))
    return items

def render_index():
    items = board_items()
    lis = []
    for it in items:
        t = re.sub(r"\s*\(20\d\d\)\s*$", "", it["title"])
        lis.append(f'''<li data-cat="{it['cat']}"><a href="{it['path']}">
<img src="/assets/thumb/{it['slug']}.jpg" alt="{esc(t)}" loading="lazy" width="1200" height="630">
<div class="txt"><div class="meta"><span class="cat" style="background:{it['ac']}">{esc(it['city'])}</span><span class="kind">{CAT[it['cat']]}</span>{'<span class="new">NEW</span>' if it['new'] else ''}<span class="date">{it['date'].replace('-', '.')}</span></div>
<h3>{esc(t)}</h3><p>{esc(it['desc'])}</p></div></a></li>''')
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "중앙아시아 여행 글 모음", "url": SITE + "/travel/", "inLanguage": "ko-KR",
         "isPartOf": {"@type": "WebSite", "name": "중앙아시아 여행 가이드", "url": SITE + "/"}},
        {"@type": "ItemList", "name": "최신 중앙아시아 여행 글", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": SITE + it["path"], "name": it["title"]} for i, it in enumerate(items)]}]}
    filt = "".join(f'<button type="button" data-f="{k}" aria-pressed="false" id="{k}">{v}</button>' for k, v in CAT.items())
    # 인기 검색어·도시 링크는 실제로 존재하는 글에서만 만든다 (깨진 링크 방지)
    pop = "".join(f'<a href="{p["path"]}">{esc(p["city"])}</a>' for p in POSTS[:10])
    empty_note = '' if items else '<li style="padding:40px 20px;color:#5a6169">첫 글을 준비하고 있습니다. 곧 중앙아시아 도시별 가이드가 올라옵니다.</li>'
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>중앙아시아 여행 글 모음 | 우즈베키스탄·카자흐스탄·키르기스스탄 최신 가이드</title>
<meta name="description" content="중앙아시아 자유여행 최신 글 모음. 타슈켄트, 사마르칸트, 알마티, 비슈케크 등 도시별 코스와 경비, 교통·환전·유심 준비 정보를 계속 올립니다.">
<meta name="keywords" content="중앙아시아 여행, 우즈베키스탄 여행, 카자흐스탄 여행, 키르기스스탄 여행, 타슈켄트, 사마르칸트, 알마티, 비슈케크">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{SITE}/travel/">
<link rel="alternate" type="application/rss+xml" title="중앙아시아 여행 가이드" href="{SITE}/rss.xml">
<link rel="icon" href="/assets/logo.png">
<meta name="naver-site-verification" content="{NAVER}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="중앙아시아 여행 가이드">
<meta property="og:title" content="중앙아시아 여행 글 모음 | 도시별 최신 가이드">
<meta property="og:description" content="타슈켄트, 사마르칸트, 알마티, 비슈케크 등 중앙아시아 도시별 코스·경비·준비 정보 최신 글.">
<meta property="og:url" content="{SITE}/travel/">
<meta property="og:image" content="{thumb_url('og-main')}">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{thumb_url('og-main')}">
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<style>
:root{{--brand:#1f4d9e;--naver:#03c75a;--naver2:#02a84c;--ink:#1c1f23;--soft:#5a6169;--line:#e6e8eb;--alt:#f6f7f9}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"Pretendard","Apple SD Gothic Neo","Malgun Gothic","Noto Sans KR",sans-serif;color:var(--ink);background:var(--alt);line-height:1.6;word-break:keep-all}}
a{{color:inherit}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
.topbar{{background:#fff;border-bottom:1px solid var(--line)}}
.topbar .wrap{{display:flex;align-items:center;justify-content:space-between;height:60px}}
.logo{{font-weight:900;font-size:19px;text-decoration:none;letter-spacing:-.02em}}.logo span{{color:var(--brand)}}
.top-cta{{font-size:14px;font-weight:700;color:#fff;background:var(--naver);text-decoration:none;padding:8px 14px;border-radius:8px}}
.hero{{background:#fff;border-bottom:1px solid var(--line);padding:28px 0 24px}}
.hero h1{{font-size:clamp(24px,4.4vw,32px);line-height:1.35;letter-spacing:-.02em}}
.hero p{{color:var(--soft);margin-top:10px;font-size:16px}}
.hero p a{{color:var(--brand);font-weight:700}}
.layout{{display:grid;grid-template-columns:1fr 300px;gap:24px;padding:26px 0 60px;align-items:start}}
.board{{background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden}}
.board-head{{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:16px 18px;border-bottom:1px solid var(--line);flex-wrap:wrap}}
.board-head h2{{font-size:19px}}
.board-head h2 small{{font-size:14px;color:var(--soft);font-weight:500;margin-left:6px}}
.filters{{display:flex;flex-wrap:wrap;gap:6px}}
.filters button{{font:inherit;font-size:13.5px;border:1px solid var(--line);background:#fff;border-radius:99px;padding:5px 12px;cursor:pointer;color:var(--soft)}}
.filters button[aria-pressed="true"]{{background:var(--ink);color:#fff;border-color:var(--ink)}}
.posts{{list-style:none}}
.posts li{{border-bottom:1px solid var(--line)}}
.posts li:last-child{{border:0}}
.posts a{{display:grid;grid-template-columns:200px 1fr;gap:18px;padding:16px 18px;text-decoration:none;align-items:start}}
.posts a:hover{{background:var(--alt)}}
.posts img{{width:200px;height:auto;aspect-ratio:1200/630;object-fit:cover;border-radius:10px;display:block;background:var(--alt)}}
.meta{{display:flex;gap:6px;align-items:center;font-size:12.5px;color:var(--soft);flex-wrap:wrap}}
.cat{{font-weight:800;color:#fff;padding:1px 8px;border-radius:5px}}
.kind{{font-weight:700}}
.new{{font-size:11px;font-weight:800;color:var(--brand);border:1px solid var(--brand);padding:0 5px;border-radius:4px}}
.date{{margin-left:auto}}
.posts h3{{font-size:17px;line-height:1.45;margin:5px 0 4px}}
.posts p{{font-size:14px;color:var(--soft);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.more{{display:none;width:100%;font:inherit;font-weight:700;font-size:15px;padding:14px;border:0;border-top:1px solid var(--line);background:#fff;cursor:pointer}}
.more:hover{{background:var(--alt)}}
aside{{display:grid;gap:16px;position:sticky;top:16px}}
.box{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:18px}}
.box h2{{font-size:16px;margin-bottom:10px}}
.cafe{{background:linear-gradient(160deg,#eafaf1,#fff);border-color:#bfe9d0}}
.cafe p{{font-size:14.5px;color:var(--soft);margin-bottom:10px}}
.cafe ul{{list-style:none;font-size:14px;margin-bottom:14px}}
.cafe li{{padding:4px 0 4px 18px;position:relative}}
.cafe li::before{{content:"";position:absolute;left:2px;top:12px;width:7px;height:7px;border-radius:50%;background:var(--naver)}}
.btn{{display:flex;align-items:center;justify-content:center;gap:8px;background:var(--naver);color:#fff;text-decoration:none;font-weight:700;padding:12px 16px;border-radius:10px;font-size:15.5px}}
.btn:hover{{background:var(--naver2)}}
.btn .n{{display:inline-grid;place-items:center;width:20px;height:20px;background:#fff;color:var(--naver);border-radius:5px;font-weight:900;font-size:13px}}
.info li{{list-style:none;font-size:14px;padding:7px 0;border-bottom:1px dashed var(--line);display:flex;justify-content:space-between;gap:10px}}
.info li:last-child{{border:0}}
.tags{{display:flex;flex-wrap:wrap;gap:6px}}
.tags a{{font-size:13px;background:var(--alt);border-radius:6px;padding:4px 9px;text-decoration:none;color:var(--soft)}}
.tags a:hover{{color:var(--ink)}}
footer{{background:#fff;border-top:1px solid var(--line);padding:26px 0 40px;font-size:13.5px;color:var(--soft)}}
footer a{{color:var(--soft)}}
@media (max-width:900px){{.layout{{grid-template-columns:1fr}}aside{{position:static}}}}
@media (max-width:560px){{.posts a{{grid-template-columns:110px 1fr;gap:12px;padding:14px}}.posts img{{width:110px}}.posts p{{display:none}}.posts h3{{font-size:15.5px}}.date{{display:none}}}}
</style>
</head>
<body>
<div class="topbar"><div class="wrap"><a class="logo" href="/">중앙아시아<span>여행</span>가이드</a><a class="top-cta" href="{CAFE}" target="_blank" rel="noopener">카페 가입</a></div></div>

<section class="hero"><div class="wrap">
<h1>중앙아시아 여행 글 모음</h1>
<p>우즈베키스탄, 카자흐스탄, 키르기스스탄 도시별 코스·경비·준비 정보를 계속 올립니다. 처음이라면 <a href="/">중앙아시아 여행 가이드 총정리</a>부터 보세요.</p>
</div></section>

<div class="wrap layout">
<main>
<div class="board">
<div class="board-head">
<h2>최신 여행 글 <small>{len(items)}개</small></h2>
<div class="filters" role="group" aria-label="주제 필터"><button type="button" data-f="all" aria-pressed="true">전체</button>{filt}</div>
</div>
<!-- 새 글은 build 스크립트로 추가하면 목록·사이트맵·RSS가 함께 갱신됩니다 -->
<ul class="posts" id="posts">
{empty_note}{chr(10).join(lis)}
</ul>
<button class="more" id="more" type="button">더 보기</button>
</div>
</main>

<aside>
<div class="box cafe"><h2>중앙아시아 여행 카페</h2><p>글에 다 담지 못한 실시간 정보는 네이버 카페에서 나눕니다.</p>
<ul><li>항공권·투어 특가 소식</li><li>회원들의 실제 여행 후기</li><li>여행 질문과 동행 모집</li><li>도시별 최신 현지 소식</li></ul>
<a class="btn" href="{CAFE}" target="_blank" rel="noopener"><span class="n">N</span>무료로 가입하기</a></div>
<div class="box"><h2>중앙아시아 기본 정보</h2><ul class="info">
<li><span>비자</span><b>4개국 무비자</b></li><li><span>시차</span><b>한국보다 3~4시간 느림</b></li>
<li><span>직항</span><b>인천·부산 출발</b></li><li><span>필수 앱</span><b>얀덱스 고·번역</b></li></ul></div>
{f'<div class="box"><h2>최근 다룬 도시</h2><div class="tags">{pop}</div></div>' if pop else ''}
</aside>
</div>

<footer><div class="wrap"><p>© stantournaver.com · 중앙아시아 여행 가이드. 게시된 정보는 작성일 기준이며 비자·요금·운영 시간은 바뀔 수 있습니다.</p>
<p>최신 중앙아시아 여행 정보: <a href="{CAFE}" target="_blank" rel="noopener">cafe.naver.com/snowiii</a> · <a href="/rss.xml">RSS</a> · <a href="/sitemap.xml">사이트맵</a></p></div></footer>

<script>
(function(){{
  var PAGE=10, limit=PAGE, f='all';
  var btns=[].slice.call(document.querySelectorAll('.filters button'));
  var items=[].slice.call(document.querySelectorAll('#posts li[data-cat]'));
  var more=document.getElementById('more');
  function draw(){{
    var match=items.filter(function(li){{return f==='all'||li.getAttribute('data-cat')===f;}});
    items.forEach(function(li){{li.style.display='none';}});
    match.forEach(function(li,i){{if(i<limit)li.style.display='';}});
    more.style.display=match.length>limit?'block':'none';
  }}
  btns.forEach(function(b){{b.addEventListener('click',function(){{
    f=b.getAttribute('data-f');limit=PAGE;
    btns.forEach(function(x){{x.setAttribute('aria-pressed',x===b?'true':'false');}});draw();
  }});}});
  more.addEventListener('click',function(){{limit+=PAGE;draw();}});
  var h=location.hash.slice(1); var hb=btns.filter(function(b){{return b.getAttribute('data-f')===h;}})[0];
  if(hb){{hb.click();}}else{{draw();}}
}})();
</script>
</body>
</html>
"""

# ───────────────────────────── 랜딩페이지(메인)에 최신 글 블록 주입
def patch_landing():
    f = os.path.join(OUT, "index.html")
    s = open(f, encoding="utf-8").read()
    card = lambda x: (f'<a href="{x["path"]}" style="display:block;text-decoration:none;color:inherit;border:1px solid #e7dfcd;border-radius:14px;overflow:hidden;background:#fff">'
                      f'<img src="/assets/thumb/{x["slug"]}.jpg" alt="{esc(item_title(x))}" loading="lazy" width="1200" height="630" style="width:100%;height:auto;display:block">'
                      f'<span style="display:block;padding:10px 14px 12px;font-size:15px;font-weight:700;line-height:1.5">{esc(item_title(x))}</span></a>')
    latest = POSTS[:6]
    if latest:
        cards = "".join(card(x) for x in latest)
        block = (f'\n<section id="latest" data-tone="lapis"><div class="h2-band"><h2>최신 중앙아시아 여행 글</h2></div>'
                 f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px">{cards}</div>'
                 f'<p style="margin-top:14px"><a href="/travel/">전체 글 보기 →</a></p></section>\n')
    else:
        block = '\n'
    s = re.sub(r"\n?<!-- latest-start -->.*?<!-- latest-end -->\n?",
               "\n<!-- latest-start -->" + block + "<!-- latest-end -->\n", s, flags=re.S)
    open(f, "w", encoding="utf-8").write(s)

def write_feeds():
    urls = ["/", "/travel/"] + [h["path"] for h in HUBS] + [p["path"] for p in POSTS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
    for u in urls:
        slug = "og-main" if u in ("/", "/travel/") else u.strip("/").split("/")[-1]
        sm += f"  <url><loc>{SITE}{u}</loc><lastmod>{LATEST}</lastmod><image:image><image:loc>{thumb_url(slug)}</image:loc></image:image></url>\n"
    sm += "</urlset>\n"
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write(sm)
    items = board_items() or [dict(title="중앙아시아 여행 가이드 2026 — 코스·경비·비자·직항 총정리", path="/", slug="og-main",
                                   desc="우즈베키스탄·카자흐스탄·키르기스스탄 무비자 조건, 직항 노선, 추천 코스와 경비 총정리.", date=DATE)]
    rss = f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n  <channel>\n    <title>중앙아시아 여행 가이드 | stantournaver.com</title>\n    <link>{SITE}/</link>\n    <description>우즈베키스탄, 카자흐스탄, 키르기스스탄 등 중앙아시아 도시별 자유여행 코스·경비·비자·직항 정보</description>\n    <language>ko</language>\n    <lastBuildDate>{datetime.date.fromisoformat(LATEST).strftime("%a, %d %b %Y")} 21:00:00 +0900</lastBuildDate>\n'
    for i, it in enumerate(items):
        hh, mm = divmod(21 * 60 - (i % 60) * 10, 60)
        dt = datetime.date.fromisoformat(it["date"]).strftime("%a, %d %b %Y")
        rss += f"    <item>\n      <title>{esc(it['title'])}</title>\n      <link>{SITE}{it['path']}</link>\n      <guid>{SITE}{it['path']}</guid>\n      <description>{esc(it['desc'])}</description>\n      <enclosure url=\"{thumb_url(it['slug'])}\" type=\"image/jpeg\" length=\"0\"/>\n      <pubDate>{dt} {hh:02d}:{mm:02d}:00 +0900</pubDate>\n    </item>\n"
    rss += "  </channel>\n</rss>\n"
    open(os.path.join(OUT, "rss.xml"), "w", encoding="utf-8").write(rss)
