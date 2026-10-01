#!/usr/bin/env python3
"""AI 회사는 결제 회사가 될까: 그림 3종."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, ul, wrap,
                   INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, PURPLE, TEAL)

TXT = {
    "ko": {
        "roles_title": "같은 결제라도 돈이 다르다",
        "panels": [
            ("blue", BLUE, "① 내 상품값 받기", "사용자", "결제사(Stripe 등)", "AI 회사", 2,
             "AI 회사의 자리: 상인", "예: 구독료"),
            ("green", GREEN, "② 사용자 대신 내기", "사용자", "에이전트가 대신 결제", "호텔", 1,
             "AI 회사의 자리: 심부름하는 실행자", "예: Muse가 호텔을 잡는다"),
            ("amber", AMBER, "③ 성사시키고 떼기", "호텔", "성사 수수료", "AI 회사", 2,
             "AI 회사의 자리: 중개자", "예: 저커버그가 말한 수수료"),
        ],
        "roles_foot1": "셋은 한 회사 안에 같이 있을 수 있지만 서로 다른 돈이다",
        "roles_foot2": "돈을 실제로 옮겨준 값(결제 처리 수수료)은 이 셋과 또 다른 자리, 결제사 몫이다",
        "rev_title": "한 번의 거래에 붙는 네 가지 돈",
        "rev_sub": "Muse가 사용자 대신 호텔을 잡는다고 하면",
        "steps": ["에이전트가 호텔을 고른다", "카드에서 호텔로 돈이 간다", "에이전트가 모델·API를 쓴다", "클라우드에서 돌고 지갑을 쓴다"],
        "cols": [
            ("amber", AMBER, "① 성사 수수료", "AI 플랫폼", "손님을 데려온 값", "추천이 공정했나"),
            ("blue", BLUE, "② 결제 처리 수수료", "카드사·결제사", "돈을 옮겨준 값", "도용·차지백·환불"),
            ("purple", PURPLE, "③ 과금", "과금 도구", "쓴 만큼 청구한 값", "계량이 정확한가"),
            ("green", GREEN, "④ 실행 인프라", "클라우드·지갑", "에이전트를 돌린 값", "한도와 기록"),
        ],
        "labels": ("받는 곳", "무엇의 값", "따라붙는 책임"),
        "rev_foot1": "마진은 ②가 가장 얇고, 사고 책임은 ②가 가장 두껍다",
        "rev_foot2": "모든 거래에 넷이 다 붙지는 않는다. 받는 회사도 다 다를 수 있다",
        "risk_title": "승인할 때 묻는 질문이 바뀐다",
        "risk_heads": ("사람이 결제할 때", "에이전트가 결제할 때"),
        "rows": [
            ("승인 질문", "이 카드 주인이 맞나", "위임받은 범위 안인가"),
            ("보는 신호", "기기·위치·평소 결제 습관", "에이전트 신원·위임 한도·사람 확인 여부"),
            ("분쟁의 증거", "내가 안 했다 / 받은 게 다르다", "시킨 건 맞는데 산 게 틀렸다 → 위임 기록"),
            ("피해 줄이기", "결제 한도·추가 인증", "일회용 카드·결제 세션 한도"),
        ],
        "risk_foot": "Google AP2의 결제 위임서에는 결제 순간 사람이 있었는지가 같이 실려 간다",
    },
    "en": {
        "roles_title": "The same payment, different money",
        "panels": [
            ("blue", BLUE, "① Getting paid for your product", "user", "processor (Stripe etc.)", "AI company", 2,
             "AI company as: merchant", "e.g. a subscription"),
            ("green", GREEN, "② Paying on the user's behalf", "user", "agent pays for them", "hotel", 1,
             "AI company as: delegated executor", "e.g. Muse books a hotel"),
            ("amber", AMBER, "③ Taking a cut of the deal", "hotel", "transaction fee", "AI company", 2,
             "AI company as: intermediary", "e.g. the fee Zuckerberg described"),
        ],
        "roles_foot1": "All three can live inside one company, but they are different money",
        "roles_foot2": "The fee for actually moving the money (processing) is yet another seat: the processor's",
        "rev_title": "Four kinds of money on one transaction",
        "rev_sub": "Say Muse books a hotel for the user",
        "steps": ["the agent picks the hotel", "money moves card to hotel", "the agent calls models and APIs", "it runs in a cloud, uses a wallet"],
        "cols": [
            ("amber", AMBER, "① Transaction fee", "AI platform", "for bringing the buyer", "was the pick fair?"),
            ("blue", BLUE, "② Processing fee", "networks, processors", "for moving the money", "fraud, chargebacks, refunds"),
            ("purple", PURPLE, "③ Billing", "billing tools", "for metering usage", "is the metering right?"),
            ("green", GREEN, "④ Execution", "cloud, wallets", "for running the agent", "limits and logs"),
        ],
        "labels": ("who earns it", "paid for", "liability attached"),
        "rev_foot1": "② has the thinnest margin and the heaviest liability",
        "rev_foot2": "Not every transaction carries all four, and each may go to a different company",
        "risk_title": "The question at approval changes",
        "risk_heads": ("a person pays", "an agent pays"),
        "rows": [
            ("the approval question", "is this the cardholder?", "is this inside the mandate?"),
            ("signals", "device, location, usual habits", "agent identity, mandate limit, human present?"),
            ("dispute evidence", "\"not me\" / \"not as described\"", "\"I asked, but it bought wrong\": the mandate log"),
            ("limiting damage", "spend limits, step-up auth", "one-time cards, session caps"),
        ],
        "risk_foot": "A Google AP2 payment mandate carries whether a human was present at the moment of payment",
    },
}


def d1_roles(L):
    t = TXT[L]
    r = R(2101); b = []
    W, H = 900, 470
    b.append(T(450, 46, t["roles_title"], 28, INK, weight="bold"))
    b.append(ul(r, 290 if L == "ko" else 250, 610 if L == "ko" else 650, 63))
    for i, (wash, col, title, payer, via, payee, hot, role, ex) in enumerate(t["panels"]):
        x = 36 + i * 284
        b.append(box(r, x, 84, 260, 286, wash, col, sw=1.8))
        b.append(T(x + 130, 116, title, 17 if L == "ko" else 15, col, weight="bold"))
        rows = [(payer, 0), (via, 1), (payee, 2)]
        for name, k in rows:
            y = 136 + k * 66
            is_hot = (k == hot)
            b.append(box(r, x + 30, y, 200, 40, wash if is_hot else None, col if is_hot else INK_LIGHT,
                         sw=1.6 if is_hot else 1.2, amp=1.1))
            b.append(T(x + 130, y + 26, name, 15 if L == "ko" else 14, col if is_hot else INK,
                       weight="bold" if is_hot else "normal"))
            if k < 2:
                b.append(arr(r, x + 130, y + 44, x + 130, y + 62, INK_LIGHT, 1.4, 7))
        b.append(T(x + 130, 334, role, 14 if L == "ko" else 13, INK))
        b.append(T(x + 130, 356, ex, 13 if L == "ko" else 12.5, INK_LIGHT))
    b.append(T(450, 412, t["roles_foot1"], 18 if L == "ko" else 17, INK, weight="bold"))
    b.append(T(450, 442, t["roles_foot2"], 14.5 if L == "ko" else 14, INK_LIGHT))
    return W, H, "".join(b)


def d2_revenues(L):
    t = TXT[L]
    r = R(2102); b = []
    W, H = 900, 540
    b.append(T(450, 46, t["rev_title"], 28, INK, weight="bold"))
    b.append(ul(r, 270 if L == "ko" else 230, 630 if L == "ko" else 670, 63))
    b.append(T(450, 94, t["rev_sub"], 15.5, INK_LIGHT))
    for i, s in enumerate(t["steps"]):
        x = 36 + i * 210
        b.append(box(r, x, 112, 198, 44, "gray", INK_LIGHT, sw=1.2, amp=1.1))
        b.append(T(x + 99, 139, s, 13.5 if L == "ko" else 12.5, INK))
        b.append(arr(r, x + 99, 160, x + 99, 184, INK_LIGHT, 1.4, 7))
    lab = t["labels"]
    for i, (wash, col, name, who, what, risk) in enumerate(t["cols"]):
        x = 36 + i * 210
        b.append(box(r, x, 190, 198, 232, wash, col, sw=1.8))
        b.append(T(x + 99, 222, name, 17 if L == "ko" else 15.5, col, weight="bold"))
        for j, (k, v) in enumerate(zip(lab, (who, what, risk))):
            y = 258 + j * 54
            b.append(T(x + 99, y, k, 12.5, INK_LIGHT))
            b.append(T(x + 99, y + 22, v, 15 if L == "ko" else 13, INK, weight="bold" if j == 2 else "normal"))
    b.append(box(r, 36, 440, 828, 48, "red", RED, sw=1.7))
    b.append(T(450, 470, t["rev_foot1"], 18, RED, weight="bold"))
    b.append(T(450, 516, t["rev_foot2"], 14.5, INK_LIGHT))
    return W, H, "".join(b)


def d3_risk(L):
    t = TXT[L]
    r = R(2103); b = []
    W, H = 900, 500
    b.append(T(450, 46, t["risk_title"], 28, INK, weight="bold"))
    b.append(ul(r, 270 if L == "ko" else 240, 630 if L == "ko" else 660, 63))
    h1, h2 = t["risk_heads"]
    b.append(box(r, 36, 84, 380, 44, "gray", INK_LIGHT, sw=1.7))
    b.append(T(226, 113, h1, 20, INK, weight="bold"))
    b.append(box(r, 448, 84, 416, 44, "amber", AMBER, sw=1.7))
    b.append(T(656, 113, h2, 20, AMBER, weight="bold"))
    y = 158
    for label, left, right in t["rows"]:
        b.append(T(432, y - 9, label, 14.5, INK_LIGHT))
        b.append(box(r, 36, y, 380, 44, None, INK_LIGHT, sw=1.2, amp=1.2))
        b.append(T(226, y + 28, left, 15 if L == "ko" else 14, INK))
        b.append(box(r, 448, y, 416, 44, None, AMBER, sw=1.3, amp=1.2))
        b.append(T(656, y + 28, right, 15 if L == "ko" else 14, INK, weight="bold"))
        y += 70
    b.append(T(450, 476, t["risk_foot"], 15.5 if L == "ko" else 14.5, INK_LIGHT))
    return W, H, "".join(b)


def build(L, outdir):
    suf = "" if L == "ko" else "-en"
    diagrams = {f"agentpay-roles{suf}": d1_roles, f"agentpay-four-revenues{suf}": d2_revenues,
                f"agentpay-risk{suf}": d3_risk}
    os.makedirs(outdir, exist_ok=True)
    for name, fn in diagrams.items():
        w, h, body = fn(L)
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    return len(diagrams)


if __name__ == "__main__":
    lang = sys.argv[2] if len(sys.argv) > 2 else "ko"
    print("generated", build(lang, sys.argv[1]))
