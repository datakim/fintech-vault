#!/usr/bin/env python3
"""월드모델 두 계보의 역사 — 그림 4종 (초보자용)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


# ── 1. 같은 질문에서 갈라졌다
def d1_fork():
    r = R(111); b = []
    W, H = 840, 400
    b.append(T(420, 46, "출발점은 같은 질문 하나였다", 28, INK, weight="bold"))
    b.append(ul(r, 250, 590, 63))

    b.append(box(r, 210, 84, 420, 62, "gray", INK, sw=1.8))
    b.append(T(420, 112, "세계가 어떻게 돌아가는지를", 20, INK, weight="bold"))
    b.append(T(420, 136, "기계 안에 어떻게 넣을 것인가?", 20, INK, weight="bold"))

    b.append(arr(r, 360, 150, 250, 196, INK_LIGHT, 1.6))
    b.append(arr(r, 480, 150, 590, 196, INK_LIGHT, 1.6))

    b.append(box(r, 60, 202, 340, 130, "purple", PURPLE, sw=1.8))
    b.append(T(230, 236, "심볼릭 — 적어 넣는 쪽", 21, PURPLE, weight="bold"))
    b.append(T(230, 272, "\"사람이 규칙을 적어주자\"", 18, INK))
    b.append(T(230, 304, "논리 · 규칙 · 상태 기계", 17, INK_LIGHT))

    b.append(box(r, 440, 202, 340, 130, "green", GREEN, sw=1.8))
    b.append(T(610, 236, "뉴럴 — 보고 배우는 쪽", 21, GREEN, weight="bold"))
    b.append(T(610, 272, "\"기계가 스스로 배우게 하자\"", 18, INK))
    b.append(T(610, 304, "제어이론 · 신경망 · 예측", 17, INK_LIGHT))

    b.append(T(420, 372, "이 갈림길에서 70년이 흘렀고, 둘은 아주 다른 길을 걸었다", 19, INK_LIGHT))
    return W, H, "".join(b)


# ── 2. 심볼릭 연표
def d2_symbolic():
    r = R(122); b = []
    W, H = 860, 560
    b.append(T(430, 46, "심볼릭 — 적으려다 계속 범위를 좁혀온 역사", 28, PURPLE, weight="bold"))
    b.append(ul(r, 165, 695, 63))

    steps = [
        ("1950~60년대", "논리로 적으면 되지 않을까", "세계의 사실을 논리 문장으로 적어두면 기계가 추론한다", None),
        ("1971", "행동을 적기 시작 — STRIPS", "\"문을 열려면 앞에 있어야 하고, 열면 열린 상태가 된다\"",
         "안 변하는 것까지 다 적어야 한다 (프레임 문제)"),
        ("1970~80년대", "세계 전체는 포기, 좁은 분야만", "의료 진단, 설비 구성 — 전문가 시스템이 상업적으로 성공",
         "규칙이 수천 개 넘자 손을 못 대게 됐다"),
        ("1990~2000년대", "표준을 만들어 나눠 쓰자", "RDF · OWL — 웹 전체를 기계가 읽게 하려던 시맨틱 웹",
         "아무도 태그를 달지 않았다"),
        ("2012~", "실용적 후퇴 — 지식 그래프", "완벽한 추론은 접고 쓸모 위주로. 이게 오히려 살아남았다", None),
    ]
    y = 86
    for era, title, desc, wall in steps:
        h = 84 if wall else 62
        b.append(box(r, 36, y, 788, h, "purple", PURPLE, sw=1.5))
        b.append(T(120, y + 28, era, 17, PURPLE, weight="bold"))
        b.append(T(240, y + 28, title, 19, INK, anchor="start", weight="bold"))
        b.append(T(240, y + 52, desc, 16, INK_LIGHT, anchor="start"))
        if wall:
            b.append(box(r, 240, y + 60, 560, 20, "red", RED, sw=1.1, amp=1.0))
            b.append(T(520, y + 75, "벽 — " + wall, 15, RED))
        y += h + 12

    b.append(T(430, 542, "좁고 실패 비용이 큰 곳에서는 지금도 조용히 돌아가고 있다", 19, INK))
    return W, H, "".join(b)


# ── 3. 뉴럴 연표
def d3_neural():
    r = R(133); b = []
    W, H = 860, 560
    b.append(T(430, 46, "뉴럴 — 그리려다 계속 그릴 것을 줄여온 역사", 28, GREEN, weight="bold"))
    b.append(ul(r, 168, 692, 63))

    steps = [
        ("1960", "칼만 필터 — 뿌리는 공학이었다", "세계 모형을 수식으로 쓰고 다음을 예측. 아폴로에 실렸다",
         "그 수식을 사람이 써야 한다"),
        ("1990", "그럼 수식을 학습시키자", "신경망으로 환경의 동역학을 배우자는 발상",
         "계산력도 데이터도 없던 시절"),
        ("2018", "이름이 붙은 순간 — World Models", "눈(압축) + 기억(예측) + 손(행동). 상상한 세계 안에서 학습", None),
        ("2019~23", "산업화 — Dreamer 계열", "상상 속 학습을 다듬어 150개 넘는 과제를 설정 하나로", None),
        ("2020~", "다 그리지 말자 — MuZero, JEPA", "화면 복원을 포기하고 결정에 필요한 것만 예측한다", None),
        ("2024~", "그런데 비디오 생성이 합류", "픽셀을 통째로 그려내는 쪽이 놀라운 결과를 냈다", None),
    ]
    y = 86
    for era, title, desc, wall in steps:
        h = 78 if wall else 58
        b.append(box(r, 36, y, 788, h, "green", GREEN, sw=1.5))
        b.append(T(112, y + 26, era, 17, GREEN, weight="bold"))
        b.append(T(216, y + 26, title, 19, INK, anchor="start", weight="bold"))
        b.append(T(216, y + 48, desc, 16, INK_LIGHT, anchor="start"))
        if wall:
            b.append(box(r, 216, y + 56, 584, 18, "red", RED, sw=1.1, amp=1.0))
            b.append(T(508, y + 70, "벽 — " + wall, 15, RED))
        y += h + 12

    b.append(T(430, 540, "지금은 픽셀을 그릴 것인가 버릴 것인가로 안에서도 갈라져 있다", 19, INK))
    return W, H, "".join(b)


# ── 4. 거울상
def d4_mirror():
    r = R(144); b = []
    W, H = 840, 400
    b.append(T(420, 46, "두 계보는 거울상으로 닮았다", 28, INK, weight="bold"))
    b.append(ul(r, 245, 595, 63))

    b.append(box(r, 36, 84, 372, 168, "purple", PURPLE, sw=1.8))
    b.append(T(222, 116, "심볼릭", 22, PURPLE, weight="bold"))
    b.append(T(222, 152, "다 적으려다 못 적어서", 19, INK))
    b.append(T(222, 180, "적을 범위를 좁혀왔다", 19, INK))
    b.append(box(r, 66, 196, 312, 40, None, PURPLE, sw=1.2, amp=1.1))
    b.append(T(222, 222, "세계 전체 → 한 분야 → 한 업무", 17, INK_LIGHT))

    b.append(box(r, 432, 84, 372, 168, "green", GREEN, sw=1.8))
    b.append(T(618, 116, "뉴럴", 22, GREEN, weight="bold"))
    b.append(T(618, 152, "다 그리려다 너무 비싸서", 19, INK))
    b.append(T(618, 180, "그릴 대상을 좁혀왔다", 19, INK))
    b.append(box(r, 462, 196, 312, 40, None, GREEN, sw=1.2, amp=1.1))
    b.append(T(618, 222, "화면 전부 → 필요한 것만 → 표현만", 17, INK_LIGHT))

    b.append(box(r, 36, 274, 768, 62, "amber", AMBER, sw=1.8))
    b.append(T(420, 302, "둘 다 무엇을 포기할지를 배워온 역사다", 21, INK, weight="bold"))
    b.append(T(420, 326, "그리고 포기한 자리가 서로 정확히 반대편이라, 지금 만나고 있다", 17, INK_LIGHT))

    b.append(T(420, 376, "넓게 읽는 쪽과 좁게 보장하는 쪽이 동시에 필요해졌기 때문이다", 18, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {
    "lineage-fork": d1_fork,
    "lineage-symbolic": d2_symbolic,
    "lineage-neural": d3_neural,
    "lineage-mirror": d4_mirror,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
