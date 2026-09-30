---
title: "판매량 예측 (2) 타임 어텐션과 그룹 어텐션 뜯어보기"
description: "시계열 트랜스포머는 셀러 한 명의 매출과 공변량들을 격자로 놓고, 가로로는 시간을 따라, 세로로는 같은 그룹의 시계열끼리 어텐션을 번갈아 건다. 크로노스-2 구조를 기준으로 토큰화부터 그룹 마스크까지 파이토치 코드로 따라가고, 판매 예측에 쓸 때 조심할 것을 정리했다. 일별 분위수를 더하면 월 분위수가 안 되는 이유까지."
pubDatetime: 2026-09-29T23:55:00Z
tags:
  - financial-ai
  - machine-learning
  - time-series
  - llm
---

[1편](/posts/sales-forecasting-1/)에서 크로노스-2가 공변량과 여러 셀러를 다루게 된 건 그룹 어텐션 덕분이라고 했다. 이번엔 그 안을 열어본다.

기준은 크로노스-2 논문이다. 핵심만 남긴 파이토치 코드로 따라가면서, 각 부분이 판매 데이터에서 왜 필요한지를 같이 적었다. 코드는 전부 직접 돌려봤다. 6절에는 작은 실험을 재현할 수 있는 전체 스크립트도 붙였다.

## 1. 시계열을 토큰으로 바꾸기

언어 모델은 단어를 토큰으로 바꿔서 넣는다. 시계열은 숫자라서 토큰을 어떻게 만들지부터 정해야 한다.

시점 하나를 토큰 하나로 쓰는 게 제일 단순하다. 그런데 2년치 일별 매출이면 토큰이 730개라 어텐션 비용이 커진다. 첫 크로노스처럼 값을 구간으로 잘라 어휘를 만드는 방법도 있다. 대신 구간 경계에서 정밀도가 깎인다.

요즘은 대부분 패치를 쓴다.

연속된 P개 시점을 묶어 토큰 하나로 만드는 방식. PatchTST가 널리 퍼뜨린 뒤로 크로노스-볼트, 크로노스-2, 구글의 TimesFM이 다 이렇게 한다.

P=16이면 730개가 46개 정도로 준다. 토큰 하나가 2주 남짓한 매출의 모양을 담는 셈이다.

패치로 자르기 전에 스케일부터 맞춰야 한다. 판매 데이터에선 이게 특히 중요하다. 셀러마다 규모가 수천 배 차이 나고, 프로모션 날 매출은 평소의 몇 배로 튀니까.

크로노스-2는 두 단계로 한다. 시계열마다 과거 구간의 평균과 표준편차로 표준화한다. 그다음 역쌍곡사인(asinh)을 한 번 더 씌운다.

asinh는 0 근처에서는 거의 직선이고, 멀어질수록 로그처럼 눌러준다. 튀는 값의 영향은 줄이면서 0과 음수는 그대로 다룰 수 있다. 매출 0인 날이 흔한 작은 셀러에서 로그를 못 쓰는 문제를 이걸로 피해 간다.

```python
def robust_scale(x, obs):
    """표준화 + asinh. x: (S, T) 과거 값, obs: 관측이면 1"""
    n = obs.sum(-1, keepdim=True).clamp_min(1)
    mu = (x * obs).sum(-1, keepdim=True) / n
    sd = ((((x - mu) * obs) ** 2).sum(-1, keepdim=True) / n).sqrt().clamp_min(1e-6)
    return torch.asinh((x - mu) / sd), mu, sd

def unscale(z, mu, sd):
    return mu + sd * torch.sinh(z)
```

그다음 시계열마다 메타 정보 두 개를 붙인다.

하나는 시간 인덱스다. 예측 첫날을 0으로 두고, 과거는 음수 미래는 양수로 매긴 상대 위치를 최대 컨텍스트 길이로 나눈 값. 다른 하나는 마스크다. 값이 관측됐으면 1, 아니면 0.

이 마스크가 생각보다 많은 일을 한다.

결측 표시는 기본이고, 더 중요한 건 미래 구간이다. 매출 줄은 0이고 미래를 아는 공변량 줄은 1이다. 모델은 이걸 보고 어느 줄이 맞혀야 할 대상이고 어느 줄이 힌트인지 구분한다.

