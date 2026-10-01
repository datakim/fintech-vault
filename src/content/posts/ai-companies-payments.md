---
title: "AI 회사는 결제 회사가 될까: 에이전트가 물건을 사면 누가 돈을 버나"
description: "Meta가 개인 에이전트 Muse를 무료로 풀고, 성사된 거래에서 작은 수수료를 받겠다고 했다. AI 회사와 결제사와 클라우드가 각자 어느 쪽에서 결제에 다가오는지, 한 번의 거래에 붙는 네 가지 돈에 어떤 책임이 따라붙는지, 수수료를 받는 에이전트는 누구 편인지를 핀테크 쪽에서 본다."
pubDatetime: 2026-10-01T10:00:00Z
tags:
  - agentic-commerce
  - payments
  - ai-agent
  - fintech
  - financial-ai
---

9월 23일, 저커버그가 Meta Connect 무대에서 수수료 얘기를 꺼냈다.

Meta는 9월 초에 개인 에이전트 Muse를 내놨다. 쇼핑을 하고, 익스피디아로 여행을 잡고, 인스타카트로 장을 본다. 메시지를 보내거나 결제를 끝낼 때는 사용자 승인을 받는다. 지금은 미국에서 앱과 웹, 왓츠앱으로 쓸 수 있다.

그날 저커버그는 Muse가 사용자에게 돈을 벌어줄 거라고 했다. 그래서 Muse를 "엄청난 양의 토큰까지" 무료로 풀고, 시간이 지나면 거래에서 작은 수수료를 받아 수익을 내겠다고 했다. 이 수수료는 사는 사람보다 상인 쪽에서 나올 수 있다는 설명도 붙었다.

결제는 Stripe의 Link가 맡는다. 거래마다 일회용 카드를 새로 만들어서 진짜 카드 번호는 밖으로 나가지 않는다. Link의 구매 보호를 받는 첫 에이전트라고 한다.

광고로 돈을 벌던 회사가 거래에서 돈을 떼겠다는 얘기다.

요즘 핀테크 쪽에서는 "AI 회사는 결국 다 결제 회사가 된다"는 말이 자주 들린다. 나는 이 말이 반쯤 맞다고 본다. 어느 쪽 반인지 보려면 결제라는 말부터 쪼개야 한다.

## 1. 같은 결제라도 돈이 다르다

AI 회사가 돈과 엮이는 자리는 생각보다 여러 겹이다.

먼저 자기 상품값을 받는 자리. ChatGPT 구독료 같은 돈이다. 이때 AI 회사는 결제 서비스를 쓰는 평범한 상인이다.

사용자 대신 돈을 내는 자리도 있다. Muse가 호텔을 잡으면 나가는 건 사용자 돈이고, 받는 건 호텔이다. AI 회사는 심부름을 맡은 실행자가 된다.

그리고 성사된 거래에서 떼는 자리. 호텔이 Meta에 수수료를 주면 Meta는 중개자가 된다.

![돈이 오가는 세 자리](/agentpay-roles.svg)

_한 회사 안에 셋이 같이 있을 수 있지만, 셋은 서로 다른 돈이다._

성사 수수료와 결제 처리 수수료도 다른 돈이다. 여행 플랫폼이 예약 수수료를 받는다고 결제 회사라고 부르진 않잖나. Muse가 노리는 건 지금 보기엔 앞쪽, 성사 수수료에 가깝다.

그래도 작은 변화는 아니다. 광고는 무엇을 살지에 영향을 주고 받는 돈이었다. 에이전트가 사는 데까지 해주면 팔린 것에 대해 돈을 받을 수 있다. 구매 결정에 미치던 힘이 구매를 끝내는 힘으로 늘어나는 셈이다.

대신 떠안는 것도 생긴다.

결제가 실패하면, 물건이 안 오면, 엉뚱한 걸 샀으면 사용자는 에이전트를 탓한다. 돈은 Stripe가 옮겨도 일을 잘했는지는 에이전트가 평가받는다.

## 2. 계산대까지 가본 AI 회사들

다른 AI 회사들도 결제 쪽으로 걸어왔다. 걸어온 길은 좀 다르다.

