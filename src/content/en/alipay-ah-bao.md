---
title: "Ah Bao Arrives: Alipay's Turn Toward an AI-Native Super App for a Billion Users"
description: "On 16 June 2026 Alipay formally shipped a version carrying the AI assistant Ah Bao (阿宝). Swipe right on the home screen and the icon grid gives way to a conversational interface that calls more than ten thousand services by voice or plain language. The largest interface change in Alipay's twenty-year history, and the next round of its agent contest with WeChat."
pubDatetime: 2026-06-17T03:00:00Z
koSlug: alipay-ah-bao
tags:
  - financial-ai
  - ai-agent
  - alipay
  - fintech
  - super-app
  - agentic-commerce
---

## 1. 16 June 2026, the biggest change in twenty years

On 16 June 2026 Alipay officially released a new version carrying an AI agent interface. China Daily, Global Times and others characterised it as the largest change in Alipay's twenty-year history.

At the centre of the new version is the AI assistant **Ah Bao (阿宝)**. Swipe right from the Alipay home screen and the familiar icon menu and search bar give way to an extremely simplified conversational interface. Two tabs sit at the top: Assets (资产) and 阿宝. Select 阿宝 and an AI avatar asks "上午好, 有什么我可以帮你的吗?" — good morning, what can I help you with? At the bottom only a minimal set of core buttons remains: scan (扫一扫), pay/receive (收付款), transit (出行), wealth (理财).

![The 阿宝 interface in the AI version of Alipay](/ahbao1.png)

_Two tabs at the top, a conversation window in the middle, four core buttons at the bottom — an interface stripped to the bone. (Source: Alipay)_

The version is currently invitation-only, with a gradual expansion to all users planned.

## 2. What Ah Bao does: calling a service by speaking

The use cases Alipay published look like this.

| User request | What Ah Bao does |
| --- | --- |
| "帮我查下公积金" (check my housing fund) | navigates to the exact service entry point |
| "车快没电了，帮我找充电桩" (car is low, find a charger) | lists nearby chargers by location, with availability and price |
| "帮我叫辆车" (call me a car) | hails a ride and carries it through to payment |
| "帮我点杯咖啡" (order me a coffee) | places the order and pays via [AI付](/en/alipay-ai-payment-era/) |
| "帮我买基金" (buy me a fund) | executes the investment **after explicit user authorisation** |

The financial execution is the part worth attention. Ah Bao carries out fund purchases and investment account management only after the user's explicit authorisation. Alipay's design philosophy about the most sensitive point in an "AI spends money for you" structure shows through directly.

## 3. Why now: the agent war with WeChat

The timing is not accidental. On 8 June 2026 Tencent opened WeChat's AI ecosystem, announcing Meituan, Trip.com, Tongcheng and Didi as first partners. Say "帮我订去上海的高铁" (book me a high-speed train to Shanghai) in WeChat and the AI calls Trip.com and issues the ticket.

36kr read the situation this way.

> Alipay's internal test looks like an active interruption of the news rhythm around WeChat's AI. But whether or not the timing was calculated, the pressure WeChat brought is real — because what WeChat connected first were precisely the consumption scenarios Alipay depends on most.