값, 시간 인덱스, 마스크를 각각 P개씩 잘라 이어 붙이면 패치 하나가 3P개 숫자가 된다. 이걸 잔차 MLP에 통과시켜 모델 차원 D짜리 토큰을 만든다.

크로노스-2는 과거 패치와 미래 패치 사이에 REG라는 특수 토큰도 하나 끼운다. 과거와 미래를 가르는 구분자이면서, 어텐션이 딱히 볼 데가 없을 때 쏠려 쉬어 가는 자리(attention sink)다.

```python
class PatchEmbed(nn.Module):
    """[값, 시간 인덱스, 마스크] 패치를 잔차 MLP로 D차원 토큰으로"""
    def __init__(self, P, d):
        super().__init__()
        self.lin = nn.Linear(3 * P, d)
        self.mlp = nn.Sequential(nn.Linear(3 * P, d), nn.GELU(), nn.Linear(d, d))

    def forward(self, v, t, m, P):          # 각 (S, L), L은 P의 배수
        S, L = v.shape
        x = torch.cat([a.reshape(S, L // P, P) for a in (v, t, m)], -1)  # (S, N, 3P)
        return self.lin(x) + self.mlp(x)
```

![시계열이 토큰이 되기까지](/tst-tokenize.svg)

_매출의 미래 패치는 값도 마스크도 0이다. 모델은 이 자리를 채우도록 학습된다._

## 2. 셀러 한 명을 격자로 놓기

토큰을 만들고 나면 셀러 한 명의 입력이 격자 모양이 된다. 세로로는 시계열이 놓인다. 매출, 프로모션 여부, 반품률 같은 것. 가로로는 패치가 놓인다. 시계열이 V개, 패치가 N개면 토큰은 V×N개다.

이 격자에서 정보가 흘러야 하는 방향은 두 가지다.

하나는 매출 줄 안에서 과거 패치가 미래 패치로 흐르는 것. 작년 이맘때 어땠는지, 최근 추세가 어떤지 같은 정보다. 다른 하나는 같은 패치 위치에서 프로모션 줄이 매출 줄로 흐르는 것. 다음 주에 프로모션이 잡혀 있다는 사실 같은 정보다.

크로노스-2는 두 방향에 어텐션을 따로 건다. 가로로 거는 게 타임 어텐션, 세로로 거는 게 그룹 어텐션이다.

![타임 어텐션은 가로로, 그룹 어텐션은 세로로](/tst-time-group.svg)

_그룹 어텐션은 같은 그룹 안에서만 흐른다. 셀러 A의 공변량이 셀러 B에게 새지 않는다._

## 3. 타임 어텐션

타임 어텐션은 익숙한 그 셀프 어텐션이다. 시계열 하나의 패치 N개끼리 서로 본다. 격자를 (시계열 수, 패치 수, D) 모양으로 두고 시계열 축을 배치처럼 취급하면 구현이 끝난다.

```python
class TimeAttention(nn.Module):
    """한 시계열 안에서, 패치끼리"""
    def __init__(self, d, h):
        super().__init__()
        self.norm = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, h, batch_first=True)

    def forward(self, x):                   # x: (S, N, D)
        y = self.norm(x)
        return x + self.attn(y, y, y, need_weights=False)[0]   # 실제로는 여기에 RoPE
```

인과 마스크는 없다.

크로노스-2는 인코더만 있는 구조라, 과거 패치가 미래 패치를 보고 미래 패치도 과거 패치를 본다.

새는 게 없을까? 괜찮다. 매출의 미래 패치는 값이 비어 있으니까. 오히려 미래 구간에 들어온 공변량 정보가 과거 쪽으로도 퍼져 나가는 통로가 된다.

위치 정보는 RoPE(회전 위치 인코딩)로 넣는다. 위 코드에선 핵심만 남기려고 뺐다.

## 4. 그룹 어텐션

그룹 어텐션은 격자를 돌려서 본다. 패치 위치 하나를 고정하고, 그 위치에 있는 같은 그룹의 시계열끼리 어텐션을 건다. 셀러 A의 매출 둘째 패치는 셀러 A의 프로모션 둘째 패치, 반품률 둘째 패치를 본다.

