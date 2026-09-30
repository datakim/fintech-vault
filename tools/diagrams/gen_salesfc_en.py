#!/usr/bin/env python3
"""영문판: 판매량 예측 시리즈 1·2편 그림 7종."""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap, wobble_line, WASH,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)


def sketch(r, pts, color=INK, sw=1.6, op=1.0, dash=None):
    """점들을 손으로 그은 듯한 선으로."""
    d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f} "
    for (x, y) in pts[1:]:
        d += f"L {x + r.between(-0.6, 0.6):.1f} {y + r.between(-0.6, 0.6):.1f} "
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" opacity="{op}"{da}/>')


def band(r, upper, lower, wash, op=0.9):
    pts = upper + lower[::-1]
    d = f"M {pts[0][0]:.1f} {pts[0][1]:.1f} " + " ".join(
        f"L {x + r.between(-0.8, 0.8):.1f} {y + r.between(-0.8, 0.8):.1f}" for x, y in pts[1:]) + " Z"
    return f'<path d="{d}" fill="{WASH[wash]}" stroke="none" opacity="{op}"/>'


def vline(r, x, y1, y2, color=INK_LIGHT, sw=1.3, dash="5 5"):
    return (f'<path d="{wobble_line(r, x, y1, x, y2, 1.0)}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-dasharray="{dash}" stroke-linecap="round"/>')


# ───────────────────────── 1편 ─────────────────────────

def d_covariates():
    r = R(1201); b = []
    W, H = 900, 470
    b.append(T(450, 46, "What goes into a sales forecast", 28, INK, weight="bold"))
    b.append(ul(r, 290, 610, 63))

    X0, XS, X1 = 300, 590, 860
    b.append(f'<path d="M {XS} 92 L {X1} 92 L {X1} 404 L {XS} 404 Z" fill="{WASH["gray"]}" opacity="0.7"/>')
    b.append(vline(r, XS, 86, 408))
    b.append(T((X0 + XS) / 2, 102, "Past", 16, INK_LIGHT, weight="bold"))
    b.append(T((XS + X1) / 2, 102, "Future (forecast window)", 16, INK_LIGHT, weight="bold"))

    lanes = [
        (150, "Sales", "target", RED),
        (224, "Category · tenure · region", "static covariates", PURPLE),
        (298, "Returns · rating · visits", "known only afterwards", AMBER),
        (372, "Calendar · holidays · planned promos", "known in advance", GREEN),
    ]
    for y, name, kind, col in lanes:
        b.append(T(36, y - 4, name, 12.5, INK, anchor="start", weight="bold"))
        b.append(T(36, y + 16, kind, 12, col, anchor="start"))

    # 매출: 과거만
    pts = [(X0 + i * 8, 150 + 14 * math.sin(i * 0.9) + r.between(-6, 6)) for i in range(int((XS - X0) / 8))]
    b.append(sketch(r, pts, RED, 1.7))
    b.append(T((XS + X1) / 2, 156, "?  this is what we predict", 17, RED, weight="bold"))
    # 정적: 전 구간 상수
    b.append(sketch(r, [(X0, 224), (X1 - 10, 224)], PURPLE, 2.2))
    b.append(T((XS + X1) / 2, 214, "does not change", 13, PURPLE))
    # 반품률: 과거만
    pts = [(X0 + i * 10, 298 + 8 * math.sin(i * 0.5) + r.between(-4, 4)) for i in range(int((XS - X0) / 10))]
    b.append(sketch(r, pts, AMBER, 1.6))
    b.append(T((XS + X1) / 2, 304, "unknown", 15, INK_LIGHT))
    # 프로모션: 전 구간 (스파이크)
    pts = []
    for i in range(int((X1 - 10 - X0) / 6)):
        x = X0 + i * 6
        spike = (i % 23 in (6, 7)) or (i % 31 in (18, 19))
        pts.append((x, 384 - (22 if spike else 0)))
    b.append(sketch(r, pts, GREEN, 1.6))

    b.append(T(450, 440, "In the forecast window, only static covariates and the last row are available", 16.5, INK))
    return W, H, "".join(b)


