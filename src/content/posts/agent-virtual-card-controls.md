---
title: "단일 사용 카드가 두 번 결제되는 이유: AI 에이전트의 권한을 가상카드로 표현할 때 생기는 빈틈"
description: "Ramp, Corpay, Stripe, Sunrate가 AI 에이전트용 가상카드를 내놓고 있다. 한도·업종·기한을 카드에 걸면 모델이 속아도 피해가 묶이지만, 발급사 문서를 읽어 보면 이 통제는 승인 순간에만 작동하고 돈이 움직이는 매입에는 닿지 않는다. 호텔 대금 지급을 예로 빈틈이 어디서 생기는지, 대사를 어떻게 짜야 하는지 정리했다."
pubDatetime: 2026-11-09T19:30:00Z
tags:
  - agentic-commerce
  - payments
  - ai-agent
  - fintech
---

Stripe의 카드 발급 문서에는 1회용으로 만든 가상카드에서 결제가 두 번 일어나는 예시가 있다. 15달러 승인이 나면 카드는 규칙대로 바로 해지되는데, 그 뒤에 가맹점이 승인 없이 5달러를 매입 요청으로 보내면 이 돈도 빠져나간다. 문서는 카드사 규칙상 이런 강제 매입(force post)은 처리해야 하니 필요하면 이의 제기를 하라고 안내한다. ([Stripe](https://docs.stripe.com/issuing/controls/lifecycle-controls))

평소라면 드문 예외로 넘길 문장이다. 그런데 올해 들어 AI 에이전트에게 결제를 맡기는 방법으로 이런 가상카드를 고르는 회사가 늘고 있어서, 이 예외가 어디까지 커질 수 있는지 한 번 따져 볼 만하다.

## 1. 에이전트 전용 카드가 한 해에 여럿 나왔다

11월 2일 홍콩 핀테크 위크에서 국경 간 결제 회사 Sunrate가 Agentic Card를 발표했다. 승인받은 AI 에이전트가 결제 수단을 만들고, 결제를 일으키고, 결과를 조회할 수 있는 다통화 기업용 가상카드다. 금액, 업종, 통화, 지역, 유효기간으로 한도를 걸 수 있고, 맡은 작업이 끝나면 카드가 자동으로 만료된다. Mastercard Agent Pay 인증도 받았다. 예시로 든 곳은 온라인 여행사(OTA)였는데, 공급사 대금이나 마케팅 캠페인마다 카드를 따로 발급해 쓰는 방식이다. ([PR Newswire 배포 보도자료](https://finance.yahoo.com/technology/ai/articles/sunrate-launches-agentic-card-enable-090000037.html))

비슷한 제품은 이미 여럿 나와 있다.

| 회사 | 발표 | 상태 | 공개된 통제 |
|---|---|---|---|
| Ramp | 2026년 4월 | 얼리 액세스, Visa Intelligent Commerce 기반 | 거래별 한도, 가맹점 고정 |
| Corpay | 2026년 7월 28일 | 출시 일정과 지역 미공개 | 승인된 거래마다 목적에 맞춘 가상카드 |
| Stripe | 개발 문서 공개 | 신청제, 토큰 결제 경로는 비공개 프리뷰 | 업종, 국가, 금액 한도, 1회용 카드, 실시간 승인 |
| Sunrate | 2026년 11월 2일 | Mastercard Agent Pay 인증 | 금액, 업종, 통화, 지역, 유효기간, 작업 종료 시 만료 |

어느 곳도 이 카드로 거래가 얼마나 일어났는지는 밝히지 않았다. Sunrate 보도자료에도 고객 이름이나 거래액은 없어서, 지금은 제품의 설계를 보는 단계로 보는 게 맞다.

네 회사의 공통점은 새 결제 수단을 만들지 않았다는 데 있다. 기업이 원래 쓰던 가상카드를 그대로 두고, 그 카드를 발급하고 쓰는 주체를 에이전트로 바꿨다. Corpay의 최고 AI 책임자는 가상카드가 정밀한 통제를 걸어 발급할 수 있어서 에이전트 결제에 잘 맞는다고 설명한다. ([Corpay](https://www.corpay.com/corporate-newsroom/20326/corpay-introduces-agent-card-capability-to-power-secure-agentic-commerce)) 이 글은 그 통제가 실제로 어디까지 닿는지를 따라가 본다.

## 2. 권한을 카드 설정으로 옮기면 좋은 점

"방콕의 이 호텔에 3박 숙박비로 300달러까지 내라"는 지시를 카드 설정으로 옮겨 보면 생각보다 많은 부분이 그대로 들어간다. 금액은 거래당 한도로, 호텔이라는 조건은 숙박업 업종 코드로, 언제까지라는 조건은 유효기간으로 바꿀 수 있고, 발급사에 따라서는 특정 가맹점에만 쓰이도록 묶을 수도 있다.

이 방식의 가장 큰 장점은 통제가 언어 모델 밖에서 집행된다는 데 있다. 에이전트가 웹페이지에 숨은 지시에 속아 다른 결제를 시도해도, 발급사의 승인 시스템은 프롬프트를 읽지 않으니 카드 설정을 벗어난 요청을 거절한다. 모델이 속는 건 가정해야 하는 일이다. 구글의 에이전트 결제 프로토콜(AP2)을 레드팀 방식으로 시험한 연구에서는, Gemini 2.5 Flash로 만든 쇼핑 에이전트가 간단한 프롬프트 인젝션에 상품 순위를 조작당하고 민감한 정보를 내줬다. arXiv에 올라온 프리프린트라 결과는 걸러 볼 필요가 있다. ([arXiv](https://arxiv.org/abs/2601.22569))

카드 설정만으로 부족한 판단은 실시간 승인으로 보탤 수 있다. Stripe에서는 결제 시도가 들어올 때마다 금액, 가맹점 이름과 업종 코드, 발급 때 카드에 붙여 둔 메타데이터(에이전트 ID, 주문 번호 같은 것)가 담긴 승인 요청이 기업 서버로 오고, 서버가 승인이나 거절로 답한다. 기본 응답 기한은 2초이고, 그 안에 답하지 않으면 카드의 기본 규칙대로 처리된다. ([Stripe](https://docs.stripe.com/issuing/agents))

에이전트에게 법인카드 번호를 통째로 넘기는 것과 비교하면 훨씬 나은 설계다. 다만 여기까지의 통제는 전부 승인이라는 한 순간에 걸려 있다.

## 3. 승인은 막아도 매입은 못 막는다

카드 결제는 두 단계로 나뉜다. 결제하는 순간 가맹점이 발급사에 이 금액을 써도 되는지 묻는 것이 승인이고, 나중에 실제로 그 돈을 가져가겠다고 청구하는 것이 매입이다. 식당에서 카드를 긁으면 그 자리에서 승인이 나고, 팁을 더한 최종 금액은 그날 밤이나 다음 날 매입으로 들어오는 식이다.

Stripe 문서에 따르면 지출 통제, 실시간 승인 판단, 카드의 활성 여부는 승인 여부를 정할 때만 쓰이고 매입에는 적용되지 않는다. 승인된 건의 매입은 항상 성공한다. 매입은 보통 24시간 안에 들어오지만 호텔, 항공사, 렌터카 회사는 승인 후 31일까지 매입할 수 있다. ([Stripe](https://docs.stripe.com/issuing/purchases/transactions))

가장 흔한 경우는 승인 금액보다 큰 매입이다. 식당 팁처럼 정상적인 사례가 많아서 막을 수 없고, 금액이 지나치면 카드 소유자가 알아채 이의 제기를 해야 한다. 승인 없이 들어오는 강제 매입도 인터넷이 안 되는 기내 단말기처럼 정상적인 사례가 있어서 막지 못한다. 해지도 새 승인을 막을 뿐이라, 이미 승인된 건의 매입이나 강제 매입은 해지 뒤에도 들어온다. 첫 문단의 1회용 카드 예시가 바로 이 경우다.

Stripe만의 사정도 아니다. 다른 발급 플랫폼인 Lithic도 지출 한도로는 강제 매입을 막지 못한다고 적어 두었고, 남은 한도가 100달러인 카드에 90달러 승인이 난 뒤 110달러로 매입되는 경우를 예로 든다. 90달러 승인은 한도 안이라 통과되고, 110달러 매입은 한도와 상관없이 처리된다. ([Lithic](https://docs.lithic.com/docs/spend-limits))

![카드 발급부터 승인, 매입, 환불까지의 시간선. 한도, 업종, 국가, 카드 상태, 실시간 승인 판단은 발급과 승인 구간에서만 작동하고, 승인보다 큰 매입, 승인 없는 매입, 해지 뒤 매입은 그대로 처리된다.](/agentcard-timeline.svg)

_그림 1. 카드 통제가 작동하는 구간과 닿지 않는 구간. Stripe와 Lithic 발급 문서를 바탕으로 그렸고, 세부 동작은 발급사마다 다르다._

한도 계산 자체에도 오차가 있다. Stripe는 지출 집계가 최선 노력 방식이라 실제 결제와 집계 사이에 최대 30초가 걸릴 수 있다고 밝힌다. ([Stripe](https://docs.stripe.com/issuing/controls/spending-controls)) 사람이 카드 한 장을 쓸 때는 신경 쓸 일이 거의 없는 간격이다. 하지만 에이전트 여러 개가 같은 상위 한도 아래에서 몇 초 사이에 결제를 몰아서 일으키면, 집계가 따라잡기 전에 한도를 넘는 승인이 날 수 있다고 본다.

사람이 법인카드를 쓸 때는 이 빈틈을 명세서가 메웠다. 이상한 매입이 있으면 쓴 사람이 알아보고 이의를 제기했다. 에이전트가 하루에 카드 수백 장을 만들고 버리면, 그 명세서를 읽는 사람이 없다.

## 4. 업종 코드는 호텔을 구분하지 못한다

업종 코드는 가맹점이 카드 결제를 받으려고 등록할 때 정해지는 업종 분류다. Booking.com은 숙박업으로 등록된 가맹점만 자사 가상카드를 결제할 수 있고, 그렇지 않으면 "Invalid merchant" 오류가 난다고 안내한다. ([Booking.com](https://partner.booking.com/en-us/help/commission-invoices-tax/payment-products/getting-paid-virtual-credit-cards-vccs-when-using)) 숙박업 코드로 카드를 묶으면 호텔이 아닌 곳의 결제는 확실히 막힌다. 하지만 숙박업으로 등록된 호텔이라면 어느 곳이든 통과한다.

에이전트가 실제로 저지를 법한 실수는 대부분 이 안쪽에서 일어난다. 이름이 비슷한 다른 호텔을 예약하거나, 날짜를 하루 밀리게 잡거나, 다른 시스템에서 이미 낸 숙박비를 한 번 더 내는 실수는 전부 숙박업 코드와 금액 한도를 그대로 통과한다.

승인 요청에 무엇이 들어오는지를 보면 이유가 드러난다. Stripe의 승인 요청 예시에는 금액, 가맹점 이름, 업종 코드, 도시와 국가, 그리고 발급 때 붙인 메타데이터가 있다. 어느 호텔의 몇 박인지, 취소 규정이 무엇인지, 같은 예약을 이미 결제했는지는 없다. 이런 확인을 하려면 기업이 메타데이터에 주문 번호를 붙여 두고, 승인 요청이 올 때 자기 주문 시스템과 대조해야 한다. 가맹점 단위로 묶는 기능이 있긴 하지만 Stripe에서는 아직 비공개 프리뷰이고, Ramp는 결제 자격을 발급받을 때 가맹점 이름과 주소를 함께 넘기는 방식을 쓴다. ([Stripe](https://docs.stripe.com/issuing/controls/spending-controls), [Ramp](https://agents.ramp.com/skills/ramp-agentic-purchase))

![발급사가 승인 순간에 보는 정보와 보지 못하는 정보. 금액, 통화, 상호명, 업종 코드, 국가, 메타데이터, 에이전트 토큰은 실려 오고, 호텔과 날짜, 취소 규정, 이중 결제 여부, 사람의 원래 요청은 실려 오지 않는다. Verifiable Intent는 가맹점, 품목, 금액 범위를 서명해 함께 보낸다.](/agentcard-visible.svg)

_그림 2. 승인 요청에 실려 오는 정보와 빠지는 정보._

카드 네트워크도 이 공백을 알고 있다. Mastercard는 3월 5일 구글과 함께 만든 Verifiable Intent를 공개했는데, 사람이 무엇을 허락했는지를 위변조가 어려운 기록으로 남겨 결제와 함께 보내자는 명세다. ([Mastercard](https://www.mastercard.com/us/en/news-and-trends/stories/2026/verifiable-intent.html)) 2월 18일자 초안 v0.1의 제약 조건 문서는 허용 가맹점, 허용 품목과 수량, 수취인, 금액 범위, 총예산, 정기 결제 두 종류, 결제와 주문의 상호 참조까지 여덟 가지 조건을 정의한다. 이 조건을 검증하는 쪽은 가맹점이나 결제 네트워크다. ([Verifiable Intent](https://github.com/agent-intent/verifiable-intent/blob/main/spec/constraints.md))

품목과 가맹점을 서명된 형태로 함께 보낸다는 점에서 그림 2의 오른쪽 칸을 상당 부분 메운다. 다만 가맹점 조건을 검증하려면 가맹점이 서명한 체크아웃 정보가 있어야 하는데, POS 단말기에 카드번호를 입력해 결제하는 호텔 공급사에게는 보통 그런 정보가 없다. 총예산 조건도 이전에 승인된 금액을 더해서 계산하니, 의도를 확인하는 장치 역시 승인 단계에 걸려 있다.

## 5. 호텔 결제는 에이전트가 떠난 뒤에 일어난다

Sunrate가 첫 사례로 든 여행업은 에이전트가 오기 전부터 가상카드로 대금을 주고받던 곳이다. Booking.com의 사례를 보면 호텔 쪽에서 이 카드가 어떻게 쓰이는지 알 수 있다. Booking.com은 손님이 낸 돈을 임시 Mastercard 가상카드에 담아 호텔에 정산하고, 호텔은 이 카드를 자기 POS에 입력해 결제한다. 환불 불가 예약은 예약일부터, 나머지는 예약이 90% 이상 환불 불가가 되는 시점부터 결제할 수 있다. 신규 숙소처럼 조건을 채우지 못한 곳은 체크인 다음 날부터다. 체크아웃 후 12개월까지 결제할 수 있으며, 잔액이 0이 될 때까지 여러 번 나눠 결제해도 된다. ([Booking.com](https://partner.booking.com/en-us/help/commission-invoices-tax/payment-products/getting-paid-virtual-credit-cards-vccs-when-using))

여기서 "작업이 끝나면 카드가 만료된다"는 설계가 부딪힌다. 에이전트의 작업은 예약을 잡고 카드 정보를 넘기는 순간 끝나지만, 호텔은 체크인 이후나 몇 달 뒤에 카드를 결제한다. 예약이 끝났을 때 카드를 만료시키면 호텔의 정상적인 결제가 거절되고, 숙박이 끝날 때까지 열어 두면 카드는 몇 달 동안 살아 있다. 그동안 들어오는 매입이 맞는지는 이미 다른 일로 넘어간 에이전트가 볼 수 없다.

취소와 환불도 같은 문제를 겪는다. Booking.com에서는 이미 결제한 예약이 취소되면 호텔이 45일 안에 같은 가상카드로 환불해야 하고, 만료된 카드에도 환불할 수 있다. Stripe 쪽에서도 해지된 카드로 환불이 들어오는데, 환불이 원래 승인과 꼭 연결되지는 않아서 엉뚱한 승인에 연결되거나 아예 연결되지 않을 수 있다. ([Stripe](https://docs.stripe.com/issuing/purchases/transactions)) Lithic에서는 월 단위 한도가 환불로 다시 늘어나지 않는다. 900달러를 쓰고 900달러를 환불받아도, 같은 달에 다시 900달러를 결제하면 한도 초과로 거절된다. 예약이 취소돼 다시 잡아야 할 때 에이전트가 이 거절을 만날 수 있다. ([Lithic](https://docs.lithic.com/docs/spend-limits))

중복 결제도 조심해야 한다. Ramp의 공개 결제 스킬은 결제 제출이 시간 초과되거나 결과가 불분명하면 결제가 안 됐다고 추정하지 말고, 새 결제 자격을 받기 전에 그 결제의 상태부터 맞춰 보라고 적어 두었다. ([Ramp](https://agents.ramp.com/skills/ramp-agentic-purchase)) 사람이라면 화면을 새로고침해 볼 일을, 에이전트는 다시 시도하는 쪽으로 처리하기 쉽다.

승인 단계에서 막을 수 없는 일은 결국 매입이 들어온 뒤에 잡아야 하고, 그 수단은 대사다. 작업마다 사람이 승인한 금액과 승인 내역, 매입과 환불 내역을 카드 단위로 묶어 보면 위에서 말한 빈틈이 대부분 드러난다. 아래는 그 뼈대를 pandas로 짠 예시다. 데이터는 설명을 위해 만든 가상 값이다.

```python
import pandas as pd

def reconcile(tasks, auths, txns):
    """작업(사람이 승인한 금액) · 승인 · 매입을 카드 단위로 맞춰 본다."""
    approved = auths[auths.approved].groupby("card_id").amount.sum().rename("authorized")
    caps = txns[txns.type == "capture"]
    captured = caps.groupby("card_id").amount.sum().rename("captured")
    no_auth = caps.auth_id.isna().groupby(caps.card_id).sum().rename("no_auth")
    refunded = txns[txns.type == "refund"].groupby("card_id").amount.sum().rename("refunded")
    late = (caps.merge(tasks[["card_id", "closed_at"]], on="card_id")
                .query("posted_at > closed_at").groupby("card_id").size().rename("late"))
    m = (tasks.set_index("card_id")
              .join([approved, captured, no_auth, refunded, late]).fillna(0))
    m["net"] = m.captured - m.refunded
    checks = {
        "매입>승인": m.captured > m.authorized,
        "승인 없는 매입": m.no_auth > 0,
        "작업 종료 뒤 매입": m.late > 0,
        "순지출>작업 금액": m.net > m.task_amount,
    }
    m["flags"] = [", ".join(k for k, v in checks.items() if v[i]) for i in m.index]
    return m[["task_amount", "authorized", "captured", "refunded", "net", "flags"]]
```

가상의 카드 네 장을 넣으면 이렇게 나온다. 작업 종료일은 모두 11월 3일로 두었다.

| 카드 | 작업 금액 | 승인 | 매입 | 환불 | 순지출 | 표시 |
|---|---|---|---|---|---|---|
| c1 | 300 | 300 | 300 | 0 | 300 | |
| c2 | 300 | 280 | 330 | 0 | 330 | 매입>승인, 순지출>작업 금액 |
| c3 | 120 | 120 | 160 | 0 | 160 | 매입>승인, 승인 없는 매입, 작업 종료 뒤 매입, 순지출>작업 금액 |
| c4 | 200 | 200 | 200 | 200 | 0 | |

c2는 280달러 승인 뒤 330달러로 매입된 경우이고, c3는 1회용 카드가 해지된 뒤 11월 9일에 40달러 강제 매입이 들어온 경우다. c4는 취소 후 전액 환불받은 카드라서 순지출이 0이다. 실무에서는 여기에 통화 환산, 부분 매입, 환불과 원거래의 연결, 이의 제기 기한까지 붙여야 하지만, 카드 설정만으로는 보이지 않던 것을 보이게 만든다는 점은 이 정도로도 충분히 드러난다.

## 6. 카드를 만드는 것도 에이전트라면

Sunrate 보도자료는 승인받은 에이전트가 결제 수단을 직접 만들고 관리한다고 설명한다. Stripe도 계정에 권한이 있으면 Stripe MCP로 에이전트가 카드와 카드 소유자를 만들 수 있게 해 두었다. ([Stripe](https://docs.stripe.com/issuing/agents)) 편리한 기능이지만, 에이전트가 자기가 쓸 카드의 한도까지 정한다면 2절에서 말한 "모델 밖의 통제"는 약해진다. 같은 에이전트가 결제 권한과 카드 설정 권한을 다 갖고 있으면, 프롬프트 인젝션으로 결제를 바꿀 수 있는 공격자는 카드 설정도 바꿀 수 있다.

그래서 한도는 층을 나눠서 걸어야 한다. 가장 바깥은 사람이 정하고 에이전트는 바꿀 수 없는 상위 한도다. 월 예산, 허용 업종, 사람이 직접 확인해야 하는 금액이 여기에 들어간다. 그 안쪽이 에이전트가 작업마다 만드는 카드이고, 가장 안쪽이 에이전트 손에 실제로 들어가는 결제 자격이다. Stripe에서는 카드 소유자 단위 한도가 그 사람의 모든 카드에 걸리고 겹치는 한도 중 가장 엄격한 쪽이 적용된다. 토큰으로 결제할 때는 판매자, 금액, 만료가 묶인 공유 결제 토큰(SPT)의 한도와 카드 한도를 둘 다 통과해야 한다. Ramp에서는 관리자가 열어 준 펀드 안에서만 에이전트가 1회용 결제 자격을 받는다. ([Stripe](https://docs.stripe.com/issuing/agents/programmatic-checkout), [Ramp](https://agents.ramp.com/skills/ramp-agentic-purchase))

![누가 어느 한도를 정하는지 보여 주는 3단 구조. 바깥은 사람이 정하는 상위 한도, 그 안은 에이전트가 만드는 작업별 카드, 가장 안쪽은 일회용 카드번호나 토큰 같은 결제 자격이다.](/agentcard-layers.svg)

_그림 3. 한도를 세 층으로 나누기. 에이전트는 안쪽 두 층만 다룰 수 있어야 한다._

가장 안쪽 층에서는 카드번호 노출이 문제가 된다. 판매자가 Stripe의 MPP나 UCP 같은 프로그램 결제를 지원하면 카드번호 대신 토큰을 넘길 수 있지만, 일반 웹 결제 화면에서는 에이전트가 가상카드의 번호를 받아 입력해야 한다. Stripe 문서는 이 경우 1회용 카드를 쓰라고 안내하고, Ramp의 결제 스킬도 받은 카드 정보를 브라우저로 바로 제출하라고 적어 두었다. 앞서 소개한 레드팀 연구가 보여 준 공격 중 하나가 에이전트에게서 민감한 정보를 빼내는 것이었으니, 카드번호가 모델의 맥락에 들어가는 순간부터는 새어 나갈 수 있다고 가정하는 편이 안전하다. 1회용 카드는 그 피해를 한 건으로 줄여 주지만, 3절에서 봤듯이 그 한 건에도 강제 매입은 들어올 수 있다.

## 7. 개인적인 견해

나는 에이전트 결제를 가상카드에서 시작하는 게 맞는 선택이라고 본다. 모델이 얼마나 똑똑한지와 상관없이 잃을 수 있는 금액이 정해지고, 기업 재무팀이 이미 알고 있는 도구라 도입 장벽도 낮다. 에이전트에게 법인카드 번호를 넘기는 것과는 비교할 수 없이 낫다.

다만 카드 설정이 표현하는 건 "얼마까지, 어떤 업종에서, 언제까지"이고, 그것도 승인 순간에만 확인된다. 에이전트에게 맡긴 일이 제대로 됐는지, 즉 맞는 호텔에 맞는 날짜로 한 번만 결제했는지는 카드 밖에서 확인해야 한다. 그래서 에이전트 결제의 실제 통제는 발급 화면의 한도 설정보다 5절의 대사에 있다고 생각한다. 사람이 명세서를 읽지 않는 구조라면 대사도 자동이어야 하고, 매입이 승인과 다르거나 작업이 끝난 카드에 돈이 나가면 바로 사람에게 넘어가야 한다.

발급사 이상거래 탐지(FDS) 쪽에도 일이 생긴다. 발급사 FDS는 주로 승인 요청 시점에 점수를 매기는데, 에이전트 카드에서 위험이 커지는 곳은 승인과 매입 사이다. 작업 단위로 승인과 매입의 차이를 보는 모델, 해지된 카드에 들어오는 매입을 따로 보는 규칙이 필요해질 것이다.

도입을 검토한다면 데모에서 결제가 성공하는지보다 결제 한 건이 맞게 끝나기까지 사람이 들인 시간과 이의 제기 비율을 재 보는 게 좋겠다. Sunrate의 여행사 사례도 같은 기준으로 평가할 수 있는데, 체크아웃 후 몇 달 뒤 호텔이 카드를 결제하는 날에 그 카드가 어떤 상태인지가 이 설계의 첫 시험이 될 것이다.

**함께 보면 좋은 글:**

- [AI 회사는 결제 회사가 될까: 에이전트가 물건을 사면 누가 돈을 버나](/posts/ai-companies-payments/)
- [AI 에이전트 결제 시대가 오면 무엇이 바뀔까: 중국의 감독 문서와 결제 프로토콜로 미리 보기](/posts/china-agentic-payment-rules/)

## 참고 자료

- [Sunrate Launches Agentic Card to Enable AI-Driven Business Payments (PR Newswire 배포, 2026-11-02)](https://finance.yahoo.com/technology/ai/articles/sunrate-launches-agentic-card-enable-090000037.html)
- [Corpay Introduces Agent Card Capability to Power Secure Agentic Commerce (Corpay, 2026-07-28)](https://www.corpay.com/corporate-newsroom/20326/corpay-introduces-agent-card-capability-to-power-secure-agentic-commerce)
- [Virtual cards for AI agents: How they work and what to look for (Ramp, 2026-04-28)](https://ramp.com/blog/virtual-cards-for-ai-agents)
- [Agent Card Checkout 스킬 (Ramp)](https://agents.ramp.com/skills/ramp-agentic-purchase)
- [Issuing for agents (Stripe Docs)](https://docs.stripe.com/issuing/agents)
- [Pay with a Shared Payment Token from an Issuing card (Stripe Docs)](https://docs.stripe.com/issuing/agents/programmatic-checkout)
- [Issuing transactions (Stripe Docs)](https://docs.stripe.com/issuing/purchases/transactions)
- [Issuing spending controls (Stripe Docs)](https://docs.stripe.com/issuing/controls/spending-controls)
- [Issuing lifecycle controls (Stripe Docs)](https://docs.stripe.com/issuing/controls/lifecycle-controls)
- [Spend Limits (Lithic Docs)](https://docs.lithic.com/docs/spend-limits)
- [When AI starts buying for you, trust becomes the product (Mastercard, 2026-03-05)](https://www.mastercard.com/us/en/news-and-trends/stories/2026/verifiable-intent.html)
- [Verifiable Intent: Constraint Type Definitions, Draft v0.1 (2026-02-18)](https://github.com/agent-intent/verifiable-intent/blob/main/spec/constraints.md)
- [Getting paid by virtual credit cards (Booking.com for Partners)](https://partner.booking.com/en-us/help/commission-invoices-tax/payment-products/getting-paid-virtual-credit-cards-vccs-when-using)
- [Debi & Zhu, Whispers of Wealth: Red-Teaming Google's Agent Payments Protocol via Prompt Injection (arXiv 2601.22569)](https://arxiv.org/abs/2601.22569)

_본 글은 2026년 11월 10일 기준 각 사 발표와 공개 문서를 바탕으로 작성했다. 승인과 매입의 동작은 Stripe와 Lithic 문서를 근거로 했고, 다른 발급사나 Sunrate의 실제 동작은 다를 수 있다. 코드와 표의 거래 데이터는 설명을 위해 만든 가상 값이다._
