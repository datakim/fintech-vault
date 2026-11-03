---
title: "What Changes When AI Agents Pay? A Preview from China's Rules and Protocols"
description: "Once AI agents pay on our behalf, who decides, what gets written into the user's agreement and who is liable when things go wrong all have to be settled anew. Reading China's 2026 ministry opinions, financial-regulator guidance and industry convention, and the protocols from UnionPay, JD, Alipay and Ant, clause by clause gives an early view of those changes."
pubDatetime: 2026-11-03T05:10:00Z
koSlug: china-agentic-payment-rules
tags:
  - payments
  - agentic-commerce
  - china
  - fintech
---

On 24 August 2026 the Payment & Clearing Association of China (PCAC) published its self-regulatory convention on agent payment applications (智能体支付应用自律公约). It runs to 8 chapters and 34 articles and sets out how member banks, payment institutions and clearing houses should run services in which an AI agent pays on a user's behalf. It took effect on the day it was published.

Around it, the government and industry put out a string of related documents. In May three ministries issued opinions on AI agents in general, and in June the National Financial Regulatory Administration (NFRA) issued guidance on AI in banking and insurance. Over the same months UnionPay, JD, Alipay and Ant International each released or expanded an agent payment protocol. Read one by one, the documents are a tangle, but laying the three supervisory documents and four company protocols side by side, clause by clause, gives a fairly consistent picture, and an early view of what changes once AI agents pay on our behalf. Who decides to pay, what is written into the agreement with the user, how the agent's identity is checked and who is liable when something goes wrong are all being settled anew.

## 1. The documents that arrived through 2026

