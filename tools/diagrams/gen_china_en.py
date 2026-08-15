#!/usr/bin/env python3
"""영문판: 중국 핀테크 3층 구조 한 장 정리."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap, wobble_line,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


def d_stack():
    r = R(511); b = []
    W, H = 940, 758
    b.append(T(470, 50, "How Chinese fintech actually works", 30, INK, weight="bold"))
    b.append(T(470, 84, "The triangle of super apps, mini programs and payment infrastructure", 18, INK_LIGHT))
    b.append(ul(r, 250, 690, 66))

    CX = 346

    # ① 슈퍼앱
    b.append(box(r, 36, 118, 620, 152, "red", RED, sw=1.9))
    b.append(T(CX, 148, "①  User touchpoint   |   Super Apps", 20, RED, weight="bold"))
    apps = [
        (60, "WeChat", ["messenger · social", "mini programs · transfers"]),
        (352, "Alipay", ["payments · finance", "daily & public services"]),
    ]
    for x, name, lines in apps:
        b.append(box(r, x, 160, 280, 76, None, RED, sw=1.3, amp=1.2))
        b.append(T(x + 140, 184, name, 18, INK, weight="bold"))
        b.append(T(x + 140, 206, lines[0], 13.5, INK_LIGHT))
        b.append(T(x + 140, 226, lines[1], 13.5, INK_LIGHT))
    b.append(T(CX, 258, "the entrance where users stay", 15, INK_LIGHT))

    b.append(arr(r, CX, 274, CX, 296, RED, 2.2, 10))

    # ② 미니프로그램
    b.append(box(r, 36, 300, 620, 172, "green", GREEN, sw=1.9))
    b.append(T(CX, 330, "②  Service layer   |   Mini Programs", 20, GREEN, weight="bold"))
    tiles = ["Retail", "Food", "Mobility", "Healthcare",
             "Government", "Gaming", "Insurance", "Lending"]
    for i, name in enumerate(tiles):
        x = 60 + (i % 4) * 148
        y = 344 + (i // 4) * 52
        b.append(box(r, x, y, 136, 40, None, GREEN, sw=1.2, amp=1.1))
        b.append(T(x + 68, y + 26, name, 15, INK))
    b.append(T(CX, 460, "small services that run without installing an app", 15, INK_LIGHT))

    b.append(arr(r, CX, 476, CX, 498, GREEN, 2.2, 10))

    # ③ 결제·청산
    b.append(box(r, 36, 502, 620, 148, "blue", BLUE, sw=1.9))
    b.append(T(CX, 532, "③  Payments & Clearing", 20, BLUE, weight="bold"))
    rails = ["WeChat Pay", "Alipay", "NetsUnion", "Bank accounts", "POS / IoT", "e-CNY"]
    for i, name in enumerate(rails):
        x = 56 + i * 98
        b.append(box(r, x, 548, 90, 42, None, BLUE, sw=1.2, amp=1.1))
        b.append(T(x + 45, 574, name, 12.5, INK))
        if i < 5:
            b.append(arr(r, x + 92, 569, x + 100, 569, INK_LIGHT, 1.2, 5))
    b.append(T(CX, 622, "where money actually moves and gets settled", 15, INK_LIGHT))

    # 사이드 스냅샷
    b.append(box(r, 686, 118, 218, 532, "amber", AMBER, sw=1.8))
    b.append(T(795, 152, "2025 snapshot", 19, AMBER, weight="bold"))
    snap = [
        ("Fintech market", "US$51.3B"),
        ("WeChat MAU", "1.4B+"),
        ("NetsUnion", "1T+ / year"),
        ("Daily clearing", "3.2B+ txns"),
    ]
    for i, (label, value) in enumerate(snap):
        y0 = 206 + i * 112
        b.append(T(795, y0, label, 14.5, INK))
        b.append(T(795, y0 + 32, value, 21, AMBER, weight="bold"))
        if i < 3:
            b.append(f'<path d="{wobble_line(r, 712, y0 + 62, 878, y0 + 62, 1.2)}" fill="none" '
                     f'stroke="{AMBER}" stroke-width="1.1" stroke-linecap="round" opacity="0.45"/>')

    # 하단 요약
    b.append(box(r, 36, 668, 868, 68, "gray", INK, sw=1.8))
    b.append(T(470, 696, "Users stay in the super app, services arrive as mini programs,", 18, INK, weight="bold"))
    b.append(T(470, 720, "and payment and clearing are handled on national infrastructure.", 18, INK, weight="bold"))
    return W, H, "".join(b)


DIAGRAMS = {"china-fintech-stack-en": d_stack}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
