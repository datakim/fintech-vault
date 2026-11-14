---
title: "What the Risk Function Has to Change When AI Agents Run Bank Work"
description: "When an agent flags slightly fewer early warnings in one sector, case sampling and a weekly control chart both miss it, while on synthetic data a CUSUM monitor caught the shift in a median of six weeks. This post works through what a second line that can no longer approve decisions one by one should measure, and what it should record."
pubDatetime: 2026-11-14T06:15:00Z
koSlug: agent-bank-risk-function
tags:
  - financial-ai
  - ai-agent
  - machine-learning
---

Say a large bank hands first-pass monitoring of its mid-market loan book to an AI agent. Within three months the agent is watching tens of thousands of exposures and working through hundreds of reviews a day, analysing cash flows, updating probability of default (PD) estimates and flagging possible covenant breaches, work that used to be split across dozens of credit officers.

Now suppose that in one sector the agent gives a single early-warning indicator slightly less weight, consistently. Every individual call can be explained and every exception sits within tolerance, but repeated across thousands of cases the same tilt turns the whole sector into a meaningful risk position.

That scene opens BCG's September 2026 whitepaper, "When Agents Run the Bank".

The paper argues that most banks still assume review, challenge and escalation can happen at the pace people work, and that this assumption strains or breaks once agents produce decisions at volume. The second line (risk and compliance) therefore has to move from reviewing human decisions case by case to governing the whole system through which agents produce decisions. I agree with the direction, but the paper stops short of saying how each step should be measured, and that gap is worth filling from the data side.

## 1. Decisions that are right one by one and wrong in aggregate

I rebuilt the scene with synthetic data. In one sector the agent reviews 500 cases a week and raises an early warning on 6% of them. From week 13 its judgement shifts slightly and the flag rate drops to 4.8%, which means one in five warnings that should appear goes missing, about six a week.

Case sampling cannot see this. If people re-examine 1% of decisions, that is five cases a week, and the expected number of warnings among them is 0.30 before the shift and 0.24 after. However carefully the reviewer looks each week, there is no way to tell the two apart.

A control chart of the weekly flag rate does not help much either. At 500 cases a week and a 6% rate, the three-sigma limits run from 2.8% to 9.2%, so 4.8% sits comfortably inside. On the simulated path in the figure below, not a single week out of 26 crossed a limit.

![The upper panel shows the weekly early-warning flag rate in one sector, which stays between the control limits of 2.8% and 9.2% before and after week 13. The lower panel shows the CUSUM statistic, which stays below 1 until week 12, rises after week 13 and crosses the alarm line of 4 in week 18.](/agentbank-cusum-en.svg)

_One path generated from synthetic data. The weekly flag rate is on top and the CUSUM statistic below._

What caught the shift was a cumulative sum, or CUSUM. Each week it computes the log-likelihood ratio of that week's flag count coming from a 4.8% rate rather than a 6% rate, adds it to a running total, and resets the total to zero whenever it falls below zero. In a week with $x$ flags the increment is $x\ln(0.048/0.06) + (500-x)\ln(0.952/0.94)$, which comes to about $-0.73$ when the baseline 30 flags appear and about $+0.68$ when the shifted 24 appear. The total therefore hovers near zero in normal weeks and starts to build once a small shift persists for a few weeks. Page introduced the method for industrial process control in 1954, and it is strongest against exactly this kind of small, sustained change.

On this path the total crossed the alarm line of 4 in week 18, six weeks after the shift began. Repeating the same setup 4,000 times gave a median detection delay of six weeks, with 90% of shifts caught within eleven. With no shift, the total crossed the line by chance about once every 290 weeks on average. The warnings missed before detection on this path come to about 36 in expectation.

In practice you would not watch the flag rate alone. The share of cases handed to people, the mix of tool calls and drift in the average PD estimate can all be monitored the same way, by sector, region and borrower size. More segments mean more false alarms, though: monitoring 20 sectors separately produces an alarm somewhere about once every 15 weeks, so the threshold has to be set with the number of segments and the size of the investigation team in mind.

A CUSUM alarm only tells you that behaviour has moved away from its baseline. The sector may genuinely have improved and produced fewer warnings, so someone has to investigate when the alarm sounds, and that requires a record behind every decision (section 6). The baseline also has to be set before launch. If you build it while the agent is running, behaviour that has already drifted becomes the reference.

## 2. From model validation to system validation

