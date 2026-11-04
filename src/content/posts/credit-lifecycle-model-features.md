---
title: "같은 한도 소진율 80%, 모델마다 뜻이 다르다: 마케팅부터 추심까지 신용 모델 5종의 변수 설계"
description: "한도의 80%를 쓰는 고객은 마케팅 모델에는 수요 신호이고 신청 모델에는 부담 신호다. 신용 모델 다섯 개를 결정, 변수, 라벨, 사용 가능 시점으로 다시 정리하고, Plaid, Upstart, 카카오뱅크, Nubank, Tala 등이 공개한 변수와 라벨, 수치를 모델별로 모았다."
pubDatetime: 2026-11-04T01:30:00Z
tags:
  - financial-ai
  - credit
  - fintech
  - machine-learning
---

카드 한도의 80%를 쓰고 있는 고객이 한 명 있다.

마케팅 모델에서 이 사람은 돈이 필요해서 대출 제안에 반응할 가능성이 큰 고객이고, 신청 모델에서는 이미 빚 부담이 큰 신청자다. 행동 모델은 80%라는 숫자보다 석 달 전에 40%였는지를 더 궁금해하고, 추심 모델은 연락했을 때 갚을 여력이 남아 있는지를 본다. 같은 변수의 뜻이 이렇게 갈리는 건 모델마다 묻는 질문이 다르기 때문이다.

스코어카드 변수를 정리한 자료는 많지만 대개 모델별 변수 이름을 늘어놓는 데서 끝나서, 막상 만들려고 하면 계산식과 기준 시점부터 막힌다. 그래서 변수 이름보다 먼저 정해야 할 것들, 즉 결정, 라벨, 사용 가능 시점부터 정리했다. 뒤쪽 6절에는 핀테크 회사와 연구자들이 실제로 공개한 변수와 라벨, 수치를 모델별로 모았다.

## 1. 모델 다섯 개는 서로 다른 결정을 내린다

업계에서는 신청평점을 A 스코어, 행동평점을 B 스코어, 추심평점을 C 스코어라고 부르고, 여기에 사기 모델과 마케팅 모델을 더해 다섯 개로 나누는 경우가 많다. 나누는 기준은 고객 생애주기의 어느 시점에서 어떤 결정을 내리느냐다.

| 모델 | 점수를 내는 때 | 내리는 결정 | Y의 예 | 점수 다음 행동 |
|------|------|------|------|------|
| 마케팅 | 제안 전 | 누구에게 어떤 제안을 보낼까 | 제안 때문에 늘어난 전환, 취급액 | 발송 대상, 혜택 금액 배정 |
| 사기 | 신청·거래 순간 | 실재하는 사람인가, 갚을 뜻이 있나 | 사후에 확정된 사기 판정 | 거절, 추가 인증, 심사 대기열 |
| 신청(A) | 신청 심사 | 승인, 금리, 한도 | 6~24개월 안의 연체 | 컷오프, 금리 구간, 한도 승수 |
| 행동(B) | 실행 후 매월 또는 매일 | 한도 증액·감액, 조기 경보 | 2~12개월 안의 연체 | 증액 대상 선정, 감액, 모니터링 |
| 추심(C) | 연체 후 매일 | 누구에게 어떤 조치를 할까 | 조치 때문에 늘어난 회수 | 통화 배정, 채널 선택, 분할 상환 제안 |

사기와 신청은 같은 순간에 돌아가도 묻는 내용이 다르다. 사기 모델은 갚을 뜻이 있는지를, 신청 모델은 갚을 능력이 있는지를 보기 때문에 두 라벨이 섞이면 양쪽 모델의 결과를 해석하기 어려워진다. 마케팅과 추심은 표에 적은 대로 Y 자체가 예측값이 아니라 조치의 효과라는 점이 다르다. 이 차이는 5절에서 다시 다룬다.

흐름도는 보통 마케팅에서 추심까지 직선으로 그리지만, 실제로는 아래처럼 되돌아오는 길이 있다.

![신용 모델 다섯 개의 흐름. 앞으로 가는 화살표 외에 추심에서 사기 라벨로, 행동 점수에서 마케팅으로 되돌아오는 화살표가 있고, 거절 건은 학습 표본에서 빠진다](/creditm-loop.svg)
_행동 점수는 한도 증액과 교차 판매로, 추심 결과는 사기 라벨로 돌아가고, 거절 건의 결과는 관측되지 않는다._

거절자의 결과가 없다는 점은 신청 모델을 다시 만들 때마다 따라다니는 편향이고, [Lift 글](/posts/risk-metrics-lift/)에서 다룬 문제와 같은 뿌리다.

## 2. 변수를 데이터 출처로 묶으면 겹치는 곳이 보인다

모델별로 변수 목록을 따로 적으면 같은 변수가 다섯 번 나오고, 어떤 건 데이터 출처로, 어떤 건 내용으로, 어떤 건 파생 방식으로 분류되어 축이 섞이기 쉽다. 출처를 기준으로 묶으면 다섯 모델이 한 표에 들어간다.

![데이터 출처 여섯 개와 모델 다섯 개의 표. 신청 모델은 신청서와 신용정보, 사기 모델은 기기와 관계망, 행동과 추심은 자사 거래 이력과 접촉 이력을 주로 쓴다](/creditm-sources.svg)
_흔한 구성을 정리한 것이고 회사와 상품에 따라 다르다._

