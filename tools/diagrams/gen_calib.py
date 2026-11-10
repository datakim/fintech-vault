#!/usr/bin/env python3
"""결정 모델 확률 보정 글의 그림 3개 (한/영).

그림 2와 3의 숫자는 글에 실은 합성 데이터 시뮬레이션(AUROC 0.90, 시드 고정)의 결과다.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (R, T, box, arr, wobble_line, ul, INK, INK_LIGHT, BLUE, RED, GREEN, AMBER, WASH)


def lines(x, y, texts, size=18, fill=INK, gap=None, anchor="middle"):
    gap = gap or size + 8
    return "".join(T(x, y + i * gap, s, size, fill, anchor=anchor) for i, s in enumerate(texts))


def line(r, x1, y1, x2, y2, color=INK, sw=1.4, op=1.0, dash=False):
    d = ' stroke-dasharray="6 6"' if dash else ""
    return (f'<path d="{wobble_line(r, x1, y1, x2, y2, 1.0)}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" opacity="{op}"{d}/>')


def poly(r, pts, color, sw=2.6, jitter=0.5):
    d = "M " + " L ".join(f"{x + r.between(-jitter, jitter):.1f} {y + r.between(-jitter, jitter):.1f}"
                          for x, y in pts)
    return (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linejoin="round" stroke-linecap="round"/>')


def dot(x, y, color, rad=5.0):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rad}" fill="{color}" stroke="#FBF9F4" stroke-width="2"/>'


# 그림 1. 확률이 나오는 세 곳
def d_sources(lang):
    r = R(6101)
    ko = lang == "ko"
    W, H = 1240, 520
    B = [T(W / 2, 44, "같은 0.9라도 숫자가 나온 곳이 다르다" if ko else "The same 0.9 can come from three places", 28)]
    B.append(ul(r, 380, 860, 58))
    cols = [
        ("amber", AMBER,
         "말로 한 확률" if ko else "Verbalised confidence",
         ["\"90% 확신합니다\"라는", "글자를 생성한다"] if ko else ["The model writes", "\"I'm 90% sure\" as text"],
         ["결과와 대조해 학습하지", "않았다면 그럴듯한 숫자일 뿐", "0.7~0.95의 둥근 값에 몰린다"] if ko
         else ["Unless trained against outcomes,", "it is just a plausible number", "Clusters on round values, 0.7 to 0.95"]),
        ("blue", BLUE,
         "토큰 확률" if ko else "Token probability",
         ["답 토큰에 모델이 붙인", "확률을 읽는다"] if ko else ["Read the probability the", "model puts on the answer token"],
         ["사전학습 모델은 꽤 맞지만", "RLHF를 거치면 나빠진다", "많은 API가 내주지 않는다"] if ko
         else ["Fairly calibrated after pretraining,", "worse after RLHF", "Many APIs do not expose it"]),
        ("green", GREEN,
         "결정 모델의 분포" if ko else "Decision-model distribution",
         ["선택지마다 확률을 내고", "합은 1이다"] if ko else ["A probability for each option,", "summing to 1"],
         ["보정을 목표로 학습했다", "(학습 방법은 비공개)", "내가 준 선택지 안에서만 나뉜다"] if ko
         else ["Trained with calibration as a goal", "(method not disclosed)", "Split only across the options given"]),
    ]
    x0, bw, gap = 50, 360, 30
    for i, (wash, col, name, how, notes) in enumerate(cols):
        x = x0 + i * (bw + gap)
        B.append(box(r, x, 90, bw, 330, wash=wash, stroke=col))
        B.append(T(x + bw / 2, 136, name, 25, col))
        B.append(lines(x + bw / 2, 190, how, 19, INK))
        B.append(line(r, x + 40, 262, x + bw - 40, 262, INK_LIGHT, 1.2, 0.7))
        B.append(lines(x + bw / 2, 306, notes, 18, INK_LIGHT, gap=34))
    B.append(T(W / 2, 474, "어느 쪽이든 학습 때 본 데이터 기준이다. 내 데이터에서 맞는지는 따로 재야 한다." if ko
               else "Each is calibrated, if at all, on the data it was trained on. Your data needs its own check.", 19, INK))
    return W, H, "".join(B)


# 그림 2. 합쳐 보면 맞고 과제별로는 틀린다 (합성 데이터)
CURVES = {
    "pooled": [(0.03, 0.035), (0.14, 0.148), (0.25, 0.243), (0.35, 0.346), (0.45, 0.437),
               (0.55, 0.564), (0.65, 0.642), (0.75, 0.752), (0.85, 0.856), (0.95, 0.953)],
    0.5: [(0.04, 0.096), (0.15, 0.351), (0.25, 0.532), (0.35, 0.612), (0.45, 0.705),
          (0.55, 0.808), (0.65, 0.844), (0.75, 0.903), (0.85, 0.95), (0.95, 0.979)],
    0.2: [(0.03, 0.029), (0.14, 0.115), (0.24, 0.175), (0.35, 0.295), (0.45, 0.363),
          (0.55, 0.515), (0.65, 0.586), (0.75, 0.73), (0.85, 0.838), (0.95, 0.944)],
    0.03: [(0.03, 0.004), (0.14, 0.021), (0.25, 0.034), (0.35, 0.046), (0.44, 0.078),
           (0.55, 0.117), (0.65, 0.152), (0.75, 0.194), (0.85, 0.373), (0.94, 0.706)],
}


def d_reliability(lang):
    r = R(6202)
    ko = lang == "ko"
    W, H = 1240, 640
    x0, y0, w, h = 120, 560, 460, 460
    P = lambda fx, fy: (x0 + fx * w, y0 - fy * h)
    B = [T(W / 2, 44, "세 과제를 합치면 대각선에 붙지만 과제마다 보면 어긋난다" if ko else "Pooled, the curve sits on the diagonal; task by task, it does not", 28)]
    B.append(ul(r, 330, 910, 58))
    # 축
    B.append(line(r, x0, y0, x0 + w, y0)); B.append(line(r, x0, y0, x0, y0 - h))
    for t in (0, 0.5, 1):
        B.append(T(x0 + t * w, y0 + 24, f"{t:g}", 15, INK_LIGHT))
        B.append(T(x0 - 14, y0 - t * h + 5, f"{t:g}", 15, INK_LIGHT, anchor="end"))
    B.append(T(x0 + w / 2, y0 + 56 - 6, "모델이 낸 확률" if ko else "Probability the model gave", 17))
    B.append(T(x0 - 54, y0 - h / 2, "실제 양성 비율" if ko else "Actual positive rate", 17, rot=-90))
    B.append(line(r, *P(0, 0), *P(1, 1), INK_LIGHT, 1.3, 0.8, dash=True))
    series = [(0.5, BLUE), (0.2, GREEN), (0.03, RED), ("pooled", INK)]
    for key, col in series:
        pts = [P(a, b) for a, b in CURVES[key]]
        B.append(poly(r, pts, col, 3.0 if key == "pooled" else 2.4))
        for x, y in pts:
            B.append(dot(x, y, col, 4.2))
    # 곡선 끝 라벨
    B.append(T(*P(0.27, 0.62), "과제 A (양성 50%)" if ko else "Task A (50% positive)", 17, BLUE, anchor="end"))
    B.append(T(*P(0.70, 0.47), "과제 B (양성 20%)" if ko else "Task B (20% positive)", 17, GREEN, anchor="start"))
    B.append(T(*P(0.58, 0.07), "과제 C (양성 3%)" if ko else "Task C (3% positive)", 17, RED, anchor="start"))
    B.append(T(*P(0.76, 0.29), "셋을 합친 것" if ko else "All three pooled", 17, INK, anchor="start"))
    B.append(arr(r, *P(0.80, 0.33), *P(0.68, 0.62), INK, 1.2, 7))
    # 오른쪽 설명
    rx = 680
    B.append(box(r, rx, 110, 510, 430, wash="gray", stroke=INK_LIGHT))
    rows = ([("모델이 아는 양성 비율", "24% (세 과제 평균)"),
             ("과제 A", "평균 확률 0.36 · 실제 0.50"),
             ("과제 B", "평균 확률 0.23 · 실제 0.20"),
             ("과제 C", "평균 확률 0.15 · 실제 0.03"),
             ("합친 것", "평균 확률 0.24 · 실제 0.24")] if ko else
            [("Base rate the model assumes", "24% (average of three)"),
             ("Task A", "mean prob 0.36, actual 0.50"),
             ("Task B", "mean prob 0.23, actual 0.20"),
             ("Task C", "mean prob 0.15, actual 0.03"),
             ("Pooled", "mean prob 0.24, actual 0.24")])
    cols = [INK, BLUE, GREEN, RED, INK]
    for i, ((a, b), c) in enumerate(zip(rows, cols)):
        y = 160 + i * 58
        B.append(T(rx + 30, y, a, 19, c, anchor="start"))
        B.append(T(rx + 30, y + 26, b, 17, INK_LIGHT, anchor="start"))
    B.append(T(rx + 255, 476, "세 과제 모두 AUROC 0.90" if ko else "AUROC is 0.90 on all three tasks", 19, AMBER))
    B.append(T(rx + 255, 508, "순서는 맞고 수준만 틀렸다" if ko else "The ranking holds; the level is off", 17, INK_LIGHT))
    B.append(T(60, 620, "합성 데이터, 과제마다 2만 건." if ko else "Synthetic data, 20,000 items per task.", 15, INK_LIGHT, anchor="start"))
    return W, H, "".join(B)


# 그림 3. 내 라벨로 임계값 고르기 (가맹점 심사 예시, 합성 데이터)
ROWS = [  # 임계값, 자동 승인 비율, 검증 건수, 오류, 상한, 통과
    (0.002, "26%", "0/516", "0.89%", True),
    (0.005, "44%", "1/888", "0.75%", True),
    (0.01, "58%", "1/1,166", "0.57%", True),
    (0.02, "72%", "6/1,436", "1.01%", False),
    (0.05, "85%", "14/1,699", "1.49%", False),
]


def d_threshold(lang):
    r = R(6303)
    ko = lang == "ko"
    W, H = 1240, 660
    B = [T(W / 2, 44, "자동 승인 임계값을 내 라벨로 고르기" if ko else "Choosing the auto-approve threshold with your own labels", 28)]
    B.append(ul(r, 380, 860, 58))
    # 왼쪽 흐름
    B.append(box(r, 50, 100, 300, 110, wash="gray", stroke=INK_LIGHT))
    B.append(lines(200, 142, ["심사역 판정이 붙은", "가맹점 3,000곳"] if ko else ["3,000 merchants with", "an underwriter's verdict"], 20))
    B.append(arr(r, 200, 214, 200, 262))
    B.append(box(r, 50, 268, 300, 110, wash="blue", stroke=BLUE))
    B.append(lines(200, 308, ["1,000곳: 확률 다시 맞추기", "(Platt scaling)"] if ko else ["1,000: refit the probabilities", "(Platt scaling)"], 19, BLUE))
    B.append(arr(r, 200, 382, 200, 430))
    B.append(box(r, 50, 436, 300, 130, wash="amber", stroke=AMBER))
    B.append(lines(200, 476, ["2,000곳: 후보마다", "자동 승인 구간 오류율의", "95% 상한 계산"] if ko
                   else ["2,000: for each candidate,", "the 95% upper bound on", "the auto-approve error rate"], 19, AMBER))
    B.append(arr(r, 356, 500, 420, 400, AMBER))
    # 오른쪽 표
    tx, ty = 430, 110
    B.append(box(r, tx, ty, 770, 420, wash=None, stroke=INK_LIGHT))
    heads = (["자동 승인 기준", "자동 승인 비율", "검증 오류", "오류율 상한", "목표 1%"] if ko
             else ["Approve if p <", "Share approved", "Errors", "Upper bound", "Target 1%"])
    xs = [tx + 90, tx + 240, tx + 395, tx + 540, tx + 680]
    for x, hd in zip(xs, heads):
        B.append(T(x, ty + 42, hd, 18, INK))
    B.append(line(r, tx + 20, ty + 62, tx + 750, ty + 62, INK_LIGHT, 1.2))
    for i, (t, share, err, ub, ok) in enumerate(ROWS):
        y = ty + 108 + i * 62
        best = t == 0.01
        if best:
            B.append(f'<rect x="{tx + 14}" y="{y - 32}" width="742" height="50" rx="8" fill="{WASH["green"]}"/>')
        col = GREEN if ok else RED
        B.append(T(xs[0], y, f"{t:g}", 19))
        B.append(T(xs[1], y, share, 19))
        B.append(T(xs[2], y, err, 19, INK_LIGHT))
        B.append(T(xs[3], y, ub, 19, col))
        B.append(T(xs[4], y, ("통과" if ok else "탈락") if ko else ("pass" if ok else "fail"), 19, col))
    B.append(T(tx + 385, ty + 400, "통과한 후보 중 가장 넓은 0.01을 고른다" if ko else "Pick 0.01, the widest candidate that passes", 19, GREEN))
    # 아래 결과
    B.append(T(W / 2 + 190, 578, "앞으로 들어올 가맹점 20만 곳에서: 59% 자동 승인, 그 안의 실제 오류율 0.34%" if ko
               else "On 200,000 future merchants: 59% auto-approved, actual error 0.34% among them", 18, INK))
    B.append(T(W / 2 + 190, 612, "유입 경로, 모델 버전, 질문 문구가 바뀌면 이 표를 다시 만든다" if ko
               else "Rebuild this table when the channel, model version or question wording changes", 17, INK_LIGHT))
    B.append(T(50, 612, "합성 데이터." if ko else "Synthetic data.", 15, INK_LIGHT, anchor="start"))
    return W, H, "".join(B)


def build():
    out = {}
    for lang, suf in (("ko", ""), ("en", "-en")):
        out[f"calib-sources{suf}"] = d_sources(lang)
        out[f"calib-reliability{suf}"] = d_reliability(lang)
        out[f"calib-threshold{suf}"] = d_threshold(lang)
    return out


if __name__ == "__main__":
    from style import wrap
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    figs = build()
    for name, (w, h, body) in figs.items():
        open(os.path.join(outdir, name + ".svg"), "w").write(wrap(w, h, body))
    print("generated", len(figs))