구현에서 재밌는 대목은 그룹마다 크기가 다르다는 점이다. 어떤 셀러는 공변량이 셋이고, 어떤 셀러는 열이다.

그룹마다 패딩해서 크기를 맞출 수도 있는데, 크로노스-2는 다른 길을 택했다. 배치 안의 모든 시계열을 한 줄로 편다. 시계열마다 그룹 ID를 붙인다. 그 ID를 2차원 마스크로 바꾼다.

그룹 ID가 [0, 0, 0, 1, 1]이면 앞의 셋끼리, 뒤의 둘끼리만 서로 볼 수 있는 블록 대각 마스크가 나온다.

```python
class GroupAttention(nn.Module):
    """같은 그룹의 시계열끼리, 같은 패치 위치에서"""
    def __init__(self, d, h):
        super().__init__()
        self.norm = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, h, batch_first=True)

    def forward(self, x, group_ids):        # x: (S, N, D), group_ids: (S,)
        y = self.norm(x).transpose(0, 1)    # (N, S, D): 패치 위치마다 시계열이 한 줄로
        blocked = group_ids[:, None] != group_ids[None, :]   # (S, S), True면 못 본다
        y = self.attn(y, y, y, attn_mask=blocked, need_weights=False)[0]
        return x + y.transpose(0, 1)
```

transpose 한 번으로 축이 바뀌는 게 전부다. 타임 어텐션에서 배치였던 시계열 축이 여기선 시퀀스가 된다. 시퀀스였던 패치 축은 배치가 되고.

위치 인코딩은 넣지 않는다. 그룹 안의 시계열에는 순서가 없으니까. 매출이 첫 줄이든 셋째 줄이든 결과가 같아야 한다.

마스크가 제대로 막는지는 쉽게 확인할 수 있다. 그룹 ID를 [0, 0, 1, 1, 1]로 주고, 그룹 1의 입력을 크게 흔든 다음 블록을 통과시켜 봤다. 그룹 1의 출력은 16 가까이 움직였다. 그룹 0의 출력은 정확히 0만큼 변했다.

셀러 B의 데이터가 셀러 A의 예측에 조금도 새지 않는다는 얘기다.

두 어텐션을 번갈아 쌓으면 블록 하나가 된다.

```python
class Block(nn.Module):
    def __init__(self, d, h):
        super().__init__()
        self.time = TimeAttention(d, h)
        self.group = GroupAttention(d, h)
        self.ff = nn.Sequential(nn.LayerNorm(d), nn.Linear(d, 4 * d),
                                nn.GELU(), nn.Linear(4 * d, d))

    def forward(self, x, group_ids):
        x = self.time(x)
        x = self.group(x, group_ids)
        return x + self.ff(x)
```

## 5. 격자 전체에 한 번에 걸지 않는 이유

V×N개 토큰을 한 줄로 펴서 전부 서로 보게 하면 되지 않을까?

그러면 비용이 (V·N)²으로 불어난다. 실제로 Moirai-1이 다변량을 이렇게 펴서 다뤘고, 크로노스-2 논문은 이게 변수가 많을 때 확장성을 제한한다고 짚는다.

가로와 세로로 나누면 타임 어텐션이 V·N², 그룹 어텐션이 N·V²라 훨씬 싸다. 이미지 모델에서 축 방향 어텐션(axial attention)이라고 부르던 것과 같은 발상이다.

숫자로 보면 체감이 된다. 2년치 일별 매출에 90일 예측, 패치 16이면 N이 52 정도 된다. 매출에 공변량 9개를 붙여 V가 10이면, 전체 어텐션은 서로 주고받는 쌍이 27만 개다. 나눠서 걸면 3만 2천 개로 8배쯤 줄어든다.

셀러 한 명의 상품 50개를 한 그룹으로 묶으면(V=50) 차이가 더 벌어진다. 676만 개 대 26만 5천 개, 25배다.

![그룹 ID가 마스크가 된다](/tst-group-mask.svg)

_변수가 많아질수록 나눠서 거는 쪽이 압도적으로 싸다._

나누면 잃는 게 있을 것 같지만, 층을 번갈아 쌓으면 대각선 방향으로도 정보가 흐른다. 프로모션 줄의 다음 달 패치가 매출 줄의 다음 달 패치로 가는 건 그룹 어텐션 한 번이면 된다.

