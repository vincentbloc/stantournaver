# 600x630 컬러 일러스트 장면 (일반적인 풍경·사물, 특정 캐릭터·로고 없음)
def sky(id_, top, bottom):
    return f'<defs><linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset="1" stop-color="{bottom}"/></linearGradient></defs><rect width="600" height="630" fill="url(#{id_})"/>'

def stars(n=26, seed=3):
    import random
    r = random.Random(seed); s = ""
    for _ in range(n):
        s += f'<circle cx="{r.randint(10,590)}" cy="{r.randint(10,300)}" r="{r.choice([1.5,2,2.5,3])}" fill="#fff" opacity="{r.choice([.5,.7,.9])}"/>'
    return s

def burst(cx, cy, r, color):
    import math
    s = ""
    for i in range(16):
        a = i * math.pi / 8
        s += f'<line x1="{cx+math.cos(a)*r*.3:.0f}" y1="{cy+math.sin(a)*r*.3:.0f}" x2="{cx+math.cos(a)*r:.0f}" y2="{cy+math.sin(a)*r:.0f}" stroke="{color}" stroke-width="5" stroke-linecap="round"/>'
        s += f'<circle cx="{cx+math.cos(a)*r*1.12:.0f}" cy="{cy+math.sin(a)*r*1.12:.0f}" r="4" fill="{color}"/>'
    return s

def balloon(x, y, c):
    return f'<ellipse cx="{x}" cy="{y}" rx="22" ry="28" fill="{c}"/><path d="M{x} {y+28} q-6 30 4 60" stroke="#fff" stroke-width="2" fill="none" opacity=".8"/>'

SCENES = {}

SCENES["castle_park"] = sky("g1", "#3b1e7a", "#ff8fb1") + stars(20) + burst(140, 120, 60, "#ffd23f") + burst(460, 90, 50, "#3ee6c8") + burst(330, 170, 38, "#ff5d8f") + """
<g fill="#fff3fb">
<rect x="170" y="330" width="260" height="220"/>
<rect x="250" y="220" width="100" height="330"/>
<rect x="150" y="300" width="60" height="250"/><rect x="390" y="300" width="60" height="250"/>
</g>
<polygon points="250,222 300,110 350,222" fill="#5b7cfa"/>
<polygon points="146,302 180,230 214,302" fill="#ff6fa5"/><polygon points="386,302 420,230 454,302" fill="#ff6fa5"/>
<polygon points="200,334 230,280 260,334" fill="#9b5de5"/><polygon points="340,334 370,280 400,334" fill="#9b5de5"/>
<line x1="300" y1="110" x2="300" y2="70" stroke="#fff" stroke-width="4"/><polygon points="300,70 336,82 300,94" fill="#ffd23f"/>
<rect x="276" y="470" width="48" height="80" rx="24" fill="#7b5ad6"/>
<g fill="#ffd23f"><rect x="285" y="270" width="30" height="40" rx="15"/><rect x="170" y="380" width="22" height="30" rx="11"/><rect x="408" y="380" width="22" height="30" rx="11"/></g>
<rect x="0" y="550" width="600" height="80" fill="#6a3fb5"/>
""" + balloon(70, 420, "#ff5d8f") + balloon(520, 440, "#3ec1ff") + balloon(560, 380, "#ffd23f")

SCENES["city_night"] = sky("g2", "#0b1340", "#4b2a8f") + stars(30) + """
<g>
<rect x="20" y="300" width="60" height="230" fill="#2a3a8f"/><rect x="90" y="250" width="50" height="280" fill="#3b2f9a"/>
<rect x="150" y="330" width="70" height="200" fill="#26307a"/>
<rect x="400" y="220" width="55" height="310" fill="#2f3fa8"/><rect x="465" y="170" width="50" height="360" fill="#433bb0"/>
<polygon points="465,170 490,120 515,170" fill="#433bb0"/>
<rect x="525" y="280" width="60" height="250" fill="#2a3a8f"/>
<line x1="300" y1="80" x2="300" y2="530" stroke="#c6b8ff" stroke-width="10"/>
<line x1="270" y1="530" x2="300" y2="300" stroke="#c6b8ff" stroke-width="7"/><line x1="330" y1="530" x2="300" y2="300" stroke="#c6b8ff" stroke-width="7"/>
<circle cx="300" cy="330" r="48" fill="#ff4fa3"/><circle cx="300" cy="190" r="32" fill="#ff4fa3"/><circle cx="300" cy="120" r="12" fill="#ffd23f"/>
</g>
<g fill="#ffe27a" opacity=".9">
<rect x="32" y="320" width="10" height="10"/><rect x="56" y="360" width="10" height="10"/><rect x="100" y="280" width="10" height="10"/><rect x="118" y="330" width="10" height="10"/>
<rect x="170" y="360" width="10" height="10"/><rect x="195" y="400" width="10" height="10"/><rect x="412" y="250" width="10" height="10"/><rect x="430" y="300" width="10" height="10"/>
<rect x="478" y="210" width="10" height="10"/><rect x="495" y="260" width="10" height="10"/><rect x="540" y="320" width="10" height="10"/><rect x="560" y="370" width="10" height="10"/>
</g>
<rect x="0" y="530" width="600" height="100" fill="#1b1f6b"/>
<g stroke-width="6" stroke-linecap="round" opacity=".8"><line x1="280" y1="555" x2="320" y2="555" stroke="#ff4fa3"/><line x1="60" y1="570" x2="110" y2="570" stroke="#3ee6c8"/><line x1="440" y1="575" x2="500" y2="575" stroke="#ffd23f"/><line x1="270" y1="595" x2="330" y2="595" stroke="#ff4fa3"/></g>
"""

