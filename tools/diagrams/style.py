"""블로그 손그림 다이어그램 공통 스타일.

- 선을 두 번 그어 겹치는 러프 스케치
- 채움은 윤곽선과 따로 흔들어 물감이 번진 느낌
- 채도를 낮춘 천연 안료 팔레트
- 글씨는 나눔펜(손글씨체)을 SVG에 직접 심는다 (embed_fonts.py)
"""
import math

# ── 결정론적 난수 (매번 같은 그림이 나오도록)
class R:
    def __init__(self, seed=12345):
        self.s = seed
    def next(self):
        self.s = (self.s * 1103515245 + 12345) % (2**31)
        return self.s / (2**31)
    def between(self, a, b):
        return a + (b - a) * self.next()

def _bow(r, ax, ay, bx, by, amp):
    mx, my = (ax + bx) / 2, (ay + by) / 2
    dx, dy = bx - ax, by - ay
    L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    off = r.between(-amp, amp)
    return mx + nx * off, my + ny * off

def wobble_line(r, x1, y1, x2, y2, amp=1.6):
    cx, cy = _bow(r, x1, y1, x2, y2, amp)
    return f"M {x1:.1f} {y1:.1f} Q {cx:.1f} {cy:.1f} {x2:.1f} {y2:.1f}"

def rough_rect(r, x, y, w, h, amp=2.0, passes=2, overshoot=3.5):
    corners = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    jc = [(cx + r.between(-amp, amp), cy + r.between(-amp, amp)) for cx, cy in corners]
    out = []
    for _ in range(passes):
        d = ""
        for i in range(4):
            ax, ay = jc[i]
            bx, by = jc[(i + 1) % 4]
            dx, dy = bx - ax, by - ay
            L = math.hypot(dx, dy) or 1
            ux, uy = dx / L, dy / L
            o1, o2 = r.between(-1.0, overshoot), r.between(-1.0, overshoot)
            sx, sy = ax - ux * o1, ay - uy * o1
            ex, ey = bx + ux * o2, by + uy * o2
            cx, cy = _bow(r, sx, sy, ex, ey, amp * 0.55)
            d += f"M {sx:.1f} {sy:.1f} Q {cx:.1f} {cy:.1f} {ex:.1f} {ey:.1f} "
        out.append(d.strip())
    return out

def rough_fill(r, x, y, w, h, amp=2.8):
    pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    jp = [(cx + r.between(-amp, amp), cy + r.between(-amp, amp)) for cx, cy in pts]
    d = f"M {jp[0][0]:.1f} {jp[0][1]:.1f} "
    for i in range(4):
        ax, ay = jp[i]
        bx, by = jp[(i + 1) % 4]
        cx, cy = _bow(r, ax, ay, bx, by, amp * 0.5)
        d += f"Q {cx:.1f} {cy:.1f} {bx:.1f} {by:.1f} "
    return d + "Z"

def _arrow_head(r, x, y, angle, size=8):
    a1 = angle + math.radians(150 + r.between(-12, 12))
    a2 = angle + math.radians(-150 + r.between(-12, 12))
    p1 = (x + size * math.cos(a1), y + size * math.sin(a1))
    p2 = (x + size * math.cos(a2), y + size * math.sin(a2))
    return f"M {p1[0]:.1f} {p1[1]:.1f} L {x:.1f} {y:.1f} L {p2[0]:.1f} {p2[1]:.1f}"

# ── 팔레트
INK = "#33312E"
INK_LIGHT = "#7A736A"
PAPER = "#FBF9F4"
BLUE = "#4C6079"
RED = "#A9614F"
GREEN = "#6E8567"
AMBER = "#A8834B"
PURPLE = "#7A6379"
TEAL = "#4E7D79"

WASH = {
    "blue": "#E9EDF2", "red": "#F5E8E4", "green": "#EBEFE8",
    "amber": "#F5EEE1", "purple": "#F0EBF0", "teal": "#E6EDEC",
    "gray": "#F2EFE8",
}

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def T(x, y, s, size=19, fill=INK, anchor="middle", weight="normal", opacity=1.0, rot=None):
    a = f' text-anchor="{anchor}"' if anchor else ""
    w = f' font-weight="{weight}"' if weight != "normal" else ""
    o = f' opacity="{opacity}"' if opacity != 1.0 else ""
    r = f' transform="rotate({rot} {x} {y})"' if rot else ""
    return f'<text x="{x}" y="{y}" font-size="{size}"{a} fill="{fill}"{w}{o}{r}>{esc(s)}</text>'

def box(r, x, y, w, h, wash=None, stroke=INK, sw=1.6, amp=1.8):
    amp = amp * 1.8
    out = ""
    if wash:
        out += f'<path d="{rough_fill(r, x, y, w, h, amp * 1.4)}" fill="{WASH[wash]}" stroke="none"/>'
    for d in rough_rect(r, x, y, w, h, amp, passes=2, overshoot=amp * 1.8):
        out += (f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw * 0.8:.2f}" '
                f'stroke-linecap="round" opacity="0.82"/>')
    return out

def arr(r, x1, y1, x2, y2, color=INK, sw=1.6, head=9, amp=1.5):
    line = wobble_line(r, x1, y1, x2, y2, amp)
    ang = math.atan2(y2 - y1, x2 - x1)
    hd = _arrow_head(r, x2, y2, ang, head)
    return (f'<path d="{line}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>'
            f'<path d="{hd}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')

def ul(r, x1, x2, y, color=AMBER, sw=4.0, op=0.45):
    return (f'<path d="{wobble_line(r, x1, y, x2, y, 1.6)}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" opacity="{op}"/>')

def dots(w, h, gap=26):
    out = []
    y = gap
    while y < h:
        x = gap
        while x < w:
            out.append(f'<circle cx="{x}" cy="{y}" r="0.85" fill="#CFC7B6" opacity="0.5"/>')
            x += gap
        y += gap
    return "".join(out)

def wrap(w, h, body):
    return (f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
            f'<rect width="{w}" height="{h}" fill="{PAPER}"/>'
            f'{dots(w, h)}'
            f'<g font-family="__HANDFONT__, -apple-system, sans-serif">{body}</g>'
            f'</svg>')
