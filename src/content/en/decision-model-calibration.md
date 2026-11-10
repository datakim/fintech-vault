---
title: "What Does an AI's 90% Guarantee? Probability Calibration Through the Jev Decision Model"
description: "TypeSafe says its decision model Jev is trained so that answers given 0.8 are right about 80% of the time. Independent evaluations found the calibration holds when tasks are pooled but drifts task by task, because the model's base rate does not match each task's. How this differs from the probabilities a general LLM states in words, and, using merchant underwriting as the example, how to use your own labels to bound the error rate of an auto-approve threshold."
pubDatetime: 2026-11-10T04:00:00Z
koSlug: decision-model-calibration
tags:
  - financial-ai
  - llm
  - ai-agent
  - machine-learning
---

On 15 September 2026, a model arrived that does not write a single sentence. It is Jev, from TypeSafe, a company co-founded by former OpenAI researcher Diogo Almeida. Give it a question and a set of options and it returns one option plus a probability for each, and the company says these probabilities are calibrated: answers given 0.8 are right about 80% of the time.

When a financial firm plugs in a model like this, a threshold goes onto that probability almost immediately. Above 0.9 it approves automatically and below that it hands over to a person, and when estimating losses the probability is multiplied by an amount. So the first things to settle are who guarantees that the 0.9 is right, and how, and what makes this different from asking a general LLM to state a probability alongside its answer.

The short answer is that no model can guarantee it on its own, and the guarantee comes from the labels you hold. Merchant underwriting at a card acquirer or payment gateway makes a good example for following the reasons and the method.

## 1. A model that returns only options and probabilities