SCENES["water_town"] = sky("g3", "#bdefff", "#fff4d6") + """
<circle cx="480" cy="120" r="50" fill="#ffcf5c"/>
<g><rect x="20" y="250" width="160" height="170" fill="#fff"/><polygon points="10,255 100,195 190,255" fill="#34405e"/>
<rect x="420" y="240" width="170" height="180" fill="#fff"/><polygon points="410,245 505,185 600,245" fill="#34405e"/>
<rect x="60" y="310" width="30" height="40" fill="#8a5a3c"/><rect x="120" y="300" width="36" height="30" fill="#6ec6ff"/>
<rect x="460" y="300" width="36" height="30" fill="#6ec6ff"/><rect x="520" y="310" width="30" height="40" fill="#8a5a3c"/></g>
<path d="M150 420 Q300 250 450 420 L420 420 Q300 300 180 420 Z" fill="#d7d2c8"/>
<rect x="0" y="420" width="600" height="210" fill="#3ec1d9"/>
<path d="M180 420 Q300 300 420 420" fill="none" stroke="#b6afa3" stroke-width="4"/>
<g stroke="#fff" stroke-width="4" opacity=".6" stroke-linecap="round"><line x1="60" y1="470" x2="140" y2="470"/><line x1="380" y1="500" x2="480" y2="500"/><line x1="200" y1="560" x2="300" y2="560"/></g>
<path d="M230 520 L370 520 L345 548 L255 548 Z" fill="#8a5a3c"/><rect x="290" y="480" width="4" height="40" fill="#5b3a26"/>
<g fill="#ff4d4d"><ellipse cx="70" cy="280" rx="12" ry="16"/><ellipse cx="530" cy="270" rx="12" ry="16"/><ellipse cx="160" cy="270" rx="12" ry="16"/></g>
<g fill="#ffd23f"><rect x="66" y="294" width="8" height="6"/><rect x="526" y="284" width="8" height="6"/><rect x="156" y="284" width="8" height="6"/></g>
"""

SCENES["lake_pagoda"] = sky("g4", "#ff9a8b", "#ffe29f") + """
<circle cx="150" cy="200" r="70" fill="#fff1b8"/>
<g fill="#7a3b5c">
<rect x="380" y="330" width="80" height="60"/><polygon points="350,335 420,300 490,335" /><rect x="390" y="270" width="60" height="40"/>
<polygon points="365,275 420,245 475,275"/><rect x="400" y="215" width="40" height="36"/><polygon points="380,220 420,190 460,220"/><rect x="417" y="160" width="6" height="35"/>
</g>
<path d="M0 360 Q150 330 300 370 T600 350 L600 400 L0 400Z" fill="#8fbf7a"/>
<rect x="0" y="390" width="600" height="240" fill="#6fb7d6"/>
<g stroke="#fff" stroke-width="4" opacity=".6" stroke-linecap="round"><line x1="60" y1="440" x2="160" y2="440"/><line x1="330" y1="470" x2="450" y2="470"/></g>
<g fill="#3fae6b"><ellipse cx="100" cy="540" rx="50" ry="14"/><ellipse cx="260" cy="590" rx="44" ry="12"/><ellipse cx="470" cy="560" rx="54" ry="15"/></g>
<g fill="#ff6fa5"><circle cx="110" cy="522" r="12"/><circle cx="470" cy="540" r="13"/><circle cx="262" cy="574" r="10"/></g>
<path d="M560 0 Q520 160 560 330" stroke="#4d8a3a" stroke-width="5" fill="none"/>
<g stroke="#6fbf4f" stroke-width="3" fill="none"><path d="M560 60 q-40 60 -30 150"/><path d="M560 100 q-60 70 -45 170"/><path d="M570 40 q-20 90 0 200"/></g>
"""

SCENES["theme_park"] = sky("g5", "#7fd3ff", "#fff0c9") + """
<circle cx="500" cy="100" r="45" fill="#ffd23f"/>
<g fill="none" stroke-linecap="round">
<circle cx="170" cy="330" r="130" stroke="#ff6fa5" stroke-width="8"/>
<g stroke="#ff6fa5" stroke-width="3"><line x1="170" y1="200" x2="170" y2="460"/><line x1="40" y1="330" x2="300" y2="330"/><line x1="78" y1="238" x2="262" y2="422"/><line x1="78" y1="422" x2="262" y2="238"/></g>
</g>
<g fill="#9b5de5"><circle cx="170" cy="200" r="16"/><circle cx="300" cy="330" r="16"/><circle cx="170" cy="460" r="16"/><circle cx="40" cy="330" r="16"/></g>
<g fill="#3ec1ff"><circle cx="262" cy="238" r="16"/><circle cx="262" cy="422" r="16"/><circle cx="78" cy="238" r="16"/><circle cx="78" cy="422" r="16"/></g>
<polygon points="150,560 170,330 190,560" fill="#ff9f1c"/>
<path d="M260 520 C320 180 380 180 420 380 S520 520 600 250" fill="none" stroke="#2ec4b6" stroke-width="10"/>
<g stroke="#2ec4b6" stroke-width="4"><line x1="320" y1="300" x2="320" y2="560"/><line x1="420" y1="380" x2="420" y2="560"/><line x1="540" y1="330" x2="540" y2="560"/></g>
<rect x="352" y="210" width="36" height="22" rx="6" fill="#ff4d4d" transform="rotate(20 370 221)"/>
<rect x="0" y="555" width="600" height="75" fill="#8ac926"/>
""" + balloon(470, 470, "#ff5d8f") + balloon(520, 500, "#ffd23f")

SCENES["ice_castle"] = sky("g6", "#071441", "#1c3f9c") + stars(34, 7) + """
<defs><linearGradient id="ic" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7df9ff"/><stop offset=".5" stop-color="#b58bff"/><stop offset="1" stop-color="#ff7ad9"/></linearGradient></defs>
<g fill="url(#ic)" opacity=".95">
<rect x="220" y="200" width="160" height="340"/><polygon points="220,202 300,90 380,202"/>
<rect x="100" y="300" width="110" height="240"/><polygon points="100,302 155,230 210,302"/>
<rect x="390" y="280" width="120" height="260"/><polygon points="390,282 450,200 510,282"/>
<rect x="30" y="400" width="80" height="140"/><rect x="510" y="390" width="70" height="150"/>
</g>
<g stroke="#fff" stroke-width="2" opacity=".5"><line x1="220" y1="260" x2="380" y2="260"/><line x1="220" y1="330" x2="380" y2="330"/><line x1="220" y1="400" x2="380" y2="400"/><line x1="100" y1="380" x2="210" y2="380"/><line x1="390" y1="360" x2="510" y2="360"/><line x1="390" y1="440" x2="510" y2="440"/></g>
<rect x="276" y="450" width="48" height="90" rx="24" fill="#0b1f5c"/>
<rect x="0" y="540" width="600" height="90" fill="#e8f4ff"/>
<g fill="#fff">
<circle cx="80" cy="120" r="5"/><circle cx="520" cy="160" r="6"/><circle cx="430" cy="80" r="4"/><circle cx="160" cy="220" r="4"/><circle cx="560" cy="300" r="5"/>
</g>
"""

