#!/usr/bin/env python3
"""영문판: FDE 고찰 — 그림 3종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap, wobble_line,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


def d1_map():
    r = R(211); b = []
    W, H = 920, 540
    b.append(T(460, 46, "Many names, and underneath only two axes", 28, INK, weight="bold"))
    b.append(ul(r, 225, 695, 63))

    b.append(f'<path d="{wobble_line(r, 104, 446, 860, 446, 1.4)}" fill="none" stroke="{INK_LIGHT}" stroke-width="1.6" stroke-linecap="round"/>')
    b.append(f'<path d="{wobble_line(r, 104, 446, 104, 96, 1.4)}" fill="none" stroke="{INK_LIGHT}" stroke-width="1.6" stroke-linecap="round"/>')
    b.append(T(482, 478, "when they come in", 19, INK, weight="bold"))
    b.append(T(168, 468, "before the deal", 14, INK_LIGHT))
    b.append(T(806, 468, "after go-live", 14, INK_LIGHT))
    b.append(T(66, 272, "how much code", 19, INK, weight="bold", rot=-90))
    b.append(T(84, 118, "high", 13.5, INK_LIGHT))
    b.append(T(84, 426, "low", 13.5, INK_LIGHT))

    pts = [
        (228, 400, "Sales Engineer", "first demo → signature", "gray", INK_LIGHT),
        (472, 400, "Deployment Strategist", "what to build, and why", "purple", PURPLE),
        (334, 296, "Solutions Architect", "tech review → design", "blue", BLUE),
        (598, 252, "Resident Solutions Architect", "on site through the build", "teal", TEAL),
        (622, 152, "FDE · FDSE", "kickoff → production → renewal", "amber", AMBER),
        (766, 342, "Customer Success Engineer", "support once it is running", "green", GREEN),
    ]
    for x, y, name, when, wash, col in pts:
        w = 212
        b.append(box(r, x - w / 2, y - 26, w, 52, wash, col, sw=1.5, amp=1.3))
        b.append(T(x, y - 4, name, 15, col, weight="bold"))
        b.append(T(x, y + 16, when, 12.5, INK_LIGHT))

    b.append(T(460, 514, "The names differ; the mix of next to the customer · writing code · owning the outcome differs by degree", 16.5, INK_LIGHT))
    return W, H, "".join(b)


def d2_quadrant():
    r = R(222); b = []
    W, H = 880, 500
    b.append(T(440, 46, "Only one square actually needs an FDE", 28, INK, weight="bold"))
    b.append(ul(r, 245, 635, 63))

    b.append(T(470, 100, "who is buying", 18, INK, weight="bold"))
    b.append(T(320, 128, "a technical buyer", 16, INK_LIGHT))
    b.append(T(640, 128, "a non-technical buyer", 16, INK_LIGHT))
    b.append(T(96, 290, "what you sell", 18, INK, weight="bold", rot=-90))

    cells = [
        (170, 148, "gray", INK_LIGHT, "a complex product", "not needed",
         ["GitHub · Datadog", "the buyer is an engineer and", "absorbs the complexity"], False),
        (490, 148, "amber", AMBER, "a complex product", "only this square",
         ["Palantir — and most", "agentic products today", "the customer cannot see what it does"], True),
        (170, 320, "gray", INK_LIGHT, "a simple product", "not needed",
         ["configuration, not", "something to be built"], False),
        (490, 320, "gray", INK_LIGHT, "a simple product", "not needed",
         ["Slack · Jira", "usable without knowing how it works"], False),
    ]
    for x, y, wash, col, kind, verdict, lines, hot in cells:
        h = 152 if len(lines) == 3 else 134
        b.append(box(r, x, y, 300, h, wash, col, sw=1.9 if hot else 1.4))
        b.append(T(x + 150, y + 30, kind, 16.5, INK_LIGHT))
        b.append(T(x + 150, y + 58, verdict, 21, col, weight="bold"))
        for i, ln in enumerate(lines):
            b.append(T(x + 150, y + 88 + i * 22, ln, 13.5, INK))

    b.append(T(440, 486, "The first question is not \"do we want this\" but \"are we in this square\"", 19, INK_LIGHT))
    return W, H, "".join(b)


def d3_platform():
    r = R(233); b = []
    W, H = 880, 456
    b.append(T(440, 46, "Looks like the same job, and the outcomes split", 27, INK, weight="bold"))
    b.append(ul(r, 215, 665, 63))

    b.append(box(r, 36, 84, 392, 226, "red", RED, sw=1.8))
    b.append(T(232, 116, "Without a platform", 21, RED, weight="bold"))
    b.append(T(232, 152, "every customer built from scratch", 16.5, INK))
    b.append(T(232, 180, "the repo count climbs to 55", 16.5, INK))
    b.append(T(232, 208, "nobody can maintain any of it", 16.5, INK))
    b.append(box(r, 66, 226, 332, 62, None, RED, sw=1.3, amp=1.2))
    b.append(T(232, 252, "this is not an FDE organisation,", 15, INK_LIGHT))
    b.append(T(232, 276, "it is a dev shop", 19, RED, weight="bold"))

    b.append(box(r, 452, 84, 392, 226, "green", GREEN, sw=1.8))
    b.append(T(648, 116, "With a platform", 21, GREEN, weight="bold"))
    b.append(T(648, 152, "assembled on top of primitives", 16.5, INK))
    b.append(T(648, 180, "more customers, no more code", 16.5, INK))
    b.append(T(648, 208, "what generalises moves into the platform", 15, INK))
    b.append(box(r, 482, 226, 332, 62, None, GREEN, sw=1.3, amp=1.2))
    b.append(T(648, 252, "that layer of primitives is", 15, INK_LIGHT))
    b.append(T(648, 276, "where the Ontology sits", 19, GREEN, weight="bold"))

    b.append(box(r, 36, 332, 808, 62, "amber", AMBER, sw=1.8))
    b.append(T(440, 360, "So the diagnostic question is a single one", 20, AMBER, weight="bold"))
    b.append(T(440, 384, "\"What are your FDEs assembling on top of right now?\"", 18, INK))

    b.append(T(440, 440, "No answer to that, and it is an FDE in name only", 18, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {
    "fde-map-en": d1_map,
    "fde-quadrant-en": d2_quadrant,
    "fde-platform-en": d3_platform,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
