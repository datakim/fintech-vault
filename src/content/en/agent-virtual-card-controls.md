---
title: "Why a Single-Use Card Gets Charged Twice: The Gaps in Expressing an AI Agent's Authority as a Virtual Card"
description: "Ramp, Corpay, Stripe and Sunrate are all shipping virtual cards for AI agents. Putting limits, merchant categories and expiry on a card bounds the damage when a model is fooled, but issuer documentation shows these controls only act at authorisation and never reach the capture, where the money actually moves. Using hotel supplier payments as the example, this post traces where the gaps open and how to reconcile around them."
pubDatetime: 2026-11-09T19:30:00Z
koSlug: agent-virtual-card-controls
tags:
  - agentic-commerce
  - payments
  - ai-agent
  - fintech
---

Stripe's card-issuing documentation includes an example in which a card created for one use is charged twice. A 15 USD authorisation is approved and the card is cancelled, as its rules require. The merchant then sends a 5 USD capture with no authorisation, and that money leaves the account too. The documentation explains that under network rules such force posts must be processed, and suggests filing a dispute if needed. ([Stripe](https://docs.stripe.com/issuing/controls/lifecycle-controls))

Normally you would file that under rare exceptions. This year, though, more and more companies have picked exactly this kind of virtual card as the way to let AI agents pay, so it is worth working out how large the exception can get.

## 1. Several agent cards arrived in one year

