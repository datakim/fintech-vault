---
title: "The Age of AI Paying: Alipay's AI付, AI收 and the Start of the Agent Economy"
description: "Alipay announced 300 million AI agent payments alongside Token Pay and AI Wallet. Not a payment feature but an early large-scale commercialisation of agentic commerce infrastructure — an AI acting within delegated authority to pay, collect and settle."
pubDatetime: 2026-05-26T12:00:00Z
koSlug: alipay-ai-payment-era
tags:
  - financial-ai
  - ai-agent
  - alipay
  - fintech
  - agentic-commerce
  - payments
---

![Alipay Unveils Next-generation AI Payment Infrastructure](/images/alipay/overview.png)

_Alipay's next-generation AI payment infrastructure. (Source: Alipay announcement material)_

## 1. Why "AI payments" now?

Anyone who has used ChatGPT, Claude or Gemini has felt it already. AI no longer stops at finding information. It understands intent, compares, recommends, builds an itinerary, calls the service you need — closer to an **executor of actions.**

But there is one point where an AI carrying a real-life task to completion always gets blocked: **payment.**

Ask an AI to plan a weekend trip. It can compare flights, recommend hotels, find restaurants, assemble an itinerary. To actually book the flight or pay for the hotel, though, you still have to move to a payment page. At that moment the AI's flow breaks.

That is the background to AI付 and AI收. If AI handles recommendation and execution, payment infrastructure has to change to fit a conversational, agent-shaped flow too. Alipay launched AI付 in September 2025 and AI收 in April 2026, connecting both directions — agent payment and agent collection.

More precisely, this is less "an era where AI spends money entirely on its own" and closer to **an era where AI executes payment inside a scope the user has delegated.** Understanding that distinction matters. The essence of agent payments is not automation but **delegated authority and controllable execution.**

## 2. AI付: ordering and paying inside the conversation

AI付 lets a user order and pay for goods in plain language inside the screen where they are talking to an agent. It minimises jumps to another app, a cart, a payment page, and carries ordering and payment through the conversation.

The flagship case is Lucky AI, Luckin Coffee's ordering assistant. A user calls Lucky AI in Luckin's Alipay mini program or in the Luckin app, orders a coffee by speaking, says "下单" to place it, and completes payment after identity verification. Previously, even when the AI helped with the order, the final payment required a separate page; AI付 pulled that flow into the conversation.

The flow runs roughly like this.

1. The user tells the assistant to order two iced americanos.
2. The AI confirms the order and asks about payment.
3. The user approves.
4. Identity verification or authentication completes the payment.
5. The user sees the result and the receipt inside the conversation.

The point is not that clicks went down. The more important change is that **the boundaries between browsing, recommendation, ordering and payment collapse into one conversational flow.** In existing commerce, the user searched, compared, added to a cart and moved to a payment page. AI付 points elsewhere: the user states intent, the AI executes, and payment dissolves into that flow.

## 3. AI收: collecting each time an AI service is called

If AI付 changes the consumer payment experience, AI收 changes the monetisation structure for developers and merchants.

AI收 is collection infrastructure that lets merchants and individual developers charge per user call when providing a paid service through an agent. It launched officially on 28 April 2026, aimed at developers and merchants providing commercial services through agents such as OpenClaw (Chinese name 龙虾).

Say a user asks an agent to summarise the latest industry analysis report. The agent requests the necessary resources from a server and checks the price. The user pays ¥0.02, that amount lands in the provider's AI收 account, and the agent delivers the result. The example given in reporting is likewise call-based charging at ¥0.02 granularity.

![AI收 three-step onboarding: register → create app → install SDK](/images/alipay/ai-shou-3step.png)

_AI收 connects to per-call instant collection in three steps: register, create an app, install the SDK. (Source: Alipay)_

What matters here is **collection** rather than payment.

