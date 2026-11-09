#!/usr/bin/env python3
"""에이전트 가상카드 글의 그림 3개 (한/영). 숫자는 발급사 공개 문서에 적힌 값만 쓴다."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, wobble_line, INK, INK_LIGHT, BLUE, RED, GREEN, AMBER)


def lines(x, y, texts, size=18, fill=INK, gap=None, anchor="middle"):
    gap = gap or size + 7
    return "".join(T(x, y + i * gap, s, size, fill, anchor=anchor) for i, s in enumerate(texts))


def seg(r, x1, y1, x2, y2, color=INK, sw=1.6, dash=False):
    d = ' stroke-dasharray="7 6"' if dash else ""
    return (f'<path d="{wobble_line(r, x1, y1, x2, y2, 1.0)}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round"{d}/>')


# 그림 1. 통제는 승인까지, 돈은 매입에서 움직인다
def d_timeline(lang):
    r = R(5101)
    ko = lang == "ko"
    W, H = 1240, 600
    B = [T(W / 2, 40, "카드 통제가 닿는 구간" if ko else "Where card controls reach", 28)]
    ly = 300
    B.append(arr(r, 50, ly, 1195, ly, sw=2.0))
    stops = [
        (130, "작업 승인" if ko else "Task approved", ["사람이 예산을 정한다"] if ko else ["a person sets the budget"]),
        (360, "카드 발급" if ko else "Card issued", ["한도, 업종, 기한"] if ko else ["limit, category, expiry"]),
        (600, "승인 요청" if ko else "Authorisation", ["실시간 승인,", "응답 기한 2초"] if ko else ["real-time decision,", "2-second window"]),
        (850, "매입" if ko else "Capture", ["보통 하루 안,", "호텔은 최대 31일"] if ko else ["usually within a day,", "hotels up to 31 days"]),
        (1085, "환불" if ko else "Refund", ["해지된 카드에도", "들어온다"] if ko else ["arrives even on", "a closed card"]),
    ]
    for x, name, sub in stops:
        B.append(seg(r, x, ly - 12, x, ly + 12, INK, 2.2))
        B.append(T(x, ly + 44, name, 22))
        B.append(lines(x, ly + 74, sub, 17, INK_LIGHT))
    # 위: 통제가 작동하는 구간
    B.append(box(r, 270, 92, 420, 150, wash="green", stroke=GREEN))
    B.append(T(480, 130, "통제가 작동한다" if ko else "Controls apply", 24, GREEN))
    B.append(lines(480, 166, ["한도, 업종, 국가, 카드 상태,", "실시간 승인 판단"] if ko
                   else ["limits, category, country,", "card status, real-time decision"], 18))
    B.append(seg(r, 290, 250, 290, ly - 14, GREEN, dash=True))
    B.append(seg(r, 670, 250, 670, ly - 14, GREEN, dash=True))
    # 아래: 통제 밖
    B.append(box(r, 730, 420, 450, 150, wash="red", stroke=RED))
    B.append(T(955, 458, "통제가 닿지 않는다" if ko else "Controls do not apply", 24, RED))
    B.append(lines(955, 494, ["승인보다 큰 매입, 승인 없는 매입,", "해지 뒤 매입은 그대로 처리된다"] if ko
                   else ["captures above the authorisation,", "without one, or after closure go through"], 18))
    B.append(T(955, 556, "남는 수단은 사후 이의 제기와 대사" if ko else "What is left: disputes and reconciliation", 17, INK_LIGHT))
    B.append(T(60, 470, "Stripe·Lithic 발급 문서 기준." if ko else "Based on Stripe and Lithic issuing docs.", 16, INK_LIGHT, anchor="start"))
    B.append(T(60, 494, "세부 동작은 발급사마다 다르다." if ko else "Details vary by issuer.", 16, INK_LIGHT, anchor="start"))
    return W, H, "".join(B)


# 그림 2. 승인 요청에 실려 오는 것과 빠지는 것
def d_visible(lang):
    r = R(5202)
    ko = lang == "ko"
    W, H = 1240, 620
    B = [T(W / 2, 40, "발급사가 승인 순간에 보는 것" if ko else "What the issuer sees at authorisation", 28)]
    lx, rx, y0, bw, bh = 60, 650, 80, 530, 330
    B.append(box(r, lx, y0, bw, bh, wash="blue", stroke=BLUE))
    B.append(T(lx + bw / 2, y0 + 44, "승인 요청에 실려 온다" if ko else "Carried in the request", 24, BLUE))
    left = (["금액과 통화", "상호명, 업종 코드, 국가", "발급 때 붙인 메타데이터", "(작업 번호, 에이전트 ID 등)", "어느 에이전트의 토큰인지"]
            if ko else ["Amount and currency", "Merchant name, category code, country", "Metadata attached at issuance", "(task ID, agent ID and so on)", "Which agent's token it is"])
    B.append(lines(lx + 40, y0 + 100, left, 20, INK, gap=44, anchor="start"))
    B.append(box(r, rx, y0, bw, bh, wash="red", stroke=RED))
    B.append(T(rx + bw / 2, y0 + 44, "실려 오지 않는다" if ko else "Not carried", 24, RED))
    right = (["어느 호텔, 며칠, 몇 박인지", "취소 규정이 무엇인지", "다른 경로로 이미 냈는지", "사람이 처음에 뭐라고 했는지"]
             if ko else ["Which hotel, which dates, how many nights", "What the cancellation terms are", "Whether it was already paid elsewhere", "What the person originally asked for"])
    B.append(lines(rx + 40, y0 + 100, right, 20, INK, gap=52, anchor="start"))
    # Verifiable Intent
    B.append(box(r, 300, 460, 640, 120, wash="amber", stroke=AMBER))
    B.append(T(620, 500, "Verifiable Intent (초안 v0.1)" if ko else "Verifiable Intent (draft v0.1)", 22, AMBER))
    B.append(lines(620, 536, ["가맹점, 품목, 금액 범위를 서명해 함께 보낸다.", "가맹점과 결제 흐름이 지원할 때만 쓸 수 있다."] if ko
                   else ["Sends signed limits on merchant, items and amount.", "Works only where the merchant and flow support it."], 18))
    B.append(arr(r, 900, y0 + bh + 8, 860, 456, color=AMBER))
    B.append(arr(r, 380, 456, 340, y0 + bh + 8, color=AMBER))
    return W, H, "".join(B)


# 그림 3. 한도를 세 층으로 나누기
def d_layers(lang):
    r = R(5303)
    ko = lang == "ko"
    W, H = 1240, 600
    B = [T(W / 2, 40, "누가 어느 한도를 정하나" if ko else "Who sets which limit", 28)]
    B.append(box(r, 60, 80, 760, 490, wash="blue", stroke=BLUE))
    B.append(T(90, 122, "사람이 정하는 상위 한도" if ko else "Envelope set by people", 24, BLUE, anchor="start"))
    B.append(T(90, 154, "월 예산, 허용 업종, 사람 확인이 필요한 금액" if ko else "Monthly budget, allowed categories, amounts needing review", 18, INK, anchor="start"))
    B.append(box(r, 110, 190, 660, 340, wash="amber", stroke=AMBER))
    B.append(T(140, 230, "에이전트가 만드는 작업별 카드" if ko else "Per-task card the agent creates", 24, AMBER, anchor="start"))
    B.append(T(140, 262, "이 작업의 금액, 가맹점, 기한" if ko else "Amount, merchant and expiry for this task", 18, INK, anchor="start"))
    B.append(box(r, 160, 300, 560, 190, wash="green", stroke=GREEN))
    B.append(T(190, 340, "결제 자격" if ko else "Payment credential", 24, GREEN, anchor="start"))
    B.append(lines(190, 374, ["일회용 카드번호, 또는", "판매자·금액·만료가 묶인 토큰"] if ko
                   else ["A single-use card number, or a token", "bound to seller, amount and expiry"], 18, INK, anchor="start"))
    # 오른쪽 설명
    B.append(arr(r, 850, 120, 812, 120, color=BLUE))
    B.append(lines(860, 112, ["에이전트에게 쓰기 권한이", "없어야 하는 층"] if ko else ["The agent should have", "no write access here"], 18, BLUE, anchor="start"))
    B.append(arr(r, 850, 240, 772, 240, color=AMBER))
    B.append(lines(860, 232, ["바깥 한도를 넘게", "만들 수 없어야 한다"] if ko else ["Must not be creatable", "beyond the envelope"], 18, AMBER, anchor="start"))
    B.append(arr(r, 850, 380, 722, 380, color=GREEN))
    B.append(lines(860, 372, ["에이전트 손에 들어가는 것.", "새도 피해가 작아야 한다"] if ko else ["What the agent holds.", "A leak should cost little"], 18, GREEN, anchor="start"))
    return W, H, "".join(B)


def build():
    out = {}
    for lang, suf in (("ko", ""), ("en", "-en")):
        out[f"agentcard-timeline{suf}"] = d_timeline(lang)
        out[f"agentcard-visible{suf}"] = d_visible(lang)
        out[f"agentcard-layers{suf}"] = d_layers(lang)
    return out


if __name__ == "__main__":
    from style import wrap
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    figs = build()
    for name, (w, h, body) in figs.items():
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(figs))