OpenAI는 2025년 9월 Stripe와 Agentic Commerce Protocol(ACP)을 내놨다. ChatGPT 안에서 바로 사는 Instant Checkout도 같이 나왔다. 그리고 2026년 3월에 방향을 틀었다. 첫 Instant Checkout이 원하던 만큼 유연하지 못했다면서, 상인이 자기 결제 화면을 쓰게 하고 자기들은 상품 발견에 집중하겠다고 했다.

Google은 표준 쪽으로 갔다. 2025년 9월에 Agent Payments Protocol(AP2)을, 2026년 1월에는 Universal Commerce Protocol(UCP)을 발표했다. UCP는 Shopify, Etsy, Wayfair, Target, Walmart와 같이 만들었고, 검색의 AI Mode와 Gemini 결제에 붙는다.

Perplexity는 2025년 11월 PayPal과 Instant Buy를 냈다. 신원 확인과 결제, 구매자·판매자 보호는 PayPal이 맡는다.

Anthropic은 9월 2일 Claude Commerce Agents라는 공개 설계도를 내놨다. 상품을 찾아 장바구니를 채우는 쇼핑 에이전트, 그리고 재고·가격·마케팅을 다루는 상인 운영 에이전트. 둘 다 상인의 웹사이트와 앱, 백오피스 안에 들어간다. PYMNTS 보도에 따르면 이 설계도에는 결제 프로토콜도, 상품 카탈로그도, 광고 층도 없다. 계산대와 고객 관계는 상인에게 그대로 남겨뒀다.

이 중에서 제일 많은 걸 말해주는 건 OpenAI의 후퇴라고 본다.

체크아웃은 버튼 하나가 아니다. 그 뒤에 회원 등급과 쿠폰, 적립금이 붙어 있다. 재고와 배송, 반품과 고객 데이터도 다 거기 걸려 있다. 상인 입장에선 계산대를 넘기는 순간 이걸 통째로 넘기는 셈이다.

배달앱을 떠올리면 쉽다. 주문을 앱이 받는 순간 손님 연락처와 리뷰와 재주문이 앱 쪽으로 간다. 식당 사장님들이 배달앱에 그렇게 예민한 이유다.

그래서 길이 둘로 갈린다. 사용자와 거래를 자기 입구에 두려는 쪽이 있다. Meta, 그리고 처음의 OpenAI. 상인의 입구를 AI로 바꿔주려는 쪽도 있다. 지금의 Anthropic. 어느 쪽이든 실제 결제 처리는 Stripe나 PayPal 같은 결제사에 맡긴다.

## 3. 결제사와 클라우드는 반대쪽에서 온다

결제사도 가만히 있지 않는다. 이쪽은 AI 회사의 돈 문제를 통째로 맡겠다는 쪽에 가깝다.

Stripe는 2026년 1월 14일 사용량 기반 과금 회사 Metronome 인수를 마쳤다. 보도 기준 약 10억 달러. Metronome은 OpenAI, Anthropic 같은 AI 회사의 과금을 맡아 온 곳이다. 8월 19일에는 OpenRouter 인수에 합의했다. 400개 넘는 모델 사이에서 요청을 나눠주는 게이트웨이다. 금액은 공개되지 않았고, 70억 달러가 넘는다는 보도가 나왔다.

내 눈엔 AI 회사 손익계산서의 양쪽을 잡는 그림으로 보인다. Metronome은 들어오는 돈 쪽이다. 고객이 쓴 만큼 청구서를 만드는 일. OpenRouter는 나가는 돈인 모델 사용료 쪽에 서 있다.

상인 쪽 장치도 있다. Stripe는 2025년 12월 Agentic Commerce Suite를 냈다. 상인이 연동 한 번으로 여러 AI 에이전트에 물건을 팔 수 있게 해준다. 에이전트가 구매자의 결제 수단을 상인에게 넘길 때는 공유 결제 토큰(Shared Payment Token)을 쓴다.

Muse의 일회용 카드도 같은 생각이다. 에이전트가 돈을 쓰게는 하되, 진짜 카드는 보여주지 않는다.

카드사도 비슷한 걸 깔았다. Mastercard는 2025년 4월 Agent Pay를 발표했다. 에이전트를 먼저 등록시키고 에이전트 전용 토큰으로 결제하게 하는 구조다. Visa도 같은 달 Intelligent Commerce를 내놨고, 파트너 명단에 Anthropic과 OpenAI가 있었다.

클라우드 쪽에서는 아예 프로그램끼리 돈을 주고받는 길이 생기고 있다.

