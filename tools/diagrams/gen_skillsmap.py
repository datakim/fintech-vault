#!/usr/bin/env python3
"""AI 엔지니어링 스킬맵 분석 — 그림 3종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


# ── 1. 평면 목록이 아니라 층이다
def d1_layers():
    r = R(311); b = []
    W, H = 840, 470
    b.append(T(420, 46, "나란한 목록으로 읽으면 놓치는 것", 28, INK, weight="bold"))
    b.append(ul(r, 218, 622, 63))

    b.append(T(210, 96, "제시된 순서", 18, INK_LIGHT, weight="bold"))
    items = ["① AI 앱 구축·배포", "② 소프트웨어 기본기", "③ 코딩 에이전트 활용", "④ 빌드 형성하기"]
    y = 116
    for it in items:
        b.append(box(r, 44, y, 332, 44, "gray", INK_LIGHT, sw=1.3, amp=1.2))
        b.append(T(210, y + 29, it, 18, INK))
        y += 54

    b.append(arr(r, 392, 220, 436, 220, INK_LIGHT, 1.6))
    b.append(T(414, 200, "다시", 15, INK_LIGHT))
    b.append(T(414, 254, "쌓으면", 15, INK_LIGHT))

    b.append(T(650, 96, "실제 의존 관계", 18, INK_LIGHT, weight="bold"))
    stack = [
        (116, "④ 빌드 형성하기", "무엇을 만들지 정한다", "purple", PURPLE),
        (180, "① AI 앱 구축·배포", "확률적 부품을 다룬다", "amber", AMBER),
        (244, "③ 코딩 에이전트 활용", "만드는 속도를 올린다", "green", GREEN),
        (308, "② 소프트웨어 기본기", "나머지 셋이 딛고 서는 바닥", "blue", BLUE),
    ]
    for y0, name, desc, wash, col in stack:
        b.append(box(r, 456, y0, 348, 56, wash, col, sw=1.7))
        b.append(T(630, y0 + 24, name, 18, col, weight="bold"))
        b.append(T(630, y0 + 44, desc, 15, INK_LIGHT))

    b.append(T(420, 404, "②는 나머지와 나란히 놓일 항목이 아니라, 나머지가 성립하는 조건이다", 19, INK))
    b.append(T(420, 436, "기본기 없이 에이전트를 쓰면 무엇을 맡겼는지도 모른 채 받게 된다", 17, INK_LIGHT))
    return W, H, "".join(b)


# ── 2. 네 가지를 관통하는 축
def d2_verify():
    r = R(322); b = []
    W, H = 860, 470
    b.append(T(430, 46, "네 항목 전부에 같은 것이 들어 있다", 28, INK, weight="bold"))
    b.append(ul(r, 205, 655, 63))

    rows = [
        (88, "① AI 앱 구축", "평가와 오류 분석 루프", "blue", BLUE),
        (168, "② 소프트웨어 기본기", "무엇이 틀릴 수 있는지 아는 것", "green", GREEN),
        (248, "③ 코딩 에이전트", "검증기를 쥐여줘 스스로 닫게 한다", "amber", AMBER),
        (328, "④ 빌드 형성", "무엇이 완료인지를 정한다", "purple", PURPLE),
    ]
    for y, name, what, wash, col in rows:
        b.append(box(r, 36, y, 300, 64, wash, col, sw=1.6))
        b.append(T(186, y + 40, name, 19, col, weight="bold"))
        b.append(arr(r, 344, y + 32, 380, y + 32, INK_LIGHT, 1.4, 8))
        b.append(box(r, 388, y, 436, 64, None, col, sw=1.3, amp=1.2))
        b.append(T(606, y + 40, what, 18, INK))

    b.append(box(r, 36, 408, 788, 46, "amber", AMBER, sw=1.8))
    b.append(T(430, 438, "넷 다 \"무엇이 맞는지 어떻게 아는가\"로 수렴한다", 21, INK, weight="bold"))
    return W, H, "".join(b)


# ── 3. 지도에 없는 것
def d3_missing():
    r = R(333); b = []
    W, H = 840, 440
    b.append(T(420, 46, "지도에 흐리게 그려진 곳", 28, INK, weight="bold"))
    b.append(ul(r, 262, 578, 63))

    items = [
        (36, "red", RED, "배포 이후", ["비용 구조, 관측 가능성,", "조용한 품질 저하.", "\"배포\"는 한 단어로만 있다"]),
        (302, "amber", AMBER, "도메인 지식", ["넷 중 어디에도 없다.", "그런데 무엇을 만들지는", "대개 도메인이 정한다"]),
        (568, "purple", PURPLE, "방법론의 시차", ["채용 공고 1만 건은", "이미 합의된 것만 담는다.", "앞선 것은 공고에 없다"]),
    ]
    for x, wash, col, title, lines in items:
        b.append(box(r, x, 84, 236, 208, wash, col, sw=1.8))
        b.append(T(x + 118, 120, title, 21, col, weight="bold"))
        for i, ln in enumerate(lines):
            b.append(T(x + 118, 164 + i * 30, ln, 16, INK))

    b.append(T(420, 340, "클러스터링은 데이터의 중심을 찾지, 가장자리를 찾지 않는다", 20, INK))
    b.append(T(420, 372, "그래서 이 지도는 지금 합의된 것의 사진에 가깝다", 18, INK_LIGHT))
    b.append(T(420, 412, "빠졌다는 게 아니라, 흐리게 그려진 곳을 알고 봐야 한다는 뜻이다", 17, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {
    "skills-layers": d1_layers,
    "skills-verify": d2_verify,
    "skills-missing": d3_missing,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
