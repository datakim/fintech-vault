---
title: "Why a Rule With Lift 2.4 on Its Own Fades Inside a Strategy: Four Ways to Measure Lift"
description: "A new rule measured a lift of 2.4 on its own, but once it was added to the existing strategy the bad rate among approved customers stayed at 3.62%. What decile, cumulative, marginal and amount-weighted lift each measure, and how to measure marginal lift when you never see what happens to people you decline, worked through with a simulated example."
pubDatetime: 2026-11-02T22:10:00Z
koSlug: risk-metrics-lift
tags:
  - financial-ai
  - credit
  - machine-learning
---

Suppose you want to add a new rule to a loan product with 20,000 applicants and a 5% bad rate. Measured on its own against past data, the rule catches 2,000 applicants, 240 of them bad, so its bad rate of 12% is 2.4 times the overall 5%.

A lift of 2.4 looks like a useful rule. Yet when you bolt it onto the existing strategy, the bad rate among approved customers barely moves. Nothing was miscalculated; the lift was measured on a different population and against a different baseline. [The previous post](/en/risk-metrics-ks-auc/) argued that KS and AUC need re-measuring on the applicants who pass the policy rules, and lift for a single rule runs into the same problem.

## 1. Decile lift and cumulative lift

Lift is the bad rate of some group divided by a baseline bad rate, and what you choose as the group and the baseline gives each kind of lift its name. The most common is decile lift: split the score into 10% bands and measure each band. In the figure below these are the bars. The riskiest 10% band has 275 bads out of 2,000, a 13.75% bad rate and a lift of 2.75, while the safest band has a lift of 0.15. Decile lift tells you how much worse than average the people in a band are, so it is what teams look at when setting policies such as declining the top band or offering better rates or limits to the bottom one.

![Decile lift bars and the cumulative lift curve. Cumulative lift falls towards 1 as the reject line moves down from the riskiest band.](/riskm-lift-en.svg)

_Decile and cumulative lift for a simulated example with 20,000 applicants and 1,000 bads._

Cumulative lift moves the reject line down from the top and compares the bad rate of everyone rejected so far with the average. Reject the top 20% and 470 of 4,000 are bad, a lift of 2.35; move the line all the way down and you reject everyone, so lift falls to 1. The finer the bands, the more jagged decile lift gets, while cumulative lift falls smoothly, which makes it easier to read when choosing a reject line.

Cumulative lift ties straight back to the ROC curve from the previous post. Divide the bad rate among rejected applicants by the average bad rate and, after rearranging, you get TPR divided by the reject rate. Rejecting the top 20% catches 47% of all bads, so 0.47 / 0.20 = 2.35. KS reads the same ranking as TPR − FPR, and cumulative lift reads it as TPR / reject rate.

## 2. Marginal lift: leaving out the people existing rules already catch

The new rule's lift of 2.4 was measured as if no other rule existed. A real strategy already runs rules, and in this example they decline 1,500 applicants, 330 of them bad.

![Overlap between the existing rules and the new rule. The new rule only adds 800 declines, 30 of them bad.](/riskm-overlap-en.svg)

_Of the 2,000 applicants the new rule catches, 1,200 were already declined by existing rules. (Simulated example.)_

Of the 2,000 applicants the new rule catches, 1,200 were already declined by the existing rules, and 210 of its 240 bads sit in that overlap. The people the new rule actually adds to the declines are the other 800, and only 30 of them (3.75%) are bad. Marginal lift compares the bad rate of those 800 with the bad rate of the population the rule really acts on, the 18,500 applicants who pass the existing rules, at 3.62%. That gives 3.75 / 3.62 ≈ 1.04, so the new rule is adding declines among people who are about as risky as the average.

In portfolio terms, before the new rule there are 18,500 approved customers with 670 bads, a 3.62% bad rate, and after it there are 17,700 with 640 bads, still 3.62%. The rule turns away 770 good customers to stop 30 bad ones, the bad rate stays where it was, and only the approval rate falls, from 92.5% to 88.5%.

Rule order matters for marginal lift too. Put the new rule first and the existing rules after it, and the credit for those 210 overlapping bads goes to the new rule, which now makes the existing rules look weak. When reporting results rule by rule, state the order you used, and when deciding whether to remove a rule, look at what changes if you run everything except that one rule.

## 3. Declined applicants have no outcomes

