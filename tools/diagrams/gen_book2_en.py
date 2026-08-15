#!/usr/bin/env python3
"""영문판: 데이터가 썩는 경로 (책 시리즈 2편) — 그림 4종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


def d1_drift():
    r = R(411); b = []
    W, H = 880, 496
    b.append(T(440, 46, "When the shape changes vs when the meaning changes", 27, INK, weight="bold"))
    b.append(ul(r, 195, 685, 63))

    b.append(box(r, 36, 84, 400, 44, "green", GREEN, sw=1.7))
    b.append(T(236, 114, "Schema drift", 22, GREEN, weight="bold"))
    b.append(box(r, 452, 84, 392, 44, "red", RED, sw=1.7))
    b.append(T(648, 114, "Semantic drift", 22, RED, weight="bold"))

    rows = [
        ("What changes", "Column name · type · format", "The business meaning inside"),
        ("How you catch it", "Schema validation, automatically", "Distribution monitoring + people talking"),
        ("Difficulty", "Easy", "Not solvable by technology alone"),
        ("How it fails", "The pipeline throws an error", "It passes without a sound"),
        ("In an LLM", "It breaks loudly, so you know", "Perfect syntax, wrong meaning"),
    ]
    y = 152
    for label, l, rr in rows:
        b.append(T(440, y - 9, label, 15, INK_LIGHT))
        b.append(box(r, 36, y, 400, 40, None, GREEN, sw=1.2, amp=1.2))
        b.append(T(236, y + 27, l, 16.5, INK))
        b.append(box(r, 452, y, 392, 40, None, RED, sw=1.2, amp=1.2))
        b.append(T(648, y + 27, rr, 15.5, INK))
        y += 64

    b.append(T(440, 480, "The first one trips the defences. The second walks straight through.", 19, INK))
    return W, H, "".join(b)


def d2_price():
    r = R(422); b = []
    W, H = 880, 450
    b.append(T(440, 46, "Every check passes, and only the model goes mad", 27, INK, weight="bold"))
    b.append(ul(r, 185, 695, 63))

    b.append(box(r, 70, 84, 300, 88, "gray", INK_LIGHT, sw=1.5))
    b.append(T(220, 112, "Until yesterday", 18, INK_LIGHT, weight="bold"))
    b.append(T(220, 140, "price: 15000.0", 19, INK))
    b.append(T(220, 162, "currency is won", 15.5, INK_LIGHT))

    b.append(arr(r, 382, 128, 466, 128, RED, 1.8))
    b.append(T(424, 110, "finance switches", 14, RED))
    b.append(T(424, 152, "to dollars", 14, RED))

    b.append(box(r, 478, 84, 320, 88, "red", RED, sw=1.7))
    b.append(T(638, 112, "From today", 18, RED, weight="bold"))
    b.append(T(638, 140, "price: 11.50", 19, INK))
    b.append(T(638, 162, "currency is USD — nobody told us", 14.5, INK_LIGHT))

    checks = [
        (36, "green", GREEN, "Type check", "Float, correct", "pass"),
        (326, "green", GREEN, "Value check", "greater than zero", "pass"),
        (616, "amber", AMBER, "Distribution check", "the mean collapses", "the only one that fires"),
    ]
    for x, wash, col, name, what, verdict in checks:
        b.append(box(r, x, 202, 228, 96, wash, col, sw=1.6))
        b.append(T(x + 114, 230, name, 18, col, weight="bold"))
        b.append(T(x + 114, 258, what, 15.5, INK))
        b.append(T(x + 114, 284, verdict, 15.5, col, weight="bold"))

    b.append(box(r, 36, 316, 808, 76, "red", RED, sw=1.8))
    b.append(T(440, 344, "What the model sees: \"people suddenly buy only cheap things\"", 20, INK, weight="bold"))
    b.append(T(440, 372, "High-value recommendations disappear. Nothing lands in the error log.", 16.5, INK))

    b.append(T(440, 428, "Mix the two currencies and shift the ratio slowly — even the distribution check stays under threshold", 15.5, INK_LIGHT))
    return W, H, "".join(b)


def d3_poison():
    r = R(433); b = []
    W, H = 880, 460
    b.append(T(440, 46, "Vector search has no sense of time", 28, INK, weight="bold"))
    b.append(ul(r, 245, 635, 63))

    b.append(box(r, 300, 84, 280, 50, "gray", INK, sw=1.6))
    b.append(T(440, 116, "\"How does Company A look?\"", 18, INK, weight="bold"))

    b.append(arr(r, 390, 138, 260, 176, INK_LIGHT, 1.5))
    b.append(arr(r, 490, 138, 620, 176, INK_LIGHT, 1.5))

    b.append(box(r, 70, 182, 350, 104, "red", RED, sw=1.8))
    b.append(T(245, 210, "2024 report", 19, RED, weight="bold"))
    b.append(T(245, 238, "target 50,000 · Buy", 18, INK))
    b.append(T(245, 266, "similarity 0.93", 17, RED, weight="bold"))

    b.append(box(r, 460, 182, 350, 104, "green", GREEN, sw=1.8))
    b.append(T(635, 210, "2026 report", 19, GREEN, weight="bold"))
    b.append(T(635, 238, "target 20,000 · Sell", 18, INK))
    b.append(T(635, 266, "similarity 0.91", 17, GREEN, weight="bold"))

    b.append(T(440, 316, "Both are outlook documents about Company A, so the semantic distance is similar", 17.5, INK))
    b.append(T(440, 344, "Which is how the older one sometimes scores higher", 17.5, INK))

    b.append(box(r, 36, 366, 808, 62, "amber", AMBER, sw=1.8))
    b.append(T(440, 394, "Harder to catch than a hallucination — the cited document really exists", 19, INK, weight="bold"))
    b.append(T(440, 418, "Show the source and it is a genuine research report. Just a two-year-old one.", 16, INK_LIGHT))
    return W, H, "".join(b)


def d4_loop():
    r = R(444); b = []
    W, H = 880, 470
    b.append(T(440, 46, "When output becomes data, an error hardens into truth", 26, INK, weight="bold"))
    b.append(ul(r, 175, 705, 63))

    steps = [
        (340, 92, "amber", AMBER, "The model gets it wrong", "ad copy read as a buy signal"),
        (590, 200, "red", RED, "User behaviour shifts", "they see the alert and buy"),
        (340, 308, "red", RED, "That behaviour becomes data", "\"buying follows this news\""),
        (120, 200, "purple", PURPLE, "The model learns it", "the first mistake becomes truth"),
    ]
    for x, y, wash, col, title, desc in steps:
        b.append(box(r, x - 100, y, 200, 76, wash, col, sw=1.7))
        b.append(T(x, y + 30, title, 15.5, col, weight="bold"))
        b.append(T(x, y + 56, desc, 12.5, INK))

    b.append(arr(r, 445, 140, 492, 200, INK_LIGHT, 1.6))
    b.append(arr(r, 540, 280, 445, 320, INK_LIGHT, 1.6))
    b.append(arr(r, 235, 322, 158, 280, INK_LIGHT, 1.6))
    b.append(arr(r, 150, 196, 243, 145, INK_LIGHT, 1.6))

    b.append(T(357, 218, "each turn round", 17, INK_LIGHT))
    b.append(T(357, 244, "amplifies it a little", 17, INK_LIGHT))

    b.append(box(r, 36, 400, 808, 52, "gray", INK, sw=1.6))
    b.append(T(440, 432, "In ordinary software the output of code does not rewrite the code. In AI it does.", 19, INK, weight="bold"))
    return W, H, "".join(b)


DIAGRAMS = {
    "book2-drift-en": d1_drift,
    "book2-price-en": d2_price,
    "book2-poison-en": d3_poison,
    "book2-loop-en": d4_loop,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