def d_targets():
    r = R(1202); b = []
    W, H = 900, 500
    b.append(T(450, 46, "What to predict: amount, growth rate, distribution", 26, INK, weight="bold"))
    b.append(ul(r, 230, 670, 63))

    cols = [
        (36, "blue", BLUE, "The amount itself",
         ["plugs straight into the limit", "daily sums up to monthly"],
         ["seller scales differ 1,000×", "trees can't exceed what they saw"]),
        (324, "amber", AMBER, "Growth rate",
         ["scale-free, sellers comparable", "declining sellers stand out"],
         ["undefined when the base is 0", "errors compound over periods"]),
        (612, "green", GREEN, "Distribution (quantiles)",
         ["shows the downside", "separates volatile sellers"],
         ["needs its own evaluation", "daily quantiles don't sum to monthly"]),
    ]
    for x, wash, col, title, pros, cons in cols:
        b.append(box(r, x, 84, 252, 330, wash, col, sw=1.8))
        b.append(T(x + 126, 116, title, 20, col, weight="bold"))
        sx, sy = x + 30, 190
        if title == "The amount itself":
            pts = [(sx + i * 12, sy - i * 2.2 + 12 * math.sin(i * 1.1)) for i in range(12)]
            b.append(sketch(r, pts, INK, 1.6))
            fp = [(pts[-1][0] + i * 12, pts[-1][1] - i * 2.5) for i in range(7)]
            b.append(sketch(r, fp, col, 1.8, dash="6 5"))
        elif title == "Growth rate":
            b.append(sketch(r, [(sx, sy), (sx + 192, sy)], INK_LIGHT, 1.2))
            hs = [14, -8, 20, 6, -22, 10, -6, 16, -12, 8, 18, -4]
            for i, h in enumerate(hs):
                bx = sx + 6 + i * 15.5
                y0, y1 = (sy - h, sy) if h > 0 else (sy, sy - h)
                b.append(box(r, bx, y0, 9, abs(h), None, GREEN if h > 0 else RED, sw=1.1, amp=0.5))
        else:
            up = [(sx + i * 16, sy - 6 - i * 3.2) for i in range(13)]
            lo = [(sx + i * 16, sy + 6 + i * 3.2) for i in range(13)]
            pts = up + lo[::-1]
            d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
            b.append(f'<path d="{d}" fill="{GREEN}" opacity="0.16" stroke="none"/>')
            b.append(sketch(r, up, GREEN, 1.2, 0.8))
            b.append(sketch(r, lo, RED, 1.6))
            b.append(sketch(r, [(sx + i * 16, sy) for i in range(13)], col, 1.8))
            b.append(T(sx + 206, sy - 42, "P90", 11.5, INK_LIGHT))
            b.append(T(sx + 206, sy + 4, "P50", 11.5, INK_LIGHT))
            b.append(T(sx + 206, sy + 50, "P10", 11.5, INK_LIGHT))
        b.append(T(x + 126, 262, "Good", 14, GREEN, weight="bold"))
        for i, ln in enumerate(pros):
            b.append(T(x + 126, 286 + i * 21, ln, 13, INK))
        b.append(T(x + 126, 344, "Trap", 14, RED, weight="bold"))
        for i, ln in enumerate(cons):
            b.append(T(x + 126, 368 + i * 21, ln, 13, INK))

    b.append(box(r, 36, 432, 828, 48, "gray", INK, sw=1.6))
    b.append(T(450, 462, "A common combination: predict the distribution of a normalised amount, then scale back", 16, INK, weight="bold"))
    return W, H, "".join(b)