SCENES["panda_bamboo"] = sky("g7", "#c9f7c1", "#fffbe0") + """
<g stroke="#3fa34d" stroke-width="18" stroke-linecap="round">
<line x1="60" y1="630" x2="80" y2="40"/><line x1="140" y1="630" x2="130" y2="90"/><line x1="500" y1="630" x2="520" y2="30"/><line x1="560" y1="630" x2="570" y2="120"/>
</g>
<g stroke="#2b7a36" stroke-width="4"><line x1="62" y1="200" x2="82" y2="200"/><line x1="66" y1="340" x2="86" y2="340"/><line x1="502" y1="220" x2="522" y2="220"/><line x1="506" y1="380" x2="526" y2="380"/></g>
<g fill="#6fcf5a"><ellipse cx="110" cy="150" rx="40" ry="12" transform="rotate(-30 110 150)"/><ellipse cx="470" cy="160" rx="40" ry="12" transform="rotate(30 470 160)"/><ellipse cx="160" cy="300" rx="36" ry="11" transform="rotate(-20 160 300)"/><ellipse cx="545" cy="280" rx="36" ry="11" transform="rotate(25 545 280)"/></g>
<ellipse cx="300" cy="470" rx="150" ry="120" fill="#fff"/>
<ellipse cx="300" cy="500" rx="150" ry="70" fill="#222"/>
<circle cx="300" cy="300" r="105" fill="#fff"/>
<circle cx="215" cy="215" r="38" fill="#222"/><circle cx="385" cy="215" r="38" fill="#222"/>
<ellipse cx="258" cy="300" rx="28" ry="36" fill="#222" transform="rotate(-20 258 300)"/><ellipse cx="342" cy="300" rx="28" ry="36" fill="#222" transform="rotate(20 342 300)"/>
<circle cx="262" cy="296" r="9" fill="#fff"/><circle cx="338" cy="296" r="9" fill="#fff"/>
<ellipse cx="300" cy="345" rx="18" ry="12" fill="#222"/>
<ellipse cx="228" cy="345" rx="16" ry="10" fill="#ff9fb4" opacity=".7"/><ellipse cx="372" cy="345" rx="16" ry="10" fill="#ff9fb4" opacity=".7"/>
<line x1="330" y1="420" x2="420" y2="330" stroke="#3fa34d" stroke-width="14" stroke-linecap="round"/>
<ellipse cx="360" cy="420" rx="34" ry="28" fill="#222"/>
<rect x="0" y="580" width="600" height="50" fill="#7ccf5f"/>
"""

SCENES["cliff_night"] = sky("g8", "#12092e", "#3d1a6e") + stars(24, 11) + """
<path d="M0 630 L0 200 L120 190 L160 630Z" fill="#241448"/>
<g fill="#5a2d1a">
<rect x="10" y="220" width="120" height="50"/><rect x="0" y="280" width="140" height="55"/><rect x="10" y="345" width="130" height="60"/><rect x="0" y="415" width="150" height="70"/>
</g>
<g fill="#ffb938"><rect x="20" y="232" width="100" height="10"/><rect x="10" y="294" width="120" height="12"/><rect x="20" y="360" width="110" height="12"/><rect x="10" y="432" width="130" height="14"/></g>
<g fill="#ff5a36"><polygon points="0,220 70,195 140,220"/><polygon points="0,280 75,258 150,280"/><polygon points="0,345 75,322 150,345"/></g>
<rect x="400" y="160" width="60" height="330" fill="#2d2a7a"/><rect x="470" y="210" width="50" height="280" fill="#3a2f8f"/><rect x="530" y="120" width="60" height="370" fill="#2d2a7a"/>
<g fill="#7df9ff" opacity=".8"><rect x="412" y="190" width="8" height="8"/><rect x="440" y="240" width="8" height="8"/><rect x="482" y="250" width="8" height="8"/><rect x="545" y="160" width="8" height="8"/><rect x="566" y="220" width="8" height="8"/></g>
<line x1="150" y1="180" x2="600" y2="90" stroke="#ddd" stroke-width="3"/>
<rect x="330" y="110" width="44" height="34" rx="6" fill="#ff4d6d"/><line x1="352" y1="112" x2="352" y2="100" stroke="#ddd" stroke-width="3"/>
<rect x="0" y="490" width="600" height="140" fill="#1b2470"/>
<g stroke-width="7" stroke-linecap="round" opacity=".85"><line x1="30" y1="520" x2="120" y2="520" stroke="#ffb938"/><line x1="40" y1="560" x2="100" y2="560" stroke="#ffb938"/><line x1="420" y1="530" x2="500" y2="530" stroke="#7df9ff"/><line x1="530" y1="565" x2="580" y2="565" stroke="#ff4d6d"/></g>
"""

SCENES["terracotta"] = sky("g9", "#ffcf87", "#f7a35c") + """
<circle cx="470" cy="130" r="60" fill="#fff0b3"/>
<rect x="0" y="330" width="600" height="300" fill="#c9824a"/>
""" + "".join(
    f'<g fill="{c}"><circle cx="{x}" cy="{y}" r="{r*.45:.0f}"/><path d="M{x-r*.7:.0f} {y+r*.4:.0f} L{x+r*.7:.0f} {y+r*.4:.0f} L{x+r*.55:.0f} {y+r*2.1:.0f} L{x-r*.55:.0f} {y+r*2.1:.0f}Z"/><rect x="{x-r*.35:.0f}" y="{y+r*2.1:.0f}" width="{r*.7:.0f}" height="{r*.7:.0f}"/></g>'
    for row, (y, r, c) in enumerate([(350, 26, "#9c5b33"), (410, 34, "#8a4d2a"), (490, 44, "#7a4222")])
    for x in range(40 + row * 20, 600, int(r * 2.3))
)

