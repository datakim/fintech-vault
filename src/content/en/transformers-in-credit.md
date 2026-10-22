---
title: "Where Transformers Fit in Credit Models: Affirm, Revolut, Parafin and Ant"
description: "Affirm has put a transformer in front of its underwriting model. It reads each credit-report account as one token and feeds the resulting embeddings into XGBoost. From Revolut's PRAGMA and Parafin's ParaFormer to Ant's Falcon TST and BYB, where financial companies have placed transformers next to tree models, and how to read the numbers they publish."
pubDatetime: 2026-10-21T23:00:00Z
koSlug: transformers-in-credit
tags:
  - financial-ai
  - machine-learning
  - fintech
---

On 17 September, Affirm announced that it had started using a transformer model to underwrite new customers.

Affirm is a US buy now, pay later (BNPL) lender. It decides whether to approve an instalment loan in under a second, at checkout. Until now that decision came from XGBoost.

The new model keeps XGBoost. A transformer reads the credit report and produces embeddings, and those embeddings go into the existing XGBoost model as features.

Similar announcements have come all year. In April, Revolut published a paper on PRAGMA, a foundation model trained on 24 billion banking events. In May, Brazil's Nubank published results for its transformer credit model, nuFormer, and Parafin, which lends to small businesses, wrote that it had replaced an XGBoost ensemble with a single transformer. In August, Ant International, part of the Ant Group family, released version 2.0 of its time-series model Falcon TST.

All of them use transformers, but what each one predicts and how it treats tree models differ quite a lot from company to company.

## 1. This year's cases

| Company | Published | Predicts | Input | Relation to tree models |
|---|---|---|---|---|
| Nubank (nuFormer) | Paper July 2025, revised August 2026 | Credit default and other tasks | Card and account transaction sequences | Trained jointly with a differentiable tabular model instead of LightGBM |
| Revolut (PRAGMA) | Paper April 2026, revised August | Several tasks: credit, fraud, recommendations | Sequences of app, transaction and trading events | Type of baseline model not disclosed |
| Parafin (ParaFormer) | May 2026 | Distribution of a small business's sales over the next 12 months | Daily sales aggregated to monthly series | Replaces an XGBoost ensemble |
| Ant International (Falcon TST) | 1.0 November 2025, 2.0 August 2026 | Cash flow, FX exposure | Time series | Not a credit model |
| Affirm | September 2026 | Delinquency risk of new customers | Credit-report accounts and inquiries | Embeddings fed into XGBoost |

Revolut trained its model on 25 months of events from 26 million users. These are card payments, in-app navigation, trades and communications sent to customers. That single model is then adapted to tasks such as credit scoring, fraud detection and product recommendation, either with a light classification head or by fine-tuning.

Nubank pretrained a transformer GPT-style, predicting the next token, on more than 100 billion transactions from over 100 million customers. In the paper, its credit-default AUC is 1.25% higher than LightGBM in relative terms. A May press release says it cut risk by 70% for an equivalent population, without saying what was measured or how.

Parafin lends to sellers inside platforms such as Amazon and DoorDash. At the end of September it announced that Stripe would acquire it. ParaFormer is not a default model. It forecasts the range of a seller's sales over the next 12 months, and the loan size is set from that forecast.

Chinese media call Falcon TST 鹰序 (Yingxu) TST. It comes from Ant International, the Singapore-based affiliate of Ant Group, not from domestic Alipay. The company uses it to forecast its own cash flow and FX exposure, and says Citi, Barclays, Standard Chartered and Deutsche Bank have built it into FX products or liquidity management.

Ant Group has a case closer to credit: the BYB paper, posted to arXiv in late May 2025. It pretrained a four-layer transformer encoder on 180 days of in-app behaviour from about 10 million Alipay users. Its pretraining is unusual. Instead of predicting a distribution over a hand-picked behaviour vocabulary, as earlier methods do, it uses a student and a teacher encoder and predicts an embedding that summarises all behaviour in a future time window. Over two months of online deployment, it reports KS improvements of about 2.7% and 7.1% on two loan-delinquency tasks.

