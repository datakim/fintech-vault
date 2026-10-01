---
title: "Will AI Companies Become Payments Companies? Who Makes Money When an Agent Buys"
description: "Meta plans to keep its personal agent Muse free and take a small fee from the transactions it completes. Where AI companies, payment firms and clouds are each coming at payments from, the four kinds of money on one agent purchase and the liability attached to each, and whose side a fee-earning agent is on, seen from fintech."
pubDatetime: 2026-10-01T10:00:00Z
koSlug: ai-companies-payments
tags:
  - agentic-commerce
  - payments
  - ai-agent
  - fintech
  - financial-ai
---

On 23 September, Mark Zuckerberg brought up fees on stage at Meta Connect.

Meta had launched Muse, its personal agent, earlier in the month. It shops, books travel through Expedia and orders groceries through Instacart. It asks for approval before sending a message or completing a purchase. For now it runs in the US, in an app, on the web and inside WhatsApp.

Zuckerberg said Muse would make its users money. Meta would make it free "for a huge number of tokens" and, over time, profit by taking a small fee from transactions. That fee, the explanation went, could come from merchants rather than buyers.

Payment runs through Stripe's Link. Each transaction gets a fresh one-time card, so the real card number never leaves. Muse is described as the first agent covered by Link's purchase protections.

A company that made its money on ads now wants a cut of the deal.

In fintech circles you hear a line a lot lately: every AI company eventually becomes a payments company.

I think it is about half right. To see which half, you have to take the word "payments" apart first.

## 1. Same payment, different money

An AI company touches money in more places than it first appears.

The first is getting paid for its own product, like a ChatGPT subscription. Here the AI company is an ordinary merchant using a payment service.

The second is paying on the user's behalf. When Muse books a hotel, the money going out is the user's and the hotel receives it. The AI company is an executor running an errand.

The third is taking a cut of a completed deal. If the hotel pays Meta a fee, Meta becomes an intermediary.

![Three places money changes hands](/agentpay-roles-en.svg)

_All three can sit inside one company, but they are different money._

A transaction fee and a processing fee are different money too. Nobody calls a travel platform a payments company because it charges a booking commission. For now, Muse is aiming at the former.

It is still not a small change.

Advertising was paid for influencing what people buy. If the agent goes as far as buying, the platform can charge for what actually sold. The power to shape a purchase grows into the power to finish one.

Something comes with it, though.

If the payment fails, if the item never arrives, if it bought the wrong thing, the user blames the agent. Stripe may move the money, but the agent is the one judged on whether the job got done.

## 2. AI companies that walked up to the till

Other AI companies have walked toward payments as well, by different routes.

OpenAI launched the Agentic Commerce Protocol (ACP) with Stripe in September 2025, along with Instant Checkout for buying inside ChatGPT. In March 2026 it changed course. The first version had not offered the flexibility it wanted, it said, so merchants could use their own checkout while OpenAI concentrated on product discovery.

Google went after standards. It announced the Agent Payments Protocol (AP2) in September 2025 and the Universal Commerce Protocol (UCP) in January 2026. UCP was built with Shopify, Etsy, Wayfair, Target and Walmart, and plugs into checkout in Search's AI Mode and in Gemini.

Perplexity launched Instant Buy with PayPal in November 2025. PayPal handles identity checks, payment, and buyer and seller protection.

Anthropic released an open blueprint called Claude Commerce Agents on 2 September. It pairs a shopping agent that finds products and fills a basket with a merchant agent that handles inventory, pricing and marketing. Both live inside the merchant's own site, app and back office. According to PYMNTS, the blueprint includes no payment protocol, no product catalogue and no advertising layer.

The till and the customer relationship stay with the merchant.

Of all these, OpenAI's retreat tells you the most, I think.

A checkout is not just a button. Behind it sit loyalty tiers, coupons and points. Stock, delivery, returns and customer data are all wired into it too.

Hand over the till and a merchant hands over the lot.