The paper divides AI in banking into three horizons: predictive models such as credit scoring and fraud detection, the generative AI copilots that arrived after 2022, and an ecosystem of agents that carry work through to completion. The first horizon already has a model risk management framework, best known from the US Federal Reserve's SR 11-7 (2011), built around approving models, validating them independently and revalidating them periodically. In BCG's 2026 survey of about 30 leading international banks, 80% said they had an AI policy in place, yet one in five reported issues or incidents of AI in production producing biased or incorrect outputs.

In the third horizon the object of validation is no longer a single model. An agent's "model" is the combination of a foundation model, prompts, the tools it can call, the data it reads, the memory it accumulates, its permissions and its workflow, so the scope of what has to be pinned to a version widens too. The dated model ID, the prompts, the tool list and input schemas, the permission scope and the version of policy code it consults should be managed as one bundle, and a change to any of them should count as a new version whose baseline is checked again. In [the LLM judge post](/en/llm-judge-financial-chatbot/) I suggested versioning a judge in the same way, down to the prompt, the rubric and the model ID. A quarterly revalidation cycle built for the first horizon cannot keep up with that pace of change.

The paper names three failures banks are not yet measuring: drift, authorisation failure and adversarial manipulation. Drift is when, with no change to the model, an instruction to "flag suspicious transactions" slides over thousands of cases into "flag only obviously suspicious transactions", and the segment monitoring in section 1 is aimed at this. You can pair it with a fixed set of cases whose correct answers are known, rerun every month to see whether judgements have changed while the version stayed the same, because accumulating memory or a change in upstream data can shift behaviour too.

Authorisation failure comes from bank entitlement systems having been designed for people and applications. An agent running under an employee's account inherits permissions granted to a supervised human, and it can chain permitted steps into work nobody permitted. The audit log shows the employee's account but not which agent acted, on whose delegation, for what purpose. In anti-money laundering, transactions that each fall below the reporting threshold add up to structuring once you link them, and permissions likewise need checking against the chain of steps and its purpose rather than one step at a time. Giving agents their own credentials is the starting point, and as I found in [the post on virtual card controls](/en/agent-virtual-card-controls/), expressing authority narrowly by purpose and scope is harder than it looks.

Then there is adversarial manipulation. A borrower's financial statements in PDF or an email may hide instructions aimed at the agent, which then reaches a bad outcome through steps that are each permitted. The basic defences are to treat content read from documents as data rather than instructions, and to route every tool call through the orchestration engine's policy checks regardless of what the model has decided.

Some of the risk also reaches beyond any single bank. If banks use the same foundation models, the same cloud and the same tools, they may read the same market signals in the same direction. The Financial Stability Board's 2024 report lists concentration among AI service providers and rising market correlation among the financial stability risks of AI. When judgements ought to diverge and everyone moves the same way instead, no individual bank's control framework can prevent it.

## 3. The seven layers in three groups

The paper proposes a seven-layer risk architecture for an agentic bank, with first-line and second-line roles set out for each layer. Grouping layers of a similar kind into three makes the structure easier to follow.

![Risk architecture for an agentic bank. The facts group holds layer 1, the world model (business context data), and layer 2, risk services. The rules group holds layer 3, policy as code, and layer 4, the orchestration engine. The checks group holds layer 5, validation and monitoring, layer 6, human judgement, and layer 7, evidence and reporting. Below, the first line builds and runs agents and services and owns the outcomes, the second line sets standards and limits and challenges the system without approving cases one by one, and the third line tests whether controls work as designed.](/agentbank-layers-en.svg)

_This post regroups the seven layers of the BCG whitepaper into three._

Layer 1 in the facts group is what the paper calls the bank's world model, meaning its business context data. It is a governed knowledge graph on top of the data platform that links this customer to this counterparty, this covenant and this control status, and building it means making machine-readable the knowledge that today lives in rulebooks, procedures and employees' heads. Layer 2, risk services, turns functions such as sanctions screening, credit risk assessment and transaction monitoring into APIs. Today sanctions screening is a button inside a case management screen and the real control lies in the procedures around that button, whereas as a service it becomes a single controlled object with validated thresholds, permitted uses, an owner, a version history and evidence.

In the rules group, layer 3 is policy as code, turning risk limits and regulatory obligations into machine-readable rules, and layer 4 is the orchestration engine that composes services into decisions. The paper recommends handling cases that fit a known schema with rule-based logic and keeping model reasoning for exceptions where the system cannot proceed safely. It also stresses that agents built separately by business units have to go through this engine as well.

