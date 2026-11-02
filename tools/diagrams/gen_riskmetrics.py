#!/usr/bin/env python3
"""리스크 지표 시리즈 그림 (KS·AUC 편, Lift 편), 한/영.

KS·AUC 편 숫자는 아래 simulate()의 가상 데이터에서 나온다. 본문 숫자와 같아야 하므로
숫자를 바꾸려면 여기서 바꾸고 본문도 함께 고친다.
"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap, wobble_line, esc,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, TEAL, WASH)


# ── 시뮬레이션 (KS·AUC 편)
def roc(score, y):
    o = np.argsort(-score, kind="mergesort")
    ys = y[o]
    tp, fp = np.cumsum(ys), np.cumsum(1 - ys)
    return np.r_[0, fp / fp[-1]], np.r_[0, tp / tp[-1]]


def simulate():
    """신청 20만 명, 불량률 약 6%. 불량의 44%에 외부 데이터의 강한 신호가 있다.
    V1은 그 신호를 조금만 반영하고, V2는 그 신호에 크게 기대며 나머지 구분력은 약하다."""
    rng = np.random.default_rng(7)
    N = 200_000
    y = (rng.random(N) < 0.06).astype(int)
    flag = np.where(y == 1, rng.random(N) < 0.44, rng.random(N) < 0.006)
    s1 = 0.62 * y + 0.8 * flag + rng.standard_normal(N)
    s2 = 0.20 * y + 3.5 * flag + rng.standard_normal(N)
    return y, flag, s1, s2


def curve_stats(score, y):
    fpr, tpr = roc(score, y)
    i = int(np.argmax(tpr - fpr))
    keep = np.unique(np.r_[np.linspace(0, len(fpr) - 1, 320).astype(int), i])
    return dict(fpr=fpr[keep], tpr=tpr[keep], auc=float(np.trapezoid(tpr, fpr)),
                ks=float(tpr[i] - fpr[i]), ks_fpr=float(fpr[i]), ks_tpr=float(tpr[i]))


# ── 그리기 도우미
def poly(r, pts, color, sw=2.4, jitter=0.5, op=1.0):
    d = "M " + " L ".join(f"{x + r.between(-jitter, jitter):.1f} {y + r.between(-jitter, jitter):.1f}"
                          for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linejoin="round" stroke-linecap="round" opacity="{op}"/>')


def area(pts, base_y, color, op=0.55):
    d = f"M {pts[0][0]:.1f} {base_y:.1f} " + " ".join(f"L {x:.1f} {y:.1f}" for x, y in pts)
    d += f" L {pts[-1][0]:.1f} {base_y:.1f} Z"
    return f'<path d="{d}" fill="{color}" opacity="{op}" stroke="none"/>'


def line(r, x1, y1, x2, y2, color=INK, sw=1.4, op=1.0):
    return (f'<path d="{wobble_line(r, x1, y1, x2, y2, 1.0)}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" opacity="{op}"/>')


def dot(x, y, color, rad=5.5):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="{color}" stroke="#FBF9F4" stroke-width="2"/>'


def axes(r, x0, y0, w, h, xlabel, ylabel, ticks=(0, 0.5, 1)):
    b = [line(r, x0, y0, x0 + w, y0), line(r, x0, y0, x0, y0 - h)]
    for t in ticks:
        b.append(T(x0 + t * w, y0 + 22, f"{t:g}", 14, INK_LIGHT))
        b.append(T(x0 - 12, y0 - t * h + 5, f"{t:g}", 14, INK_LIGHT, anchor="end"))
    b.append(T(x0 + w / 2, y0 + 48, xlabel, 16, INK))
    b.append(T(x0 - 44, y0 - h / 2, ylabel, 16, INK, rot=-90))
    return "".join(b)


TEXT = {
    "ko": {
        "roc_title": "ROC 곡선 하나에서 KS와 AUC가 함께 나온다",
        "fpr": "우량 고객 누적 비율 (FPR)", "tpr": "불량 고객 누적 비율 (TPR)",
        "auc_lab": ["AUC = 곡선 아래 면적", "= {auc:.2f}"],
        "ks_lab": ["KS = 대각선과의", "가장 큰 세로 거리 = {ks:.2f}"],
        "diag": "무작위로 줄 세운 모델",
        "roc_note": ["점수가 높은 사람부터 거절선을", "한 칸씩 내리며 점을 찍으면", "이 곡선이 된다"],
        "two_title": "AUC는 둘 다 0.75인데 곡선 모양이 다르다",
        "v1": "V1 (기존)", "v2": "V2 (새 모델)",
        "v1_ks": ["V1의 KS {ks:.2f}", "신청자 31%를 거절하는 지점"],
        "v2_ks": ["V2의 KS {ks:.2f}", "신청자 8%만 거절하는 지점"],
        "dist_title": "V2 점수 분포 (그룹마다 그룹 안의 비율로 그림)",
        "good": "우량", "bad_flag": "불량 · 외부 신호 있음 (불량의 44%)", "bad_noflag": "불량 · 외부 신호 없음",
        "score": "V2 점수 (높을수록 위험)",
        "dist_note": ["신호가 없는 불량은", "우량과 거의 겹친다"],
        "flow_title": "규칙을 통과한 사람들로 다시 재면",
        "apply": ["신청 20만 명", "불량률 5.9%"],
        "rule": ["정책 규칙", "외부 데이터 신호"],
        "rule_out": ["신청자의 3.1%를 거절", "그 안에 불량의 44%"],
        "score_box": ["스코어카드가 보는 사람", "불량률 3.4%"],
        "post": ["규칙 통과 후 AUC", "V1 0.67 · V2 0.56"],
        "appr": ["승인율 80%에서 부실률", "V1 2.5% · V2 3.1%"],
        "dev_note": "개발 표본에는 규칙이 없었다: AUC 0.75 · 0.75",
    },
    "en": {
        "roc_title": "KS and AUC come from the same ROC curve",
        "fpr": "Cumulative share of goods (FPR)", "tpr": "Cumulative share of bads (TPR)",
        "auc_lab": ["AUC = area under", "the curve = {auc:.2f}"],
        "ks_lab": ["KS = largest vertical", "gap to the diagonal = {ks:.2f}"],
        "diag": "a model that ranks at random",
        "roc_note": ["Move the reject line down", "one applicant at a time and", "plot each point: that's the curve"],
        "two_title": "Both have AUC 0.75, but the curves differ",
        "v1": "V1 (current)", "v2": "V2 (new)",
        "v1_ks": ["V1 KS {ks:.2f}", "where 31% are rejected"],
        "v2_ks": ["V2 KS {ks:.2f}", "where only 8% are rejected"],
        "dist_title": "V2 score distribution (each group normalised)",
        "good": "Good", "bad_flag": "Bad, with external signal (44% of bads)", "bad_noflag": "Bad, no signal",
        "score": "V2 score (higher = riskier)",
        "dist_note": ["Bads without the signal", "overlap the goods"],
        "flow_title": "Measured again after the policy rule",
        "apply": ["200,000 applicants", "bad rate 5.9%"],
        "rule": ["Policy rule", "external data signal"],
        "rule_out": ["rejects 3.1% of applicants", "and 44% of all bads"],
        "score_box": ["Who the scorecard sees", "bad rate 3.4%"],
        "post": ["AUC after the rule", "V1 0.67, V2 0.56"],
        "appr": ["Bad rate at 80% approval", "V1 2.5%, V2 3.1%"],
        "dev_note": "The development sample had no rule: AUC 0.75 and 0.75",
    },
}


def d_roc(lang, st):
    t = TEXT[lang]; r = R(301); b = []
    W, H = 840, 560
    x0, y0, w, h = 110, 480, 380, 380
    P = lambda fx, fy: (x0 + fx * w, y0 - fy * h)
    b.append(T(W / 2, 46, t["roc_title"], 26, INK, weight="bold"))
    b.append(ul(r, 190, 650, 60))
    pts = [P(f, tp) for f, tp in zip(st["fpr"], st["tpr"])]
    b.append(area(pts, y0, WASH["blue"], 0.95))
    b.append(axes(r, x0, y0, w, h, t["fpr"], t["tpr"]))
    b.append(line(r, *P(0, 0), *P(1, 1), INK_LIGHT, 1.3, 0.8))
    b.append(T(*P(0.63, 0.555), t["diag"], 14, INK_LIGHT, rot=-45))
    b.append(poly(r, pts, BLUE, 2.6))
    kx, ky = st["ks_fpr"], st["ks_tpr"]
    b.append(line(r, *P(kx, kx), *P(kx, ky), RED, 2.6))
    b.append(dot(*P(kx, ky), RED, 4.5))
    a1, a2 = t["auc_lab"]
    b.append(T(*P(0.64, 0.24), a1, 17, BLUE))
    b.append(T(*P(0.64, 0.17), a2.format(auc=st["auc"]), 17, BLUE))
    k1, k2 = t["ks_lab"]
    # 곡선 위쪽 빈자리에 적고 짧은 화살표로 KS 지점을 가리킨다
    b.append(T(P(0.03, 0)[0], P(0, 0.95)[1], k1, 17, RED, anchor="start"))
    b.append(T(P(0.03, 0)[0], P(0, 0.95)[1] + 24, k2.format(ks=st["ks"]), 17, RED, anchor="start"))
    b.append(arr(r, P(0.16, 0)[0], P(0, 0.86)[1], P(kx, 0)[0] - 4, P(0, ky)[1] - 10, RED, 1.2, 7))
    for i, ln in enumerate(t["roc_note"]):
        b.append(T(530, 250 + i * 26, ln, 16, INK_LIGHT, anchor="start"))
    return W, H, "".join(b)


def d_two(lang, s1, s2):
    t = TEXT[lang]; r = R(302); b = []
    W, H = 840, 560
    x0, y0, w, h = 110, 480, 380, 380
    P = lambda fx, fy: (x0 + fx * w, y0 - fy * h)
    b.append(T(W / 2, 46, t["two_title"], 26, INK, weight="bold"))
    b.append(ul(r, 180, 660, 60))
    b.append(axes(r, x0, y0, w, h, t["fpr"], t["tpr"]))
    b.append(line(r, *P(0, 0), *P(1, 1), INK_LIGHT, 1.3, 0.7))
    for st, col in ((s1, BLUE), (s2, RED)):
        b.append(poly(r, [P(f, tp) for f, tp in zip(st["fpr"], st["tpr"])], col, 2.6))
    for i, (st, col, name, key) in enumerate(((s1, BLUE, t["v1"], "v1_ks"), (s2, RED, t["v2"], "v2_ks"))):
        kx, ky = st["ks_fpr"], st["ks_tpr"]
        b.append(line(r, *P(kx, kx), *P(kx, ky), col, 2.0, 0.85))
        b.append(dot(*P(kx, ky), col))
        # 범례: 이름, KS 값, KS가 나온 지점
        yy = 190 + i * 110
        l1, l2 = t[key]
        b.append(line(r, 540, yy, 572, yy, col, 3))
        b.append(T(582, yy + 6, name, 18, INK, anchor="start", weight="bold"))
        b.append(T(582, yy + 34, l1.format(ks=st["ks"]), 17, INK, anchor="start"))
        b.append(T(582, yy + 58, l2, 15, INK_LIGHT, anchor="start"))
    return W, H, "".join(b)


def d_dist(lang, y, flag, s2):
    t = TEXT[lang]; r = R(303); b = []
    W, H = 840, 470
    x0, y0, w, h = 70, 395, 700, 220
    bins = np.linspace(-3.5, 7.5, 45)
    mids = (bins[:-1] + bins[1:]) / 2
    groups = ((t["good"], y == 0, INK_LIGHT),
              (t["bad_noflag"], (y == 1) & ~flag, BLUE),
              (t["bad_flag"], (y == 1) & flag, RED))
    dens = []
    for _, m, _c in groups:
        hcount, _ = np.histogram(s2[m], bins=bins)
        dens.append(hcount / m.sum())
    top = max(d.max() for d in dens)
    X = lambda v: x0 + (v - bins[0]) / (bins[-1] - bins[0]) * w
    Y = lambda v: y0 - v / top * h
    b.append(T(W / 2, 44, t["dist_title"], 25, INK, weight="bold"))
    b.append(ul(r, 230, 610, 58))
    b.append(line(r, x0, y0, x0 + w, y0))
    for (lab, _m, col), dd in zip(groups, dens):
        pts = [(X(mx), Y(v)) for mx, v in zip(mids, dd)]
        b.append(area(pts, y0, col, 0.10))
        b.append(poly(r, pts, col, 2.4))
    b.append(T(x0 + w / 2, y0 + 34, t["score"], 16, INK))
    lx = [70, 200, 420] if lang == "ko" else [70, 180, 360]
    for (lab, _m, col), x in zip(groups, lx):
        b.append(line(r, x, 100, x + 28, 100, col, 3))
        b.append(T(x + 36, 105, lab, 15.5, INK, anchor="start"))
    n1, n2 = t["dist_note"]
    b.append(T(120, 200, n1, 16, BLUE))
    b.append(T(120, 222, n2, 16, BLUE))
    b.append(arr(r, 150, 232, 215, 262, BLUE, 1.2, 7))
    return W, H, "".join(b)


def d_flow(lang):
    t = TEXT[lang]; r = R(304); b = []
    W, H = 840, 470
    b.append(T(W / 2, 44, t["flow_title"], 25, INK, weight="bold"))
    b.append(ul(r, 250, 590, 58))
    bx = [(40, "gray", INK, t["apply"]), (300, "red", RED, t["rule"]), (560, "blue", BLUE, t["score_box"])]
    for x, wash, col, (l1, l2) in bx:
        b.append(box(r, x, 110, 230, 96, wash, col, sw=1.6))
        b.append(T(x + 115, 150, l1, 19, col if col != INK else INK, weight="bold"))
        b.append(T(x + 115, 180, l2, 17, INK))
    b.append(arr(r, 274, 158, 296, 158, INK_LIGHT, 1.6, 8))
    b.append(arr(r, 534, 158, 556, 158, INK_LIGHT, 1.6, 8))
    o1, o2 = t["rule_out"]
    b.append(arr(r, 415, 212, 415, 262, RED, 1.5, 8))
    b.append(T(415, 290, o1, 17, RED))
    b.append(T(415, 314, o2, 17, RED))
    for i, key in enumerate(("post", "appr")):
        l1, l2 = t[key]
        yy = 256 + i * 82
        b.append(box(r, 590, yy, 200, 64, None, BLUE, sw=1.2, amp=1.2))
        b.append(T(690, yy + 26, l1, 15.5, INK_LIGHT))
        b.append(T(690, yy + 50, l2, 18, BLUE, weight="bold"))
    b.append(arr(r, 675, 212, 675, 250, INK_LIGHT, 1.3, 7))
    b.append(T(W / 2, 440, t["dev_note"], 16, INK_LIGHT))
    return W, H, "".join(b)


# ── Lift 편
DECILE_BADS = [275, 195, 145, 110, 85, 65, 50, 35, 25, 15]   # 위험 높은 구간부터, 구간당 2,000명
BASE = 0.05

TEXT2 = {
    "ko": {
        "lift_title": "구간 Lift와 누적 Lift (신청 2만 명, 불량률 5%)",
        "dec": "구간 Lift", "cum": "누적 Lift (위에서부터 거절)",
        "x": "위험 순위 10% 구간", "base": "Lift 1 = 전체 평균",
        "xlab": ["상위", "10%"],
        "cum_note": ["누적 Lift = TPR ÷ 거절률", "상위 20%: 0.47 ÷ 0.20 = 2.35"],
        "ov_title": "새 규칙이 실제로 더 거절하는 사람",
        "old": ["기존 규칙", "1,500명 · 불량 330명"],
        "new": ["새 규칙", "2,000명 · 불량 240명 (12%)"],
        "both": ["겹침", "1,200명", "불량 210명"],
        "only": ["새 규칙만", "800명", "불량 30명 (3.75%)"],
        "base_post": "기존 규칙 통과자 1만 8,500명의 불량률 3.62%",
        "solo": "단독 Lift 12% ÷ 5% = 2.4",
        "marg": "한계 Lift 3.75% ÷ 3.62% ≈ 1.04",
        "hold_title": "거절된 사람의 결과를 보려면",
        "apply": "신청",
        "main": ["98%", "평소 경로"],
        "hold": ["2%", "홀드아웃"],
        "rules": "기존 규칙",
        "shadow": ["새 규칙 (섀도 모드)", "판정 없이 기록만"],
        "card": "스코어카드",
        "dec_box": ["승인", "또는 거절"],
        "skip": ["일부 규칙을 건너뛰고", "결과를 지켜본다"],
        "keep": "법·규제 규칙과 명백한 사기 규칙은 홀드아웃에도 그대로 적용",
        "label": ["몇 달 뒤 연체 여부가 나오면", "규칙별 한계 Lift를 다시 잰다"],
    },
    "en": {
        "lift_title": "Decile lift and cumulative lift (20,000 applicants, 5% bad)",
        "dec": "Decile lift", "cum": "Cumulative lift (reject from the top)",
        "x": "Risk-ranked 10% bands", "base": "Lift 1 = overall average",
        "xlab": ["top", "10%"],
        "cum_note": ["Cumulative lift = TPR / reject rate", "top 20%: 0.47 / 0.20 = 2.35"],
        "ov_title": "Who the new rule actually adds",
        "old": ["Existing rules", "1,500 applicants, 330 bad"],
        "new": ["New rule", "2,000 applicants, 240 bad (12%)"],
        "both": ["Overlap", "1,200", "210 bad"],
        "only": ["New rule only", "800", "30 bad (3.75%)"],
        "base_post": "Bad rate of the 18,500 who pass the existing rules: 3.62%",
        "solo": "Stand-alone lift 12% / 5% = 2.4",
        "marg": "Marginal lift 3.75% / 3.62% ≈ 1.04",
        "hold_title": "Getting outcomes for people you reject",
        "apply": "Applications",
        "main": ["98%", "normal path"],
        "hold": ["2%", "holdout"],
        "rules": "Existing rules",
        "shadow": ["New rule (shadow mode)", "logs hits, decides nothing"],
        "card": "Scorecard",
        "dec_box": ["Approve", "or decline"],
        "skip": ["skips some rules", "and is observed"],
        "keep": "Legal, regulatory and clear-cut fraud rules still apply to the holdout",
        "label": ["Once repayment outcomes arrive,", "re-measure each rule's marginal lift"],
    },
}


def d_lift(lang):
    t = TEXT2[lang]; r = R(401); b = []
    W, H = 840, 500
    x0, y0, w, h = 90, 400, 640, 290
    ymax = 3.0
    Y = lambda v: y0 - v / ymax * h
    bw = w / 10
    b.append(T(W / 2, 44, t["lift_title"], 24, INK, weight="bold"))
    b.append(ul(r, 150, 690, 58))
    b.append(line(r, x0, y0, x0 + w, y0))
    b.append(line(r, x0, y0, x0, y0 - h))
    for v in (0, 1, 2, 3):
        b.append(T(x0 - 12, Y(v) + 5, f"{v}", 14, INK_LIGHT, anchor="end"))
    b.append(line(r, x0, Y(1), x0 + w, Y(1), INK_LIGHT, 1.2, 0.8))
    b.append(T(x0 + w - 4, Y(1) + 20, t["base"], 14, INK_LIGHT, anchor="end"))
    cum, tot = [], 0
    for i, bad in enumerate(DECILE_BADS):
        lift = bad / 2000 / BASE
        x = x0 + i * bw + bw * 0.2
        b.append(box(r, x, Y(lift), bw * 0.6, y0 - Y(lift), "teal", TEAL, sw=1.2, amp=0.8))
        b.append(T(x + bw * 0.3, Y(lift) - 8, f"{lift:.2f}", 13.5, TEAL))
        tot += bad
        cum.append(tot / ((i + 1) * 2000) / BASE)
        b.append(T(x0 + (i + 0.5) * bw, y0 + 22, f"{(i + 1) * 10}%", 13.5, INK_LIGHT))
    pts = [(x0 + (i + 0.5) * bw, Y(v)) for i, v in enumerate(cum)]
    b.append(poly(r, pts, AMBER, 2.6))
    for (px, py), v in zip(pts, cum):
        b.append(dot(px, py, AMBER, 4.5))
    b.append(T(x0 + w / 2, y0 + 50, t["x"], 16, INK))
    for i, (lab, col) in enumerate(((t["dec"], TEAL), (t["cum"], AMBER))):
        yy = 96 + i * 28
        b.append(line(r, 470, yy, 500, yy, col, 4))
        b.append(T(510, yy + 5, lab, 16, INK, anchor="start"))
    c1, c2 = t["cum_note"]
    b.append(T(560, 190, c1, 16, AMBER))
    b.append(T(560, 214, c2, 16, AMBER))
    b.append(arr(r, 470, 206, pts[1][0] + 10, pts[1][1] - 4, AMBER, 1.2, 7))
    return W, H, "".join(b)


def d_overlap(lang):
    t = TEXT2[lang]; r = R(402); b = []
    W, H = 840, 470
    b.append(T(W / 2, 44, t["ov_title"], 25, INK, weight="bold"))
    b.append(ul(r, 260, 580, 58))
    # 기존 규칙 상자와 새 규칙 상자가 겹친다
    b.append(box(r, 70, 110, 420, 200, "blue", BLUE, sw=1.6))
    b.append(box(r, 330, 140, 440, 200, "amber", AMBER, sw=1.6))
    o1, o2 = t["old"]
    b.append(T(180, 145, o1, 19, BLUE, weight="bold"))
    b.append(T(180, 172, o2, 15.5, INK))
    n1, n2 = t["new"]
    b.append(T(640, 372, n1, 19, AMBER, weight="bold"))
    b.append(T(640, 398, n2, 15.5, INK))
    bo = t["both"]
    b.append(T(410, 205, bo[0], 17, INK_LIGHT))
    b.append(T(410, 232, bo[1], 19, INK, weight="bold"))
    b.append(T(410, 258, bo[2], 16, INK))
    on = t["only"]
    b.append(T(630, 205, on[0], 17, AMBER))
    b.append(T(630, 232, on[1], 19, INK, weight="bold"))
    b.append(T(630, 258, on[2], 16, INK))
    b.append(T(W / 2, 430, t["base_post"], 16, INK_LIGHT))
    b.append(T(175, 372, t["solo"], 16, INK_LIGHT))
    b.append(T(175, 398, t["marg"], 17, RED, weight="bold"))
    return W, H, "".join(b)


def d_holdout(lang):
    t = TEXT2[lang]; r = R(403); b = []
    W, H = 840, 470
    b.append(T(W / 2, 44, t["hold_title"], 25, INK, weight="bold"))
    b.append(ul(r, 270, 570, 58))
    b.append(box(r, 30, 180, 110, 70, "gray", INK, sw=1.4))
    b.append(T(85, 222, t["apply"], 18, INK, weight="bold"))
    # 평소 경로
    m1, m2 = t["main"]
    b.append(arr(r, 142, 200, 196, 138, INK_LIGHT, 1.5, 8))
    b.append(T(160, 150, m1, 15, INK_LIGHT))
    steps = [(200, t["rules"], "blue", BLUE), (370, None, "amber", AMBER), (560, t["card"], "green", GREEN)]
    for x, lab, wash, col in steps:
        b.append(box(r, x, 100, 150 if x != 370 else 170, 70, wash, col, sw=1.4))
    b.append(T(275, 141, t["rules"], 17, BLUE, weight="bold"))
    s1, s2 = t["shadow"]
    b.append(T(455, 131, s1, 15.5, AMBER, weight="bold"))
    b.append(T(455, 154, s2, 13.5, INK))
    b.append(T(635, 141, t["card"], 17, GREEN, weight="bold"))
    b.append(arr(r, 352, 135, 366, 135, INK_LIGHT, 1.4, 7))
    b.append(arr(r, 542, 135, 556, 135, INK_LIGHT, 1.4, 7))
    b.append(arr(r, 712, 135, 740, 135, INK_LIGHT, 1.4, 7))
    d1, d2 = t["dec_box"]
    b.append(T(790, 130, d1, 15.5, INK))
    b.append(T(790, 151, d2, 15.5, INK))
    # 홀드아웃
    h1, h2 = t["hold"]
    b.append(arr(r, 142, 232, 196, 292, TEAL, 1.5, 8))
    b.append(T(160, 286, h1, 15, TEAL))
    b.append(box(r, 200, 270, 300, 70, "teal", TEAL, sw=1.4))
    k1, k2 = t["skip"]
    b.append(T(350, 300, h2 + ": " + k1, 16, TEAL, weight="bold"))
    b.append(T(350, 324, k2, 15, INK))
    b.append(arr(r, 502, 305, 556, 160, TEAL, 1.3, 7))
    l1, l2 = t["label"]
    b.append(T(660, 300, l1, 15, INK_LIGHT))
    b.append(T(660, 322, l2, 15, INK_LIGHT))
    b.append(T(W / 2, 410, t["keep"], 15.5, INK_LIGHT))
    return W, H, "".join(b)


def build():
    y, flag, s1, s2 = simulate()
    st1, st2 = curve_stats(s1, y), curve_stats(s2, y)
    out = {}
    for lang, suf in (("ko", ""), ("en", "-en")):
        out[f"riskm-roc{suf}"] = d_roc(lang, st1)
        out[f"riskm-two-curves{suf}"] = d_two(lang, st1, st2)
        out[f"riskm-v2-dist{suf}"] = d_dist(lang, y, flag, s2)
        out[f"riskm-rule-flow{suf}"] = d_flow(lang)
        out[f"riskm-lift{suf}"] = d_lift(lang)
        out[f"riskm-overlap{suf}"] = d_overlap(lang)
        out[f"riskm-holdout{suf}"] = d_holdout(lang)
    return out


if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    figs = build()
    for name, (w, h, body) in figs.items():
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(figs))
