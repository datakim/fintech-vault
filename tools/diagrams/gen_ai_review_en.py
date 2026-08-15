#!/usr/bin/env python3
"""영문판: AI에 평가받는 시대 — 그림 3종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


def d1_loop():
    r = R(11); b = []
    W, H = 900, 440
    b.append(T(450, 46, "The first reader of my report has changed", 28, INK, weight="bold"))
    b.append(ul(r, 230, 670, 63))

    b.append(box(r, 36, 80, 828, 130, "gray", INK_LIGHT, sw=1.6))
    b.append(T(60, 108, "before", 21, INK_LIGHT, anchor="start", weight="bold"))
    seq = [("the report I wrote", 190), ("my manager reads it", 200), ("feedback", 140)]
    x = 180
    for name, bw in seq:
        b.append(box(r, x, 122, bw, 52, None, INK, sw=1.3, amp=1.2))
        b.append(T(x + bw / 2, 154, name, 17, INK))
        if name != "feedback":
            b.append(arr(r, x + bw + 4, 148, x + bw + 24, 148, INK_LIGHT, 1.4, 7))
        x += bw + 28
    b.append(T(450, 196, "their experience and taste were the standard", 17, INK_LIGHT))

    b.append(box(r, 36, 228, 828, 158, "amber", AMBER, sw=1.8))
    b.append(T(60, 256, "now", 21, AMBER, anchor="start", weight="bold"))
    b.append(box(r, 120, 274, 170, 52, None, INK, sw=1.3, amp=1.2))
    b.append(T(205, 306, "the report I wrote", 17, INK))
    b.append(arr(r, 294, 300, 314, 300, INK_LIGHT, 1.4, 7))
    b.append(box(r, 318, 274, 210, 52, "red", RED, sw=1.6, amp=1.3))
    b.append(T(423, 297, "manager feeds it to an AI", 16, RED, weight="bold"))
    b.append(T(423, 317, "\"summarise it and critique it\"", 14, INK))
    b.append(arr(r, 532, 300, 552, 300, INK_LIGHT, 1.4, 7))
    b.append(box(r, 556, 274, 180, 52, None, INK, sw=1.3, amp=1.2))
    b.append(T(646, 297, "their own judgement", 15.5, INK))
    b.append(T(646, 317, "on top (or not)", 15.5, INK))
    b.append(arr(r, 740, 300, 758, 300, INK_LIGHT, 1.4, 7))
    b.append(box(r, 762, 274, 100, 52, None, INK, sw=1.3, amp=1.2))
    b.append(T(812, 306, "feedback", 16, INK))
    b.append(T(450, 366, "more and more often, a model reads what I write before a person does", 17.5, INK))

    b.append(T(450, 422, "CVs, code reviews, proposals — each passes through this route somewhere", 17.5, INK_LIGHT))
    return W, H, "".join(b)


def d2_cross():
    r = R(22); b = []
    W, H = 900, 456
    b.append(T(450, 46, "Run it myself before somebody else does", 28, INK, weight="bold"))
    b.append(ul(r, 245, 655, 63))

    b.append(box(r, 350, 82, 200, 54, "gray", INK, sw=1.7))
    b.append(T(450, 115, "the thing I made", 19, INK, weight="bold"))
    b.append(arr(r, 450, 138, 450, 166, INK_LIGHT, 1.5))

    b.append(box(r, 270, 172, 360, 60, "blue", BLUE, sw=1.7))
    b.append(T(450, 196, "have model A attack it", 19, BLUE, weight="bold"))
    b.append(T(450, 220, "\"try to take this argument apart\"", 16, INK))
    b.append(arr(r, 450, 234, 450, 262, INK_LIGHT, 1.5))

    b.append(box(r, 230, 268, 440, 60, "green", GREEN, sw=1.7))
    b.append(T(450, 292, "feed that critique to model B", 19, GREEN, weight="bold"))
    b.append(T(450, 316, "\"is this fair? anything overstated?\"", 16, INK))
    b.append(arr(r, 450, 330, 450, 358, INK_LIGHT, 1.5))

    b.append(box(r, 300, 364, 300, 54, "amber", AMBER, sw=1.7))
    b.append(T(450, 397, "fix only what survives", 19, AMBER, weight="bold"))

    b.append(T(112, 198, "a model from another", 15.5, INK_LIGHT))
    b.append(T(112, 220, "family catches", 15.5, INK_LIGHT))
    b.append(T(112, 242, "different things", 15.5, INK_LIGHT))
    b.append(T(782, 288, "trust just one and", 15.5, INK_LIGHT))
    b.append(T(782, 310, "its habits come", 15.5, INK_LIGHT))
    b.append(T(782, 332, "along with it", 15.5, INK_LIGHT))

    b.append(T(450, 442, "A criticism both models raise is usually a real one", 18, INK_LIGHT))
    return W, H, "".join(b)


def d3_ways():
    r = R(33); b = []
    W, H = 900, 406
    b.append(T(450, 46, "Ask \"what do you think?\" and you get compliments", 27, INK, weight="bold"))
    b.append(ul(r, 205, 695, 63))

    ways = [
        (36, "red", RED, "Make it summarise",
         ["\"summarise in three lines\"", "if it comes out wrong,", "the writing is wrong"]),
        (248, "blue", BLUE, "Make it argue back",
         ["\"take this argument apart\"", "the aim is counter-examples,", "not praise"]),
        (460, "green", GREEN, "Ask what is missing",
         ["\"what should be here", "but is not?\"", "blanks are invisible"]),
        (672, "amber", AMBER, "Grade against criteria",
         ["a checklist instead of", "a vague ask", "results come out consistent"]),
    ]
    for x, wash, col, title, lines in ways:
        b.append(box(r, x, 82, 192, 216, wash, col, sw=1.7))
        b.append(T(x + 96, 116, title, 18, col, weight="bold"))
        for i, ln in enumerate(lines):
            b.append(T(x + 96, 158 + i * 30, ln, 14.5, INK))

    b.append(T(450, 348, "What you ask for decides what comes back", 20, INK))
    b.append(T(450, 382, "Which means, in the end, you can only ask as much as you already know", 17.5, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {
    "review-loop-en": d1_loop,
    "review-cross-en": d2_cross,
    "review-ways-en": d3_ways,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