Payments and fraud show the same trend. Stripe says that after adding a payments foundation model trained on tens of billions of transactions, its detection rate for card-testing attacks on large businesses rose from 59% to 97%. That figure covers a particularly sophisticated slice of attacks. Visa, which acquired Featurespace, introduced large transaction models (LTMs) and says a proof of concept caught more than five times the fraud value of a production GBT model. A footnote calls the results illustrative.

## 2. Credit data as tree models see it

A credit report does not arrive as one row per customer. A person has several accounts. Each has an open date, a limit and a balance. Every month another cell records whether the payment was on time or how many days late it was. People differ in how many accounts they have and how long their history is.

A tree model needs each customer as one fixed-length row, so people build aggregate features. Typical examples are accounts delinquent in the last six months, months since the last delinquency and card utilisation. Lenders build these features, sometimes hundreds of them, and put a GBDT on top.

This works well in practice, and research backs it up. Grinsztajn et al. (NeurIPS 2022) ran 45 datasets and concluded that tree-based models remain state of the art on medium-sized tabular data of around 10,000 samples. The 2025 TabArena benchmark also found gradient-boosted trees still strong contenders. It added that deep learning catches up with large time budgets and ensembling, and that foundation models such as TabPFN lead on small datasets.

Trees are fast, robust to missing values, and accept monotonic constraints on each variable. They also make it easy to explain a decline. Aggregation does, however, throw some information away.

![Same summary, different payment histories](/tfin-affirm-histories.png)