In the checks group, layer 5 sets behavioural baselines before launch and watches for drift in production, layer 6 is where named people exercise judgement at defined points, and layer 7 is the record proving how each decision was produced and authorised.

In this structure the first line builds and runs the agents and owns the outcomes. The second line does not approve individual AI systems or decisions. It sets the limits for policy code and the orchestration engine along with validation and evidence standards, and it challenges the architecture itself. Internal audit, the third line, does not redo decisions either. It tests whether the control architecture works as designed and produces evidence that can be examined independently.

## 4. What happens when policy becomes code

When policy lives in documents, errors spread through human interpretation. Each officer reads it slightly differently, so the damage is uneven. Once policy becomes code that changes. In the paper's words, a single miscoded threshold can distort every credit decision before review detects the pattern.

Here is the kind of mistake that is easy to make. A rule says "send to human review if PD exceeds 5%", and whoever codes it writes the number 5, while the data stores PD as a fraction such as 0.05. PD can never exceed 1, so not a single case trips the rule. No error message appears and decisions keep coming out normally, so something an officer would have found odd under the document regime slips through silently in code.

Policy code therefore needs testing with the same weight as model validation. Each policy gets tests with boundary cases such as PD 4.9%, 5.0% and 5.1% to confirm the rule splits them as intended. Before a changed policy is deployed, last month's decisions are rerun under the new policy code and the decisions whose outcome changes are counted by segment. If zero borrowers trip the PD rule, the problem shows up on the spot. When I suggested in [the Lift post](/en/risk-metrics-lift/) running a new rule in shadow mode first, this kind of accident was what I had in mind. What the second line approves also shifts, from the policy document to the code diff and the results of this impact analysis.

## 5. Keeping the human check from becoming a rubber stamp

The paper holds that human judgement should not sit above the system as an after-the-fact sign-off, but be designed in at defined points. Those points are when the orchestration engine decides a case calls for more ethical, reputational or risk appetite judgement than the bank is comfortable handing to a machine, and when layer 5 detects drift or an anomaly. Its example is a credit officer reviewing a $200 million exposure, who should not recalculate the risk but decide whether the context of that edge case changes how the risk appetite applies, and take accountability for that judgement. The paper notes that many serious AI control failures happen precisely at this interface between people and machines, where people trust the output too much, hesitate to challenge it, or approve it because they have nothing to challenge it with.

Automation bias has been studied for a long time. Reviewing the research in 2010, Parasuraman and Manzey concluded that errors from relying on automated decision aids, missing problems or following wrong advice, appear in experts as well as novices and are not prevented by training or instructions alone. The human check therefore has to be treated as something to validate and measure as well.

The first number to look at is the override rate, the share of the agent's calls that reviewers reverse, broken down by reviewer and by sector. If it has sat near 0% for months, it is fair to ask whether people are really exercising judgement. The distribution of review time belongs alongside it. If cases backed by dozens of pages of evidence are being approved in seconds, the check has become a formality.

A more direct approach is to seed the review queue with cases whose answers are known. Mixing in about 2% of past cases where the warning proved right, or synthetic cases with warning signs planted in them, puts roughly one a day in front of someone reviewing 50 cases a day. Measuring how often reviewers correct the agent on these cases tells you how sensitive the check is. It works like the gold questions used in data labelling quality control, and it should be clear from the start that the results measure whether the check works and are never used to appraise individual reviewers. The paper adds a point about screen design here, arguing that showing evidence, uncertainty, the policy applied and data provenance together is what lets reviewers challenge the agent without wearing out.

## 6. The record of a single decision, and who is accountable

The paper's layer 7 calls for recording, at the moment each decision is made rather than reconstructing it afterwards, which agent acted, on whose delegation, with which credentials and data, through which services, policy code and human checks, and with what result. Supervisors, it expects, will ask both whether individual decisions can be explained and whether the control environment itself is governed, tested, monitored and change-controlled.