Which makes Ah Bao closer to a defensive release than an offensive one. Having completed one round of payment infrastructure — AI付 at 300 million transactions, AI收, Token Pay, AI Wallet (detail in [the post on Alipay's AI payments](/en/alipay-ai-payment-era/)) — Alipay is now redesigning the **entry point** through which users reach that infrastructure. The other side of the same round, WeChat's conversation-first strategy, is covered in [WeChat's different road](/en/wechat-ai-strategy/).

## 4. "Project Bao": a year of preparation

Ah Bao did not appear from nowhere. According to 36kr and *STCN Daily*, the project formally started in December 2025 under the code name **宝计划** (Project Bao), with more than a year of preparation before that.

Alipay's move into AI has proceeded in stages.

| When | Event | What it meant |
| --- | --- | --- |
| March 2025 | core pivot: drop the standalone-app route, return to AI inside Alipay | strategic turn |
| September 2025 | "AI付" launches | AI-native payments begin |
| January 2026 | Qwen wired across the Alibaba ecosystem, Alipay as the payment node | group integration |
| February 2026 | AI付 passes 100 million users and 100 million transactions | critical scale |
| April 2026 | "AI收" launches, settlement for agent commerce connected | the receiving side completed |
| 26 May 2026 | AI付 cumulative 300 million; Token Pay and AI Wallet announced | full-stack payment infrastructure |
| 15 June 2026 | MiniMax M3 wired into Token Pay | MaaS payments commercialised |
| 16 June 2026 | AI version "阿宝" formally released | the whole platform turns AI-native |

![Alipay's AI evolution timeline](/ahbao2.jpg)

_Milestones from the 2004 founding to the 16 June 2026 launch of 阿宝. (Source: based on Alipay announcement material, via 雪球)_

The timeline shows one thing. Alipay completed the payment pipeline first and layered a product form on top of it. That is the exact opposite starting point from WeChat, which built the conversational infrastructure first and is now dissolving payments into it.

## 5. An agent open platform for developers, merchants and ISVs

Alongside Ah Bao, Alipay announced an agent open platform for developers, merchants and independent software vendors.

The core of the platform is making the AI payment infrastructure Alipay has already built — AI付, AI收, Token Pay, AI Wallet, Payment MCP Server, Payment Integration Skill, AI Tipping, AI Subscription Payment — easy for outside developers to wire into their own agents.

Ask in plain language for payments to be connected to an agent, for instance, and the Payment Integration Skill generates the API automatically. It dovetails with vibe coding — generating code from natural language.

That platform is what makes Ah Bao something other than an in-house assistant inside Alipay: a gateway through which many external agents can reach Alipay's billion users and its payment infrastructure.

## 6. The strategy in numbers

### 6.1 Scale

| Metric | Figure | Basis |
| --- | --- | --- |
| Alipay MAU | 890M+ | public material, 2024 |
| AI付 users | passed 100M | Lunar New Year 2026 (February) |
| AI付 cumulative payments | 300M | 26 May 2026 |
| Agent frameworks supported | roughly 95% | Alipay announcement |
| Services reachable via Ah Bao | 10,000+ | Alipay announcement |

### 6.2 The matchup: Alipay vs WeChat

| | Alipay (阿宝) | WeChat (AI agent) |
| --- | --- | --- |
| MAU | 890M+ | 1.418B (end of 2025) |
| Strength | finance, payments, wealth | social, mini programs, P2P |
| AI entry point | payment infrastructure → conversation | conversation infrastructure → payments |
| Financial execution | fund purchases, account management (post-authorisation) | not yet announced |
| Developer support | Token Pay, AI收, Payment MCP Server | WeChat AI ecosystem opened (8 June) |
| Core strategy | "infrastructure for AI to spend and receive money" | "the conversational space where AI lives" |

All figures come from Alipay and Tencent announcements or local reporting, and may not be independently verified industry statistics.

## 7. A personal view

The most interesting thing about the Ah Bao launch is that Alipay **abandoned its interface.** Twenty years of accumulated feature menus, icon grids and a search bar — the whole GUI tradition — folded at once in favour of conversation. It reads as a declaration that the era of people going to find services is over and the era of services coming to find people has begun.

The name itself carries meaning. 宝 is the 宝 of 支付宝 (Alipay), and 阿 is a familiar colloquial prefix. It is closer to an attempt to move away from the tool-like, transactional image Alipay has carried and reposition itself as a friendly companion.

There is an inherent tension in the move, though. Alipay's ground is finance. Payments, housing funds, social insurance, wealth management — its strength, and simultaneously the area most sensitive to AI automation. "AI orders a coffee" and "AI buys a fund" sit at completely different thresholds of user trust. Ah Bao tries to cross that threshold with the technical device of user authorisation, but the real test arrives when hundreds of millions of people use the feature at once.

And to survive the contest with WeChat, conversation alone will not be enough. WeChat has 1.418 billion MAU and an ecosystem of millions of mini programs. The one weapon Alipay holds is its "**depth in handling money**". That Ah Bao can execute fund purchases, credit limit adjustments, insurance enrolment and loan repayment is territory WeChat's agent has not yet shown.

Which makes it likely that this war is decided not by who builds the smarter AI but by who can manage a user's **money** for longer and more safely. Alipay has laid twenty-two years of financial data and risk control underneath Ah Bao. It is close to the only card that can face WeChat's social graph.

---

## Keywords

阿宝, Ah Bao, Alipay AI Agent, AI-native super app, Agent Open Platform, Payment MCP Server, AI付, AI收, Token Pay, AI Wallet, WeChat AI Agent, 宝计划

## References

- [Alipay launches AI version to reinvent China's super app — China Daily (2026-06-16)](https://www.chinadaily.com.cn/)
- [Alipay App launches major AI agent interface — Global Times (2026-06-16)](https://www.globaltimes.cn/)
- AI版支付宝"阿宝"来了，正式完成全端AI化 — 雪球 (2026-06-16)
- AI支付宝要来了，AI服务入口大战再次升级 — 36kr (2026-06-14)
- 支付宝内测AI版本"阿宝" 超级App迎来重构 — 新浪财经/科创板日报 (2026-06-14)
- AI版支付宝来了，她叫"阿宝"！ — 移动支付网 (2026-06-16)
- 支持95%通用智能体，支付宝全域布局AI支付 — 科学网 (2026-05-26)
- AI支付之战一点就燃：支付宝、微信双双亮剑 — 21世纪经济报道 (2026-06-16)

---

_Written as of 17 June 2026 from public reporting and company announcements. Some Ah Bao features are in invitation-only testing, and no schedule for a full rollout has been officially announced. Automatic AI execution of financial services such as fund purchases presupposes explicit user authorisation._

**Related posts:**

- [The Age of AI Paying: Alipay's AI付 and AI收](/en/alipay-ai-payment-era/)
- [WeChat's Different Road: A 1.4 Billion MAU Super App Absorbs the Agent](/en/wechat-ai-strategy/)
- [How Chinese Fintech Actually Works](/en/china-fintech-stack/)
