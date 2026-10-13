# 알록달록한 본문 인포그래픽 HTML (가로 1200px, Playwright로 JPG 렌더)
import html
esc = html.escape
PAL = [("#FF6B6B", "#FFE8E8"), ("#FFA41B", "#FFF2DC"), ("#20C997", "#DDF7EF"),
       ("#4D96FF", "#E3EEFF"), ("#9B5DE5", "#F0E6FF"), ("#F15BB5", "#FDE4F2"),
       ("#00B4D8", "#DDF6FB"), ("#7CB518", "#EDF7DC")]

BASE = """<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;font-family:'Noto Sans CJK KR','Noto Color Emoji',sans-serif;color:#1d2330;background:#fff;word-break:keep-all}
.frame{position:relative;padding:64px 70px 70px;background:linear-gradient(135deg,#fff7ec 0%,#f3f0ff 50%,#e9f8ff 100%);overflow:hidden}
.dots span{position:absolute;border-radius:50%;opacity:.55}
.head{position:relative;display:flex;align-items:center;gap:18px;margin-bottom:40px}
.head .em{font-size:54px;line-height:1}
.head h1{font-size:56px;font-weight:900;letter-spacing:-.02em;line-height:1.2}
.head h1 u{text-decoration:none;background:linear-gradient(transparent 62%,#ffe066 62%)}
.brand{position:absolute;right:40px;bottom:24px;font-size:20px;font-weight:700;color:#8a8fa3}
.emo{font-family:'Noto Color Emoji'}
@@CSS@@
</style></head><body><div class="frame" id="cap">
<div class="dots"><span style="width:180px;height:180px;background:#ffd6e7;right:-50px;top:-40px"></span><span style="width:120px;height:120px;background:#d6f5ff;left:-30px;bottom:-30px"></span><span style="width:60px;height:60px;background:#fff0b3;right:160px;bottom:60px"></span></div>
<div class="head"><span class="em emo">@@EM@@</span><h1><u>@@TITLE@@</u></h1></div>
@@BODY@@
<div class="brand">stantournaver.com · 중앙아시아 여행 가이드</div>
</div></body></html>"""

def page(css, emoji, title, body):
    return BASE.replace("@@CSS@@", css).replace("@@EM@@", emoji).replace("@@TITLE@@", esc(title)).replace("@@BODY@@", body)

def facts(spec):
    n = len(spec["items"]); cols = 3 if n in (3, 6, 9) else 2
    css = f""".grid{{display:grid;grid-template-columns:repeat({cols},1fr);gap:22px;position:relative}}
.t{{border-radius:26px;padding:28px 26px;min-height:190px;box-shadow:0 6px 0 rgba(0,0,0,.06)}}
.t .ic{{width:84px;height:84px;border-radius:24px;display:grid;place-items:center;font-size:48px;margin-bottom:16px;background:#fff}}
.t small{{display:block;font-size:30px;font-weight:700;opacity:.85}}
.t b{{display:block;font-size:{38 if cols==3 else 44}px;font-weight:900;line-height:1.25;margin-top:4px;letter-spacing:-.01em}}"""
    tiles = ""
    for i, (em, lab, val) in enumerate(spec["items"]):
        c, bg = PAL[i % len(PAL)]
        tiles += f'<div class="t" style="background:{bg};color:{c}"><div class="ic emo">{em}</div><small>{esc(lab)}</small><b style="color:#1d2330">{esc(val)}</b></div>'
    return page(css, "📌", spec["title"], f'<div class="grid">{tiles}</div>')

