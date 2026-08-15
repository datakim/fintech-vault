#!/usr/bin/env python3
"""책 시리즈 2편 — 데이터가 썩는 경로. 그림 4종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


# ── 1. 두 종류의 드리프트
def d1_drift():
    r = R(411); b = []
    W, H = 860, 470
    b.append(T(430, 46, "구조가 바뀌는 것과 의미가 바뀌는 것", 28, INK, weight="bold"))
    b.append(ul(r, 205, 655, 63))

    b.append(box(r, 36, 84, 396, 44, "green", GREEN, sw=1.7))
    b.append(T(234, 114, "스키마 드리프트", 22, GREEN, weight="bold"))
    b.append(box(r, 448, 84, 376, 44, "red", RED, sw=1.7))
    b.append(T(636, 114, "시맨틱 드리프트", 22, RED, weight="bold"))

    rows = [
        ("무엇이 바뀌나", "컬럼 이름 · 타입 · 포맷", "그 안에 담긴 비즈니스 의미"),
        ("어떻게 잡나", "스키마 검증으로 자동 감지", "분포 모니터링 + 사람 사이 소통"),
        ("난이도", "쉽다", "기술만으로는 불가능하다"),
        ("실패하는 방식", "파이프라인이 에러를 뱉는다", "아무 소리 없이 통과한다"),
        ("LLM에서는", "즉시 터져서 알게 된다", "문법은 완벽한데 뜻이 틀린 답"),
    ]
    y = 142
    for label, l, rr in rows:
        b.append(T(430, y - 6, label, 15.5, INK_LIGHT))
        b.append(box(r, 36, y, 396, 44, None, GREEN, sw=1.2, amp=1.2))
        b.append(T(234, y + 29, l, 17, INK))
        b.append(box(r, 448, y, 376, 44, None, RED, sw=1.2, amp=1.2))
        b.append(T(636, y + 29, rr, 17, INK))
        y += 62

    b.append(T(430, 456, "앞의 것은 방어막에 걸리고, 뒤의 것은 방어막을 그냥 통과한다", 19, INK))
    return W, H, "".join(b)


# ── 2. price 컬럼 사례
def d2_price():
    r = R(422); b = []
    W, H = 840, 450
    b.append(T(420, 46, "검사는 전부 통과하는데 모델만 미쳐간다", 28, INK, weight="bold"))
    b.append(ul(r, 175, 665, 63))

    b.append(box(r, 60, 84, 300, 88, "gray", INK_LIGHT, sw=1.5))
    b.append(T(210, 112, "어제까지", 18, INK_LIGHT, weight="bold"))
    b.append(T(210, 140, "price: 15000.0", 19, INK))
    b.append(T(210, 162, "통화는 원", 15.5, INK_LIGHT))

    b.append(arr(r, 372, 128, 456, 128, RED, 1.8))
    b.append(T(414, 112, "재무팀이 달러로", 15, RED))

    b.append(box(r, 468, 84, 300, 88, "red", RED, sw=1.7))
    b.append(T(618, 112, "오늘부터", 18, RED, weight="bold"))
    b.append(T(618, 140, "price: 11.50", 19, INK))
    b.append(T(618, 162, "통화는 달러 — 공유 안 됨", 15.5, INK_LIGHT))

    checks = [
        (36, "green", GREEN, "타입 검사", "Float 맞음", "통과"),
        (306, "green", GREEN, "값 검사", "0보다 큼", "통과"),
        (576, "amber", AMBER, "분포 검사", "평균이 급락", "여기서만 걸린다"),
    ]
    for x, wash, col, name, what, verdict in checks:
        b.append(box(r, x, 202, 228, 96, wash, col, sw=1.6))
        b.append(T(x + 114, 230, name, 19, col, weight="bold"))
        b.append(T(x + 114, 258, what, 16, INK))
        b.append(T(x + 114, 284, verdict, 17, col, weight="bold"))

    b.append(box(r, 36, 316, 768, 76, "red", RED, sw=1.8))
    b.append(T(420, 344, "모델이 보는 세상: \"사람들이 갑자기 싼 것만 산다\"", 20, INK, weight="bold"))
    b.append(T(420, 372, "고가 상품 추천이 사라진다. 에러 로그에는 아무것도 안 남는다.", 17, INK))

    b.append(T(420, 428, "원화와 달러가 섞여 서서히 비율이 바뀌면, 분포 검사마저 임곗값을 못 넘는다", 18, INK_LIGHT))
    return W, H, "".join(b)


# ── 3. 컨텍스트 포이즈닝
def d3_poison():
    r = R(433); b = []
    W, H = 840, 460
    b.append(T(420, 46, "벡터 검색은 시간을 모른다", 28, INK, weight="bold"))
    b.append(ul(r, 262, 578, 63))

    b.append(box(r, 300, 84, 240, 50, "gray", INK, sw=1.6))
    b.append(T(420, 116, "\"A기업 전망 어때?\"", 19, INK, weight="bold"))

    b.append(arr(r, 370, 138, 240, 176, INK_LIGHT, 1.5))
    b.append(arr(r, 470, 138, 600, 176, INK_LIGHT, 1.5))

    b.append(box(r, 60, 182, 340, 104, "red", RED, sw=1.8))
    b.append(T(230, 210, "2024년 보고서", 19, RED, weight="bold"))
    b.append(T(230, 238, "목표가 50,000원 · 매수", 18, INK))
    b.append(T(230, 266, "유사도 0.93", 17, RED, weight="bold"))

    b.append(box(r, 440, 182, 340, 104, "green", GREEN, sw=1.8))
    b.append(T(610, 210, "2026년 보고서", 19, GREEN, weight="bold"))
    b.append(T(610, 238, "목표가 20,000원 · 매도", 18, INK))
    b.append(T(610, 266, "유사도 0.91", 17, GREEN, weight="bold"))

    b.append(T(420, 316, "둘 다 A기업 전망 문서라 의미적 거리가 비슷하다", 18, INK))
    b.append(T(420, 344, "그래서 오래된 쪽이 더 높은 점수를 받기도 한다", 18, INK))

    b.append(box(r, 36, 366, 768, 62, "amber", AMBER, sw=1.8))
    b.append(T(420, 394, "할루시네이션보다 잡기 어렵다 — 근거 문서가 실제로 존재하기 때문이다", 19, INK, weight="bold"))
    b.append(T(420, 418, "출처를 보여줘도 진짜 리서치 보고서다. 다만 2년 전 것일 뿐이다.", 16.5, INK_LIGHT))
    return W, H, "".join(b)


# ── 4. 피드백 루프
def d4_loop():
    r = R(444); b = []
    W, H = 840, 470
    b.append(T(420, 46, "출력이 데이터가 되면 오류가 정답으로 굳는다", 28, INK, weight="bold"))
    b.append(ul(r, 165, 675, 63))

    steps = [
        (330, 92, "amber", AMBER, "모델이 틀린 출력을 낸다", "광고 섞인 뉴스를 매수 기회로 읽음"),
        (560, 200, "red", RED, "사용자 행동이 바뀐다", "알림 받고 실제로 매수"),
        (330, 308, "red", RED, "그 행동이 데이터가 된다", "\"이 뉴스 뒤엔 매수가 따른다\""),
        (100, 200, "purple", PURPLE, "모델이 그걸 학습한다", "처음의 오해가 정답으로 굳음"),
    ]
    for x, y, wash, col, title, desc in steps:
        b.append(box(r, x - 90, y, 180, 76, wash, col, sw=1.7))
        b.append(T(x, y + 30, title, 16.5, col, weight="bold"))
        b.append(T(x, y + 56, desc, 13, INK))

    b.append(arr(r, 424, 130, 474, 200, INK_LIGHT, 1.6))
    b.append(arr(r, 522, 276, 424, 322, INK_LIGHT, 1.6))
    b.append(arr(r, 236, 322, 148, 276, INK_LIGHT, 1.6))
    b.append(arr(r, 194, 200, 244, 130, INK_LIGHT, 1.6))

    b.append(T(420, 212, "한 바퀴 돌 때마다", 17, INK_LIGHT))
    b.append(T(420, 236, "조금씩 증폭된다", 17, INK_LIGHT))

    b.append(box(r, 36, 400, 768, 52, "gray", INK, sw=1.6))
    b.append(T(420, 432, "전통 소프트웨어에서는 코드의 출력이 코드를 다시 쓰지 않는다. AI에서는 쓴다.", 19, INK, weight="bold"))
    return W, H, "".join(b)


DIAGRAMS = {
    "book2-drift": d1_drift,
    "book2-price": d2_price,
    "book2-poison": d3_poison,
    "book2-loop": d4_loop,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