_Both consumers have two accounts and two late months. The summary is the same, the histories are not. (Source: [Affirm Tech Blog](https://tech.affirm.com/learning-richer-credit-representations-with-transformers-at-affirm-c774e7c1cea6))_

This is Affirm's example. Consumer A was late twice on one account five to six months ago and has paid on time since. Consumer B was late once on each of two accounts within the last two months. Fold that into "late payments in the last six months" and both score 2.

The figure alone does not tell you who is riskier. Affirm notes that it implies no risk ranking. The point is that identical summaries can hide different histories.

You could add "late payments in the last three months" and the two would separate. But you cannot turn every combination of accounts, months and delinquency stages into a feature. Someone still has to pick which combinations matter.

## 3. One account, one token

The companies here leave that aggregation to the model. Affirm turns each account on the credit report (a tradeline) into one token. So a token is a record rather than a word. The token holds the account's numeric and categorical attributes. The monthly payment statuses are encoded together with their position and folded into that account's token. Credit inquiries become tokens too.

Attention then runs across these tokens. The model can see for itself whether recent delinquency on one account tends to appear alongside high utilisation on another. There is less need to hand-build interaction features.

Revolut splits each event further, down to individual fields.

![PRAGMA tokenisation](/tfin-pragma-tokens.png)

_One card payment split into keys, values and time. The amount becomes a percentile-bucket token and the description becomes BPE tokens. (Source: [Ostroukhov et al., PRAGMA, arXiv:2604.08649](https://arxiv.org/abs/2604.08649), CC BY 4.0)_

Every field of an event becomes a key token and a value token. Numbers such as amounts map to percentile buckets learned from the training data, with a separate bucket for zero. Categories such as the merchant category code (MCC) stay as one token. Free text such as a merchant description is split with BPE. Time enters as the log of the gap since the previous event, plus calendar features such as hour, weekday and day of month.

![PRAGMA architecture](/tfin-pragma-backbone.png)

_An Event Encoder turns each event into an [EVT] embedding, and a History Encoder reads the whole sequence. Profile information goes in through a separate Profile State Encoder. (Source: [PRAGMA, arXiv:2604.08649](https://arxiv.org/abs/2604.08649), CC BY 4.0)_

The model is built from three encoders: one summarises each event, a second reads the sequence of those summaries, and a third reads profile information such as balance band and plan. The model comes in three sizes: 10 million, 100 million and 1 billion parameters.

The companies pretrained in different ways. Revolut pretrained BERT-style, hiding parts of the input and predicting them. It masks 15% of tokens, 10% of whole events, and 10% of all values of a chosen key. Each task then adds a light classification head or fine-tunes. Nubank went GPT-style, predicting the next token. Each transaction becomes tokens for the sign of the amount, an amount bucket, month, day and weekday, plus BPE tokens for the description.

In Revolut's paper, pretraining paid off. For the 100-million-parameter model, this beat the same architecture trained from scratch by 13.0% in credit-scoring PR-AUC and 1.6% in ROC-AUC.

Affirm also tried self-supervised masked pretraining. Supervised learning on repayment outcomes worked better. Several heads predicted short-term outcomes, such as whether the first payment is four or more days late (FPDQ4), alongside longer ones, such as 60 or more days delinquent within the repayment window (DQ60). Against a self-supervised baseline, the gain in FPDQ60 AUC was 25 bps for the tuned self-supervised version and 187 bps for the tuned supervised multi-head version. A footnote says less research time went into the self-supervised approach.

I think the difference comes from data scale and the mix of tasks. Revolut and Nubank train on 24 billion and over 100 billion records respectively, and have many tasks to serve. Affirm has one task, underwriting, with plenty of labels. Those two have more reason to build a shared representation in advance.

## 4. Using transformers alongside trees

Affirm placed the transformer in front of XGBoost, with the single job of turning the credit report into embeddings.

![Affirm's hybrid architecture](/tfin-affirm-hybrid.png)

_A Stage 1 transformer turns credit-report data into embeddings, and a Stage 2 AFT XGBoost model combines them with established underwriting features to produce a risk score. (Source: [Affirm Tech Blog](https://tech.affirm.com/learning-richer-credit-representations-with-transformers-at-affirm-c774e7c1cea6))_

The embeddings come from the layer just before the prediction heads. The Stage 2 XGBoost uses an accelerated failure time (AFT) objective, a survival-analysis formulation. The existing credit, merchant and user features stay in.

Affirm also tested the transformer on its own, and says the transformer-only model never got above the best XGBoost model worth putting into production.

The hybrid was compared with the production model and, alongside it, with the next XGBoost iteration that was in research at the same time. The evaluation used a one-month time holdout of loans.

![AUC change relative to production](/tfin-affirm-auc.png)

_Relative change in AUC over the production model. FPDQ60 means the first scheduled payment is 60 or more days late. (Source: [Affirm Tech Blog](https://tech.affirm.com/learning-richer-credit-representations-with-transformers-at-affirm-c774e7c1cea6))_

On FPDQ60 the next XGBoost iteration gained 2.16% and the hybrid 3.83%. Affirm's "1.8x" is the ratio of those two gains. For thin-file customers, who have a credit report but no FICO score, the gains were 4.64% and 9.84%, a 2.1x difference.

In production, Affirm started with a second-look test: the model could approve some applications the existing model would have declined. Conversion rose by 1.2 percentage points, or 3.4% in relative terms. The extra loans performed better than a comparable expansion under the previous XGBoost model, according to Affirm. It is now testing the model for all approve and decline decisions on new users, and the next iteration extends to returning users.

Revolut goes the other way: one foundation model, with only what each task needs trained on top. The simple route is a linear probe, freezing the model and fitting a logistic regression on the embeddings, which usually takes a few minutes. The heavier route fine-tunes 2 to 4% of the parameters with LoRA. The paper notes that GBDTs work well on lower-dimensional embeddings. They were not the default because each task needs its own tuning and they take longer to fit.

Nubank went a step further. A tree model cannot pass gradients back, so it cannot be trained together with a transformer. Nubank put a differentiable tabular network (DCNv2) where LightGBM was and trained it end to end with the transformer. The paper calls this joint fusion.

In the paper's comparison, swapping in the tabular network alone was roughly on par with LightGBM (+0.08%). Simply feeding the transformer embeddings into LightGBM gave +0.97%. Training the two together gave +1.25%. Most of the gain already arrives at the step Affirm took, adding embeddings.

In sales forecasting, Parafin removed the trees entirely.

![ParaFormer sales quantile forecasts](/tfin-parafin-forecasts.png)

_Twenty-four months of past sales and a 12-month forecast for a retailer, a tax preparer and a landscaping business. The shaded band is the 10th to 90th percentile. (Source: [Parafin](https://www.parafin.com/blog/paraformer-a-transformer-architecture-for-small-business-credit-underwriting))_

Before, 28 separate XGBoost models ran, one for each combination of seven quantiles and four horizons, with about 130 covariates. ParaFormer replaced them with a single Temporal Fusion Transformer. It reads 32 months of daily sales aggregated to monthly totals, and outputs 17 quantiles, from the 10th to the 90th percentile in steps of 5, for each of the next 12 months in one pass.

As noted, this is a sales forecaster used to set the loan size. Parafin writes that it was never trained on delinquency or loss outcomes and is not a loss model. A separate model handles default probability. Sellers with less than 12 months of history are routed to a lightweight, conservative model instead of the transformer.

In default models, Nubank is about the only one that removed the trees, and it replaced them with another neural network rather than ending with a transformer alone. Affirm put the transformer in front of the tree, and Revolut does not say what its baseline was.

## 5. That 2.3x

Introducing the Revolut case, NVIDIA wrote that PRAGMA is 2.3 times better at identifying credit default risk. In the paper's table, that is a 130.2% gain in PR-AUC; the same model's ROC-AUC rose 12.4%.

Both figures are in the paper, but PR-AUC starts from a floor set by the default rate. A model that guesses at random has a PR-AUC equal to the default rate. For a product with a 2% default rate, the floor is 0.02. If the old model scored 0.10, a 2.3x gain means 0.23. The same improvement looks far smaller in ROC-AUC.

The 0.10 is an assumption for illustration. Revolut reports only relative changes, saying absolute metrics are commercially sensitive. The paper also does not say what kind of model the "task-specific baselines" are. So "2.3 times better than tree models" would be wrong.

Affirm's figures are relative changes in AUC too. It does not disclose the production model's AUC, or the delinquency and loss rates of the extra approvals.

Ant International announced that Falcon TST 2.0 came first on GIFT-Eval, a time-series forecasting benchmark. That first place comes with conditions. In the paper it has the best point-forecast error (MASE) of 29 models but ranks seventh on the probabilistic metric (CRPS). Recomputed from the published result files, its MASE lead over Google's TimesFM-3 is under 0.001. Partner banks are also said to see "accuracy above 93%", with no definition of accuracy.

The announcements have something in common. Every company compared against its own previous model, and none disclosed loss rates, the number a lender cares about most.

## 6. Where tree models stay

Read closely, the same announcements also give reasons why tree models will not be pushed out soon.

On performance, Affirm's transformer-only model never beat its best XGBoost. In another post, Affirm says that when it tested pretrained tabular models such as TabPFN on its own data, boosted trees and ensembles were strongest overall. Visa's own LTM brochure says GBTs are faster to deploy, easier to interpret and perform well in low-data scenarios. Transformers win at reading sequences. Clean tables are still the trees' territory.

Latency is another constraint. Affirm had to go from input preparation to score in under a second, and optimised the serving path separately on CPU and GPU. Parafin runs a daily batch instead of real time, and says it serves hundreds of millions of daily forecasts in under an hour on a single A10 GPU.

In lending, the heaviest constraint is explanation. In the US, Regulation B requires a lender that declines an application to give specific principal reasons, and says that "failed to achieve a qualifying score" is not enough. In 2022 the CFPB added that using a complex algorithm is no exception. That circular was withdrawn in May 2025, but the Regulation B requirement itself still stands. Affirm says it built a proprietary algorithm to explain the hybrid model's decisions with the same rigour as before, without describing how it works. An aggregate feature yields a reason like "too many recent late payments" directly, but a single embedding dimension is hard to turn into a sentence like that.

Some tasks depend on links between people. Revolut itself reports that on anti-money laundering, PRAGMA (1 billion parameters, linear probe) did 47.1% worse in F0.5 than the production model. The production model uses network features across customers, while PRAGMA reads each customer's history in isolation.

Labels are a problem too. Repayment outcomes exist only for approved loans, as Affirm also points out. Nobody knows how the people declined under past policy would have done. A better representation does not remove that selection bias.

## 7. My view

The figure I found most interesting is Affirm's thin-file result (2.1x), for customers who have a credit report but no score. Aggregate features do their work when the history is long. With only one or two accounts, features like "late payments in the last six months" are often zero, and the model has little to go on. Reading each account's history directly seems to pull out a bit more signal even from short histories.

Korea has the same problem. Young people starting their careers and people who have not used loans or cards for years have thin credit files. Korean credit data is also recorded per loan and card account, so there is room to try the same approach.

For a Korean lender, I think Affirm's approach is the realistic starting point. Keep the validated GBDT and the decline-reason system, and add transformer embeddings as a handful of extra features. That keeps the scope of what must be explained to model validation teams and supervisors relatively narrow. Measure the effect separately on the thin-file segment. The evidence for this route has been building. At Nubank, feeding embeddings into LightGBM delivered most of the gain. In Sber AI Lab's 2022 CoLES paper, transaction-sequence embeddings alone (AUROC 0.87) were about as good as hand-crafted features (0.88), and the two together did best at 0.92. Pretraining a foundation model on billions of events, as Revolut did, makes sense when you have that much data and that many tasks.

The hardest part is explanation, and Korean rules require it. Article 36-2 of the Credit Information Act lets people subject to automated evaluation ask for an explanation of the result and its main criteria. The Financial Services Commission's financial-sector AI guideline, revised this June, says credit decisions should be explained mainly in terms of the key factors behind them.

Once embeddings go in as features, the answer to "why was this person declined" moves one step further away. The part Affirm chose not to publish is, I think, the part Korean lenders will run into first.

When reading announcements like these, check what the baseline model is, what the absolute figures are, what the default rate is if the metric is PR-AUC, and what happened to losses after approvals went up. Checked this way, Revolut's 2.3x is a 12.4% gain in ROC-AUC.

---

**Related posts:**

- [Sales Forecasting (1) From Tree Models to Chronos](/en/sales-forecasting-1/)
- [Sales Forecasting (2) Inside Time Attention and Group Attention](/en/sales-forecasting-2/)
- [\[FDS\] How Does Stripe Judge Payment Fraud in 100ms?](/en/fds-stripe-radar/)

## References

- [Learning Richer Credit Representations with Transformers at Affirm (Affirm Tech Blog, 2026-09-17)](https://tech.affirm.com/learning-richer-credit-representations-with-transformers-at-affirm-c774e7c1cea6)
- [Affirm launches transformer-based machine learning model for real-time underwriting (Affirm, 2026-09-17)](https://investors.affirm.com/news-releases/news-release-details/affirm-launches-transformer-based-machine-learning-model-real)
- [The Model Is Not the Modeling (Affirm Tech Blog, 2026-09-29)](https://tech.affirm.com/the-model-is-not-the-modeling-c0970512205e)
- [PRAGMA: Revolut Foundation Model (Ostroukhov et al., arXiv:2604.08649, 2026)](https://arxiv.org/abs/2604.08649)
- [Revolut case study (NVIDIA)](https://www.nvidia.com/en-us/case-studies/revolut/)
- [Revolut announces launch of dedicated AI research division, Revolut Research (Zawya, 2026-08-25)](https://www.zawya.com/en/press-release/companies-news/revolut-announces-launch-of-dedicated-ai-research-division-revolut-research-466886)
- [ParaFormer: A transformer architecture for small business credit underwriting (Parafin, 2026-05-19)](https://www.parafin.com/blog/paraformer-a-transformer-architecture-for-small-business-credit-underwriting)
- [ParaFormer in production (Parafin, 2026-06-12)](https://www.parafin.com/blog/paraformer-in-production-serving-hundreds-of-millions-of-daily-transformer-forecasts-for-small)
- [Parafin is joining Stripe (Parafin, 2026-09-30)](https://www.parafin.com/blog/parafin-is-joining-stripe)
- [Falcon-TST (Ant International, GitHub)](https://github.com/ant-intl/Falcon-TST)
- [Falcon-2.0 (arXiv:2608.13262, 2026)](https://arxiv.org/abs/2608.13262)
- [Ant International's FalconTST Model 2.0 achieves SOTA (Financial IT, 2026-08)](https://financialit.net/news/artificial-intelligence/ant-internationals-falcontst-model-20-achieves-sota-elevating)
- [GIFT-Eval results (Salesforce AI Research, GitHub)](https://github.com/SalesforceAIResearch/gift-eval)
- [Bootstrapping your behavior: a new pretraining strategy for user behavior sequence data (arXiv:2506.11053, 2025)](https://arxiv.org/abs/2506.11053)
- [Your Spending Needs Attention: Modeling Financial Habits with Transformers (Nubank, arXiv:2507.23267 v2, 2026)](https://arxiv.org/abs/2507.23267)
- [Nubank's AI-powered credit model extends access while maintaining portfolio quality (Nubank, 2026-05-07)](https://nu.com/en/newsroom/company/nubanks-ai-powered-credit-model-extends-access-while-maintaining-portfolio-quality)
- [Using AI to optimize payments performance with the Payments Intelligence Suite (Stripe, 2025-05-15)](https://stripe.com/blog/using-ai-optimize-payments-performance-payments-intelligence-suite)
- [Large transaction models (LTMs) (Visa)](https://usa.visa.com/content/dam/VCOM/regional/na/us/Solutions/documents/large-transaction-models.pdf)
- [Why do tree-based models still outperform deep learning on typical tabular data? (Grinsztajn et al., NeurIPS 2022)](https://papers.nips.cc/paper_files/paper/2022/hash/0378c7692da36807bdec87ab043cdadc-Abstract-Datasets_and_Benchmarks.html)
- [TabArena (Erickson et al., NeurIPS 2025)](https://proceedings.neurips.cc/paper_files/paper/2025/hash/1697e3fb412da11dc9488249f9e7bbc9-Abstract-Datasets_and_Benchmarks_Track.html)
- [CoLES: Contrastive Learning for Event Sequences with Self-Supervision (Babaev et al., SIGMOD 2022)](https://arxiv.org/abs/2002.08232)
- [12 CFR 1002.9 Notifications (Regulation B, CFPB)](https://www.consumerfinance.gov/rules-policy/regulations/1002/9/)
- [CFPB Circular 2022-03: Adverse action notification requirements in connection with credit decisions based on complex algorithms (CFPB)](https://www.consumerfinance.gov/compliance/circulars/circular-2022-03-adverse-action-notification-requirements-in-connection-with-credit-decisions-based-on-complex-algorithms/)
- [Withdrawal of CFPB guidance documents (Federal Register, 2025-05-12)](https://www.govinfo.gov/content/pkg/FR-2025-05-12/html/2025-08286.htm)
- [Revised AI guideline for the financial sector (Financial Services Commission, Korea, 2026-06-18)](https://fsc.go.kr/po010101/87142)

_Written on 22 October 2026 from each company's technical blog posts, papers and press releases. All performance figures are relative changes published by the companies; absolute values were not disclosed. The 0.10 in the PR-AUC example is an assumption for illustration. Nubank figures are from the revised paper (August 2026). Falcon TST 2.0's GIFT-Eval ranking is based on the published result files. Figures are reproduced from their sources; the PRAGMA figures are used under CC BY 4.0._