def d_quantile_limit():
    r = R(1203); b = []
    W, H = 900, 470
    b.append(T(450, 46, "Which quantile should set the limit?", 28, INK, weight="bold"))
    b.append(ul(r, 260, 640, 63))

    X0, XS, X1, Y = 56, 250, 440, 230
    b.append(vline(r, XS, 96, 380))
    b.append(T(150, 104, "past sales", 14, INK_LIGHT))
    b.append(T(350, 104, "next 30 days", 14, INK_LIGHT))
    past = [(X0 + i * 8, Y + 18 * math.sin(i * 0.7) + r.between(-8, 8)) for i in range(25)]
    b.append(sketch(r, past, INK, 1.6))
    n = 12
    up = [(XS + i * 16, Y - 4 - i * 7.5) for i in range(n)]
    lo = [(XS + i * 16, Y + 4 + i * 7.5) for i in range(n)]
    b.append(band(r, up, lo, "green"))
    b.append(sketch(r, [(XS + i * 16, Y) for i in range(n)], GREEN, 2.0))
    b.append(sketch(r, up, GREEN, 1.2, 0.7))
    b.append(sketch(r, lo, RED, 2.0))
    b.append(T(X1 + 8, up[-1][1] + 4, "P90", 13, INK_LIGHT, anchor="start"))
    b.append(T(X1 + 8, Y + 4, "P50", 13, GREEN, anchor="start"))
    b.append(T(X1 + 8, lo[-1][1] + 4, "P10", 13, RED, anchor="start", weight="bold"))
    b.append(T(345, 372, "P10 as the limit basis", 14, RED))

    b.append(box(r, 500, 96, 364, 248, "amber", AMBER, sw=1.9))
    b.append(T(682, 128, "Optimal quantile", 18, AMBER, weight="bold"))
    b.append(T(682, 162, "τ* = under-lending cost ÷ (under + over)", 15, INK, weight="bold"))
    rows = [("over-lending hurts 9× more", "P10"), ("hurts 4× more", "P20"),
            ("hurts the same", "P50")]
    for i, (a, q) in enumerate(rows):
        y = 204 + i * 42
        b.append(box(r, 520, y - 24, 324, 34, None, AMBER, sw=1.1, amp=1.0))
        b.append(T(540, y - 2, a, 14.5, INK, anchor="start"))
        b.append(T(824, y - 2, q, 16, RED if q == "P10" else INK, anchor="end", weight="bold"))
    b.append(T(682, 330, "pinball loss and the newsvendor problem share a formula", 12.5, INK_LIGHT))

    b.append(T(450, 420, "The quantile is set by the cost ratio of over- to under-lending", 17, INK))
    b.append(T(450, 446, "(a simplification assuming linear costs; real default losses arrive all at once past a threshold)", 13, INK_LIGHT))
    return W, H, "".join(b)


# ───────────────────────── 2편 ─────────────────────────

