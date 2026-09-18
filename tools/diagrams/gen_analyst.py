#!/usr/bin/env python3
"""앤트로픽 데이터팀 소고 — 그림 2종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap, wobble_line,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


def d1_before_sql():
    r = R(1101); b = []
    W, H = 900, 500
    b.append(T(450, 46, "SQL 앞에 정할 게 셋 있다", 28, INK, weight="bold"))
    b.append(ul(r, 300, 600, 63))

    b.append(box(r, 250, 84, 400, 48, "gray", INK, sw=1.8))
    b.append(T(450, 115, "\"지난달 활성 고객이 몇 명이야?\"", 19, INK, weight="bold"))

    choices = [
        (36, "blue", BLUE, "활성의 정의", "로그인만 해도?", "결제까지 해야?"),
        (320, "amber", AMBER, "제외 기준", "환불 고객은?", "부정거래 계정은?"),
        (604, "purple", PURPLE, "공식 테이블", "비슷한 게 여럿인데", "어느 게 기준?"),
    ]
    for x, wash, col, name, l1, l2 in choices:
        b.append(arr(r, x + 130, 140, x + 130, 160, INK_LIGHT, 1.4, 7))
        b.append(box(r, x, 164, 260, 96, wash, col, sw=1.8))
        b.append(T(x + 130, 194, name, 19, col, weight="bold"))
        b.append(T(x + 130, 222, l1, 14, INK))
        b.append(T(x + 130, 244, l2, 14, INK))
    for x in (166, 450, 734):
        b.append(arr(r, x, 266, x, 288, INK_LIGHT, 1.4, 7))

    b.append(box(r, 36, 292, 828, 56, None, INK, sw=1.4, amp=1.2))
    b.append(T(450, 327, "SELECT COUNT(*) FROM users WHERE ...     실행 에러 0건", 17, INK))

    b.append(box(r, 36, 372, 828, 52, "red", RED, sw=1.8))
    b.append(T(450, 404, "셋 중 하나만 다르게 골라도 SQL은 멀쩡히 돌고 숫자는 틀린다", 19, RED, weight="bold"))

    b.append(T(450, 458, "앤트로픽: 틀린 답의 80%는 정답이 과거 SQL 더미 안에 있었다. 정보가 아니라 매핑이 문제였다.", 15, INK_LIGHT))
    b.append(T(450, 484, "사람은 이 셋을 되묻고 시작한다. AI는 누가 적어줘야 안다.", 15, INK_LIGHT))
    return W, H, "".join(b)


def d2_deliverables():
    r = R(1102); b = []
    W, H = 900, 480
    b.append(T(450, 46, "분석가가 내놓는 것", 28, INK, weight="bold"))
    b.append(ul(r, 320, 580, 63))

    b.append(box(r, 36, 84, 380, 250, "gray", INK_LIGHT, sw=1.7))
    b.append(T(226, 116, "지금까지", 20, INK_LIGHT, weight="bold"))
    chain = ["요청", "쿼리", "숫자"]
    for i, s in enumerate(chain):
        x = 66 + i * 110
        b.append(box(r, x, 140, 90, 44, None, INK, sw=1.3, amp=1.2))
        b.append(T(x + 45, 168, s, 16, INK))
        if i < 2:
            b.append(arr(r, x + 94, 162, x + 106, 162, INK_LIGHT, 1.3, 6))
    b.append(T(226, 224, "이 숫자가 맞는지, 활성이 뭔지,", 14, INK))
    b.append(T(226, 246, "어느 테이블이 맞는지는", 14, INK))
    b.append(T(226, 268, "분석가 머릿속에 있었다", 14, INK))
    b.append(T(226, 306, "산출물에는 쿼리와 숫자만 남는다", 13.5, INK_LIGHT))

    b.append(arr(r, 426, 208, 474, 208, INK_LIGHT, 1.8))

    b.append(box(r, 484, 84, 380, 250, "amber", AMBER, sw=1.9))
    b.append(T(674, 116, "앞으로", 20, AMBER, weight="bold"))
    items = [("정의", "활성 고객은 이렇게 센다"), ("절차", "이런 질문은 이 순서로 푼다"),
             ("정답셋", "답이 알려진 질문 몇십 개"), ("유지 루프", "데이터가 바뀌면 같이 바뀐다")]
    for i, (name, desc) in enumerate(items):
        y = 132 + i * 42
        b.append(box(r, 504, y, 340, 38, None, AMBER, sw=1.2, amp=1.1))
        b.append(T(560, y + 25, name, 15, AMBER, weight="bold"))
        b.append(T(700, y + 25, desc, 13, INK))
    b.append(T(674, 318, "문서는 AI가 만들고, 정의는 사람이 소유한다", 13.5, INK_LIGHT))

    b.append(box(r, 36, 362, 828, 60, "red", RED, sw=1.8))
    b.append(T(450, 388, "정의를 방치하면 한 달 만에 정확도 95%에서 65%로", 19, RED, weight="bold"))
    b.append(T(450, 411, "그래서 정의를 변환 코드 옆에 두고 CI가 물게 했다. 데이터 PR의 90%가 스킬 수정을 같이 담는다.", 13.5, INK))

    b.append(T(450, 456, "쿼리는 누가 짜도 되는데, 활성 고객이 뭔지는 여전히 누군가 정해야 한다", 15.5, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {"analyst-before-sql": d1_before_sql, "analyst-deliverables": d2_deliverables}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
