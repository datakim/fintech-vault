---
title: "What to Decide Before an LLM Grades a Financial Chatbot's Answers"
description: "An LLM judge that agrees with human graders 85% of the time can still catch only one in four answers that deserve a zero. When an LLM grades a financial chatbot, decide how to tie each conversation to the customer's state and the terms in force at the time, what code checks and what the LLM judges, which failures act as gates, which agreement metrics to trust, and how to version the judge."
pubDatetime: 2026-11-13T00:05:00Z
koSlug: llm-judge-financial-chatbot
tags:
  - financial-ai
  - llm
  - machine-learning
---

Say a bank's chatbot told a customer on 3 September that a savings product paid 3.5% a year. On 1 October the rate on that product dropped to 3.2%. If a quality review in November feeds that conversation to an LLM judge together with today's product data, an answer that was correct in September gets a zero for quoting the wrong rate.

Quality review of customer conversations used to be a human job. QA staff pulled a sample of call recordings or chats and scored them against a checklist, and once a chatbot is answering tens of thousands of questions a day, sampling can no longer keep up. More firms are therefore putting an LLM in the grader's seat, an approach known as LLM-as-a-judge. I covered the grading methods themselves in [an earlier post on LLM evaluation](/en/llm-evaluation-methods/). When you actually wire one into operations, though, more of the work sits outside the prompt than inside it.

## 1. Grade one conversation, tied to its context at the time

If the unit of grading is a single reply, you get the interest rate problem above.

Whether a reply was right cannot be read off the reply alone. You need to know which products the customer held at the time, which rates and terms were in force that day, and the order in which the conversation unfolded. So the unit of grading is one conversation, carrying the customer's state, the time of the conversation, and the full exchange in order.

This is the same principle as the point-in-time join used to build credit scoring models. If arrears that appeared after the application date leak into the features, the model learns from the future, so features only get values that were knowable on the application date. For grading, you attach the rate table, the version of the terms, and the customer data that were valid when the conversation happened. If your product system simply overwrites old values with new ones, you need history tables first, and that work is likely to take more effort than tuning the judge prompt.

The same reply can also be a different sample depending on who received it. A line like "you could lose some of your principal" may be too little for a customer buying a fund for the first time and enough for one who has invested in similar products many times. Korea's Financial Consumer Protection Act frames the duty to explain (Article 19) as explaining the important points so that the ordinary customer can understand them, so whether an explanation was sufficient is hard to judge without knowing the customer.

Decide in advance what happens when context is missing. A failed rate lookup, a lookup that was never requested, and a product that simply has no rate should be recorded as different statuses, and the model should not be left to fill the gap. LLMs are good at filling blanks with plausible values, and if you ask one to grade a rate answer without the rate data, it may grade against whatever market rates it happens to know. Quietly dropping conversations with missing context and averaging the rest is risky too. Lookups are more likely to fail for discontinued products or limited-time offers whose history is poorly kept, and those are the conversations where wrong answers are more likely.

Within one conversation, each criterion also has its own scope. Whether a rate figure was correct can be checked reply by reply, but whether the risk was disclosed has to be judged across the whole conversation. If the third reply explained that principal could be lost, the fifth reply should not lose marks for not repeating it. Writing down for each rubric item whether it applies per reply or per conversation cuts out this kind of misjudgement.

## 2. Code checks the numbers, the LLM judges the explanation

Hand a whole conversation to an LLM and ask for a grade, and you will get a score. But with every piece of evidence mixed into one prompt, the criteria bleed into each other, and the model ends up weighing tone while judging the rate. When a score comes back low, you also cannot tell whether context was missing or the model misread it.

The split follows where the evidence for each judgement lives. Anything that structured data can settle is computed in code, such as comparing the rates, fees and limits quoted in a reply against the product data at the time, or checking that a required disclosure is present. Information that code can extract but that still needs interpretation is extracted by code first and passed to the LLM. Code can find the word "principal", but whether the sentence explains deposit insurance or presents an investment product as if the principal were guaranteed only becomes clear by reading it. The LLM only takes the judgements that need context, such as whether the reply answered what the customer asked and whether it explained things at the customer's level.

