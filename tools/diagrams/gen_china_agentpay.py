#!/usr/bin/env python3
"""중국 에이전트 결제 규칙 지도: 그림 3종 (한/영).

날짜와 조문은 원문으로 확인한 값만 쓴다(2026-11-03 확인).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap, wobble_line,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, TEAL, PURPLE)


def line(r, x1, y1, x2, y2, color=INK_LIGHT, sw=1.4, op=1.0):
    return (f'<path d="{wobble_line(r, x1, y1, x2, y2, 1.0)}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" opacity="{op}"/>')


def dot(x, y, color, rad=6):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="{color}" stroke="#FBF9F4" stroke-width="2"/>'


TL = {
    "ko": {
        "title": "2026년, 중국 에이전트 결제 규칙이 나온 순서",
        "months": ["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월"],
        "bands": [("정부·감독기관", "위: 국무원 AI+ 의견(2025.8)"), ("협회·국가표준", ""), ("기업", "")],
        "events": [
            (0, 5, 8, "3개 부처 실시의견", "결정 방식 세 가지"),
            (0, 6, 18, "금감총국 8호", "금융 AI 고위험 통로"),
            (1, 5, 22, "국가표준 GB/Z 185", "에이전트 상호연결 7부"),
            (1, 8, 24, "지급청산협회 자율공약", "8장 34조"),
            (2, 1, 16, "알리페이 ACT", ""),
            (2, 4, 2, "은련 APOP", ""),
            (2, 4, 28, "앤트 AMP", "9.11 세계 확대"),
            (2, 6, 11, "징둥 A2P2", "L0~L5"),
            (2, 6, 17, "위챗 AI 전용 카드", "(제품)"),
            (2, 9, 10, "앤트·비자·마스터카드", "KYA 협력 시작"),
        ],
    },
    "en": {
        "title": "How China's agent payment rules arrived in 2026",
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
        "bands": [("Government and regulators", "above: State Council AI+ (Aug 2025)"), ("Association and standards", ""), ("Companies", "")],
        "events": [
            (0, 5, 8, "Three-ministry opinions", "three decision modes"),
            (0, 6, 18, "NFRA guidance No. 8", "high-risk AI in finance"),
            (1, 5, 22, "GB/Z 185 standard", "agent interconnection, 7 parts"),
            (1, 8, 24, "PCAC self-regulatory convention", "8 chapters, 34 articles"),
            (2, 1, 16, "Alipay ACT", ""),
            (2, 4, 2, "UnionPay APOP", ""),
            (2, 4, 28, "Ant AMP", "global rollout 11 Sep"),
            (2, 6, 11, "JD A2P2", "L0 to L5"),
            (2, 6, 17, "WeChat AI card", "(a product)"),
            (2, 9, 10, "Ant, Visa, Mastercard", "begin KYA work"),
        ],
    },
}


def d_timeline(lang):
    t = TL[lang]; r = R(501); b = []
    W, H = 860, 560
    x0, x1 = 200, 830
    mw = (x1 - x0) / 9
    X = lambda m, d: x0 + (m - 1 + (d - 1) / 30) * mw
    bands = [(96, 196), (196, 296), (296, 500)]
    cols = [RED, AMBER, BLUE]
    b.append(T(W / 2, 46, t["title"], 25, INK, weight="bold"))
    b.append(ul(r, 230, 630, 60))
    for i, ((top, bot), (name, sub), col) in enumerate(zip(bands, t["bands"], cols)):
        if i:
            b.append(line(r, 20, top, W - 20, top, "#D8D1C2", 1.2))
        mid = (top + bot) / 2
        b.append(T(24, mid - (6 if sub else -6), name, 17, col, anchor="start", weight="bold"))
        if sub:
            b.append(T(24, mid + 18, sub, 13, INK_LIGHT, anchor="start"))
    for m in range(9):
        x = x0 + m * mw
        b.append(line(r, x, 92, x, 500, "#E3DCCD", 1.0))
        b.append(T(x + mw / 2, 528, t["months"][m], 14, INK_LIGHT))
    # 이름표 자리(점 위/아래, 정렬)는 겹치지 않게 사건마다 정해 둔다
    place = [("u", "middle"), ("u", "start"), ("d", "middle"), ("d", "middle"),
             ("u", "middle"), ("d", "middle"), ("u", "middle"), ("d", "middle"),
             ("u", "start"), ("d", "end")]
    for (band, m, d, l1, l2), (pos, anchor) in zip(t["events"], place):
        top, bot = bands[band]
        ly = (top + bot) / 2
        x = X(m, d)
        col = cols[band]
        b.append(dot(x, ly, col))
        # 두 줄 이름표를 점 위 또는 아래에 붙인다
        if pos == "u":
            y1 = ly - 22 - (19 if l2 else 0)
            y2 = ly - 22
        else:
            y1, y2 = ly + 30, ly + 49
        tx = {"middle": x, "start": x + 10, "end": x + 8}[anchor]
        b.append(T(tx, y1, l1, 15.5, INK, anchor=anchor, weight="bold"))
        if l2:
            b.append(T(tx, y2, l2, 13, INK_LIGHT, anchor=anchor))
    return W, H, "".join(b)


LV = {
    "ko": {
        "title": "AI에게 얼마나 맡기나: 세 문서의 단계를 나란히",
        "cols": ["3개 부처 실시의견 6항", "지급청산협회 공약 해설", "징둥 A2P2"],
        "axis": "에이전트 자율성",
        "rows": [
            ["사용자 본인만 결정", "에이전트 보조 결제", "L0 매 결제를 사람이 확인"],
            ["사용자가 위임한 범위에서 결정\n위임 범위를 넘으면 안 된다", "미리 정한 조건 안에서\n자율 결제", "L3 한 작업 안에서 자율 발의\nL4 정해 둔 금액·장면 안 자율 완료"],
            ["에이전트 자율 결정\n알 권리·최종 결정권은 사용자", "넓은 조건에서 자율 결제", "L5 완전 자율"],
        ],
        "note": "비슷한 수준끼리 필자가 나란히 놓았다. A2P2의 L1~L2는 공개 설명이 적어 뺐다.",
    },
    "en": {
        "title": "How much to hand to the agent: three documents side by side",
        "cols": ["Three-ministry opinions, item 6", "PCAC convention Q&A", "JD A2P2"],
        "axis": "agent autonomy",
        "rows": [
            ["Only the user decides", "Agent-assisted payment", "L0 a person confirms\nevery payment"],
            ["Decides within what the user\nauthorised, never beyond it", "Autonomous payment\nunder preset conditions", "L3 initiates payments in one task\nL4 completes them within set limits"],
            ["Agent decides on its own;\nuser keeps final say", "Autonomous payment\nunder broad conditions", "L5 fully autonomous"],
        ],
        "note": "Lined up by the author. A2P2's L1 and L2 are left out because little is published about them.",
    },
}


def multiline(x, y, text, size, color, weight="normal", gap=21):
    return "".join(T(x, y + i * gap, ln, size, color, weight=weight) for i, ln in enumerate(text.split("\n")))


def d_levels(lang):
    t = LV[lang]; r = R(502); b = []
    W, H = 860, 520
    b.append(T(W / 2, 46, t["title"], 24, INK, weight="bold"))
    b.append(ul(r, 190, 670, 60))
    cx = [235, 480, 715]
    colw = [220, 220, 240]
    heads = [RED, AMBER, BLUE]
    for x, head, col in zip(cx, t["cols"], heads):
        b.append(T(x, 104, head, 16, col, weight="bold"))
    # 아래가 낮은 자율성, 위가 높은 자율성
    rows_y = [402, 282, 162]
    washes = ["gray", "amber", "red"]
    for (row, y, wash) in zip(t["rows"], rows_y, washes):
        for x, w, cell in zip(cx, colw, row):
            b.append(box(r, x - w / 2, y - 6, w, 92, wash, INK_LIGHT, sw=1.1, amp=1.0))
            n = cell.count("\n") + 1
            b.append(multiline(x, y + 48 - (n - 1) * 11.5, cell, 16, INK, gap=23))
    b.append(arr(r, 70, 480, 70, 150, INK_LIGHT, 1.8, 10))
    b.append(T(52, 320, t["axis"], 15, INK_LIGHT, rot=-90))
    b.append(T(W / 2, 506, t["note"], 13.5, INK_LIGHT))
    return W, H, "".join(b)


PC = {
    "ko": {
        "title": "지급청산협회 자율공약: 지금 해야 하는 것과 앞으로 만들 것",
        "must": "해야 한다 (应)",
        "explore": "탐색한다 (探索)",
        "must_items": [
            ("12조", "등록·신고된 에이전트만 쓴다"),
            ("13조", "위임 약정: 한도, 결제 계좌와 우선순위, 유효기간 등"),
            ("14조", "사용자 신원과 결제 의사를 확인한다"),
            ("15조", "위임 범위 안에서만 결제한다"),
            ("16조", "사용자가 위임을 거둘 수 있게 한다"),
            ("26조", "자율 결제는 출시 전 협회에 보고한다"),
        ],
        "explore_items": [
            ("9조", "KYA: 에이전트 신원을 식별·검증한다"),
            ("10조", "위험 등급(고·중·저)별로 관리한다"),
            ("11조", "신원·등급 정보를 결제 전 과정에 넘긴다"),
            ("18조", "위임·모델 결정·결제 지시·위험 통제의 증거 체인"),
            ("26조", "에이전트 자율 결제 자체를 신중히 시도한다"),
        ],
        "foot": "26조의 다섯 가지 장치: 사람 상담, 위험 모니터링, 여론 모니터링, 비상 대응, 되돌리기",
    },
    "en": {
        "title": "PCAC convention: what is required now and what is to be built",
        "must": "Must (应)",
        "explore": "Explore (探索)",
        "must_items": [
            ("Art. 12", "use only registered or filed agents"),
            ("Art. 13", "agreement: limits, account and priority, validity"),
            ("Art. 14", "verify the user's identity and intent to pay"),
            ("Art. 15", "pay only within what was authorised"),
            ("Art. 16", "let users withdraw the authorisation"),
            ("Art. 26", "report autonomous payment before launch"),
        ],
        "explore_items": [
            ("Art. 9", "KYA: identify and verify the agent"),
            ("Art. 10", "manage agents by high, medium, low risk"),
            ("Art. 11", "pass identity and tier along the payment chain"),
            ("Art. 18", "evidence chain: mandate, model decision,\npayment instruction, risk control"),
            ("Art. 26", "approach autonomous payment itself with care"),
        ],
        "foot": "Art. 26 safeguards: human service, risk monitoring, public-opinion monitoring, emergency response, fallback",
    },
}


def d_pcac(lang):
    t = PC[lang]; r = R(503); b = []
    W, H = 860, 520
    b.append(T(W / 2, 46, t["title"], 23, INK, weight="bold"))
    b.append(ul(r, 170, 690, 60))
    for (x, head, items, wash, col) in ((30, t["must"], t["must_items"], "green", GREEN),
                                         (440, t["explore"], t["explore_items"], "amber", AMBER)):
        b.append(box(r, x, 84, 390, 380, wash, col, sw=1.6))
        b.append(T(x + 195, 118, head, 20, col, weight="bold"))
        y = 160
        for art, text in items:
            b.append(T(x + 22, y, art, 15.5, col, anchor="start", weight="bold"))
            for i, ln in enumerate(text.split("\n")):
                b.append(T(x + (92 if lang == "en" else 70), y + i * 21, ln, 15.5, INK, anchor="start"))
            y += 52 + (text.count("\n") * 14)
    b.append(T(W / 2, 496, t["foot"], 14, INK_LIGHT))
    return W, H, "".join(b)


DIAGRAMS = {
    "cn-agentpay-timeline": lambda: d_timeline("ko"),
    "cn-agentpay-timeline-en": lambda: d_timeline("en"),
    "cn-agentpay-levels": lambda: d_levels("ko"),
    "cn-agentpay-levels-en": lambda: d_levels("en"),
    "cn-agentpay-pcac": lambda: d_pcac("ko"),
    "cn-agentpay-pcac-en": lambda: d_pcac("en"),
}

if __name__ == "__main__":
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    for name, fn in DIAGRAMS.items():
        w, h, body = fn()
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(DIAGRAMS))