For an agent ecosystem to grow, developers providing models, data, reports, APIs, expertise and automation tools need to be able to take money in very small units. Existing SaaS mostly charges a monthly subscription. Services in the agent era are likely to move toward a few cents per call.

AI收 addresses exactly that. Not advertising, not subscription, not app store in-app purchase, but **call-based monetisation.**

Alipay described a 0% fee for individual developers through 31 December 2026, and integration through a relatively simple sequence: registration, app creation, server SDK installation. That is less a promotion than a strategy to draw individual developers and small AI service providers in first and make Alipay the default rail for payment and collection inside the agent ecosystem.

## 4. What changes when AI付 and AI收 meet

Seen separately, AI付 looks like a consumer payment feature and AI收 like a developer collection feature. Working together they mean something else.

AI付 is the channel by which a user pays through AI. AI收 is the channel by which developers and merchants receive money through AI calls. On one side an AI takes the user's request and executes payment; on the other, the service provider the AI called collects automatically. Connect them and a closed loop forms.

> user intent → AI understands → service call → price presented → user approves → payment → collection → result delivered → transaction recorded

The loop matters because it addresses the three hardest problems in AI commerce at once. First, **who holds payment authority.** Second, **on what basis the AI chose that service.** Third, **who gets settled, and how.**

In existing e-commerce that flow was split across web pages, apps, card networks, PSPs and seller systems. In an agent era the user decides inside a conversation without moving screens, so the trust structure of payment and settlement has to be redesigned conversationally too.

On that reading AI付 and AI收 are less convenience features than **the transaction rails of the agent economy.**

## 5. The ACT protocol: a common language for AI commerce

Looking only at AI付 and AI收 is not enough to understand Alipay's strategy. Underneath sits ACT — the Agentic Commerce Trust Protocol.

In January 2026 Alipay announced ACT together with the Qwen App, Taobao Instant Commerce, Rokid, Damai and Alibaba Cloud Bailian. It was presented as an open technical framework for AI to work with e-commerce, food delivery, ticketing and local service platforms. Its core purpose is a common language between agents and service platforms.

ACT should not be read as merely a payment protocol. More precisely it is a commerce protocol standardising the **trust, authority, invocation and traceability** an AI needs when it finds a service, calls it, and executes a transaction under delegated authority.

AI付, AI收, Token Pay and AI Wallet each take a role on top of that.

| Component | Role | What it means in fintech terms |
| --- | --- | --- |
| **AI付** | consumer → AI → payment | payment closing inside a conversational UI |
| **AI收** | developer/merchant → AI → collection | real-time micropayments for microservices |
| **Token Pay** | payment solution for AI model companies | B2B settlement per API call |
| **AI Wallet** | a user-facing AI wallet | visibility and control over agent spending |

![The stage where Alipay announced 300 million AI payments](/images/alipay/3eok-stage.jpg)

_In May 2026 Alipay announced that AI支付 had processed 300 million AI agent payments. (Source: Alipay event)_

Alipay stated in May 2026 that AI支付 had processed 300 million agent payments and supported 95% of major general-purpose agent frameworks, while unveiling Token Pay and AI Wallet. Those figures are Alipay's own rather than independently verified industry statistics, but the direction is clear. Alipay treats AI-era payment infrastructure as a full stack — **payment, collection, settlement, wallet, protocol** — rather than a single feature.

## 6. A personal view

The reason this announcement drew relatively little attention outside China is that on the surface it looks like another Chinese convenience payment feature. From a data and platform strategy perspective, I think a far larger change is hiding in it.

What lands hardest is the change in who transacts. E-commerce has been understood through C2C, B2C, B2B. AI付 and AI收 wedge a new party in: the agent. It is hard to say AI has become a fully independent economic actor at this stage — the user's approval, authentication and delegation scope still matter. But the fact that "user → AI → service → payment → collection" is now connected inside one commercial infrastructure makes it worth reading as an early form of an agent-to-agent economy. Before long, a user's scheduling AI calling a travel booking AI, or a company's procurement AI calling a supplier's quoting AI, could feel ordinary. The genuinely hard problem then is not the technology of AIs talking to each other but the structure through which money moves safely behind that conversation.

