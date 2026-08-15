#!/usr/bin/env python3
"""영문판: 팔란티어 온톨로지 — 그림 3종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


def d1_layers():
    r = R(81); b = []
    W, H = 880, 440
    b.append(T(440, 46, "Nouns, verbs, and the grammar between them", 28, INK, weight="bold"))
    b.append(ul(r, 175, 705, 63))

    rows = [
        (84, "Semantic", "nouns", "blue", BLUE,
         "Object Type · Property · Link Type",
         "Machines, customers, purchase orders, and how they relate"),
        (196, "Kinetic", "verbs", "green", GREEN,
         "Action Type · Function",
         "Schedule maintenance, cancel an order, approve a refund"),
        (308, "Dynamic", "grammar", "red", RED,
         "Runtime security · permissions · purpose-based policy",
         "Who may do what, for what purpose, decided at run time"),
    ]
    for y, name, role, wash, col, comps, desc in rows:
        b.append(box(r, 36, y, 808, 96, wash, col, sw=1.8))
        b.append(T(150, y + 40, name, 21, col, weight="bold"))
        b.append(box(r, 96, y + 52, 108, 32, None, col, sw=1.2, amp=1.1))
        b.append(T(150, y + 74, role, 18, INK, weight="bold"))
        b.append(T(534, y + 40, comps, 17, INK))
        b.append(T(534, y + 70, desc, 15, INK_LIGHT))

    b.append(T(440, 428, "Most data platforms stop at the first layer", 19, INK_LIGHT))
    return W, H, "".join(b)


def d2_axes():
    r = R(92); b = []
    W, H = 900, 470
    b.append(T(450, 46, "The two ontologies, measured on four axes", 28, INK, weight="bold"))
    b.append(ul(r, 185, 715, 63))

    b.append(box(r, 320, 80, 272, 44, "gray", INK_LIGHT, sw=1.5))
    b.append(T(456, 110, "Classical (OWL · RDF)", 18, INK, weight="bold"))
    b.append(box(r, 604, 80, 260, 44, "amber", AMBER, sw=1.6))
    b.append(T(734, 110, "Palantir Ontology", 18, AMBER, weight="bold"))

    rows = [
        (134, "1. What exists?", "strong", "present", GREEN, AMBER,
         "class hierarchy, inference", "Object Type, no inference"),
        (208, "2. What state is it in?", "present", "strong", AMBER, GREEN,
         "ABox — largely static", "live, and writable"),
        (282, "3. What may change?", "absent", "strong", RED, GREEN,
         "no notion of action at all", "Action Type is the centre"),
        (356, "4. What is forbidden?", "weak", "strong", RED, GREEN,
         "logical constraints only", "permissions, policy, audit"),
    ]
    for y, axis, l, rr, lcol, rcol, ldesc, rdesc in rows:
        b.append(box(r, 36, y, 268, 62, None, INK_LIGHT, sw=1.2, amp=1.2))
        b.append(T(170, y + 38, axis, 17, INK))
        b.append(box(r, 320, y, 272, 62, None, lcol, sw=1.3, amp=1.2))
        b.append(T(456, y + 26, l, 18, lcol, weight="bold"))
        b.append(T(456, y + 48, ldesc, 13.5, INK_LIGHT))
        b.append(box(r, 604, y, 260, 62, None, rcol, sw=1.3, amp=1.2))
        b.append(T(734, y + 26, rr, 18, rcol, weight="bold"))
        b.append(T(734, y + 48, rdesc, 13.5, INK_LIGHT))

    b.append(T(450, 446, "Not an ontology by the academic test, yet fuller on the axes an agent needs", 18, INK))
    return W, H, "".join(b)


def d3_action():
    r = R(103); b = []
    W, H = 880, 420
    b.append(T(440, 46, "An action is not just a function", 28, INK, weight="bold"))
    b.append(ul(r, 240, 640, 63))

    b.append(box(r, 36, 84, 808, 92, "gray", INK_LIGHT, sw=1.5))
    b.append(T(120, 136, "Plain function", 19, INK_LIGHT, weight="bold"))
    x = 236
    for s in ["input", "run", "result"]:
        b.append(box(r, x, 106, 150, 48, None, INK_LIGHT, sw=1.2, amp=1.2))
        b.append(T(x + 75, 136, s, 18, INK))
        if s != "result":
            b.append(arr(r, x + 154, 130, x + 178, 130, INK_LIGHT, 1.4, 7))
        x += 182

    b.append(box(r, 36, 196, 808, 124, "green", GREEN, sw=1.8))
    b.append(T(120, 246, "Governed", 19, GREEN, weight="bold"))
    b.append(T(120, 272, "operation", 16, INK_LIGHT))
    steps = ["input", "validate", "check perms", "run", "write back", "audit log"]
    x = 200
    bw = 100
    for i, s in enumerate(steps):
        hot = s in ("validate", "check perms", "audit log")
        b.append(box(r, x, 224, bw, 48, "amber" if hot else None,
                     AMBER if hot else INK, sw=1.4 if hot else 1.2, amp=1.2))
        b.append(T(x + bw / 2, 254, s, 15, AMBER if hot else INK,
                   weight="bold" if hot else "normal"))
        if i < len(steps) - 1:
            b.append(arr(r, x + bw + 2, 248, x + bw + 10, 248, INK_LIGHT, 1.3, 6))
        x += bw + 12

    b.append(T(440, 300, "The amber boxes are what separate a button a person may press from one they may not", 16.5, INK))
    b.append(T(440, 366, "Handing an agent execution rights needs exactly this difference", 20, INK))
    b.append(T(440, 398, "Not what can be done, but what may be done, written down alongside", 18, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {
    "palantir-layers-en": d1_layers,
    "palantir-axes-en": d2_axes,
    "palantir-action-en": d3_action,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