Coinbase가 만든 x402는 웹 표준에 오래 잠들어 있던 '402 Payment Required' 응답을 깨웠다. 유료 API가 402를 돌려주면 에이전트가 그 자리에서 스테이블코인으로 값을 치르고 다시 요청한다. AWS는 8월 18일 Bedrock AgentCore payments를 정식 출시했다. 에이전트가 Coinbase나 Stripe Privy 지갑으로 유료 API, MCP 서버, 콘텐츠 값을 낸다. 결제 세션마다 최대 금액과 만료 시간을 건다.

에이전트가 데이터 한 번 조회하려고 회원가입하고 월 구독까지 할 수는 없다. 쓴 만큼 그 자리에서 내는 길이 필요하고, 클라우드가 그 길을 실행 환경에 붙이는 중이다.

## 4. 한 번의 거래에 붙는 네 가지 돈

세 갈래가 한 거래에서 만나면 돈도 여러 갈래로 나뉜다. Muse가 사용자 대신 호텔을 잡는다고 해보자.

호텔을 골라준 값이 있다. 성사 수수료다. 저커버그가 말한 그 돈이고, 에이전트 쪽으로 간다.

돈이 카드에서 호텔 계좌까지 건너간 값도 있다. 결제 처리 수수료. 카드사와 결제사가 나눠 가진다.

에이전트가 일하면서 쓴 모델과 API 값이 있다. 쓴 만큼 청구서를 만드는 과금 도구가 여기 낀다. Metronome이 서 있는 자리다.

에이전트가 돌아간 클라우드와 지갑, 한도 관리의 값도 있다. 실행 인프라다.

![한 번의 거래에 붙는 네 가지 돈](/agentpay-four-revenues.svg)

_모든 거래에 넷이 다 붙지는 않는다. 받는 회사도 다 다를 수 있다._

넷은 받는 사람도 다르지만, 따라붙는 책임이 더 다르다.

결제 일을 옆에서 본 사람이면 여기서 하나가 눈에 걸린다. 결제 처리 수수료는 얇다. 거래액의 몇 퍼센트를 카드사와 결제사가 나눠 갖는다. 그런데 사고가 나면 책임은 두껍다. 도용, 차지백, 환불, 정산 오류가 다 이쪽으로 온다. 마진은 몇 퍼센트인데 사기 한 건의 손실은 거래액 전부다.

결제 처리는 위험을 관리하는 사업에 가깝다.

AI 회사들이 계산대는 결제사에 맡기고 성사 수수료를 챙기려는 것도 이렇게 보면 자연스럽다. OpenAI가 체크아웃에서 물러선 것도, Anthropic이 결제를 빼고 설계도를 낸 것도 같은 판단이지 싶다.

그래서 "AI 회사가 결제 회사가 된다"는 말은 반만 맞다고 본다. 돈의 흐름에는 끼어든다. 결제 처리의 책임까지 지겠다는 AI 회사는 아직 거의 없다.

## 5. 수수료를 받는 에이전트는 누구 편인가

성사 수수료 쪽에는 다른 문제가 기다린다.

조건이 거의 같은 호텔이 두 곳 있다. 한 곳은 하룻밤에 2만 원 싸다. 다른 곳은 플랫폼에 수수료를 더 준다. 에이전트는 어디를 잡을까?

금융에선 오래된 문제다. 미국 증권가에는 브로커가 고객 주문을 특정 시장조성자에게 넘기고 대가를 받는 관행이 있다. 주문흐름 대가(PFOF)라고 부른다. 수수료 무료 주식 앱이 가능했던 배경으로 자주 꼽히는데, 고객이 정말 가장 좋은 가격에 체결됐는지가 늘 의심을 받는다. 그래서 미국은 브로커가 주문을 어디로 보냈고 대가를 얼마나 받았는지 공시하게 한다. 한국 자본시장법에도 고객 주문을 가장 유리한 조건으로 처리하라는 최선집행의무가 있다.

에이전트 쇼핑도 같은 구조다. 상인이 낸 수수료가 추천 순서에 영향을 줬는지, 줬다면 사용자에게 알렸는지가 문제가 된다.

Meta가 수수료를 상인 쪽에서 받을 수 있다고 한 대목이 그래서 눈에 걸린다. 내가 찾아본 범위에서는 Muse가 수수료를 추천에 어떻게 반영하는지 공개된 내용이 없다.

