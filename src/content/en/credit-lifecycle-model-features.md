---
title: "The Same 80% Utilisation Means Different Things: Feature Design for Five Credit Models, from Marketing to Collections"
description: "A customer using 80% of their limit is a demand signal to a marketing model and a burden signal to an application model. This post lays out five credit models by decision, features, labels and availability, then collects the features, labels and numbers published by Plaid, Upstart, KakaoBank, Nubank, Tala and others."
pubDatetime: 2026-11-04T01:30:00Z
koSlug: credit-lifecycle-model-features
tags:
  - financial-ai
  - credit
  - fintech
  - machine-learning
---

Take a customer who is using 80% of their card limit.

To a marketing model, this person probably needs money and is likely to respond to a loan offer. To an application model, the same person already carries a heavy debt burden. A behaviour model cares less about the 80% than about whether it was 40% three months ago, and a collections model wants to know whether any capacity to repay is left. The meaning shifts because each model is asking a different question.

There is no shortage of scorecard feature lists, but most stop at names grouped by model, and anyone trying to build from one gets stuck on formulas and timing straight away. So this post starts with what has to be settled before feature names: the decision, the label and when a value can be used. Section 6 then collects the features, labels and numbers that fintech companies and researchers have actually published, model by model.

## 1. Five models, five different decisions

The industry often calls the application score an A score, the behaviour score a B score and the collections score a C score, and adds fraud and marketing models to make five. What separates them is the decision they make and where it falls in the customer lifecycle.

| Model | When it scores | Decision | Example Y | What follows the score |
|------|------|------|------|------|
| Marketing | Before an offer | Whom to approach, with what | Conversions and volume added by the offer | Audience and incentive allocation |
| Fraud | At application or transaction | Is the person real and willing to repay | Fraud verdict confirmed later | Decline, step-up verification, review queue |
| Application (A) | Underwriting | Approval, price, limit | Arrears within 6-24 months | Cut-off, price band, limit multiplier |
| Behaviour (B) | Monthly or daily after booking | Limit changes, early warning | Arrears within 2-12 months | Increase list, decrease, monitoring |
| Collections (C) | Daily after arrears begin | Whom to contact, how | Recoveries added by the action | Call allocation, channel, instalment offer |

Fraud and application models can run at the same moment and still ask different things. One looks at willingness to repay and the other at ability, so when the two labels blur, the results of both models become hard to interpret. Marketing and collections differ in another way: as the table shows, their Y is the effect of an action rather than a prediction. Section 5 returns to this.

Lifecycle diagrams usually draw a straight line from marketing to collections, but in practice there are paths that loop back.

![Flow of the five credit models. Besides the forward arrows, collections feeds back into fraud labels and behaviour scores feed back into marketing, while declined applicants drop out of the training sample](/creditm-loop-en.svg)
_Behaviour scores return as limit increases and cross-sell lists, collections outcomes return as fraud labels, and outcomes for declined applicants are never observed._

The missing outcomes for declined applicants are a bias that follows every rebuild of an application model, and they share a root with the problem in [the Lift post](/en/risk-metrics-lift/).

## 2. Grouping features by data source shows where they overlap

Listing features model by model repeats the same feature five times, and the categories tend to mix source, content and derivation. Grouping by source puts all five models in one table.

![Table of six data sources and five models. Application models lean on forms and credit bureau data, fraud models on devices and links between accounts, behaviour and collections models on own transaction and contact history](/creditm-sources-en.svg)
_A common set-up; it varies by company and product._