SCENES["beach"] = sky("g10", "#4fd1ff", "#c9f4ff") + """
<circle cx="130" cy="120" r="55" fill="#ffd23f"/>
<rect x="0" y="330" width="600" height="160" fill="#16c2c2"/>
<rect x="0" y="330" width="600" height="40" fill="#0fa3b1"/>
<path d="M0 480 Q300 440 600 480 L600 630 L0 630Z" fill="#ffe3a3"/>
<g stroke="#fff" stroke-width="4" opacity=".7" stroke-linecap="round"><line x1="80" y1="400" x2="170" y2="400"/><line x1="330" y1="430" x2="440" y2="430"/></g>
<path d="M470 600 Q450 450 500 300" stroke="#8a5a3c" stroke-width="14" fill="none"/>
<g fill="#2eb872"><ellipse cx="455" cy="300" rx="70" ry="20" transform="rotate(20 455 300)"/><ellipse cx="545" cy="300" rx="70" ry="20" transform="rotate(-20 545 300)"/><ellipse cx="500" cy="270" rx="60" ry="18" transform="rotate(-80 500 270)"/><ellipse cx="530" cy="330" rx="60" ry="16" transform="rotate(40 530 330)"/></g>
<line x1="200" y1="600" x2="200" y2="470" stroke="#555" stroke-width="5"/>
<path d="M120 480 Q200 400 280 480Z" fill="#ff5d8f"/><path d="M160 480 Q200 400 240 480Z" fill="#fff"/>
<rect x="260" y="560" width="90" height="16" rx="8" fill="#9b5de5"/>
"""

SCENES["karst_river"] = sky("g11", "#ffd6e7", "#d6f5ff") + """
<g fill="#7cc79a"><path d="M-20 420 Q40 120 100 420Z"/><path d="M500 420 Q560 150 620 420Z"/></g>
<g fill="#4fae7a"><path d="M60 430 Q140 90 220 430Z"/><path d="M380 430 Q450 110 520 430Z"/></g>
<g fill="#2e8b5b"><path d="M180 440 Q260 180 340 440Z"/></g>
<rect x="0" y="420" width="600" height="210" fill="#5ec6e0"/>
<g fill="#2e8b5b" opacity=".35"><path d="M180 420 Q260 560 340 420Z"/><path d="M60 420 Q140 640 220 420Z"/></g>
<g stroke="#fff" stroke-width="4" opacity=".6" stroke-linecap="round"><line x1="40" y1="480" x2="120" y2="480"/><line x1="420" y1="500" x2="520" y2="500"/></g>
<g fill="#c89b5a"><rect x="210" y="545" width="200" height="12" rx="6"/><rect x="210" y="560" width="200" height="12" rx="6"/></g>
<circle cx="330" cy="505" r="11" fill="#ffb6a0"/><path d="M315 518 L345 518 L340 545 L320 545Z" fill="#ff5d5d"/>
<line x1="300" y1="490" x2="360" y2="570" stroke="#8a5a3c" stroke-width="4"/>
<path d="M300 505 Q330 470 360 505Z" fill="#ffd23f"/>
"""

SCENES["snow_mountain"] = sky("g12", "#2f80ed", "#b3e5ff") + """
<polygon points="40,450 260,90 480,450" fill="#6c7a93"/>
<polygon points="200,200 260,90 320,200 290,180 260,210 230,180" fill="#fff"/>
<polygon points="300,450 450,170 600,450" fill="#8594ad"/>
<polygon points="410,245 450,170 490,245 465,230 450,250 435,230" fill="#fff"/>
<rect x="0" y="440" width="600" height="190" fill="#2ec4d6"/>
<path d="M0 470 Q150 450 300 480 T600 470" fill="none" stroke="#7cf0ff" stroke-width="10" opacity=".7"/>
<path d="M0 530 Q150 510 300 540 T600 530" fill="none" stroke="#7cf0ff" stroke-width="10" opacity=".6"/>
<line x1="0" y1="330" x2="340" y2="140" stroke="#333" stroke-width="3"/>
<rect x="150" y="238" width="40" height="30" rx="6" fill="#ff4d6d"/><line x1="170" y1="240" x2="170" y2="228" stroke="#333" stroke-width="3"/>
<g fill="#fff" opacity=".9"><ellipse cx="480" cy="90" rx="60" ry="18"/><ellipse cx="90" cy="130" rx="50" ry="15"/></g>
"""

SCENES["island_piano"] = sky("g13", "#8fd3ff", "#e8fbff") + """
<rect x="0" y="360" width="600" height="270" fill="#1fa7c9"/>
<path d="M60 380 Q300 200 560 380Z" fill="#6cc46a"/>
<g><rect x="170" y="300" width="60" height="50" fill="#fff5e0"/><polygon points="165,302 200,275 235,302" fill="#e2574c"/>
<rect x="260" y="270" width="70" height="60" fill="#fff5e0"/><polygon points="255,272 295,240 335,272" fill="#e2574c"/>
<rect x="360" y="300" width="60" height="50" fill="#fff5e0"/><polygon points="355,302 390,275 425,302" fill="#e2574c"/></g>
<circle cx="300" cy="215" r="16" fill="#9e8a6b"/>
<path d="M90 520 L250 520 L230 555 L110 555Z" fill="#fff"/><rect x="130" y="490" width="80" height="30" fill="#fff"/><rect x="140" y="498" width="60" height="10" fill="#3ec1ff"/>
<g transform="translate(330 470)">
<rect width="240" height="90" rx="8" fill="#fff"/>
<g fill="#222"><rect x="22" y="0" width="16" height="55"/><rect x="52" y="0" width="16" height="55"/><rect x="112" y="0" width="16" height="55"/><rect x="142" y="0" width="16" height="55"/><rect x="172" y="0" width="16" height="55"/></g>
<g stroke="#ccc" stroke-width="2"><line x1="30" y1="0" x2="30" y2="90"/><line x1="60" y1="0" x2="60" y2="90"/><line x1="90" y1="0" x2="90" y2="90"/><line x1="120" y1="0" x2="120" y2="90"/><line x1="150" y1="0" x2="150" y2="90"/><line x1="180" y1="0" x2="180" y2="90"/><line x1="210" y1="0" x2="210" y2="90"/></g>
</g>
<g fill="#ff5d8f"><circle cx="480" cy="420" r="8"/><rect x="486" y="380" width="3" height="40"/></g>
"""

SCENES["coast_city"] = sky("g14", "#6ec6ff", "#fdfbe2") + """
<g fill="#4a6fd1"><rect x="40" y="230" width="50" height="160"/><rect x="100" y="190" width="40" height="200"/><rect x="150" y="250" width="60" height="140"/><rect x="420" y="210" width="45" height="180"/><rect x="475" y="240" width="60" height="150"/><rect x="545" y="200" width="40" height="190"/></g>
<ellipse cx="300" cy="420" rx="260" ry="60" fill="#f3d9a4"/>
<ellipse cx="300" cy="420" rx="170" ry="38" fill="#ffe9b8" stroke="#e2a95c" stroke-width="4"/>
<circle cx="300" cy="420" r="10" fill="#e2574c"/>
<rect x="0" y="470" width="600" height="160" fill="#2aa7d6"/>
<path d="M360 560 L480 560 L460 585 L380 585Z" fill="#fff"/><polygon points="420,470 420,555 470,555" fill="#ffd23f"/><polygon points="415,480 415,555 375,555" fill="#ff5d8f"/>
<g fill="none" stroke="#333" stroke-width="3" stroke-linecap="round"><path d="M110 110 q12 -12 24 0 q12 -12 24 0"/><path d="M200 70 q10 -10 20 0 q10 -10 20 0"/></g>
<circle cx="480" cy="90" r="40" fill="#ffd23f"/>
"""

