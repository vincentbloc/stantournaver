"""배포 전 검사. 문제가 있으면 exit 1 → 푸시하지 않는다."""
import os, re, json, glob, sys, xml.dom.minidom as m
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
sys.path.insert(0, os.path.join(ROOT, "src"))
from scenes import SCENES
from infographics import RENDER

err, warn = [], []
REQ = ["slug", "city", "region", "cat", "title", "h1", "desc", "kw", "thumb", "lead", "body", "faq", "date", "x"]
slugs = set()
for f in sorted(glob.glob(os.path.join(ROOT, "data", "posts", "*.json"))):
    n = os.path.basename(f)
    try: p = json.load(open(f, encoding="utf-8"))
    except Exception as e: err.append(f"{n}: JSON 오류 {e}"); continue
    for k in REQ:
        if k not in p: err.append(f"{n}: 필드 없음 {k}")
    if not all(k in p for k in REQ): continue
    if p["slug"] in slugs: err.append(f"{n}: slug 중복 {p['slug']}")
    slugs.add(p["slug"])
    if not re.fullmatch(r"[a-z0-9-]+", p["slug"]): err.append(f"{n}: slug 형식")
    if p["region"] not in ("uz", "kz", "kg", "other", "prep"): err.append(f"{n}: region 값")
    if p["cat"] not in ("city", "spot", "nature", "prep"): err.append(f"{n}: cat 값")
    x = p["x"]
    for k in ("scene", "stitle", "facts", "imgs", "tips"):
        if k not in x: err.append(f"{n}: x.{k} 없음")
    if x.get("scene") not in SCENES: err.append(f"{n}: scene 없음 {x.get('scene')}")
    h2n = len(re.findall(r"<h2>", p["body"]))
    if h2n < 3: err.append(f"{n}: h2가 3개 미만")
    for s in x.get("imgs", []):
        if s.get("type") not in RENDER: err.append(f"{n}: 이미지 type {s.get('type')}")
        if not (0 <= s.get("after", -1) < h2n): err.append(f"{n}: 이미지 after 범위 {s.get('after')}")
    if len(x.get("tips", {}).get("items", [])) != 4: err.append(f"{n}: tips는 4개")
    if len(p["faq"]) < 3: err.append(f"{n}: FAQ 3개 이상")
    plain = re.sub("<[^>]+>", "", p["body"])
    if len(plain) < 600: err.append(f"{n}: 본문이 너무 짧음 ({len(plain)}자)")
    if p["date"] > "2026-10-13":  # 자동 작성 글은 더 높은 기준
        if len(plain) < 2000: err.append(f"{n}: 본문 2,000자 미만 ({len(plain)}자)")
        if h2n < 5: err.append(f"{n}: h2 5개 이상 필요")
        if len(p["faq"]) < 4: err.append(f"{n}: FAQ 4개 이상 필요")
        links = set(re.findall(r'href="(/[^"#]+)"', p["body"]))
        if len(links) < 2: err.append(f"{n}: 내부 링크 2개 이상 필요")
        if len(p.get("sources", [])) < 3: err.append(f"{n}: sources(참고 출처) 3개 이상 필요")
    if len(x.get("stitle", "")) > 45: warn.append(f"{n}: 제목이 김 ({len(x['stitle'])}자)")
    if not (60 <= len(p["desc"]) <= 160): warn.append(f"{n}: 설명 길이 {len(p['desc'])}자")
    han = re.findall(r"[一-鿿]", plain)
    if len(han) > 6: warn.append(f"{n}: 한자 {len(han)}자 (한국어로 풀어 쓰기)")
    for q, a in p["faq"]:
        if len(a) < 20: warn.append(f"{n}: FAQ 답변 짧음")

# 사이트 결과물 검사
try:
    m.parse(os.path.join(SITE, "sitemap.xml")); m.parse(os.path.join(SITE, "rss.xml"))
except Exception as e: err.append(f"sitemap/rss XML 오류 {e}")
pages = glob.glob(os.path.join(SITE, "index.html")) + glob.glob(os.path.join(SITE, "*", "index.html")) + glob.glob(os.path.join(SITE, "travel", "*", "index.html"))
for f in pages:
    h = open(f, encoding="utf-8").read(); rel = os.path.relpath(f, SITE)
    for j in re.findall(r'ld\+json">(.*?)</script>', h, re.S):
        try: json.loads(j)
        except Exception: err.append(f"{rel}: JSON-LD 오류")
    if h.count("<h1") != 1: err.append(f"{rel}: h1 개수")
    for l in set(re.findall(r'(?:href|src)="(/[^"#]*)', h)):
        pth = l.lstrip("/")
        if not pth: continue
        t = pth + "index.html" if pth.endswith("/") else pth
        if not os.path.exists(os.path.join(SITE, t)): err.append(f"{rel}: 깨진 링크 {l}")
    if rel.startswith("travel" + os.sep) and rel != os.path.join("travel", "index.html"):
        for a in re.findall(r'href="#([^"]+)"', h):
            if f'id="{a}"' not in h: err.append(f"{rel}: 목차 앵커 {a}")
for s in slugs:
    if not os.path.exists(os.path.join(SITE, "travel", s, "index.html")): err.append(f"페이지 없음 {s}")

for w in warn: print("경고:", w)
for e in err: print("오류:", e)
print(f"글 {len(slugs)}개, 페이지 {len(pages)}개 검사 — 오류 {len(err)} / 경고 {len(warn)}")
sys.exit(1 if err else 0)
