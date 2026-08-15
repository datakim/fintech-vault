#!/usr/bin/env python3
"""영문판: 모델은 무죄다 (책 시리즈 1편) — 그림 4종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


def d1_sw12():
    r = R(101); b = []
    W, H = 880, 472
    b.append(T(440, 46, "Rules live in the code  vs  nobody knows where the rules live", 26, INK, weight="bold"))
    b.append(ul(r, 130, 750, 63))

    b.append(box(r, 40, 74, 396, 44, "blue", BLUE))
    b.append(T(238, 104, "Traditional software", 21, BLUE, weight="bold"))
    b.append(box(r, 456, 74, 388, 44, "amber", AMBER))
    b.append(T(650, 104, "AI system", 21, AMBER, weight="bold"))

    rows = [
        ("Where the logic lives", "In the source code", "Model weights + prompt + data"),
        ("Predicting behaviour", "Read the code and you know", "Run it and find out, probably"),
        ("Debugging", "Follow the stack trace", "Dig through prompt, retrieval, output"),
        ("Blast radius of a change", "The code you changed", "The whole system, unpredictably"),
    ]
    y = 132
    for label, l, rr in rows:
        b.append(T(440, y + 22, label, 15.5, INK_LIGHT))
        b.append(box(r, 40, y + 30, 396, 40, None, BLUE, sw=1.3, amp=1.3))
        b.append(T(238, y + 56, l, 18, INK))
        b.append(box(r, 456, y + 30, 388, 40, None, AMBER, sw=1.3, amp=1.3))
        b.append(T(650, y + 56, rr, 17, INK))
        y += 72

    b.append(T(440, 452, "Everything about why familiar debugging instincts stop working is in this table", 18, INK_LIGHT))
    return W, H, "".join(b)


def d2_cace():
    r = R(202); b = []
    W, H = 880, 450
    b.append(T(440, 46, "One line changed, the whole system moves", 28, INK, weight="bold"))
    b.append(ul(r, 190, 690, 63))

    steps = ["clean query", "embed", "retrieve", "rerank", "build context", "generate"]
    x = 40
    bw = 122
    for i, s in enumerate(steps):
        hot = (s == "retrieve")
        b.append(box(r, x, 80, bw, 46, "red" if hot else None, RED if hot else INK,
                     sw=1.7 if hot else 1.2, amp=1.3))
        b.append(T(x + bw / 2, 109, s, 15, RED if hot else INK, weight="bold" if hot else "normal"))
        if i < len(steps) - 1:
            b.append(arr(r, x + bw + 2, 103, x + bw + 10, 103, INK_LIGHT, 1.4, 6))
        x += bw + 12

    b.append(T(390, 158, "top_k went from 5 to 3. That is the entire change.", 19, RED, weight="bold"))
    b.append(arr(r, 390, 168, 390, 196, RED, 1.6))

    outs = [
        (46, "green", GREEN, "Some questions improved", ["Noise dropped out,", "answers got cleaner"]),
        (320, "amber", AMBER, "Some can no longer be answered", ["The document needed", "fell out of the top three"]),
        (594, "red", RED, "Some hallucinate more", ["Thin context, so the model", "fills the gap itself"]),
    ]
    for x0, wash, col, title, lines in outs:
        b.append(box(r, x0, 206, 250, 120, wash, col, sw=1.7))
        b.append(T(x0 + 125, 238, title, 17, col, weight="bold"))
        b.append(T(x0 + 125, 272, lines[0], 15.5, INK))
        b.append(T(x0 + 125, 296, lines[1], 15.5, INK))

    b.append(T(440, 366, "One number, and the result splits three ways depending on the question", 19, INK))
    b.append(T(440, 398, "\"Why did the part I never touched break?\" usually starts here", 17.5, INK_LIGHT))
    b.append(T(440, 428, "Google researchers called it CACE — changing anything changes everything", 16.5, INK_LIGHT))
    return W, H, "".join(b)


def d3_where():
    r = R(303); b = []
    W, H = 880, 420
    b.append(T(440, 46, "Where failures actually start", 28, INK, weight="bold"))
    b.append(ul(r, 250, 630, 63))

    b.append(box(r, 40, 78, 336, 250, "red", RED, sw=1.8))
    b.append(T(208, 106, "Before the model", 21, RED, weight="bold"))
    b.append(box(r, 394, 78, 190, 250, "gray", INK, sw=1.8))
    b.append(T(489, 106, "The model", 21, INK, weight="bold"))
    b.append(box(r, 602, 78, 242, 250, "amber", AMBER, sw=1.8))
    b.append(T(723, 106, "Around and after", 21, AMBER, weight="bold"))

    items_l = [("#1", "Input data quality"), ("#2", "Training-serving skew")]
    y = 126
    for rank, name in items_l:
        b.append(box(r, 64, y, 288, 54, None, RED, sw=1.3, amp=1.2))
        b.append(T(208, y + 24, rank, 17, RED, weight="bold"))
        b.append(T(208, y + 45, name, 17, INK))
        y += 66
    b.append(box(r, 64, y, 288, 54, None, RED, sw=1.3, amp=1.2))
    b.append(T(208, y + 24, "#4", 17, RED, weight="bold"))
    b.append(T(208, y + 45, "Pre/post-processing bugs", 16, INK))

    b.append(box(r, 414, 192, 150, 54, None, INK, sw=1.3, amp=1.2))
    b.append(T(489, 216, "#5", 17, INK_LIGHT, weight="bold"))
    b.append(T(489, 237, "Model drift", 17, INK))
    b.append(T(489, 288, "dead last", 17, INK_LIGHT))

    b.append(box(r, 624, 192, 198, 54, None, AMBER, sw=1.3, amp=1.2))
    b.append(T(723, 216, "#3", 17, AMBER, weight="bold"))
    b.append(T(723, 237, "External dependencies", 16, INK))

    b.append(T(440, 362, "Four of the five sit outside the model. Yet everyone suspects the model first.", 19, INK))
    b.append(T(440, 394, "Ranked by frequency, the model is rarely the culprit", 17.5, INK_LIGHT))
    return W, H, "".join(b)


def d4_order():
    r = R(404); b = []
    W, H = 880, 470
    b.append(T(440, 46, "Outside in — the order to suspect things", 28, INK, weight="bold"))
    b.append(ul(r, 195, 685, 63))

    order = [
        ("1", "Input data", "nulls, outliers, schema", "red", RED),
        ("2", "Preprocessing", "same as at training?", "amber", AMBER),
        ("3", "Dependencies", "feature store, vector DB", "green", GREEN),
        ("4", "Postprocessing", "thresholds, labels", "teal", TEAL),
        ("5", "The model", "only after the above", "purple", PURPLE),
    ]
    x = 42
    bw = 148
    for num, name, desc, wash, col in order:
        b.append(box(r, x, 78, bw, 108, wash, col, sw=1.7))
        b.append(T(x + bw / 2, 108, num, 24, col, weight="bold"))
        b.append(T(x + bw / 2, 136, name, 17, INK, weight="bold"))
        b.append(T(x + bw / 2, 162, desc, 12.5, INK_LIGHT))
        if num != "5":
            b.append(arr(r, x + bw + 3, 132, x + bw + 13, 132, INK_LIGHT, 1.4, 7))
        x += bw + 16

    b.append(T(440, 218, "The same incident, chased two ways", 20, INK_LIGHT))

    b.append(box(r, 40, 240, 396, 176, "red", RED, sw=1.8))
    b.append(T(238, 270, "Suspect the model first", 21, RED, weight="bold"))
    for i, ln in enumerate(["Day 1  start retraining", "Day 2  deploy — no change",
                            "Day 3-4  tune hyperparameters — no change",
                            "Day 5  check data, find a cache setting"]):
        b.append(T(238, 300 + i * 24, ln, 15.5, INK))
    b.append(T(238, 402, "Four and a half days gone", 20, RED, weight="bold"))

    b.append(box(r, 476, 240, 368, 176, "green", GREEN, sw=1.8))
    b.append(T(660, 270, "Start outside", 21, GREEN, weight="bold"))
    for i, ln in enumerate(["Input data — fine", "Preprocessing — unchanged",
                            "Dependencies — cache TTL changed!", "Roll back, metric recovers"]):
        b.append(T(660, 300 + i * 24, ln, 15.5, INK))
    b.append(T(660, 402, "Done before lunch", 20, GREEN, weight="bold"))

    b.append(T(440, 452, "Cheapest first, outermost first. The order alone is worth days.", 18, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {
    "book1-sw12-en": d1_sw12,
    "book1-cace-en": d2_cace,
    "book1-where-fails-en": d3_where,
    "book1-debug-order-en": d4_order,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