def d_tokenize():
    r = R(1204); b = []
    W, H = 920, 500
    b.append(T(460, 46, "How a time series becomes tokens", 28, INK, weight="bold"))
    b.append(ul(r, 300, 620, 63))

    steps = [
        ("Raw sales", "1,000× scale gaps", "gray", INK_LIGHT),
        ("Standardise + asinh", "tames spikes, keeps zeros", "blue", BLUE),
        ("Add meta features", "value · time index · mask", "purple", PURPLE),
        ("Cut into patches", "one patch = 3P numbers", "amber", AMBER),
        ("Residual MLP", "patch → D-dim token", "green", GREEN),
    ]
    for i, (a, c, wash, col) in enumerate(steps):
        x = 30 + i * 176
        b.append(box(r, x, 90, 160, 84, wash, col, sw=1.7))
        b.append(T(x + 80, 124, a, 16, col, weight="bold"))
        b.append(T(x + 80, 152, c, 11.5, INK))
        if i < 4:
            b.append(arr(r, x + 163, 132, x + 173, 132, INK_LIGHT, 1.3, 6))

    b.append(T(460, 214, "One row of tokens (one series)", 16, INK, weight="bold"))
    x = 60
    for i in range(5):
        b.append(box(r, x, 232, 70, 44, "blue", BLUE, sw=1.3, amp=1.1))
        b.append(T(x + 35, 259, f"past {i+1}", 13, INK))
        x += 78
    b.append(box(r, x, 232, 70, 44, "purple", PURPLE, sw=1.8, amp=1.1))
    b.append(T(x + 35, 259, "REG", 15, PURPLE, weight="bold"))
    x += 78
    for i in range(2):
        b.append(box(r, x, 232, 90, 44, "red", RED, sw=1.6, amp=1.1))
        b.append(T(x + 45, 259, f"future {i+1}", 13, RED, weight="bold"))
        x += 98
    b.append(T(505, 300, "separator between past and future, and an attention sink", 12.5, PURPLE))

    b.append(box(r, 36, 330, 848, 126, "gray", INK, sw=1.6))
    b.append(T(460, 360, "What goes into the future patches", 17, INK, weight="bold"))
    rows = [("Sales (target)", "value 0 · mask 0", "to be predicted", RED),
            ("Known-future covariate (promo)", "actual value · mask 1", "used as a hint", GREEN),
            ("Past-only covariate (returns)", "value 0 · mask 0", "past only", AMBER)]
    for i, (a, b2, c, col) in enumerate(rows):
        y = 390 + i * 24
        b.append(T(80, y, a, 14, col, anchor="start", weight="bold"))
        b.append(T(520, y, b2, 14, INK))
        b.append(T(790, y, c, 13.5, INK_LIGHT))
    b.append(T(460, 484, "The mask alone tells the model which rows are questions and which are hints", 14.5, INK_LIGHT))
    return W, H, "".join(b)


