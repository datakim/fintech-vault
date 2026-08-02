#!/usr/bin/env python3
"""FDE 고찰 — 그림 3종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap, wobble_line,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


# ── 1. 이름들의 지도 (참여 시점 × 코드 비중)
def d1_map():
    r = R(211); b = []
    W, H = 860, 520
    b.append(T(430, 46, "이름은 많은데, 놓고 보면 축은 둘뿐이다", 28, INK, weight="bold"))
    b.append(ul(r, 195, 665, 63))

    # 축
    b.append(f'<path d="{wobble_line(r, 96, 430, 800, 430, 1.4)}" fill="none" stroke="{INK_LIGHT}" stroke-width="1.6" stroke-linecap="round"/>')
    b.append(f'<path d="{wobble_line(r, 96, 430, 96, 96, 1.4)}" fill="none" stroke="{INK_LIGHT}" stroke-width="1.6" stroke-linecap="round"/>')
    b.append(T(448, 462, "언제 들어가는가", 19, INK, weight="bold"))
    b.append(T(150, 452, "계약 전", 15, INK_LIGHT))
    b.append(T(760, 452, "운영 이후", 15, INK_LIGHT))
    b.append(T(62, 264, "코드 비중", 19, INK, weight="bold", rot=-90))
    b.append(T(74, 118, "높음", 14, INK_LIGHT))
    b.append(T(74, 412, "낮음", 14, INK_LIGHT))

    # 점들
    pts = [
        (190, 386, "세일즈 엔지니어", "첫 데모 ~ 계약", "gray", INK_LIGHT),
        (395, 386, "디플로이먼트 전략가", "무엇을 왜 만들지", "purple", PURPLE),
        (300, 286, "솔루션 아키텍트", "기술 검토 ~ 설계", "blue", BLUE),
        (560, 246, "레지던트 솔루션 아키텍트", "구축 기간 상주", "teal", TEAL),
        (580, 150, "FDE · FDSE", "킥오프 ~ 프로덕션 ~ 갱신", "amber", AMBER),
        (705, 330, "커스터머 석세스 엔지니어", "운영 중 대응", "green", GREEN),
    ]
    for x, y, name, when, wash, col in pts:
        w = 190
        b.append(box(r, x - w / 2, y - 26, w, 52, wash, col, sw=1.5, amp=1.3))
        b.append(T(x, y - 4, name, 16, col, weight="bold"))
        b.append(T(x, y + 16, when, 13.5, INK_LIGHT))

    b.append(T(430, 494, "부르는 이름은 달라도, 고객 옆에서 · 코드를 쓰며 · 결과를 책임진다는 조합의 정도 차이다", 18, INK_LIGHT))
    return W, H, "".join(b)


# ── 2. FDE가 필요한 사분면
def d2_quadrant():
    r = R(222); b = []
    W, H = 840, 470
    b.append(T(420, 46, "FDE가 필요한 칸은 딱 하나다", 28, INK, weight="bold"))
    b.append(ul(r, 240, 600, 63))

    b.append(T(430, 100, "사는 사람", 18, INK, weight="bold"))
    b.append(T(300, 128, "기술을 아는 구매자", 16, INK_LIGHT))
    b.append(T(600, 128, "기술을 모르는 구매자", 16, INK_LIGHT))
    b.append(T(96, 280, "파는 것", 18, INK, weight="bold", rot=-90))

    cells = [
        (170, 148, "gray", INK_LIGHT, "복잡한 제품", "필요 없음",
         ["GitHub · Datadog", "구매자가 엔지니어라", "복잡도를 알아서 흡수한다"], False),
        (470, 148, "amber", AMBER, "복잡한 제품", "여기만 필요하다",
         ["팔란티어 · 그리고 요즘의", "에이전틱 제품 대부분", "고객이 뭘 할 수 있는지 모른다"], True),
        (170, 304, "gray", INK_LIGHT, "단순한 제품", "필요 없음",
         ["설정만 하면 되고", "개발할 물건이 아니다"], False),
        (470, 304, "gray", INK_LIGHT, "단순한 제품", "필요 없음",
         ["슬랙 · 지라", "구매자가 몰라도 쓸 수 있다"], False),
    ]
    for x, y, wash, col, kind, verdict, lines, hot in cells:
        h = 148 if hot else 132
        b.append(box(r, x, y, 300, h, wash, col, sw=1.9 if hot else 1.4))
        b.append(T(x + 150, y + 30, kind, 17, INK_LIGHT))
        b.append(T(x + 150, y + 58, verdict, 21, col, weight="bold"))
        for i, ln in enumerate(lines):
            b.append(T(x + 150, y + 88 + i * 22, ln, 14.5, INK))

    b.append(T(420, 456, "\"하고 싶은가\"가 아니라 \"이 칸에 있는가\"를 먼저 물어야 한다", 19, INK_LIGHT))
    return W, H, "".join(b)


# ── 3. FDE와 외주사를 가르는 것
def d3_platform():
    r = R(233); b = []
    W, H = 840, 450
    b.append(T(420, 46, "같은 일처럼 보이는데 결과가 갈린다", 28, INK, weight="bold"))
    b.append(ul(r, 210, 630, 63))

    b.append(box(r, 36, 84, 372, 226, "red", RED, sw=1.8))
    b.append(T(222, 116, "플랫폼이 없으면", 21, RED, weight="bold"))
    b.append(T(222, 152, "고객마다 맨바닥부터 만든다", 17.5, INK))
    b.append(T(222, 180, "저장소가 55개로 늘어난다", 17.5, INK))
    b.append(T(222, 208, "아무도 유지보수를 못 한다", 17.5, INK))
    b.append(box(r, 66, 226, 312, 62, None, RED, sw=1.3, amp=1.2))
    b.append(T(222, 252, "이건 FDE 조직이 아니라", 16, INK_LIGHT))
    b.append(T(222, 276, "외주 개발사다", 19, RED, weight="bold"))

    b.append(box(r, 432, 84, 372, 226, "green", GREEN, sw=1.8))
    b.append(T(618, 116, "플랫폼이 있으면", 21, GREEN, weight="bold"))
    b.append(T(618, 152, "프리미티브 위에 조립한다", 17.5, INK))
    b.append(T(618, 180, "고객이 늘어도 코드는 안 늘어난다", 17.5, INK))
    b.append(T(618, 208, "일반화할 것은 플랫폼으로 올린다", 17.5, INK))
    b.append(box(r, 462, 226, 312, 62, None, GREEN, sw=1.3, amp=1.2))
    b.append(T(618, 252, "그 프리미티브 층이", 16, INK_LIGHT))
    b.append(T(618, 276, "온톨로지가 맡는 자리다", 19, GREEN, weight="bold"))

    b.append(box(r, 36, 332, 768, 62, "amber", AMBER, sw=1.8))
    b.append(T(420, 360, "그래서 판별 질문은 하나다", 20, AMBER, weight="bold"))
    b.append(T(420, 384, "\"당신 회사의 FDE는 지금 무엇 위에 조립하고 있는가?\"", 18, INK))

    b.append(T(420, 434, "여기에 답이 없으면 이름만 FDE다", 18, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {
    "fde-map": d1_map,
    "fde-quadrant": d2_quadrant,
    "fde-platform": d3_platform,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
