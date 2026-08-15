---
title: "[FDS] How Does Stripe Judge Payment Fraud in 100ms?"
description: "Where do machine learning and deep learning actually get used in financial AI? Fraud detection in practice, through the Stripe Radar case."
pubDatetime: 2026-05-24T03:00:00Z
koSlug: fds-stripe-radar
tags:
  - fds
  - financial-ai
  - machine-learning
  - fraud-detection
  - stripe
---

After a lecture on financial AI agents recently, one of the topics that drew the most questions afterwards was FDS — fraud detection systems.

More students than I expected asked things like: where is machine learning actually used in financial AI? Is fraud detection just rules? Does deep learning really get used in production?

There is not much material explaining FDS from a practitioner's angle. Credit scoring, investing and LLM agents get plenty of writing; payment fraud detection, which touches a financial service's P&L and its customer experience at the same time, is comparatively less covered.

So this piece works through how Stripe uses machine learning for fraud detection, centred on Stripe Radar — older material, but still a good reference. Stripe's guide was updated in December 2021 and describes how Radar uses Stripe network data to detect online card payment fraud. ([Stripe](https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection))

Rather than covering all of payment fraud, this focuses on how an FDS judges risk at the moment of an online payment. Fraud types by payment method, account takeover, refund abuse, promotion abuse and mule accounts can be separate pieces later.

## FDS is not a simple "fraud or not" classification problem

The usual first impression of FDS goes like this.

> Feed in transaction data, classify 1 for fraud and 0 for legitimate — isn't that it?

Technically, yes. In practice, that is far too simple.

The real difficulty is threefold.

First, fraud is extremely rare. Most transactions are legitimate and fraudulent ones are a tiny fraction. The model has to find a very small anomalous signal inside an enormous mass of normal traffic.

Second, the judgement has to be real time. Saying "this looks like fraud" a few minutes after the payment came in is already too late. Immediately after the user presses pay, one of approve, decline, step-up authentication or manual review has to be chosen.

Third, blocking fraud too well is also a problem. Wrongly blocking a good customer destroys revenue and worsens the experience. Stripe likewise describes the trade-off between false negatives — missing fraud — and false positives — wrongly blocking legitimate customers — as the core issue. ([Stripe](https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection))

