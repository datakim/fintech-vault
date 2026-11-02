---
title: "Same AUC, Higher KS: KS and AUC Come From the Same Curve"
description: "A new scorecard matches the current one on AUC (0.75) but lifts KS from 0.36 to 0.42. Because both metrics come from one ROC curve, that gap is a sign the curve has an odd shape. In a simulated example, re-measuring on the applicants who pass a policy rule shows the new model is actually weaker."
pubDatetime: 2026-11-02T22:00:00Z
koSlug: risk-metrics-ks-auc
tags:
  - financial-ai
  - credit
  - machine-learning
---

Suppose the development results for a new scorecard, V2, have just come in. On the same development sample as the current model, V1, both have an AUC of 0.75, but KS is 0.36 for V1 and 0.42 for V2.

A team that leans on KS will naturally want to switch to V2. Yet when V2 runs as a challenger, the bad rate among approved customers at the same approval rate turns out higher for V2 than for V1. The numbers below reproduce this with simulated data (200,000 applicants, 5.9% bad), built around a set-up you can easily meet in practice. Once you know that KS and AUC come from the same curve, you can see this coming at the development stage.

## 1. KS and AUC come from the same ROC curve

Line applicants up from the highest score (the riskiest) down, and move the reject line down one applicant at a time. At each step you can work out what share of all bads has been rejected so far, and what share of all goods. The first is the TPR and the second the FPR, and in a scorecard's band table they are the "cumulative % bad" and "cumulative % good" columns. Plot those points with FPR across and TPR up, and you have the ROC curve.

![The ROC curve of model V1. The area under the curve is AUC; the longest vertical line between the curve and the diagonal is KS.](/riskm-roc-en.svg)

_V1's ROC curve. The blue area is AUC and the red vertical line is KS. (Simulated data, my own drawing.)_

KS is the largest vertical distance between this curve and the diagonal. As a formula it is KS = max(TPR − FPR), which is the same as finding the row in the band table where cumulative % bad and cumulative % good are furthest apart. AUC is the area under the curve, and it equals the probability that a randomly chosen bad scores higher than a randomly chosen good. The accuracy ratio (Gini) that many credit teams report is just 2 × AUC − 1.

Both metrics also look only at the order of the scores. Take logs, or rescale to a 300 to 900 range, and as long as the ranking stays the same, KS and AUC do not move. That is also why neither tells you whether the predicted bad rate matches the actual one (calibration). KS reads the single highest point of the curve, and AUC reads the area of the whole curve.

## 2. When the curve has an ordinary shape, AUC nearly fixes KS

Two numbers taken from one curve ought to be related. In the case textbooks use most, the scores of bads and goods are each normally distributed with the same spread, and their means sit d apart. Then both metrics are pinned down by d alone.

$$
\text{AUC} = \Phi\left(\frac{d}{\sqrt{2}}\right), \qquad \text{KS} = 2\,\Phi\left(\frac{d}{2}\right) - 1
$$

Φ is the cumulative distribution function of the standard normal. Eliminate d and KS becomes a function of AUC. A few values:

| AUC | 0.65 | 0.70 | 0.75 | 0.80 | 0.85 |
|---|---|---|---|---|---|
| KS for an ordinary curve | 0.22 | 0.29 | 0.37 | 0.45 | 0.54 |

Real scores never follow this assumption exactly, but when the curve bends smoothly, KS usually lands close to this table. V1, with an AUC of 0.75 and a KS of 0.36, is almost on it, while V2 has a KS of 0.42 at the same AUC, about 0.05 above what the table expects.

That gap is a useful diagnostic in its own right. When the actual KS is noticeably above or below what the AUC implies, draw the curve before you compare the two models' metrics.

## 3. V2's KS comes from the very start of the curve

Overlay the two ROC curves and the difference is easy to see.

![ROC curves of V1 and V2, both with AUC 0.75. V2 rises steeply at the start and then flattens.](/riskm-two-curves-en.svg)

_Both curves have the same area, but they cross. The dots mark where each model's KS is reached. (Simulated data.)_

V1's curve bends smoothly, and its KS is reached at the point where 31% of applicants are rejected. V2's curve shoots almost straight up at the start, then flattens quickly and drops below V1's. V2's KS of 0.42 comes from the point where only 8% of applicants are rejected, right where the curve has just risen. Because the curves cross, the same area can still give either model the edge depending on which reject line you compare at.

Split V2's score distribution into bads and goods and the reason shows.

![V2 score distribution. Bads with the external signal sit apart at the far right; bads without it overlap the goods.](/riskm-v2-dist-en.svg)

_V2's score distribution. The groups differ a lot in size, so each one is normalised separately. (Simulated data.)_

In this set-up V2 leans heavily on a strong signal from newly bought external data, something like a record that the applicant has just started missing payments at another lender. Applicants with that signal make up 44% of all bads, and V2 pushes them firmly to the top of the score range. The remaining bads, without the signal, overlap the goods almost completely, which is why the curve shoots up and then flattens. Catching that one cluster at the head is what lifted KS, but in the body V2 separates bads from goods less well than V1, and in terms of area the two effects cancel out to the same AUC.

## 4. Re-measured on the applicants who pass the rule