The other interesting point is that micro-transactions finally become real. AI收's ¥0.02 per-call charge was uneconomic under existing card and transfer structures — fees, settlement cost and user friction were too large. When an agent calls a service, the unit of charging changes. There is no need for a monthly subscription. Call once when needed, pay for that. This will not replace SaaS subscriptions outright, but it makes pay-per-use much more natural for call-friendly services: data lookup, report generation, expert summarisation, image processing, code execution, financial analysis, legal and tax drafting.

Alipay's 0% fee for individual developers through the end of 2026 also reads as prioritising ecosystem capture over near-term revenue. Payment infrastructure has strong network effects. More developers bring more users; more users bring more merchants. Early on, owning the standard matters more than the fee. Visa and Mastercard took that position in the card era, Alipay and WeChat Pay in the mobile era. In the agent era, who becomes the default rail for agent payment and collection is the new contested point.

And perhaps most important is the change in the data. Payment data used to be close to "who spent how much, when and where." In AI payments, the context in front of it comes attached. What the user asked for, what the AI recommended, which alternatives were compared, which conditions the user weighted, what they finally bought, whether they were satisfied afterwards. That is not transaction data but intent data — a powerful asset for a fintech or commerce platform. Existing recommenders inferred taste from clicks, carts and purchase history; in agentic commerce the user says outright what conditions they want. A payment platform that captures that flow has a far richer basis for recommendation, risk management, credit scoring, marketing and personalisation.

## 7. But the core is control, not convenience

The biggest risk in AI payments is not a failed payment. The larger problem is a transaction executing while the user does not know what they agreed to.

In existing payments the user checked a product page, a cart and a payment page in sequence. In AI payments, recommendation, comparison, ordering and payment compress into a conversation window. The more convenient it gets, the more the user's cognitive confirmation step can shrink.

So competitiveness ahead depends less on how fast you can get someone to pay than on how well you design three things.

1. How far the user has delegated authority to the AI
2. On what basis the AI selected the product or service
3. Whether the user can easily review, cancel, restrict and control activity afterwards

On that reading AI Wallet has the potential to become not a wallet but the spending control panel of the agent era. Genuine agent payments require being able to see which AI holds which authority, which agent spent how much, and which services were called.

The future of AI payments is not completed by frictionless payment alone. What matters more is **a design that removes friction while leaving the necessary control.**

## 8. The global picture: not only an Alipay story

Alipay's move should not be read only inside the Chinese market. Global payment networks and AI platforms are already moving the same way.

OpenAI and Stripe announced Instant Checkout and the Agentic Commerce Protocol in September 2025, letting users buy inside ChatGPT. It began with US users buying from Etsy sellers, with Shopify seller support signalled.

Visa, through Visa Intelligent Commerce, describes providing APIs, standards and payment networks so agents can transact safely on behalf of consumers and businesses.

Mastercard unveiled Agent Pay in 2025, presenting a structure for registering and authenticating trusted agents and paying safely on a user's behalf. Mastercard emphasises agent registration, authentication, tokenisation and transaction control as core elements.

So AI付 and AI收 are not an isolated case. The larger current is clear. The payments industry is moving from **payment a person presses** to **payment an AI executes under delegation.**

What makes the Alipay case interesting is the attempt to bind consumer payment, developer collection, AI Wallet, Token Pay and the ACT protocol into one ecosystem. Where OpenAI and Stripe focus on the checkout experience inside an AI platform, and Visa and Mastercard emphasise trust infrastructure on global card networks, Alipay is putting forward an integrated **AI-native payment stack.**

## 9. What this means for fintech elsewhere

Agent technology is developing quickly in Korea too. Naver, Kakao, Toss, Coupang, Baemin, financial institutions and commerce platforms are all attaching AI to their services. Most of it still sits at recommendation and consultation.