프로모션 줄의 작년 패치가 매출 줄의 올해 패치로 가려면 두 번 움직인다. 그룹 어텐션으로 건너고, 타임 어텐션으로 옮겨 간다. 블록을 여러 개 쌓는 이유다.

## 6. 공변량이 들어가는 방식

그룹 어텐션이 생기고 나면 공변량을 넣는 방법이 의외로 단순해진다. 공변량도 그냥 같은 그룹에 든 시계열이다. 다른 건 미래 구간에 값이 있느냐 없느냐뿐.

매출은 과거에만 값이 있고 미래는 마스크 0이다. 지나야 아는 공변량(반품률, 평점)도 미래는 마스크 0. 미래를 아는 공변량(프로모션 일정, 공휴일)은 미래 구간까지 값이 차 있고 마스크가 1이다. 모델은 마스크를 보고 이 줄이 뭔지 알아서 판단한다.

나머지 세부는 이렇다. 범주형 공변량은 타깃이 하나일 땐 타깃 인코딩으로 숫자로 바꿔서 같은 식으로 넣는다. 손실은 매출 줄의 미래 패치에서만 계산하고, 공변량 줄에 대한 예측은 버린다. 분위수는 0.01부터 0.99까지 21개를 한 번에 낸다.

정말 작동하는지 보려고 작은 실험을 돌렸다. 매출에는 주간 계절성을 넣었다. 프로모션이 있는 날은 매출이 2.5배가 된다. 프로모션 일정은 미래까지 알려진 공변량으로 줬다. 위 블록 두 개로 만든 작은 모델(임베딩 64차원)을 CPU에서 600스텝씩 학습시켰다.

| 설정 | 분위수 손실 (정규화) | 실제값이 P10 아래로 떨어진 비율 |
| --- | --- | --- |
| 그룹 없음 (매출 혼자) | 0.091 | 12.5% |
| 매출과 프로모션을 한 그룹으로 | 0.029 | 9.3% |

모델도 데이터도 같고 그룹 ID만 다르다.

매출 혼자서는 다음 주 프로모션을 알 길이 없다. 그러니 모든 날을 비슷하게 예측하고 불확실성을 넓게 잡는다. 같은 그룹에 넣으면 프로모션 패치에서 정보를 받아 매출이 뛰는 날을 짚어낸다. 손실은 3분의 1 수준으로 줄었고, P10 커버리지도 목표인 10%에 가까워졌다.

<details>
<summary>실험 전체 코드 (파이토치, CPU에서 1분 안쪽)</summary>

