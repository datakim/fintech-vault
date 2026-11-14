#!/usr/bin/env python3
"""AI 에이전트가 은행 업무를 맡을 때 리스크관리부가 바꿔야 할 것: 그림, 한/영 (카드형).

1절 그림의 숫자는 아래 시뮬레이션에서 나온다. 본문 숫자와 같아야 한다.

  python3 gen_agentbank.py out_agentbank && ./fontenv/bin/python embed_fonts.py out_agentbank final_agentbank \
    && cp final_agentbank/*.svg ../../public/
  python3 gen_agentbank.py --sim      # 탐지까지 걸리는 주 수 등 숫자만 출력
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import R
from style_card import (T, shape, layer, icon, card, chips, arrow, title, wrap,
                        INK, SOFT, MUTED, ORANGE, ORANGE_DARK, EDGE, FILL)

# ── 1절 시뮬레이션: 한 업종에서 주당 500건 검토, 조기경보 판정률 6%가 13주차부터 4.8%로
P0, P1, N, THR = 0.06, 0.048, 500, 4.0
SEED = 42              # 13주차 변화 뒤 6주째(18주차)에 경보선을 넘는 경로. 4,000회 반복의 탐지 중앙값과 같다
WEEKS_BEFORE, WEEKS_AFTER = 12, 14


def llr(x):
    return x * math.log(P1 / P0) + (N - x) * math.log((1 - P1) / (1 - P0))


def path():
    import numpy as np
    rng = np.random.default_rng(SEED)
    xs = [int(v) for v in rng.binomial(N, P0, WEEKS_BEFORE)] + \
         [int(v) for v in rng.binomial(N, P1, WEEKS_AFTER)]
    S, Ss, det = 0.0, [], None
    for w, x in enumerate(xs, 1):
        S = max(0.0, S + llr(x)); Ss.append(S)
        if S > THR and det is None:
            det = w
    return xs, Ss, det


def run_lengths(reps=4000):
    import numpy as np
    rng = np.random.default_rng(0)
    def rl(p):
        S = 0.0
        for w in range(1, 5000):
            S = max(0.0, S + llr(rng.binomial(N, p)))
            if S > THR:
                return w
        return 5000
    a0 = np.array([rl(P0) for _ in range(reps)]); a1 = np.array([rl(P1) for _ in range(reps)])
    return a0, a1


TEXT = {
    "ko": {
        "c_title": "건별로는 안 보이고 누적하면 보이는 편향",
        "c_top": "한 업종의 주간 조기경보 판정률",
        "c_bot": "누적합(CUSUM) 통계량",
        "legend": "점선: 기준 6%, 파선: 관리 한계 2.8%와 9.2%",
        "change": "13주차: 에이전트 판정이 바뀜", "alarm": "18주차: 경보선을 넘음",
        "thr": "경보선 4", "week": "주차",
        "note": "합성 데이터: 주당 500건 검토, 기준 판정률 6%, 13주차부터 4.8%. 경보선 4에서 오경보는 평균 약 290주에 한 번.",
        "l_title": "에이전트 은행의 리스크 구조",
        "g_fact": "사실", "g_rule": "규칙", "g_check": "확인",
        "L1": ("1. 세계 모델", ["고객, 계약, 약정, 통제 상태를", "잇는 업무 맥락 데이터"]),
        "L2": ("2. 리스크 서비스", ["제재 검색, 신용평가,", "거래 감시를 API로"]),
        "L3": ("3. 정책 코드", ["한도와 의무를", "기계가 읽는 규칙으로"]),
        "L4": ("4. 실행 엔진", ["서비스를 엮어 결정을 만들고", "예외는 사람에게 넘긴다"]),
        "L5": ("5. 검증과 모니터링", ["출시 전 기준선, 운영 중 표류"]),
        "L6": ("6. 사람의 판단", ["정해진 지점에서 이름 있는 사람이"]),
        "L7": ("7. 증적과 보고", ["누가 어떤 근거로 결정했나"]),
        "roles": "누가 무엇을 맡나",
        "R1": ("1선 (사업 부서)", ["에이전트와 서비스를 만들고 운영,", "결과에 책임진다"]),
        "R2": ("2선 (리스크, 준법)", ["기준과 한도를 정하고 구조를 견제,", "건별 승인은 하지 않는다"]),
        "R3": ("3선 (감사)", ["통제 구조가 설계대로", "작동하는지 시험한다"]),
        "l_note": "BCG 백서(2026년 9월)의 7개 층을 이 글에서 세 묶음으로 다시 정리했다.",
        "r_title": "결정 한 건에 남겨야 할 기록",
        "r_head": "결정 기록 2026-11-03 / 0412번",
        "rows": [
            ("결정", "건설업 A사, 조기경보 미표시"),
            ("에이전트", "여신 모니터링 에이전트 v3.2 (모델 ID 날짜 포함)"),
            ("위임", "기업여신부 대신, 조기경보 판정 목적만"),
            ("권한", "에이전트 전용 자격증명 (직원 계정 아님)"),
            ("입력", "재무제표, 연체 이력, 업종 지표 (11월 3일 기준)"),
            ("서비스", "신용평가 v5, 조기경보 지표 v2"),
            ("정책 코드", "경보 기준 v14"),
            ("사람 확인", "없음 (자동 처리 구간)"),
            ("결과", "미표시 (경보 점수 0.42, 기준 0.50 미만)"),
        ],
        "q_title": "이 기록으로 답하는 질문",
        "qs": [("어느 정책 버전부터", "건설업 경보가 줄었나", "yellow"),
               ("같은 입력과 버전으로", "다시 돌리면 같은가", "blue"),
               ("사람이 본 결정은", "업종별로 몇 %인가", "purple"),
               ("직원 권한을 빌려 쓴", "결정이 있었나", "red")],
    },
    "en": {
        "c_title": "A bias invisible case by case, visible in the running total",
        "c_top": "Weekly early-warning flag rate in one sector",
        "c_bot": "CUSUM statistic",
        "legend": "dotted: baseline 6%, dashed: control limits 2.8% and 9.2%",
        "change": "week 13: the agent's judgement shifts", "alarm": "week 18: crosses the alarm line",
        "thr": "alarm line 4", "week": "week",
        "note": "Synthetic data: 500 reviews a week, baseline flag rate 6%, 4.8% from week 13. At threshold 4, a false alarm comes about once every 290 weeks.",
        "l_title": "Risk architecture for an agentic bank",
        "g_fact": "Facts", "g_rule": "Rules", "g_check": "Checks",
        "L1": ("1. World model", ["data linking customers, contracts,", "covenants and control status"]),
        "L2": ("2. Risk services", ["sanctions screening, credit", "scoring, monitoring as APIs"]),
        "L3": ("3. Policy as code", ["limits and obligations as", "machine-readable rules"]),
        "L4": ("4. Orchestration", ["composes services into decisions,", "hands exceptions to people"]),
        "L5": ("5. Validation, monitoring", ["baseline before launch, drift after"]),
        "L6": ("6. Human judgement", ["named people at defined gates"]),
        "L7": ("7. Evidence, reporting", ["who decided, on what basis"]),
        "roles": "Who does what",
        "R1": ("First line (business)", ["builds and runs agents and services,", "owns the outcomes"]),
        "R2": ("Second line (risk, compliance)", ["sets standards and limits, challenges", "the system, no case-by-case approval"]),
        "R3": ("Third line (audit)", ["tests whether controls", "work as designed"]),
        "l_note": "This post regroups the seven layers in BCG's September 2026 whitepaper into three.",
        "r_title": "What to record for every decision",
        "r_head": "Decision record 2026-11-03 / no. 0412",
        "rows": [
            ("Decision", "Construction firm A, no early warning"),
            ("Agent", "credit monitoring agent v3.2 (dated model ID)"),
            ("Delegation", "on behalf of corporate lending, warnings only"),
            ("Credential", "agent's own credential (not a staff login)"),
            ("Inputs", "financials, arrears history, sector data (as of 3 Nov)"),
            ("Services", "credit scoring v5, early-warning indicators v2"),
            ("Policy code", "warning rules v14"),
            ("Human check", "none (automated band)"),
            ("Result", "no flag (score 0.42, threshold 0.50)"),
        ],
        "q_title": "Questions the record answers",
        "qs": [("From which policy version", "did sector warnings drop?", "yellow"),
               ("Rerun with the same inputs", "and versions: same result?", "blue"),
               ("What share of decisions", "did a person see, by sector?", "purple"),
               ("Did any decision borrow", "a staff member's access?", "red")],
    },
}


def line(x1, y1, x2, y2, color=INK, sw=1.6, dash=None, op=1.0):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    o = f' opacity="{op}"' if op != 1.0 else ""
    return (f'<path d="M {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f}" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" fill="none"{d}{o}/>')


def d_cusum(lang):
    t = TEXT[lang]; r = R(901); b = []
    xs, Ss, det = path()
    W, H = 980, 720
    b.append(title(W / 2, 58, t["c_title"], 30))
    x0, x1 = 120, 930
    X = lambda w: x0 + (w - 1) / (len(xs) - 1) * (x1 - x0)
    # 위 패널: 주간 판정률
    b.append(layer(r, 24, 92, W - 48, 268, t["c_top"], 18))
    ty, by = 150, 330
    Y = lambda p: by - p / 0.10 * (by - ty)
    for p in (0.0, 0.05, 0.10):
        b.append(T(x0 - 14, Y(p) + 5, f"{p * 100:.0f}%", 14, MUTED, anchor="end"))
    lo, hi = P0 - 3 * math.sqrt(P0 * (1 - P0) / N), P0 + 3 * math.sqrt(P0 * (1 - P0) / N)
    for p in (lo, hi):
        b.append(line(x0, Y(p), x1, Y(p), MUTED, 1.3, "6 6"))
    b.append(line(x0, Y(P0), x1, Y(P0), SOFT, 1.2, "2 5"))
    b.append(T(x1, Y(0.012), t["legend"], 13.5, SOFT, anchor="end"))
    b.append(line(x0, by, x1, by, INK, 1.6))
    pts = [(X(w), Y(x / N)) for w, x in enumerate(xs, 1)]
    b.append('<path d="' + " ".join(("M" if i == 0 else "L") + f" {px:.1f} {py:.1f}" for i, (px, py) in enumerate(pts))
             + f'" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
    for w, (px, py) in enumerate(pts, 1):
        f = FILL["white"] if w <= WEEKS_BEFORE else FILL["peach"]
        b.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{f}" stroke="{INK}" stroke-width="1.6"/>')
    # 아래 패널: CUSUM
    b.append(layer(r, 24, 380, W - 48, 268, t["c_bot"], 18))
    ty2, by2 = 438, 618
    Y2 = lambda s: by2 - s / 8.0 * (by2 - ty2)
    for s in (0, 2, 4, 6, 8):
        b.append(T(x0 - 14, Y2(s) + 5, f"{s}", 14, MUTED, anchor="end"))
    b.append(line(x0, Y2(THR), x1, Y2(THR), ORANGE, 2.0, "8 6"))
    b.append(T(x0 + 8, Y2(THR) - 9, t["thr"], 14.5, ORANGE_DARK, anchor="start", weight="bold"))
    b.append(line(x0, by2, x1, by2, INK, 1.6))
    pts2 = [(X(w), Y2(s)) for w, s in enumerate(Ss, 1)]
    b.append('<path d="' + " ".join(("M" if i == 0 else "L") + f" {px:.1f} {py:.1f}" for i, (px, py) in enumerate(pts2))
             + f'" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
    for w, (px, py) in enumerate(pts2, 1):
        f = FILL["white"] if w <= WEEKS_BEFORE else (FILL["red"] if det and w >= det else FILL["peach"])
        b.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="5" fill="{f}" stroke="{INK}" stroke-width="1.6"/>')
    for w in (1, 6, 12, 13, 18, 26):
        b.append(T(X(w), by2 + 22, f"{w}", 13.5, MUTED))
    b.append(T(x1 + 4, by2 + 40, t["week"], 13.5, MUTED, anchor="end"))
    # 변화 시점, 경보 시점
    xc = (X(WEEKS_BEFORE) + X(WEEKS_BEFORE + 1)) / 2
    b.append(line(xc, 150, xc, by, SOFT, 1.4, "4 5"))
    b.append(line(xc, ty2 - 10, xc, by2, SOFT, 1.4, "4 5"))
    b.append(T(xc - 8, Y(0.012), t["change"], 14.5, SOFT, anchor="end", weight="bold"))
    xd = X(det)
    b.append(line(xd, Y2(Ss[det - 1]) - 9, xd, 462, ORANGE_DARK, 1.4, "4 5"))
    b.append(T(xd - 8, 470, t["alarm"], 14.5, ORANGE_DARK, anchor="end", weight="bold"))
    b.append(T(W / 2, 690, t["note"], 14, SOFT))
    return W, H, "".join(b)


def d_layers(lang):
    t = TEXT[lang]; r = R(902); b = []
    W, H = 980, 700
    b.append(title(W / 2, 58, t["l_title"], 30))
    gx = [24, 344, 664]; gw = 292
    groups = [("g_fact", ["L1", "L2"], ["blue", "blue"]),
              ("g_rule", ["L3", "L4"], ["yellow", "yellow"]),
              ("g_check", ["L5", "L6", "L7"], ["green", "peach", "purple"])]
    for (gk, keys, fills), x in zip(groups, gx):
        b.append(layer(r, x, 92, gw, 360, t[gk], 20))
        if len(keys) == 2:
            for i, (k, f) in enumerate(zip(keys, fills)):
                b.append(card(r, x + 16, 140 + i * 150, gw - 32, 132, f, t[k][0], t[k][1], tsize=19, ssize=15))
        else:
            for i, (k, f) in enumerate(zip(keys, fills)):
                b.append(card(r, x + 16, 140 + i * 102, gw - 32, 88, f, t[k][0], t[k][1], tsize=18.5, ssize=14.5))
    b.append(arrow(r, 318, 272, 340, 272))
    b.append(arrow(r, 638, 272, 660, 272))
    # 역할
    b.append(T(W / 2, 492, t["roles"], 20, INK, weight="bold"))
    rx = [24, 344, 664]
    for (k, f), x in zip((("R1", "white"), ("R2", "white"), ("R3", "white")), rx):
        if k == "R2":
            b.append(shape(r, x - 5, 510 - 5, gw + 10, 120 + 10, None, EDGE["peach"], 6, 18, None, 0.4))
        b.append(card(r, x, 510, gw, 120, f, t[k][0], t[k][1], tsize=19, ssize=14.5))
    b.append(T(W / 2, 672, t["l_note"], 14, SOFT))
    return W, H, "".join(b)


def d_record(lang):
    t = TEXT[lang]; r = R(903); b = []
    W, H = 980, 640
    b.append(title(W / 2, 58, t["r_title"], 30))
    cx, cy, cw, ch = 24, 96, 600, 510
    b.append(shape(r, cx - 6, cy - 6, cw + 12, ch + 12, None, EDGE["peach"], 7, 20, None, 0.4))
    b.append(shape(r, cx, cy, cw, ch, "white", INK, 2.0, 16))
    b.append(icon("check", cx + 22, cy + 18, 28))
    b.append(T(cx + 60, cy + 40, t["r_head"], 20, INK, anchor="start", weight="bold"))
    b.append(f'<path d="M {cx + 18} {cy + 62} L {cx + cw - 18} {cy + 62}" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="4 5"/>')
    ky = cy + 100
    kw = 120 if lang == "ko" else 128
    for i, (k, v) in enumerate(t["rows"]):
        y = ky + i * 48
        hi = k in ("정책 코드", "Policy code", "권한", "Credential")
        b.append(shape(r, cx + 18, y - 24, kw, 32, "peach" if hi else "gray", INK, 1.3, 10, None, 0.4))
        b.append(T(cx + 18 + kw / 2, y - 2, k, 15.5, INK, weight="bold"))
        b.append(T(cx + 18 + kw + 16, y - 2, v, 15.5 if lang == "ko" else 14.5, SOFT, anchor="start"))
    # 오른쪽: 질문
    qx, qw = 650, 306
    b.append(layer(r, qx, 96, qw, 510, t["q_title"], 18.5))
    for i, (l1, l2, f) in enumerate(t["qs"]):
        y = 146 + i * 112
        b.append(shape(r, qx + 18, y, qw - 36, 92, f, INK, 1.8, 12))
        b.append(T(qx + qw / 2, y + 38, l1, 16, INK, weight="bold"))
        b.append(T(qx + qw / 2, y + 64, l2, 16, INK, weight="bold"))
    b.append(arrow(r, 628, 350, 646, 350))
    return W, H, "".join(b)


def build():
    out = {}
    for lang, suf in (("ko", ""), ("en", "-en")):
        out[f"agentbank-cusum{suf}"] = d_cusum(lang)
        out[f"agentbank-layers{suf}"] = d_layers(lang)
        out[f"agentbank-record{suf}"] = d_record(lang)
    return out


if __name__ == "__main__":
    if sys.argv[1:] == ["--sim"]:
        xs, Ss, det = path()
        print("flags per week:", xs)
        print("detection week:", det, "| expected missed flags until detection:", round(N * (P0 - P1) * (det - WEEKS_BEFORE)))
        lo = P0 - 3 * math.sqrt(P0 * (1 - P0) / N); hi = P0 + 3 * math.sqrt(P0 * (1 - P0) / N)
        print("p-chart limits: %.3f %.3f | all weeks inside: %s" % (lo, hi, all(lo < x / N < hi for x in xs)))
        a0, a1 = run_lengths()
        import numpy as np
        print("false alarm every %.0f weeks on average (median %d)" % (a0.mean(), np.median(a0)))
        print("detection after shift: median %d weeks, 90th pct %d" % (np.median(a1), np.percentile(a1, 90)))
        sys.exit()
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    figs = build()
    for name, (w, h, body) in figs.items():
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(figs))