Availability and cost usually follow from the source. Device signals exist the moment a session opens, while bureau data needs consent and a paid enquiry, which often makes it hard to use at the marketing stage. New applicants have no history with the lender, so the difference between application and behaviour models shows up here too. Revolut names the same boundary for PRAGMA, its model pretrained on its own transaction sequences: applicants without history and tabular bureau data sit outside it, so it is combined with a model for tabular data. ([Revolut](https://www.revolut.com/blog/post/fromresearchtorealtime/)) Regulation and platform policy also tend to apply by source, so this grouping makes the constraints in section 7 easier to apply.

## 3. One feature, different meanings

When Y changes, the direction of the same value can change too. The table shows how five common features tend to be read across the models.

| Feature | Marketing | Fraud | Application | Behaviour | Collections |
|------|------|------|------|------|------|
| High utilisation | Demand signal | Suspicious if a new account drains fast | Debt burden | Trend matters more than level | Little capacity left |
| Many recent enquiries | Shopping for money | Identity theft if clustered in time | Financial pressure | New rises suggest more debt elsewhere | Competing with other creditors |
| Night-time activity | Hint for send time | Matters only if unusual for the person | Weak signal | Matters only when habits change | Reachable hours |
| Device change | Rarely used | Strong just before a large transaction | No baseline for new customers | Watch if it coincides with a number change | Sign of losing contact |
| Early repayment | Risk of refinancing away | Suspicious if the limit is reused at once | Good sign in past history | Possible cheaper refinancing | Part payment signals intent |

This table is a starting hypothesis and not an answer. Each portfolio needs its own check of bad rates or effects by band. Even so, laying the models side by side shows that risk and response are separate axes. In a text message experiment at a Colombian bank, effects were concentrated among borrowers about six days late on average who had higher credit scores and unsecured, short-term products, while messages to borrowers who were paying on time had an effect close to zero. ([Barboni et al., working paper](https://warwick.ac.uk/fac/soc/economics/research/centres/cage/manage/publications/wp633.2022.pdf)) That is a different picture from contacting people in order of risk score.

The same reason explains why monotonic constraints cannot be shared across models. Plaid applies a monotonic relationship to each feature in its credit risk model ([Plaid](https://plaid.com/blog/how-we-built-lendscore/)), which suits a Y of arrears. Copying the same direction onto a feature like utilisation, whose reading differs between risk and demand models, would make a marketing model learn the demand signal backwards.

## 4. Defining utilisation all the way through

A feature name takes one line, but building it takes several decisions. Using utilisation as the example:

- **Formula:** balance divided by limit. Decide whether balance means statement or daily average, and whether limit means granted or available.
- **Zero denominator:** someone with a zero limit does not have 0% utilisation; the value is undefined. Keep a separate missing flag.
- **Window:** a point value, a three-month average and a three-month slope are different features. Behaviour models use the latter two more.
- **Scoring point:** use only values that had reached the system when the score was produced. The arrival date is what counts, not the statement date.
- **Limit changes:** in a month with a limit increase, the denominator moves and utilisation appears to fall. This hurts slope features in behaviour models most.

The fourth is the one most often wrong. The code below assumes a three-day arrival lag and attaches only the statement that was visible at the scoring point.

```python
import pandas as pd

def utilization_asof(apps, stmts, lag_days=3):
    # Use only statements that had already arrived at the scoring point
    stmts = stmts.assign(available_at=stmts.stmt_date + pd.Timedelta(days=lag_days))
    m = pd.merge_asof(
        apps.sort_values("scored_at"),
        stmts.sort_values("available_at"),
        left_on="scored_at", right_on="available_at", by="customer_id",
        direction="backward", tolerance=pd.Timedelta(days=60),
    )
    m["util"] = (m.balance / m.limit.where(m.limit > 0)).clip(upper=1.5)
    m["no_limit"] = m.limit.eq(0)      # zero limit: not the same as 0% utilisation
    m["no_stmt"] = m.limit.isna()      # no statement: new customer or a delay
    return m
```

Run on made-up customers, someone applying on 2 March gets the end-January statement rather than the end-February one, because the February statement arrives only on 3 March. A join on month-end would feed in the February value, and this kind of data leakage does not show in the development sample; it only costs performance in production. Nubank reports catching a similar case, where BNPL prepayments changed transaction timing and let future information in. ([nuFormer paper v3](https://arxiv.org/html/2507.23267v3))

Representative features for each model look like this in the same format. The formulas and windows are examples and vary by company.

| Model | Feature | Example formula | Available from | Watch out for |
|------|------|------|------|------|
| Marketing | Limit or rate page views | Visits in the last 14 days | Just before send | Views driven by an earlier campaign |
| Marketing | Past offer response rate | Conversions / sends, last 6 months | Just before send | Keep as missing if there were no sends |
| Fraud | Accounts per device | Accounts on the same device, last 7 days | Session start | Family and shared devices |
| Fraud | Time from first login to application | Seconds | Application submitted | Separate returning customers |
| Fraud | Applications sharing a payout account | Same account, last 30 days | Application submitted | Includes applications not yet labelled |
| Application | Bureau enquiries, last 3 months | Count, split by purpose | After bureau pull | Rate shopping versus real applications |
| Application | Income regularity | Coefficient of variation of monthly inflows | After account link | Can penalise freelancers and the self-employed |
| Application | DSR (debt service ratio) | Annual debt service / annual income | Underwriting | Depends on how income is evidenced |
| Behaviour | Utilisation slope, 3 months | Regression slope of month-end values | Monthly snapshot | Months with limit changes |
| Behaviour | Consecutive minimum payments | Run of minimum-only cycles | After due date | Customers on revolving plans |
| Behaviour | Days since salary-like inflow | Days since the last one | Daily | Weak if this is not the main account |
| Collections | Days-past-due band | 2-10, 11-25 and so on | Daily | Treat bands as different problems |
| Collections | Promise-kept rate | Kept / made | After first contact | No value on day one of arrears |
| Collections | Days since last app login | Days | Daily | Affected by app notifications |

The promise-kept rate is often named as a strong feature for predicting recoveries, but it exists only after contact, so it cannot go into a day-one allocation model. If training data aggregates values through day 30 of arrears, the day-one model ends up seeing the future.

## 5. Where labels and windows divide the models

The scoring point and the label come before any feature. Only what lies to the left of the vertical line below can be a feature.

![Scoring point, observation window and performance window for each of the five models](/creditm-windows-en.svg)
_Lengths show a common set-up and are not to scale. Actual values from published cases are in section 6._

**Roll rates set the bad definition.** If most accounts entering 30 days past due recover, a 30-day bad label carries a lot of temporary delay. These numbers are made up for illustration.

| Stage | Accounts | Share rolling from the previous stage |
|------|------|------|
| 30+ days past due | 1,000 | - |
| 60+ days | 420 | 42% |
| 90+ days | 340 | 81% |
| 120+ days | 315 | 93% |
| Charged off | 300 | 95% |

With these numbers, most accounts keep rolling from 90 days on, which supports a 90-day bad definition. Shorter products need shorter windows and thresholds, though. Plaid built its general model on 90+ days past due within 12 months, and its model for short-term products such as BNPL on 60+ days within 6 months. ([LendScore](https://plaid.com/blog/how-we-built-lendscore/), [LendScore 2](https://plaid.com/blog/instant-link-next-generation-lendscore/)) Affirm trains early indicators such as first payment 4+ days late (FPDQ4) and longer ones such as 60+ days late (DQ60) as outputs of one model. ([Affirm](https://tech.affirm.com/learning-richer-credit-representations-with-transformers-at-affirm-c774e7c1cea6)) That is one answer to labels arriving late.

**The boundary between fraud and credit is the blurriest label.** First payment default (FPD) is often used as a fraud proxy, yet the definition itself varies. Experian describes it as failing to make the initial payment and says temporary hardship must be separated from fraud. ([Experian](https://www.experian.com/blogs/insights/first-payment-default/)) An Ant Financial paper on auto loans does the opposite, labelling loans as fraud when they go more than 30 days late after three months of normal payments. The authors explain that default within three months is more easily prosecuted as fraud, so fraudsters use this pattern. ([Xu et al., AAAI-21](https://ojs.aaai.org/index.php/AAAI/article/view/16582)) A Federal Reserve white paper notes that synthetic identity fraud losses are often misclassified as credit losses and separates the two by whether the account holder is real and whether there was intent to repay. ([Federal Reserve](https://fedpaymentsimprovement.org/wp-content/uploads/frs-synthetic-identity-payments-fraud-white-paper-october-2019.pdf)) I could not find an independent study that measures how often FPD labels are wrong. Recording identity theft, synthetic identity, first-party fraud and hardship separately is safer than merging them into one label. KakaoBank's three classes of normal, fraud and victim in its sequence fraud model can be read the same way, since marking a victim's account as fraud pollutes the label. ([KakaoBank](https://tech.kakaobank.com/posts/2606-sequence-based-fds-model/))

**In marketing and collections, Y is the increment.** Suppose collections has four groups of 1,000 people each and capacity for 1,000 calls. The numbers are made up.

| Group | Repays if called | Repays if not called | Added by the call |
|------|------|------|------|
| A. Would repay anyway | 90% | 88% | 2pp |
| B. Repays if called | 60% | 35% | 25pp |
| C. Late but responsive | 30% | 10% | 20pp |
| D. Cannot repay either way | 8% | 7% | 1pp |

Calling in order of repayment probability spends the calls on group A and adds 20 payers. Calling in order of increment spends them on group B and adds 250. Marketing has the same structure, and a conversion model drifts towards giving coupons to customers who would have converted anyway. Estimating the increment requires data with randomly assigned treatment, so in these two models experiment design comes before features.

## 6. Features and labels from published cases

Disclosure is uneven. Application models are the best documented. Collections has almost no company write-ups, so papers using lenders' data are the main evidence. Korean companies tend to publish feature categories while leaving out bad definitions and algorithms. Most numbers are company claims or working paper results, and since the comparison baselines differ, they cannot be compared with each other.

| Case | Model | Inputs | Y | Published result |
|------|------|------|------|------|
| Naver Pay | Marketing | Undisclosed; randomised amounts | Conversion, payment | Live numbers undisclosed |
| Mercado Libre loan campaign | Marketing | Masked features | Conversion, volume | Top 3 deciles (26%) hold 63% of volume (similar-data example) |
| Ant GRC | Fraud | Applicant, seller, agent graph | 30+ days late after 3 months of normal payment | F1 85.56%, GCN 79.07% |
| Ant GEM | Fraud | Graph of 6 device types, 168 activity slots | Accounts judged malicious later | F1 0.8165 in week 1, 0.7344 in week 4 |
| KakaoBank FDS | Fraud | App event and transaction sequences | Normal, fraud, victim | Detection metrics undisclosed |
| Plaid LendScore | Application | 145 features, mostly cash flow | 90+ days past due in 12 months | KS +9.1% overall (benchmark undisclosed) |
| Upstart | Application | Over 2,500 | Default and prepayment by period | 41% more approvals, 33% lower APR (simulation) |
| Affirm | Application | Credit report record tokens plus tabular | FPDQ4, DQ60 and others | Relative AUC gain 3.83%, conversion +1.2pp |
| KakaoBank alternative score | Application | About 3,800 | Undisclosed | About 1.1 trillion won of extra approvals (press) |
| Mercado Crédito | Application | Sales, reputation, sector | Losses at 30+ days late | AUROC 0.76, bureau model 0.64 |
| Berg et al. | Application | 10 digital footprint variables | Sent to a collection agency | AUC 69.6%, bureau 68.3% |
| Nubank limit increases | Behaviour | Undisclosed | Non-payment, typically in 60-180 days | No numbers |
| Nubank nuFormer v3 | Credit decisions | Transaction tokens plus 291 tabular | 65 days late six months on | Relative AUC +1.25% |
| Ant limit increases | Behaviour | Spending, balances, credit grade | Balance growth after the increase | RMAE 38.30%, linear 94.10% |
| Affirm PredictPay | Behaviour | Payment and per-method history | Payment failure | AUC 0.81 to 0.88, FPDQ4 relative -2.8% |
| Tala | Collections | Repayment history, call results, app use | Repayment added by a call | Top 50% capture 90% of incremental revenue |
| Wang and Zhou | Collections | Hard data plus 5,000 terms from agent notes | Repayment within 180 days | 53.24% versus 43.14% |
| Choi et al. | Collections | Caller screen fields, daily internal score | NPV of recoveries | AI callers about 5pp lower at one year |

### Marketing: from response probability to increment

Naver Pay starts from a randomised experiment on whom to give 0, 1,000 or 2,000 won in promotions such as MyData sign-ups and partner payments. It trains Double ML on the randomised data to estimate effects per treatment (CATE) and gives larger amounts to users whose response rises most with the amount. The CPA figures of 1,429 and 1,643 won in that post are labelled by the author as a made-up example, so they should not be read as results. ([Naver Pay](https://medium.com/naverfinancial/uplift-modeling%EC%9D%84-%ED%86%B5%ED%95%9C-%EB%A7%88%EC%BC%80%ED%8C%85-%EB%B9%84%EC%9A%A9-%EC%B5%9C%EC%A0%81%ED%99%94-with-multiple-treatments-5e4e3824b9df))

Mercado Libre's loan campaign case shows the conflict that appears when thresholds rise. A binary classifier reached 42% conversion at a 0.55 threshold and 75% at 0.95, but moving only from 0.40 to 0.60 cut volume by more than a million dollars. So the team dropped the binary decision for propensity deciles and separated models for new and returning customers. Credit Origination in the title means loan marketing rather than underwriting, and the final 18.5x and 412% figures are maximums with no control group, so they are hard to take at face value. ([Mercado Libre](https://medium.com/mercadolibre-tech/how-a-data-product-approach-help-mercado-libre-build-a-credit-origination-framework-23c02a821b49)) The same company's Kairós does not use uplift scores directly either. It feeds them into an allocation problem constrained by messages per user, audience size per offer and send capacity. ([Mercado Libre Kairós](https://medium.com/mercadolibre-tech/kair%C3%B3s-powering-optimized-audience-targeting-for-next-generation-campaign-delivery-in-mercado-c196735e4cb5))

### Fraud: where resources cluster, and labels that arrive late

Ant's GEM turns an assumption into features: fraudsters have limited resources, so they cluster on devices and in time. It rebuilds a daily graph from the last seven days linking accounts to six device types such as phone number, MAC and IMSI, and stacks activity into 168 slots of seven days by 24 hours. Its F1 beat GBDT with graph features, yet the same model's F1 fell from 0.8165 in week 1 to 0.7344 in week 4, which shows how quickly fraud features age. ([Liu et al., CIKM 2018](https://arxiv.org/abs/2002.12307)) GRC, whose label appeared above, splits relationships by whether they formed within 30 days before the application, and relationships in the period just before applying carried more weight. The test set's composition, including the fraud rate, is not disclosed, so its F1 should not be read as production performance.

KakaoPay tackles late labels with a feature. It includes the recent incident rate per payment item type, which covers the gap between a new kind of incident appearing and a retrained model being deployed. It reports about 30% better detection than a static model, without saying whether that is relative or absolute. ([KakaoPay](https://tech.kakaopay.com/post/ifkakao2024-fds/)) The incident rate is built from labels, so it must count only incidents confirmed by the scoring point.

A fraud score does not have to mean a decline. KakaoBank's sequence FDS handles about 18 million inferences a day at under 20 ms on average, but instead of blocking automatically it combines scores with analyst conditions to produce a monitoring list. Plaid's Trust Index 2 picks who gets step-up verification. Its retrospective analysis says that verifying 5% of a large digital lender's users would have caught 40% of the first-party fraud its existing solution missed. That is a vendor's retrospective, and the label is undisclosed. ([Plaid](https://plaid.com/blog/plaid-protect-trust-index/))

### Application: between 7 features and 2,500

Upstart's filing shows personal loan model features growing from 23 at the end of 2014 to more than 2,500 at the end of 2025, trained on about 104 million repayment events. Its traditional comparison is a Cox model with seven inputs: FICO, DTI, loan amount, number of trade accounts, enquiries, monthly income and age of oldest account. Simulated on 2025 applicants, Upstart reports 41% more approvals and 33% lower APR, but the company built the comparison itself and this is not a live experiment. Hard criteria set by lenders, such as minimum score and DTI, come first and the model runs only on what passes, and most declines come from those criteria. ([10-K](https://www.sec.gov/Archives/edgar/data/1647639/000164763926000027/upst-20251231.htm), [Access to Credit](https://www.upstart.com/lenders/regulatory-compliance/access-to-credit-report/))

Plaid LendScore has the most detailed public design. It categorises consented account transactions, aggregates them over 30, 60 and 90-day windows and picks 145 out of hundreds of features. Cash flow features such as average monthly inflow, standard deviation of deposit balance, discretionary and essential spending shares, income to total outflow and income regularity account for about 81% of predictive power. Network features such as the number of connected lending, savings and cash advance apps account for about 19%. The model is a monotonically constrained XGBoost trained on 1.44 million tradelines, and SHAP picks the five features that lowered a score most and maps them to standard reason codes. The benchmark behind KS +9.1% is not disclosed. ([Plaid](https://plaid.com/blog/how-we-built-lendscore/))

Affirm builds embeddings with a transformer that takes credit report tradelines and enquiries as record-level tokens, then scores with XGBoost on those embeddings plus existing features. The transformer alone did not beat XGBoost; only the hybrid did. The rollout order is worth noting: it went in first as a second-look review of applications the existing system had declined, which limited risk, and is now being tested as the primary decision. The offline numbers cover approved loans only, so declined applications are missing. ([Affirm](https://tech.affirm.com/learning-richer-credit-representations-with-transformers-at-affirm-c774e7c1cea6))

In Korea, KakaoBank's decision structure is known in relative detail. According to an interview with its team leads, a financial model sets pricing and cut-offs, a strategy model gives first-round approval, and first-round declines who score well on alternative data get approved through an override. The limit adds a score-based multiplier on top of an income-based amount. ([Dailian](https://www.dailian.co.kr/news/view/1610964/)) For features, book purchases serve as the example: frequency, spend, price per book and purchases by genre over 1, 3 and 6 months form a pool, and those related to credit quality are kept. ([Hankyoreh](https://v.daum.net/v/20240205165507379)) The figures of 18 million pseudonymised linked records, about 3,800 variables and a 9.7% share of thin-file customers in the top 30% (1.8% for the standard score) come from press reports citing the company, and the bad definition and algorithm are undisclosed. ([The Fact](https://news.tf.co.kr/read/economy/2256959.htm)) Weakening bureau scores are part of the background. At a Financial Services Commission meeting in January 2026, the bureau KCB reported that 28.6% of those scored were at 950 or above and that thin-file consumers averaged about 710 at the end of 2024. ([FSC](https://www.fsc.go.kr/no010101/86084))

Naver Pay applies a different kind of constraint. Its score uses Naver Pay activity and MyData assets, plus sales, delivery and enquiry response speed and reviews for business owners, and the company says it counts only in the applicant's favour and never against them. Unlike monotonic constraints on individual features, this is a policy constraint on the whole score. The 13.57pp improvement is a simulation with an unnamed metric. ([Naver](https://navercorp.com/media/pressReleasesDetail?seq=31685))

Two academic studies show the power and limits of cheap features. Berg et al. analysed about 270,000 pay-later purchases at a German online shop. Ten variables, including device type, operating system, traffic channel, purchase time and email host, reached an AUC of 69.6%, close to the bureau score's 68.3%, and 73.6% combined. Default was 1.07% for iOS users and 1.79% for Android. The sample was already screened by the company for high predicted default, and the authors themselves note that behaviour may change once such features are known to be used. ([NBER](https://www.nber.org/system/files/working_papers/w24551/w24551.pdf)) In an analysis of 7,300 sellers at Mercado Crédito in Argentina, logistic regression on bureau data alone had an AUROC of 0.64, against 0.76 for the internal score built on platform data. The data is from 2017, and one co-author works at Mercado Libre. ([BIS](https://www.bis.org/publications/working-paper-779-bigtech-and-changing-structure-financial-intermediation.pdf))

### Behaviour: limit models have two Ys

Nubank models card limit increases as time to default. It treats non-payment within a set window (typically 60 to 180 days) as a survival curve and refreshes only the curve calibration often, leaving the ranking model in place. Ranking and calibration run on different refresh cycles, though features and numbers are not published. ([Nubank](https://building.nu.com/how-nubank-models-risk-for-smarter-scalable-credit-limit-increases/)) Nubank's newsroom says its limit increase models have reached generation 17 and its new customer models generation 10. ([Nubank newsroom](https://nu.com/en/newsroom/company/nubanks-ai-powered-credit-model-extends-access-while-maintaining-portfolio-quality)) It is worth noting that limit models have gone through more generations. Version 3 of the nuFormer paper uses 65 days late six months on as its label, combines transaction tokens with 291 tabular features for a relative AUC gain of 1.25%, and admits that late labels prevented A/B testing every variant. It does not say which credit decision the model serves, and version 1 of the paper describes the same sample and number as a recommendation problem, so the versions need telling apart. ([arXiv](https://arxiv.org/html/2507.23267v3))

Limit decisions need response as well as risk. Ant's limit increase paper sets Y to balance growth after an increase rather than default. It randomly assigned increase amounts within six segments built from credit grade and demand, with features such as default probability, credit grade, average monthly spend over 3 and 6 months, maximum monthly spend over 12 months and past balances. The balance response error (RMAE) was 94.10% for a linear model, 47.58% for a single GBDT and 38.30% for GBDT encoding with a log transform of the treatment. There is no online result, and a footnote says the data does not represent the actual business. ([Miao et al.](https://arxiv.org/abs/2007.05188)) How much borrowing follows an increase can be seen in an experiment at a Turkish bank that randomly withheld increases for nine months among 45,307 pre-approved customers: participants borrowed 11 cents per dollar of new limit in the first quarter and 28 cents by the third year. ([Aydin, AER](https://www.aeaweb.org/articles?id=10.1257/aer.20191178)) Researchers at Rappi proposed reinforcement learning with a reward based on the difference in expected profit including provisions. They note that online exploration is hard because random limit changes hurt customer experience and the reward appears only three months later, and their results are synthetic. ([Alfonso-Sánchez et al.](https://arxiv.org/abs/2306.15585))

Scores are not the only lever on arrears. Affirm's PredictPay is a batch XGBoost model that predicts payment failure and reorders default AutoPay methods. Version 2 added recent success and failure patterns and per-method history, raising ROC-AUC from 0.81 to 0.88. An experiment in June to August 2026 showed FPDQ4 down 2.8% and AutoPay payment failures down 7.1% in relative terms against version 1. ([Affirm](https://tech.affirm.com/predictpay-from-hackathon-idea-to-smarter-payments-at-scale-a8dc7c3837db)) On operations, Merpay describes automating about 50 monthly release tasks for the several models behind its monthly limit refresh. It covers no features or labels. ([Mercari](https://engineering.mercari.com/blog/entry/20241219-e9ad9948c2/))

### Collections: few company write-ups, some real experiments

Tala's post is a rare company description of a collections model. It trains an S-Learner on repayment history, past call results and app interaction features, and the training data itself comes from an experiment that randomised calls. It ranks by revenue uplift, which multiplies probability uplift by debt and expected repayment. After deployment, a random 5% are always called and another 5% never called, so the real effect stays visible. On the test set, calling the top 10% earned more than half of the incremental revenue from calling everyone, and the top 50% earned 90%. Sample, costs and post-deployment numbers are not given. ([Tala](https://tala.co/blog/2021/01/14/helping-late-borrowers-repay-with-uplift-modeling/))

The most concrete evidence is a randomised experiment at a Dutch collection agency. For 180 days, 7,839 borrowers had their call targets picked either by human managers or by an algorithm, with the same agents making the calls on both sides. The algorithm used hard data such as debt amount and age, along with call counts, website logins and the top 5,000 terms from agent notes, and estimated call effects with day-by-day GBDTs and a meta-learner to choose high-effect calls. Repayment was 53.24% against 43.14%, with fewer calls on average, 3.50 against 3.82. ([Wang and Zhou, working paper](https://ncbankruptcyexpert.com/sites/default/files/2024-07/artificial_intelligence_and_debt_collection_evidence_from_a_field_experiment_compressed_0.pdf))

Another result looks like the opposite. An NBER paper on over 22 million cases at a Chinese online consumer lender finds the NPV of recoveries for cases handled by AI callers 9pp lower about a month into arrears and still about 5pp lower at one year. The question differs, though: the Dutch experiment has an algorithm choosing whom to call, while here AI makes the call. For feature design, the internal score is refreshed daily with the previous day's call results, and strategy changes across the bands of 2-10, 11-25, 26-59, 60-84 and 85+ days. An internal survey found that the filter most used by productive callers was the time of last app login. ([Choi et al., NBER](https://www.nber.org/system/files/working_papers/w33669/w33669.pdf))

Sometimes the action matters more than the score. At a digital lender in sub-Saharan Africa, offering four instalments to borrowers 90 to 150 days late raised the share making any repayment by 9.3pp from a control level of 16.2%. A notice that repaying in full would restore loan eligibility was not significant alone, and the group receiving both showed no significant effect on full repayment. ([Burlando et al., working paper](https://silviaprina.com/files/ungated-papers/working-papers/BKPW_delinquent_digital_borrowers.pdf)) A study of point-of-sale loans at a German bank uses the assignment of the first call's weekday to show larger call effects for borrowers who are harder to reach, which suggests that repeatedly calling those who pick up can be a losing routine. This is the 2021 working paper; I did not check the published journal version. ([Laudenbach et al.](https://www.ifo.de/DocDL/cesifo1_wp7295.pdf))

## 7. Features that rules take away

Features in published papers often cannot be copied. Ant's SemiGNN built graphs from app logins, nicknames and address words, raising arrears prediction AUC from 0.753 to 0.807, but these would be hard to bring to a lending app in Korea or the US today. ([Wang et al.](https://arxiv.org/abs/2003.01171)) The same goes for the contacts and app lists once used in digital lending in emerging markets.

| Region | Rule | Effect on feature design |
|------|------|------|
| Android apps | [Google Play Financial Services policy](https://support.google.com/googleplay/android-developer/answer/9876821) | Personal loan apps cannot use contacts, photo and video, fine location, phone number or installed app list permissions |
| US | [Regulation B §1002.9(b)(2)](https://www.consumerfinance.gov/rules-policy/regulations/1002/9/) | Reasons for adverse action must be specific; failing to reach a qualifying score is not enough |
| US | [2026 Regulation B amendment](https://public-inspection.federalregister.gov/2026-07804.pdf) | The effects test was removed from 21 July 2026, with litigation under way. The prohibited bases such as sex remain |
| Korea | [Credit Information Act, Art. 36-2](https://elaw.klri.re.kr/kor_service/lawViewContent.do?hseq=70283) (February 2024 text) | People can ask for the result, main criteria and an outline of the base data of automated assessments, and can ask for correction and recalculation |
| Korea | [FSC reform, December 2018](https://www.fsc.go.kr/no010101/73473) | From January 2019, the threshold for reflecting short-term arrears moved from 100,000 won and 5 business days to 300,000 won and 30 days, so arrears features differ before and after |
| Korea | [Enforcement Decree, Art. 28-3](https://www.law.go.kr/lumLsLinkPop.do?lspttninfSeq=164679&chrClsCd=010202) | MyData transfer requests cover tax, social insurance and telecom payment data, among others |
| China | [Measures on credit reporting business](https://www.gov.cn/gongbao/content/2021/content_5654782.htm) (in force 2022) | Financial institutions cannot get credit reporting services from unlicensed firms, factors unrelated to credit cannot be evaluation criteria, and anti-fraud products need fraud determination standards |
| EU | [AI Act, Annex III](https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3) | Credit scoring is high risk and fraud detection is excepted. High-risk duties apply from [2 December 2027](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-113) |

CFPB circulars 2022-03 and 2023-03 on adverse action for complex algorithms were [withdrawn in May 2025](https://public-inspection.federalregister.gov/2025-08286.pdf), so the regulation text above is the better citation for the explanation duty. Application feature lists also sometimes include sex without comment. Features that are prohibited bases or that need a proxy check should be flagged at the candidate stage so they can be explained later. None of this is legal advice, and I could not check the latest text of every Korean provision at the time of writing.

## 8. My view

Across these cases, the competition over features is concentrated in application models, while the larger numbers came from further down the lifecycle. The 10pp repayment gap in the Dutch experiment and Affirm's reordering of payment methods came from changing how actions are chosen, not from adding hundreds of features. Countries, products and baselines differ, so the numbers cannot be compared directly, and it is possible that only successful collections experiments get written up. Even so, it seems worth asking which has more effect: a little more AUC on the application model, or a randomised control group in collections.

If I had to set an order of repairs, the label dictionary would come first. Without agreement on how to split fraud from credit losses and how to set bad definitions and windows by product, models will not reconcile however good the features are. Timing comes next, and simply writing each feature's arrival date into the feature dictionary prevents much of the leakage. Adding features comes after that.

I would keep one feature dictionary but write the interpretation separately per model, because five models can share utilisation's formula but not its direction. When the people building marketing and application models sit in different organisations, there is less chance than you might expect of ever lining these up.

The Korean cases leave something to be desired. Feature categories for alternative scores are fairly open, but bad definitions, windows and baselines are often missing, which makes results hard to verify from outside, and I found no technical write-ups on arrears prediction or collections models. Disclosure at the level KakaoBank and KakaoPay have shown for fraud would raise the bar for the whole industry.

---

**Related posts:**

- [Same AUC, Higher KS: KS and AUC Come From the Same Curve](/en/risk-metrics-ks-auc/)
- [Why a Rule With Lift 2.4 on Its Own Fades Inside a Strategy: Four Ways to Measure Lift](/en/risk-metrics-lift/)
- [Where Transformers Fit in Credit Models: Affirm, Revolut, Parafin and Ant](/en/transformers-in-credit/)

## References

**Marketing**

- [Marketing cost optimisation through uplift modelling (Naver Pay, 2024, in Korean)](https://medium.com/naverfinancial/uplift-modeling%EC%9D%84-%ED%86%B5%ED%95%9C-%EB%A7%88%EC%BC%80%ED%8C%85-%EB%B9%84%EC%9A%A9-%EC%B5%9C%EC%A0%81%ED%99%94-with-multiple-treatments-5e4e3824b9df)
- [How a Data Product approach helps Mercado Libre build a Credit Origination Framework (Mercado Libre, 2025)](https://medium.com/mercadolibre-tech/how-a-data-product-approach-help-mercado-libre-build-a-credit-origination-framework-23c02a821b49)
- [Kairós: Powering optimized audience targeting (Mercado Libre, 2025)](https://medium.com/mercadolibre-tech/kair%C3%B3s-powering-optimized-audience-targeting-for-next-generation-campaign-delivery-in-mercado-c196735e4cb5)

**Fraud**

- [Towards Consumer Loan Fraud Detection (Xu et al., AAAI-21)](https://ojs.aaai.org/index.php/AAAI/article/view/16582)
- [Heterogeneous Graph Neural Networks for Malicious Account Detection (Liu et al., CIKM 2018)](https://arxiv.org/abs/2002.12307)
- [A Semi-supervised Graph Attentive Network for Financial Fraud Detection (Wang et al., 2020)](https://arxiv.org/abs/2003.01171)
- [Sequence-based FDS model (KakaoBank, 2026, in Korean)](https://tech.kakaobank.com/posts/2606-sequence-based-fds-model/)
- [Continuously improving ML models in FDS (KakaoPay, 2024, in Korean)](https://tech.kakaopay.com/post/ifkakao2024-fds/)
- [Introducing Ti2 (Plaid, 2025)](https://plaid.com/blog/plaid-protect-trust-index/)
- [Detecting Synthetic Identity Fraud in the U.S. Payment System (Federal Reserve, 2019)](https://fedpaymentsimprovement.org/wp-content/uploads/frs-synthetic-identity-payments-fraud-white-paper-october-2019.pdf)
- [What Lenders Need to Know About First Payment Default (Experian, updated 2026)](https://www.experian.com/blogs/insights/first-payment-default/)

**Application**

- [How we built LendScore (Plaid, 2025)](https://plaid.com/blog/how-we-built-lendscore/)
- [Instant Link & LendScore 2 (Plaid, 2026)](https://plaid.com/blog/instant-link-next-generation-lendscore/)
- [Upstart FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/1647639/000164763926000027/upst-20251231.htm)
- [Upstart 2025 Access to Credit Report](https://www.upstart.com/lenders/regulatory-compliance/access-to-credit-report/)
- [Learning Richer Credit Representations with Transformers at Affirm (Affirm, 2026)](https://tech.affirm.com/learning-richer-credit-representations-with-transformers-at-affirm-c774e7c1cea6)
- [From research to real time (Revolut, 2026)](https://www.revolut.com/blog/post/fromresearchtorealtime/)
- [KakaoBank alternative credit interview (Dailian, 2026, in Korean)](https://www.dailian.co.kr/news/view/1610964/)
- [KakaoBank alternative credit interview (Hankyoreh, 2024, in Korean)](https://v.daum.net/v/20240205165507379)
- [Kakaobank Score report (The Fact, 2025, in Korean)](https://news.tf.co.kr/read/economy/2256959.htm)
- [Naver Pay Score press release (Naver, 2024, in Korean)](https://navercorp.com/media/pressReleasesDetail?seq=31685)
- [On the Rise of FinTechs: Credit Scoring Using Digital Footprints (Berg et al., NBER WP 24551)](https://www.nber.org/system/files/working_papers/w24551/w24551.pdf)
- [BigTech and the changing structure of financial intermediation (Frost et al., BIS WP 779)](https://www.bis.org/publications/working-paper-779-bigtech-and-changing-structure-financial-intermediation.pdf)
- [Credit scoring reform task force release (FSC, 2026, in Korean)](https://www.fsc.go.kr/no010101/86084)

**Behaviour**

- [How Nubank models risk for smarter, scalable credit limit increases (Nubank, 2025)](https://building.nu.com/how-nubank-models-risk-for-smarter-scalable-credit-limit-increases/)
- [Nubank's AI-powered credit model (Nubank newsroom, 2026)](https://nu.com/en/newsroom/company/nubanks-ai-powered-credit-model-extends-access-while-maintaining-portfolio-quality)
- [nuFormer paper (arXiv 2507.23267 v3)](https://arxiv.org/html/2507.23267v3)
- [Intelligent Credit Limit Management in Consumer Loans Based on Causal Inference (Miao et al., 2020)](https://arxiv.org/abs/2007.05188)
- [Consumption Response to Credit Expansions (Aydin, AER 2022)](https://www.aeaweb.org/articles?id=10.1257/aer.20191178)
- [Optimizing Credit Limit Adjustments Under Adversarial Goals Using Reinforcement Learning (Alfonso-Sánchez et al.)](https://arxiv.org/abs/2306.15585)
- [PredictPay (Affirm, 2026)](https://tech.affirm.com/predictpay-from-hackathon-idea-to-smarter-payments-at-scale-a8dc7c3837db)
- [Running ML systems at Merpay (Mercari, 2024, in Japanese)](https://engineering.mercari.com/blog/entry/20241219-e9ad9948c2/)

**Collections**

- [Helping late borrowers repay with uplift modeling (Tala, 2021)](https://tala.co/blog/2021/01/14/helping-late-borrowers-repay-with-uplift-modeling/)
- [Artificial Intelligence and Debt Collection (Wang and Zhou, 2024 working paper)](https://ncbankruptcyexpert.com/sites/default/files/2024-07/artificial_intelligence_and_debt_collection_evidence_from_a_field_experiment_compressed_0.pdf)
- [How Good is AI at Twisting Arms? (Choi et al., NBER WP 33669)](https://www.nber.org/system/files/working_papers/w33669/w33669.pdf)
- [Behavioral Messages and Debt Repayment (Barboni et al., CAGE WP 633)](https://warwick.ac.uk/fac/soc/economics/research/centres/cage/manage/publications/wp633.2022.pdf)
- [From Default to Second Chances (Burlando et al., 2026 working paper)](https://silviaprina.com/files/ungated-papers/working-papers/BKPW_delinquent_digital_borrowers.pdf)
- [Personal Communication in an Automated World (Laudenbach et al., CESifo WP 7295)](https://www.ifo.de/DocDL/cesifo1_wp7295.pdf)

**Rules**

- [Google Play Financial Services policy](https://support.google.com/googleplay/android-developer/answer/9876821)
- [Regulation B §1002.9](https://www.consumerfinance.gov/rules-policy/regulations/1002/9/), [2026 final rule](https://public-inspection.federalregister.gov/2026-07804.pdf), [CFPB withdrawal notice](https://public-inspection.federalregister.gov/2025-08286.pdf)
- [Credit Information Act (February 2024 text)](https://elaw.klri.re.kr/kor_service/lawViewContent.do?hseq=70283), [Enforcement Decree Art. 28-3](https://www.law.go.kr/lumLsLinkPop.do?lspttninfSeq=164679&chrClsCd=010202), [FSC release, December 2018](https://www.fsc.go.kr/no010101/73473)
- [Measures on credit reporting business (People's Bank of China, 2021)](https://www.gov.cn/gongbao/content/2021/content_5654782.htm)
- [EU AI Act Annex III](https://ai-act-service-desk.ec.europa.eu/en/ai-act/annex-3), [Article 113](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-113)

_Written on 4 November 2026 from public sources. Company numbers are company claims or press reports, and paper numbers follow the stated version. The roll rate and collections group numbers and the customers in the code example are made up for illustration. This is not legal advice, and rules are as checked in the stated versions, so check the latest text before applying them._
