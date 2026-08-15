#!/usr/bin/env python3
"""영문판: LLM 평가 방법 11가지 — 그림 7종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


# ── 1. 같은 뜻인데 0점
def d_why_hard():
    r = R(701); b = []
    W, H = 880, 448
    b.append(T(440, 46, "Same meaning, and the score comes back zero", 28, INK, weight="bold"))
    b.append(ul(r, 215, 665, 63))

    b.append(box(r, 60, 82, 760, 48, "gray", INK_LIGHT, sw=1.4))
    b.append(T(96, 113, "Question:", 18, INK_LIGHT, anchor="start"))
    b.append(T(196, 113, "\"What is the capital of France?\"", 20, INK, anchor="start"))

    b.append(box(r, 60, 152, 370, 92, "blue", BLUE, sw=1.7))
    b.append(T(245, 182, "Reference (gold answer)", 18, BLUE, weight="bold"))
    b.append(T(245, 214, "\"Paris is the capital of France.\"", 18, INK))

    b.append(box(r, 450, 152, 370, 92, "amber", AMBER, sw=1.7))
    b.append(T(635, 182, "What the model said", 18, AMBER, weight="bold"))
    b.append(T(635, 214, "\"France's capital? Paris, of course.\"", 17, INK))

    b.append(box(r, 60, 268, 370, 132, "red", RED, sw=1.8))
    b.append(T(245, 300, "Counting word overlap", 20, RED, weight="bold"))
    b.append(T(245, 330, "shared words: \"France\", \"Paris\"", 16.5, INK))
    b.append(T(245, 354, "order and phrasing are different", 16.5, INK))
    b.append(T(245, 386, "→  close to zero", 21, RED, weight="bold"))

    b.append(box(r, 450, 268, 370, 132, "green", GREEN, sw=1.8))
    b.append(T(635, 300, "When a person reads it", 20, GREEN, weight="bold"))
    b.append(T(635, 330, "it answers exactly what was asked", 16.5, INK))
    b.append(T(635, 354, "and the fact is correct", 16.5, INK))
    b.append(T(635, 386, "→  full marks", 21, GREEN, weight="bold"))

    b.append(T(440, 432, "The same answer scores zero or full marks depending on the grader", 19, INK_LIGHT))
    return W, H, "".join(b)


# ── 2. 네 계열 지도
def d_map():
    r = R(702); b = []
    W, H = 900, 770
    b.append(T(450, 48, "Eleven ways to evaluate an LLM, grouped into four families", 27, INK, weight="bold"))
    b.append(T(450, 82, "The families split on one question: what counts as the ground truth?", 18, INK_LIGHT))

    secs = [
        ("①", "Compare against a reference", "measure how far the answer strays from a gold answer",
         "blue", BLUE,
         [("BLEU", "of what it said, how much is in the reference"),
          ("ROUGE", "of the reference, how much is in the answer"),
          ("BERTScore", "compare by meaning, not by characters")]),
        ("②", "Let a model do the grading", "no reference — hand another LLM the criteria",
         "amber", AMBER,
         [("G-Eval", "unfold criteria into steps, then score"),
          ("LLM-as-Judge", "put two side by side, pick a winner"),
          ("LLM jury", "average several independent judges")]),
        ("③", "People nail the standard down", "two things that hold steady when auto-grading wobbles",
         "purple", PURPLE,
         [("Human evaluation", "the reference point every metric must match"),
          ("DAG", "a decision tree of yes/no branches")]),
        ("④", "Look at behaviour, not the answer", "score the path, the conversation and the risk",
         "teal", TEAL,
         [("Trajectory accuracy", "the steps the agent actually took"),
          ("Multi-turn", "the whole conversation as one unit"),
          ("Safety", "a gate, not a score")]),
    ]

    y0 = 112
    for num, head, desc, wash, col, items in secs:
        b.append(box(r, 36, y0, 828, 140, wash, col, sw=1.8))
        b.append(T(58, y0 + 34, num, 26, col, anchor="start", weight="bold"))
        b.append(T(90, y0 + 34, head, 22, col, anchor="start", weight="bold"))
        b.append(T(92, y0 + 60, desc, 16.5, INK_LIGHT, anchor="start"))
        if len(items) == 3:
            cols = [(52, 252), (330, 252), (608, 252)]
        else:
            cols = [(52, 390), (474, 386)]
        for (x, w), (name, sub) in zip(cols, items):
            b.append(box(r, x, y0 + 76, w, 52, None, col, sw=1.2, amp=1.2))
            b.append(T(x + w / 2, y0 + 99, name, 18, col, weight="bold"))
            b.append(T(x + w / 2, y0 + 119, sub, 14, INK_LIGHT))
        y0 += 156

    b.append(T(450, 750, "Going down, the question shifts from \"did it get it right\" to \"does this work as a product\"", 18, INK))
    return W, H, "".join(b)


# ── 3. 정답지 비교 세 가지
def d_reference():
    r = R(703); b = []
    W, H = 900, 560
    b.append(T(450, 46, "The three reference-based metrics — the arrows point different ways", 25, INK, weight="bold"))
    b.append(ul(r, 195, 705, 63))

    blocks = [
        ("BLEU", 78, "— is what it said grounded?  (precision)", "green", GREEN, "forward",
         "is this phrasing in the reference?",
         ["Fits translation, where wording is near-fixed.",
          "A length penalty stops it gaming brevity."]),
        ("ROUGE", 90, "— did it leave anything out?  (recall)", "blue", BLUE, "back",
         "is this content in the answer?",
         ["Fits summarisation, where omission hurts most.",
          "Longer answers win — pair it with precision."]),
        ("BERTScore", 138, "— match meaning, not characters", "amber", AMBER, "both",
         "close in meaning counts",
         ["Catches a right answer worded differently.",
          "Scores bunch in a narrow band; not absolute."]),
    ]

    y0 = 110
    for name, nw, tag, wash, col, direction, arrow_label, notes in blocks:
        b.append(T(44, y0, name, 23, col, anchor="start", weight="bold"))
        b.append(T(44 + nw, y0, tag, 16.5, INK_LIGHT, anchor="start"))

        b.append(box(r, 44, y0 + 40, 168, 46, wash, col, sw=1.6))
        b.append(T(128, y0 + 69, "model answer", 17, INK))
        b.append(box(r, 316, y0 + 40, 150, 46, "gray", INK_LIGHT, sw=1.6))
        b.append(T(391, y0 + 69, "reference", 17, INK))

        if direction == "forward":
            b.append(arr(r, 218, y0 + 63, 310, y0 + 63, col, 1.6))
        elif direction == "back":
            b.append(arr(r, 310, y0 + 63, 218, y0 + 63, col, 1.6))
        else:
            b.append(arr(r, 264, y0 + 63, 218, y0 + 63, col, 1.6))
            b.append(arr(r, 264, y0 + 63, 310, y0 + 63, col, 1.6))
        b.append(T(264, y0 + 24, arrow_label, 15, col))

        b.append(T(500, y0 + 56, notes[0], 16.5, INK, anchor="start"))
        b.append(T(500, y0 + 80, notes[1], 16.5, INK, anchor="start"))
        y0 += 150

    b.append(T(450, 538, "All three need a reference. Without one you move to the next family.", 19, INK))
    return W, H, "".join(b)


# ── 4. 판정 모델 세 방식
def d_judge_pipeline():
    r = R(704); b = []
    W, H = 900, 494
    b.append(T(450, 46, "No reference: three ways to hand the grading to a model", 26, INK, weight="bold"))
    b.append(ul(r, 200, 700, 63))

    rows = [
        ("G-Eval — unfold the criteria into steps, then score", "green", GREEN,
         [("the answer +", "the criteria"), ("judge model", "generates steps"),
          ("walks the steps", "and scores"), ("probability-weighted", "final score")]),
        ("LLM-as-Judge — set two answers side by side, pick the better", "blue", BLUE,
         [("answer A and", "answer B"), ("hold the rubric,", "compare the two"),
          ("pick a winner", "(repeat over pairs)"), ("who won most often", "win-rate ranking")]),
        ("LLM jury — scatter one judge's habits across several", "purple", PURPLE,
         [("the answer", "to be graded"), ("judge models", "A · B · C"),
          ("average each", "of their scores"), ("a steadier", "consensus score")]),
    ]

    hy = 96
    for head, wash, col, stages in rows:
        b.append(T(44, hy, head, 20, col, anchor="start", weight="bold"))
        x = 48
        for i, (l1, l2) in enumerate(stages):
            b.append(box(r, x, hy + 18, 176, 58, wash, col, sw=1.5))
            b.append(T(x + 88, hy + 42, l1, 16.5, INK))
            b.append(T(x + 88, hy + 63, l2, 16.5, INK))
            if i < 3:
                b.append(arr(r, x + 180, hy + 47, x + 200, hy + 47, INK_LIGHT, 1.4, 7))
            x += 204
        hy += 136

    b.append(T(450, 478, "Three models from one family only cut noise — the habit stays. Mix different families.", 18, INK))
    return W, H, "".join(b)


# ── 5. 판정 모델의 버릇 셋
def d_judge_bias():
    r = R(705); b = []
    W, H = 900, 384
    b.append(T(450, 46, "The grader is a model too — three known habits", 27, INK, weight="bold"))
    b.append(ul(r, 235, 665, 63))

    cols = [
        (30, "red", RED, "It follows order",
         ["compare two answers and it", "picks the first one more often"],
         "the same answer wins more often in slot A",
         "shuffle the order at random"),
        (315, "amber", AMBER, "It likes long answers",
         ["even when the content is no better,", "length earns extra points"],
         "a padded answer beats a crisp correct one",
         "match lengths, or control for it"),
        (600, "purple", PURPLE, "It favours its own kin",
         ["answers written by models from", "its own family score higher"],
         "three of the same model will not fix it",
         "mix in different model families"),
    ]
    for x, wash, col, title, lines, note, fix in cols:
        cx = x + 135
        b.append(box(r, x, 76, 270, 208, wash, col, sw=1.8))
        b.append(T(cx, 108, title, 21, col, weight="bold"))
        b.append(T(cx, 140, lines[0], 15.5, INK))
        b.append(T(cx, 162, lines[1], 15.5, INK))
        b.append(T(cx, 198, note, 13.5, INK_LIGHT))
        b.append(T(cx, 234, "how to block it", 16, col, weight="bold"))
        b.append(T(cx, 260, fix, 15.5, INK))

    b.append(T(450, 326, "None of these wash out by averaging over many runs — they are a lean, not noise", 18, INK))
    b.append(T(450, 356, "So before trusting a judge, calibrate it against a small human-graded set", 17, INK_LIGHT))
    return W, H, "".join(b)


# ── 6. 경로 정확도
def d_agent_path():
    r = R(706); b = []
    W, H = 900, 452
    b.append(T(450, 46, "Score the answer alone and these two did equally well", 26, INK, weight="bold"))
    b.append(ul(r, 215, 685, 63))

    b.append(T(44, 96, "Agent A", 20, GREEN, anchor="start", weight="bold"))
    stepsA = ["query DB", "aggregate", "write answer"]
    x = 44
    for s in stepsA:
        b.append(box(r, x, 112, 132, 46, "green", GREEN, sw=1.5))
        b.append(T(x + 66, 141, s, 16.5, INK))
        b.append(arr(r, x + 136, 135, x + 150, 135, INK_LIGHT, 1.3, 6))
        x += 152
    b.append(box(r, x, 112, 110, 46, "green", GREEN, sw=1.8))
    b.append(T(x + 55, 141, "correct", 18, GREEN, weight="bold"))
    b.append(T(676, 126, "3 steps, 3 tool calls", 16, INK, anchor="start"))
    b.append(T(676, 150, "and a clean path", 16, INK, anchor="start"))

    b.append(T(44, 208, "Agent B", 20, RED, anchor="start", weight="bold"))
    stepsB = [("query DB", None), ("query DB again", None),
              ("customer API", "off-limits tool"), ("aggregate again", None)]
    x = 44
    for s, warn in stepsB:
        b.append(box(r, x, 224, 132, 46, "red" if warn else None, RED if warn else INK_LIGHT,
                     sw=1.7 if warn else 1.3))
        if warn:
            b.append(T(x + 66, 245, s, 15.5, INK))
            b.append(T(x + 66, 263, warn, 13, RED, weight="bold"))
        else:
            b.append(T(x + 66, 253, s, 16, INK))
        b.append(arr(r, x + 136, 247, x + 150, 247, INK_LIGHT, 1.3, 6))
        x += 152
    b.append(box(r, x, 224, 110, 46, "green", GREEN, sw=1.8))
    b.append(T(x + 55, 253, "correct", 18, GREEN, weight="bold"))

    b.append(T(44, 300, "12 steps, 4× the tokens, and it touched a tool it was not allowed to. Same final answer as A.",
               17, INK, anchor="start"))

    b.append(box(r, 40, 324, 396, 96, "red", RED, sw=1.8))
    b.append(T(238, 356, "Score the answer only", 20, RED, weight="bold"))
    b.append(T(238, 386, "both get full marks — the incident", 16, INK))
    b.append(T(238, 408, "surfaces after launch", 16, INK))

    b.append(box(r, 464, 324, 396, 96, "green", GREEN, sw=1.8))
    b.append(T(662, 356, "Score the path separately", 20, GREEN, weight="bold"))
    b.append(T(662, 386, "B's waste and its permission breach", 16, INK))
    b.append(T(662, 408, "are caught in advance", 16, INK))
    return W, H, "".join(b)


# ── 7. 선택 가이드
def d_choose():
    r = R(707); b = []
    W, H = 900, 548
    b.append(T(450, 46, "So which one do I actually use?", 28, INK, weight="bold"))
    b.append(ul(r, 285, 615, 63))

    b.append(box(r, 300, 74, 300, 44, "gray", INK, sw=1.8))
    b.append(T(450, 104, "Is there a reference answer?", 19, INK, weight="bold"))

    b.append(arr(r, 390, 122, 258, 160, INK_LIGHT, 1.5))
    b.append(T(344, 146, "yes", 16, INK_LIGHT))
    b.append(arr(r, 510, 122, 642, 160, INK_LIGHT, 1.5))
    b.append(T(556, 146, "no", 16, INK_LIGHT))

    b.append(box(r, 80, 166, 320, 40, "blue", BLUE, sw=1.7))
    b.append(T(240, 193, "Is the wording near-fixed too?", 18, BLUE, weight="bold"))
    b.append(arr(r, 180, 210, 138, 240, INK_LIGHT, 1.4, 7))
    b.append(T(112, 232, "yes", 15, INK_LIGHT))
    b.append(arr(r, 300, 210, 346, 240, INK_LIGHT, 1.4, 7))
    b.append(T(376, 232, "no", 15, INK_LIGHT))

    b.append(box(r, 40, 244, 196, 62, "green", GREEN, sw=1.7))
    b.append(T(138, 272, "BLEU / ROUGE", 19, GREEN, weight="bold"))
    b.append(T(138, 294, "translation · extraction", 14.5, INK))
    b.append(box(r, 248, 244, 196, 62, "green", GREEN, sw=1.7))
    b.append(T(346, 272, "BERTScore", 19, GREEN, weight="bold"))
    b.append(T(346, 294, "same sense, other words", 14.5, INK))

    b.append(box(r, 500, 166, 320, 40, "amber", AMBER, sw=1.7))
    b.append(T(660, 193, "What do you want to know?", 18, AMBER, weight="bold"))
    b.append(arr(r, 600, 210, 566, 240, INK_LIGHT, 1.4, 7))
    b.append(arr(r, 720, 210, 774, 240, INK_LIGHT, 1.4, 7))

    b.append(box(r, 468, 244, 196, 62, "amber", AMBER, sw=1.7))
    b.append(T(566, 272, "G-Eval", 19, AMBER, weight="bold"))
    b.append(T(566, 294, "tone, following instructions", 13.5, INK))
    b.append(box(r, 676, 244, 196, 62, "amber", AMBER, sw=1.7))
    b.append(T(774, 272, "LLM-as-Judge", 18, AMBER, weight="bold"))
    b.append(T(774, 294, "which version is better", 14, INK))

    b.append(T(450, 352, "Whatever route you took, these always attach", 21, INK, weight="bold"))
    attach = [(40, "Human evaluation", "what the metrics calibrate to"),
              (316, "DAG", "format rules you must not break"),
              (592, "Safety", "a gate, not a score")]
    for x, name, sub in attach:
        b.append(box(r, x, 366, 268, 52, "purple", PURPLE, sw=1.5))
        b.append(T(x + 134, 390, name, 17, PURPLE, weight="bold"))
        b.append(T(x + 134, 410, sub, 14, INK))

    b.append(T(450, 460, "Building an agent? Two more attach here", 21, INK, weight="bold"))
    agentic = [(130, "Trajectory accuracy", "score path and answer separately"),
               (470, "Multi-turn", "what collapses as talk deepens")]
    for x, name, sub in agentic:
        b.append(box(r, x, 474, 300, 52, "teal", TEAL, sw=1.5))
        b.append(T(x + 150, 498, name, 17, TEAL, weight="bold"))
        b.append(T(x + 150, 518, sub, 14, INK))
    return W, H, "".join(b)


DIAGRAMS = {
    "eval-why-hard-en": d_why_hard,
    "eval-map-en": d_map,
    "eval-reference-based-en": d_reference,
    "eval-judge-pipeline-en": d_judge_pipeline,
    "eval-judge-bias-en": d_judge_bias,
    "eval-agent-path-en": d_agent_path,
    "eval-choose-en": d_choose,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
