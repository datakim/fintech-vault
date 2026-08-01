#!/usr/bin/env python3
"""팔란티어 온톨로지 — 그림 3종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


# ── 1. 세 개의 층
def d1_layers():
    r = R(81); b = []
    W, H = 840, 440
    b.append(T(420, 46, "명사 · 동사 · 문법으로 나눠 보기", 28, INK, weight="bold"))
    b.append(ul(r, 218, 622, 63))

    rows = [
        (84, "의미 (Semantic)", "명사", "blue", BLUE,
         "Object Type · Property · Link Type",
         "기계, 고객, 구매주문 그리고 그들 사이의 관계"),
        (196, "운동 (Kinetic)", "동사", "green", GREEN,
         "Action Type · Function",
         "점검 예약, 주문 취소, 환불 승인 — 실제로 세계를 바꾸는 것"),
        (308, "동적 (Dynamic)", "문법", "red", RED,
         "런타임 보안 · 권한 · 목적 기반 정책",
         "누가 무엇을 어떤 목적으로 할 수 있는지를 실행 시점에 판단"),
    ]
    for y, name, role, wash, col, comps, desc in rows:
        b.append(box(r, 36, y, 768, 96, wash, col, sw=1.8))
        b.append(T(150, y + 40, name, 21, col, weight="bold"))
        b.append(box(r, 96, y + 52, 108, 32, None, col, sw=1.2, amp=1.1))
        b.append(T(150, y + 74, role, 19, INK, weight="bold"))
        b.append(T(512, y + 40, comps, 18, INK))
        b.append(T(512, y + 70, desc, 16, INK_LIGHT))

    b.append(T(420, 428, "대부분의 데이터 플랫폼은 첫 번째 층에서 멈춘다", 19, INK_LIGHT))
    return W, H, "".join(b)


# ── 2. 네 축으로 재보기
def d2_axes():
    r = R(92); b = []
    W, H = 860, 470
    b.append(T(430, 46, "네 축으로 두 온톨로지를 나란히 재보면", 28, INK, weight="bold"))
    b.append(ul(r, 205, 655, 63))

    b.append(box(r, 300, 80, 262, 44, "gray", INK_LIGHT, sw=1.5))
    b.append(T(431, 110, "고전 온톨로지 (OWL·RDF)", 19, INK, weight="bold"))
    b.append(box(r, 574, 80, 250, 44, "amber", AMBER, sw=1.6))
    b.append(T(699, 110, "팔란티어 온톨로지", 19, AMBER, weight="bold"))

    rows = [
        (134, "① 무엇이 존재하는가", "강하다", "있다", GREEN, AMBER,
         "클래스 계층 · 자동 추론", "Object Type · 추론은 없음"),
        (208, "② 지금 어떤 상태인가", "있다", "강하다", AMBER, GREEN,
         "ABox — 대체로 정적", "실시간 · 쓰기까지"),
        (282, "③ 어떤 변화가 허용되는가", "없다", "강하다", RED, GREEN,
         "행동 개념이 아예 없다", "Action Type이 제품의 중심"),
        (356, "④ 무엇이 금지되는가", "약하다", "강하다", RED, GREEN,
         "논리적 제약에 그친다", "권한 · 정책 · 감사 내장"),
    ]
    for y, axis, l, rr, lcol, rcol, ldesc, rdesc in rows:
        b.append(box(r, 36, y, 252, 62, None, INK_LIGHT, sw=1.2, amp=1.2))
        b.append(T(162, y + 38, axis, 18, INK))
        b.append(box(r, 300, y, 262, 62, None, lcol, sw=1.3, amp=1.2))
        b.append(T(431, y + 26, l, 19, lcol, weight="bold"))
        b.append(T(431, y + 48, ldesc, 14.5, INK_LIGHT))
        b.append(box(r, 574, y, 250, 62, None, rcol, sw=1.3, amp=1.2))
        b.append(T(699, y + 26, rr, 19, rcol, weight="bold"))
        b.append(T(699, y + 48, rdesc, 14.5, INK_LIGHT))

    b.append(T(430, 446, "학술 기준으로는 온톨로지가 아니지만, 에이전트가 필요로 하는 축은 오히려 더 채워져 있다", 18, INK))
    return W, H, "".join(b)


# ── 3. 액션은 그냥 함수가 아니다
def d3_action():
    r = R(103); b = []
    W, H = 840, 420
    b.append(T(420, 46, "액션은 그냥 함수가 아니다", 28, INK, weight="bold"))
    b.append(ul(r, 262, 578, 63))

    # 그냥 함수
    b.append(box(r, 36, 84, 768, 92, "gray", INK_LIGHT, sw=1.5))
    b.append(T(110, 136, "그냥 함수", 20, INK_LIGHT, weight="bold"))
    x = 216
    for s in ["입력", "실행", "결과"]:
        b.append(box(r, x, 106, 140, 48, None, INK_LIGHT, sw=1.2, amp=1.2))
        b.append(T(x + 70, 136, s, 18, INK))
        if s != "결과":
            b.append(arr(r, x + 144, 130, x + 168, 130, INK_LIGHT, 1.4, 7))
        x += 172

    # 통제된 연산
    b.append(box(r, 36, 196, 768, 124, "green", GREEN, sw=1.8))
    b.append(T(110, 246, "통제된 연산", 20, GREEN, weight="bold"))
    b.append(T(110, 272, "(governed)", 15, INK_LIGHT))
    steps = ["입력", "검증 규칙", "권한 확인", "실행", "원본 반영", "감사 기록"]
    x = 190
    bw = 96
    for i, s in enumerate(steps):
        hot = s in ("검증 규칙", "권한 확인", "감사 기록")
        b.append(box(r, x, 224, bw, 48, "amber" if hot else None,
                     AMBER if hot else INK, sw=1.4 if hot else 1.2, amp=1.2))
        b.append(T(x + bw / 2, 254, s, 16, AMBER if hot else INK,
                   weight="bold" if hot else "normal"))
        if i < len(steps) - 1:
            b.append(arr(r, x + bw + 2, 248, x + bw + 12, 248, INK_LIGHT, 1.3, 6))
        x += bw + 14

    b.append(T(420, 300, "노란 칸이 붙어 있느냐가 사람이 눌러도 되는 버튼과 아닌 버튼을 가른다", 17, INK))
    b.append(T(420, 366, "에이전트에게 실행 권한을 줄 때 필요한 게 정확히 이 차이다", 20, INK))
    b.append(T(420, 398, "무엇을 할 수 있는지가 아니라, 무엇을 해도 되는지가 함께 적혀 있어야 한다", 18, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {
    "palantir-layers": d1_layers,
    "palantir-axes": d2_axes,
    "palantir-action": d3_action,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