Think of food delivery apps. The moment the app takes the order, the customer's contact details, the reviews and the repeat orders flow to the app. Restaurant owners are touchy about those apps for exactly that reason.

So the roads split in two. One side wants users and transactions inside its own entrance: Meta, and OpenAI at first. The other wants to turn the merchant's own entrance into AI, which is where Anthropic is now.

Either way, the actual processing goes to firms like Stripe or PayPal.

## 3. Payment firms and clouds come from the other side

Payment firms are not sitting still. They look closer to taking over an AI company's money problems wholesale.

Stripe closed its acquisition of Metronome, a usage-based billing company, on 14 January 2026, for about $1 billion according to reports. Metronome has handled billing for AI companies such as OpenAI and Anthropic.

On 19 August Stripe agreed to buy OpenRouter, a gateway that routes requests across more than 400 models. The price was not disclosed; reports put it above $7 billion.

To me it looks like a grip on both sides of an AI company's income statement. Metronome sits on the money coming in, turning usage into bills. OpenRouter sits on the money going out, the model spend.

There is merchant-side plumbing too. In December 2025 Stripe launched the Agentic Commerce Suite, which lets a merchant sell through many AI agents with one integration. When an agent passes a buyer's payment method to the merchant, it uses a Shared Payment Token.

Muse's one-time cards come from the same idea. Let the agent spend, but never show it the real card.

The card networks laid similar track. Mastercard announced Agent Pay in April 2025: agents register first, then pay with agent-specific tokens. Visa announced Intelligent Commerce the same month, with Anthropic and OpenAI on its partner list.

On the cloud side, a road is opening for software to pay software directly.

Coinbase's x402 wakes up "402 Payment Required", a response code that sat dormant in the web standard for decades. When a paid API answers 402, the agent pays in stablecoins on the spot and repeats the request.

AWS made Bedrock AgentCore payments generally available on 18 August. Agents pay for paid APIs, MCP servers and content from Coinbase or Stripe Privy wallets. Each payment session carries a maximum spend and an expiry time.

An agent cannot sign up and take out a monthly subscription to run one data query. It needs to pay as it goes, and the clouds are building that into the place agents run.

## 4. Four kinds of money on one transaction

When the three roads meet on a single transaction, the money splits several ways. Say Muse books a hotel for the user.

There is a fee for choosing the hotel. That is the transaction fee Zuckerberg talked about, and it goes to the agent's side.

There is a fee for moving the money from the card to the hotel's account. That is processing, split between the card networks and the processors.

There is the cost of the models and APIs the agent used along the way. A billing tool that turns usage into invoices sits here. Metronome's seat.

And there is the cost of the cloud the agent ran in, the wallet and the limit management. Execution infrastructure.

![Four kinds of money on one transaction](/agentpay-four-revenues-en.svg)

_Not every transaction carries all four, and each may go to a different company._

The four go to different hands, but the liabilities attached to them differ even more.

Anyone who has worked near payments will notice one thing.

The processing fee is thin, a few per cent of the amount, split between networks and processors. The liability is thick. Fraud, chargebacks, refunds and settlement errors all land here.

The margin is a few per cent; a single fraud loss is the whole amount.

Payment processing is closer to a business of managing risk.

Seen that way, it makes sense that AI companies leave the till to processors and reach for the transaction fee. OpenAI stepping back from checkout and Anthropic shipping a blueprint without payments look like the same call to me.

So "AI companies become payments companies" strikes me as half right. They cut into the flow of money. Very few of them want the liability of processing it.

## 5. Whose side is a fee-earning agent on?

The transaction fee brings a different problem.

Two hotels fit the brief almost equally. One is noticeably cheaper per night. The other pays the platform a bigger fee. Which does the agent book?

Finance has lived with this for a long time.

In US equities, brokers route customer orders to particular market makers and get paid for it, a practice called payment for order flow (PFOF). It is often cited as what made commission-free trading apps possible, and whether customers really got the best price has been questioned all along. So US rules make brokers disclose where they routed orders and what they were paid. Korea's Capital Markets Act carries a best-execution duty too: handle a client's order on the most favourable terms.

