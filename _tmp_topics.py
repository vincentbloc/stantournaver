import json
f = "data/topics.json"
t = json.load(open(f, encoding="utf-8"))
for x in t:
    if x["id"] == 61:
        x["status"] = "done"
        x["post"] = "almaty-airport-guide"
new = [
    ("사마르칸트 시압 바자르 구경법: 말린 과일·논(빵)·견과류 고르는 요령과 비비하눔 연결 동선", "siab-bazaar", "사마르칸트", "uz", "spot", ["시압 바자르", "사마르칸트 시장", "사마르칸트 기념품", "사마르칸트 가볼만한곳"], "bazaar"),
    ("우즈베키스탄 고속열차 히바 연장: 타슈켄트-히바 직통 노선·소요 시간·예매 팁", "uzbekistan-khiva-train", "히바", "uz", "prep", ["히바 기차", "타슈켄트 히바 기차", "우즈베키스탄 고속열차", "아프로시욥 히바"], "train"),
    ("알마티 맛집 가이드: 베쉬바르막·카자흐 전통 음식과 현지 식당 고르는 법", "almaty-food", "알마티", "kz", "city", ["알마티 맛집", "카자흐스탄 음식", "베쉬바르막", "알마티 식당"], "bazaar"),
    ("부하라 숙소 고르기: 라비하우즈 주변 전통 가옥 호텔과 위치별 장단점", "bukhara-hotels", "부하라", "uz", "prep", ["부하라 숙소", "부하라 호텔", "라비하우즈", "우즈베키스탄 숙소"], "dome_city"),
    ("키르기스스탄 스카즈카 협곡·제티오구즈: 이식쿨 남쪽 하루 코스", "skazka-jeti-oguz", "이식쿨", "kg", "nature", ["스카즈카 협곡", "제티오구즈", "이식쿨 남쪽", "키르기스스탄 가볼만한곳"], "canyon"),
    ("중앙아시아 가을 여행: 9~10월 단풍·포도·축제와 나라별 날씨", "central-asia-autumn", "중앙아시아", "prep", "prep", ["중앙아시아 가을 여행", "우즈베키스탄 10월 날씨", "알마티 가을", "키르기스스탄 9월"], "snow_mountain"),
    ("우즈베키스탄 사원 복장과 매너: 모스크·영묘 입장 시 옷차림과 사진 예절", "uzbekistan-etiquette", "우즈베키스탄", "uz", "prep", ["우즈베키스탄 복장", "우즈베키스탄 매너", "모스크 복장", "우즈베키스탄 여행 주의사항"], "dome_city"),
    ("알마티 근교 투르겐 계곡: 폭포·전망대 당일치기와 투어 고르는 법", "turgen-gorge", "알마티", "kz", "nature", ["투르겐 계곡", "알마티 근교", "알마티 당일치기", "투르겐 폭포"], "mountain_lake"),
    ("비슈케크 오쉬 바자르와 맛집: 키르기스 음식·라그만·시장 구경 동선", "bishkek-osh-bazaar", "비슈케크", "kg", "spot", ["오쉬 바자르", "비슈케크 맛집", "키르기스스탄 음식", "비슈케크 시장"], "bazaar"),
    ("중앙아시아 여행자 보험과 병원 이용: 응급 상황·약국·의료비 대비법", "central-asia-travel-insurance", "중앙아시아", "prep", "prep", ["중앙아시아 여행자 보험", "우즈베키스탄 병원", "카자흐스탄 약국", "여행 응급 상황"], "passport"),
]
existing = {x["slug"] for x in t}
nid = max(x["id"] for x in t)
for topic, slug, city, reg, cat, kw, scene in new:
    assert slug not in existing, slug
    nid += 1
    t.append({"id": nid, "topic": topic, "slug": slug, "city": city, "region": reg, "cat": cat,
              "keywords": kw, "scene": scene, "status": "todo"})
json.dump(t, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(sum(x["status"] == "todo" for x in t))
