#!/usr/bin/env python3
"""Strands Decider 티켓 분류 글 그림, 한/영.

비용 숫자는 아래 COSTS에서 계산한다. 본문 숫자와 같아야 하므로 바꾸려면 여기서 바꾸고 본문도 고친다.

  python3 gen_strands.py out_strands && ./fontenv/bin/python embed_fonts.py out_strands final_strands \
    && cp final_strands/*.svg ../../public/
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import R, T, box, arr, ul, wrap, wobble_line, INK, INK_LIGHT, BLUE, TEAL, RED, AMBER


# ── 티켓 한 건당 토큰 (Strands 블로그 보고값) 과 100만 토큰당 가격 (2026-11 공개 가격표)
IN_TOK, OUT_TOK = 6554, 170          # Sonnet 4.6 티켓당 입력·출력 토큰
STATIC = 5000                        # 가정: 입력 중 매번 같은 시스템 프롬프트와 라벨 설명
NEW_TOKENIZER = 1.3                  # 4.7 이후 모델의 새 토크나이저는 같은 글을 약 30% 더 센다


def per_million(inp, out, p_in, p_out, cached=0, p_cache=0.0):
    """티켓 100만 건당 달러."""
    return (cached * p_cache + (inp - cached) * p_in + out * p_out)


COSTS = [
    # (key, 보고/추정, 계열, 100만 건당 달러)
    ("s46", "rep", "llm", per_million(IN_TOK, OUT_TOK, 3.0, 15.0)),
    ("s46c", "est", "llm", per_million(IN_TOK, OUT_TOK, 3.0, 15.0, STATIC, 0.30)),
    ("h55", "est", "llm", per_million(IN_TOK * NEW_TOKENIZER, OUT_TOK * NEW_TOKENIZER, 0.10, 0.50)),
    ("h55c", "est", "llm", per_million(IN_TOK * NEW_TOKENIZER, OUT_TOK * NEW_TOKENIZER, 0.10, 0.50,
                                       STATIC * NEW_TOKENIZER, 0.01)),
    ("dec", "rep", "dec", 500.0),
    ("decfull", "rep", "dec", 250.0),            # 보고값 (1.408달러 ÷ 시간당 약 5,600건)
]


def line(r, x1, y1, x2, y2, color=INK, sw=1.4, op=1.0):
    return (f'<path d="{wobble_line(r, x1, y1, x2, y2, 1.0)}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" opacity="{op}"/>')


TEXT = {
    "ko": {
        "cost_title": "티켓 100만 건당 모델 비용 (로그 눈금)",
        "rows": {
            "s46": "Sonnet 4.6, 캐시 없음",
            "s46c": "Sonnet 4.6, 고정 프롬프트 캐시",
            "h55": "Haiku 5.5, 캐시 없음",
            "h55c": "Haiku 5.5, 고정 프롬프트 캐시",
            "dec": "Strands Decider E4B, 여유 포함",
            "decfull": "Strands Decider E4B, 최대 가동",
        },
        "rep": "보고값", "est": "공개 가격표로 계산한 추정",
        "note": "추정: 입력 6,554토큰 중 5,000토큰이 고정, 새 토크나이저는 토큰 30% 증가, thinking 끔",
        "dual_title": "DUAL 모드에서 라벨이 쌓이는 곳",
        "ticket": "티켓",
        "sonnet": ["Sonnet 4.6", "결과를 티켓에 적용"],
        "decider": ["Strands Decider", "결과는 기록만"],
        "cmp": "두 답 비교",
        "dis": ["답이 다르면", "사람이 전부 판정"],
        "agr": ["답이 같으면", "무작위 표본만 검수"],
        "dis_out": "어느 쪽이 맞았는지",
        "agr_out": "둘 다 틀린 비율",
        "switch": "AppConfig 스위치: BEDROCK · DUAL · DECIDER (되돌리는 데 45초)",
        "gap": "공개된 사례에는 없는 단계",
    },
    "en": {
        "cost_title": "Model cost per million tickets (log scale)",
        "rows": {
            "s46": "Sonnet 4.6, no caching",
            "s46c": "Sonnet 4.6, fixed prompt cached",
            "h55": "Haiku 5.5, no caching",
            "h55c": "Haiku 5.5, fixed prompt cached",
            "dec": "Strands Decider E4B, with headroom",
            "decfull": "Strands Decider E4B, fully busy",
        },
        "rep": "reported", "est": "estimated from list prices",
        "note": "Estimates assume 5,000 of 6,554 input tokens are fixed, 30% more tokens on the new tokenizer, thinking off",
        "dual_title": "Where labels come from in DUAL mode",
        "ticket": "Ticket",
        "sonnet": ["Sonnet 4.6", "label applied"],
        "decider": ["Strands Decider", "label logged only"],
        "cmp": "Compare",
        "dis": ["Different answers:", "a person judges all"],
        "agr": ["Same answer:", "audit a random sample"],
        "dis_out": "which one was right",
        "agr_out": "how often both are wrong",
        "switch": "AppConfig switch: BEDROCK, DUAL, DECIDER (45 seconds to roll back)",
        "gap": "not in the published write-up",
    },
}


def fmt(v, lang):
    return f"${v:,.0f}"


def d_cost(lang):
    t = TEXT[lang]; r = R(601); b = []
    W, H = 840, 520
    x0, w = 330 if lang == "ko" else 350, 400
    lo, hi = math.log10(100), math.log10(50_000)
    X = lambda v: x0 + (math.log10(v) - lo) / (hi - lo) * w
    b.append(T(W / 2, 44, t["cost_title"], 24, INK, weight="bold"))
    b.append(ul(r, 200, 640, 58))
    top, row = 100, 50
    base_y = top + row * len(COSTS) + 6
    for v in (100, 1_000, 10_000):
        b.append(line(r, X(v), top - 6, X(v), base_y, INK_LIGHT, 1.0, 0.45))
        b.append(T(X(v), base_y + 22, fmt(v, lang), 14, INK_LIGHT))
    for i, (key, kind, fam, v) in enumerate(COSTS):
        y = top + i * row
        col = BLUE if fam == "llm" else TEAL
        wash = ("blue" if fam == "llm" else "teal") if kind == "rep" else None
        b.append(T(x0 - 14, y + 24, t["rows"][key], 15.5, INK, anchor="end"))
        bw = max(X(v) - x0, 6)
        b.append(box(r, x0, y + 8, bw, 26, wash, col, sw=1.5 if kind == "rep" else 1.1, amp=0.7))
        b.append(T(x0 + bw + 10, y + 26, f"{fmt(v, lang)}", 15, col, anchor="start",
                   weight="bold" if kind == "rep" else "normal"))
    b.append(line(r, x0, top - 6, x0, base_y, INK, 1.4))
    ly = base_y + 56
    b.append(box(r, 120, ly - 13, 24, 15, "blue", BLUE, sw=1.3, amp=0.5))
    b.append(T(152, ly, t["rep"], 14.5, INK, anchor="start"))
    b.append(box(r, 290, ly - 13, 24, 15, None, BLUE, sw=1.0, amp=0.5))
    b.append(T(322, ly, t["est"], 14.5, INK, anchor="start"))
    b.append(T(W / 2, ly + 34, t["note"], 12.5, INK_LIGHT))
    return W, H, "".join(b)


def d_dual(lang):
    t = TEXT[lang]; r = R(602); b = []
    W, H = 840, 500
    b.append(T(W / 2, 44, t["dual_title"], 25, INK, weight="bold"))
    b.append(ul(r, 250, 590, 58))
    b.append(box(r, 40, 175, 110, 64, "gray", INK, sw=1.4))
    b.append(T(95, 213, t["ticket"], 18, INK, weight="bold"))
    for (y, wash, col, (l1, l2)) in ((95, "blue", BLUE, t["sonnet"]), (255, "teal", TEAL, t["decider"])):
        b.append(box(r, 210, y, 190, 72, wash, col, sw=1.4))
        b.append(T(305, y + 30, l1, 17, col, weight="bold"))
        b.append(T(305, y + 54, l2, 14, INK))
    b.append(arr(r, 152, 198, 204, 140, INK_LIGHT, 1.4, 7))
    b.append(arr(r, 152, 216, 204, 280, INK_LIGHT, 1.4, 7))
    b.append(box(r, 450, 175, 110, 64, None, INK, sw=1.3, amp=1.2))
    b.append(T(505, 213, t["cmp"], 16, INK, weight="bold"))
    b.append(arr(r, 402, 132, 446, 190, INK_LIGHT, 1.3, 7))
    b.append(arr(r, 402, 290, 446, 226, INK_LIGHT, 1.3, 7))
    for (y, wash, col, (l1, l2), out) in ((100, "amber", AMBER, t["dis"], t["dis_out"]),
                                         (262, "red", RED, t["agr"], t["agr_out"])):
        b.append(box(r, 610, y, 200, 70, wash, col, sw=1.4))
        b.append(T(710, y + 30, l1, 15.5, col, weight="bold"))
        b.append(T(710, y + 52, l2, 14.5, INK))
        b.append(T(710, y + 92, "→ " + out, 14, INK_LIGHT))
    b.append(arr(r, 562, 196, 604, 140, INK_LIGHT, 1.3, 7))
    b.append(arr(r, 562, 220, 604, 290, INK_LIGHT, 1.3, 7))
    b.append(T(710, 384, "(" + t["gap"] + ")", 13.5, RED))
    b.append(T(W / 2, 452, t["switch"], 15, INK_LIGHT))
    return W, H, "".join(b)


def build():
    out = {}
    for lang, suf in (("ko", ""), ("en", "-en")):
        out[f"strands-cost{suf}"] = d_cost(lang)
        out[f"strands-dual{suf}"] = d_dual(lang)
    return out


if __name__ == "__main__":
    if sys.argv[1:] == ["--costs"]:
        for key, kind, fam, v in COSTS:
            print(f"{key:8s} {kind} {v:10.1f}")
        sys.exit()
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    figs = build()
    for name, (w, h, body) in figs.items():
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(figs))