![A flow diagram. The full conversation and an as-of snapshot (products held, risk profile, that day's rates and terms) go into a context assembly step, where missing items are recorded as a status. The work then splits into code checks and an LLM judge, both pass through a gate, and the result is stored with the snapshot ID and judge version. A note says complaints and CSAT are kept out of the judge and joined only at analysis.](/judge-flow-en.svg)

_Scoring one conversation. Code takes the judgements it can settle, the LLM takes the rest, and every result keeps the input snapshot and the judge version._

For each item the LLM handles, write separate criteria for 0, 1 and 2 points, so the line between good, fair and poor is not left to the model. For risk disclosure, a reply that explains both the chance of loss and the conditions under which it happens gets 2, one that mentions the chance of loss but leaves out the conditions gets 1, and one that says nothing or implies there is no risk of loss gets 0. Have the judge return the score, the reason and an execution status separately. The score and reason are the judgement, and the status records whether all inputs were present and whether grading finished normally.

The middle score needs an especially narrow definition. When the criteria are vague, people and models alike push borderline replies into the 1 bucket, both give a 1, agreement goes up, and in practice nobody has judged anything.

A composite score that combines the dimensions is only for an overview. A reply that quoted the wrong rate but scored 2 for tone and 2 for completeness averages 1.33 across the three items and looks acceptable, yet in financial advice it is a reply someone needs to check straight away, whatever the average. So items like a wrong rate, presenting an investment product as if principal were guaranteed, or revealing another customer's personal data are set as gates, and tripping any one of them fails the conversation regardless of the other scores. It is the same structure as a credit decision that puts knockout rules, such as rejecting applicants currently in arrears, ahead of the scorecard. Whether a chatbot's reply counts as a sales recommendation in law needs separate analysis. Even so, the conduct that Article 21 of the same Act treats as improper solicitation, giving a definitive answer on something uncertain or saying things likely to make the customer believe an uncertain outcome is certain, is a sensible starting point for the list of gates.

Some information should never reach the judge, namely outcomes such as whether a complaint followed the conversation or what satisfaction score the customer gave. A judge that knows a complaint was filed may score the conversation low regardless of what was said, and any later finding that low-scoring conversations drew more complaints would then be counting the same information twice. For the same reason you keep the target variable out of a model's features, outcome data is joined only at the analysis stage, after grading is done.

## 3. When an 85% agreement judge misses the bad answers

Before a judge goes into operation, you check how well it matches human grading by having people and the judge score the same conversations against the same rubric, independently. Looking at the agreement rate alone at this step makes it easy to draw the wrong conclusion.

I built a synthetic example. Of 1,000 chatbot replies graded by people, 700 scored 2, 220 scored 1 and 80 scored 0, a distribution meant to reflect a chatbot that mostly answers well.

I then ran three judges with different temperaments against it.

![Bar charts for three judges compared with human grades. Exact agreement: always 2 at 70%, lenient judge 85%, strict judge 79%. Weighted kappa: 0.00, 0.65, 0.74. Recall on score-0 answers: 0%, 28%, 85%.](/judge-agreement-en.svg)

_Results computed on synthetic data. The lenient judge has the highest agreement but scores only 22 of the 80 zero-score answers as 0._

A judge that gives 2 to everything judges nothing, yet agrees with people 70% of the time. When 70% of the data scores 2, the floor for agreement is 70%, not 0%. The lenient judge has a habit of rounding up when in doubt, which gives it the highest agreement of the three at 85%, but it catches only 22 of the 80 zero-score answers. The strict judge has lower agreement at 79% and still catches 68 of them. A study comparing judge models with human graders also found that judges leaned towards lenient scoring, and that judges with similarly high agreement could still give quite different scores. ([Thakur et al., 2024](https://arxiv.org/abs/2406.12624))

Weighted kappa fixes part of this. Because it subtracts the agreement expected by chance, the always-2 judge drops to 0, and it penalises mistaking a 0 for a 2 more heavily than mistaking a 0 for a 1. That is why the strict judge comes out at 0.74, above the lenient judge's 0.65. Even so, the gap between the two kappas looks much smaller than the gap between 28% and 85% recall on zero-score answers. Weighted kappa sums up agreement across all three score levels in one number, so whatever happens in the zero bucket, 8% of the data, gets diluted. Feinstein and Cicchetti set out the paradox of high agreement with low kappa in 1990, and in a follow-up paper advised against relying on one omnibus number and looking at agreement for each category separately.

A financial chatbot judge should therefore be measured on weighted kappa for overall agreement and, separately, on recall for the zero-score answers that correspond to gates. Raising that recall has a price. Of the 105 replies the strict judge scored 0, people gave 37 a score of 1 or more, so reviewers make that many wasted trips. In financial advice this cost is usually worth paying. A missed zero-score reply can turn into a complaint or a mis-selling dispute, while a false flag costs a reviewer a few minutes. You can set gate items to favour recall and the remaining items to favour agreement.

Agreement between people sets the ceiling for the judge. If two QA staff grading the same conversations reach a weighted kappa of 0.7, asking the judge for 0.9 is close to asking it to copy one person's grading habits. The MT-Bench study's finding that GPT-4 agreed with human judges more than 80% of the time, about the level at which humans agree with each other, only means something read against that ceiling. ([Zheng et al., 2023](https://arxiv.org/abs/2306.05685))

When people and the judge disagree, sort out the cause first. If missing context caused the error, fix the data pipeline. If the rubric wording was ambiguous, fix the rubric, and if the model misread a clear rubric, change the prompt or the model. Tweaking the prompt to match the human score after every disagreement just hides the rubric's ambiguity inside the prompt. The human side does not stand still either. One study observed graders rewriting their criteria as they saw more outputs, even going back to change grades they had already given, a pattern it calls criteria drift. A rubric is a document that gets refined through grading, so it needs version numbers like anything else. ([Shankar et al., 2024](https://arxiv.org/abs/2404.12272))

## 4. Change the judge, regrade the same sample

If the average score was 1.71 three months ago and 1.64 this month, rule out other explanations before concluding the chatbot got worse. The judge prompt or rubric may have changed in between, or the rate history tables may have been reworked so that the judge now sees different context. The judge model itself may have changed, since a model behind an API can behave differently while keeping the same name. One study found that GPT-4's accuracy at identifying prime numbers fell from 84% to 51% between March and June 2023, under the same model name. ([Chen et al., 2023](https://arxiv.org/abs/2307.09009))

Every grading result should therefore keep two things. One is the input snapshot, meaning the customer state, rate and terms versions, and raw conversation attached to that case. The other is the judge version, covering the prompt, the rubric, rule thresholds, how inputs were trimmed and a dated model ID. With both in hand you can tell whether a change in scores came from the chatbot or from the judge, and months later you can rerun the same grading on the same input.

When you change the judge, grade a fixed sample with both the old and the new judge, and have reviewers open the cases where the results differ and mark whether the new judgement fits the rubric better, about the same, or worse. The question is whether judgements moved closer to the rubric, not whether scores went up or down. It works like champion and challenger testing when a credit scoring model is redeveloped, with the old and new models compared side by side on the same development sample, and the sample should mix randomly drawn conversations with borderline cases. As in the [Strands Decider post](/en/strands-decider-ticket-labeling/), you also need to audit a random share of the conversations where both judges gave the same score, or the cases where both are wrong stay hidden.

## 5. Watch the low end, not the average

Comparing averages alone also misses things when you test a new prompt for the chatbot itself. Suppose the share of 2s rises from 64% to 70% and the share of 0s rises from 2% to 3%. The average goes up from 1.62 to 1.67. For a service handling 500,000 conversations a month, that means zero-score replies rise from 10,000 to 15,000, and in financial advice those extra 5,000 weigh far more than a 0.05 gain in the average.

So read experiment results as a score distribution with the zero share alongside, and work down from the dimension that changed to the conversation, the reply, and the evidence and reason behind the score. If the risk disclosure score fell, open the low-scoring conversations and check whether the disclosure was missing altogether or was given but got buried behind other information. The score is an index for finding where the problem is, and the grounds for the judgement are the conversation and reason tied to it. If grading results do not keep their inputs and reasons, this path ends halfway.

LLM grading does not stand in for customer response. Grading shows how the content of the replies changed, and whether customers were actually better served still has to be checked through repeat contacts, complaints and satisfaction surveys. You can also have an LLM play the customer and run multi-turn conversations in advance, but a simulated customer tends to be more cooperative and more articulate than real ones, so this stays a way to filter out problems before launch.

## 6. Personal view

I think the most labour-intensive part of building an LLM judge is less the grading prompt and more the data work of retrieving the context as it was at the time of each conversation. Most firms have conversation logs piling up, but few will be able to attach that day's rate table, the version of the terms, and the products the customer held at the time. That work does not serve grading alone. In a dispute, showing what was explained and on what basis relies on the same data, so building the grading infrastructure also produces the records needed to check whether the duty to explain was met.

It is also worth remembering that the judge is a model too. In the [Jev post](/en/decision-model-calibration/) I argued that using a decision model's probabilities means resetting the threshold on your own labels. The same holds for a judge, which should be trusted on the recall for zero-score answers measured on your own conversations against your own rubric. The judge checks the chatbot and people check the judge, and since the human criteria move as well, this checking never finishes in one round.

If I were starting out, I would pick three or four gates and measure recall on zero-score answers for those items first. Having two QA staff independently grade a few hundred conversations to measure agreement between people also settles, from that number, how much you can expect from the judge.

---

**Related posts:**

- [How Do You Grade an LLM? Eleven Evaluation Methods, Sorted into Four Families](/en/llm-evaluation-methods/)
- [What Does an AI's 90% Guarantee? Probability Calibration Through the Jev Decision Model](/en/decision-model-calibration/)
- [What to Check Before Moving a Classifier From an LLM to a Decision Model: Amazon's Ticket Labelling Case](/en/strands-decider-ticket-labeling/)

## References

- [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (Zheng et al., 2023)](https://arxiv.org/abs/2306.05685)
- [Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges (Thakur et al., 2024)](https://arxiv.org/abs/2406.12624)
- [Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences (Shankar et al., UIST 2024)](https://arxiv.org/abs/2404.12272)
- [How Is ChatGPT's Behavior Changing over Time? (Chen, Zaharia & Zou, 2023)](https://arxiv.org/abs/2307.09009)
- [Weighted kappa: Nominal scale agreement with provision for scaled disagreement or partial credit (Cohen, 1968)](https://pubmed.ncbi.nlm.nih.gov/19673146/)
- [High agreement but low kappa: I. The problems of two paradoxes (Feinstein & Cicchetti, 1990)](https://doi.org/10.1016/0895-4356%2890%2990158-L)
- [High agreement but low kappa: II. Resolving the paradoxes (Cicchetti & Feinstein, 1990)](https://doi.org/10.1016/0895-4356%2890%2990159-M)
- [Financial Consumer Protection Act (Korea Law Information Center, in Korean)](https://www.law.go.kr/%EB%B2%95%EB%A0%B9/%EA%B8%88%EC%9C%B5%EC%86%8C%EB%B9%84%EC%9E%90%EB%B3%B4%ED%98%B8%EC%97%90%EA%B4%80%ED%95%9C%EB%B2%95%EB%A5%A0)

_This post is based on papers and legislation publicly available as of 13 November 2026. The judge comparison in the figure and the score distributions in section 5 are synthetic data built for illustration, not measurements on real conversations._