SCENES["tech_city"] = sky("g15", "#1a0b4a", "#7b2ff7") + stars(18, 5) + """
<g><rect x="30" y="260" width="70" height="300" fill="#3a1e9c"/><rect x="110" y="190" width="60" height="370" fill="#4c2bd1"/>
<rect x="250" y="110" width="80" height="450" fill="#5b3ff0"/><polygon points="250,112 290,40 330,112" fill="#5b3ff0"/>
<rect x="340" y="220" width="70" height="340" fill="#3a1e9c"/><rect x="430" y="170" width="60" height="390" fill="#4c2bd1"/><rect x="500" y="280" width="80" height="280" fill="#3a1e9c"/></g>
<g stroke="#3ee6c8" stroke-width="3" fill="none" opacity=".9"><path d="M0 590 H120 V520 H200"/><path d="M600 600 H470 V540 H400"/><path d="M200 600 H330 V560"/></g>
<g fill="#3ee6c8"><circle cx="200" cy="520" r="7"/><circle cx="400" cy="540" r="7"/><circle cx="330" cy="560" r="7"/></g>
<g fill="#ffd23f" opacity=".9"><rect x="265" y="140" width="10" height="10"/><rect x="300" y="200" width="10" height="10"/><rect x="265" y="260" width="10" height="10"/><rect x="125" y="230" width="10" height="10"/><rect x="445" y="210" width="10" height="10"/><rect x="460" y="300" width="10" height="10"/></g>
<g transform="translate(150 100)"><rect x="-26" y="-6" width="52" height="12" rx="6" fill="#ff5d8f"/><line x1="-40" y1="-14" x2="-12" y2="-14" stroke="#fff" stroke-width="4"/><line x1="12" y1="-14" x2="40" y2="-14" stroke="#fff" stroke-width="4"/></g>
<rect x="0" y="560" width="600" height="70" fill="#12063a"/>
"""

SCENES["passport"] = sky("g16", "#ffe0ec", "#e0f0ff") + """
<g transform="rotate(-8 300 330)">
<rect x="170" y="150" width="260" height="360" rx="18" fill="#8c1c2e"/>
<circle cx="300" cy="290" r="62" fill="none" stroke="#f3c96a" stroke-width="7"/>
<circle cx="300" cy="290" r="28" fill="#f3c96a"/>
<rect x="230" y="400" width="140" height="12" rx="6" fill="#f3c96a"/><rect x="250" y="425" width="100" height="10" rx="5" fill="#f3c96a" opacity=".7"/>
</g>
<g opacity=".9">
<circle cx="110" cy="170" r="55" fill="none" stroke="#2ec4b6" stroke-width="7"/><circle cx="110" cy="170" r="40" fill="none" stroke="#2ec4b6" stroke-width="3"/>
<rect x="440" y="430" width="120" height="80" rx="12" fill="none" stroke="#ff5d8f" stroke-width="7" transform="rotate(12 500 470)"/>
<circle cx="500" cy="170" r="45" fill="none" stroke="#9b5de5" stroke-width="7"/>
</g>
<g transform="translate(90 500) rotate(-25)"><path d="M0 0 L90 -8 L100 0 L90 8Z" fill="#4d96ff"/><path d="M40 -4 L20 -40 L32 -40 L60 -4Z" fill="#4d96ff"/><path d="M40 4 L20 40 L32 40 L60 4Z" fill="#4d96ff"/></g>
"""

SCENES["phone_pay"] = sky("g17", "#d9f7ff", "#e9e0ff") + """
<rect x="190" y="90" width="220" height="440" rx="34" fill="#1f2a44"/>
<rect x="205" y="120" width="190" height="380" rx="20" fill="#fff"/>
<rect x="205" y="120" width="190" height="60" rx="20" fill="#1677ff"/><rect x="205" y="150" width="190" height="30" fill="#1677ff"/>
<g fill="#1f2a44">
<rect x="235" y="215" width="40" height="40"/><rect x="325" y="215" width="40" height="40"/><rect x="235" y="305" width="40" height="40"/>
<rect x="285" y="215" width="12" height="12"/><rect x="300" y="240" width="12" height="12"/><rect x="285" y="265" width="30" height="12"/><rect x="330" y="285" width="12" height="30"/><rect x="290" y="300" width="20" height="20"/><rect x="345" y="330" width="20" height="12"/><rect x="310" y="330" width="12" height="12"/>
</g>
<g fill="#fff"><rect x="243" y="223" width="24" height="24"/><rect x="333" y="223" width="24" height="24"/><rect x="243" y="313" width="24" height="24"/></g>
<g fill="#1f2a44"><rect x="249" y="229" width="12" height="12"/><rect x="339" y="229" width="12" height="12"/><rect x="249" y="319" width="12" height="12"/></g>
<rect x="235" y="400" width="130" height="40" rx="20" fill="#2ec4b6"/>
<g><circle cx="110" cy="420" r="48" fill="#ffd23f"/><circle cx="110" cy="420" r="34" fill="none" stroke="#e0a800" stroke-width="5"/>
<circle cx="490" cy="200" r="40" fill="#ffd23f"/><circle cx="490" cy="200" r="28" fill="none" stroke="#e0a800" stroke-width="5"/></g>
<circle cx="480" cy="440" r="50" fill="#8ac926"/><path d="M458 440 L475 458 L505 424" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
"""

