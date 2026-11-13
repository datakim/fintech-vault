"""카드형 다이어그램 스타일 (2026-11-13 추가).

크림색 바탕, 점선으로 묶은 영역(layer), 파스텔 채움에 진한 윤곽선을 두른 둥근 카드,
카드마다 선 아이콘, 굵은 제목과 작은 설명, 알약 모양 칩. 선은 아주 조금만 흔들어
손으로 그린 느낌만 남긴다. 글씨는 Gaegu(Regular·Bold)를 __CARDFONT__ 자리에 embed_fonts.py가 심는다.
"""
import math
from style import R, esc

BG = "#F7F2E8"
INK = "#2E2A26"
SOFT = "#5A534B"
MUTED = "#8A8277"
ORANGE = "#E07A4F"
ORANGE_DARK = "#6B3A24"

FILL = {
    "green": "#D9EBD2", "blue": "#D6E5F4", "purple": "#E5DBF3", "peach": "#F9DAC6",
    "red": "#F6D3CB", "yellow": "#F8EBC4", "gray": "#ECE6DA", "white": "#FFFDF8",
}
EDGE = {"peach": "#EDB08F", "green": "#9DC895", "red": "#E3A193"}


def text_w(s, size):
    """Gaegu 글자 폭 대략치 (한글 0.82em, 공백 0.42em)."""
    w = 0.0
    for ch in s:
        if "\uac00" <= ch <= "\ud7a3":
            w += 0.82
        elif ch == " ":
            w += 0.42
        elif ch.isdigit() or ch == "%":
            w += 0.6
        elif ch.isupper():
            w += 0.56
        elif ch in ",.()/:'":
            w += 0.38
        else:
            w += 0.49
    return w * size


# Gaegu에는 가운뎃점(·)과 화살표가 없어서 쉼표로 바꿔 쓴다
def _clean(s):
    return s.replace(" · ", ", ").replace("·", ", ")


def T(x, y, s, size=16, fill=INK, anchor="middle", weight="normal", opacity=1.0):
    a = f' text-anchor="{anchor}"' if anchor else ""
    w = ' font-weight="700"' if weight == "bold" else ""
    o = f' opacity="{opacity}"' if opacity != 1.0 else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}"{a} fill="{fill}"{w}{o}>{esc(_clean(s))}</text>'


def rrect(r, x, y, w, h, rad=12, amp=0.7):
    """살짝 흔들린 둥근 사각형 경로."""
    j = lambda: r.between(-amp, amp)
    x1, y1, x2, y2 = x + j(), y + j(), x + w + j(), y + h + j()
    rad = min(rad, w / 2, h / 2)
    return (f"M {x1 + rad:.1f} {y1:.1f} "
            f"Q {(x1 + x2) / 2:.1f} {y1 + j():.1f} {x2 - rad:.1f} {y1 + j() * 0.3:.1f} "
            f"Q {x2:.1f} {y1:.1f} {x2:.1f} {y1 + rad:.1f} "
            f"Q {x2 + j():.1f} {(y1 + y2) / 2:.1f} {x2:.1f} {y2 - rad:.1f} "
            f"Q {x2:.1f} {y2:.1f} {x2 - rad:.1f} {y2:.1f} "
            f"Q {(x1 + x2) / 2:.1f} {y2 + j():.1f} {x1 + rad:.1f} {y2:.1f} "
            f"Q {x1:.1f} {y2:.1f} {x1:.1f} {y2 - rad:.1f} "
            f"Q {x1 + j():.1f} {(y1 + y2) / 2:.1f} {x1:.1f} {y1 + rad:.1f} "
            f"Q {x1:.1f} {y1:.1f} {x1 + rad:.1f} {y1:.1f} Z")


def shape(r, x, y, w, h, fill=None, stroke=INK, sw=2.0, rad=12, dash=None, amp=0.7, op=1.0):
    f = FILL.get(fill, fill) if fill else "none"
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{op}"' if op != 1.0 else ""
    return (f'<path d="{rrect(r, x, y, w, h, rad, amp)}" fill="{f}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"{d}{o}/>')