![An example decision record. Decision: construction firm A, no early warning. Agent: credit monitoring agent v3.2. Delegation: on behalf of corporate lending, for early-warning calls only. Credential: the agent's own. Inputs: financial statements, arrears history and sector indicators as of 3 November. Services: credit scoring v5 and early-warning indicators v2. Policy code: warning rules v14. Human check: none. Result: no flag, with a warning score of 0.42 against a threshold of 0.50. On the right are four questions this record can answer.](/agentbank-record-en.svg)

_A hypothetical decision record. Records like this are what let you trace the cause when the CUSUM alarm in section 1 goes off._

With this record in place, an alarm like the one in section 1 comes with a clear first step. Pull the decisions from the weeks when construction-sector warnings started falling and compare policy code versions, agent versions and input data dates, and you can tell whether a policy change, agent drift or a change in the sector data is behind it. Rerunning a decision with the same inputs and versions to check that it reproduces also depends on this record.

Accountability is the harder problem. The paper's example is a prompt injection that manipulated customer risk assessments. Cybersecurity owns the technical incident, financial crime owns the effect on customer due diligence and compliance owns the regulatory impact, yet there may be nobody who owns the whole job of finding every affected decision, coordinating remediation, deciding whether onboarding continues and judging whether the remaining risk is acceptable.

For Korean banks it is worth connecting this to the responsibility map (책무구조도), a regime often compared to the UK's Senior Managers and Certification Regime. Introduced by a 2024 amendment to Korea's Act on Corporate Governance of Financial Companies and applied to banks and financial holding companies from January 2025, it requires each executive's internal control responsibilities to be set out in writing. Executives who breach their duty to manage the internal controls assigned to them, or a CEO who breaches the overall management duty, face personal sanctions. Since the framework already documents who is responsible for which controls, it gives agent responsibilities somewhere to live. A practical first step would be to name an accountable executive for each agent and to state who owns end-to-end coordination of agent incidents that cut across departments. Supervisors have not asked for this; it is my own attempt to carry the paper's concern into the current regime.

## 7. My take

The paper's subtitle is "The End of the Second Line as You Know It", but what I see ending is case-by-case approval, not the second line's independence. If anything, independence matters more. If the second line writes the standards and then checks results using the same orchestration engine and world model the first line built, a data error in the world model blinds both lines at once. The second line needs its own way of confirming results, with separately drawn samples and separate calculations.

Of the seven layers, the world model in layer 1 is likely to be the most expensive and slowest to build. In most banks the data linking customers, contracts, covenants, collateral and control status is still spread across separate systems, and the paper itself expects the transition to be gradual.

That is why I think decision records and segment-level CUSUM monitoring are the realistic place to start. Both can be built from existing data and standard statistical tools, and they catch scenes like the one in section 1 well before all seven layers are in place. If you set a baseline for how an agent's decisions should be distributed across sectors before you deploy it, a shift that starts in week 13 becomes visible by week 18.

---

**Related posts:**

- [What to Decide Before an LLM Grades a Financial Chatbot's Answers](/en/llm-judge-financial-chatbot/)
- [Why a Single-Use Card Gets Charged Twice: The Gaps in Expressing an AI Agent's Authority as a Virtual Card](/en/agent-virtual-card-controls/)
- [Why a Rule With Lift 2.4 on Its Own Fades Inside a Strategy: Four Ways to Measure Lift](/en/risk-metrics-lift/)

## References

- Matteo Coppola, Anne Kleppe, When Agents Run the Bank: The End of the Second Line as You Know It (BCG whitepaper, September 2026)
- [The Financial Stability Implications of Artificial Intelligence (FSB, November 2024)](https://www.fsb.org/uploads/P14112024.pdf)
- [SR 11-7: Guidance on Model Risk Management (Board of Governors of the Federal Reserve System, 2011)](https://www.federalreserve.gov/boarddocs/srletters/2011/sr1107.htm)
- [Continuous Inspection Schemes (Page, Biometrika, 1954)](https://doi.org/10.1093/biomet/41.1-2.100)
- [Complacency and Bias in Human Use of Automation: An Attentional Integration (Parasuraman & Manzey, Human Factors, 2010)](https://pubmed.ncbi.nlm.nih.gov/21077562/)
- [Responsibility map regime takes effect (Newsis, 3 January 2025, in Korean)](https://mobile.newsis.com/view/NISX20250103_0003019527)

_This post is based on the BCG whitepaper and public sources as of 14 November 2026. The flag rates and detection delays in section 1, the PD rule in section 4 and the decision record in section 6 are synthetic data and hypothetical cases built for illustration. The suggestion on the responsibility map is the author's opinion and not a supervisory requirement._