SCENES["train"] = sky("g18", "#9be7ff", "#fff3d6") + """
<g fill="#8fd18a"><path d="M-20 400 Q120 220 260 400Z"/><path d="M200 400 Q360 250 520 400Z"/><path d="M430 400 Q540 280 640 400Z"/></g>
<rect x="0" y="390" width="600" height="240" fill="#e9dcc2"/>
<g stroke="#8a7a66" stroke-width="6"><line x1="0" y1="500" x2="600" y2="500"/><line x1="0" y1="530" x2="600" y2="530"/></g>
<g stroke="#b5a48c" stroke-width="8">""" + "".join(f'<line x1="{x}" y1="495" x2="{x-10}" y2="536"/>' for x in range(20, 620, 40)) + """</g>
<path d="M40 490 L470 490 Q570 490 590 420 Q540 380 440 380 L40 380Z" fill="#fff"/>
<path d="M40 440 L560 440 Q575 430 580 420 L40 420Z" fill="#e2574c"/>
<path d="M455 392 Q530 392 560 415 L455 415Z" fill="#1f2a44"/>
<g fill="#1f2a44"><rect x="70" y="392" width="50" height="22" rx="4"/><rect x="140" y="392" width="50" height="22" rx="4"/><rect x="210" y="392" width="50" height="22" rx="4"/><rect x="280" y="392" width="50" height="22" rx="4"/><rect x="350" y="392" width="50" height="22" rx="4"/></g>
<g stroke="#4d96ff" stroke-width="6" stroke-linecap="round" opacity=".7"><line x1="-10" y1="400" x2="20" y2="400"/><line x1="-10" y1="450" x2="25" y2="450"/></g>
<circle cx="480" cy="110" r="45" fill="#ffd23f"/>
"""

SCENES["taxi"] = sky("g19", "#fff1d6", "#ffe0ec") + """
<rect x="40" y="60" width="520" height="420" rx="30" fill="#e6f7ee"/>
<g stroke="#fff" stroke-width="26"><line x1="40" y1="200" x2="560" y2="200"/><line x1="40" y1="360" x2="560" y2="360"/><line x1="180" y1="60" x2="180" y2="480"/><line x1="420" y1="60" x2="420" y2="480"/></g>
<g fill="#b8e4ff"><rect x="60" y="80" width="100" height="100" rx="10"/><rect x="440" y="220" width="100" height="120" rx="10"/></g>
<g fill="#ffd6a5"><rect x="200" y="220" width="200" height="120" rx="10"/><rect x="440" y="80" width="100" height="100" rx="10"/></g>
<path d="M180 440 L180 360 L420 360 L420 200 L500 200" fill="none" stroke="#ff5d8f" stroke-width="10" stroke-dasharray="4 16" stroke-linecap="round"/>
<g transform="translate(500 150)"><path d="M0 50 C-40 0 -30 -40 0 -40 C30 -40 40 0 0 50Z" fill="#e2574c"/><circle cx="0" cy="-8" r="13" fill="#fff"/></g>
<g transform="translate(120 480)">
<path d="M0 60 L0 30 Q10 0 50 0 L130 0 Q170 0 180 30 L180 60Z" fill="#ff9f1c"/>
<rect x="40" y="8" width="45" height="26" rx="4" fill="#bde7ff"/><rect x="95" y="8" width="45" height="26" rx="4" fill="#bde7ff"/>
<circle cx="40" cy="62" r="18" fill="#222"/><circle cx="140" cy="62" r="18" fill="#222"/>
<rect x="70" y="-14" width="40" height="14" rx="4" fill="#1f2a44"/>
</g>
"""

SCENES["suitcase"] = sky("g20", "#e0f7ff", "#fff0f5") + """
<rect x="100" y="250" width="400" height="280" rx="24" fill="#4d96ff"/>
<path d="M100 250 L140 120 L460 120 L500 250Z" fill="#6ea8ff"/>
<rect x="120" y="270" width="360" height="240" rx="16" fill="#e8f1ff"/>
<rect x="150" y="300" width="80" height="110" rx="10" fill="#8c1c2e"/><circle cx="190" cy="345" r="18" fill="none" stroke="#f3c96a" stroke-width="5"/>
<rect x="255" y="290" width="70" height="130" rx="14" fill="#1f2a44"/><rect x="263" y="302" width="54" height="100" rx="6" fill="#7df9ff"/>
<rect x="350" y="300" width="100" height="55" rx="10" fill="#8ac926"/><rect x="360" y="312" width="12" height="30" rx="3" fill="#fff"/><rect x="380" y="312" width="12" height="30" rx="3" fill="#fff"/>
<rect x="160" y="435" width="120" height="50" rx="10" fill="#ff5d8f"/><rect x="170" y="448" width="40" height="24" rx="4" fill="#fff" opacity=".8"/>
<rect x="300" y="430" width="150" height="55" rx="10" fill="#ffd23f"/>
<rect x="260" y="210" width="80" height="30" rx="10" fill="#1f2a44"/>
<g fill="#9b5de5"><circle cx="80" cy="120" r="14"/><circle cx="530" cy="90" r="10"/></g><g fill="#2ec4b6"><circle cx="540" cy="200" r="12"/><circle cx="60" cy="560" r="10"/></g>
"""

# 도시 총정리용
SCENES["red_roof_sea"] = sky("g21", "#7fd3ff", "#e9fbff") + """
<rect x="0" y="380" width="600" height="250" fill="#1f8fd1"/>
<g><rect x="60" y="260" width="90" height="120" fill="#fff5e0"/><polygon points="50,262 105,210 160,262" fill="#e2574c"/>
<rect x="170" y="230" width="100" height="150" fill="#fff5e0"/><polygon points="160,232 220,175 280,232" fill="#e2574c"/>
<rect x="290" y="270" width="80" height="110" fill="#fff5e0"/><polygon points="280,272 330,225 380,272" fill="#e2574c"/></g>
<g fill="#6ec6ff"><rect x="85" y="290" width="16" height="20"/><rect x="200" y="260" width="16" height="20"/><rect x="230" y="260" width="16" height="20"/><rect x="310" y="300" width="16" height="20"/></g>
<rect x="380" y="430" width="220" height="12" fill="#c89b5a"/><g fill="#c89b5a"><rect x="400" y="440" width="8" height="40"/><rect x="460" y="440" width="8" height="40"/><rect x="520" y="440" width="8" height="40"/></g>
<polygon points="560,380 590,400 590,430 560,430" fill="#e2574c"/>
<g transform="translate(430 170)"><rect width="90" height="120" rx="12" fill="#ffc83d"/><rect x="0" y="0" width="90" height="28" rx="12" fill="#fff"/><path d="M90 30 q40 0 40 40 q0 40 -40 40" fill="none" stroke="#ffc83d" stroke-width="14"/></g>
<circle cx="110" cy="100" r="45" fill="#ffd23f"/>
"""

