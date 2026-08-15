#!/usr/bin/env python3
"""Opik 소개 — 그림 3종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


# ── 1. 네 계열이 그대로 들어 있다
def d1_families():
    r = R(511); b = []
    W, H = 860, 500
    b.append(T(430, 46, "지난번에 정리한 네 계열이 그대로 들어 있다", 28, INK, weight="bold"))
    b.append(ul(r, 175, 685, 63))

    fams = [
        (88, "① 정답지와 비교", "blue", BLUE,
         "BLEU · ROUGE · BERTScore · METEOR · ChrF · Levenshtein · Equals · Contains"),
        (188, "② 모델이 채점", "amber", AMBER,
         "GEval · LLMJuriesJudge · Hallucination · AnswerRelevance · ContextPrecision"),
        (288, "③ 규칙으로 못 박기", "purple", PURPLE,
         "IsJson · RegexMatch · StructuredOutputCompliance"),
        (388, "④ 동작을 본다", "green", GREEN,
         "TrajectoryAccuracy · AgentToolCorrectness · Conversation* · Moderation · PromptInjection"),
    ]
    for y, name, wash, col, items in fams:
        b.append(box(r, 36, y, 788, 84, wash, col, sw=1.7))
        b.append(T(180, y + 38, name, 21, col, weight="bold"))
        b.append(box(r, 330, y + 16, 470, 52, None, col, sw=1.2, amp=1.2))
        b.append(T(565, y + 47, items, 13.5, INK))

    b.append(T(430, 488, "설치 직후 쓸 수 있는 내장 지표가 64개다 — 직접 구현할 일이 거의 없다", 19, INK_LIGHT))
    return W, H, "".join(b)


# ── 2. 실제로 돌려본 결과
def d2_result():
    r = R(522); b = []
    W, H = 840, 470
    b.append(T(420, 46, "돌려보니 정말로 0점이 나왔다", 28, INK, weight="bold"))
    b.append(ul(r, 240, 600, 63))

    # 헤더
    b.append(box(r, 300, 84, 168, 42, "gray", INK_LIGHT, sw=1.4))
    b.append(T(384, 112, "ROUGE", 18, INK, weight="bold"))
    b.append(box(r, 480, 84, 168, 42, "gray", INK_LIGHT, sw=1.4))
    b.append(T(564, 112, "BLEU", 18, INK, weight="bold"))
    b.append(box(r, 660, 84, 156, 42, "gray", INK_LIGHT, sw=1.4))
    b.append(T(738, 112, "Levenshtein", 17, INK, weight="bold"))

    rows = [
        (138, "표현까지 거의 같을 때", "0.000", "0.322", "0.897", GREEN),
        (216, "뜻은 같고 표현이 다를 때", "0.000", "0.000", "0.467", RED),
        (294, "아예 틀렸을 때", "0.000", "0.119", "0.571", AMBER),
    ]
    for y, label, a, bb, c, col in rows:
        b.append(box(r, 36, y, 250, 62, None, col, sw=1.4, amp=1.2))
        b.append(T(161, y + 38, label, 16.5, INK))
        for x, w, v in [(300, 168, a), (480, 168, bb), (660, 156, c)]:
            b.append(box(r, x, y, w, 62, None, col, sw=1.2, amp=1.2))
            b.append(T(x + w / 2, y + 39, v, 20, col, weight="bold"))

    b.append(box(r, 36, 376, 780, 76, "red", RED, sw=1.8))
    b.append(T(426, 406, "아예 틀린 답이 정답 패러프레이즈보다 높은 점수를 받는다", 20, INK, weight="bold"))
    b.append(T(426, 434, "BLEU 0.119 > 0.000, Levenshtein 0.571 > 0.467 — 우연이 아니라 구조다", 17, INK))
    return W, H, "".join(b)


# ── 3. 한국어 토크나이저 함정
def d3_tokenizer():
    r = R(533); b = []
    W, H = 840, 440
    b.append(T(420, 46, "ROUGE가 전부 0이었던 진짜 이유", 28, INK, weight="bold"))
    b.append(ul(r, 232, 608, 63))

    b.append(box(r, 36, 84, 372, 158, "green", GREEN, sw=1.8))
    b.append(T(222, 114, "영어를 넣으면", 20, GREEN, weight="bold"))
    b.append(T(222, 146, "\"Paris is the capital of France.\"", 15.5, INK))
    b.append(arr(r, 222, 158, 222, 178, INK_LIGHT, 1.4))
    b.append(T(222, 200, "['paris','is','the','capital',...]", 15, INK))
    b.append(T(222, 226, "ROUGE 1.0", 19, GREEN, weight="bold"))

    b.append(box(r, 432, 84, 372, 158, "red", RED, sw=1.8))
    b.append(T(618, 114, "한국어를 넣으면", 20, RED, weight="bold"))
    b.append(T(618, 146, "\"파리는 프랑스의 수도이다.\"", 16, INK))
    b.append(arr(r, 618, 158, 618, 178, INK_LIGHT, 1.4))
    b.append(T(618, 200, "[ ]  — 토큰이 하나도 안 남는다", 15, RED, weight="bold"))
    b.append(T(618, 226, "ROUGE 0.0", 19, RED, weight="bold"))

    b.append(box(r, 36, 262, 768, 60, "amber", AMBER, sw=1.8))
    b.append(T(420, 290, "기본 토크나이저가 영문자·숫자만 남기고 나머지를 버린다", 19, INK, weight="bold"))
    b.append(T(420, 312, "에러도 경고도 없이 그냥 0점이 찍힌다", 16.5, INK_LIGHT))

    b.append(T(420, 366, "tokenizer 인자에 직접 만든 것을 넣으면 해결된다", 19, INK))
    b.append(T(420, 400, "한국어로 평가할 거라면 이건 선택이 아니라 필수 점검 항목이다", 18, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {
    "opik-families": d1_families,
    "opik-result": d2_result,
    "opik-tokenizer": d3_tokenizer,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