```python
import math, torch, torch.nn as nn

def robust_scale(x, obs):
    n = obs.sum(-1, keepdim=True).clamp_min(1)
    mu = (x * obs).sum(-1, keepdim=True) / n
    sd = ((((x - mu) * obs) ** 2).sum(-1, keepdim=True) / n).sqrt().clamp_min(1e-6)
    return torch.asinh((x - mu) / sd), mu, sd

class PatchEmbed(nn.Module):
    def __init__(self, P, d):
        super().__init__()
        self.lin = nn.Linear(3 * P, d)
        self.mlp = nn.Sequential(nn.Linear(3 * P, d), nn.GELU(), nn.Linear(d, d))
    def forward(self, v, t, m, P):
        S, L = v.shape
        x = torch.cat([a.reshape(S, L // P, P) for a in (v, t, m)], -1)
        return self.lin(x) + self.mlp(x)

class TimeAttention(nn.Module):
    def __init__(self, d, h):
        super().__init__()
        self.norm, self.attn = nn.LayerNorm(d), nn.MultiheadAttention(d, h, batch_first=True)
    def forward(self, x):
        y = self.norm(x)
        return x + self.attn(y, y, y, need_weights=False)[0]

class GroupAttention(nn.Module):
    def __init__(self, d, h):
        super().__init__()
        self.norm, self.attn = nn.LayerNorm(d), nn.MultiheadAttention(d, h, batch_first=True)
    def forward(self, x, group_ids):
        y = self.norm(x).transpose(0, 1)
        blocked = group_ids[:, None] != group_ids[None, :]
        y = self.attn(y, y, y, attn_mask=blocked, need_weights=False)[0]
        return x + y.transpose(0, 1)

class Block(nn.Module):
    def __init__(self, d, h):
        super().__init__()
        self.time, self.group = TimeAttention(d, h), GroupAttention(d, h)
        self.ff = nn.Sequential(nn.LayerNorm(d), nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))
    def forward(self, x, group_ids):
        x = self.time(x)
        x = self.group(x, group_ids)
        return x + self.ff(x)

class Tiny(nn.Module):
    def __init__(self, P=8, d=64, h=4, n_blocks=2, qs=(0.1, 0.5, 0.9)):
        super().__init__()
        self.P, self.qs = P, torch.tensor(qs)
        self.embed = PatchEmbed(P, d)
        self.blocks = nn.ModuleList(Block(d, h) for _ in range(n_blocks))
        self.head = nn.Sequential(nn.LayerNorm(d), nn.Linear(d, P * len(qs)))
    def forward(self, v, t, m, group_ids):
        x = self.embed(v, t, m, self.P)
        for b in self.blocks:
            x = b(x, group_ids)
        return self.head(x)

def pinball(pred, y, qs):
    d = y.unsqueeze(-1) - pred
    return torch.maximum(qs * d, (qs - 1) * d).mean()

T, H, P = 64, 16, 8   # 과거 64일, 예측 16일, 패치 8

def make_batch(B):
    t = torch.arange(T + H).float()
    base = 100 * (1 + 0.3 * torch.sin(2 * math.pi * t / 7))       # 주간 계절성
    promo = (torch.rand(B, T + H) < 0.15).float()                 # 미래까지 알려진 프로모션
    level = torch.exp(torch.randn(B, 1))                          # 셀러마다 규모가 다르다
    y = level * base * (1 + 1.5 * promo) * torch.exp(torch.randn(B, T + H) * 0.1)
    return y, promo

def to_inputs(y, promo, use_group):
    B = y.shape[0]
    tgt_obs = torch.cat([torch.ones(B, T), torch.zeros(B, H)], 1)  # 매출의 미래는 가린다
    cov_obs = torch.ones(B, T + H)                                 # 프로모션의 미래는 보인다
    zt, mu, sd = robust_scale(y[:, :T], tgt_obs[:, :T])
    zt = torch.cat([zt, torch.zeros(B, H)], 1)
    zc, pm, ps = robust_scale(promo[:, :T], cov_obs[:, :T])
    zc = torch.cat([zc, torch.asinh((promo[:, T:] - pm) / ps)], 1)
    v = torch.stack([zt, zc], 1).reshape(2 * B, T + H)            # [매출, 프로모션] 쌍으로
    m = torch.stack([tgt_obs, cov_obs], 1).reshape(2 * B, T + H)
    tix = ((torch.arange(T + H) - T) / 2048.0).expand(2 * B, -1)  # 예측 시작점이 0
    g = torch.arange(B).repeat_interleave(2) if use_group else torch.arange(2 * B)
    return v, tix, m, g, mu, sd

def run(use_group, steps=600, B=64):
    torch.manual_seed(1)
    model = Tiny(P=P)
    opt = torch.optim.AdamW(model.parameters(), 3e-3)
    for _ in range(steps):
        y, promo = make_batch(B)
        v, tix, m, g, mu, sd = to_inputs(y, promo, use_group)
        out = model(v, tix, m, g)[0::2, T // P:].reshape(B, H, 3)  # 매출 줄의 미래 패치만
        loss = pinball(out, torch.asinh((y[:, T:] - mu) / sd), model.qs)
        opt.zero_grad(); loss.backward(); opt.step()
    torch.manual_seed(123)
    with torch.no_grad():
        y, promo = make_batch(2048)
        v, tix, m, g, mu, sd = to_inputs(y, promo, use_group)
        out = model(v, tix, m, g)[0::2, T // P:].reshape(2048, H, 3)
        pred = mu.unsqueeze(-1) + sd.unsqueeze(-1) * torch.sinh(out)
        wql = pinball(pred, y[:, T:], model.qs).item() / y[:, T:].abs().mean().item()
        below_p10 = (y[:, T:] < pred[..., 0]).float().mean().item()
    return wql, below_p10

for use_group in (False, True):
    wql, below = run(use_group)
    print(f"group={use_group}: 분위수 손실 {wql:.3f}, P10 아래 {below:.1%}")

```

