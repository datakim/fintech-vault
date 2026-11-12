---
title: "What to Check Before Moving a Classifier From an LLM to a Decision Model: Amazon's Ticket Labelling Case"
description: "An Amazon team replaced Claude Sonnet 4.6 with the decision model Strands Decider for internal ticket labelling, and model cost per million tickets fell from about 22,200 USD to 500 USD. Measured against today's price lists, the gap narrows to the same order of magnitude, and what remains is probabilities, speed and in-house hosting. Also covers the coverage and accuracy figures the write-up leaves out, auditing in DUAL mode, and input formatting that moves the probabilities."
pubDatetime: 2026-11-12T04:45:00Z
koSlug: strands-decider-ticket-labeling
tags:
  - financial-ai
  - llm
  - ai-agent
  - machine-learning
---

An Amazon team has replaced the model that sorted internal tickets into 20 categories, moving from Claude Sonnet 4.6 to a small decision model built on Gemma 4 E4B. The system collects tickets from across the company, from customer escalations and capacity requests to automated alarms and security findings. After the switch, average time per call fell from 4,215 ms to 897 ms, and model cost per million tickets went from about 22,200 USD to about 500 USD.

Two engineers who run the system described the change on the Strands Agents blog on 9 November. ([Strands Agents](https://strandsagents.com/blog/amazon-saves-millions-replacing-sonnet-with-strands-decider/))

Strands Decider is the same kind of model as Jev, which I covered in [the previous post](/en/decision-model-calibration/). It does not generate text: it takes a state, a question and a set of options, and returns a probability for each option. The Jev post looked at what that probability guarantees, and this case shows what to measure, and what to keep on record, when a model like this goes into production.

## 1. Strands Decider, an open model built the way Jev is

Strands Labs, the experimental arm behind AWS's agent SDK Strands Agents, released Strands Decider in October 2026 under the Apache-2.0 licence. The reference model has 1.9 billion parameters: it takes Qwen3.5-2B-Base, removes the final layer that picks the next token (the LM head) and attaches a small pointer head. The head scores each option by comparing the hidden state at the `<answer>` position with the hidden state at that option's last token. One forward pass gives the probability of every option, so there is no loop generating text token by token. Because the head holds no per-option weights, the label set is not baked into the model and is passed with each request. Versions built on Gemma 4 (E2B, E4B, 12B and 26B-A4B) were released alongside, and E4B is the one the Amazon team used. ([GitHub](https://github.com/strands-labs/strands-decider))

The resemblance to Jev goes beyond the architecture. The question types are the same, noul (yes/no), choice and score, and the HTTP endpoint is also called `/v1/systemone`. Performance is reported on JevBench (231 tasks), the benchmark from the Jev side, and the repository lists E4B at 187 of 231 with a Brier score of 0.243. Confidence appears to be defined the same way as well. In a README example with three options, billing has probability 0.773 and confidence 0.659, and the formula from the Jev post gives exactly that: $(0.773 - 1/3) \div (1 - 1/3) \approx 0.659$.

The README says that on short classification tasks it has not seen, answers with a confidence of 0.9 or more are right about 95% of the time, and suggests checking or asking a person below that. The Jev post showed how far such a figure can move between tasks: in an independent evaluation, Jev's accuracy in the band at or above 0.9 ranged from 0.975 to 0.611 depending on the task. ([arXiv 2609.24574](https://arxiv.org/abs/2609.24574))

## 2. Measuring the 44x against today's price list

The Amazon team's arithmetic holds. Sonnet 4.6 used 6,554 input tokens and 170 output tokens per ticket, which at Bedrock list prices (3 USD per million input tokens, 15 USD per million output) comes to 0.0222 USD a ticket. Decider takes about 640 ms per request on a SageMaker ml.g5.xlarge (one A10G, 1.408 USD an hour). Running flat out, that is about 5,600 requests an hour, or 250 USD per million. With headroom for bursts the team puts the real figure at about 500 USD, and 22,200 divided by 500, about 44x, is where the 98% saving comes from.

The baseline, though, is Sonnet 4.6, a model released nine months ago, at list price with no caching. The write-up does not mention prompt caching, yet every ticket carries the same long system prompt and label descriptions, which is exactly the kind of work caching suits. If 5,000 of the 6,554 input tokens are the same every time, caching alone brings Sonnet 4.6 down to about 8,700 USD per million tickets.

Against today's small models the gap shrinks further. Anthropic's price list has Claude Haiku 5.5 at 0.10 USD per million input tokens, 0.50 USD per million output tokens and 0.01 USD per million cache reads. Allowing for the new tokenizer counting the same text as about 30% more tokens, and with thinking turned off, it comes to about 960 USD per million tickets without caching. With the fixed prompt cached it is about 380 USD, the same order of magnitude as Decider's 500 USD.

![Bar chart of model cost per million tickets: Sonnet 4.6 without caching 22,212 USD, with caching 8,712 USD, Haiku 5.5 without caching 963 USD, with caching 378 USD, Strands Decider with headroom 500 USD, fully busy 250 USD.](/strands-cost-en.svg)

_Tokens per ticket and the Decider costs are the Amazon team's reported figures; Sonnet 4.6 with caching and Haiku 5.5 are estimates from the November 2026 public price lists. There is no evidence yet on whether Haiku 5.5 handles this task as well as Sonnet 4.6._

Calling a decision model through an API is another option. Jev charges 0.042 USD per million input tokens and nothing for output, so sending the same 2,009 tokens that went to Decider would cost about 84 USD per million tickets. The tokenizers and input limits differ, so the comparison is rough, and the ticket contents would leave the company, but on model cost alone it is cheaper than a self-hosted GPU.

Even with the price gap set aside, the decision model keeps some advantages. Answers come back in under a second, it can run on an internal endpoint with outbound traffic blocked, and above all it returns a probability for each option. Many LLM APIs do not return token probabilities, so putting a threshold on an LLM means either using a confidence the model states in words or asking several times and measuring how much the answers disagree. The first runs into the overconfidence problem from the Jev post, and the second multiplies the cost by the number of calls.

## 3. What share of tickets cleared the threshold?

The Amazon team ran the 2B reference model and E4B on a test set of tickets, picked E4B, and then tuned how confident the model had to be before applying a label. Evaluated on a separate set of tickets, E4B reportedly beat the Sonnet in production. Recalibrating on their own tickets rather than trusting the README's "95% above 0.9" points the same way as the conclusion of the Jev post.

What is missing is any of this in numbers. There is no accuracy or macro-F1, no count of evaluation tickets, and nothing on who decided the correct labels. Nor is there the share of tickets that actually cleared the threshold and received a label (the coverage). Raising the threshold lifts the accuracy of the labels applied but leaves more tickets unlabelled, so the two figures only mean something when reported together.

How tickets below the threshold were handled also changes the cost calculation. DECIDER mode does not call Bedrock at all, so they may have been left unlabelled or sent to 'none'. Suppose 15% fall below the threshold and go back to Sonnet 4.6: cost per million tickets becomes Decider's 500 USD plus 3,330 USD for Sonnet, or 3,830 USD, a saving of about 6x rather than 44x. Handing them to people instead adds the labour cost of 150,000 tickets.

Either way, the 98% saving applies only to the tickets above the threshold.

## 4. Errors DUAL mode cannot see

The part of this case most worth copying is the three-way switch, which the Amazon team also singles out. The Lambda that does the labelling reads one of BEDROCK, DUAL or DECIDER from AWS AppConfig for each message. BEDROCK calls only Sonnet and DECIDER only Decider. DUAL calls both at once, applies Sonnet's result to the ticket and logs Decider's for comparison. The team says that running the two side by side on live traffic and judging each disagreement taught them more than any offline evaluation, and rolling back took a 45-second config change.

It is the same approach as the shadow mode suggested for new rules in [the risk metrics post](/en/risk-metrics-lift/), but one step is missing. If only disagreements are judged, nobody looks at the tickets where both models gave the same answer. Tickets where both are wrong for the same reason, for instance when a vague label description leads both to the same wrong category, never surface this way.

![Flow diagram: a ticket goes to Sonnet 4.6 and Strands Decider at the same time and the two answers are compared. When they differ, a person judges every case; when they match, only a random sample is audited.](/strands-dual-en.svg)

_The paths by which verdicts accumulate in DUAL mode. Auditing a sample of matching answers is not in the published case and is added here._

Closing that gap means drawing a random sample from the tickets where the answers match and auditing it separately. If the two models are wrong together around 2% of the time, about 750 tickets are needed to measure that rate to within ±1 percentage point. Combining the disagreement verdicts with this sample is what gives Decider's actual accuracy, because its rate of agreement with Sonnet cannot stand in for accuracy.

## 5. JSON key order moved the probabilities by 0.19

The Amazon team also notes something that surprised them. Sending the same content with the JSON keys in a different order moved the output probabilities by up to 0.19, and they now send every request with sorted keys. They add that anyone serving a decision model behind an API should check this before comparing runs.

The Decider README explains that because the pointer head has no per-option parameters, it cannot learn a bias such as "the first option is usually right". Even so, the hidden states the head compares are built by reading the preceding input in order, so the same content laid out differently can shift the probabilities. It looks like the same family of problem as the one the Jev documentation lists as a weakness, where the answer changes with the order of the options. ([TypeSafe](https://docs.typesafe.ai/model-jaggedness))

With a threshold at 0.8, a swing of 0.19 is enough to decide between automatic handling and a human check. With a decision model, the way inputs are built has to be treated as part of the model. Fix the serialisation rules such as key sorting, the label wording and the option order together with the model version, and revalidate the threshold if any of them changes. Another option, as the Jev documentation suggests, is to ask again with the options reordered and act automatically only when the two answers agree. Decision-model calls are cheap, so asking twice costs little.

The input limit causes similar trouble. The label descriptions in production were, on their own, longer than Decider's 4,096-token window. The team rewrote each of the 20 labels as a one- or two-sentence criterion and, adding 'none', passed them as the options of a single choice question. Long tickets had their oldest comments cut first. A ticket with a long comment thread is likely to be a drawn-out escalation, so misclassifying it tends to be costly as well. It is safer to track accuracy separately by ticket length band and to have a rule that sends long tickets to the LLM. Problems like these do not show up in a model's benchmark table. They come from the code that builds the input, the same kind of failure covered in [the post on AI failures that start outside the model](/en/ai-system-fails-outside-model/).

## 6. Carrying it over to financial operations

The Amazon team names the conditions under which this worked: a closed set of options, high volume, and latency on the old path that mattered. Conversely, they see a decision model as a poor replacement where labels need explanatory text, where the label catalogue changes weekly, or where the context needed will not fit in a few thousand tokens.

Financial firms have plenty of operational work that fits these conditions. Sorting complaints and call notes into set categories, classifying card disputes by reason code, and assigning transactions to categories in a budgeting app all have closed options and high volume. As an open model that fits on a single 24 GB GPU, it is also worth a look under the network separation rules common at Korean financial firms, which make calling an external API difficult.

Work that needs a written rationale does not end with a decision model. Closing an AML alert usually means recording the reason for closure, and a decision model cannot write that sentence. A realistic setup uses the decision model to prioritise alerts and leaves the closure decision and the write-up to a person or an LLM. In some cases complaint categories grow with each new product. Because the options are passed with every request, no retraining is needed, but the threshold has to be revalidated each time a new category is added.

## 7. My view

What will last from this case, I think, is the three-way switch rather than the 98% figure: running two models side by side on the same traffic, recording judged disagreements as labels, and being able to roll back within 45 seconds. It works for any model swap, decision model or not, and adding a sample audit of matching answers makes it possible to measure accuracy as well.

For a fair cost comparison, the baseline should be the cheapest alternative available now. The 44x comes from a nine-month-old model run without caching, a baseline set too high for choosing between real options, and at today's prices the gap narrows to the same order of magnitude. The reason to pick a decision model is that it returns probabilities, and using those probabilities means setting the threshold on your own labels, as the Jev post argued.

Had the write-up included coverage and accuracy above the threshold, other teams would find it much easier to judge whether to try this on their own work. A financial firm weighing a similar swap could start by putting those two figures, plus accuracy by ticket length band, in its first report.

---

**Related posts:**

- [What Does an AI's 90% Guarantee? Probability Calibration Through the Jev Decision Model](/en/decision-model-calibration/)
- [Why a Rule With Lift 2.4 on Its Own Fades Inside a Strategy: Four Ways to Measure Lift](/en/risk-metrics-lift/)
- [The Model Is Smart, So Why Is the System Stupid? Most AI Failures Start Outside the Model](/en/ai-system-fails-outside-model/)

## References

- [Amazon saves millions by replacing Sonnet 4.6 with Strands Decider (Strands Agents, 2026-11-09)](https://strandsagents.com/blog/amazon-saves-millions-replacing-sonnet-with-strands-decider/)
- [strands-labs/strands-decider (GitHub)](https://github.com/strands-labs/strands-decider)
- [Pricing (Claude Docs)](https://platform.claude.com/docs/en/about-claude/pricing)
- [Models (TypeSafe Docs)](https://docs.typesafe.ai/models)
- [Model jaggedness (TypeSafe Docs)](https://docs.typesafe.ai/model-jaggedness)
- [Ibrahim & Zaki, Evaluating Decision Models for Text Annotation in Computational Social Science (arXiv 2609.24574)](https://arxiv.org/abs/2609.24574)

_This post is based on the Strands Agents blog and the public materials in the Strands Decider repository as of 12 November 2026. The costs for Sonnet 4.6 with caching, Haiku 5.5 and Jev, and the scenario for handling tickets below the threshold, are estimates from public price lists and assumptions._