def steps(spec):
    css = """.row{position:relative;display:flex;align-items:center;gap:26px;margin-bottom:22px}
.num{flex:0 0 96px;height:96px;border-radius:50%;display:grid;place-items:center;color:#fff;font-size:40px;font-weight:900;box-shadow:0 6px 0 rgba(0,0,0,.12)}
.card{flex:1;background:#fff;border-radius:24px;padding:24px 30px;border:3px solid}
.card b{display:block;font-size:34px;font-weight:900}
.card span{display:block;font-size:28px;color:#4a5263;margin-top:2px}
.line{position:absolute;left:47px;top:96px;width:4px;height:26px}"""
    rows = ""
    for i, (a, b) in enumerate(spec["items"]):
        c, bg = PAL[i % len(PAL)]
        rows += f'<div class="row"><div class="num" style="background:{c}">{i+1}</div><div class="card" style="border-color:{bg}"><b style="color:{c}">{esc(a)}</b><span>{esc(b)}</span></div></div>'
    return page(css, "🧭", spec["title"], rows)

def compare(spec):
    n = len(spec["cols"])
    css = f""".cols{{display:grid;grid-template-columns:repeat({n},1fr);gap:24px;position:relative}}
.c{{background:#fff;border-radius:28px;overflow:hidden;box-shadow:0 8px 0 rgba(0,0,0,.06)}}
.c .top{{padding:28px 20px;text-align:center;color:#fff}}
.c .top .emo{{font-size:60px;display:block}}
.c .top b{{display:block;font-size:{40 if n==2 else 36}px;font-weight:900;margin-top:6px}}
.c ul{{list-style:none;padding:22px 28px 30px}}
.c li{{font-size:{30 if n==2 else 27}px;padding:12px 0 12px 40px;position:relative;border-bottom:2px dashed #eceef3;line-height:1.35}}
.c li:last-child{{border:0}}
.c li::before{{content:"";position:absolute;left:4px;top:22px;width:18px;height:18px;border-radius:50%}}"""
    body = ""
    for i, (em, name, items) in enumerate(spec["cols"]):
        c, bg = PAL[(i * 2 + 3) % len(PAL)]
        lis = "".join(f'<li style="--c:{c}"><i style="position:absolute;left:4px;top:22px;width:18px;height:18px;border-radius:50%;background:{c}"></i>{esc(t)}</li>' for t in items)
        body += f'<div class="c"><div class="top" style="background:{c}"><span class="emo">{em}</span><b>{esc(name)}</b></div><ul>{lis}</ul></div>'
    css = css.replace('.c li::before{content:"";position:absolute;left:4px;top:22px;width:18px;height:18px;border-radius:50%}', "")
    return page(css, "⚖️", spec["title"], f'<div class="cols">{body}</div>')

def rank(spec):
    css = """.r{display:flex;align-items:center;gap:24px;background:#fff;border-radius:24px;padding:18px 26px;margin-bottom:16px;box-shadow:0 5px 0 rgba(0,0,0,.05);position:relative}
.r .n{flex:0 0 80px;height:80px;border-radius:24px;display:grid;place-items:center;color:#fff;font-size:40px;font-weight:900}
.r b{flex:1;font-size:34px;font-weight:900;letter-spacing:-.01em}
.r em{font-style:normal;font-size:26px;font-weight:800;padding:8px 18px;border-radius:99px}"""
    rows = ""
    medals = {0: "🥇", 1: "🥈", 2: "🥉"}
    for i, (name, tag) in enumerate(spec["items"]):
        c, bg = PAL[i % len(PAL)]
        num = f'<span class="emo" style="font-size:48px">{medals[i]}</span>' if i in medals else str(i + 1)
        rows += f'<div class="r"><div class="n" style="background:{bg if i in medals else c}">{num}</div><b>{esc(name)}</b><em style="background:{bg};color:{c}">{esc(tag)}</em></div>'
    return page(css, "🏆", spec["title"], rows)

def checklist(spec):
    css = """.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;position:relative}
.it{display:flex;align-items:center;gap:20px;background:#fff;border-radius:22px;padding:22px 24px;border:3px solid}
.it .emo{font-size:46px}
.it b{flex:1;font-size:31px;font-weight:800;line-height:1.3}
.it .ck{width:46px;height:46px;border-radius:12px;display:grid;place-items:center;color:#fff;font-size:30px;font-weight:900}"""
    items = ""
    for i, (em, t) in enumerate(spec["items"]):
        c, bg = PAL[i % len(PAL)]
        items += f'<div class="it" style="border-color:{bg}"><span class="emo">{em}</span><b>{esc(t)}</b><span class="ck" style="background:{c}">✓</span></div>'
    return page(css, "✅", spec["title"], f'<div class="grid">{items}</div>')