![Timeline of China's agent payment documents and protocols from January to September 2026, in three layers: government and regulators, association and standards, companies](/cn-agentpay-timeline-en.svg)

_The 2026 timeline in three layers. Dates are each organisation's announcement date._

At the top sits the State Council's August 2025 opinion on implementing the "AI+" initiative (国发〔2025〕11号). It is the parent policy, with a target of lifting adoption of applications such as agents above 70% by 2027, and most of the 2026 documents cite it as their basis.

The government and regulator layer holds two documents. On 8 May the Cyberspace Administration of China, the National Development and Reform Commission and the Ministry of Industry and Information Technology jointly issued implementation opinions on the regulated use and innovative development of AI agents (智能体规范应用与创新发展实施意见). It is described as the first national policy framework devoted to agents, well beyond payments. On 18 June the NFRA issued its guidance on the safe development and use of AI in banking and insurance (金发〔2026〕8号), which covers how financial institutions handle AI internally.

The association and standards layer holds the PCAC convention of August and, from 22 May, the national guidance document GB/Z 185 on AI agent interconnection. It comes in seven parts: overall architecture, identity codes, identity management, agent description, discovery, interaction and tool invocation. A GB/Z document is guidance, not a mandatory standard.

The company layer starts with Alipay's ACT on 16 January, then UnionPay's APOP and Ant International's AMP in April, and JD's A2P2 and WeChat Pay's AI card in June. On 10 September Ant International, Visa and Mastercard announced that they had begun work on a Know Your Agent (KYA) interoperability framework.

## 2. Who decides: three decision modes in the opinions

Of the opinions' 38 items, the one that uses the word "payment" is item 4. Among the basic technologies for an agent internet it lists agent identity markers, trusted interconnection, compliant payment (合规支付), security protection and conflict resolution, which places agent payments inside the national plan for agent infrastructure. The same item asks for an agent registration platform to be explored: a registry that gives agents digital identities and supports discovery and capability declarations. It reads as a national-level sketch of what payments people call KYA. Item 22 also names online shopping and bill payment among the areas of use.

The item that bears most directly on how a payment service is designed is item 6, on setting the boundaries of decision authority. It asks for a line between decisions only the user may make, decisions an agent may make once the user has authorised it, and decisions an agent may make on its own. Even when an agent decides on its own, the user keeps the right to be informed and the final say, and the agent may not act beyond what the user authorised.

![The three decision modes from the ministry opinions, the three stages from the PCAC convention Q&A, and JD A2P2's levels, lined up by autonomy](/cn-agentpay-levels-en.svg)

_Lined up by the author at roughly matching levels. A2P2's L1 and L2 are left out because little is published about them._

The PCAC and JD split the same question of how much to hand over into stages too. In its Q&A on the convention (答记者问), the PCAC described three stages: agent-assisted payment, autonomous payment under preset conditions, and autonomous payment under general conditions (泛条件). JD's A2P2 uses six levels, L0 to L5, modelled on driving automation. The names differ, but each separates a stage where a person confirms every payment, a stage where the agent acts within set limits, and full autonomy.

## 3. Payments have their own rules: the PCAC convention

Among the convention's basic principles, the one with most practical weight is Article 5. Core payment functions such as account management, transaction processing and clearing and settlement must be carried out by licensed institutions, and under the principle that "whoever provides the payment service is responsible" (谁提供支付服务谁负责), members bear primary responsibility for account, transaction, fund and information security. However much of the conversation an agent developer handles up front, the part where money moves, and the liability for it, stays with the payment institution.

Article 2 defines an agent payment application as one in which, with the user's authorisation and according to the user's genuine intention, an agent interacts with digital services such as e-commerce to initiate and execute payment instructions. When reading the articles it helps to start with the verbs. Some say members "must" (应) and others say they should "explore" (探索). In Chinese policy documents 探索 usually means to pilot and work out an approach rather than a firm requirement, so the difference separates what is required now from where things are meant to go.

![PCAC convention articles split into two columns: those written as 'must' and those written as 'explore'](/cn-agentpay-pcac-en.svg)

_The convention's articles sorted by verb. Article 26 asks members to approach autonomous payment with care but makes reporting before launch mandatory._

Article 13 is the centre of the obligations. It requires members to set the scope of authorisation and sign an authorisation agreement with the user. The agreement must state key terms such as transaction limits, the debit account and its priority, and the validity period, along with the rights and duties around the agent acting, accessing data and calling APIs on the user's behalf.

Article 14 requires strict verification of the user's identity and intent to pay, and Article 15 requires members to block payments beyond the authorisation and protect the integrity, authenticity and traceability of transactions. The user's right to withdraw the authorisation is guaranteed by Article 16. Article 12 adds that members must use only agents registered or filed with the authorities, and must assess risk and run due diligence on outside agent developers as a matter of routine.

KYA sits on the explore side. Article 9 asks members to explore a KYA mechanism built on KYC: identifying and verifying agents that enter the payment chain, managing users under their real names, and setting out the link between agent and user by agreement. Article 10 asks members to explore sorting agents into high, medium and low risk by model source, identity marker, permission boundary, interface calls and behaviour, and Article 11 covers passing that information along the whole payment chain.

Article 18 likewise treats as something to explore an evidence chain for four processes, user authorisation, model decision, payment instruction and risk control, that is verifiable, traceable and tamper-proof.

Autonomous payment has its own article, Article 26. Services in which an agent initiates payments on its own are to be explored with care, but before launch they must be filed with the PCAC in advance (报备). According to the PCAC's Q&A, this covers the second and third of the three stages: autonomous payment under preset conditions and under general conditions. They also need assessments of business effectiveness, technical security and ethical compliance, plus five safeguards: a channel where people handle cases directly (人工服务), risk monitoring, monitoring of complaints and reputation (舆情监测), emergency response, and a mechanism to fall back to the previous way of working when something goes wrong (回退机制). What the convention requires today, then, is the agreement, verification of intent, staying within scope, the right to withdraw and filing before launch, while KYA and the evidence chain are a direction that has been set.

## 4. Banks and insurers take the high-risk route: NFRA guidance No. 8

A financial institution offering agent payments has to follow the NFRA guidance as well as the convention. Item 15 asks institutions to classify AI applications by five factors: importance of the business area, scale of use, impact on customers, reliance on the model and model complexity. Item 16 treats applications involving fund transactions, asset valuation, credit approval, underwriting and claims, and risk management as high risk. Generative AI applications directly tied to customer interests or the conclusion of financial contracts count as high risk too, and high-risk applications need approval from the institution's risk management committee before they go live. Item 17 calls for human oversight and intervention at key points, conditions for emergency shutdown and model retirement, and backup systems or manual fallback.

A service in which an agent executes payments involves fund transactions, so inside a bank it is likely to be classed as high risk from the outset. That means designing around committee approval and human intervention rather than running it like an ordinary IT project.

## 5. Companies turned the rules into products

While the supervisory documents set principles, the companies built the same principles into protocols.

UnionPay's Agentic Payment Open Protocol (APOP) was announced in Shanghai on 2 April. It has four capabilities: lifecycle management of agent identity, generation, registration and verification of intent, user identity management, and payment authorisation. What stands out is that it treats what the user wants to buy (purchase intent), not just the amount paid, as something to verify in its own right. On the same day it ran a test transaction in Hong Kong in which an AI assistant chose and paid for a taxi.

JD's A2P2 (11 June) splits delegation into six levels, from L0, where a person confirms every payment, to L5, full autonomy. At L3 the agent initiates payments on its own within one task, and the system decides whether to approve them within limits the user set. At L4 the agent completes payments itself when the amount, use case and user all fall within preset ranges. There are four building blocks. ARI (agent runtime identity) binds the real user, the agent's identity and its runtime environment together at the moment of payment, and a Mandate turns a natural-language instruction into an authorisation the machine can verify. Add to that a dedicated account with limits, kept apart from the main account, and an evidence chain that links each payment to its mandate, identity, decision and execution token. An attempt to pay 300 yuan under a 200-yuan instruction is rejected or sent back to the user to confirm.

Alipay's Agentic Commerce Trust Protocol (ACT, 16 January) is built around four domains: delegated authorisation, commercial interaction, payment services and trust services. It offers two modes, instant payment, where the user picks from suggestions in the chat, and delegated payment, where the user sets a time window, spending cap and merchant scope in advance. In May Alipay also launched an AI Wallet and Token Pay.

Ant International's Agentic Mobile Protocol (AMP) was open-sourced on 28 April and rolled out globally on 11 September. The first phase brought in 10 Alipay+ wallets serving 1.5 billion user accounts and 7 acquirers including Adyen, Checkout.com and Fiserv. It also includes a high-frequency agent-to-agent settlement mechanism for transactions as small as US$0.000001.

WeChat Pay's AI card (17 June) is a product rather than a protocol, but it shows the same principles most simply. It sits inside the WeChat balance (零钱) yet is separated from the main WeChat Pay account, so an agent can spend only what is on the card. The user can move money in and out at any time, and every payment has to be confirmed on the phone before it goes through. At launch it worked only with WorkBuddy, Tencent's office agent.

| | Agent identity | Intent and mandate | Limits and isolation | Evidence |
|---|---|---|---|---|
| UnionPay APOP | identity lifecycle management | intent generation, registration, verification | payment authorisation | - |
| JD A2P2 | ARI | Mandate | L0 to L5, dedicated account | evidence chain |
| Alipay ACT | trust services domain | delegated authorisation domain | spending cap, merchant scope | traceable and verifiable (per announcement) |
| Ant AMP | KYA work begun with Visa and Mastercard | Mandate role (open-source docs) | - | - |
| WeChat AI card | - | confirmation on the phone for each payment | separate from main account, card balance only | - |

_"-" marks cells I could not confirm from public material. The WeChat card is a product, not a protocol, and is included only for comparison._

## 6. Compared with the West

In the US and Europe, protocols from payment companies and big tech came first. In 2025 came Mastercard's Agent Pay (April), Google's AP2 (September), Stripe and OpenAI's ACP (September) and Visa's TAP (October). In March 2026 Mastercard's Verifiable Intent and Stripe and Tempo's MPP followed. AP2 launched with more than 60 partners and records the user's intent and cart as signed mandates. OpenAI was reported in March 2026 to have scaled back paying inside ChatGPT (Instant Checkout) and handed checkout back to merchants.

On standards, EMVCo published a draft framework for agentic payments for comment in September 2026, and the FIDO Alliance set up working groups on agent authentication and payments in April.

Supervision has mostly stayed at the level of recommendations. In its September 2025 AI principles, the PCI SSC suggested treating an AI with payment authority as a "potential malicious insider" in threat analysis. It also recommended logging enough to audit the prompt inputs and the reasoning. An IMF note of April 2026 concluded that liability turns on whether the agent acted within its authority. In September six banks, ASB, Bank of America, Capital One, CBA, ING and NatWest, published a non-binding set of principles. In October came reports that Citi, Bank of America and JPMorgan were blocking or limiting outside agents' access to customer accounts.

| | China | US and Europe |
|---|---|---|
| Who moved first | government, association and platforms at about the same time | protocols from payment companies and big tech |
| Nature of supervisory documents | opinions and guidance, plus an association convention with some mandatory articles | mostly recommendations and non-binding principles |
| Main protocols | APOP, A2P2, ACT, AMP | AP2, ACP, TAP, Agent Pay and Verifiable Intent, MPP |
| Standards | national guidance document GB/Z 185 | EMVCo draft, FIDO and IETF work |

Whoever writes the rules, the content converges on four things: who the agent is (identity), what the user handed over (intent and mandate records), how far it may go (limits and isolation), and what proves it afterwards (evidence). UnionPay managing intent separately, Mastercard releasing Verifiable Intent and Article 18 of the convention asking for an evidence chain covering authorisation and model decisions are all ways of dealing with the same problem.

## 7. My view

From a data point of view, what stands out most is that intent becomes something that is recorded. Until now payment data has held what was bought and how much was paid. With mandates, it also holds what the user asked for, what the cap was and which merchants were allowed. For fraud detection that adds a new baseline. The first step will be rules that block payments beyond the instruction, as JD's A2P2 does. After that, I think it likely that how far a payment strays from its instruction, and whether the merchants an agent picks for the same instruction differ from usual, will be used as model inputs.

The second thing to watch is the word "explore". That KYA and the evidence chain are still things to explore in the convention suggests that the technology and the industry consensus are not there yet. Whether these articles turn into "must" once the identity parts of GB/Z 185 and the KYA work Ant, Visa and Mastercard began in September settle down remains to be seen.

On the product side, WeChat's AI card makes an interesting choice. Asking for confirmation on every payment looks like a step backwards for convenience, but by fencing spendable money into a separate balance and showing each payment, it lets users always see what they have handed over. Article 26 of the convention requiring a fallback mechanism for autonomous payment, and A2P2 slicing delegation into fine levels with its weight on L3 and L4, point the same way. Given that WeChat opened the card to only one agent, WorkBuddy, at first, delegation within limits rather than full autonomy looks set to be the centre of agent payments in China for now.

---

**Related posts:**

- [The Age of AI Paying: Alipay's AI付, AI收 and the Start of the Agent Economy](/en/alipay-ai-payment-era/)
- [Will AI Companies Become Payments Companies? Who Makes Money When an Agent Buys](/en/ai-companies-payments/)
- [WeChat's Different Road: A 1.4 Billion MAU Super App Absorbs the Agent](/en/wechat-ai-strategy/)

## References

- [Payment & Clearing Association of China, Notice on issuing the self-regulatory convention on agent payment applications (中支协发〔2026〕128号), 24 Aug 2026 (in Chinese)](https://www.pcac.org.cn/eportal/ui?pageId=598041&articleKey=627014&columnId=595027)
- [Cyberspace Administration of China, Implementation opinions on the regulated use and innovative development of AI agents, 8 May 2026 (in Chinese)](https://www.cac.gov.cn/2026-05/08/c_1779979789523320.htm)
- [NFRA, Guidance on the safe development and use of AI in banking and insurance (金发〔2026〕8号), 18 Jun 2026 (in Chinese)](https://www.nfra.gov.cn/cn/view/pages/ItemDetail.html?docId=1261784&itemId=861&generaltype=1)
- [State Council, Opinions on deepening the "AI+" initiative (国发〔2025〕11号), 26 Aug 2025 (in Chinese)](https://www.gov.cn/zhengce/content/202508/content_7037861.htm) · [unofficial English translation (CSET)](https://cset.georgetown.edu/publication/china-ai-plus-opinions-2025/)
- [Science and Technology Daily, GB/Z 185 AI agent interconnection standards, 9 Jun 2026 (in Chinese)](https://www.stdaily.com/web/gdxw/2026-06/09/content_529630.html)
- [UnionPay International, UnionPay Launches Agentic Payment Open Protocol Framework (PR Newswire), 3 Apr 2026](https://www.prnewswire.com/apac/news-releases/unionpay-launches-agentic-payment-open-protocol-framework-building-an-open-trusted-smart-payment-ecosystem-302733540.html)
- [IT之家, JD releases agent autonomous payment protocol A2P2, 11 Jun 2026 (in Chinese)](https://www.ithome.com/0/963/090.htm)
- [Yangtse Evening Post, Alipay releases the ACT protocol, 16 Jan 2026 (in Chinese)](https://www.yzwb.net/news/ch/202601/t20260116_311925.html)
- [Ant International, Agentic Mobile Protocol Rolls Out Globally with Wallets and Acquirers, 11 Sep 2026](https://www.ant-intl.com/en/news/detail/?id=ant-internationals-agentic-mobile-protocol-rolls-out-globally-with-wallets-and-acquirers-initiating-collaboration-on-kya-interoperability-framework-with-mastercard-and-visa)
- [Ant International, Ant International, Mastercard and Visa Initiate Collaboration on Know-Your-Agent Interoperability, 10 Sep 2026](https://www.ant-intl.com/en/news/detail/?id=ant-international-mastercard-and-visa-initiate-collaboration-on-know-your-agent-interoperability-to-scale-agentic-commerce)
- [Caixin Global, Tencent lets AI agent make purchases through WeChat Pay, 17 Jun 2026](https://www.caixinglobal.com/2026-06-17/tencent-lets-ai-agent-make-purchases-through-wechat-pay-102455141.html)
- [Caixin Global, China pioneers know-your-agent rules for AI payments, 25 Aug 2026](https://www.caixinglobal.com/2026-08-25/china-pioneers-know-your-agent-rules-for-ai-payments-102477712.html)
- [Google Cloud, Powering AI commerce with the new Agent Payments Protocol (AP2), 16 Sep 2025](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol)
- [Mastercard, When AI starts buying for you, trust becomes the product (Verifiable Intent), 5 Mar 2026](https://www.mastercard.com/us/en/news-and-trends/stories/2026/verifiable-intent.html)
- [Visa, Visa Introduces Trusted Agent Protocol, 14 Oct 2025](https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21716.html)
- [EMVCo, EMV Agentic Payments Framework for Specifications v1.0 draft, Sep 2026](https://www.emvco.com/resources/emv-agentic-payments-framework-for-specifications-v1-0-draft-comment-period-ends-30-sept-2026/)
- [PCI SSC, AI Principles: Securing the Use of AI in Payment Environments, 11 Sep 2025](https://blog.pcisecuritystandards.org/ai-principles-securing-the-use-of-ai-in-payment-environments)
- [IMF, How Agentic AI Will Reshape Payments (Note 2026/004), Apr 2026](https://www.imf.org/-/media/files/publications/imf-notes/2026/english/insea2026004.pdf)
- [Commonwealth Bank, Global banks collaborate on principles for trusted agentic commerce, 23 Sep 2026](https://www.commbank.com.au/articles/newsroom/2026/09/agentic-commerce-principles-paper-launch.html)
- [The Paypers, Citi and Bank of America restrict AI agents from accessing accounts, 19 Oct 2026](https://thepaypers.com/fintech/news/citi-and-bank-of-america-restrict-ai-agents-from-accessing-accounts)

_This post is based on each organisation's original documents, official announcements and press reports as of 3 November 2026. Names of Chinese documents and the wording of articles are my own translations, so check the originals for exact language._