All of this assumed past data holds an outcome for everyone. In live operation, declined applicants never got a loan, so you cannot know whether they would have defaulted. Without outcomes for the people existing rules decline, even the bad rate in the overlap is really unknown, and the longer a rule runs, the less data you have to check whether it still earns its place. That is why risk teams deliberately leave themselves a way to observe outcomes.

![The new rule runs in shadow mode on the normal path, while a small holdout skips some rules.](/riskm-holdout-en.svg)

_Shadow mode and a holdout. The percentages are illustrative; set them by product and by the losses you can absorb._

A new rule runs first in shadow mode. It records who it would catch but makes no decisions, so outcomes build up for the people it flags who were approved anyway, and from those you can measure its marginal lift on the population it would really act on. Repayment outcomes take months to settle for most lending products, so the shadow period has to be about as long.

Rules that are already live are measured with a holdout: a very small share of applicants (2% in the figure) skips some of the rules. You accept a little extra loss on those applicants in return for data showing whether the rules still work. Rules required by law or regulation, and clear-cut fraud blocks, still apply to the holdout. A small holdout yields few bads, so it can take several months of data before differences show, and the share should be set by weighing the loss you can absorb against the sample size you need.

## 4. Count lift and amount lift

So far everything has been counted in people, but losses come in money. Take the 800 applicants only the new rule catches and look at them by amount. If the 18,500 applicants who pass the existing rules borrow 5 million won on average and their 670 bads borrow 4.5 million won on average, the amount-weighted bad rate is 670 × 4.5 million / (18,500 × 5 million) ≈ 3.26%. If the 800 applicants caught only by the new rule borrow 9 million won on average and their 30 bads 14 million won, their amount-weighted bad rate is 30 × 14 million / (800 × 9 million) ≈ 5.83%, and the amount lift is 5.83 / 3.26 ≈ 1.8.

By headcount these people are as risky as the average, but by amount they cause close to twice the average loss. A rule like this may be useless as a decline rule and still useful as a limit rule, because lowering their limits instead of declining them cuts the loss without turning away good customers.

Turned around, a band where amount lift runs consistently above count lift may be a sign that risky people are getting large limits. Customers from products or channels that naturally borrow more may be mixed in, though, so split by product and channel before changing limits. Card fraud rules are tracked by fraud rate on transaction value as well as on transaction count for the same reason.

One step beyond amount is weighting by loss itself. Credit risk writes expected loss as EL = PD × EAD × LGD, where PD is the probability of default, EAD the exposure at default and LGD the share not recovered after a default. When recovery through collateral or collections varies a lot between products, loan amount alone does not capture the real loss, so use lift weighted by actual losses for periods with outcomes and by EL for periods still waiting for them.

## 5. My view

When reviewing a new rule, I think it pays to go through four questions in order.

1. Which lift is this: decile, cumulative, marginal or amount-weighted?
2. What is the marginal lift, measured on the applicants who pass the existing rules?
3. How will you see outcomes for the people this rule will decline (a shadow period, a holdout)?
4. Does the conclusion hold by amount as well, and would a limit change suit better than a decline?

The same goes for buying new external data. Data that tests well on its own adds little once it overlaps with the variables and rules you already use, so measuring its marginal effect on top of the existing model and strategy before signing a contract saves money.

Had the team in the example looked at the 1.04 measured behind the existing rules instead of the stand-alone 2.4, they would have known in advance that the rule would cost 770 good customers and leave the bad rate where it was.

---

**Related posts:**

- [Same AUC, Higher KS: KS and AUC Come From the Same Curve](/en/risk-metrics-ks-auc/) (previous in the series)
- [Where Transformers Fit in Credit Models: Affirm, Revolut, Parafin and Ant](/en/transformers-in-credit/)

## References

- Siddiqi, N. (2017). Intelligent Credit Scoring: Building and Implementing Better Credit Risk Scorecards (2nd ed.). Wiley.
- Thomas, L. C., Edelman, D. B., & Crook, J. N. (2002). Credit Scoring and Its Applications. SIAM.
- [Basel Committee on Banking Supervision (2005). An Explanatory Note on the Basel II IRB Risk Weight Functions.](https://www.bis.org/publications/explanatory-note-basel-ii-irb-risk-weight-functions)

_The numbers in this post are a simulated example built for illustration (20,000 applicants, 1,000 bads), not figures from any real company or product. Written on 3 November 2026._