So far this only says V2 is strong at the head and weak in the body, which is not bad in itself. The problem was that the external data did not go into V2 alone. At the same time, the strategy team turned the same signal into a policy rule, so applicants with the signal were declined by the rule before the scorecard ever scored them.

![Applicants flow through a policy rule before reaching the scorecard, with metrics measured after the rule.](/riskm-rule-flow-en.svg)

_The numbers after the policy rule removes applicants with the external signal. (Simulated data.)_

In the simulated data this rule declines only 3.1% of applicants, yet that group holds 44% of all bads. The bad rate among those who pass the rule and reach the scorecard falls from 5.9% to 3.4%, and the head cluster that earned V2 its KS disappears entirely. Measured on this population, V1 has an AUC of 0.67 and a KS of 0.25, while V2 drops to an AUC of 0.56 and a KS of 0.09. At an 80% approval rate, the bad rate among approved customers is 2.5% for V1 and 3.1% for V2, which is what the challenger showed.

The development metrics were not wrong. The rule did not exist when V2 was built, and a KS of 0.42 was the right number for a world without it. The population where decisions are actually made had simply moved away from the development sample.

A common way to compare two models in practice is swap set analysis: at the same approval rate, you look only at the applicants on whom the two models disagree. Anyone both models approve, or both decline, gets the same outcome whichever model you use, so the only people a switch affects are the ones where the decisions differ.

| Applicants who pass the rule, 80% approval | Share | Bad rate |
|---|---|---|
| Both approve | 64.0% | 2.3% |
| Only V1 approves (declined if you switch to V2) | 16.0% | 3.4% |
| Only V2 approves (newly approved if you switch) | 16.0% | 6.4% |
| Both decline | 4.0% | 9.3% |

Switching to V2 means declining people with a 3.4% bad rate and approving people with a 6.4% bad rate in their place. This one table says far more about the effect of the switch than a KS difference of 0.05 does.

## 5. What to check before trusting a KS

The cause here was a policy rule, but there are plenty of other ways a KS can look better than the real effect. Start by checking whether the population you evaluated is the one where decisions are made. If anything that filters applicants before the scorecard has changed, such as policy rules, fraud blocks or pre-screening, re-measure on the people who get through it. Something similar happens when a model is built and evaluated only on previously approved customers, whose distribution differs from all applicants, so the metrics come out differently.

Check where the KS was reached, too. KS is a single point on the curve, so it means less when that point is far from the approval rate you actually run at. V2's KS comes from an 8% reject rate, but for a product run at 80% approval, TPR − FPR around a 20% reject rate is the more relevant number.

With few bads, KS moves around more than you might expect. Drawing samples of 5,000 applicants (about 300 bads) 400 times from a model whose true KS is 0.37 gave a 95% range of 0.33 to 0.43, and even the median, 0.38, sat a little above the true value. Because KS picks the maximum over many points on the curve, small samples make it easy to pick a point that jumped by chance, so it tends to be biased upwards. With 50,000 applicants the range narrows to 0.35 to 0.38. On a small validation sample, a KS difference of 0.05 needs a bootstrap range next to it.

If you compute KS from score bands, the gap is only measured at band edges, so on the same data it comes out equal to or lower than KS on raw scores, and figures from teams using 10 and 20 bands cannot be compared directly. Finally, if information that only exists after the application leaks into the variables, KS and AUC both inflate, so when development metrics look too good, check when each variable is created.

## 6. My view

When reporting a model change, I think two things belong next to KS and AUC. One is the bad rate at the approval rate you will actually run, and the other is the swap set table. KS and AUC only tell you how well the model ranks; what changes at the reject line you actually use is what those two show.

Comparing the actual KS with the KS the AUC implies is also a cheap check. If the gap is large, draw the curve, and if the head stands out, find which variable created that cluster and whether it is also used in a policy rule or another model. When model and strategy teams are separate, it is easy for both to bring in the same external data on their own.

Watching both metrics helps in ongoing monitoring as well. If both fall, the model as a whole has weakened; if AUC holds but KS drops sharply, it is worth suspecting that the strong signal behind the head has changed. Both only measure ranking, though, so score distribution shift (PSI) and predicted versus actual bad rates still need watching separately.

None of this means throwing V2 away. If the external signal is going to be used in a policy rule, the right move is to redevelop V2 on the applicants who pass that rule and strengthen how well it separates the body.

---

**Related posts:**

- [Why a Rule With Lift 2.4 on Its Own Fades Inside a Strategy: Four Ways to Measure Lift](/en/risk-metrics-lift/) (next in the series)
- [Where Transformers Fit in Credit Models: Affirm, Revolut, Parafin and Ant](/en/transformers-in-credit/)

## References

- [Fawcett, T. (2006). An introduction to ROC analysis. Pattern Recognition Letters, 27(8), 861-874.](https://doi.org/10.1016/j.patrec.2005.10.010)
- [Hanley, J. A., & McNeil, B. J. (1982). The meaning and use of the area under a receiver operating characteristic (ROC) curve. Radiology, 143(1), 29-36.](https://doi.org/10.1148/radiology.143.1.7063747)
- Siddiqi, N. (2017). Intelligent Credit Scoring: Building and Implementing Better Credit Risk Scorecards (2nd ed.). Wiley.

_The numbers and figures in this post come from simulated data I built for illustration (200,000 applicants, 5.9% bad), not from any real company or product. Written on 3 November 2026._
