#!/usr/bin/env python3
"""AI 도구들이 Rust로 옮겨 가는 이유: 그림 2종 (한/영)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER)


TEXT = {
    "ko": {
        "mem_title": "메모리를 치우는 세 가지 방법",
        "cols": [
            ("red", RED, "직접 치운다", "C, C++",
             ["빠르고 가볍다", "치운 자리를 다시 쓰면", "멈추거나 보안 구멍이 난다"]),
            ("blue", BLUE, "청소기에 맡긴다", "Python, Java, Go",
             ["실수할 일이 적다", "대신 청소하는 동안", "가끔 멈칫한다"]),
            ("green", GREEN, "주인을 하나로 정한다", "Rust",
             ["규칙을 어기면", "아예 빌드가 안 된다", "실행 중에는 청소기가 없다"]),
        ],
        "mem_foot1": "Rust는 이 검사를 실행 전에, 컴파일러가 끝낸다",
        "mem_foot2": "그래서 빠르고 안전한데, 처음 배우는 사람은 이 규칙에서 많이 막힌다",
        "lay_title": "쓰는 쪽은 Python, 밑에서 도는 건 Rust",
        "lay_top": "내가 쓰는 Python 코드",
        "lay_code": ["import tiktoken", "from tokenizers import Tokenizer", "from pydantic import BaseModel"],
        "lay_bottom": "속에서 도는 Rust",
        "lay_items": [("토큰 나누기", "tiktoken, tokenizers"), ("데이터 검증", "pydantic-core")],
        "lay_note": ["Rust를 몰라도", "그냥 import해서 쓴다"],
        "lay_foot": "무거운 계산만 Rust로 내리고, 쓰는 방법은 그대로 둔다",
    },
    "en": {
        "mem_title": "Three ways to clean up memory",
        "cols": [
            ("red", RED, "Clean it up yourself", "C, C++",
             ["fast and light", "touch freed memory again", "and it crashes or leaks"]),
            ("blue", BLUE, "Leave it to a collector", "Python, Java, Go",
             ["fewer mistakes", "but it pauses now and then", "while it cleans"]),
            ("green", GREEN, "Give each value one owner", "Rust",
             ["break the rule", "and it won't compile", "no collector at run time"]),
        ],
        "mem_foot1": "Rust runs this check before the program runs, in the compiler",
        "mem_foot2": "so it is fast and safe, but this rule is where most newcomers get stuck",
        "lay_title": "Python on top, Rust underneath",
        "lay_top": "The Python code you write",
        "lay_code": ["import tiktoken", "from tokenizers import Tokenizer", "from pydantic import BaseModel"],
        "lay_bottom": "Rust running inside",
        "lay_items": [("Tokenising", "tiktoken, tokenizers"), ("Validation", "pydantic-core")],
        "lay_note": ["no Rust needed,", "just import it"],
        "lay_foot": "only the heavy lifting moves to Rust; how you use it stays the same",
    },
}


def d_memory(lang):
    t = TEXT[lang]
    r = R(41); b = []
    W, H = 840, 430
    b.append(T(420, 46, t["mem_title"], 28, INK, weight="bold"))
    b.append(ul(r, 230, 610, 63))
    x = 36
    for wash, col, head, langs, lines in t["cols"]:
        b.append(box(r, x, 84, 248, 236, wash, col, sw=1.7))
        b.append(T(x + 124, 120, head, 21 if lang == "ko" else 19, col, weight="bold"))
        b.append(T(x + 124, 148, langs, 16, INK_LIGHT))
        for i, ln in enumerate(lines):
            b.append(T(x + 124, 200 + i * 32, ln, 17 if lang == "ko" else 16, INK))
        x += 268
    b.append(T(420, 366, t["mem_foot1"], 19, INK))
    b.append(T(420, 400, t["mem_foot2"], 17, INK_LIGHT))
    return W, H, "".join(b)


def d_layers(lang):
    t = TEXT[lang]
    r = R(52); b = []
    W, H = 840, 470
    b.append(T(420, 46, t["lay_title"], 28, INK, weight="bold"))
    b.append(ul(r, 220, 620, 63))

    b.append(box(r, 120, 86, 460, 150, "blue", BLUE, sw=1.7))
    b.append(T(350, 120, t["lay_top"], 21, BLUE, weight="bold"))
    for i, ln in enumerate(t["lay_code"]):
        b.append(T(350, 158 + i * 28, ln, 17, INK))

    b.append(arr(r, 350, 240, 350, 280, INK_LIGHT, 1.6))

    b.append(box(r, 120, 286, 460, 120, "green", GREEN, sw=1.7))
    b.append(T(350, 318, t["lay_bottom"], 21, GREEN, weight="bold"))
    for i, (name, libs) in enumerate(t["lay_items"]):
        bx = 150 + i * 210
        b.append(box(r, bx, 336, 190, 56, None, INK, sw=1.2, amp=1.2))
        b.append(T(bx + 95, 360, name, 17.5, INK, weight="bold"))
        b.append(T(bx + 95, 382, libs, 14.5, INK_LIGHT))

    b.append(T(700, 150, t["lay_note"][0], 17, INK_LIGHT))
    b.append(T(700, 174, t["lay_note"][1], 17, INK_LIGHT))
    b.append(arr(r, 650, 186, 590, 210, INK_LIGHT, 1.3, 8))

    b.append(T(420, 446, t["lay_foot"], 18, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {
    "rust-memory": lambda: d_memory("ko"),
    "rust-memory-en": lambda: d_memory("en"),
    "rust-layers": lambda: d_layers("ko"),
    "rust-layers-en": lambda: d_layers("en"),
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