사용자가 에이전트에게 결제를 맡기는 건 그게 내 편에서 골라준다고 믿어서다. 그 믿음이 깨지면 맡겼던 권한도 금방 거둬들인다.

그래서 권한 화면이 결제 승인 버튼 하나로 끝나면 곤란하다. 에이전트가 얼마까지 쓸 수 있는지, 무엇을 대신 정할 수 있는지, 추천에 돈이 섞였는지가 보여야 한다. 잘못 샀을 때 누구에게 따지면 되는지도.

## 6. 승인할 때 묻는 질문이 바뀐다

사기 탐지(FDS)를 강의하고 글로 써온 입장에서 제일 흥미로운 건 이 부분이다.

사람이 결제할 때 사기 탐지는 한 가지를 묻는다. 이 카드 주인이 지금 결제하는 게 맞나. 그래서 기기와 위치와 평소 결제 습관을 본다. 이 구조는 [Stripe Radar 글](/posts/fds-stripe-radar/)에서 다뤘다.

에이전트 결제에서는 결제하는 게 처음부터 사람이 아니다. 기기는 클라우드에 있다. 결제 패턴도 사람 같지 않다. 그래서 질문이 "주인이 맞나"에서 "위임받은 범위 안인가"로 옮겨간다.

Google AP2는 이걸 서명된 기록으로 남긴다. 사용자의 요청을 담은 의도 위임서(Intent Mandate). 상인이 서명한 장바구니에 사용자가 같이 서명하는 장바구니 위임서(Cart Mandate). 그리고 카드 네트워크로 넘어가는 결제 위임서(Payment Mandate)가 있다. 결제 위임서에는 결제 순간 사람이 있었는지를 표시하는 값이 들어가고, 카드 발급사의 리스크 엔진이 그걸 본다.

![사람이 결제할 때와 에이전트가 결제할 때](/agentpay-risk.svg)

_승인 질문도, 분쟁의 증거도, 피해를 줄이는 장치도 달라진다._

분쟁도 달라진다. 카드 분쟁은 보통 둘로 나뉜다. 내가 하지 않은 결제(부정 사용), 그리고 받은 게 다른 결제(상품 분쟁). 에이전트가 엉뚱한 걸 샀다면 어느 쪽일까? 시킨 건 맞는데 산 게 틀렸다. 이 회색지대를 가르는 증거가 위임 기록이다.

피해를 줄이는 방식도 같은 생각에서 나온다. Muse의 일회용 카드는 거래 한 건에서 끝난다. AWS의 결제 세션에는 최대 금액과 만료 시간이 걸린다. 에이전트가 틀릴 수 있다고 보고, 틀려도 피해가 그 한 건과 그 한도 안에서 끝나게 해두는 설계다.

모델을 만드는 쪽에도 일이 생긴다. 사기 탐지 모델의 피처가 바뀔 거다. 기기 지문이나 입력 속도 대신 에이전트 신원, 위임 한도 대비 결제 금액, 사람 확인 여부 같은 게 들어온다. 라벨도 바뀐다. 에이전트가 잘못 산 거래는 사기도 정상도 아닌 새 클래스가 되지 싶다.

## 7. 개인적인 견해

AI 회사가 결제 회사가 될지 묻는다면, 나는 이름보다 실패한 거래를 누가 치우느냐가 갈림길이라고 본다.

돈의 흐름에 끼어드는 건 쉬워졌다. 프로토콜도 토큰도 지갑도 다 나와 있다. 어려운 건 그다음이다. 잘못 산 물건을 돌려받고, 두 번 빠져나간 돈을 돌려주고, 왜 그 호텔을 골랐는지 설명해야 한다. 결제사가 수십 년 동안 해온 일이 이쪽이다.

그래서 내가 지켜볼 숫자는 거래액보다 분쟁률이다. 에이전트가 산 주문의 환불·분쟁 비율이 사람이 산 주문보다 높은지 낮은지. 낮게 나오기 시작하면 사람들은 더 큰 결제를 맡길 거고, 그때부터 성사 수수료가 진짜 사업이 된다.

한국 쪽도 궁금하다. 국내 간편결제는 이미 앱 안에 깊이 들어와 있다. 에이전트용 일회용 토큰이나 위임 한도를 먼저 내놓는 곳이 이 판에서 Link 같은 자리를 잡을 가능성이 크다고 본다.

