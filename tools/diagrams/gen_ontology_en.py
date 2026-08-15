#!/usr/bin/env python3
"""영문판: 규범은 데이터에 없다 — 그림 3종.

한국어판(gen_ontology.py)과 같은 레이아웃에 문자열만 영어로 바꾼 것.
영문은 같은 글자수라도 폭을 더 먹으므로 상자를 조금씩 넓혔다.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


# ── 1. 네 축이 세 층위로 갈린다
def d1_axes():
    r = R(51); b = []
    W, H = 900, 470
    b.append(T(450, 46, "The four axes, read as families of formalism", 28, INK, weight="bold"))
    b.append(ul(r, 175, 725, 63))

    rows = [
        (86, ["1. What exists?", "2. What state is it in?"], "Ontology",
         "Concepts and taxonomy (TBox), individuals and facts (ABox)", "blue", BLUE, 96),
        (198, ["3. What changes are allowed?"], "Dynamics",
         "Action formalisms — PDDL preconditions and effects", "green", GREEN, 68),
        (282, ["4. What is forbidden?"], "Norms",
         "Integrity constraints, access control, deontic logic", "red", RED, 68),
    ]
    for y, axes, layer, formal, wash, col, h in rows:
        b.append(box(r, 36, y, 300, h, "gray", INK_LIGHT, sw=1.4))
        for i, a in enumerate(axes):
            b.append(T(186, y + (34 if len(axes) == 1 else 30 + i * 34), a, 17, INK))
        b.append(arr(r, 344, y + h / 2, 384, y + h / 2, INK_LIGHT, 1.6))
        b.append(box(r, 392, y, 140, h, wash, col, sw=1.7))
        b.append(T(462, y + h / 2 + 7, layer, 21, col, weight="bold"))
        b.append(box(r, 544, y, 320, h, None, col, sw=1.3, amp=1.2))
        b.append(T(704, y + h / 2 + 6, formal, 14, INK))

    b.append(box(r, 36, 372, 828, 62, "amber", AMBER, sw=1.8))
    b.append(T(450, 398, "1–3 ask what is possible. Only 4 asks what is permitted.", 20, INK, weight="bold"))
    b.append(T(450, 422, "Logic calls the first alethic and the second deontic.", 17, INK_LIGHT))

    b.append(T(450, 458, "Not one flat list, but three layers of a different kind stacked together", 17, INK_LIGHT))
    return W, H, "".join(b)


# ── 2. 알레틱과 데온틱 사이의 간극
def d2_gap():
    r = R(62); b = []
    W, H = 880, 470
    b.append(T(440, 46, "A line no amount of observation crosses", 28, INK, weight="bold"))
    b.append(ul(r, 185, 695, 63))

    b.append(box(r, 36, 84, 376, 236, "blue", BLUE, sw=1.8))
    b.append(T(224, 116, "Alethic — what is possible", 20, BLUE, weight="bold"))
    b.append(T(224, 152, "A ball falls when dropped", 17, INK))
    b.append(T(224, 180, "This balance cannot cover the charge", 17, INK))
    b.append(T(224, 208, "This API answers within three seconds", 17, INK))
    b.append(box(r, 62, 228, 324, 68, None, BLUE, sw=1.2, amp=1.2))
    b.append(T(224, 254, "Facts about the world,", 16, INK))
    b.append(T(224, 280, "so they can be learned from data", 16, INK))

    b.append(box(r, 468, 84, 376, 236, "red", RED, sw=1.8))
    b.append(T(656, 116, "Deontic — what is permitted", 20, RED, weight="bold"))
    b.append(T(656, 152, "May this transaction be approved?", 17, INK))
    b.append(T(656, 180, "May this customer record be read?", 17, INK))
    b.append(T(656, 208, "May this refund be auto-processed?", 17, INK))
    b.append(box(r, 494, 228, 324, 68, None, RED, sw=1.2, amp=1.2))
    b.append(T(656, 254, "Norms we decided on,", 16, INK))
    b.append(T(656, 280, "so they appear nowhere in the data", 16, INK))

    b.append(T(440, 176, "?", 40, INK_LIGHT, weight="bold"))
    b.append(T(440, 214, "no bridge", 15, INK_LIGHT))

    b.append(box(r, 36, 344, 808, 82, "amber", AMBER, sw=1.8))
    b.append(T(440, 374, "You cannot derive an ought from an is — Hume, 1739", 20, INK, weight="bold"))
    b.append(T(440, 404, "So a neural world model missing norms is not short on data", 18, INK))

    b.append(T(440, 456, "It is the wrong category of thing, and scale does not close it", 18, INK_LIGHT))
    return W, H, "".join(b)


# ── 3. 뉴로심볼릭의 역할 분담
def d3_split():
    r = R(73); b = []
    W, H = 880, 480
    b.append(T(440, 46, "Each one fills exactly the other's hole", 28, INK, weight="bold"))
    b.append(ul(r, 200, 680, 63))

    b.append(box(r, 36, 84, 376, 226, "green", GREEN, sw=1.8))
    b.append(T(224, 116, "The neural line", 22, GREEN, weight="bold"))
    b.append(T(224, 150, "Good at", 17, GREEN, weight="bold"))
    b.append(T(224, 178, "Turning messy reality into symbols", 16.5, INK))
    b.append(T(224, 202, "Reading situations it has never seen", 16.5, INK))
    b.append(T(224, 240, "Bad at", 17, RED, weight="bold"))
    b.append(T(224, 268, "Wobbling on corner cases", 16.5, INK))
    b.append(T(224, 292, "Guaranteeing anything at all", 16.5, INK))

    b.append(box(r, 468, 84, 376, 226, "purple", PURPLE, sw=1.8))
    b.append(T(656, 116, "The symbolic line", 22, PURPLE, weight="bold"))
    b.append(T(656, 150, "Good at", 17, GREEN, weight="bold"))
    b.append(T(656, 178, "Executing only permitted transitions", 16.5, INK))
    b.append(T(656, 202, "Making audit a structural property", 16.5, INK))
    b.append(T(656, 240, "Bad at", 17, RED, weight="bold"))
    b.append(T(656, 268, "Needing the world written down", 16.5, INK))
    b.append(T(656, 292, "Stalling on what was never written", 16.5, INK))

    b.append(arr(r, 420, 200, 460, 200, INK_LIGHT, 1.6))
    b.append(arr(r, 460, 250, 420, 250, INK_LIGHT, 1.6))

    b.append(box(r, 36, 334, 808, 106, "amber", AMBER, sw=1.8))
    b.append(T(440, 364, "So the division of labour is not arbitrary", 21, AMBER, weight="bold"))
    b.append(T(440, 398, "Neural handles grounding — reading an open world into symbols", 18, INK))
    b.append(T(440, 424, "Symbolic handles enforcement — letting only the allowed through", 18, INK))

    b.append(T(440, 466, "Keep possibility wide, keep execution narrow and safe", 18, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {
    "onto-axes-en": d1_axes,
    "onto-gap-en": d2_gap,
    "onto-split-en": d3_split,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
