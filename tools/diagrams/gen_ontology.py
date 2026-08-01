#!/usr/bin/env python3
"""월드모델의 두 계보와 온톨로지 — 그림 3종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


# ── 1. 네 축이 세 층위로 갈린다
def d1_axes():
    r = R(51); b = []
    W, H = 860, 470
    b.append(T(430, 46, "네 축을 형식론 계보로 다시 읽으면", 28, INK, weight="bold"))
    b.append(ul(r, 205, 655, 63))

    rows = [
        (86, ["① 무엇이 존재하는가", "② 지금 어떤 상태인가"], "존재론",
         "온톨로지 — 개념·분류(TBox), 개체·사실(ABox)", "blue", BLUE, 96),
        (198, ["③ 어떤 변화가 허용되는가"], "동역학",
         "행동 형식론 — PDDL의 전제조건·효과, 상황 계산법", "green", GREEN, 68),
        (282, ["④ 무엇이 금지·제한되는가"], "규범",
         "무결성 제약, 접근통제, 의무논리(deontic logic)", "red", RED, 68),
    ]
    for y, axes, layer, formal, wash, col, h in rows:
        b.append(box(r, 36, y, 300, h, "gray", INK_LIGHT, sw=1.4))
        for i, a in enumerate(axes):
            b.append(T(186, y + (34 if len(axes) == 1 else 30 + i * 34), a, 19, INK))
        b.append(arr(r, 344, y + h / 2, 384, y + h / 2, INK_LIGHT, 1.6))
        b.append(box(r, 392, y, 130, h, wash, col, sw=1.7))
        b.append(T(457, y + h / 2 + 7, layer, 22, col, weight="bold"))
        b.append(box(r, 534, y, 290, h, None, col, sw=1.3, amp=1.2))
        b.append(T(679, y + h / 2 + 6, formal, 15.5, INK))

    b.append(box(r, 36, 372, 788, 62, "amber", AMBER, sw=1.8))
    b.append(T(430, 398, "①~③은 \"무엇이 가능한가\", ④만 \"무엇을 해도 되는가\"를 묻는다", 20, INK, weight="bold"))
    b.append(T(430, 422, "논리학에서는 앞을 알레틱, 뒤를 데온틱 양상이라 부른다", 17, INK_LIGHT))

    b.append(T(430, 458, "네 축은 한 줄로 늘어선 목록이 아니라, 성격이 다른 세 층이 겹쳐 있는 구조다", 17, INK_LIGHT))
    return W, H, "".join(b)


# ── 2. 알레틱과 데온틱 사이의 간극
def d2_gap():
    r = R(62); b = []
    W, H = 840, 470
    b.append(T(420, 46, "관측을 아무리 늘려도 넘어가지 못하는 선", 28, INK, weight="bold"))
    b.append(ul(r, 175, 665, 63))

    b.append(box(r, 36, 84, 356, 236, "blue", BLUE, sw=1.8))
    b.append(T(214, 116, "알레틱 — 무엇이 가능한가", 21, BLUE, weight="bold"))
    b.append(T(214, 152, "공이 떨어진다", 18, INK))
    b.append(T(214, 180, "이 잔고로는 결제가 안 된다", 18, INK))
    b.append(T(214, 208, "이 API는 3초 안에 응답한다", 18, INK))
    b.append(box(r, 62, 228, 304, 68, None, BLUE, sw=1.2, amp=1.2))
    b.append(T(214, 254, "세계에 관한 사실이라서", 17, INK))
    b.append(T(214, 280, "관측에서 배울 수 있다", 17, INK))

    b.append(box(r, 448, 84, 356, 236, "red", RED, sw=1.8))
    b.append(T(626, 116, "데온틱 — 무엇을 해도 되는가", 21, RED, weight="bold"))
    b.append(T(626, 152, "이 거래를 승인해도 되는가", 18, INK))
    b.append(T(626, 180, "이 고객정보를 조회해도 되는가", 18, INK))
    b.append(T(626, 208, "이 환불을 자동 처리해도 되는가", 18, INK))
    b.append(box(r, 474, 228, 304, 68, None, RED, sw=1.2, amp=1.2))
    b.append(T(626, 254, "우리가 정한 규범이라서", 17, INK))
    b.append(T(626, 280, "관측 어디에도 없다", 17, INK))

    # 간극
    b.append(T(420, 176, "?", 40, INK_LIGHT, weight="bold"))
    b.append(T(420, 214, "건널 수", 16, INK_LIGHT))
    b.append(T(420, 234, "없다", 16, INK_LIGHT))

    b.append(box(r, 36, 344, 768, 82, "amber", AMBER, sw=1.8))
    b.append(T(420, 374, "사실(is)에서 당위(ought)는 도출되지 않는다 — 흄이 1739년에 지적한 그 간극", 20, INK, weight="bold"))
    b.append(T(420, 404, "그래서 뉴럴 월드모델이 규범을 못 배우는 건 데이터가 모자라서가 아니다", 18, INK))

    b.append(T(420, 456, "범주가 다른 문제라서, 모델을 키운다고 넘어가지지 않는다", 18, INK_LIGHT))
    return W, H, "".join(b)


# ── 3. 뉴로심볼릭의 역할 분담
def d3_split():
    r = R(73); b = []
    W, H = 840, 480
    b.append(T(420, 46, "각자의 구멍에 상대가 정확히 들어간다", 28, INK, weight="bold"))
    b.append(ul(r, 190, 650, 63))

    # 뉴럴
    b.append(box(r, 36, 84, 356, 226, "green", GREEN, sw=1.8))
    b.append(T(214, 116, "뉴럴 계보", 22, GREEN, weight="bold"))
    b.append(T(214, 150, "잘하는 것", 17, GREEN, weight="bold"))
    b.append(T(214, 178, "지저분한 현실을 기호로 옮긴다", 17.5, INK))
    b.append(T(214, 202, "본 적 없는 상황도 뭉뚱그려 읽는다", 17.5, INK))
    b.append(T(214, 240, "못 하는 것", 17, RED, weight="bold"))
    b.append(T(214, 268, "코너 케이스에서 흔들리고", 17.5, INK))
    b.append(T(214, 292, "무엇도 보장하지 못한다", 17.5, INK))

    # 심볼릭
    b.append(box(r, 448, 84, 356, 226, "purple", PURPLE, sw=1.8))
    b.append(T(626, 116, "심볼릭 계보", 22, PURPLE, weight="bold"))
    b.append(T(626, 150, "잘하는 것", 17, GREEN, weight="bold"))
    b.append(T(626, 178, "허용된 전이만 실행한다", 17.5, INK))
    b.append(T(626, 202, "검증·감사가 구조로 보장된다", 17.5, INK))
    b.append(T(626, 240, "못 하는 것", 17, RED, weight="bold"))
    b.append(T(626, 268, "세계를 다 적어야 하고", 17.5, INK))
    b.append(T(626, 292, "안 적은 상황 앞에서 멈춘다", 17.5, INK))

    b.append(arr(r, 400, 200, 440, 200, INK_LIGHT, 1.6))
    b.append(arr(r, 440, 250, 400, 250, INK_LIGHT, 1.6))

    b.append(box(r, 36, 334, 768, 106, "amber", AMBER, sw=1.8))
    b.append(T(420, 364, "그래서 역할 분담이 임의로 정해진 게 아니다", 21, AMBER, weight="bold"))
    b.append(T(420, 398, "뉴럴은 접지를 맡는다 — 열린 세계를 읽어 기호로 바꾼다", 18, INK))
    b.append(T(420, 424, "심볼릭은 집행을 맡는다 — 닫힌 세계에서 허용된 것만 통과시킨다", 18, INK))

    b.append(T(420, 466, "가능성은 넓게 열어두고, 실행은 좁고 안전하게 묶는다", 18, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {
    "onto-axes": d1_axes,
    "onto-gap": d2_gap,
    "onto-split": d3_split,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
