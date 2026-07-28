#!/usr/bin/env python3
"""[잡담] AI에 평가받는 시대 — 그림 3종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


# ── 1. 예전 피드백 루프 vs 지금
def d1_loop():
    r = R(11); b = []
    W, H = 840, 430
    b.append(T(420, 46, "보고서를 제일 먼저 읽는 사람이 바뀌었다", 28, INK, weight="bold"))
    b.append(ul(r, 190, 650, 63))

    # 예전
    b.append(box(r, 36, 80, 768, 130, "gray", INK_LIGHT, sw=1.6))
    b.append(T(60, 108, "예전", 22, INK_LIGHT, anchor="start", weight="bold"))
    seq = [("내가 쓴 보고서", 150), ("팀장이 읽는다", 150), ("피드백", 130)]
    x = 170
    for name, bw in seq:
        b.append(box(r, x, 122, bw, 52, None, INK, sw=1.3, amp=1.2))
        b.append(T(x + bw / 2, 154, name, 18, INK))
        if name != "피드백":
            b.append(arr(r, x + bw + 4, 148, x + bw + 26, 148, INK_LIGHT, 1.4, 8))
        x += bw + 30
    b.append(T(420, 196, "그 사람의 경험과 취향이 곧 기준이었다", 17, INK_LIGHT))

    # 지금
    b.append(box(r, 36, 228, 768, 158, "amber", AMBER, sw=1.8))
    b.append(T(60, 256, "지금", 22, AMBER, anchor="start", weight="bold"))
    b.append(box(r, 128, 274, 148, 52, None, INK, sw=1.3, amp=1.2))
    b.append(T(202, 306, "내가 쓴 보고서", 18, INK))
    b.append(arr(r, 280, 300, 306, 300, INK_LIGHT, 1.4, 8))
    b.append(box(r, 310, 274, 172, 52, "red", RED, sw=1.6, amp=1.3))
    b.append(T(396, 297, "팀장이 AI에 넣는다", 17.5, RED, weight="bold"))
    b.append(T(396, 317, "\"요약하고 비평해줘\"", 15, INK))
    b.append(arr(r, 486, 300, 512, 300, INK_LIGHT, 1.4, 8))
    b.append(box(r, 516, 274, 152, 52, None, INK, sw=1.3, amp=1.2))
    b.append(T(592, 297, "거기에 자기 판단을", 16.5, INK))
    b.append(T(592, 317, "얹어서 (또는 그대로)", 16.5, INK))
    b.append(arr(r, 672, 300, 692, 300, INK_LIGHT, 1.4, 8))
    b.append(box(r, 696, 274, 96, 52, None, INK, sw=1.3, amp=1.2))
    b.append(T(744, 306, "피드백", 18, INK))
    b.append(T(420, 366, "내 글을 사람보다 먼저 읽는 건 이제 모델인 경우가 많다", 18, INK))

    b.append(T(420, 414, "채용 서류도, 코드 리뷰도, 기획안도 어딘가에서 한 번은 이 경로를 지난다", 18, INK_LIGHT))
    return W, H, "".join(b)


# ── 2. 교차검증 흐름
def d2_cross():
    r = R(22); b = []
    W, H = 840, 450
    b.append(T(420, 46, "남이 돌리기 전에 내가 먼저 돌린다", 28, INK, weight="bold"))
    b.append(ul(r, 215, 625, 63))

    b.append(box(r, 330, 82, 180, 54, "gray", INK, sw=1.7))
    b.append(T(420, 115, "내가 만든 결과물", 19, INK, weight="bold"))
    b.append(arr(r, 420, 138, 420, 166, INK_LIGHT, 1.5))

    b.append(box(r, 250, 172, 340, 60, "blue", BLUE, sw=1.7))
    b.append(T(420, 196, "A 모델에 비평을 시킨다", 19, BLUE, weight="bold"))
    b.append(T(420, 220, "\"이 주장을 무너뜨려봐\"", 16.5, INK))
    b.append(arr(r, 420, 234, 420, 262, INK_LIGHT, 1.5))

    b.append(box(r, 210, 268, 420, 60, "green", GREEN, sw=1.7))
    b.append(T(420, 292, "그 비평을 B 모델에 다시 넣는다", 19, GREEN, weight="bold"))
    b.append(T(420, 316, "\"이 비평이 타당한가? 과한 지적은 없나?\"", 16.5, INK))
    b.append(arr(r, 420, 330, 420, 358, INK_LIGHT, 1.5))

    b.append(box(r, 288, 364, 264, 54, "amber", AMBER, sw=1.7))
    b.append(T(420, 397, "남는 지적만 골라서 고친다", 19, AMBER, weight="bold"))

    # 옆 메모
    b.append(T(122, 200, "계열이 다른 모델은", 17, INK_LIGHT))
    b.append(T(122, 222, "다른 걸 잡아낸다", 17, INK_LIGHT))
    b.append(T(700, 290, "한쪽만 믿으면", 17, INK_LIGHT))
    b.append(T(700, 312, "그 모델의 버릇까지", 17, INK_LIGHT))
    b.append(T(700, 334, "같이 따라온다", 17, INK_LIGHT))

    b.append(T(420, 438, "두 모델이 함께 짚은 지적은 대체로 진짜다", 18, INK_LIGHT))
    return W, H, "".join(b)


# ── 3. 검증을 시키는 네 가지 방식
def d3_ways():
    r = R(33); b = []
    W, H = 840, 400
    b.append(T(420, 46, "\"평가해줘\"라고 하면 칭찬만 돌아온다", 28, INK, weight="bold"))
    b.append(ul(r, 185, 655, 63))

    ways = [
        (36, "red", RED, "요약시켜 보기", ["\"세 줄로 요약해봐\"", "내 의도대로 안 나오면", "글이 잘못된 것이다"]),
        (238, "blue", BLUE, "반박시켜 보기", ["\"이 주장을 무너뜨려봐\"", "칭찬 대신 반례를", "받아내는 게 목적이다"]),
        (440, "green", GREEN, "빠진 것 찾기", ["\"이 글에 없는데", "있어야 할 건 뭔가\"", "빈칸은 안 보인다"]),
        (642, "amber", AMBER, "기준 주고 채점", ["막연한 평가 대신", "체크리스트를 준다", "결과가 일관된다"]),
    ]
    for x, wash, col, title, lines in ways:
        b.append(box(r, x, 82, 162, 216, wash, col, sw=1.7))
        b.append(T(x + 81, 116, title, 20, col, weight="bold"))
        for i, ln in enumerate(lines):
            b.append(T(x + 81, 158 + i * 30, ln, 16, INK))

    b.append(T(420, 344, "무엇을 물었느냐가 무엇이 돌아오는지를 정한다", 20, INK))
    b.append(T(420, 376, "그래서 결국, 아는 만큼만 물을 수 있다", 18, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {
    "review-loop": d1_loop,
    "review-cross": d2_cross,
    "review-ways": d3_ways,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