def d_time_group():
    r = R(1205); b = []
    W, H = 920, 566
    b.append(T(460, 46, "Time attention runs across, group attention runs down", 25, INK, weight="bold"))
    b.append(ul(r, 190, 730, 63))

    cols_past, cols_fut = 5, 2
    CW, CH, GAP = 72, 36, 8
    X0 = 214
    def cx(j):
        return X0 + j * (CW + GAP) + (26 if j >= cols_past else 0)
    XS = cx(cols_past) - 17
    b.append(vline(r, XS, 86, 440))
    b.append(T((X0 + XS) / 2, 98, "past patches", 14, INK_LIGHT, weight="bold"))
    b.append(T((XS + cx(cols_past + 1) + CW) / 2 + 6, 98, "future patches", 14, INK_LIGHT, weight="bold"))

    groups = [
        ("Seller A", BLUE, [("Sales", "tgt"), ("Promo", "known"), ("Returns", "past")], 150),
        ("Seller B", AMBER, [("Sales", "tgt"), ("Promo", "known")], 346),
    ]
    for gname, gcol, rows, y0 in groups:
        top = y0 - (34 if gname == "Seller A" else 14)
        gh = len(rows) * (CH + 8) + (y0 - top) + 4
        b.append(box(r, 30, top, 866, gh, None, gcol, sw=1.3, amp=1.0))
        b.append(T(44, y0 + 8, gname, 15, gcol, anchor="start", weight="bold"))
        for i, (name, kind) in enumerate(rows):
            y = y0 + i * (CH + 8)
            b.append(T(196, y + 24, name, 13.5, INK, anchor="end"))
            for j in range(cols_past + cols_fut):
                x = cx(j)
                fut = j >= cols_past
                if not fut:
                    b.append(box(r, x, y, CW, CH, "blue" if kind == "tgt" else ("green" if kind == "known" else "amber"),
                                 INK_LIGHT, sw=1.0, amp=0.8))
                else:
                    if kind == "tgt":
                        b.append(box(r, x, y, CW, CH, "red", RED, sw=1.6, amp=0.9))
                        b.append(T(x + CW / 2, y + 25, "?", 17, RED, weight="bold"))
                    elif kind == "known":
                        b.append(box(r, x, y, CW, CH, "green", GREEN, sw=1.2, amp=0.8))
                        b.append(T(x + CW / 2, y + 23, "known", 11.5, GREEN))
                    else:
                        b.append(box(r, x, y, CW, CH, None, INK_LIGHT, sw=0.9, amp=0.8))
                        b.append(T(x + CW / 2, y + 23, "unknown", 11.5, INK_LIGHT))

    # 타임 어텐션 (셀러 A 매출 줄, 가로)
    ya = 150 - 12
    b.append(arr(r, cx(0) + 10, ya, cx(6) + CW - 10, ya, BLUE, 1.8, 8))
    b.append(arr(r, cx(6) + CW - 10, ya, cx(0) + 10, ya, BLUE, 1.8, 8))
    # 그룹 어텐션 (첫 미래 패치 열, 세로)
    xg = cx(5) + CW + 4
    b.append(arr(r, xg, 150 + 4, xg, 150 + 2 * (CH + 8) + CH - 4, PURPLE, 2.0, 8))
    b.append(arr(r, xg, 150 + 2 * (CH + 8) + CH - 4, xg, 150 + 4, PURPLE, 2.0, 8))
    # 그룹 사이 차단
    b.append(T(xg, 314, "✕", 22, RED, weight="bold"))
    b.append(T(xg + 14, 316, "blocked across groups", 12.5, RED, anchor="start"))

    b.append(box(r, 30, 452, 424, 58, "blue", BLUE, sw=1.5))
    b.append(T(242, 478, "Time attention", 16, BLUE, weight="bold"))
    b.append(T(242, 499, "across patches within one series; RoPE gives position", 12.5, INK))
    b.append(box(r, 472, 452, 424, 58, "purple", PURPLE, sw=1.5))
    b.append(T(684, 478, "Group attention", 16, PURPLE, weight="bold"))
    b.append(T(684, 499, "same group, same patch position; no order, so no positional encoding", 12, INK))
    b.append(T(460, 544, "Stacked in turn, last year's promo patch can reach this year's sales patch", 14.5, INK_LIGHT))
    return W, H, "".join(b)


def d_group_mask():
    r = R(1206); b = []
    W, H = 900, 480
    b.append(T(450, 46, "Group IDs become the mask", 28, INK, weight="bold"))
    b.append(ul(r, 300, 600, 63))

    ids = [0, 0, 0, 1, 1]
    names = ["A sales", "A promo", "A returns", "B sales", "B promo"]
    b.append(T(210, 100, "group_ids = [0, 0, 0, 1, 1]", 16, INK, weight="bold"))
    C = 44; MX, MY = 150, 150
    for i in range(5):
        b.append(T(MX - 8, MY + i * C + 27, names[i], 12, INK, anchor="end"))
        b.append(T(MX + i * C + C / 2, MY - 10, str(ids[i]), 13, INK_LIGHT))
        for j in range(5):
            ok = ids[i] == ids[j]
            wash = ("blue" if ids[i] == 0 else "amber") if ok else None
            b.append(box(r, MX + j * C, MY + i * C, C - 4, C - 4, wash,
                         (BLUE if ids[i] == 0 else AMBER) if ok else INK_LIGHT, sw=1.1 if ok else 0.8, amp=0.6))
            if not ok:
                b.append(T(MX + j * C + C / 2 - 2, MY + i * C + 26, "✕", 12, INK_LIGHT))
    b.append(T(260, 390, "only shaded cells attend to each other (block diagonal)", 12.5, INK))
    b.append(T(260, 412, "groups of any size share one batch, no padding", 12.5, INK_LIGHT))

    b.append(box(r, 470, 90, 394, 322, "gray", INK, sw=1.7))
    b.append(T(667, 120, "Attention pairs (N = 52 patches)", 16, INK, weight="bold"))
    blocks = [
        ("V=10  sales + 9 covariates", "270,400", "32,240", "8×"),
        ("V=50  one seller's 50 products", "6,760,000", "265,200", "25×"),
    ]
    for k, (title, full, split, ratio) in enumerate(blocks):
        y = 160 + k * 124
        b.append(T(490, y, title, 14.5, INK, anchor="start", weight="bold"))
        b.append(T(500, y + 30, "flatten, attend to all", 13.5, INK_LIGHT, anchor="start"))
        b.append(T(844, y + 30, full, 15, RED, anchor="end", weight="bold"))
        b.append(T(500, y + 58, "split into time + group", 13.5, INK_LIGHT, anchor="start"))
        b.append(T(844, y + 58, split, 15, GREEN, anchor="end", weight="bold"))
        b.append(T(844, y + 84, f"about {ratio} fewer", 13, GREEN, anchor="end"))
    b.append(T(667, 402, "full (V·N)²  vs  V·N² + N·V²", 13, INK_LIGHT))

    b.append(T(450, 456, "The more variables, the more the split wins (the same idea as axial attention)", 15, INK))
    return W, H, "".join(b)


