#!/usr/bin/env python3
"""영문판: 월드모델 두 계보의 역사 — 그림 4종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


def d1_fork():
    r = R(111); b = []
    W, H = 880, 400
    b.append(T(440, 46, "It started from one shared question", 28, INK, weight="bold"))
    b.append(ul(r, 255, 625, 63))

    b.append(box(r, 210, 84, 460, 62, "gray", INK, sw=1.8))
    b.append(T(440, 112, "How do you put how the world works", 20, INK, weight="bold"))
    b.append(T(440, 136, "inside a machine?", 20, INK, weight="bold"))

    b.append(arr(r, 380, 150, 260, 196, INK_LIGHT, 1.6))
    b.append(arr(r, 500, 150, 620, 196, INK_LIGHT, 1.6))

    b.append(box(r, 50, 202, 380, 130, "purple", PURPLE, sw=1.8))
    b.append(T(240, 236, "Symbolic — write it down", 21, PURPLE, weight="bold"))
    b.append(T(240, 272, "\"people write the rules\"", 18, INK))
    b.append(T(240, 304, "logic · rules · state machines", 16.5, INK_LIGHT))

    b.append(box(r, 450, 202, 380, 130, "green", GREEN, sw=1.8))
    b.append(T(640, 236, "Neural — learn by looking", 21, GREEN, weight="bold"))
    b.append(T(640, 272, "\"let the machine learn it\"", 18, INK))
    b.append(T(640, 304, "control theory · nets · prediction", 16, INK_LIGHT))

    b.append(T(440, 372, "Seventy years have passed since that fork, and the two took very different roads", 17.5, INK_LIGHT))
    return W, H, "".join(b)


def d2_symbolic():
    r = R(122); b = []
    W, H = 920, 570
    b.append(T(460, 46, "Symbolic — a history of narrowing what to write down", 26, PURPLE, weight="bold"))
    b.append(ul(r, 200, 720, 63))

    steps = [
        ("1950s–60s", "Maybe we can just write it in logic",
         "write facts about the world as logical statements and the machine infers", None),
        ("1971", "Writing actions down — STRIPS",
         "\"to open a door you must be at it; opening it makes it open\"",
         "you must also write what does not change (the frame problem)"),
        ("1970s–80s", "Give up the world, take one narrow field",
         "medical diagnosis, system configuration — expert systems sold commercially",
         "past a few thousand rules nobody could touch it"),
        ("1990s–2000s", "Make a standard and share it",
         "RDF · OWL — the Semantic Web, making the whole web machine-readable",
         "nobody tagged anything"),
        ("2012–", "A practical retreat — knowledge graphs",
         "drop perfect inference, aim at usefulness. This one survived", None),
    ]
    y = 86
    for era, title, desc, wall in steps:
        h = 86 if wall else 62
        b.append(box(r, 36, y, 848, h, "purple", PURPLE, sw=1.5))
        b.append(T(122, y + 28, era, 16, PURPLE, weight="bold"))
        b.append(T(232, y + 28, title, 18, INK, anchor="start", weight="bold"))
        b.append(T(232, y + 50, desc, 15, INK_LIGHT, anchor="start"))
        if wall:
            b.append(box(r, 232, y + 60, 620, 22, "red", RED, sw=1.1, amp=1.0))
            b.append(T(542, y + 76, "the wall — " + wall, 14.5, RED))
        y += h + 12

    b.append(T(460, 552, "Where the field is narrow and failure is expensive, it is still quietly running", 18, INK))
    return W, H, "".join(b)


def d3_neural():
    r = R(133); b = []
    W, H = 920, 592
    b.append(T(460, 46, "Neural — a history of drawing less and less", 27, GREEN, weight="bold"))
    b.append(ul(r, 230, 690, 63))

    steps = [
        ("1960", "The Kalman filter — the root was engineering",
         "write the world model as equations and predict the next state. It flew on Apollo",
         "a person has to write those equations"),
        ("1990", "So let the equations be learned",
         "the idea of learning environment dynamics with a neural network",
         "neither the compute nor the data existed yet"),
        ("2018", "The moment it got a name — World Models",
         "eyes (compress) + memory (predict) + hands (act). Trained inside an imagined world", None),
        ("2019–23", "Industrialised — the Dreamer line",
         "imagination-based training refined until one config solves 150+ tasks", None),
        ("2020–", "No need to draw it all — MuZero, JEPA",
         "abandon frame reconstruction and predict only what the decision needs", None),
        ("2024–", "And then video generation joined",
         "the side that draws every pixel started producing striking results", None),
    ]
    y = 86
    for era, title, desc, wall in steps:
        h = 80 if wall else 58
        b.append(box(r, 36, y, 848, h, "green", GREEN, sw=1.5))
        b.append(T(112, y + 26, era, 16, GREEN, weight="bold"))
        b.append(T(206, y + 26, title, 18, INK, anchor="start", weight="bold"))
        b.append(T(206, y + 48, desc, 14.5, INK_LIGHT, anchor="start"))
        if wall:
            b.append(box(r, 206, y + 56, 646, 20, "red", RED, sw=1.1, amp=1.0))
            b.append(T(529, y + 71, "the wall — " + wall, 14.5, RED))
        y += h + 12

    b.append(T(460, 572, "Today the family is split internally: draw the pixels, or throw them away", 18, INK))
    return W, H, "".join(b)


def d4_mirror():
    r = R(144); b = []
    W, H = 900, 410
    b.append(T(450, 46, "The two lineages are mirror images", 28, INK, weight="bold"))
    b.append(ul(r, 260, 640, 63))

    b.append(box(r, 36, 84, 400, 168, "purple", PURPLE, sw=1.8))
    b.append(T(236, 116, "Symbolic", 22, PURPLE, weight="bold"))
    b.append(T(236, 152, "tried to write it all, could not,", 18, INK))
    b.append(T(236, 180, "and kept narrowing the scope", 18, INK))
    b.append(box(r, 66, 196, 340, 40, None, PURPLE, sw=1.2, amp=1.1))
    b.append(T(236, 222, "the world → one field → one task", 16, INK_LIGHT))

    b.append(box(r, 464, 84, 400, 168, "green", GREEN, sw=1.8))
    b.append(T(664, 116, "Neural", 22, GREEN, weight="bold"))
    b.append(T(664, 152, "tried to draw it all, too expensive,", 18, INK))
    b.append(T(664, 180, "and kept narrowing the target", 18, INK))
    b.append(box(r, 494, 196, 340, 40, None, GREEN, sw=1.2, amp=1.1))
    b.append(T(664, 222, "every pixel → what matters → abstractions", 15, INK_LIGHT))

    b.append(box(r, 36, 274, 828, 62, "amber", AMBER, sw=1.8))
    b.append(T(450, 302, "Both are histories of learning what to give up", 21, INK, weight="bold"))
    b.append(T(450, 326, "And what each gave up sits on exactly opposite sides, which is why they are meeting now", 15.5, INK_LIGHT))

    b.append(T(450, 384, "Reading broadly and guaranteeing narrowly became necessary at the same time", 17.5, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {
    "lineage-fork-en": d1_fork,
    "lineage-symbolic-en": d2_symbolic,
    "lineage-neural-en": d3_neural,
    "lineage-mirror-en": d4_mirror,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