SCENES["palace"] = sky("g22", "#ffd3a5", "#fd6585") + """
<circle cx="450" cy="150" r="60" fill="#fff0b3"/>
<rect x="0" y="470" width="600" height="160" fill="#b33a3a"/>
<rect x="60" y="340" width="480" height="130" fill="#c0392b"/>
<g fill="#8e1f1f"><rect x="90" y="360" width="18" height="110"/><rect x="170" y="360" width="18" height="110"/><rect x="250" y="360" width="18" height="110"/><rect x="332" y="360" width="18" height="110"/><rect x="412" y="360" width="18" height="110"/><rect x="492" y="360" width="18" height="110"/></g>
<path d="M20 345 Q300 300 580 345 L540 300 Q300 270 60 300Z" fill="#f2b705"/>
<rect x="140" y="250" width="320" height="55" fill="#c0392b"/>
<path d="M90 255 Q300 215 510 255 L470 215 Q300 190 130 215Z" fill="#f2b705"/>
<rect x="250" y="400" width="100" height="70" rx="50" fill="#5a1414"/>
<g fill="#fff" opacity=".85"><rect x="0" y="560" width="600" height="8"/></g>
"""

SCENES["pillars"] = sky("g23", "#c8f0e0", "#f4fff9") + """
<g fill="#b9e3cf" opacity=".9"><ellipse cx="120" cy="330" rx="140" ry="40"/><ellipse cx="480" cy="300" rx="160" ry="44"/></g>
<g fill="#6b8f7f"><path d="M40 630 L50 220 Q70 180 90 220 L100 630Z"/><path d="M480 630 L490 180 Q515 140 540 180 L550 630Z"/></g>
<g fill="#4f7565"><path d="M130 630 L145 150 Q180 110 215 150 L230 630Z"/><path d="M370 630 L380 240 Q410 200 440 240 L450 630Z"/></g>
<g fill="#3a5a4c"><path d="M250 630 L262 90 Q300 50 338 90 L350 630Z"/></g>
<g fill="#2eb872"><ellipse cx="300" cy="80" rx="46" ry="18"/><ellipse cx="180" cy="140" rx="40" ry="16"/><ellipse cx="410" cy="230" rx="34" ry="14"/><ellipse cx="515" cy="170" rx="30" ry="12"/><ellipse cx="70" cy="210" rx="28" ry="11"/></g>
<g fill="#fff" opacity=".85"><ellipse cx="300" cy="420" rx="200" ry="30"/><ellipse cx="120" cy="500" rx="140" ry="24"/><ellipse cx="480" cy="520" rx="150" ry="26"/></g>
<g fill="none" stroke="#e9895f" stroke-width="3" stroke-linecap="round"><path d="M100 110 q10 -10 20 0 q10 -10 20 0"/></g>
"""

# ───── 중앙아시아 전용 장면 (일반적인 풍경, 특정 유적·로고 아님) ─────

SCENES["dome_city"] = sky("ca1", "#1b2a6b", "#f2a65a") + stars(18) + """
<circle cx="470" cy="150" r="46" fill="#fff3d6" opacity=".95"/>
<g>
<ellipse cx="300" cy="300" rx="95" ry="88" fill="#2bb3a3"/>
<rect x="205" y="300" width="190" height="230" fill="#f5e7cd"/>
<rect x="225" y="330" width="150" height="16" fill="#2bb3a3" opacity=".7"/>
<rect x="258" y="380" width="84" height="150" rx="42" fill="#1b4e8f"/>
<rect x="276" y="420" width="48" height="110" rx="24" fill="#ffd23f" opacity=".9"/>
<rect x="120" y="250" width="44" height="300" fill="#f0dcba"/><ellipse cx="142" cy="246" rx="30" ry="26" fill="#2bb3a3"/>
<rect x="436" y="250" width="44" height="300" fill="#f0dcba"/><ellipse cx="458" cy="246" rx="30" ry="26" fill="#2bb3a3"/>
<rect x="128" y="300" width="28" height="12" fill="#1b4e8f"/><rect x="128" y="360" width="28" height="12" fill="#1b4e8f"/>
<rect x="444" y="300" width="28" height="12" fill="#1b4e8f"/><rect x="444" y="360" width="28" height="12" fill="#1b4e8f"/>
<line x1="300" y1="212" x2="300" y2="176" stroke="#ffd23f" stroke-width="5"/><circle cx="300" cy="170" r="8" fill="#ffd23f"/>
</g>
<g fill="#1b4e8f" opacity=".85"><rect x="230" y="440" width="20" height="26" rx="10"/><rect x="350" y="440" width="20" height="26" rx="10"/></g>
<rect x="0" y="550" width="600" height="80" fill="#143a6e"/>
<g stroke="#ffd23f" stroke-width="4" opacity=".6"><line x1="60" y1="575" x2="110" y2="575"/><line x1="470" y1="585" x2="540" y2="585"/></g>
"""

SCENES["mountain_lake"] = sky("ca2", "#7fd0f5", "#eaf8ff") + """
<circle cx="140" cy="110" r="42" fill="#fff6c9"/>
<g>
<polygon points="0,330 130,130 260,330" fill="#5b7cfa"/><polygon points="130,130 95,185 165,185" fill="#fff"/>
<polygon points="180,330 330,90 480,330" fill="#4154c9"/><polygon points="330,90 288,160 372,160" fill="#fff"/>
<polygon points="400,330 510,170 620,330" fill="#5b7cfa"/><polygon points="510,170 480,218 540,218" fill="#fff"/>
</g>
<rect x="0" y="330" width="600" height="220" fill="#2bb3d9"/>
<g opacity=".5" fill="#fff"><ellipse cx="150" cy="380" rx="70" ry="8"/><ellipse cx="420" cy="420" rx="90" ry="9"/><ellipse cx="270" cy="480" rx="60" ry="7"/></g>
<polygon points="0,330 130,210 260,330" fill="#3a4db0" opacity=".35"/>
<path d="M60 560 q60 -40 150 -18 q90 22 180 -6 q90 -28 150 6 L600 630 L0 630Z" fill="#7cb518"/>
<g fill="#2e7d32"><polygon points="90,560 110,510 130,560"/><polygon points="120,572 140,522 160,572"/><polygon points="470,556 490,506 510,556"/></g>
"""

