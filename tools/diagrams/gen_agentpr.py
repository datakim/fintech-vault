#!/usr/bin/env python3
"""에이전트가 한 달에 PR 11,000개를 올려도 코드베이스가 무너지지 않으려면: 그림, 한/영 (카드형).

  python3 gen_agentpr.py out_agentpr && ./fontenv/bin/python embed_fonts.py out_agentpr final_agentpr \
    && cp final_agentpr/*.svg ../../public/
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import R
from style_card import (T, shape, layer, icon, card, chips, arrow, title, wrap,
                        INK, SOFT, MUTED, ORANGE, ORANGE_DARK, EDGE, FILL)

TEXT = {
    "ko": {
        "p_title": "에이전트를 믿을 수 있게 만드는 네 층",
        "layers": [
            ("1. 코드 자체", "API 설계, 아키텍처, 리팩토링", ["useEffect 금지", "main, renderer 폴더 분리"], "blue", "code"),
            ("2. 결정론적 검사", "린트 규칙, 타입, 컴파일러, 테스트", ["import 경계", "타이머 땜질 금지"], "green", "shield"),
            ("3. 검증", "런타임 검증, 형식 검증", ["실행 영상", "TLA+", "Lean", "Bombadil"], "yellow", "check"),
            ("4. 판단이 필요한 글", "rules, skills, AGENTS.md", ["최소한만"], "peach", "chat"),
        ],
        "p_note": "위층일수록 시간을 많이 쓴다. 1, 2층은 같은 코드면 늘 같은 결과를 내는 결정론적 장치다.",
        "f_title": "PR 하나가 지나가는 길",
        "steps": [
            ("PR 도착", ["에이전트가", "PR을 올린다"], "gray", "code"),
            ("자동 검사", ["린트, 타입,", "테스트"], "green", "shield"),
            ("실행 검증", ["앱을 직접 띄워", "영상, 스크린샷"], "yellow", "spark"),
            ("사람 확인", ["코드보다", "증거물을 본다"], "peach", "user"),
            ("머지", ["볼 게 없으면", "자동 머지"], "blue", "check"),
        ],
        "reject": "실패하면 자동으로 반려",
        "loop": "사람이 잡은 문제는 다음부터 자동 검사에서 걸리게 바꾼다",
        "f_note": "자동 검사에서 걸린 PR은 사람에게 가지 않는다. 사람이 볼 몫은 시간이 갈수록 줄어든다.",
    },
    "en": {
        "p_title": "Four layers that let you trust agents",
        "layers": [
            ("1. The code itself", "API design, architecture, refactoring", ["ban useEffect", "split main and renderer"], "blue", "code"),
            ("2. Deterministic checks", "lint rules, types, compiler, tests", ["import boundaries", "no timer patches"], "green", "shield"),
            ("3. Verification", "runtime and formal verification", ["run videos", "TLA+", "Lean", "Bombadil"], "yellow", "check"),
            ("4. Prose that needs judgement", "rules, skills, AGENTS.md", ["keep it minimal"], "peach", "chat"),
        ],
        "p_note": "Spend the most time on the widest layers. Layers 1 and 2 are deterministic: the same code always gives the same result.",
        "f_title": "The path one pull request takes",
        "steps": [
            ("PR arrives", ["an agent opens", "a pull request"], "gray", "code"),
            ("Checks", ["lint, types,", "tests"], "green", "shield"),
            ("Run it", ["the agent runs", "the app, records"], "yellow", "spark"),
            ("Human review", ["reads evidence,", "not every line"], "peach", "user"),
            ("Merge", ["nothing left", "to review"], "blue", "check"),
        ],
        "reject": "fails: rejected automatically",
        "loop": "anything a person catches becomes an automatic check next time",
        "f_note": "A PR that fails the checks never reaches a person. What people review shrinks over time.",
    },
}


def d_pyramid(lang):
    t = TEXT[lang]; r = R(1101); b = []
    W, H = 980, 680
    b.append(title(W / 2, 58, t["p_title"], 30))
    widths = [880, 740, 600, 470]
    y = 100
    for (name, sub, chs, fill, ic), w in zip(t["layers"], widths):
        x = (W - w) / 2
        b.append(card(r, x, y, w, 112, fill, name, [sub], ic=ic, tsize=20, ssize=15.5))
        b.append(chips(r, W / 2, y + 76, [(c, "white") for c in chs], 13.5))
        y += 130
    b.append(T(W / 2, 640, t["p_note"], 14.5, SOFT))
    return W, H, "".join(b)


def d_flow(lang):
    t = TEXT[lang]; r = R(1102); b = []
    W, H = 980, 500
    b.append(title(W / 2, 54, t["f_title"], 30))
    cw, gap, y, ch = 162, 30, 190, 150
    x0 = (W - (5 * cw + 4 * gap)) / 2
    xs = [x0 + i * (cw + gap) for i in range(5)]
    for (name, subs, fill, ic), x in zip(t["steps"], xs):
        if fill == "green":
            b.append(shape(r, x - 5, y - 5, cw + 10, ch + 10, None, EDGE["green"], 6, 16, None, 0.4))
        b.append(card(r, x, y, cw, ch, fill, name, subs, ic=ic, tsize=19, ssize=15, icon_top=True))
    for i in range(4):
        b.append(arrow(r, xs[i] + cw + 5, y + ch / 2, xs[i + 1] - 5, y + ch / 2))
    # 반려
    cx = xs[1] + cw / 2
    b.append(arrow(r, cx, y + ch + 6, cx, y + ch + 40))
    b.append(chips(r, cx, y + ch + 46, [(t["reject"], "red")], 14))
    # 되먹임
    hx, ax = xs[3] + cw / 2, xs[1] + cw / 2
    b.append(arrow(r, hx, y - 10, ax, y - 14, bend=92, dash="7 6", color=ORANGE_DARK, sw=2.0))
    b.append(T(W / 2 + 6, 124, t["loop"], 16, ORANGE_DARK, weight="bold"))
    b.append(T(W / 2, 470, t["f_note"], 14.5, SOFT))
    return W, H, "".join(b)


def build():
    out = {}
    for lang, suf in (("ko", ""), ("en", "-en")):
        out[f"agentpr-pyramid{suf}"] = d_pyramid(lang)
        out[f"agentpr-flow{suf}"] = d_flow(lang)
    return out


if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    figs = build()
    for name, (w, h, body) in figs.items():
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(figs))