쓸 수 있는 시점과 비용은 대개 출처에서 정해진다. 기기 신호는 세션이 열리는 순간 있지만 CB 정보는 조회 비용과 동의가 필요해서, 마케팅 단계에서는 쓰기 어려운 경우가 많다. 신규 신청자에게는 자사 이력이 없으니 신청 모델과 행동 모델의 차이도 여기서 바로 드러난다. Revolut도 자사 거래 시퀀스로 사전학습한 PRAGMA의 경계로 이력이 없는 신규 신청자와 신용정보 같은 표 데이터를 꼽고, 표 데이터용 모델과 결합한다고 밝혔다. ([Revolut](https://www.revolut.com/blog/post/fromresearchtorealtime/)) 규제와 플랫폼 정책도 대개 출처 단위로 걸리기 때문에, 7절의 제약을 적용할 때도 이 분류가 편하다.

## 3. 같은 변수가 모델마다 다른 뜻이 된다

Y가 다르면 같은 값의 방향도 달라진다. 아래 표는 흔히 쓰는 변수 다섯 개를 모델별로 어떻게 읽는지 정리한 것이다.

| 변수 | 마케팅 | 사기 | 신청 | 행동 | 추심 |
|------|------|------|------|------|------|
| 한도 소진율 높음 | 자금 수요 신호 | 신규 계좌의 급격한 소진이면 의심 | 부채 부담 | 수준보다 상승 추세 | 상환 여력이 적음 |
| 최근 신용 조회 많음 | 돈을 찾는 중 | 단시간 집중이면 명의도용 의심 | 자금 압박 | 새로 늘면 타사 부채 증가 | 다른 채권자와 경쟁 중 |
| 야간 활동 | 발송 시간대 힌트 | 평소와 다를 때만 의미 | 약한 신호 | 습관이 바뀔 때만 의미 | 연락 가능 시간대 |
| 기기 변경 | 거의 안 씀 | 고액 거래 직전이면 강한 신호 | 신규 고객은 비교 기준 없음 | 번호 변경과 겹치면 주의 | 연락 두절 신호 |
| 조기 상환 | 갈아타기 이탈 위험 | 직후 한도 재사용이면 의심 | 과거 이력이면 우량 신호 | 저금리 대환 가능성 | 일부 상환은 상환 의사 신호 |

이 표는 출발 가설이지 정답이 아니다. 포트폴리오마다 구간별 불량률이나 효과를 그려 방향을 확인해야 한다. 그래도 모델을 가로질러 놓고 보면 위험과 반응이 다른 축이라는 점이 드러난다. 콜롬비아 은행의 문자 실험에서 조치 효과는 평균 약 6일 연체한 차주 중 신용점수가 높고 무담보·단기 상품을 쓰는 사람에게 몰렸고, 정상 상환자에게 보낸 문자의 효과는 0에 가까웠다. ([Barboni 외, 워킹페이퍼](https://warwick.ac.uk/fac/soc/economics/research/centres/cage/manage/publications/wp633.2022.pdf)) 위험 점수가 높은 순서대로 연락하는 운영과는 다른 그림이다.

단조 제약을 모델끼리 공유할 수 없는 것도 같은 이유다. Plaid는 신용 위험 모델의 변수마다 단조 관계를 걸었는데([Plaid](https://plaid.com/blog/how-we-built-lendscore/)), 이건 Y가 연체일 때 맞는 제약이다. 소진율처럼 위험 모델과 수요 모델에서 해석이 갈리는 변수에 같은 방향 제약을 그대로 옮기면 마케팅 모델이 수요 신호를 거꾸로 배우게 된다.

## 4. 한도 소진율 하나를 끝까지 정의해 보면

변수 이름은 한 줄이지만 실제로 만들려면 정할 것이 많다. 소진율을 예로 들면 다음과 같다.

- **계산식:** 잔액 나누기 한도. 잔액은 명세서 기준인지 일평균인지, 한도는 부여 한도인지 사용 가능 한도인지 정한다.
- **분모가 0일 때:** 한도가 0인 사람의 소진율은 0%가 아니라 정의되지 않는 값이다. 결측 표시를 따로 둔다.
- **기간:** 한 시점 값, 3개월 평균, 3개월 기울기는 서로 다른 변수다. 행동 모델에서는 뒤의 둘이 더 많이 쓰인다.
- **기준 시점:** 점수를 내는 순간에 이미 시스템에 들어와 있던 값만 쓴다. 명세서 날짜가 아니라 데이터가 도착한 날짜가 기준이다.
- **한도 변경:** 증액한 달에는 분모가 바뀌어 소진율이 떨어져 보인다. 행동 모델의 기울기 변수에서 특히 문제가 된다.

네 번째가 제일 자주 틀린다. 아래 코드는 도착 지연을 사흘로 두고 기준 시점에 볼 수 있던 명세서만 붙인다.

```python
import pandas as pd

def utilization_asof(apps, stmts, lag_days=3):
    # 기준 시점에 이미 들어와 있던 명세서로만 만든다
    stmts = stmts.assign(available_at=stmts.stmt_date + pd.Timedelta(days=lag_days))
    m = pd.merge_asof(
        apps.sort_values("scored_at"),
        stmts.sort_values("available_at"),
        left_on="scored_at", right_on="available_at", by="customer_id",
        direction="backward", tolerance=pd.Timedelta(days=60),
    )
    m["util"] = (m.balance / m.limit.where(m.limit > 0)).clip(upper=1.5)
    m["no_limit"] = m.limit.eq(0)      # 한도가 0인 사람: 소진율 0%와 다르다
    m["no_stmt"] = m.limit.isna()      # 명세서가 없는 사람: 신규 고객이나 지연
    return m
```

가상의 고객으로 돌려 보면 3월 2일에 신청한 사람에게는 2월 말 명세서가 아니라 1월 말 명세서가 붙는다. 2월 말 명세서는 3월 3일에야 들어오기 때문이다. 월말 기준으로 테이블을 조인하면 이 사람의 2월 말 값이 그대로 들어가는데, 이런 데이터 누수(data leakage)는 개발 표본에서는 티가 나지 않고 운영에서만 성능을 떨어뜨린다. Nubank도 BNPL 선납이 거래 시점을 바꿔 미래 정보가 새어 들어간 사례를 잡았다고 적었다. ([nuFormer 논문 v3](https://arxiv.org/html/2507.23267v3))

같은 형식으로 모델별 대표 변수를 적으면 다음과 같다. 계산식과 기간은 예시이고, 회사마다 다르다.

| 모델 | 변수 | 계산 예 | 쓸 수 있는 시점 | 주의할 점 |
|------|------|------|------|------|
| 마케팅 | 한도·금리 화면 조회 수 | 최근 14일 진입 횟수 | 발송 직전 | 이전 캠페인이 유도한 조회가 섞인다 |
| 마케팅 | 과거 제안 반응률 | 최근 6개월 전환 수 / 발송 수 | 발송 직전 | 발송이 0건이면 결측으로 둔다 |
| 사기 | 기기당 계정 수 | 최근 7일 같은 기기의 계정 수 | 세션 시작 | 가족, 공용 기기 |
| 사기 | 첫 로그인 후 신청까지 시간 | 초 단위 | 신청 제출 | 재가입 고객 구분 |
| 사기 | 입금 계좌 공유 신청 수 | 최근 30일 같은 입금 계좌의 신청 수 | 신청 제출 | 라벨이 확정되지 않은 신청이 섞인다 |
| 신청 | 최근 3개월 신용 조회 수 | 조회 건수, 목적별 분리 | CB 조회 후 | 금리 비교 조회와 실제 신청 구분 |
| 신청 | 소득 규칙성 | 월별 입금액의 변동계수 | 계좌 연결 후 | 프리랜서와 자영업자에게 불리할 수 있다 |
| 신청 | DSR | 연간 원리금 / 연소득 | 심사 | 소득 증빙 방식에 따라 달라진다 |
| 행동 | 소진율 3개월 기울기 | 월말 소진율의 회귀 기울기 | 월 스냅샷 | 한도 변경 달 처리 |
| 행동 | 최소 결제 연속 횟수 | 최소 금액만 낸 연속 회차 | 결제일 후 | 리볼빙 약정 고객 구분 |
| 행동 | 급여성 입금 중단 일수 | 마지막 급여성 입금 후 경과일 | 일 단위 | 주거래가 아닌 고객은 의미가 약하다 |
| 추심 | 연체 일수 구간 | 2~10일, 11~25일 등 | 매일 | 구간별로 다른 문제로 다룬다 |
| 추심 | 약속 이행률 | 이행 건수 / 약속 건수 | 첫 접촉 후 | 연체 첫날에는 값이 없다 |
| 추심 | 최근 앱 로그인 경과일 | 일 단위 | 매일 | 앱 알림 발송의 영향을 받는다 |

약속 이행률은 회수 예측에서 강한 변수로 자주 꼽히지만, 연락이 닿은 뒤에야 생기는 값이라 연체 첫날의 배정 모델에는 넣을 수 없다. 학습 표본에서 연체 30일째 값까지 함께 집계해 버리면 첫날 모델이 미래를 보게 된다.

## 5. 라벨과 기간에서 갈리는 것들

변수보다 먼저 정해야 하는 것이 기준 시점과 라벨이다. 아래 그림의 세로선 왼쪽만 변수로 쓸 수 있다.

![모델 다섯 개의 기준 시점과 관측 기간, 성과 기간을 나란히 그린 그림](/creditm-windows.svg)
_길이는 흔한 구성을 나타낸 것이고 비율에 맞춘 것은 아니다. 공개 사례의 실제 값은 6절에 적었다._

**불량 정의는 롤레이트로 정한다.** 연체 30일에 들어간 건 중 다수가 회복한다면 30일을 불량으로 잡았을 때 라벨에 일시적 지연이 많이 섞인다. 아래는 설명용 가상 숫자다.

| 단계 | 건수 | 앞 단계에서 넘어온 비율 |
|------|------|------|
| 30일 이상 연체 | 1,000 | - |
| 60일 이상 | 420 | 42% |
| 90일 이상 | 340 | 81% |
| 120일 이상 | 315 | 93% |
| 상각 | 300 | 95% |

이 숫자라면 90일부터 대부분 그대로 굴러가므로 90일을 불량으로 잡는 근거가 된다. 다만 상품의 만기가 짧으면 성과 기간과 불량 기준도 함께 짧아진다. Plaid는 일반 모델을 12개월 안의 90일 이상 연체로 만들었지만, BNPL 같은 단기 상품용 모델에는 6개월 안의 60일 이상 연체를 썼다. ([LendScore](https://plaid.com/blog/how-we-built-lendscore/), [LendScore 2](https://plaid.com/blog/instant-link-next-generation-lendscore/)) Affirm은 첫 납부 4일 연체(FPDQ4) 같은 조기 지표와 60일 연체(DQ60) 같은 장기 지표를 한 모델의 여러 출력으로 함께 학습한다. ([Affirm](https://tech.affirm.com/learning-richer-credit-representations-with-transformers-at-affirm-c774e7c1cea6)) 라벨이 늦게 도착하는 문제에 대한 답 중 하나다.

**사기와 신용의 경계는 라벨에서 가장 흐리다.** 첫 납부 연체(FPD)를 사기 대리 라벨로 쓰는 일이 흔한데, 정의부터 통일되어 있지 않다. Experian은 첫 납부를 하지 않은 경우로 설명하면서 일시적 어려움과 사기를 구분해야 한다고 적었다. ([Experian](https://www.experian.com/blogs/insights/first-payment-default/)) Ant Financial의 자동차 대출 논문은 반대로 3개월 정상 상환한 뒤 30일 넘게 연체한 건을 사기로 표기했는데, 3개월 안에 연체하면 사기로 처벌받기 쉬워서 사기범이 이 패턴을 쓴다는 저자들의 설명이 붙어 있다. ([Xu 외, AAAI-21](https://ojs.aaai.org/index.php/AAAI/article/view/16582)) 미국 연준 백서는 합성 신원 사기 손실이 신용 손실로 잘못 분류되는 경우가 많다고 지적하면서, 계좌 주인이 실재하는지와 상환 의사가 있었는지로 둘을 가른다. ([Federal Reserve](https://fedpaymentsimprovement.org/wp-content/uploads/frs-synthetic-identity-payments-fraud-white-paper-october-2019.pdf)) FPD 라벨의 오분류율을 수치로 검증한 독립 연구는 찾지 못했다. 그래서 라벨 하나로 합치기보다 명의도용, 합성 신원, 처음부터 갚을 뜻이 없던 경우(first-party fraud), 형편이 어려워진 경우를 나눠서 기록해 두는 편이 안전하다. 카카오뱅크가 시퀀스 FDS를 정상·사기·피해의 3분류로 만든 것도 비슷한 맥락으로 볼 수 있는데, 피해자 계좌를 사기로 찍으면 라벨이 오염되기 때문이다. ([카카오뱅크](https://tech.kakaobank.com/posts/2606-sequence-based-fds-model/))

**마케팅과 추심의 Y는 증분이다.** 추심 대상 고객이 네 그룹 있고, 그룹별로 1,000명이고, 전화를 1,000통만 걸 수 있다고 하자. 숫자는 가상이다.

| 그룹 | 전화하면 상환 | 전화 안 해도 상환 | 전화로 늘어나는 상환 |
|------|------|------|------|
| A. 어차피 갚을 사람 | 90% | 88% | 2%p |
| B. 전화하면 갚을 사람 | 60% | 35% | 25%p |
| C. 늦었지만 반응하는 사람 | 30% | 10% | 20%p |
| D. 연락해도 못 갚는 사람 | 8% | 7% | 1%p |

상환 확률이 높은 순서로 전화하면 A 그룹에 전화를 쓰게 되어 상환자가 20명 늘고, 증분이 큰 순서로 전화하면 B 그룹에 써서 250명이 는다. 마케팅도 구조가 같아서, 전환 확률 모델은 어차피 전환했을 고객에게 쿠폰을 주는 쪽으로 기운다. 증분을 추정하려면 처치를 무작위로 배정한 데이터가 필요하고, 그래서 이 두 모델은 변수보다 실험 설계가 먼저 나온다.

## 6. 공개 사례에서 확인한 변수와 라벨

회사들이 공개한 수준은 고르지 않다. 신청 모델은 자료가 많은 편이고, 추심은 회사가 직접 쓴 기술 글이 거의 없어서 대출사 데이터로 실험한 논문이 주된 근거다. 한국 회사는 변수 범주까지는 공개해도 불량 정의와 알고리즘은 밝히지 않은 경우가 대부분이었다. 수치는 대부분 회사 발표나 워킹페이퍼 기준이고, 비교 대상이 서로 달라 수치끼리 비교하면 안 된다.

| 사례 | 모델 | 입력 | Y | 공개된 결과 |
|------|------|------|------|------|
| 네이버페이 | 마케팅 | 비공개, 금액 무작위 실험 | 전환·결제 | 실측 수치 비공개 |
| Mercado Libre 대출 캠페인 | 마케팅 | 이름을 가린 변수 | 전환, 취급액 | 상위 3분위(26%)가 취급액의 63%(유사 데이터 예시) |
| Ant GRC | 사기 | 신청자·판매자·중개인 그래프 | 3개월 정상 상환 후 30일 초과 연체 | F1 85.56%, GCN 79.07% |
| Ant GEM | 사기 | 기기 6종 그래프, 활동 168칸 | 사후 판정 악성 계정 | 1주차 F1 0.8165, 4주차 0.7344 |
| 카카오뱅크 FDS | 사기 | 앱 이벤트·거래 시퀀스 | 정상·사기·피해 | 탐지 성능 비공개 |
| Plaid LendScore | 신청 | 현금흐름 등 145개 | 12개월 내 90일 이상 연체 | KS 전체 +9.1%(벤치마크 비공개) |
| Upstart | 신청 | 2,500개 초과 | 기간별 부도·조기상환 | 41% 더 승인, APR 33% 낮음(시뮬레이션) |
| Affirm | 신청 | 신용 보고서 레코드 토큰 + 표 변수 | FPDQ4, DQ60 등 | AUC 상대 개선 3.83%, 전환 +1.2%p |
| 카카오뱅크 카뱅스코어 | 신청 | 약 3,800개 | 비공개 | 추가 승인 약 1.1조 원(보도 기준) |
| Mercado Crédito | 신청 | 판매·평판·업종 | 30일 이상 연체 손실 | AUROC 0.76, 신용정보 모델 0.64 |
| Berg 외 | 신청 | 디지털 흔적 10개 | 추심 이관 | AUC 69.6%, 신용정보 68.3% |
| Nubank 한도 상향 | 행동 | 비공개 | 대개 60~180일 내 미상환 | 수치 비공개 |
| Nubank nuFormer v3 | 신용 결정 | 거래 토큰 + 표 변수 291개 | 6개월 뒤 65일 연체 | AUC 상대 +1.25% |
| Ant 한도 증액 | 행동 | 소비, 잔액, 신용 등급 | 증액 후 잔액 증가 | RMAE 38.30%, 선형 94.10% |
| Affirm PredictPay | 행동 | 납부 이력, 수단별 이력 | 납부 실패 | AUC 0.81에서 0.88, FPDQ4 상대 -2.8% |
| Tala | 추심 | 상환 이력, 통화 결과, 앱 사용 | 전화로 늘어난 상환 | 상위 50%가 증분 수익의 90% |
| Wang·Zhou | 추심 | 하드 정보 + 상담원 메모 5,000단어 | 180일 내 상환 | 53.24% 대 43.14% |
| Choi 외 | 추심 | 콜러 화면 항목, 일 단위 내부 점수 | 회수 NPV | AI 콜러가 1년 시점 약 5%p 낮음 |

### 마케팅: 응답 확률에서 증분으로

네이버페이는 마이데이터 등록과 제휴 결제 프로모션에서 누구에게 0원, 1,000원, 2,000원 중 얼마를 줄지 정하는 문제를 먼저 무작위 실험으로 시작한다. 금액을 무작위로 배정한 데이터로 Double ML을 학습해 처치별 효과(CATE)를 추정하고, 금액을 올렸을 때 효과가 큰 사용자에게 고액을 준다. 글에 나오는 CPA 1,429원과 1,643원은 필자가 가상 데이터 예시라고 밝힌 값이라 성과로 읽으면 안 된다. ([네이버페이](https://medium.com/naverfinancial/uplift-modeling%EC%9D%84-%ED%86%B5%ED%95%9C-%EB%A7%88%EC%BC%80%ED%8C%85-%EB%B9%84%EC%9A%A9-%EC%B5%9C%EC%A0%81%ED%99%94-with-multiple-treatments-5e4e3824b9df))

Mercado Libre의 대출 캠페인 사례는 임계값을 올릴 때 생기는 충돌을 잘 보여 준다. 이진 분류기의 임계값을 0.55로 잡으면 전환율이 42%, 0.95면 75%까지 오르지만, 0.40에서 0.60으로 올리기만 해도 취급액이 100만 달러 넘게 줄었다. 그래서 이진 결정을 버리고 성향 10분위 체계로 바꿨고, 신규 고객과 재이용 고객의 모델도 나눴다. 다만 글 제목의 Credit Origination은 심사가 아니라 대출 마케팅이고, 최종 성과 18.5배와 412%는 대조군 없는 최댓값이라 그대로 믿기는 어렵다. ([Mercado Libre](https://medium.com/mercadolibre-tech/how-a-data-product-approach-help-mercado-libre-build-a-credit-origination-framework-23c02a821b49)) 같은 회사의 Kairós는 업리프트 점수를 바로 쓰지 않고 사용자별 메시지 상한, 제안별 인원, 발송 대역폭을 제약으로 둔 할당 문제에 넣는다. ([Mercado Libre Kairós](https://medium.com/mercadolibre-tech/kair%C3%B3s-powering-optimized-audience-targeting-for-next-generation-campaign-delivery-in-mercado-c196735e4cb5))

### 사기: 자원이 몰리는 곳과 라벨 지연

Ant의 GEM은 사기범의 자원이 제한되어 있으니 기기와 시간에 몰린다는 가정을 그대로 변수로 옮겼다. 휴대폰 번호, MAC, IMSI 등 기기 6종과 계정을 잇는 그래프를 지난 7일 기준으로 매일 다시 만들고, 활동을 7일×24시간의 168칸으로 쌓는다. GBDT에 그래프 변수를 더한 모델보다 F1이 높았지만, 같은 모델의 F1도 1주차 0.8165에서 4주차 0.7344로 떨어졌다. 사기 쪽 변수가 얼마나 빨리 낡는지 보여 주는 숫자다. ([Liu 외, CIKM 2018](https://arxiv.org/abs/2002.12307)) 앞서 라벨을 소개한 GRC는 관계를 맺은 시점이 신청 전 30일 이내인지로 시간 구간을 나눴고, 신청 직전 구간의 관계가 더 중요하게 나왔다. 다만 사기 비율 등 테스트셋 구성은 공개되지 않아 F1을 실제 운영 성능으로 읽을 수는 없다.

카카오페이는 라벨이 늦게 오는 문제를 변수로 풀었다. 결제 아이템 종류별 최근 사고 비율을 변수로 넣어서, 새로운 유형의 사고가 터진 뒤 재학습 모델이 배포되기 전 공백을 메운다. 정적 모델 대비 약 30% 탐지율 개선이라고 밝혔는데 상대값인지 절대값인지는 적혀 있지 않다. ([카카오페이](https://tech.kakaopay.com/post/ifkakao2024-fds/)) 사고 비율은 라벨에서 만든 변수이므로 기준 시점에 확정된 사고만 세도록 관리해야 한다.

사기 점수가 곧 거절로 이어지는 것도 아니다. 카카오뱅크의 시퀀스 FDS는 일평균 1,800만 건 수준을 평균 20ms 이내로 추론하지만, 자동 차단이 아니라 FDS 현업 조건과 결합해 모니터링 대상자 목록을 띄우는 구조다. Plaid의 Trust Index 2도 추가 인증 대상을 고르는 데 쓰며, 대형 디지털 대출사 사용자의 5%에 추가 인증을 걸었다면 기존 솔루션이 놓친 first-party fraud의 40%를 잡았을 것이라는 사후 분석을 내놓았다. 벤더의 사후 분석이고 라벨 정의는 공개되지 않았다. ([Plaid](https://plaid.com/blog/plaid-protect-trust-index/))

### 신청: 변수 7개와 2,500개 사이

Upstart의 공시를 보면 개인대출 모델의 변수는 2014년 말 23개에서 2025년 말 2,500개 초과로 늘었고, 약 1억 400만 건의 상환 이벤트로 학습한다. 비교 대상으로 삼는 전통 모델은 FICO, DTI, 대출 금액, 트레이드 계좌 수, 조회 수, 월소득, 최고령 계좌 개월 수의 7개 입력을 쓰는 Cox 모델이다. 2025년 신청자에 시뮬레이션하면 41% 더 승인하고 APR이 33% 낮다고 하는데, 비교 모델을 회사가 직접 만들었고 실거래 실험이 아니다. 대출사가 정한 최저 점수나 DTI 같은 하드 기준을 먼저 적용하고 통과 건에 모델을 돌리며, 거절의 대부분은 이 하드 기준에서 나온다는 점도 함께 봐야 한다. ([10-K](https://www.sec.gov/Archives/edgar/data/1647639/000164763926000027/upst-20251231.htm), [Access to Credit](https://www.upstart.com/lenders/regulatory-compliance/access-to-credit-report/))

Plaid LendScore는 설계가 가장 자세히 공개된 사례다. 동의를 받은 계좌 거래를 범주화해 30·60·90일 창으로 집계하고, 수백 개 중 145개를 골랐다. 월평균 유입, 예금 잔액 표준편차, 재량·필수 지출 비중, 소득 대 총유출 비율, 소득 규칙성 같은 현금흐름 변수가 예측력의 약 81%, 대출·저축·선지급 앱 연결 수 같은 네트워크 변수가 약 19%다. 144만 트레이드라인으로 학습한 단조 제약 XGBoost에서, SHAP로 점수를 가장 깎은 변수 5개를 뽑아 표준 문구의 사유 코드로 돌려준다. 다만 KS +9.1%의 벤치마크가 무엇인지는 밝히지 않았다. ([Plaid](https://plaid.com/blog/how-we-built-lendscore/))

Affirm은 신용 보고서의 트레이드라인과 조회 기록을 레코드 단위 토큰으로 넣는 트랜스포머로 임베딩을 만들고, 기존 변수와 합쳐 XGBoost로 점수를 낸다. 트랜스포머 단독으로는 XGBoost를 넘지 못했고 하이브리드만 넘었다고 적었다. 배포 순서도 눈여겨볼 만하다. 처음에는 기존 시스템이 거절한 건을 다시 보는 2차 심사로 넣어 위험을 제한했고, 지금은 1차 심사로 넓히는 실험 중이다. 오프라인 수치는 승인된 대출만으로 잰 것이라 거절 건은 빠져 있다. ([Affirm](https://tech.affirm.com/learning-richer-credit-representations-with-transformers-at-affirm-c774e7c1cea6))

한국에서는 카카오뱅크 사례가 결정 구조까지 비교적 구체적으로 알려져 있다. 팀장 인터뷰 보도에 따르면 금융 모형으로 금리와 컷오프를 정하고, 전략 모형으로 1차 승인을 내린 뒤, 1차 거절자 중 대안신용평가 우량 고객을 오버라이드로 추가 승인한다. 한도는 소득 기반에 카뱅스코어 한도 승수를 더한다. ([데일리안](https://www.dailian.co.kr/news/view/1610964/)) 변수 쪽은 도서 구매를 예로 1·3·6개월 단위로 빈도, 금액, 권당 가격, 분야별 구매량의 변수 풀을 만들어 신용도와 관계있는 것을 추렸다고 한다. ([한겨레](https://v.daum.net/v/20240205165507379)) 가명결합 1,800만 건과 3,800여 변수, 상위 30% 안의 thin file 비중 9.7%(표준 점수 1.8%)는 회사 발표를 인용한 보도이고, 불량 정의와 알고리즘은 공개되지 않았다. ([더팩트](https://news.tf.co.kr/read/economy/2256959.htm)) 이런 대안 점수가 나오는 배경에는 CB 점수의 변별력 문제가 있다. KCB는 2026년 1월 금융위 회의에서 평가 대상의 28.6%가 950점 이상이고 금융이력 부족자의 평균이 약 710점(2024년 말)이라는 현황을 제시했다. ([금융위원회](https://www.fsc.go.kr/no010101/86084))

네이버페이는 다른 방식의 제약을 걸었다. 네이버페이 스코어는 이용 내역과 마이데이터 자산, 사업자의 경우 거래액, 배송·문의 응답 속도, 리뷰 등을 쓰는데, 심사에는 유리한 방향으로만 반영하고 불리해지는 방향으로는 쓰지 않는다고 밝혔다. 변수별 단조 제약과 달리 점수 전체에 거는 정책 제약인 셈이다. 변별력 13.57%p 개선은 지표 이름이 없는 시뮬레이션 값이다. ([네이버](https://navercorp.com/media/pressReleasesDetail?seq=31685))

값싼 변수의 힘과 한계는 학술 연구 두 편이 잘 보여 준다. 독일 온라인 쇼핑몰의 후불 결제 약 27만 건을 분석한 Berg 외의 연구는 기기 유형, OS, 유입 경로, 구매 시간대, 이메일 호스트 등 변수 10개만으로 AUC 69.6%를 얻어 신용정보 점수의 68.3%와 비슷했고, 합치면 73.6%였다. iOS 사용자의 부도율은 1.07%, Android는 1.79%다. 다만 회사가 이미 예측 부도율 높은 고객을 걸러낸 표본이고, 저자들 스스로 이런 변수는 쓰이는 게 알려지면 행동이 바뀔 수 있다고 적었다. ([NBER](https://www.nber.org/system/files/working_papers/w24551/w24551.pdf)) 아르헨티나 Mercado Crédito의 판매자 7,300건 분석에서는 신용정보만 쓴 로지스틱 회귀의 AUROC가 0.64, 플랫폼 데이터 기반 내부 점수가 0.76이었다. 2017년 자료이고 공저자 중 Mercado Libre 소속이 있다. ([BIS](https://www.bis.org/publications/working-paper-779-bigtech-and-changing-structure-financial-intermediation.pdf))

### 행동: 한도 모델에는 두 개의 Y가 있다

Nubank는 카드 한도 증액을 부도까지의 시간으로 모델링한다. 정해진 기간(대개 60~180일) 안에 청구액을 못 갚을 확률을 생존 곡선으로 보고, 순위 모델은 그대로 둔 채 곡선 보정만 자주 갱신한다. 순위와 보정의 갱신 주기를 나눈 설계인데, 변수와 수치는 공개하지 않았다. ([Nubank](https://building.nu.com/how-nubank-models-risk-for-smarter-scalable-credit-limit-increases/)) 같은 회사의 뉴스룸 자료에 따르면 한도 증액 모델은 17세대, 신규 모델은 10세대까지 왔다. ([Nubank 뉴스룸](https://nu.com/en/newsroom/company/nubanks-ai-powered-credit-model-extends-access-while-maintaining-portfolio-quality)) 신규 모델보다 한도 모델의 세대 수가 더 많다는 점은 눈여겨볼 만하다. nuFormer 논문 v3는 6개월 뒤 65일 연체를 라벨로 거래 토큰과 표 변수 291개를 합쳐 상대 AUC +1.25%를 보고했고, 라벨이 늦어 모든 변형을 A/B 테스트하지 못했다고 적었다. 어떤 신용 결정에 쓰는지는 밝히지 않았고, 논문 v1은 같은 표본과 수치를 추천 문제로 설명하고 있어 판본을 구분해서 읽어야 한다. ([arXiv](https://arxiv.org/html/2507.23267v3))

한도 결정에는 위험 말고 반응도 필요하다. Ant의 한도 증액 논문은 Y를 부도가 아니라 증액 후 잔액 증가로 잡았다. 신용 등급과 수요로 나눈 6개 세그먼트 안에서 증액폭을 무작위로 배정해 데이터를 모았고, 변수는 부도확률, 신용 등급, 최근 3·6개월 월평균 지출, 12개월 월최대 지출, 과거 잔액 등이다. 잔액 반응 오차(RMAE)는 선형 모델 94.10%, 단일 GBDT 47.58%, GBDT 인코딩에 처치 로그 변환을 더한 모델 38.30%였다. 온라인 성과는 없고 데이터가 실제 사업을 대표하지 않는다는 각주가 있다. ([Miao 외](https://arxiv.org/abs/2007.05188)) 한도를 올렸을 때 대출이 얼마나 늘어나는지는 터키 은행이 증액 대상 45,307명 중 일부의 증액을 9개월간 무작위로 보류한 실험에서 볼 수 있는데, 새 한도 1달러당 첫 분기에 11센트, 3년차까지 28센트를 더 빌렸다. ([Aydin, AER](https://www.aeaweb.org/articles?id=10.1257/aer.20191178)) Rappi 연구진은 충당금까지 넣은 기대 이익 차이를 보상으로 둔 강화학습을 제안했는데, 무작위 한도 조정의 고객 경험 문제와 3개월 뒤에야 관측되는 보상 때문에 온라인 탐색이 어렵다고 적었고 결과도 합성 실험이다. ([Alfonso-Sánchez 외](https://arxiv.org/abs/2306.15585))

연체를 줄이는 레버가 점수에만 있는 것은 아니다. Affirm의 PredictPay는 결제 실패 위험을 예측해 자동이체 기본 수단의 순서를 바꾸는 XGBoost 배치 모델로, 최근 성공·실패 패턴과 수단별 이력을 더한 v2가 ROC-AUC를 0.81에서 0.88로 올렸다. 2026년 6~8월 실험에서 v1 대비 FPDQ4가 상대 2.8%, 자동이체 납부 실패율이 상대 7.1% 줄었다. ([Affirm](https://tech.affirm.com/predictpay-from-hackathon-idea-to-smarter-payments-at-scale-a8dc7c3837db)) 운영 면에서는 메르페이가 월간 한도 갱신에 여러 모델을 쓰면서 약 50개의 월간 릴리스 작업을 자동화했다는 글이 참고가 된다. 변수와 라벨은 없고 운영 이야기다. ([Mercari](https://engineering.mercari.com/blog/entry/20241219-e9ad9948c2/))

### 추심: 회사 글은 드물고 실험은 있다

Tala의 글은 회사가 직접 쓴 추심 모델 설명으로는 드물다. 상환 이력, 과거 통화 결과, 앱 상호작용 변수로 S-Learner를 학습하는데, 학습 데이터 자체가 전화와 무전화를 무작위로 나눈 실험에서 나온다. 확률 업리프트에 채무액과 예상 상환액을 곱한 수익 업리프트로 순위를 매기고, 배포 후에는 무작위 5%에 무조건 전화하고 다른 5%는 무조건 전화하지 않아 실제 효과를 계속 감시한다. 테스트셋에서 상위 10%에 전화하면 전원 전화 때 증분 수익의 절반 이상, 상위 50%면 90%를 얻었다고 한다. 표본과 비용, 배포 후 수치는 없다. ([Tala](https://tala.co/blog/2021/01/14/helping-late-borrowers-repay-with-uplift-modeling/))

가장 구체적인 근거는 네덜란드 추심 대행사의 무작위 실험이다. 차주 7,839명을 180일 동안 사람 담당자와 알고리즘 중 하나가 통화 대상을 고르게 나눴고, 전화는 양쪽 모두 같은 상담원이 걸었다. 알고리즘은 채무액, 채무 연령 같은 하드 정보에 통화 횟수, 웹사이트 로그인, 상담원 메모에서 뽑은 상위 5,000개 단어·구를 쓰고, 추심 진행일별 GBDT와 메타 러너로 통화의 효과를 추정해 효과가 큰 통화를 고른다. 상환율은 53.24% 대 43.14%였고 평균 통화 수는 3.50회 대 3.82회로 오히려 적었다. ([Wang·Zhou, 워킹페이퍼](https://ncbankruptcyexpert.com/sites/default/files/2024-07/artificial_intelligence_and_debt_collection_evidence_from_a_field_experiment_compressed_0.pdf))

반대처럼 보이는 결과도 있다. 중국 온라인 소비자금융사의 2,200만여 건을 분석한 NBER 논문에서는 AI 콜러가 맡은 건의 회수 NPV가 연체 약 1개월 시점에 9%p, 1년 시점에도 약 5%p 낮았다. 다만 질문이 다르다. 앞의 실험은 누구에게 전화할지를 알고리즘이 고른 것이고, 이 논문은 전화를 거는 주체가 AI인 경우다. 변수 설계 면에서는 내부 점수가 전날 통화 결과를 반영해 매일 갱신되고, 연체 구간을 2~10일, 11~25일, 26~59일, 60~84일, 85일 이상으로 나눠 전략을 달리한다는 점이 참고가 된다. 생산성 높은 콜러가 가장 많이 쓴 필터가 최근 앱 로그인 시각이었다는 내부 조사도 나온다. ([Choi 외, NBER](https://www.nber.org/system/files/working_papers/w33669/w33669.pdf))

조치 내용이 점수보다 큰 경우도 있다. 사하라 이남의 디지털 대출사에서 90~150일 연체자에게 4회 분할 상환을 제안하자 일부라도 상환한 비율이 대조군 16.2%에서 9.3%p 올랐는데, 대출 자격 복원 안내만 보낸 군은 유의하지 않았고 둘을 합친 군의 완납 효과도 유의하지 않았다. ([Burlando 외, 워킹페이퍼](https://silviaprina.com/files/ungated-papers/working-papers/BKPW_delinquent_digital_borrowers.pdf)) 독일 은행의 POS 대출 연구는 첫 통화 요일 배정을 이용해 연락이 닿기 어려운 차주일수록 통화 효과가 크다는 결과를 냈다. 받는 사람에게만 계속 전화하는 운영이 손해일 수 있다는 뜻이다. 2021년 워킹페이퍼 기준이고 학술지 게재본은 확인하지 못했다. ([Laudenbach 외](https://www.ifo.de/DocDL/cesifo1_wp7295.pdf))

## 7. 어떤 변수는 규칙이 막는다

공개 논문의 변수를 그대로 가져올 수 없는 경우가 많다. Ant의 SemiGNN은 앱 로그인, 별명, 주소 단어를 그래프로 만들어 연체 예측 AUC를 0.753에서 0.807로 올렸지만, 이런 변수를 지금 한국이나 미국의 대출 앱에 옮기기는 어렵다. ([Wang 외](https://arxiv.org/abs/2003.01171)) 신흥국 디지털 대출에서 쓰이던 연락처와 앱 목록도 마찬가지다.

| 지역 | 규칙 | 변수 설계에 미치는 영향 |
|------|------|------|
| Android 앱 | [Google Play 금융 서비스 정책](https://support.google.com/googleplay/android-developer/answer/9876821) | 개인 대출 앱은 연락처, 사진·영상, 정밀 위치, 전화번호, 설치 앱 목록 권한을 쓸 수 없다 |
| 미국 | [Regulation B §1002.9(b)(2)](https://www.consumerfinance.gov/rules-policy/regulations/1002/9/) | 거절 사유는 구체적이어야 하고, 점수 미달이라는 설명으로는 부족하다 |
| 미국 | [2026년 Regulation B 개정](https://public-inspection.federalregister.gov/2026-07804.pdf) | 2026년 7월 21일부로 차별 효과 기준(effects test)이 빠졌고 소송이 진행 중이다. 성별 등 금지 사유 조항은 유지된다 |
| 한국 | [신용정보법 제36조의2](https://elaw.klri.re.kr/kor_service/lawViewContent.do?hseq=70283)(2024년 2월 판본 기준) | 자동화평가에 대해 결과, 주요 기준, 기초정보 개요를 설명 요구할 수 있고 정정과 재산출도 요구할 수 있다 |
| 한국 | [금융위 2018년 12월 개선안](https://www.fsc.go.kr/no010101/73473) | 2019년 1월부터 단기연체 반영 기준이 10만 원·5영업일에서 30만 원·30일로 바뀌었다. 그 전후 표본의 연체 변수는 정의가 다르다 |
| 한국 | [신용정보법 시행령 제28조의3](https://www.law.go.kr/lumLsLinkPop.do?lspttninfSeq=164679&chrClsCd=010202) | 마이데이터 전송 요구 대상에 세금, 4대 보험, 통신료 납부 정보 등이 들어간다 |
| 중국 | [징신 업무 관리 방법](https://www.gov.cn/gongbao/content/2021/content_5654782.htm)(2022년 시행) | 금융기관은 무허가 기관에서 징신 서비스를 받을 수 없고, 신용과 무관한 요소를 평가 기준으로 삼을 수 없다. 반사기 상품에는 사기 인정 기준을 요구한다 |
| EU | [AI Act 부속서 III](https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3) | 신용평가는 고위험이고 사기 탐지는 예외다. 고위험 의무는 [2027년 12월 2일](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-113)부터 적용된다 |

CFPB가 복잡한 알고리즘의 거절 사유를 다룬 회람 2022-03과 2023-03은 [2025년 5월 철회](https://public-inspection.federalregister.gov/2025-08286.pdf)되었으니, 설명 의무의 근거로는 회람보다 위 조문을 인용하는 편이 맞다. 또 신청 모델 변수 목록에 성별이 아무렇지 않게 들어 있는 자료를 종종 보는데, 금지 사유이거나 프록시 점검 대상이 되는 변수는 후보 단계에서 따로 표시해 두어야 나중에 설명이 된다. 법률 해석은 회사 법무와 확인해야 하고, 한국 조문은 글 작성 시점에 최신본을 확인하지 못한 부분이 있다.

## 8. 개인적인 견해

공개 사례를 모아 보면 변수 경쟁은 신청 모델에 쏠려 있는데, 숫자가 크게 나온 쪽은 오히려 후단이었다. 네덜란드 실험의 상환율 10%p 차이나 Affirm의 결제 수단 순서 변경은 새 변수를 수백 개 넣은 결과가 아니라 조치를 고르는 방식을 바꾼 결과다. 물론 나라와 상품, 비교 대상이 달라 숫자를 직접 견줄 수는 없고, 추심 쪽은 잘 된 실험만 논문으로 나왔을 가능성도 있다. 그래도 신청 모델의 AUC를 조금 더 올리는 일과 추심에 무작위 대조군을 두는 일 중 어느 쪽 효과가 큰지는 한 번 따져 볼 만하다고 생각한다.

고치는 순서를 정한다면 라벨 사전이 먼저다. 사기와 신용 손실을 어떻게 나눌지, 불량 기준과 성과 기간을 상품별로 어떻게 둘지 합의되어 있지 않으면 변수를 아무리 잘 만들어도 모델끼리 숫자가 맞지 않는다. 그다음은 기준 시점이고, 데이터가 도착한 날짜를 변수 사전에 같이 적어 두는 것만으로도 누수의 상당 부분을 막을 수 있다. 변수 추가는 그 뒤의 일로 본다.

변수 사전은 한 벌로 관리하되 해석은 모델별로 따로 적었으면 한다. 소진율의 계산식은 다섯 모델이 공유해도 되지만 방향은 공유하면 안 되니까 그렇다. 마케팅 모델을 만드는 사람과 신청 모델을 만드는 사람이 다른 조직에 있으면 이 표를 맞춰 볼 기회가 생각보다 없다.

한국 사례는 아쉬움이 남는다. 대안 점수의 변수 범주는 꽤 공개되었지만 불량 정의, 성과 기간, 비교 기준이 빠진 경우가 많아서 외부에서는 성과를 검증하기 어렵고, 연체 예측이나 추심 모델을 다룬 기술 글은 이번에 찾지 못했다. 카카오뱅크와 카카오페이가 FDS에서 보여 준 정도로만 공개되어도 업계 전체의 기준이 올라갈 것 같다.

---

**함께 보면 좋은 글:**

- [AUC는 같은데 KS만 높은 모델: KS와 AUC는 같은 곡선에서 나온다](/posts/risk-metrics-ks-auc/)
- [단독 Lift 2.4인 규칙이 전략에 들어가면 약해지는 이유: Lift를 재는 네 가지 기준](/posts/risk-metrics-lift/)
- [트랜스포머는 신용 모델의 어디에 들어가나: Affirm, Revolut, Parafin, 앤트의 경우](/posts/transformers-in-credit/)

## 참고 자료

**마케팅**

- [Uplift Modeling을 통한 마케팅 비용 최적화 (네이버페이, 2024)](https://medium.com/naverfinancial/uplift-modeling%EC%9D%84-%ED%86%B5%ED%95%9C-%EB%A7%88%EC%BC%80%ED%8C%85-%EB%B9%84%EC%9A%A9-%EC%B5%9C%EC%A0%81%ED%99%94-with-multiple-treatments-5e4e3824b9df)
- [How a Data Product approach helps Mercado Libre build a Credit Origination Framework (Mercado Libre, 2025)](https://medium.com/mercadolibre-tech/how-a-data-product-approach-help-mercado-libre-build-a-credit-origination-framework-23c02a821b49)
- [Kairós: Powering optimized audience targeting (Mercado Libre, 2025)](https://medium.com/mercadolibre-tech/kair%C3%B3s-powering-optimized-audience-targeting-for-next-generation-campaign-delivery-in-mercado-c196735e4cb5)

**사기**

- [Towards Consumer Loan Fraud Detection (Xu 외, AAAI-21)](https://ojs.aaai.org/index.php/AAAI/article/view/16582)
- [Heterogeneous Graph Neural Networks for Malicious Account Detection (Liu 외, CIKM 2018)](https://arxiv.org/abs/2002.12307)
- [A Semi-supervised Graph Attentive Network for Financial Fraud Detection (Wang 외, 2020)](https://arxiv.org/abs/2003.01171)
- [AI, 고객 행동의 순서를 읽다 (카카오뱅크, 2026)](https://tech.kakaobank.com/posts/2606-sequence-based-fds-model/)
- [FDS에 지속 성장하는 ML 모델 적용 이야기 (카카오페이, 2024)](https://tech.kakaopay.com/post/ifkakao2024-fds/)
- [Introducing Ti2 (Plaid, 2025)](https://plaid.com/blog/plaid-protect-trust-index/)
- [Detecting Synthetic Identity Fraud in the U.S. Payment System (Federal Reserve, 2019)](https://fedpaymentsimprovement.org/wp-content/uploads/frs-synthetic-identity-payments-fraud-white-paper-october-2019.pdf)
- [What Lenders Need to Know About First Payment Default (Experian, 2026 갱신)](https://www.experian.com/blogs/insights/first-payment-default/)

**신청**

- [How we built LendScore (Plaid, 2025)](https://plaid.com/blog/how-we-built-lendscore/)
- [Instant Link & LendScore 2 (Plaid, 2026)](https://plaid.com/blog/instant-link-next-generation-lendscore/)
- [Upstart FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1647639/000164763926000027/upst-20251231.htm)
- [Upstart 2025 Access to Credit Report](https://www.upstart.com/lenders/regulatory-compliance/access-to-credit-report/)
- [Learning Richer Credit Representations with Transformers at Affirm (Affirm, 2026)](https://tech.affirm.com/learning-richer-credit-representations-with-transformers-at-affirm-c774e7c1cea6)
- [From research to real time (Revolut, 2026)](https://www.revolut.com/blog/post/fromresearchtorealtime/)
- [카카오뱅크 대안신용평가 인터뷰 (데일리안, 2026)](https://www.dailian.co.kr/news/view/1610964/)
- [책 구매·쇼핑 내역도 분석해 대출 신용평가하죠 (한겨레, 2024)](https://v.daum.net/v/20240205165507379)
- [카뱅스코어 보도 (더팩트, 2025)](https://news.tf.co.kr/read/economy/2256959.htm)
- [네이버페이 스코어 보도자료 (네이버, 2024)](https://navercorp.com/media/pressReleasesDetail?seq=31685)
- [On the Rise of FinTechs: Credit Scoring Using Digital Footprints (Berg 외, NBER WP 24551)](https://www.nber.org/system/files/working_papers/w24551/w24551.pdf)
- [BigTech and the changing structure of financial intermediation (Frost 외, BIS WP 779)](https://www.bis.org/publications/working-paper-779-bigtech-and-changing-structure-financial-intermediation.pdf)
- [신용평가체계 개편 TF 보도자료 (금융위원회, 2026)](https://www.fsc.go.kr/no010101/86084)

**행동**

- [How Nubank models risk for smarter, scalable credit limit increases (Nubank, 2025)](https://building.nu.com/how-nubank-models-risk-for-smarter-scalable-credit-limit-increases/)
- [Nubank's AI-powered credit model (Nubank 뉴스룸, 2026)](https://nu.com/en/newsroom/company/nubanks-ai-powered-credit-model-extends-access-while-maintaining-portfolio-quality)
- [nuFormer 논문 (arXiv 2507.23267 v3)](https://arxiv.org/html/2507.23267v3)
- [Intelligent Credit Limit Management in Consumer Loans Based on Causal Inference (Miao 외, 2020)](https://arxiv.org/abs/2007.05188)
- [Consumption Response to Credit Expansions (Aydin, AER 2022)](https://www.aeaweb.org/articles?id=10.1257/aer.20191178)
- [Optimizing Credit Limit Adjustments Under Adversarial Goals Using Reinforcement Learning (Alfonso-Sánchez 외)](https://arxiv.org/abs/2306.15585)
- [PredictPay (Affirm, 2026)](https://tech.affirm.com/predictpay-from-hackathon-idea-to-smarter-payments-at-scale-a8dc7c3837db)
- [メルペイにおける機械学習システム運用時の工夫 (Mercari, 2024)](https://engineering.mercari.com/blog/entry/20241219-e9ad9948c2/)

**추심**

- [Helping late borrowers repay with uplift modeling (Tala, 2021)](https://tala.co/blog/2021/01/14/helping-late-borrowers-repay-with-uplift-modeling/)
- [Artificial Intelligence and Debt Collection (Wang·Zhou, 2024 워킹페이퍼)](https://ncbankruptcyexpert.com/sites/default/files/2024-07/artificial_intelligence_and_debt_collection_evidence_from_a_field_experiment_compressed_0.pdf)
- [How Good is AI at Twisting Arms? (Choi 외, NBER WP 33669)](https://www.nber.org/system/files/working_papers/w33669/w33669.pdf)
- [Behavioral Messages and Debt Repayment (Barboni 외, CAGE WP 633)](https://warwick.ac.uk/fac/soc/economics/research/centres/cage/manage/publications/wp633.2022.pdf)
- [From Default to Second Chances (Burlando 외, 2026 워킹페이퍼)](https://silviaprina.com/files/ungated-papers/working-papers/BKPW_delinquent_digital_borrowers.pdf)
- [Personal Communication in an Automated World (Laudenbach 외, CESifo WP 7295)](https://www.ifo.de/DocDL/cesifo1_wp7295.pdf)

**규칙**

- [Google Play Financial Services 정책](https://support.google.com/googleplay/android-developer/answer/9876821)
- [Regulation B §1002.9](https://www.consumerfinance.gov/rules-policy/regulations/1002/9/), [2026년 최종 규칙](https://public-inspection.federalregister.gov/2026-07804.pdf), [CFPB 해석 철회 문서](https://public-inspection.federalregister.gov/2025-08286.pdf)
- [신용정보법(2024년 2월 판본)](https://elaw.klri.re.kr/kor_service/lawViewContent.do?hseq=70283), [시행령 제28조의3](https://www.law.go.kr/lumLsLinkPop.do?lspttninfSeq=164679&chrClsCd=010202), [금융위 2018년 12월 보도자료](https://www.fsc.go.kr/no010101/73473)
- [징신 업무 관리 방법 (중국인민은행, 2021)](https://www.gov.cn/gongbao/content/2021/content_5654782.htm)
- [EU AI Act 부속서 III](https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3), [제113조](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-113)

_본 글은 2026년 11월 4일 기준 공개 자료를 바탕으로 작성했다. 회사 수치는 회사 발표 또는 보도 기준이고 논문 수치는 표기한 판본 기준이다. 롤레이트와 추심 그룹의 숫자, 코드 예시의 고객은 설명을 위해 만든 가상 데이터다. 법률 해석이 아니며 규정은 확인한 판본 기준이므로 실제 적용 전에 최신본을 확인해야 한다._
