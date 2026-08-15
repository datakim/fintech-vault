#!/usr/bin/env python3
"""영문판: AI 엔지니어링 스킬맵 분석 — 그림 3종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


def d1_layers():
    r = R(311); b = []
    W, H = 900, 480
    b.append(T(450, 46, "What you miss reading it as a flat list", 28, INK, weight="bold"))
    b.append(ul(r, 235, 665, 63))

    b.append(T(228, 96, "the order as presented", 17, INK_LIGHT, weight="bold"))
    items = ["① Building and deploying AI apps", "② Software engineering fundamentals",
             "③ Using coding agents", "④ Shaping the build"]
    y = 116
    for it in items:
        b.append(box(r, 44, y, 368, 44, "gray", INK_LIGHT, sw=1.3, amp=1.2))
        b.append(T(228, y + 29, it, 17, INK))
        y += 54

    b.append(arr(r, 426, 220, 466, 220, INK_LIGHT, 1.6))
    b.append(T(446, 200, "restack", 14, INK_LIGHT))
    b.append(T(446, 254, "them", 14, INK_LIGHT))

    b.append(T(672, 96, "the actual dependency", 17, INK_LIGHT, weight="bold"))
    stack = [
        (116, "④ Shaping the build", "decide what gets made", "purple", PURPLE),
        (180, "① Building and deploying", "handle probabilistic parts", "amber", AMBER),
        (244, "③ Using coding agents", "raise the speed of making", "green", GREEN),
        (308, "② Software fundamentals", "the floor the other three stand on", "blue", BLUE),
    ]
    for y0, name, desc, wash, col in stack:
        b.append(box(r, 488, y0, 368, 56, wash, col, sw=1.7))
        b.append(T(672, y0 + 24, name, 17, col, weight="bold"))
        b.append(T(672, y0 + 44, desc, 14, INK_LIGHT))

    b.append(T(450, 410, "② is not an item alongside the rest — it is the condition under which the rest hold", 18, INK))
    b.append(T(450, 444, "Use an agent without fundamentals and you get output without knowing what you delegated", 16.5, INK_LIGHT))
    return W, H, "".join(b)


def d2_verify():
    r = R(322); b = []
    W, H = 900, 476
    b.append(T(450, 46, "The same thing sits inside all four items", 28, INK, weight="bold"))
    b.append(ul(r, 235, 665, 63))

    rows = [
        (88, "① Building AI apps", "an evaluation and error-analysis loop", "blue", BLUE),
        (168, "② Software fundamentals", "knowing what can go wrong, and where", "green", GREEN),
        (248, "③ Coding agents", "hand it a verifier so it closes its own loop", "amber", AMBER),
        (328, "④ Shaping the build", "defining what counts as done", "purple", PURPLE),
    ]
    for y, name, what, wash, col in rows:
        b.append(box(r, 36, y, 300, 64, wash, col, sw=1.6))
        b.append(T(186, y + 40, name, 18, col, weight="bold"))
        b.append(arr(r, 344, y + 32, 378, y + 32, INK_LIGHT, 1.4, 7))
        b.append(box(r, 386, y, 478, 64, None, col, sw=1.3, amp=1.2))
        b.append(T(625, y + 40, what, 17, INK))

    b.append(box(r, 36, 408, 828, 46, "amber", AMBER, sw=1.8))
    b.append(T(450, 438, "All four converge on \"how do I know what is right?\"", 21, INK, weight="bold"))
    return W, H, "".join(b)


def d3_missing():
    r = R(333); b = []
    W, H = 900, 450
    b.append(T(450, 46, "The faint areas on the map", 28, INK, weight="bold"))
    b.append(ul(r, 290, 610, 63))

    items = [
        (36, "red", RED, "After deployment",
         ["cost structure, observability,", "quiet quality decay.", "\"deploy\" appears as one word"]),
        (330, "amber", AMBER, "Domain knowledge",
         ["absent from all four.", "yet what gets built is", "usually decided by the domain"]),
        (624, "purple", PURPLE, "The method's lag",
         ["ten thousand job posts hold", "only what is already agreed.", "what is ahead is not posted"]),
    ]
    for x, wash, col, title, lines in items:
        b.append(box(r, x, 84, 240, 208, wash, col, sw=1.8))
        b.append(T(x + 120, 120, title, 20, col, weight="bold"))
        for i, ln in enumerate(lines):
            b.append(T(x + 120, 164 + i * 30, ln, 14, INK))

    b.append(T(450, 342, "Clustering finds the centre of the data, not its edges", 20, INK))
    b.append(T(450, 376, "Which makes this map a photograph of what is agreed right now", 17.5, INK_LIGHT))
    b.append(T(450, 420, "Not that things are missing — read it knowing where it is drawn faintly", 16.5, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {
    "skills-layers-en": d1_layers,
    "skills-verify-en": d2_verify,
    "skills-missing-en": d3_missing,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
