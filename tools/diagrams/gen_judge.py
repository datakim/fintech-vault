#!/usr/bin/env python3
"""금융 상담 AI 답변을 LLM이 채점할 때 정해 둘 것: 그림, 한/영.

일치도 숫자는 아래 JUDGES의 혼동행렬에서 계산한다. 본문 숫자와 같아야 하므로
바꾸려면 여기서 바꾸고 본문도 고친다.

  python3 gen_judge.py out_judge && ./fontenv/bin/python embed_fonts.py out_judge final_judge \
    && cp final_judge/*.svg ../../public/
  python3 gen_judge.py --metrics      # 숫자만 출력
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import R
from style_card import (T, shape, layer, icon, card, chips, arrow, title, wrap,
                        INK, SOFT, MUTED, ORANGE_DARK, EDGE, FILL)


# ── 합성 데이터: 사람이 채점한 상담 답변 1,000건 (2점 700, 1점 220, 0점 80)
# JUDGES[key][t] = 사람 점수가 t인 답변을 채점기가 0, 1, 2점으로 매긴 건수
JUDGES = {
    "always2": [[0, 0, 80], [0, 0, 220], [0, 0, 700]],
    "lenient": [[22, 34, 24], [0, 130, 90], [0, 4, 696]],
    "strict": [[68, 12, 0], [30, 145, 45], [7, 112, 581]],
}


def metrics(C):
    k = 3
    n = sum(sum(r) for r in C)
    agree = sum(C[i][i] for i in range(k)) / n
    row = [sum(C[i]) for i in range(k)]
    col = [sum(C[i][j] for i in range(k)) for j in range(k)]
    w = lambda i, j: (i - j) ** 2 / (k - 1) ** 2           # 제곱 가중
    obs = sum(w(i, j) * C[i][j] for i in range(k) for j in range(k))
    exp = sum(w(i, j) * row[i] * col[j] / n for i in range(k) for j in range(k))
    kappa = 1 - obs / exp
    rec0 = C[0][0] / row[0]
    prec0 = C[0][0] / col[0] if col[0] else float("nan")
    return {"agree": agree, "kappa": kappa, "rec0": rec0, "prec0": prec0, "flag0": col[0]}



TEXT = {
    "ko": {
        "agr_title": "사람 채점과 비교한 세 채점기",
        "metrics": {"agree": "일치율", "kappa": "가중 카파", "rec0": "0점 답변 재현율"},
        "judges": {"always2": "무조건 2점", "lenient": "후한 채점기", "strict": "깐깐한 채점기"},
        "count": "{n}/80건",
        "note1": "합성 데이터 1,000건 (사람 점수 2점 70% · 1점 22% · 0점 8%), 가중 카파는 제곱 가중",
        "note2": "깐깐한 채점기가 0점을 준 105건 가운데 37건은 사람이 1점 이상을 준 답변",
        "flow_title": "상담 한 건을 채점하는 흐름",
        "in": "입력", "score": "채점", "judge": "판정", "out": "출력", "ana": "분석 단계",
        "log": ("상담 대화 전체", ["답변과 순서 그대로"]),
        "snap": ("그 시점 스냅샷", ["보유 상품 · 투자성향", "그날 금리 · 약관 버전"]),
        "ctx": ("맥락 조립", ["상담 시점 기준으로 붙인다"]),
        "missing": "빠진 항목은 상태로 기록",
        "miss_chips": ["조회 실패", "미요청", "해당 없음"],
        "rule": ("코드 검사", ["숫자와 필수 문구"]),
        "rule_chips": ["금리 대조", "수수료 대조", "필수 고지"],
        "llm": ("LLM 채점", ["차원별 0/1/2 + 이유"]),
        "llm_chips": ["설명 충분성", "질문 응답", "위험 고지"],
        "gate": ("차단 조건", ["금리 오안내 · 원금보장 오인", "개인정보 노출"]),
        "gate_out": "다른 점수와 관계없이 실패",
        "store": ("결과 저장", ["입력 스냅샷 ID", "채점기 버전", "프롬프트 · 기준표 · 규칙 · 모델 ID"]),
        "outcome": ("민원 · 만족도", ["채점기에는 넣지 않고", "분석할 때만 붙인다"]),
    },
    "en": {
        "agr_title": "Three judges compared with human grades",
        "metrics": {"agree": "Exact agreement", "kappa": "Weighted kappa", "rec0": "Recall on score-0"},
        "judges": {"always2": "Always 2", "lenient": "Lenient judge", "strict": "Strict judge"},
        "count": "{n} of 80",
        "note1": "Synthetic set of 1,000 answers (human scores: 2 = 70%, 1 = 22%, 0 = 8%), quadratic weights",
        "note2": "Of the 105 answers the strict judge scored 0, people gave 37 a score of 1 or 2",
        "flow_title": "Scoring one conversation",
        "in": "Input", "score": "Scoring", "judge": "Verdict", "out": "Output", "ana": "Analysis",
        "log": ("Conversation", ["answers in order"]),
        "snap": ("As-of snapshot", ["products, risk profile", "that day's rates, terms"]),
        "ctx": ("Assemble context", ["as of the conversation date"]),
        "missing": "record missing items as status",
        "miss_chips": ["lookup failed", "not asked", "n/a"],
        "rule": ("Code checks", ["numbers and required text"]),
        "rule_chips": ["rates", "fees", "disclosures"],
        "llm": ("LLM judge", ["0/1/2 + reason per dimension"]),
        "llm_chips": ["explained", "answered", "risk"],
        "gate": ("Gate", ["wrong rate, implied guarantee", "personal data exposed"]),
        "gate_out": "fails regardless of other scores",
        "store": ("Store result", ["input snapshot ID", "judge version", "prompt, rubric, rules, model ID"]),
        "outcome": ("Complaints, CSAT", ["kept out of the judge,", "joined only at analysis"]),
    },
}


def d_flow(lang):
    t = TEXT[lang]; r = R(812); b = []
    W, H = 980, 640
    b.append(title(W / 2, 60, t["flow_title"]))
    # 입력
    b.append(layer(r, 24, 96, 266, 330, t["in"]))
    b.append(card(r, 44, 146, 226, 92, "white", t["log"][0], t["log"][1], "chat", tsize=20))
    b.append(card(r, 44, 260, 226, 140, "yellow", t["snap"][0], t["snap"][1], "clock", tsize=20))
    # 맥락 조립 (가운데 큰 카드)
    mx, my, mw, mh = 336, 170, 290, 190
    b.append(shape(r, mx - 6, my - 6, mw + 12, mh + 12, None, EDGE["peach"], 7, 20, None, 0.4))
    b.append(shape(r, mx, my, mw, mh, "white", INK, 2.0, 16))
    b.append(icon("clipboard", mx + mw / 2 - 16, my + 14, 32))
    b.append(T(mx + mw / 2, my + 74, t["ctx"][0], 25, INK, weight="bold"))
    b.append(T(mx + mw / 2, my + 100, t["ctx"][1][0], 16.5, SOFT))
    b.append(T(mx + mw / 2, my + 132, t["missing"], 15, MUTED))
    b.append(chips(r, mx + mw / 2, my + 142, list(zip(t["miss_chips"], ["red", "yellow", "gray"])), 14 if lang == "ko" else 13.5))
    b.append(arrow(r, 272, 192, mx - 8, 232, bend=-8))
    b.append(arrow(r, 272, 330, mx - 8, 300, bend=8))
    # 채점
    b.append(layer(r, 676, 96, 284, 330, t["score"]))
    b.append(card(r, 696, 144, 244, 122, "blue", t["rule"][0], t["rule"][1], "code", tsize=20))
    b.append(chips(r, 818, 222, list(zip(t["rule_chips"], ["white"] * 3)), 12.5 if lang == "ko" else 13, 6))
    b.append(card(r, 696, 284, 244, 122, "purple", t["llm"][0], t["llm"][1], "spark", tsize=20))
    b.append(chips(r, 818, 362, list(zip(t["llm_chips"], ["white"] * 3)), 12.5 if lang == "ko" else 13, 6))
    b.append(arrow(r, mx + mw + 8, 265, 672, 265))
    # 판정
    b.append(T(818, 462, t["judge"], 19, INK, weight="bold"))
    b.append(shape(r, 700 - 5, 476 - 5, 236 + 10, 132 + 10, None, EDGE["red"], 6, 18, None, 0.4))
    b.append(card(r, 700, 476, 236, 132, "red", t["gate"][0], t["gate"][1], "shield", tsize=20, ssize=15.5))
    b.append(T(818, 476 + 112, t["gate_out"], 15.5, ORANGE_DARK, weight="bold"))
    b.append(arrow(r, 818, 430, 818, 444))
    # 출력
    b.append(T(482, 462, t["out"], 19, INK, weight="bold"))
    b.append(shape(r, 360 - 5, 476 - 5, 244 + 10, 132 + 10, None, EDGE["green"], 6, 18, None, 0.4))
    b.append(card(r, 360, 476, 244, 132, "green", t["store"][0], t["store"][1], "db", tsize=20, ssize=15))
    b.append(arrow(r, 688, 542, 612, 542))
    # 분석 단계
    b.append(layer(r, 24, 450, 266, 168, t["ana"], 17))
    b.append(card(r, 44, 496, 226, 104, "gray", t["outcome"][0], t["outcome"][1], "megaphone", tsize=19, ssize=15))
    b.append(arrow(r, 276, 548, 348, 548, dash="3 5"))
    return W, H, "".join(b)


def d_agree(lang):
    t = TEXT[lang]; r = R(813); b = []
    W, H = 980, 580
    b.append(title(W / 2, 60, t["agr_title"]))
    order = ["always2", "lenient", "strict"]
    fills = {"always2": "gray", "lenient": "peach", "strict": "green"}
    m = {k: metrics(JUDGES[k]) for k in order}
    base, top = 392, 168
    for p, key in enumerate(["agree", "kappa", "rec0"]):
        lx = 27 + p * 315
        b.append(layer(r, lx, 96, 296, 336, t["metrics"][key]))
        b.append(f'<path d="M {lx + 22} {base} L {lx + 274} {base}" stroke="{INK}" stroke-width="1.8" '
                 f'stroke-linecap="round"/>')
        for i, k in enumerate(order):
            v = m[k][key]
            bx = lx + 36 + i * 80
            bh = max(v * (base - top), 0)
            if bh > 3:
                b.append(shape(r, bx, base - bh, 64, bh + 1, fills[k], INK, 1.9, 9, None, 0.5))
            else:
                b.append(f'<path d="M {bx} {base - 1} L {bx + 64} {base - 1}" stroke="{INK}" stroke-width="4" '
                         f'stroke-linecap="round"/>')
            lab = f"{v * 100:.0f}%" if key != "kappa" else f"{v:.2f}"
            ly = base - bh - (30 if key == "rec0" else 12)
            b.append(T(bx + 32, ly, lab, 21, INK, weight="bold"))
            if key == "rec0":
                n = JUDGES[k][0][0]
                b.append(T(bx + 32, ly + 18, t["count"].format(n=n), 14.5, SOFT))
    # 범례
    names = [t["judges"][k] for k in order]
    b.append(chips(r, W / 2, 452, list(zip(names, [fills[k] for k in order])), 16, 18))
    # 주석
    b.append(shape(r, 60, 498, W - 120, 64, None, MUTED, 1.2, 12, "5 5", 0.4))
    b.append(T(W / 2, 524, t["note1"], 15.5, SOFT))
    b.append(T(W / 2, 549, t["note2"], 15.5, SOFT))
    return W, H, "".join(b)


def build():
    out = {}
    for lang, suf in (("ko", ""), ("en", "-en")):
        out[f"judge-flow{suf}"] = d_flow(lang)
        out[f"judge-agreement{suf}"] = d_agree(lang)
    return out


if __name__ == "__main__":
    if sys.argv[1:] == ["--metrics"]:
        for k, C in JUDGES.items():
            m = metrics(C)
            print(k, {a: round(v, 3) for a, v in m.items()})
        sys.exit()
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    figs = build()
    for name, (w, h, body) in figs.items():
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(figs))