The questions you can ask Jev come in fixed forms: Choice picks one of a set of options, Score places the input on a graded scale, Noul gives the probability that a yes/no answer is yes, and Box (from version 1.14) finds a location in an image. Several questions can go in one request, and each is evaluated separately against the same input. The output is only typed values and probabilities, so there is no text to parse. The price is 0.042 USD per million input tokens, with no charge for output. ([TypeSafe](https://docs.typesafe.ai/models))

It is also worth knowing that Jev is not fine-tuned on customer data. Every customer uses the same weights, and domain knowledge has to be written into the input (the state), the questions and the option descriptions.

For merchant underwriting, you would pass the applicant's declared category and the text of its website as the input, and use a Noul to ask whether the site shows signs of selling restricted goods outside that category.

```python
from typesafe_sdk import Noul, TypeSafeClient

with TypeSafeClient() as client:
    res = client.system_one(
        model="jev-1.14.0",
        state={"declared_category": "clothing store", "site_text": site_text},
        questions={
            "restricted": Noul(
                instructions="Does `site_text` show sales of restricted goods outside "
                             "`declared_category`, such as gambling, adult content or crypto brokerage?"
            ),
        },
    )
p = res.answers["restricted"].noul   # 0 to 1, probability the answer is yes
```

The code approves automatically when p is below a threshold and sends the merchant to an underwriter otherwise. In the [post on agent virtual cards](/en/agent-virtual-card-controls/) I noted that a merchant category code does not tell you everything a merchant sells; underwriting is the step where that code is first assigned. Merchants missed here come back later as disputes and rule breaches.

## 2. What the number 0.9 promises

Calibration is the property that probabilities match observed frequencies. If you gather 100 merchants the model scored at 0.9 and about 90 of them really are restricted, that band is calibrated. TypeSafe's documentation also notes that these rates describe groups of predictions, not a guarantee about any single answer. ([TypeSafe](https://docs.typesafe.ai/introduction/machine-learning-primer))

Calibration is also different from the ability to rank. The [post on KS and AUC](/en/risk-metrics-ks-auc/) pointed out that both metrics look only at the order of the scores; halve every probability and AUROC does not move, but calibration is ruined. This is why credit risk teams validate a default model's discriminatory power and its calibration separately.

A Choice answer carries one more value besides the probabilities, called confidence. The name invites reading it as "the probability of being right", but it is actually the distance of the top probability from an even split (1/n with n options), stretched onto a 0 to 1 scale.

$$
\text{confidence} = \frac{p_{\max} - 1/n}{1 - 1/n}
$$

So a confidence of 0.5 means a probability of 0.75 with two options and 0.55 with ten. A single rule like "act automatically when confidence is at least 0.9" therefore accepts a different risk for each question, and TypeSafe's documentation recommends putting the threshold on the probability of the option your code will act on. ([TypeSafe](https://docs.typesafe.ai/confidence)) The Noul in the underwriting example has no separate confidence; the value it returns is the probability.

## 3. Stated probabilities, token probabilities and decision-model distributions

When you tell a general LLM to "give a probability too", the 0.9 you get back is text the model generated. For a model trained on next-token prediction and human preference, that number has never been checked against outcomes; it is closer to a number that sounds plausible in context. Xiong et al. (ICLR 2024) reported that confidence stated this way tends to run higher than actual accuracy, and in the independent evaluation described below, the LLMs' stated confidence clustered on a handful of round values between 0.7 and 0.95.

You can also read the token probabilities inside the model, the probability it puts on the answer token. Large pretrained models are fairly well calibrated on this measure for multiple-choice questions (Kadavath et al., 2022). The trouble is that the property weakens as the model is tuned for chat. The GPT-4 technical report includes a chart in which the pretrained model is well calibrated and the model after post-training such as RLHF is much less so. Many commercial APIs do not expose these probabilities at all; of the 19 LLM APIs in the independent evaluation, none returned usable token probabilities.

For a decision model, the probability distribution over the options is the output itself. TypeSafe says it trains this distribution with a method it calls RLCD (Reinforcement Learning for Calibrated Decisions). Its argument is that RLHF rewards answers people prefer, which encourages sycophancy and confident hallucination, so honest probabilities need a different objective from the start. The company has said only that it uses a new architecture and a parallel sampler; the reward function and training procedure have not been published. ([TypeSafe](https://typesafe.ai/blog/introducing-system-one-models-and-jev))

![The same 0.9 can come from three places. A verbalised confidence is text the model writes, so unless it was trained against outcomes it is just a plausible number, and it clusters on round values. A token probability is fairly calibrated after pretraining but worse after RLHF, and many APIs do not expose it. A decision-model distribution is trained with calibration as a goal, but the method is not disclosed, and it is split only across the options given.](/calib-sources-en.svg)

_Figure 1. Three sources of a probability. Drawn from the documentation and papers cited in the text._

So describing the difference from a general LLM as "stating a number versus returning a distribution" is only half right. For probabilities to match outcomes, the number has to be trained by scoring it against outcomes, and the scoring used for that is a proper scoring rule: a rule, such as the Brier score or log loss, under which you get the best expected score by reporting the probability you actually believe. RLCR from MIT researchers (Damani et al., ICLR 2026) added a Brier score to the correctness reward and reported that stated confidence became calibrated with no loss of accuracy. What decides calibration, in other words, is less whether the probability is spoken or returned as a distribution than what the number was trained against.

There is also a study that measures the two side by side. Ibrahim and Zaki compared Jev with 19 LLMs under the same zero-shot protocol on 18 social science text classification tasks (7,977 items). On accuracy (macro-F1), Jev trailed the best LLM for the task on 14 of the 15 evaluation tasks, with a median gap of 11.6 points, at a median of one forty-fourth of the cost. Its median expected calibration error (ECE) was 0.157: better than the stated confidence of 16 of the 19 LLMs, but worse than three frontier Claude models (Opus 5 at 0.066, Fable 5.1 at 0.073, Sonnet 5 at 0.075). ([arXiv 2609.24574](https://arxiv.org/abs/2609.24574))

Those three models' confidence, however, sat on a few values, and when the bins were redrawn to hold equal numbers of items, Fable 5.1 rose from 0.073 to 0.123 and Sonnet 5 from 0.075 to 0.156. Jev barely moved (0.157 to 0.154). A result in the other direction came from post-hoc temperature scaling (Guo et al., 2017), which here meant converting each LLM's stated confidence to a logit and fitting a single temperature on a few labelled tasks. Llama 4 Scout dropped from 0.312 to 0.060 and Gemini 3.1 Pro from 0.233 to 0.076, both below Jev after the same treatment (0.121). The authors read this as weakening the claim that built-in calibration is the advantage of this model class, since a few labels bring cheap LLMs to frontier-level calibration.

Where the decision model clearly wins is cost and output format. You get continuous probabilities for every item at low cost, and answers never fall outside the options or break the format. Whether those probabilities are right for your problem is a separate question.

## 4. Right when pooled, off task by task

Guo et al. tried Jev as a detector of AI alignment failures. Across 44 benchmarks covering ten failure types, such as sycophancy, jailbreaks and prompt injection, a single generic Noul question, not reworded for each task, reached a median AUROC of 0.886. Ranking was good, but calibration depended on the unit you looked at. ([arXiv 2609.29429](https://arxiv.org/abs/2609.29429))

Pooled over all benchmarks, the reliability curve sat close to the diagonal (ECE 0.047). Measured one benchmark at a time, the median ECE was 0.168, more than twice what a perfectly calibrated model could show through sampling noise alone (0.074), and 24 of 31 benchmarks exceeded that level. The median AUROC within a benchmark was 0.905, so ranking was not the problem. Instead, Jev's mean probability missed each benchmark's actual positive rate by a median of 0.125. The authors diagnose a base-rate mismatch and note that estimating the positive rate without labels and correcting for it did not help. Their conclusion is that thresholds need to be set separately with a few labels.

The social science evaluation produced a more extreme case. On a task judging empathy in support conversations, Jev gave confidence of 0.9 or more to 78% of items, and accuracy on those items was 0.383, almost the same as the paper's baseline of 0.371. In the authors' words, confidence carried no information on this task. Accuracy in the 0.9-and-above band ranged from 0.975 (figurative language) to 0.611 (conversational toxicity prediction) depending on the task. TypeSafe says Jev cannot hallucinate because it never answers outside the options, but as this case shows, that does not stop it from being confident about the wrong option.

A small simulation shows why this happens. I built three tasks of 20,000 items each with positive rates of 50%, 20% and 3%, and a model that ranks well on all three (AUROC 0.90) but believes the positive rate is 24%, the average of the three. The pooled curve sits on the diagonal with an ECE of 0.003, yet on task C (3% positive) the mean probability is 0.15, five times the actual rate, and on task A (50% positive) it is 0.36, below the actual rate.

![Pooled across three tasks, the reliability curve sits on the diagonal, but task by task it does not. Task A, with 50% positives, lies above the diagonal; task C, with 3% positives, lies far below. AUROC is 0.90 on all three tasks.](/calib-reliability-en.svg)

_Figure 2. Reliability curves for three tasks with the same ranking and different positive rates. Synthetic data._

A probability has the base rate baked into it. Faced with the same evidence, a rare event should get a lower posterior probability, but the model does not know your data's base rate. Take a 0.9 that was well calibrated on data with 30% positives and apply it where only 3% are positive: in odds, $9 \times \frac{3/97}{30/70} \approx 0.65$, which is a probability of about 0.39.

This is a familiar scene in credit risk. Move a model to a different product or a later cohort of customers and the ranking usually holds, but the level of predicted default rates drifts, so you recalibrate to that portfolio's actual default rate. Credit bureau scores, likewise, are not used directly as default probabilities; lenders usually rebuild a score-band table from their own bad rates. Jev is not trained on customer data, so it cannot know whether 2% or 0.2% of your merchants are restricted, and for a problem like card fraud, where the positive rate is [0.015%](/en/fds-foundation-models-anomaly/), the mismatch grows much larger.

## 5. The guarantee comes from your labels

I ran the underwriting example end to end on synthetic data. There are 3,000 merchants judged by underwriters over the past few months, and 3.07% of them are actually restricted. The model is assumed to rank well (AUROC 0.91) but to be tuned to a world where 30% are positive. It is not real Jev output; it is a hypothetical model that carries over the problem from section 4.

Counting the actual rate in each band of model probability gives this:

| Model probability | Merchants | Mean probability | Actual restricted rate |
|---|---:|---:|---:|
| 0.0 to 0.1 | 1,610 | 0.036 | 0.002 |
| 0.1 to 0.3 | 732 | 0.178 | 0.018 |
| 0.3 to 0.6 | 415 | 0.424 | 0.039 |
| 0.6 to 1.0 | 243 | 0.765 | 0.247 |

Of the 243 merchants scored 0.6 or more, a quarter are actually restricted, and the overall mean probability of 0.183 is six times the actual rate. The ranking is right, so the model is worth keeping; only the level needs refitting.

1,000 of the 3,000 merchants go to Platt scaling, which converts the original probability to a logit and fits a new slope and intercept with logistic regression. The intercept shifts the base rate and the slope corrects over- or under-confidence. The temperature scaling in section 3 only adjusts the slope, so when the base rate is off, it is better to fit the intercept too. On the remaining 2,000 merchants, the mean recalibrated probability was 3.07% against an actual rate of 2.80%.

Now to choose the auto-approve threshold. The goal is to say, with 95% confidence, that no more than 1% of auto-approved merchants are restricted. Fix five candidate thresholds in advance, count the restricted merchants among the validation merchants in each candidate's auto-approve band, and compute an upper bound on the error rate with the Clopper-Pearson method. Testing all five raises the chance that one passes by luck, so divide the 5% by five and use a 99% upper bound for each (a Bonferroni correction), then pick the candidate with the widest auto-approve band among those whose bound is at or below 1%.

```python
import numpy as np
from scipy.stats import beta
from sklearn.linear_model import LogisticRegression


def logit(p):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


def reliability(p, y, edges=(0, 0.1, 0.3, 0.6, 1.0)):
    """Count the actual positive rate in each band of model probability."""
    idx = np.digitize(p, edges[1:-1])
    rows = []
    for b in range(len(edges) - 1):
        m = idx == b
        if m.any():
            rows.append((f"{edges[b]:.1f}-{edges[b + 1]:.1f}", int(m.sum()), p[m].mean(), y[m].mean()))
    return rows


def fit_platt(p, y):
    """Fit a new slope and intercept on the logit of the original probability (Platt scaling)."""
    lr = LogisticRegression(C=1e6).fit(logit(p).reshape(-1, 1), y)
    return lambda q: lr.predict_proba(logit(q).reshape(-1, 1))[:, 1]


def certify(p, y, candidates, target=0.01, delta=0.05):
    """Pick the widest auto-approve band (p < t) whose error-rate upper bound is at or below target."""
    d = delta / len(candidates)                      # stricter per candidate (Bonferroni)
    rows, best = [], None
    for t in candidates:
        lane = p < t
        n, k = int(lane.sum()), int(y[lane].sum())
        upper = beta.ppf(1 - d, k + 1, n - k) if n > k else 1.0   # one-sided Clopper-Pearson bound
        rows.append((t, lane.mean(), n, k, upper))
        if upper <= target:
            best = t                                 # candidates run from narrow to wide
    return best, rows


# p_raw: the model's probability, y: underwriter verdict (1 if restricted)
# first 1,000 merchants for recalibration, last 2,000 for validating thresholds
calibrate = fit_platt(p_raw[:1000], y[:1000])
p_cal = calibrate(p_raw[1000:])
best, rows = certify(p_cal, y[1000:], [0.002, 0.005, 0.01, 0.02, 0.05])
```

![Choosing the auto-approve threshold with your own labels. Of 3,000 merchants with underwriter verdicts, 1,000 are used to refit the probabilities and 2,000 to compute, for each candidate, the 95% upper bound on the auto-approve error rate. Candidates 0.002, 0.005 and 0.01 have bounds at or below 1% and pass; 0.02 and 0.05 fail, so the widest passing candidate, 0.01, is chosen.](/calib-threshold-en.svg)

_Figure 3. Validation results for each candidate threshold. Synthetic data._

0.01 is the widest candidate that passes, so 58% of merchants are approved automatically. 0.02 failed even though its observed error rate on the validation sample was 0.42% (6 of 1,436), less than half the target, because its upper bound was 1.01%. A guarantee needs that much margin, and a small sample keeps the bound high even with no errors at all. Even when testing a single candidate, the 95% upper bound after observing zero errors is roughly $3/n$, so to claim a 1% error rate the auto-approve band needs close to 300 items. Testing five candidates at once with 99% bounds, as in this example, makes it roughly $4.6/n$, or about 460 items, which is why candidate 0.002 only just passed with 0 errors out of 516 and a bound of 0.89%.

Applying the same model and recalibration to 200,000 future merchants (fresh synthetic data from the same distribution), 59.3% are approved automatically and the actual restricted rate among them is 0.34%, while 93.2% of restricted merchants go to an underwriter. Repeating the experiment 100 times with different seeds, no candidate passed in 20 runs, and in the 80 runs that chose a threshold, the actual error rate never exceeded 1% (the highest was 0.97%). In other words, 2,000 validation labels are sometimes not enough to guarantee anything.

The guarantee assumes that the merchants used for validation and those still to come are drawn from the same distribution. If a new partner channel brings in a different kind of merchant, the model version changes, or the question wording or options are edited, the table has to be rebuilt. TypeSafe itself notes that aliases such as `jev-latest` move to new versions as they ship, and recommends pinning a version ID such as `jev-1.14.0` once you have tuned thresholds.

Once in production, the labels become lopsided. Underwriters never see the merchants that were approved automatically, so labels for the next validation accumulate only on the reviewed side. It is the same shape as reject inference in credit, where you never learn whether rejected applicants would have defaulted, so you need to send a random fraction of the auto-approve band to underwriters as well in order to build the next table.

## 6. More to check before using it in financial operations

If all you are doing is choosing one threshold, calibration is not strictly necessary. The procedure in section 5 works the same way with candidates set on the original probabilities, as long as the ranking is right. Calibration becomes necessary when the probability goes into a calculation as a number.

Suppose letting a restricted merchant through costs 3 million KRW in expected losses and an underwriter's review of one merchant costs 15,000 KRW. Then reviewing is worth it whenever the probability of being restricted exceeds 0.005. Feed the original probabilities into this rule and only 5.9% are approved automatically, leaving 94.1% for underwriters. With recalibrated probabilities, 44.5% are approved automatically and the actual error rate among them is 0.19% (on 200,000 synthetic merchants). The usage TypeSafe recommends rests on the same assumption: break a judgement into small questions and combine the answers in code. If each question's probabilities are off by a different amount, a score built from weighted sums or products is off as well.

Keep in mind, too, that the options are a closed set. Choice probabilities are split only across the options you supply and sum to 1, so when the right answer is not among them, the nearest option still gets a high probability. TypeSafe's documentation warns that a "none of the above" option may not work well and suggests adding a companion Noul that asks whether any option fits. ([TypeSafe](https://docs.typesafe.ai/primitives/choice)) Adding an option, say "crypto assets" to a category list, redistributes the existing probabilities, so thresholds tuned earlier need validating again.

Jev's own list of weak spots includes items that touch financial work. It can lean towards the first option, so the documentation suggests reordering the options and asking again, and it advises doing arithmetic and date comparisons in code because the model is unreliable at them. ([TypeSafe](https://docs.typesafe.ai/model-jaggedness)) Tasks with a fixed right answer, such as comparing amounts or working out settlement dates, should not be given to the model in the first place.

On cost, splitting the work into stages is the practical setup. In the social science evaluation, keeping Jev's answers for high-confidence items and passing the rest to an LLM matched or beat the LLM alone at a quarter to half of its cost. For merchant underwriting that means screening with Jev first, having an LLM read more of the site and set out the evidence for ambiguous cases, and leaving the final decision to an underwriter.

## 7. My view

What makes decision models welcome is that probabilities are the default output. Unlike the days of parsing numbers out of LLM answers, every item gets a continuous probability, and it is cheap enough to run on everything. Once you have a number you can measure, reliability tables, recalibration and threshold validation can all be done with the tools credit risk teams already use.

Reading "calibrated probabilities" as "probabilities that are right for my business" is a mistake, though. Even if training went as the company describes, the calibration fits the distribution of the data it was trained on. Just as a credit bureau score is recalibrated to your own bad rates before use, I think a decision model's probability should be treated as one more external score and put through the same procedure.

Seen this way, the weight of automation cost shifts from the model to the labels. Building the system that records underwriter verdicts as labels and samples the auto-approve band for re-checking takes more money and time than a model at 0.042 USD per million input tokens. I have not yet found a public evaluation of Jev on financial text. For a team thinking of trying it, the first job is probably to draw a reliability table from a few thousand of its own past decisions.

**Related posts:**

- [Same AUC, Higher KS: KS and AUC Come From the Same Curve](/en/risk-metrics-ks-auc/)
- [[FDS] Finding the 0.015%: Transaction Sequence Models, Anomaly Detection and Graphs](/en/fds-foundation-models-anomaly/)
- [Why a Single-Use Card Gets Charged Twice: The Gaps in Expressing an AI Agent's Authority as a Virtual Card](/en/agent-virtual-card-controls/)

## References

- [Introducing System One Models & Jev (TypeSafe, 2026-09-15)](https://typesafe.ai/blog/introducing-system-one-models-and-jev)
- [Models (TypeSafe Docs)](https://docs.typesafe.ai/models)
- [AI primer (TypeSafe Docs)](https://docs.typesafe.ai/introduction/machine-learning-primer)
- [Confidence (TypeSafe Docs)](https://docs.typesafe.ai/confidence)
- [Choice (TypeSafe Docs)](https://docs.typesafe.ai/primitives/choice)
- [Model jaggedness (TypeSafe Docs)](https://docs.typesafe.ai/model-jaggedness)
- [Ibrahim & Zaki, Evaluating Decision Models for Text Annotation in Computational Social Science (arXiv 2609.24574)](https://arxiv.org/abs/2609.24574)
- [Guo et al., Just Ask Jev: Reinforcement Learning for Calibrated Decisions as a Zero-Shot Detector of AI Alignment Failures (arXiv 2609.29429)](https://arxiv.org/abs/2609.29429)
- [Xiong et al., Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs (ICLR 2024)](https://arxiv.org/abs/2306.13063)
- [Kadavath et al., Language Models (Mostly) Know What They Know (arXiv 2207.05221)](https://arxiv.org/abs/2207.05221)
- [OpenAI, GPT-4 Technical Report (arXiv 2303.08774)](https://arxiv.org/abs/2303.08774)
- [Damani et al., Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty (ICLR 2026)](https://arxiv.org/abs/2507.16806)
- [Guo et al., On Calibration of Modern Neural Networks (ICML 2017)](https://arxiv.org/abs/1706.04599)

_This post is based on TypeSafe's public documentation and arXiv papers as of 10 November 2026. Because the RLCD training method has not been published, it covers only what can be confirmed from the company's documentation and independent evaluations. The table and the numbers in Figures 2 and 3 come from a synthetic-data simulation, not real Jev output. The loss and review costs are also assumptions for illustration._