</details>

그룹을 무엇으로 묶느냐가 곧 과제를 정한다는 것도 여기서 나온다. 크로노스-2 논문은 그룹의 예로 네 가지를 든다. 시계열 하나(단변량). 출처나 메타데이터를 공유하는 시계열들(교차 학습). 동역학을 공유하는 변수들(다변량). 타깃과 공변량(공변량을 쓰는 예측).

판매 쪽으로 옮기면 셀러 한 명과 그 공변량을 한 그룹에 두는 게 기본이다. 같은 셀러의 상품들을 묶을 수도, 같은 업종 셀러들을 묶을 수도 있다.

마지막 경우가 신규 셀러에게 특히 쓸모 있다. 이력이 두세 달인 셀러를 혼자 두면 예측이 약하다. 같은 업종의 비슷한 셀러들과 한 그룹에 넣으면 그 셀러들의 패턴을 빌려 온다. 전학 온 첫날 같은 반 친구들 시간표를 보고 하루를 짐작하는 것과 비슷하다.

크로노스-2 논문도 결론에서 메타데이터나 임베딩으로 비슷한 시계열을 찾아 한 그룹으로 묶는 검색 증강 예측(retrieval-augmented forecasting)을 앞으로의 방향으로 꼽았다. 관련 없는 셀러를 섞으면 노이즈만 는다는 건 조심해야 하고.

## 7. 일별 분위수를 더하면 월 분위수가 안 된다

대출 한도는 보통 30일이나 90일 합계로 잡는다. 그런데 크로노스-볼트나 크로노스-2는 시점마다 분위수를 따로 낸다.

그럼 30일 합계의 P10은 일별 P10을 더한 값일까?

아니다. 일 매출 중앙값이 100만 원인 셀러로 시뮬레이션해 봤다. 날짜끼리 상관이 없다면 일별 P10을 30일 더한 값은 1,390만 원이다. 실제 30일 합계의 P10은 3,060만 원. 절반 넘게 낮게 잡힌다.

날짜 간 상관이 0.8이어도 40%, 0.95여도 20% 낮다. 이렇게 한도를 잡으면 체계적으로 덜 빌려주게 된다.

![일별 P10을 더하면 30일 P10이 아니다](/tst-quantile-sum.svg)

_날짜 간 상관이 낮을수록 차이가 커진다._

일별 P10을 다 더한다는 건 30일 내내 매일 나쁜 날이 온다고 가정하는 셈이다. 한 달 수입을 매일 제일 안 풀린 날 기준으로 계산하는 것과 같다. 실제로는 나쁜 날과 좋은 날이 섞이면서 합계는 덜 흔들린다. 반대로 P90을 더하면 과하게 높게 잡힌다.

그래서 한도에 쓸 거라면 예측 대상을 처음부터 필요한 기간의 합계로 두는 게 맞다. 주별이나 월별로 집계한 시계열을 넣고 그 합계의 분위수를 바로 예측하는 식이다.

아니면 첫 크로노스처럼 미래 경로를 샘플로 여러 개 뽑아주는 모델을 써도 된다. 경로마다 합계를 낸 다음 그 분포에서 분위수를 읽으면 된다. 시점별 분위수만 내는 모델이라면 앞쪽밖에 방법이 없다.

## 8. 그 밖에 조심할 것

### 미래를 아는 공변량은 정말 알아야 한다

심사 시점에 실제로 알 수 있는 것만 미래 구간에 넣어야 한다. 이미 잡힌 프로모션 일정이나 공휴일은 된다. 광고비 집행 실적이나 실제 방문자 수는 안 된다.

백테스트에선 이런 게 섞여도 성능이 좋아 보이기만 한다. 그래서 잡아내기가 어렵다. 대출 모델에서 자주 생기는 누수라, 피처마다 "이 값을 심사 당일에 알 수 있나"를 따로 확인하는 수밖에 없다.

### 0이 많은 셀러는 집계 단위부터

asinh 스케일링이 0을 다룰 수는 있다. 그래도 매출이 있는 날보다 없는 날이 많은 셀러를 일별로 넣으면 모델이 볼 게 별로 없다.