def d_quantile_sum():
    r = R(1207); b = []
    W, H = 900, 480
    b.append(T(450, 46, "Summing daily P10s does not give the 30-day P10", 26, INK, weight="bold"))
    b.append(ul(r, 230, 670, 63))

    data = [(0.0, 13.9, 30.6, '-55%'), (0.5, 13.9, 27.6, '-50%'), (0.8, 13.9, 23.0, '-40%'), (0.95, 13.9, 17.2, '-20%')]
    base, top, vmax = 380, 110, 35.0
    def yv(v): return base - (base - top) * v / vmax
    b.append(sketch(r, [(90, base), (860, base)], INK, 1.4))
    for v in (10, 20, 30):
        b.append(sketch(r, [(90, yv(v)), (860, yv(v))], INK_LIGHT, 0.8, 0.4, dash="3 6"))
        b.append(T(82, yv(v) + 4, f"{v}M", 12, INK_LIGHT, anchor="end"))
    for k, (rho, s, t, pct) in enumerate(data):
        gx = 130 + k * 186
        b.append(box(r, gx, yv(s), 60, base - yv(s), "red", RED, sw=1.4, amp=0.8))
        b.append(T(gx + 30, yv(s) - 8, f"{s}M", 13, RED, weight="bold"))
        b.append(box(r, gx + 70, yv(t), 60, base - yv(t), "green", GREEN, sw=1.4, amp=0.8))
        b.append(T(gx + 100, yv(t) - 8, f"{t}M", 13, GREEN, weight="bold"))
        b.append(T(gx + 65, base + 24, f"ρ = {rho}", 14, INK, weight="bold"))
        b.append(T(gx + 65, base + 44, pct.replace("-", "−"), 13.5, RED))
    b.append(box(r, 640, 96, 18, 14, "red", RED, sw=1.0, amp=0.5))
    b.append(T(664, 108, "daily P10 summed over 30 days", 13, INK, anchor="start"))
    b.append(box(r, 640, 120, 18, 14, "green", GREEN, sw=1.0, amp=0.5))
    b.append(T(664, 132, "true P10 of the 30-day total", 13, INK, anchor="start"))

    b.append(T(450, 458, "median daily sales KRW 1M, log volatility 0.6, 200,000 simulations per day-to-day correlation ρ", 13, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {
    "sf-covariates-en": d_covariates,
    "sf-targets-en": d_targets,
    "sf-quantile-limit-en": d_quantile_limit,
    "tst-tokenize-en": d_tokenize,
    "tst-time-group-en": d_time_group,
    "tst-group-mask-en": d_group_mask,
    "tst-quantile-sum-en": d_quantile_sum,
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