The real change arrives when AI understands intent and then carries it through to an actual transaction.

The questions worth working through: what authentication and approval flow do you offer when an agent requests payment? How do you set the limit and scope a user can delegate? How do you provide collection and settlement to the external services and developers an AI calls? On what screen does a user control an agent's spending and permissions? And how do you separate and protect payment data from intent data?

For payment businesses, AI payments are not a new feature. If agents become the entry point for search, shopping, booking and financial activity, payment businesses have to define their position inside the agent ecosystem all over again.

The same applies to commerce platforms. Until now users came to a search box and looked for products. Ahead, a user's agent may ask a platform for products matching conditions. If product information, price, stock, delivery, reviews and return policy are not offered in a form an AI can understand, that platform can drop out of the agent's option set.

## 10. Payment keeps getting less visible

AI付 and AI收 are not a "pay by speaking" feature. They are an attempt to connect payment, collection, settlement, authority and traceability so that AI can execute part of economic activity on a person's behalf.

A full agent-to-agent economy has not opened yet, of course. User approval and authentication still matter, and transparency about the reasoning behind an AI-executed payment needs strengthening. Regulation, consumer protection, refunds, dispute handling and data privacy all remain.

Still, the direction is clear. Payment used to be a person taking out a card. In the mobile era it was a person opening a phone. In the AI era it may become a structure where the user states intent, the AI executes, and payment is handled quietly behind that flow.

The point to watch from a fintech seat is less the technology than the new transaction structure this infrastructure creates. The competition ahead is likely to move from who builds the better chatbot to **who holds the trust rails on which an agent can safely spend and receive money.**

The era of AI opening the wallet entirely on its own is not here. But the era in which AI pays inside a delegated scope, and providers collect per call, has already started. And that change could force a redesign not only of payments but of commerce, SaaS, API businesses, financial data and the developer economy as a whole.

---

## Keywords

Alipay AI付, Alipay AI收, Agentic Commerce Trust Protocol, Token Pay, AI Wallet, Agentic Commerce Protocol, Visa Intelligent Commerce, Mastercard Agent Pay

## References

- [支付宝宣布完成AI支付的全域布局 — STCN](https://www.stcn.com/article/detail/3927539.html)
- [支付宝推出"AI付"服务，在智能体内说话完成下单支付 — 新华网](https://www.news.cn/tech/20250911/d2b40fe724684cdabcd0997bb742ad17/c.html)
- [0费率免费使用！支付宝AI 收正式上线三步接入即时收款 — Sina](https://finance.sina.com.cn/tech/discovery/2026-04-28/doc-inhwaavw8466616.shtml)
- [支付宝与千问App、淘宝闪购等发布中国首个AI商业协议ACT — 东方财富](https://finance.eastmoney.com/a/202601163621688078.html)
- [Buy it in ChatGPT: Instant Checkout and the Agentic Commerce Protocol — OpenAI](https://openai.com/index/buy-it-in-chatgpt/)
- [Visa Intelligent Commerce — Visa](https://corporate.visa.com/en/products/intelligent-commerce.html)
- [Mastercard unveils Agent Pay — Mastercard](https://www.mastercard.com/global/en/news-and-trends/press/2025/april/mastercard-unveils-agent-pay-pioneering-agentic-payments-technology-to-power-commerce-in-the-age-of-ai.html)

---

_Written as of 26 May 2026 from public reporting and company announcements. Some figures are Alipay's own and may not be independently verified industry statistics._

**Related posts:**

- [Ah Bao Arrives: Alipay's Turn Toward an AI-Native Super App](/en/alipay-ah-bao/)
- [WeChat's Different Road: A 1.4 Billion MAU Super App Absorbs the Agent](/en/wechat-ai-strategy/)
- [\[FDS\] How Does Stripe Judge Payment Fraud in 100ms?](/en/fds-stripe-radar/)