def tips(spec, title):
    css = """.notes{display:grid;grid-template-columns:1fr 1fr;gap:34px 30px;position:relative;padding:10px 6px}
.nt{position:relative;border-radius:10px;padding:44px 32px 34px;box-shadow:0 12px 22px rgba(0,0,0,.08);min-height:250px}
.nt .tape{position:absolute;top:-14px;left:50%;width:120px;height:30px;margin-left:-60px;background:rgba(255,255,255,.7);border-radius:4px}
.nt .emo{font-size:52px;display:block}
.nt b{display:block;font-size:40px;font-weight:900;margin:10px 0 8px;letter-spacing:-.01em}
.nt p{font-size:31px;line-height:1.45;color:#39404f}"""
    rot = [-2, 1.5, 1.2, -1.5]
    notes = ""
    for i, (em, h, p) in enumerate(spec["items"]):
        c, bg = PAL[(i * 2 + 1) % len(PAL)]
        notes += f'<div class="nt" style="background:{bg};transform:rotate({rot[i%4]}deg)"><span class="tape"></span><span class="emo">{em}</span><b style="color:{c}">{esc(h)}</b><p>{esc(p)}</p></div>'
    return page(css, "💡", title, f'<div class="notes">{notes}</div>')

def timebar(spec):
    css = """.tb{display:grid;gap:20px;position:relative}
.row{display:grid;grid-template-columns:260px 1fr;gap:24px;align-items:center}
.row .tm{font-size:32px;font-weight:900}
.bar{height:92px;border-radius:24px;background:#fff;position:relative;overflow:hidden;box-shadow:inset 0 0 0 3px #eef0f5}
.fill{position:absolute;left:0;top:0;bottom:0;border-radius:24px;display:flex;align-items:center;padding-left:28px;font-size:30px;font-weight:800;color:#fff}
.stars{position:absolute;right:24px;top:50%;transform:translateY(-50%);font-size:38px}"""
    rows = ""
    cols = ["#20C997", "#FFA41B", "#9aa3b5"]
    for i, (tm, desc, lv) in enumerate(spec["items"]):
        c = cols[3 - lv] if lv in (1, 2, 3) else "#999"
        rows += f'<div class="row"><div class="tm">{esc(tm)}</div><div class="bar"><div class="fill" style="width:{[0,40,68,100][lv]}%;background:{c}">{esc(desc)}</div><span class="stars emo">{"⭐"*lv}</span></div></div>'
    return page(css, "⏰", spec["title"], f'<div class="tb">{rows}</div>')

def months(spec):
    css = """.m{display:grid;grid-template-columns:repeat(6,1fr);gap:16px;position:relative}
.m div{border-radius:22px;padding:26px 0;text-align:center;font-size:34px;font-weight:900;color:#fff}
.lg{display:flex;gap:30px;margin-top:30px;font-size:28px;font-weight:700;position:relative}
.lg i{display:inline-block;width:28px;height:28px;border-radius:8px;margin-right:10px;vertical-align:-4px}"""
    col = {3: "#20C997", 2: "#FFA41B", 1: "#FF6B6B"}
    cells = "".join(f'<div style="background:{col[l]}">{i+1}월</div>' for i, l in enumerate(spec["levels"]))
    a, b, c = spec["legend"]
    lg = f'<div class="lg"><span><i style="background:#20C997"></i>{esc(a)}</span><span><i style="background:#FFA41B"></i>{esc(b)}</span><span><i style="background:#FF6B6B"></i>{esc(c)}</span></div>'
    return page(css, "📅", spec["title"], f'<div class="m">{cells}</div>{lg}')

RENDER = {"facts": facts, "steps": steps, "compare": compare, "rank": rank, "checklist": checklist, "timebar": timebar, "months": months}
