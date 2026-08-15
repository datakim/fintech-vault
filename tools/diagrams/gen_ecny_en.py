#!/usr/bin/env python3
"""영문판: e-CNY 한 장 정리."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap, wobble_line,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


def d_onepager():
    r = R(611); b = []
    W, H = 940, 806
    b.append(T(470, 50, "e-CNY on one page", 30, INK, weight="bold"))
    b.append(T(470, 84, "China's central bank digital currency, and what changed in 2026", 18, INK_LIGHT))
    b.append(ul(r, 320, 620, 66))

    # 1. 무엇인가
    b.append(box(r, 36, 112, 868, 128, "gray", INK_LIGHT, sw=1.7))
    b.append(T(62, 142, "1", 24, RED, anchor="start", weight="bold"))
    b.append(T(86, 142, "What it is", 20, INK, anchor="start", weight="bold"))
    for i, ln in enumerate(["a digital yuan issued by the People's Bank of China",
                            "not a cryptocurrency — state-managed legal tender",
                            "spendable through apps, bank wallets and institutions"]):
        b.append(T(86, 170 + i * 22, "· " + ln, 14.5, INK_LIGHT, anchor="start"))

    chain = ["Central bank", "Banks & PSPs", "User wallet", "Merchants"]
    x = 470
    for i, name in enumerate(chain):
        b.append(box(r, x, 148, 96, 44, None, INK_LIGHT, sw=1.2, amp=1.1))
        b.append(T(x + 48, 175, name, 12.5, INK))
        if i < 3:
            b.append(arr(r, x + 98, 170, x + 106, 170, INK_LIGHT, 1.2, 5))
        x += 106
    b.append(T(682, 218, "issued at the top, distributed through banks, spent at the bottom", 13.5, INK_LIGHT))

    # 2. 어떻게 작동하나
    b.append(box(r, 36, 254, 868, 122, "blue", BLUE, sw=1.7))
    b.append(T(62, 284, "2", 24, BLUE, anchor="start", weight="bold"))
    b.append(T(86, 284, "How it works", 20, INK, anchor="start", weight="bold"))
    feats = [
        (300, "Two-tier structure", "central bank → banks → users"),
        (540, "QR · NFC · offline", "works without a network"),
        (760, "Conditional payment", "smart-contract disbursement"),
    ]
    for cx, name, desc in feats:
        b.append(box(r, cx - 108, 296, 216, 62, None, BLUE, sw=1.2, amp=1.1))
        b.append(T(cx, 320, name, 15.5, BLUE, weight="bold"))
        b.append(T(cx, 342, desc, 13, INK))
    b.append(T(150, 340, "the money itself is", 14, INK_LIGHT))
    b.append(T(150, 360, "central bank money", 14, INK_LIGHT))

    # 3. 2026년에 바뀐 점
    b.append(box(r, 36, 390, 868, 172, "red", RED, sw=1.9))
    b.append(T(62, 420, "3", 24, RED, anchor="start", weight="bold"))
    b.append(T(86, 420, "What changed in 2026", 20, RED, anchor="start", weight="bold"))
    b.append(T(86, 444, "from digital cash to digital deposit money", 14.5, INK_LIGHT, anchor="start"))
    changes = [
        (52, "①", "Cash → deposit-like", "past the payment pilot,", "into the institutional stage"),
        (270, "②", "Interest on balances", "tiers 1·2·3 named wallets,", "currently about 0.05% a year"),
        (488, "③", "Deposit insurance", "bank wallet balances protected", "like ordinary deposits"),
        (706, "④", "Reserve requirements", "balances at banks count", "toward reserve calculations"),
    ]
    for x, num, title, l1, l2 in changes:
        b.append(box(r, x, 458, 202, 78, None, RED, sw=1.3, amp=1.2))
        b.append(T(x + 101, 480, num + "  " + title, 14.5, RED, weight="bold"))
        b.append(T(x + 101, 502, l1, 12, INK))
        b.append(T(x + 101, 522, l2, 12, INK))
    b.append(T(470, 552, "!  tier-4 anonymous wallets earn no interest", 15, RED, weight="bold"))

    # 4. 어디에 쓰나
    b.append(box(r, 36, 576, 868, 122, "green", GREEN, sw=1.7))
    b.append(T(62, 606, "4", 24, GREEN, anchor="start", weight="bold"))
    b.append(T(86, 606, "Where people use it", 20, INK, anchor="start", weight="bold"))
    uses = [
        (300, "Everyday payments", "shops, buses, metro, retail"),
        (540, "Subsidies & coupons", "red packets, consumption vouchers"),
        (760, "Prepaid protection", "gyms, salons, tuition"),
    ]
    for cx, name, desc in uses:
        b.append(box(r, cx - 108, 618, 216, 62, None, GREEN, sw=1.2, amp=1.1))
        b.append(T(cx, 642, name, 15.5, GREEN, weight="bold"))
        b.append(T(cx, 664, desc, 12.5, INK))
    b.append(T(150, 662, "policy uses lead;", 14, INK_LIGHT))
    b.append(T(150, 682, "daily use is uneven", 14, INK_LIGHT))

    # 5. 숫자
    b.append(box(r, 36, 712, 868, 74, "amber", AMBER, sw=1.8))
    b.append(T(120, 742, "As of end-Nov 2025", 16, AMBER, anchor="start", weight="bold"))
    nums = [(420, "3.48B", "cumulative transactions"),
            (620, "¥16.7T", "cumulative value"),
            (810, "230M", "personal wallets")]
    for cx, value, label in nums:
        b.append(T(cx, 744, value, 22, INK, weight="bold"))
        b.append(T(cx, 768, label, 13, INK_LIGHT))
    b.append(T(120, 768, "cumulative, not annual", 13, INK_LIGHT, anchor="start"))
    return W, H, "".join(b)


DIAGRAMS = {"ecny-onepager-en": d_onepager}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
