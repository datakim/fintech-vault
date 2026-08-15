#!/usr/bin/env python3
"""영문판: 월드모델 3부작 — 그림 7종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap, wobble_line,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


# ── 1편: 비디오 월드모델의 입출력
def d_wm_io():
    r = R(801); b = []
    W, H = 900, 400
    b.append(T(450, 46, "How a video world model takes input and gives output", 25, INK, weight="bold"))
    b.append(ul(r, 230, 670, 63))

    b.append(box(r, 40, 88, 230, 190, "blue", BLUE, sw=1.7))
    b.append(T(155, 116, "Conditioning signals", 17, BLUE, weight="bold"))
    for i, (name, sub) in enumerate([("a starting image", None),
                                     ("a text prompt", None),
                                     ("player input", "move forward, turn the camera")]):
        y = 150 + i * 44
        b.append(T(155, y, name, 15.5, INK))
        if sub:
            b.append(T(155, y + 19, sub, 12, INK_LIGHT))
    b.append(arr(r, 274, 180, 314, 180, INK_LIGHT, 1.6))

    b.append(box(r, 318, 132, 264, 96, "amber", AMBER, sw=1.9))
    b.append(T(450, 168, "Video world model", 19, AMBER, weight="bold"))
    b.append(T(450, 196, "\"what scene should come next?\"", 14, INK))
    b.append(arr(r, 586, 180, 626, 180, INK_LIGHT, 1.6))

    b.append(box(r, 630, 132, 230, 96, "green", GREEN, sw=1.7))
    b.append(T(745, 168, "the next frame", 17, GREEN, weight="bold"))
    b.append(T(745, 196, "generated one at a time", 13.5, INK))

    b.append(f'<path d="{wobble_line(r, 745, 232, 745, 292, 2)}" fill="none" stroke="{INK_LIGHT}" stroke-width="1.5" stroke-linecap="round"/>')
    b.append(arr(r, 745, 292, 450, 292, INK_LIGHT, 1.5))
    b.append(f'<path d="{wobble_line(r, 450, 292, 450, 234, 2)}" fill="none" stroke="{INK_LIGHT}" stroke-width="1.5" stroke-linecap="round"/>')
    b.append(T(598, 316, "the frame just made becomes input to the next one", 15, INK))

    b.append(T(450, 370, "The basic shape: take conditioning signals, predict frames one at a time", 17, INK_LIGHT))
    return W, H, "".join(b)


# ── 1편: 기억하지 못하는 세계
def d_wm_no_memory():
    r = R(802); b = []
    W, H = 900, 386
    b.append(T(450, 46, "Turn the camera away and back, and the world has changed", 24, INK, weight="bold"))
    b.append(ul(r, 220, 680, 63))

    panels = [
        (40, "blue", BLUE, "① a bottle on the table", "the model renders it fine", None),
        (325, "gray", INK_LIGHT, "② the camera turns away", "the bottle leaves the frame", None),
        (610, "red", RED, "③ turn back — and?", "nothing guarantees it is still there", "?"),
    ]
    for x, wash, col, title, sub, mark in panels:
        b.append(box(r, x, 84, 250, 140, wash, col, sw=1.8))
        b.append(T(x + 125, 114, title, 16.5, col, weight="bold"))
        if mark:
            b.append(T(x + 125, 176, mark, 40, RED, weight="bold"))
        b.append(T(x + 125, 206, sub, 13, INK))
        if x < 610:
            b.append(arr(r, x + 256, 154, x + 278, 154, INK_LIGHT, 1.5, 8))

    b.append(box(r, 40, 248, 820, 76, "amber", AMBER, sw=1.8))
    b.append(T(450, 278, "The model does not remember a scene — it regenerates it every time", 19, INK, weight="bold"))
    b.append(T(450, 306, "\"When the character turns back, is the world the same? In most video models, no.\" — Anupam Singh", 14, INK_LIGHT))

    b.append(T(450, 362, "The persistence problem: whatever leaves the frame can quietly change", 17, INK_LIGHT))
    return W, H, "".join(b)


# ── 2편: 게임의 두 가지 일
def d_game_two_jobs():
    r = R(803); b = []
    W, H = 900, 430
    b.append(T(450, 46, "The two jobs that make a game a game", 27, INK, weight="bold"))
    b.append(ul(r, 240, 660, 63))

    b.append(box(r, 36, 84, 400, 236, "blue", BLUE, sw=1.9))
    b.append(T(236, 116, "① Keeping the world consistent", 18, BLUE, weight="bold"))
    for i, ln in enumerate(["persistent state — come back and it is still there",
                            "rules — applied the same way for everyone",
                            "physics — things move, collide and fall as expected",
                            "real-time sync — thousands share one world",
                            "immediacy — the world reacts the moment you act"]):
        b.append(T(236, 152 + i * 34, ln, 13.5, INK))

    b.append(box(r, 464, 84, 400, 236, "amber", AMBER, sw=1.9))
    b.append(T(664, 116, "② Making it look real", 18, AMBER, weight="bold"))
    for i, ln in enumerate(["grass moving in the wind",
                            "dust behind a car, smoke off a fire",
                            "light shifting across a surface"]):
        b.append(T(664, 152 + i * 34, ln, 13.5, INK))
    b.append(T(664, 268, "the level of realism players now", 13.5, INK))
    b.append(T(664, 292, "simply take for granted", 13.5, INK))

    b.append(T(450, 358, "Game engines are strong at ①, world models at ② — and nobody has done both cheaply", 17.5, INK))
    b.append(T(450, 398, "Graphics are the visible part; what makes a game a game is the system you cannot see", 16, INK_LIGHT))
    return W, H, "".join(b)


# ── 2편: Roblox Reality 세 구성요소
def d_roblox_reality():
    r = R(804); b = []
    W, H = 900, 452
    b.append(T(450, 46, "The three pieces of Roblox Reality", 27, INK, weight="bold"))
    b.append(ul(r, 250, 650, 63))

    b.append(box(r, 36, 84, 350, 150, "blue", BLUE, sw=1.9))
    b.append(T(211, 114, "Game engine — \"what exists\"", 16, BLUE, weight="bold"))
    for i, ln in enumerate(["the data model: a ledger of every object",
                            "(a car's position, speed, heading, material)",
                            "physics and rules recomputed identically",
                            "→ the source of truth"]):
        b.append(T(211, 144 + i * 22, ln, 12.5, INK if i < 3 else INK_LIGHT))

    b.append(box(r, 514, 84, 350, 150, "amber", AMBER, sw=1.9))
    b.append(T(689, 114, "Super Upsampler — \"how it looks\"", 15, AMBER, weight="bold"))
    for i, ln in enumerate(["takes the engine's flat draft frame",
                            "and adds texture, lighting and detail",
                            "until it is photoreal",
                            "→ it never decides what is in the scene"]):
        b.append(T(689, 144 + i * 22, ln, 12.5, INK if i < 3 else INK_LIGHT))

    b.append(arr(r, 392, 152, 508, 152, INK_LIGHT, 1.6))
    b.append(T(450, 138, "draft frame", 12.5, INK_LIGHT))
    b.append(T(450, 176, "+ conditioning", 12.5, INK_LIGHT))

    b.append(box(r, 36, 254, 828, 112, "green", GREEN, sw=1.9))
    b.append(T(450, 286, "Roblox cloud — the base that runs all of this at scale", 18, GREEN, weight="bold"))
    b.append(T(450, 316, "persists each world's state (come back days later and the game is intact) · runs millions of sessions near the player", 13, INK))
    b.append(T(450, 342, "authoritative state has to sit beside the player for fast, fair multiplayer", 13, INK))

    b.append(T(450, 410, "The engine and the cloud hold consistency; the world model handles realism", 18, INK))
    return W, H, "".join(b)


# ── 2편: 세 종류의 조건 신호
def d_upsampler_signals():
    r = R(805); b = []
    W, H = 920, 500
    b.append(T(460, 46, "The three kinds of conditioning signal", 27, INK, weight="bold"))
    b.append(ul(r, 250, 670, 63))

    sigs = [
        (86, "blue", BLUE, "① Dense — a value at every pixel",
         ["a roughly rendered frame + a depth map (distance per pixel)",
          "same grid as the output → concatenated, or injected ControlNet-style",
          "→ every pixel is pinned to its position and colour"]),
        (212, "green", GREEN, "② Global — one setting for the whole scene",
         ["midday, light rain, sun low on the left",
          "scales and shifts the model's activations (modulation)",
          "→ changes the mood of the entire frame at once"]),
        (338, "amber", AMBER, "③ Structured — description, close to text",
         ["\"metallic sports car, position (120, 0, 48), 40 m/s\" + a style prompt",
          "injected through cross-attention",
          "→ any part of the frame can consult it when needed"]),
    ]
    for y, wash, col, title, lines in sigs:
        b.append(box(r, 36, y, 560, 106, wash, col, sw=1.7))
        b.append(T(316, y + 30, title, 16, col, weight="bold"))
        for i, ln in enumerate(lines):
            b.append(T(316, y + 56 + i * 21, ln, 12, INK if i < 2 else INK_LIGHT))
        b.append(arr(r, 600, y + 53, 646, 224, INK_LIGHT, 1.3, 7))

    b.append(box(r, 650, 186, 150, 76, "purple", PURPLE, sw=1.9))
    b.append(T(725, 216, "Super", 17, PURPLE, weight="bold"))
    b.append(T(725, 240, "Upsampler", 17, PURPLE, weight="bold"))
    b.append(arr(r, 804, 224, 838, 224, INK_LIGHT, 1.5))
    b.append(T(872, 218, "2K", 15, INK, weight="bold"))
    b.append(T(872, 240, "final frame", 12.5, INK_LIGHT))

    b.append(T(460, 482, "The model never moves the car or changes a distance — it only paints realism onto a fixed scene", 16.5, INK))
    return W, H, "".join(b)


# ── 3편: self-forcing
def d_self_forcing():
    r = R(806); b = []
    W, H = 900, 430
    b.append(T(450, 46, "Offline generation vs self-forcing", 27, INK, weight="bold"))
    b.append(ul(r, 250, 650, 63))

    b.append(box(r, 36, 84, 828, 120, "red", RED, sw=1.8))
    b.append(T(150, 114, "The old way — offline generation", 16.5, RED, weight="bold"))
    b.append(box(r, 300, 100, 380, 76, None, RED, sw=1.3, amp=1.2))
    b.append(T(490, 130, "the whole clip computed at once, moving back", 13, INK))
    b.append(T(490, 152, "and forth along the time axis", 13, INK))
    b.append(T(490, 170, "nothing is visible until it finishes", 12, INK_LIGHT))
    b.append(T(780, 130, "seconds per clip", 14, RED, weight="bold"))
    b.append(T(780, 152, "unusable in a game", 12.5, INK_LIGHT))

    b.append(box(r, 36, 224, 828, 132, "green", GREEN, sw=1.8))
    b.append(T(150, 254, "Self-forcing — autoregressive", 16.5, GREEN, weight="bold"))
    for i, name in enumerate(["frame 1", "frame 2", "frame 3"]):
        x = 300 + i * 118
        b.append(box(r, x, 244, 104, 44, None, GREEN, sw=1.3, amp=1.2))
        b.append(T(x + 52, 271, name, 14, INK))
        b.append(arr(r, x + 108, 266, x + 116, 266, INK_LIGHT, 1.2, 5))
    b.append(T(672, 271, "…", 20, INK_LIGHT))
    b.append(T(780, 258, "~30ms per frame", 14, GREEN, weight="bold"))
    b.append(T(780, 280, "real-time target", 12.5, INK_LIGHT))
    b.append(T(490, 320, "each frame is generated straight away, conditioned on the frames just made → streamable", 12.5, INK))

    b.append(T(450, 388, "Latency levers used together: smaller models · KV cache compression · H200/B200 GPUs at edge data centres · placed beside the engine", 13.5, INK_LIGHT))
    b.append(T(450, 412, "The fight is to turn seconds into tens of milliseconds, network round trip included", 14, INK_LIGHT))
    return W, H, "".join(b)


# ── 3편: 네 가지 난제
def d_four_problems():
    r = R(807); b = []
    W, H = 900, 512
    b.append(T(450, 46, "Four hard problems between design and production", 26, INK, weight="bold"))
    b.append(ul(r, 220, 680, 63))

    probs = [
        (36, 84, "red", RED, "① Latency",
         ["seconds per clip → ~30ms per frame",
          "click and wait seconds, and it is not a game"],
         ["fix: self-forcing, smaller models,", "KV cache compression, edge GPUs"]),
        (464, 84, "amber", AMBER, "② Consistency",
         ["small errors accumulate and the world drifts",
          "it has to hold for minutes, not frames"],
         ["fix: pinned by the data model + longer context", "(what was generated ten minutes ago conditions now)"]),
        (36, 274, "blue", BLUE, "③ Multiplayer",
         ["drawing a crowd ≠ running 20,000 states",
          "my action must appear on everyone's screen"],
         ["fix: the server decides truth, each client", "generates only its view, prediction runs locally"]),
        (464, 274, "green", GREEN, "④ Creator control",
         ["fun comes from rules, not from graphics",
          "a generated world still obeys the creator"],
         ["fix: the game cartridge harness —", "wrap the model in deterministic game logic"]),
    ]
    for x, y, wash, col, title, lines, fix in probs:
        b.append(box(r, x, y, 400, 172, wash, col, sw=1.9))
        b.append(T(x + 200, y + 32, title, 18, col, weight="bold"))
        for i, ln in enumerate(lines):
            b.append(T(x + 200, y + 62 + i * 24, ln, 13.5, INK))
        b.append(box(r, x + 26, y + 116, 348, 44, None, col, sw=1.1, amp=1.0))
        b.append(T(x + 200, y + 136, fix[0], 12, INK_LIGHT))
        b.append(T(x + 200, y + 152, fix[1], 12, INK_LIGHT))

    b.append(T(450, 486, "A game demands all four at once, at the harshest settings", 18, INK))
    return W, H, "".join(b)


DIAGRAMS = {
    "wm-io-en": d_wm_io,
    "wm-no-memory-en": d_wm_no_memory,
    "game-two-jobs-en": d_game_two_jobs,
    "roblox-reality-en": d_roblox_reality,
    "upsampler-signals-en": d_upsampler_signals,
    "self-forcing-en": d_self_forcing,
    "wm-four-problems-en": d_four_problems,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