Agent shopping has the same shape. The question becomes whether a merchant's fee affected the ranking, and if it did, whether the user was told.

That is why Meta's remark about fees coming from merchants catches my eye. As far as I could find, nothing has been published on how Muse factors fees into what it recommends.

A user hands payment to an agent because they believe it chooses on their side. Break that belief and the permissions get pulled back fast.

So a permission screen that ends at an "approve payment" button is not enough. It has to show how much the agent can spend, what it can decide on the user's behalf and whether money is mixed into the recommendations. And who to complain to when it buys the wrong thing.

## 6. The question at approval changes

As someone who has taught and written about fraud detection, I find this part the most interesting.

When a person pays, fraud detection asks one thing: is this the cardholder paying right now? So it looks at the device, the location and the usual spending habits. I went through that structure in the [Stripe Radar post](/en/fds-stripe-radar/).

With agent payments, the payer is not a person to begin with. The device is in a cloud. The payment pattern does not look human.

So the question moves from "is this the owner?" to "is this inside the mandate?"

Google's AP2 records this as signed documents. An Intent Mandate holds the user's request. A Cart Mandate is the merchant-signed basket that the user co-signs. And a Payment Mandate goes to the card network.

The Payment Mandate carries a flag for whether a human was present at the moment of payment, and the issuer's risk engine reads it.

![When a person pays and when an agent pays](/agentpay-risk-en.svg)

_The approval question, the evidence in a dispute and the ways to limit damage all change._

Disputes change too. Card disputes usually split two ways: a payment I did not make, which is fraud, and a purchase that is not what I paid for, which is a merchant dispute. If an agent bought the wrong thing, which is it? I asked for it, but it bought wrong.

The evidence that settles that grey zone is the mandate record.

Limiting damage follows the same thinking. Muse's one-time card ends with one transaction. AWS's payment sessions carry a spending cap and an expiry. The design assumes the agent can be wrong and keeps the damage inside one transaction and one limit when it is.

Model builders get new work as well. The features in a fraud model will change. In place of device fingerprints and typing speed come agent identity, payment size against the mandate limit and whether a human confirmed. Labels change too. "The agent bought the wrong thing" may well end up as a new class that is neither fraud nor normal.

## 7. A personal view

Asked whether AI companies will become payments companies, I think the dividing line is less the label than who cleans up a failed transaction.

Getting into the flow of money has become easy. The protocols, tokens and wallets are all out there. The hard part comes after: getting a wrongly bought item back, refunding money taken twice, explaining why that hotel was chosen.

That is the work payment firms have done for decades.

So the number I will watch is the dispute rate, more than volume. Are refund and dispute rates on agent-made orders higher or lower than on orders people place themselves? Once they come in lower, people will hand over bigger payments, and that is when the transaction fee becomes a real business.

I am curious about Korea too. Simple-payment wallets such as Kakao Pay, Naver Pay and Toss already sit deep inside apps there. Whoever first offers one-time tokens and mandate limits for agents seems likely to take the seat Link holds in this story.

One day Muse will book the wrong hotel. Whether that complaint lands with Meta, Stripe or the hotel, the announcements so far do not yet say.

---

**Related posts:**

- [The Age of AI Paying: Alipay's AI付, AI收 and the Start of the Agent Economy](/en/alipay-ai-payment-era/)
- [\[FDS\] How Does Stripe Judge Payment Fraud in 100ms?](/en/fds-stripe-radar/)
- [Ah Bao Arrives: Alipay's Turn Toward an AI-Native Super App for a Billion Users](/en/alipay-ah-bao/)

## References

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

_Written as of 1 October 2026 from public reporting and company announcements. Acquisition prices are as reported, not figures the companies disclosed. As far as I could find, Muse's fee rate and how it ranks recommendations have not been published. The payment-for-order-flow comparison is there to explain the structure; it does not mean the same rules apply to agentic commerce._