![The trade-off between missing fraud (false negatives) and blocking good customers (false positives)](https://images.stripeassets.com/3sz5ney9ml0h/6EGHWdjWNXhUSwCX4EMxoA/451763adf6ece21f54068e9c6d935b5e/false_positives.png?w=1600&q=80)

_The trade-off between false negatives and false positives. (Source: Stripe)_

So FDS is not a question of model accuracy alone. It is closer to a decisioning system optimising fraud loss, authorisation rate, customer friction, operating cost, review headcount and chargeback risk simultaneously.

## Radar's real advantage is data, not the model

The first thing to look at with Stripe Radar is not the model architecture but the data structure.

Stripe is connected to enormous numbers of businesses, banks and payment networks. According to Stripe's own material, Radar uses payment data collected automatically across the whole Stripe network, and 90% of cards used on the Stripe network have been seen at least once before. ([Stripe](https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection))

Why does that matter?

Looking at one merchant, a card can appear to be showing up for the first time. Across the whole Stripe network, that card may already have been used many times at other merchants. Which IP tried multiple cards, which card is suddenly being used in several countries, which email/device/card combination looks strange — these patterns are far more visible at network scale.

Stripe's advantage, then, is not simply a good AI model. It is the ability to turn payment behaviour across many merchants into a single body of network knowledge.

That is an important point in financial AI generally. A model runs on top of data. In FDS especially, the gap between seeing only transactions inside your own service and seeing behavioural patterns across a whole network is very large.

## Machine learning catches subtler patterns than rules

![A model branching payment data across features to estimate fraud probability](https://images.stripeassets.com/3sz5ney9ml0h/2uRUqDlYeKaqWvi8lxLBCs/6511c71884d426a1b84e8091da2fb15a/decision_tree.png?w=1600&q=80)

_A model estimating fraud probability by branching on features. (Source: Stripe)_

Traditional fraud detection often starts rule-based. Something like:

- block foreign IPs
- block multiple payments on the same card in a short window
- review cards from certain countries
- step up authentication on large payments

Rules are easy to understand and directly controllable by an operator. The problem is that they can be too coarse.

Not every foreign IP is fraud — it may be a legitimate customer travelling. Not every large payment is risky; it may be a very good customer.

Stripe likewise notes that hardcoded rules can block legitimate transactions, and that machine learning can consider many signals together and catch subtler patterns. ([Stripe](https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection))

The important concept here is the feature. An FDS model does not look at the payment amount alone. It looks at signals such as:

- how many times the same card has been attempted in the last few minutes
- how many different cards have been used from the same IP
- whether the same device is linked to multiple accounts
- how many countries a card has been used in over the last 24 hours
- how far the card's issuing country is from the connecting country
- whether authorisation failure rates suddenly spiked at a given merchant

Stripe's guide likewise says Radar uses hundreds of features, a substantial share of them aggregate features computed across the whole Stripe network. ([Stripe](https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection))

In practical terms, FDS performance is not decided by the model algorithm alone. How fast you can build good features, compute them reliably in real time, and wire them into the operating environment matters far more.

## Where does deep learning come in? Representation learning

A common follow-up: is deep learning used in FDS?

It is. But not in the sense that switching to deep learning suddenly catches all the fraud.

Deep learning's advantage in FDS is learning complex non-linear relationships and representing categorical information — cards, merchants, banks, countries, devices — more richly. Stripe likewise says that having large-scale network data lets it use more complex approaches such as neural networks and deep learning. ([Stripe](https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection))

One concept that comes up frequently here is embeddings.

Payment data has a great many categorical variables: merchant ID, issuing bank, country, card BIN, email domain, device, day of week, payment method. These are hard to compare as simple magnitudes.

An embedding places such categorical values in a vector space. Merchants, countries, banks and payment environments with similar transaction patterns end up in similar positions. Stripe likewise describes using embeddings for a range of categorical features including merchant, issuing bank, user country and day of week. ([Stripe](https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection))

A caution, though. Embeddings are not all of deep learning, and embeddings alone do not solve fraud detection. More precisely, they are one of several ways deep learning gets used in FDS.

If one merchant's transaction patterns resemble another's, the model can understand the two as similar contexts rather than as entirely separate IDs. Where a risk pattern has been observed in a particular region or merchant category, it becomes more likely to generalise to other areas with similar transaction structure.

So deep learning's role is less "memorising fraud" than converting complex payment context into a better representation and computing risk on top of that.

## Labels in FDS are dirtier than you would think

Beginners usually assume:

> Fraudulent transactions carry a fraud label and legitimate ones carry a normal label.

Real FDS labels are much messier. Payment fraud labels typically arrive through:

- cardholder disputes
- chargebacks
- refund history
- manual review outcomes
- customer reports
- risk signals from card networks or issuers
- internal investigations

The problem is that these labels arrive late, are incomplete, and are shaped by operating policy.

One issue matters especially. For blocked transactions you cannot know whether they were actually fraud. Having stopped the payment, you cannot observe whether it would have produced a chargeback or turned out to be a good customer.

Stripe likewise explains that computing precision-recall or ROC curves in production is much more complex than on a validation set, and that counterfactual analysis is needed to estimate what would have happened to blocked payments. ([Stripe](https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection))

This is what makes FDS harder than an ordinary classification problem. Building the model requires fraud labels, and the moment the model intervenes some labels become unobservable. So FDS evaluation is far more complex than a test set AUC.

## A good FDS is a decisioning layer, not one model

A particularly important part of the Stripe case is that the model score is not the final judgement.

The model computes a risk score per transaction. What happens next varies with business circumstances.

- low risk: approve
- high risk: block
- ambiguous: step-up authentication
- more ambiguous: manual review
- specific merchant conditions: custom rules

![The Stripe Radar dashboard](https://images.stripeassets.com/3sz5ney9ml0h/68LpBGLVwySvUPFkPOwniS/033bc7a45effdd2b9f3f7ce77a42c5f4/dashboard.jpg?w=1600&q=80)

_Radar, with rules, step-up authentication and review layered on top of the model score. (Source: Stripe)_

Radar lets users adjust risk thresholds and use custom rules and manual review. Stripe's guide likewise describes rules, interventions and manual review as tools that can shift a user's precision-recall curve favourably. ([Stripe](https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection))

This part matters a great deal in practice. Building a good FDS model is not only raising AUC by 0.01. It requires designing the policy that decides which transactions get blocked outright, which get routed to step-up authentication, which go to the review team, and which pass for the sake of customer experience.

This is exactly where data science meets risk operations.

## Rules are not obsolete — they are the operator's control surface

One misconception to avoid: that rule-based systems are old and machine learning is modern. Rules remain important in real FDS, typically doing this work:

- blocking clear known-bad patterns
- emergency response to a new attack
- encoding conditions that policy requires blocking
- reflecting a specific merchant's business rules
- routing the review queue
- running allowlists and blocklists
- covering new patterns the model has not learned yet

Rules are not a downgrade from ML. They are closer to the device by which an operator controls the system.

A good FDS is not a system that eliminates rules but one that runs rules and models together without conflict. The model computes complex risk; rules encode business policy and operational judgement.

## FDS evaluation does not end at AUC

Learning machine learning, you see a lot of AUC, accuracy, precision and recall. Those matter in FDS too. In practice, though, you have to look somewhat differently.

![An example ROC curve](https://images.stripeassets.com/3sz5ney9ml0h/79kCPFqbbNSYI3nx4bOeJf/9a7068f7b94b788daad28083dba91127/roc_curve.png?w=1600&q=80)

_A better model catches more fraud at the same false positive rate. (Source: Stripe)_

A better AUC does not immediately make a better model. In real operations these questions can matter more.

- does it catch more fraud at the same false positive rate?
- is precision sufficient within a volume the review team can absorb?
- has the block rate suddenly climbed?
- has the authorisation rate fallen?
- is anything being blocked excessively at particular merchants or in particular countries?
- has the chargeback rate come down?
- how much has customer friction increased?

Stripe likewise describes looking at precision-recall curves, ROC curves and AUC together in model evaluation, and monitoring shifts in score distribution when a model changes. When deploying a new model in particular, it works to keep the share of transactions above threshold stable so as not to conflict with existing merchant blocking policy. ([Stripe](https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection))

That is the core of FDS in practice. Model performance has to be judged not by prediction quality alone but by whether it produces stably better decisions within operating policy.

## Deployment and operations matter as much as the model

FDS is not a lab model. Building a good model is not the end. It has to run at low latency inside a real payment API flow. Features used in training have to be computable in real time. A new model that looks better overall is still a problem if it suddenly raises the block rate at a particular merchant.

Stripe's guide highlights two production challenges: every feature has to be computed in real time for each new payment, and score distributions have to be compared so a new model does not shock existing operating policy. ([Stripe](https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection))

That is an important lesson for financial AI. "Model performance improved" is not sufficient from an operational perspective. These questions need answers too.

- how does the authorisation rate change?
- does blocking of good customers increase?
- is there an adverse change for a particular merchant or segment?
- can the review volume be absorbed?
- did chargebacks come down?
- does the score distribution conflict with existing policy?

A good FDS is not a modelling project but an operating system that is continuously deployed, monitored and retrained.

## What financial AI can take from this

Four lessons from the Radar case.

First, FDS is decisioning rather than classification. The model predicts a fraud probability, but the business has to decide approve, block, authenticate or review on top of that score.

Second, data network effects matter enormously. Patterns invisible in one merchant's data are visible across a network. In FDS, data scale and connectivity matter as much as model architecture.

Third, deep learning is a representation-learning tool, not magic. Embeddings can help represent a large number of categorical payment signals in a better form. But that is one part of the whole system. FDS performance comes from model architecture, features, label quality, real-time infrastructure and operating policy meshing together.

Fourth, real FDS is MLOps combined with risk operations. You retrain often, monitor score distributions, adjust thresholds, and run rules and review alongside.

## Closing

FDS is an excellent topic for anyone learning financial AI, because nearly every real problem in machine learning is present in it.

Sparse labels, real-time inference, imbalanced data, precision-recall trade-offs, customer friction, explainability, model drift, retraining, rule engines, manual review, and business P&L — all connected.

Understanding FDS makes clear that financial AI is not simply about building good models. A good financial AI system requires the prediction model, the data infrastructure, the decision policy and the operational feedback loop to be designed together.

That is what makes the Radar case interesting. Judging fraud in 100ms does not mean using a fast model. Compressed into that 100ms are a great deal of network data, real-time features, ML and DL models, rules, thresholds, step-up authentication, review strategy and deployment stability.

FDS is one of the most practical faces of financial AI.

---

Source: [A primer on machine learning for fraud protection — Stripe](https://stripe.com/in/guides/primer-on-machine-learning-for-fraud-protection)

**Related posts:**

- [Agentic Engineering in Financial AI](/en/agentic-engineering-in-finance/)
- [The Age of AI Paying: Alipay's AI付 and AI收](/en/alipay-ai-payment-era/)