def layer(r, x, y, w, h, label, size=19):
    """점선으로 묶은 영역과 위쪽 가운데 이름표."""
    return (shape(r, x, y, w, h, None, INK, 1.6, 18, "7 6", 0.5)
            + T(x + w / 2, y + 32, label, size, INK, weight="bold"))


# ── 선 아이콘 (s 크기 정사각형 안, 왼쪽 위가 x, y)
def _g(body, sw=1.9):
    return (f'<g fill="none" stroke="{INK}" stroke-width="{sw}" stroke-linecap="round" '
            f'stroke-linejoin="round">{body}</g>')


def icon(kind, x, y, s=28):
    k = s / 24.0
    P = lambda px, py: f"{x + px * k:.1f} {y + py * k:.1f}"
    if kind == "chat":
        b = (f'<path d="M {P(3, 5)} Q {P(3, 3)} {P(5, 3)} L {P(19, 3)} Q {P(21, 3)} {P(21, 5)} '
             f'L {P(21, 14)} Q {P(21, 16)} {P(19, 16)} L {P(10, 16)} L {P(5, 20)} L {P(6, 16)} '
             f'L {P(5, 16)} Q {P(3, 16)} {P(3, 14)} Z"/>'
             f'<path d="M {P(7, 8)} L {P(17, 8)} M {P(7, 11.5)} L {P(14, 11.5)}"/>')
    elif kind == "clock":
        b = (f'<circle cx="{x + 12 * k:.1f}" cy="{y + 12 * k:.1f}" r="{9 * k:.1f}"/>'
             f'<path d="M {P(12, 7)} L {P(12, 12)} L {P(15.5, 14)}"/>')
    elif kind == "clipboard":
        b = (f'<path d="M {P(8, 4)} L {P(6, 4)} Q {P(4, 4)} {P(4, 6)} L {P(4, 20)} Q {P(4, 22)} {P(6, 22)} '
             f'L {P(18, 22)} Q {P(20, 22)} {P(20, 20)} L {P(20, 6)} Q {P(20, 4)} {P(18, 4)} L {P(16, 4)}"/>'
             f'<path d="M {P(8, 2.5)} L {P(16, 2.5)} L {P(16, 6)} L {P(8, 6)} Z"/>'
             f'<path d="M {P(8, 11)} L {P(16, 11)} M {P(8, 15)} L {P(16, 15)} M {P(8, 19)} L {P(12, 19)}"/>')
    elif kind == "code":
        b = (f'<path d="M {P(8, 7)} L {P(3, 12)} L {P(8, 17)} M {P(16, 7)} L {P(21, 12)} L {P(16, 17)} '
             f'M {P(13.5, 5)} L {P(10.5, 19)}"/>')
    elif kind == "spark":
        b = (f'<path d="M {P(11, 2)} Q {P(12, 10)} {P(20, 11)} Q {P(12, 12)} {P(11, 20)} '
             f'Q {P(10, 12)} {P(2, 11)} Q {P(10, 10)} {P(11, 2)} Z"/>'
             f'<path d="M {P(19, 2)} L {P(19, 6)} M {P(17, 4)} L {P(21, 4)}"/>')
    elif kind == "shield":
        b = (f'<path d="M {P(12, 2)} L {P(20, 5)} L {P(20, 11)} Q {P(20, 18)} {P(12, 22)} '
             f'Q {P(4, 18)} {P(4, 11)} L {P(4, 5)} Z"/>'
             f'<path d="M {P(8.5, 12)} L {P(11, 14.5)} L {P(15.5, 9.5)}"/>')
    elif kind == "db":
        b = (f'<ellipse cx="{x + 12 * k:.1f}" cy="{y + 5 * k:.1f}" rx="{8 * k:.1f}" ry="{3 * k:.1f}"/>'
             f'<path d="M {P(4, 5)} L {P(4, 19)} Q {P(12, 25)} {P(20, 19)} L {P(20, 5)} '
             f'M {P(4, 12)} Q {P(12, 18)} {P(20, 12)}"/>')
    elif kind == "megaphone":
        b = (f'<path d="M {P(3, 10)} L {P(3, 14)} L {P(7, 14)} L {P(17, 19)} L {P(17, 5)} L {P(7, 10)} Z"/>'
             f'<path d="M {P(7, 14)} L {P(8.5, 20)} L {P(11, 20)} L {P(10, 15.5)}"/>'
             f'<path d="M {P(20, 9)} Q {P(22, 12)} {P(20, 15)}"/>')
    elif kind == "check":
        b = (f'<path d="M {P(6, 2)} L {P(15, 2)} L {P(20, 7)} L {P(20, 22)} L {P(6, 22)} Z"/>'
             f'<path d="M {P(9, 14)} L {P(12, 17)} L {P(17, 11)}"/>')
    elif kind == "user":
        b = (f'<circle cx="{x + 12 * k:.1f}" cy="{y + 8 * k:.1f}" r="{4 * k:.1f}"/>'
             f'<path d="M {P(4, 21)} Q {P(4, 14)} {P(12, 14)} Q {P(20, 14)} {P(20, 21)}"/>')
    else:
        b = ""
    return _g(b)