Muse도 언젠가 호텔을 잘못 잡는 날이 온다. 그날 항의를 Meta가 받을지, Stripe가 받을지, 호텔이 받을지. 지금 나온 발표들만으로는 아직 답이 안 보인다.

---

**함께 보면 좋은 글:**

- [AI가 결제하는 시대가 온다: 알리페이 AI付·AI收와 에이전트 경제의 시작](/posts/alipay-ai-payment-era/)
- [\[FDS\] Stripe는 어떻게 100ms 안에 결제 사기를 판단할까?](/posts/fds-stripe-radar/)
- [아빠오(阿宝)가 온다: 알리페이, 10억 사용자를 위한 AI 네이티브 슈퍼앱으로의 진화](/posts/alipay-ah-bao/)

## 참고 자료

- [所有 AI 公司，最终都会成为支付公司 (Stablehunter, 2026-09-14)](https://mp.weixin.qq.com/s/iwuC66uB0a3efnDtNTPNUA)
- [Meta launches personal AI agent with Stripe-powered checkout (The Paypers, 2026-09-09)](https://thepaypers.com/payments/news/meta-launches-personal-ai-agent-with-stripe-powered-checkout)
- [Meta CEO Mark Zuckerberg Reveals Muse AI Agent Will Take a 'Fee From Transactions' (Yahoo Finance)](https://finance.yahoo.com/technology/ai/articles/meta-ceo-mark-zuckerberg-reveals-162437502.html)
- [OpenAI revamps shopping experience in ChatGPT after struggling with Instant Checkout (CNBC, 2026-03-24)](https://www.cnbc.com/2026/03/24/openai-revamps-shopping-experience-in-chatgpt-after-instant-checkout.html)
- [Announcing Agent Payments Protocol (AP2) (Google Cloud, 2025-09-16)](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol)
- [Universal Commerce Protocol (ucp.dev)](https://ucp.dev)
- [PayPal and Perplexity Launch Instant Buy (PayPal, 2025-11)](https://newsroom.paypal-corp.com/2025-11-PayPal-and-Perplexity-Launch-Instant-Buy)
- [Anthropic debuts Claude features focused on agentic commerce (Digital Commerce 360, 2026-09-02)](https://www.digitalcommerce360.com/2026/09/02/anthropic-debuts-claude-features-focused-on-agentic-commerce/amp/)
- [Anthropic Debuts Commerce Agent Blueprint With Visa and Mastercard (PYMNTS, 2026-09-03)](https://www.pymnts.com/news/artificial-intelligence/2026/anthropic-built-the-shopping-brain-and-skipped-the-wallet/)
- [Metronome + Stripe: Building the future of billing (Stripe)](https://stripe.com/blog/metronome-stripe-building-the-future-of-billing)
- [Stripe to buy OpenRouter as fintech expands deeper into AI (CNBC, 2026-08-19)](https://www.cnbc.com/2026/08/19/stripe-openrouter-fintech-ai-model-marketplace-.html)
- [Stripe launches the Agentic Commerce Suite (Stripe)](https://stripe.com/newsroom/news/agentic-commerce-suite)
- [Mastercard unveils Agent Pay (Mastercard, 2025-04)](https://www.mastercard.com/global/en/news-and-trends/press/2025/april/mastercard-unveils-agent-pay-pioneering-agentic-payments-technology-to-power-commerce-in-the-age-of-ai.html)
- [Visa Intelligent Commerce (Visa)](https://corporate.visa.com/en/products/intelligent-commerce.html)
- [x402 (x402.org)](https://www.x402.org)
- [Amazon Bedrock AgentCore payments is now generally available (AWS, 2026-08-18)](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-agentcore-payments-is-now-generally-available-enabling-agents-to-transact-safely-and-autonomously-at-scale/)

_본 글은 2026년 10월 1일 기준 공개 보도와 기업 발표 자료를 바탕으로 작성했다. 인수 금액은 보도 기준이며 회사가 공식 발표한 숫자가 아니다. Muse의 수수료율과 추천 방식은 내가 찾아본 범위에서 공개된 내용이 없다. 증권사 주문흐름 대가(PFOF) 비유는 구조를 설명하려는 것이고, 에이전트 커머스에 같은 규제가 적용된다는 뜻은 아니다._