주별로 묶으면 0이 줄고 패턴이 살아난다. 한도가 월 단위라면 굳이 일별로 예측할 이유도 없고, 7절의 합산 문제까지 같이 풀린다.

### 평가는 한도에 쓸 분위수의 커버리지로

기준일을 여러 번 옮겨 가며 롤링 백테스트를 돌린다. 분위수 손실 같은 전체 지표와 함께, 한도에 쓸 분위수의 커버리지를 따로 본다.

P10으로 한도를 잡는다면 제일 중요한 숫자는 하나다.

실제 매출이 P10 아래로 떨어진 비율이 10% 근처인지. 1편의 LightGBM 실험처럼 기간이 바뀌면 이게 쉽게 어긋나니까, 최근 구간으로 보정하는 단계를 두는 게 좋다.

### 비교는 제로샷부터

사전학습 모델은 학습 없이 바로 돌려볼 수 있다. 같은 백테스트에 LightGBM과 크로노스-2 제로샷을 올려서, 셀러 구간별(이력 길이, 규모, 간헐성)로 어디서 무엇이 이기는지부터 본다. 파인튜닝은 그 차이를 보고 정해도 늦지 않다.

크로노스-2는 1억 2천만 파라미터라 중급 GPU 한 장이면 돌아간다. 2,800만 파라미터짜리 작은 버전은 성능이 크게 안 떨어지면서 두 배 가까이 빠르다고 한다.

## 9. 개인적인 견해

그룹 어텐션을 뜯어보면서 제일 흥미로웠던 건, 공변량을 쓰는 예측과 다변량 예측과 교차 학습이 사실 같은 연산이었다는 점이다. 셋은 오랫동안 서로 다른 문제로 따로 연구돼 왔다. 크로노스-2에서는 그룹 ID를 어떻게 주느냐만 다르다.

구조는 그대로고, 무엇을 같은 그룹에 넣느냐가 과제를 정한다.

그러면 모델을 설계하던 일의 상당 부분이 데이터를 어떻게 묶을지 정하는 일로 옮겨 간다. 어떤 공변량이 정말 미래에 알려져 있는지. 어떤 셀러들이 서로 닮았는지. 한도에 필요한 게 며칠짜리 합계인지. 이런 건 사전학습 모델이 알려주지 않는다.

결국 group_ids 한 줄을 어떻게 채우느냐가 레이어를 몇 층 쌓느냐보다 결과를 더 크게 바꾸지 싶다. 그리고 그 한 줄은 판매 데이터를 오래 들여다본 사람이 제일 잘 채운다.

---

**함께 보면 좋은 글:**

- [판매량 예측 (1) 트리 모델부터 크로노스까지](/posts/sales-forecasting-1/)
- [LLM은 어떻게 채점하나: 평가 방법 11가지를 네 계열로 정리했다](/posts/llm-evaluation-methods/)

## 참고 자료

- [Chronos-2: From Univariate to Universal Forecasting (Ansari et al., 2025)](https://arxiv.org/abs/2510.15821)
- [Chronos: Learning the Language of Time Series (Ansari et al., 2024)](https://arxiv.org/abs/2403.07815)
- [A Time Series is Worth 64 Words: Long-term Forecasting with Transformers (PatchTST, Nie et al., 2023)](https://arxiv.org/abs/2211.14730)
- [Axial Attention in Multidimensional Transformers (Ho et al., 2019)](https://arxiv.org/abs/1912.12180)
- [Unified Training of Universal Time Series Forecasting Transformers (Moirai, Woo et al., 2024)](https://arxiv.org/abs/2402.02592)
- [chronos-forecasting (GitHub)](https://github.com/amazon-science/chronos-forecasting)

_본 글은 2026년 9월 30일 기준 크로노스-2 기술 보고서를 바탕으로 작성했다. 본문의 코드는 구조를 설명하려고 핵심만 남긴 것이라 실제 구현과 다르다(RoPE, REG 토큰, 잔차 블록 세부 등). 그룹 격리 확인, 장난감 실험, 분위수 합산 시뮬레이션은 모두 직접 돌린 결과이며 실제 셀러 데이터에서는 수치가 달라진다._