On 2 November, at Hong Kong FinTech Week, the cross-border payments company Sunrate announced its Agentic Card. It is a multi-currency virtual commercial card that authorised AI agents can use to create payment instruments, initiate payments and retrieve the results. Limits can be set by amount, merchant category, currency, geography and validity period, and the card expires automatically once its task is done. It has also completed Mastercard Agent Pay certification. The example given was an online travel agency issuing a separate card for each supplier payment or marketing campaign. ([press release via PR Newswire](https://finance.yahoo.com/technology/ai/articles/sunrate-launches-agentic-card-enable-090000037.html))

Similar products are already out.

| Company | Announced | Status | Published controls |
|---|---|---|---|
| Ramp | April 2026 | Early access, built on Visa Intelligent Commerce | Per-transaction limit, merchant lock |
| Corpay | 28 July 2026 | No launch date or regions given | Purpose-specific virtual card per approved transaction |
| Stripe | Developer docs published | By application; the token payment path is in private preview | Category, country, amount limits, single-use cards, real-time authorisation |
| Sunrate | 2 November 2026 | Mastercard Agent Pay certified | Amount, category, currency, geography, validity, expiry on task completion |

None of them has said how much volume these cards carry. Sunrate's release names no customers and no transaction figures either, so for now these are designs to be read rather than track records to be judged.

What the four have in common is that none of them invented a new payment instrument. They kept the virtual cards that businesses already use and changed who issues and spends them. Corpay's Chief AI Officer explains that virtual cards suit agentic payments because they can be issued with precise controls. ([Corpay](https://www.corpay.com/corporate-newsroom/20326/corpay-introduces-agent-card-capability-to-power-secure-agentic-commerce)) This post follows how far those controls actually reach.

## 2. What you gain by moving authority into card settings

Take the instruction "pay up to 300 USD for three nights at this hotel in Bangkok" and translate it into card settings, and more of it fits than you might expect. The amount becomes a per-transaction limit, "hotel" becomes the lodging merchant category code, the deadline becomes an expiry date, and some issuers let you tie the card to a single merchant.

The biggest advantage is that the control is enforced outside the language model. If the agent is tricked by instructions hidden in a web page and tries a different payment, the issuer's authorisation system does not read prompts and will decline anything outside the card's settings. You have to assume the model can be fooled. In a red-team study of Google's Agent Payments Protocol (AP2), a shopping agent built on Gemini 2.5 Flash had its product rankings manipulated and gave up sensitive information under simple prompt injection. It is a preprint on arXiv, so the results deserve some caution. ([arXiv](https://arxiv.org/abs/2601.22569))

Judgements that card settings cannot express can be added through real-time authorisation. With Stripe, every payment attempt sends the business an authorisation request containing the amount, the merchant name and category code, and whatever metadata was attached to the card at issuance (an agent ID or order number, for instance), and the business's server approves or declines it. The default window is two seconds; if no answer arrives in time, the card's default rules apply. ([Stripe](https://docs.stripe.com/issuing/agents))

This is far better than handing an agent the company card number. All of these controls, however, hang on a single moment: authorisation.

## 3. Authorisation can be blocked; capture cannot

A card payment happens in two steps. At the moment of purchase the merchant asks the issuer whether it may take this amount, which is the authorisation. Later the merchant actually claims the money, which is the capture. When you pay at a restaurant, the authorisation happens at the table, and the final amount including the tip arrives as a capture that night or the next day.

According to Stripe's documentation, spending controls, real-time authorisation decisions and the card's active status are used only to decide whether to approve an authorisation, and they do not apply to captures. Captures for approved authorisations always succeed. Captures normally arrive within 24 hours, but hotels, airlines and car rental companies may capture up to 31 days after authorisation. ([Stripe](https://docs.stripe.com/issuing/purchases/transactions))

The most common case is a capture larger than the authorisation. Restaurant tips make many of these legitimate, so they cannot be blocked, and if the amount is excessive the cardholder has to notice and dispute it. Force posts that arrive with no authorisation also cannot be blocked, because some are legitimate too, such as purchases on in-flight terminals with no connection. Cancelling a card only stops new authorisations, so captures of earlier authorisations and force posts still arrive after cancellation. The single-use card in the opening paragraph is exactly this case.

This is not peculiar to Stripe. Lithic, another issuing platform, also states that spend limits cannot block force posts, and gives the example of a card with 100 USD of limit remaining that receives a 90 USD authorisation and is then cleared for 110 USD. The 90 USD authorisation passes because it is within the limit, and the 110 USD clearing goes through regardless of it. ([Lithic](https://docs.lithic.com/docs/spend-limits))

![A timeline from card issuance through authorisation, capture and refund. Limits, category, country, card status and real-time decisions act only around issuance and authorisation; captures above the authorisation, without one, or after closure go through.](/agentcard-timeline-en.svg)

_Figure 1. Where card controls apply and where they do not. Based on Stripe and Lithic issuing documentation; details vary by issuer._

The limit arithmetic has its own slack. Stripe says spending aggregation is best-effort, and there may be a delay of up to 30 seconds between a payment and its aggregation. ([Stripe](https://docs.stripe.com/issuing/controls/spending-controls)) For one person using one card that gap rarely matters. If several agents under the same envelope fire payments within a few seconds of each other, though, I would expect authorisations beyond the limit to slip through before aggregation catches up.

When people use company cards, the statement covered these gaps. If a strange capture appeared, the person who made the purchase noticed and disputed it. When agents create and discard hundreds of cards a day, nobody reads that statement.

## 4. A category code cannot tell one hotel from another

A merchant category code is the business classification assigned when a merchant registers to accept cards. Booking.com tells hotels that only merchants registered as accommodation providers can charge its virtual cards, and that others will see an "Invalid merchant" error. ([Booking.com](https://partner.booking.com/en-us/help/commission-invoices-tax/payment-products/getting-paid-virtual-credit-cards-vccs-when-using)) Restricting a card to the lodging category reliably blocks payments to anything that is not a hotel, but any hotel registered as lodging gets through.

Most of the mistakes an agent is likely to make happen inside that boundary. Booking a different hotel with a similar name, getting the dates wrong by a day, or paying again for a stay another system already paid for all pass the lodging category and the amount limit untouched.

The authorisation request shows why. Stripe's example request contains the amount, the merchant name, the category code, the city and country, and the metadata attached at issuance. It does not say which hotel or how many nights, what the cancellation terms are, or whether the same booking has already been paid. To check any of that, the business has to attach an order number as metadata and match each incoming request against its own order system. Merchant-level locks do exist, but at Stripe they are still in private preview, and Ramp has the agent pass the merchant's name and URL when it requests payment credentials. ([Stripe](https://docs.stripe.com/issuing/controls/spending-controls), [Ramp](https://agents.ramp.com/skills/ramp-agentic-purchase))

![What the issuer sees and does not see at authorisation. Amount, currency, merchant name, category code, country, metadata and the agent token are carried; the hotel and dates, cancellation terms, whether it was already paid and the person's original request are not. Verifiable Intent sends signed limits on merchant, items and amount.](/agentcard-visible-en.svg)

_Figure 2. What an authorisation request carries and what it leaves out._

The card networks know about this gap. On 5 March Mastercard published Verifiable Intent, developed with Google, a specification for sending a tamper-resistant record of what a person authorised along with the payment. ([Mastercard](https://www.mastercard.com/us/en/news-and-trends/stories/2026/verifiable-intent.html)) Its constraints document, draft v0.1 dated 18 February, defines eight constraint types: allowed merchants, allowed items and quantities, payees, amount range, total budget, two kinds of recurring payment, and a cross-reference between payment and checkout. The constraints are checked by the merchant or the payment network. ([Verifiable Intent](https://github.com/agent-intent/verifiable-intent/blob/main/spec/constraints.md))

By sending items and merchants in signed form, it fills much of the right-hand box in Figure 2. Checking the merchant constraint, however, requires checkout information signed by the merchant, and a hotel supplier that keys a card number into a POS terminal usually has no such thing. The total budget is also computed by adding up previously authorised amounts, so this mechanism for checking intent also sits at the authorisation step.

## 5. Hotels charge after the agent has moved on

The travel business that Sunrate chose as its first example was paying suppliers with virtual cards long before agents arrived. Booking.com shows how these cards are used on the hotel side. It loads the guest's payment onto a temporary Mastercard virtual card as the hotel's payout, and the hotel charges that card through its own POS. For non-refundable bookings the card can be charged from the booking date; for other bookings, from the point at which the reservation becomes at least 90% non-refundable. Properties that do not meet Booking.com's criteria, such as new ones, can charge it from the day after check-in. The card can be charged up to 12 months after check-out, and in several instalments until the balance reaches zero. ([Booking.com](https://partner.booking.com/en-us/help/commission-invoices-tax/payment-products/getting-paid-virtual-credit-cards-vccs-when-using))

This is where "the card expires when the task is done" runs into trouble. The agent's task ends when it books the room and hands over the card details, but the hotel charges the card after check-in, possibly months later. Expire the card when the booking is made and the hotel's legitimate charge is declined; keep it open until the stay is settled and the card lives for months. Whether the captures arriving in the meantime are correct is something the agent, long since busy with other work, cannot see.

Cancellations and refunds have the same problem. At Booking.com, when a booking that has already been charged is cancelled, the hotel must refund the same virtual card within 45 days, and it can refund a card that has expired. Stripe also accepts refunds on cancelled cards, but refunds are not always tied to the original authorisation, so a refund may be linked to the wrong authorisation or to none at all. ([Stripe](https://docs.stripe.com/issuing/purchases/transactions)) At Lithic, refunds do not restore a monthly limit: spend 900 USD, receive a 900 USD refund, and another 900 USD payment in the same month is declined for exceeding the limit. An agent rebooking after a cancellation may run straight into that decline. ([Lithic](https://docs.lithic.com/docs/spend-limits))

Duplicate payments need care too. Ramp's public checkout skill tells the agent that if a submission times out or the result is unclear, it must not infer that no charge occurred, and must reconcile that payment's status before requesting new credentials. ([Ramp](https://agents.ramp.com/skills/ramp-agentic-purchase)) Where a person would refresh the page, an agent is likely to retry.

What cannot be stopped at authorisation has to be caught after the capture arrives, and the tool for that is reconciliation. Group, per card, the amount a person approved for each task together with its authorisations, captures and refunds, and most of the gaps above become visible. Below is a skeleton in pandas. The data is made up for illustration.

```python
import pandas as pd

def reconcile(tasks, auths, txns):
    """Match tasks (amounts a person approved), authorisations and captures per card."""
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
        "capture>auth": m.captured > m.authorized,
        "capture without auth": m.no_auth > 0,
        "capture after task closed": m.late > 0,
        "net spend>task amount": m.net > m.task_amount,
    }
    m["flags"] = [", ".join(k for k, v in checks.items() if v[i]) for i in m.index]
    return m[["task_amount", "authorized", "captured", "refunded", "net", "flags"]]
```

Four hypothetical cards produce the following. Every task was closed on 3 November.

| Card | Task amount | Authorised | Captured | Refunded | Net | Flags |
|---|---|---|---|---|---|---|
| c1 | 300 | 300 | 300 | 0 | 300 | |
| c2 | 300 | 280 | 330 | 0 | 330 | capture>auth, net spend>task amount |
| c3 | 120 | 120 | 160 | 0 | 160 | capture>auth, capture without auth, capture after task closed, net spend>task amount |
| c4 | 200 | 200 | 200 | 200 | 0 | |

c2 was authorised for 280 USD and captured for 330 USD. c3 is a single-use card that received a 40 USD force post on 9 November, after it had been cancelled. c4 was cancelled and fully refunded, so its net spend is zero. A production version would add currency conversion, partial captures, matching refunds to original transactions and dispute deadlines, but even this much shows how it surfaces what the card settings alone cannot.

## 6. When the agent also creates the card

Sunrate's release says authorised agents create and manage payment instruments themselves. Stripe likewise lets an agent create cards and cardholders through Stripe MCP if the account has that access. ([Stripe](https://docs.stripe.com/issuing/agents)) It is convenient, but if the agent also sets the limits on the card it will use, the "control outside the model" from section 2 weakens. When one agent holds both the right to pay and the right to configure cards, an attacker who can redirect its payments through prompt injection can change the card settings as well.

Limits therefore need layers. The outermost is the envelope that people set and the agent cannot change: the monthly budget, the allowed categories, and the amount above which a person must confirm. Inside it sits the card the agent creates for each task, and innermost is the payment credential that actually ends up in the agent's hands. At Stripe, a cardholder's spending limits apply across all of that cardholder's cards and the most restrictive overlapping limit wins, and a token payment must satisfy both the card's limits and those of the shared payment token (SPT), which is bound to a seller, an amount and an expiry. At Ramp, agents can obtain single-use credentials only within funds an administrator has opened to them. ([Stripe](https://docs.stripe.com/issuing/agents/programmatic-checkout), [Ramp](https://agents.ramp.com/skills/ramp-agentic-purchase))

![Three nested layers showing who sets which limit. The outer layer is the envelope set by people, inside it is the per-task card the agent creates, and innermost is the payment credential, a single-use card number or token.](/agentcard-layers-en.svg)

_Figure 3. Splitting limits into three layers. The agent should only be able to touch the inner two._

At the innermost layer, exposure of the card number becomes the issue. If the seller supports a programmatic flow such as Stripe's MPP or UCP, the agent can pass a token instead of a card number, but on an ordinary web checkout the agent has to retrieve the virtual card's number and type it in. Stripe's documentation recommends a single-use card in that case, and Ramp's checkout skill tells the agent to submit the returned card details through the browser straight away. One of the attacks in the red-team study above extracted sensitive information from the agent, so it is safer to assume that a card number can leak from the moment it enters the model's context. A single-use card limits the damage to one payment, though as section 3 showed, even that one payment can still attract a force post.

## 7. My view

I think starting agent payments with virtual cards is the right choice. The amount you can lose is fixed regardless of how clever the model is, and corporate finance teams already know the tool, which keeps the barrier to adoption low. It is incomparably better than giving an agent the company card number.

What card settings express, though, is "how much, in which category, until when", and they check it only at authorisation. Whether the agent's job was done properly, meaning it paid the right hotel for the right dates exactly once, has to be checked outside the card. So I think the real control over agent payments lies less in the limits on the issuing screen than in the reconciliation of section 5. If nobody reads the statement, reconciliation has to be automatic too, and any capture that differs from its authorisation, or any money leaving a card whose task is closed, should go straight to a person.

There is work for issuer fraud detection as well. Issuer models mostly score at the moment of authorisation, but with agent cards the risk grows between authorisation and capture. Models that compare authorisation and capture per task, and rules that look separately at captures arriving on cancelled cards, are likely to be needed.

If you are evaluating one of these products, measure the human time spent per correctly completed payment and the dispute rate, rather than whether a payment succeeds in a demo. Sunrate's travel example can be judged the same way: the first real test of the design will be what state the card is in on the day, months after check-out, when the hotel finally charges it.

**Related posts:**

- [Will AI Companies Become Payments Companies? Who Makes Money When an Agent Buys](/en/ai-companies-payments/)
- [What Changes When AI Agents Pay? A Preview from China's Rules and Protocols](/en/china-agentic-payment-rules/)

## References

- [Sunrate Launches Agentic Card to Enable AI-Driven Business Payments (via PR Newswire, 2026-11-02)](https://finance.yahoo.com/technology/ai/articles/sunrate-launches-agentic-card-enable-090000037.html)
- [Corpay Introduces Agent Card Capability to Power Secure Agentic Commerce (Corpay, 2026-07-28)](https://www.corpay.com/corporate-newsroom/20326/corpay-introduces-agent-card-capability-to-power-secure-agentic-commerce)
- [Virtual cards for AI agents: How they work and what to look for (Ramp, 2026-04-28)](https://ramp.com/blog/virtual-cards-for-ai-agents)
- [Agent Card Checkout skill (Ramp)](https://agents.ramp.com/skills/ramp-agentic-purchase)
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

_This post is based on company announcements and public documentation as of 10 November 2026. The behaviour of authorisations and captures is drawn from Stripe and Lithic documentation; other issuers, including Sunrate, may behave differently. The transaction data in the code and table is made up for illustration._