def card(r, x, y, w, h, fill, title, subs=(), ic=None, tsize=20, ssize=16, icon_top=False):
    """파스텔 카드. 아이콘은 제목 왼쪽(기본) 또는 위."""
    out = shape(r, x, y, w, h, fill, INK, 2.0, 12)
    cx = x + w / 2
    if ic and icon_top:
        out += icon(ic, cx - 15, y + 12, 30)
        ty = y + 64
        out += T(cx, ty, title, tsize, INK, weight="bold")
    elif ic:
        tw = text_w(_clean(title), tsize)
        ix = cx - (tw + 34) / 2
        ty = y + 34
        out += icon(ic, ix, ty - 21, 26)
        out += T(ix + 34, ty, title, tsize, INK, anchor="start", weight="bold")
    else:
        ty = y + 32
        out += T(cx, ty, title, tsize, INK, weight="bold")
    yy = ty + ssize + 9
    for s in subs:
        out += T(cx, yy, s, ssize, SOFT)
        yy += ssize + 6
    return out


def chip(r, x, y, text, fill="gray", size=13.5, pad=11):
    w = text_w(_clean(text), size) + pad * 2
    return shape(r, x, y, w, size + 13, fill, INK, 1.3, 11, None, 0.4) + \
        T(x + w / 2, y + size + 4, text, size, INK), w


def chips(r, cx, y, items, size=13.5, gap=8):
    """가운데 정렬한 칩 한 줄. items = [(text, fill), ...]"""
    widths = [text_w(_clean(t), size) + 22 for t, _ in items]
    total = sum(widths) + gap * (len(items) - 1)
    x = cx - total / 2
    out = ""
    for (t, f), w in zip(items, widths):
        out += chip(r, x, y, t, f, size)[0]
        x += w + gap
    return out


def arrow(r, x1, y1, x2, y2, bend=0.0, dash=None, sw=1.9, color=INK, head=9):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    cx, cy = mx - dy / L * bend, my + dx / L * bend
    d = f' stroke-dasharray="{dash}"' if dash else ""
    ang = math.atan2(y2 - cy, x2 - cx)
    a1, a2 = ang + math.radians(152), ang - math.radians(152)
    hd = (f"M {x2 + head * math.cos(a1):.1f} {y2 + head * math.sin(a1):.1f} L {x2:.1f} {y2:.1f} "
          f"L {x2 + head * math.cos(a2):.1f} {y2 + head * math.sin(a2):.1f}")
    return (f'<path d="M {x1:.1f} {y1:.1f} Q {cx:.1f} {cy:.1f} {x2:.1f} {y2:.1f}" fill="none" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round"{d}/>'
            f'<path d="{hd}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def title(x, y, s, size=34):
    """주황 글씨에 진한 그림자를 비스듬히 깐 큰 제목."""
    return (T(x + 2, y + 2, s, size, ORANGE_DARK, weight="bold")
            + T(x, y, s, size, ORANGE, weight="bold"))


def wrap(w, h, body):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
            f'<rect width="{w}" height="{h}" fill="{BG}"/>'
            f'<g font-family="__CARDFONT__, -apple-system, sans-serif">{body}</g>'
            f'</svg>')
