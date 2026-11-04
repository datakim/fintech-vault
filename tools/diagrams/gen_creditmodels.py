#!/usr/bin/env python3
"""신용 모델 5종 글의 그림 3개 (한/영). 숫자 없는 구조 그림이다."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, wobble_line, INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, TEAL)


def lines(x, y, texts, size=18, fill=INK, gap=None, anchor="middle"):
    gap = gap or size + 6
    return "".join(T(x, y + i * gap, s, size, fill, anchor=anchor) for i, s in enumerate(texts))


def seg(r, x1, y1, x2, y2, color=INK, sw=1.6, dash=False):
    d = ' stroke-dasharray="7 6"' if dash else ""
    return (f'<path d="{wobble_line(r, x1, y1, x2, y2, 1.0)}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round"{d}/>')


# 그림 1. 직선이 아니라 되돌아오는 흐름
def d_loop(lang):
    r = R(4101)
    ko = lang == "ko"
    W, H = 1240, 560
    bw, bh = 260, 136
    top, bot = 60, 290
    X = {"m": 40, "f": 370, "a": 700}
    B = [T(W / 2, 34, "모델 다섯 개는 한 줄로 끝나지 않는다" if ko else "The five models do not end in a straight line", 26)]
    cards = [
        ("m", top, "blue", "마케팅" if ko else "Marketing",
         ["누구에게 제안할까", "전환이 늘어날 사람"] if ko else ["Whom to approach", "who converts because of it"]),
        ("f", top, "red", "사기" if ko else "Fraud",
         ["실재하는 사람인가", "갚을 뜻이 있나"] if ko else ["Is the person real", "and willing to repay"]),
        ("a", top, "amber", "신청" if ko else "Application",
         ["승인, 금리, 한도", "갚을 능력이 있나"] if ko else ["Approve, price, limit", "able to repay"]),
        ("a", bot, "green", "행동" if ko else "Behaviour",
         ["한도 증액·감액, 조기 경보", "지금 나빠지는 중인가"] if ko else ["Limit changes, early warning", "getting worse now"]),
        ("f", bot, "teal", "추심" if ko else "Collections",
         ["누구에게 무엇을 할까", "연락하면 더 갚을 사람"] if ko else ["Whom to contact, how", "who repays more if contacted"]),
    ]
    for key, y, wash, title, sub in cards:
        x = X[key]
        B.append(box(r, x, y, bw, bh, wash=wash))
        B.append(T(x + bw / 2, y + 42, title, 26))
        B.append(lines(x + bw / 2, y + 76, sub, 18, INK_LIGHT))
    # 앞으로 가는 흐름
    B.append(arr(r, 304, top + 68, 366, top + 68))
    B.append(arr(r, 634, top + 68, 696, top + 68))
    B.append(arr(r, 830, top + bh + 6, 830, bot - 6))
    B.append(T(842, top + bh + 52, "승인" if ko else "approved", 18, anchor="start"))
    B.append(arr(r, 696, bot + 68, 636, bot + 68))
    B.append(T(666, bot + 56, "연체" if ko else "late", 18))
    # 거절: 결과가 없다
    B.append(box(r, 1010, top, 190, bh, stroke=INK_LIGHT))
    B.append(lines(1105, top + 50, ["거절" , "결과를 알 수 없어", "학습 표본에서 빠진다"] if ko else ["Declined", "outcome unseen,", "missing from training"], 18, INK_LIGHT))
    B.append(arr(r, 964, top + 68, 1006, top + 68, color=INK_LIGHT))
    # 되돌아오는 흐름
    B.append(arr(r, 500, bot - 6, 500, top + bh + 6, color=RED))
    B.append(lines(490, top + bh + 36, ["손실 사유를 다시 보면", "사기 라벨이 된다"] if ko else ["Reviewed losses", "become fraud labels"], 18, RED, anchor="end"))
    B.append(seg(r, 830, bot + bh + 6, 830, 490, BLUE))
    B.append(seg(r, 830, 490, 170, 490, BLUE))
    B.append(arr(r, 170, 490, 170, top + bh + 6, color=BLUE))
    B.append(T(500, 522, "기존 고객의 행동 점수가 한도 증액과 교차 판매 대상으로 돌아간다" if ko
               else "Behaviour scores of existing customers feed limit increases and cross-sell", 19, BLUE))
    return W, H, "".join(B)


# 그림 2. 데이터 출처 × 모델
def d_sources(lang):
    r = R(4202)
    ko = lang == "ko"
    W, H = 1080, 590
    x0, y0 = 300, 118
    cw, ch = 150, 66
    cols = ["마케팅", "사기", "신청", "행동", "추심"] if ko else ["Marketing", "Fraud", "Application", "Behaviour", "Collections"]
    rows = [
        (("신청서·제출 서류", "소득, 직업, 입력 행태") if ko else ("Application form, documents", "income, job, input behaviour"), [0, 1, 2, 0, 1]),
        (("신용정보(CB)", "연체, 조회, 다른 금융사 부채") if ko else ("Credit bureau", "arrears, enquiries, other debt"), [1, 1, 2, 1, 1]),
        (("자사 거래·상환 이력", "입출금, 결제, 상환") if ko else ("Own transactions, repayments", "deposits, spending, payments"), [2, 1, 1, 2, 2]),
        (("기기·앱 세션", "기기, IP, 로그인, 화면 이동") if ko else ("Device and app sessions", "device, IP, logins, navigation"), [2, 2, 1, 1, 1]),
        (("접촉 이력", "캠페인 반응, 통화 결과, 약속") if ko else ("Contact history", "campaign response, calls, promises"), [2, 0, 0, 1, 2]),
        (("관계망", "공유 기기·계좌·연락처") if ko else ("Links between accounts", "shared device, account, contact"), [0, 2, 1, 1, 0]),
    ]
    B = [T(W / 2, 40, "모델마다 주로 쓰는 데이터가 다르다" if ko else "Each model leans on different data", 26)]
    for j, c in enumerate(cols):
        B.append(T(x0 + cw * j + cw / 2, y0 - 22, c, 21))
    for i, ((a, b), vals) in enumerate(rows):
        y = y0 + ch * i
        if i:
            B.append(seg(r, 30, y, W - 30, y, "#CFC7B6", 1.0))
        B.append(T(30, y + 28, a, 20, anchor="start"))
        B.append(T(30, y + 52, b, 15, INK_LIGHT, anchor="start"))
        for j, v in enumerate(vals):
            cx, cy = x0 + cw * j + cw / 2, y + ch / 2
            if v == 2:
                B.append(f'<circle cx="{cx}" cy="{cy}" r="15" fill="{TEAL}"/>')
            elif v == 1:
                B.append(f'<circle cx="{cx}" cy="{cy}" r="10" fill="none" stroke="{TEAL}" stroke-width="2.4"/>')
            else:
                B.append(f'<circle cx="{cx}" cy="{cy}" r="2.5" fill="#B9B09D"/>')
    ly = y0 + ch * 6 + 34
    B.append(f'<circle cx="190" cy="{ly - 6}" r="13" fill="{TEAL}"/>')
    B.append(T(212, ly, "주로 쓴다" if ko else "main source", 18, anchor="start"))
    B.append(f'<circle cx="420" cy="{ly - 6}" r="9" fill="none" stroke="{TEAL}" stroke-width="2.4"/>')
    B.append(T(438, ly, "보조로 쓴다" if ko else "supporting", 18, anchor="start"))
    B.append(f'<circle cx="640" cy="{ly - 6}" r="2.5" fill="#B9B09D"/>')
    B.append(T(652, ly, "거의 안 쓴다" if ko else "rarely used", 18, anchor="start"))
    B.append(T(W / 2, ly + 30, "흔한 구성을 정리한 것이며 회사와 상품에 따라 다르다" if ko else "A common set-up; it varies by company and product", 16, INK_LIGHT))
    return W, H, "".join(B)


# 그림 3. 모델별 관측 기간과 성과 기간
def d_windows(lang):
    r = R(4303)
    ko = lang == "ko"
    W, H = 1160, 590
    ax = 650
    rows = [
        (("마케팅", "최근 1~6개월 행동", "발송일", "7~30일 안의 전환") if ko else ("Marketing", "last 1-6 months of activity", "send date", "conversion in 7-30 days"), 300, 150),
        (("사기", "세션·기기 + 수개월 이력", "신청 순간", "수개월 뒤 확정되는 판정") if ko else ("Fraud", "session, device, months of history", "application", "verdict confirmed months later"), 300, 260),
        (("신청", "신청 전 12~24개월 신용 이력", "신청일", "6~24개월 안의 연체") if ko else ("Application", "12-24 months of credit history", "application date", "arrears within 6-24 months"), 400, 380),
        (("행동", "최근 3~12개월 추세", "매월 스냅샷", "2~12개월 안의 연체") if ko else ("Behaviour", "3-12 month trends", "monthly snapshot", "arrears within 2-12 months"), 260, 300),
        (("추심", "연체 전 이력 + 연체 후 접촉", "연체 N일째, 매일", "30~180일 안의 회수") if ko else ("Collections", "history plus contact since arrears", "day N of arrears, daily", "recovery within 30-180 days"), 330, 240),
    ]
    B = [T(W / 2, 40, "모델마다 기준 시점과 기간이 다르다" if ko else "Each model has its own scoring point and windows", 26)]
    B.append(T(ax - 20, 78, "기준 시점 이전: 변수" if ko else "before the scoring point: features", 18, BLUE, anchor="end"))
    B.append(T(ax + 20, 78, "기준 시점 이후: 라벨" if ko else "after the scoring point: label", 18, RED, anchor="start"))
    y = 104
    for (name, obs, pt, perf), lw, rw in rows:
        B.append(T(30, y + 30, name, 22, anchor="start"))
        B.append(box(r, ax - lw - 4, y + 2, lw, 40, wash="blue", stroke=BLUE, sw=1.2, amp=1.0))
        B.append(T(ax - 4 - lw / 2, y + 28, obs, 16))
        B.append(box(r, ax + 4, y + 2, rw, 40, wash="red", stroke=RED, sw=1.2, amp=1.0))
        B.append(T(ax + 4 + rw / 2, y + 28, perf, 16))
        B.append(T(ax + 10, y + 62, pt, 16, INK_LIGHT, anchor="start"))
        y += 88
    B.append(seg(r, ax, 92, ax, y - 18, INK, 2.0))
    B.append(T(W / 2, y + 2, "길이는 흔한 구성을 나타낸 것이고 비율에 맞춘 것은 아니다" if ko else "Lengths show a common set-up and are not to scale", 16, INK_LIGHT))
    return W, H, "".join(B)


def build():
    out = {}
    for lang, suf in (("ko", ""), ("en", "-en")):
        out[f"creditm-loop{suf}"] = d_loop(lang)
        out[f"creditm-sources{suf}"] = d_sources(lang)
        out[f"creditm-windows{suf}"] = d_windows(lang)
    return out


if __name__ == "__main__":
    from style import wrap
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    figs = build()
    for name, (w, h, body) in figs.items():
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(figs))