SCENES["yurt_steppe"] = sky("ca3", "#ff9a5a", "#ffd98a") + """
<circle cx="300" cy="200" r="62" fill="#fff1c9"/>
<path d="M0 420 q150 -60 300 -20 q150 40 300 -10 L600 630 L0 630Z" fill="#c98f3d"/>
<path d="M0 500 q200 -40 600 0 L600 630 L0 630Z" fill="#a9742c"/>
<g>
<ellipse cx="300" cy="500" rx="130" ry="26" fill="#8a5c1d" opacity=".4"/>
<path d="M190 480 q0 -60 110 -60 q110 0 110 60 Z" fill="#fff6e8"/>
<path d="M300 380 L190 480 L410 480 Z" fill="#e2574c"/>
<rect x="272" y="430" width="56" height="52" rx="8" fill="#8a3a2e"/>
<line x1="300" y1="380" x2="300" y2="352" stroke="#8a3a2e" stroke-width="5"/><circle cx="300" cy="348" r="6" fill="#ffd23f"/>
<path d="M200 470 q100 -24 200 0" stroke="#e2574c" stroke-width="7" fill="none"/>
</g>
<g fill="#5b3b16"><ellipse cx="120" cy="560" rx="14" ry="8"/><rect x="112" y="528" width="7" height="32" rx="3"/><rect x="128" y="528" width="7" height="32" rx="3"/><ellipse cx="121" cy="524" rx="18" ry="12"/><rect x="134" y="512" width="8" height="16" rx="4"/></g>
<g fill="#5b3b16" opacity=".85"><ellipse cx="500" cy="585" rx="12" ry="7"/><rect x="493" y="558" width="6" height="28" rx="3"/><rect x="506" y="558" width="6" height="28" rx="3"/><ellipse cx="500" cy="554" rx="15" ry="10"/><rect x="511" y="544" width="7" height="14" rx="3"/></g>
<g stroke="#fff" stroke-width="3" opacity=".6"><path d="M60 180 q20 -14 40 0" fill="none"/><path d="M480 140 q20 -14 40 0" fill="none"/></g>
"""

SCENES["canyon"] = sky("ca4", "#ffd0a0", "#ffeedd") + """
<circle cx="470" cy="120" r="44" fill="#fff6d9"/>
<g>
<path d="M0 630 L0 240 L70 200 L110 280 L90 630Z" fill="#c0392b"/>
<path d="M90 630 L110 300 L170 230 L210 340 L190 630Z" fill="#e2574c"/>
<path d="M600 630 L600 220 L530 190 L490 290 L510 630Z" fill="#c0392b"/>
<path d="M510 630 L495 300 L440 240 L410 350 L430 630Z" fill="#e2574c"/>
</g>
<g opacity=".35" fill="#8a2f23">
<rect x="20" y="300" width="60" height="12"/><rect x="15" y="380" width="70" height="12"/><rect x="110" y="340" width="70" height="12"/>
<rect x="520" y="300" width="60" height="12"/><rect x="440" y="360" width="60" height="12"/>
</g>
<path d="M220 630 q80 -180 80 -340 q0 160 80 340Z" fill="#f6b56b"/>
<path d="M260 630 q40 -120 40 -260 q0 140 40 260Z" fill="#ffd79a"/>
<ellipse cx="300" cy="610" rx="120" ry="14" fill="#a9742c" opacity=".5"/>
"""

SCENES["highland_road"] = sky("ca5", "#3b5bd6", "#bfe3ff") + """
<circle cx="130" cy="110" r="38" fill="#fff6c9"/>
<g>
<polygon points="0,360 120,160 250,360" fill="#6a7fd9"/><polygon points="120,160 88,212 152,212" fill="#fff"/>
<polygon points="200,360 360,110 520,360" fill="#51379e"/><polygon points="360,110 320,176 400,176" fill="#fff"/>
<polygon points="450,360 540,220 630,360" fill="#6a7fd9"/>
</g>
<rect x="0" y="360" width="600" height="270" fill="#8c6f3f"/>
<path d="M260 630 L290 360 L310 360 L340 630Z" fill="#3f3a36"/>
<path d="M300 630 L299 360 L301 360 L302 630Z" stroke="#ffd23f" stroke-width="5" stroke-dasharray="26 20" fill="none"/>
<g fill="#6b522a"><path d="M0 420 q120 -24 240 0 L240 450 Q120 430 0 450Z" opacity=".5"/><path d="M360 430 q120 -20 240 6 L600 470 Q480 450 360 462Z" opacity=".5"/></g>
<g><rect x="270" y="470" width="60" height="34" rx="8" fill="#e2574c"/><rect x="280" y="458" width="40" height="20" rx="6" fill="#ffdede"/><circle cx="283" cy="506" r="9" fill="#232a3f"/><circle cx="317" cy="506" r="9" fill="#232a3f"/></g>
"""

SCENES["bazaar"] = sky("ca6", "#ff8f6b", "#ffe3c2") + """
<circle cx="480" cy="110" r="40" fill="#fff3d0"/>
<g>
<ellipse cx="300" cy="260" rx="170" ry="60" fill="#2bb3a3"/>
<rect x="130" y="260" width="340" height="40" fill="#f5e7cd"/>
<rect x="150" y="300" width="300" height="230" fill="#f0dcba"/>
<rect x="250" y="380" width="100" height="150" rx="50" fill="#1b4e8f"/>
</g>
<g>
<rect x="60" y="430" width="130" height="14" fill="#e2574c"/><path d="M60 430 l0 -24 q32 20 65 0 q33 20 65 0 l0 24Z" fill="#ff8a7a"/>
<rect x="70" y="444" width="110" height="86" fill="#fff6e8"/>
<circle cx="95" cy="470" r="11" fill="#ffd23f"/><circle cx="120" cy="470" r="11" fill="#ff6b6b"/><circle cx="145" cy="470" r="11" fill="#7cb518"/>
<circle cx="95" cy="498" r="11" fill="#ff9a3d"/><circle cx="120" cy="498" r="11" fill="#9b5de5"/><circle cx="145" cy="498" r="11" fill="#ffd23f"/>
</g>
<g>
<rect x="410" y="430" width="130" height="14" fill="#1b9d96"/><path d="M410 430 l0 -24 q32 20 65 0 q33 20 65 0 l0 24Z" fill="#6bd6c8"/>
<rect x="420" y="444" width="110" height="86" fill="#fff6e8"/>
<ellipse cx="452" cy="478" rx="20" ry="12" fill="#f3c96a"/><ellipse cx="500" cy="478" rx="20" ry="12" fill="#f3c96a"/>
<ellipse cx="476" cy="505" rx="22" ry="13" fill="#e8b04e"/>
</g>
<rect x="0" y="560" width="600" height="70" fill="#a9742c"/>
"""
