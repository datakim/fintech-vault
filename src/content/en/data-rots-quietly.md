---
title: "Nobody Touched a Line of Code and the System Broke: The Paths by Which Data Quietly Rots"
description: "The types check out, the values sit in range, and only the model goes strange. A price column that started recording dollars instead of won, a RAG system answering confidently from a two-year-old research report, and a feedback loop where the model's own misreading hardens into ground truth."
pubDatetime: 2026-08-15T04:00:00Z
koSlug: data-rots-quietly
tags:
  - ai-engineering
  - llm
  - engineering
  - machine-learning
---

[Last time](/en/ai-system-fails-outside-model/) the argument was that most AI failures start outside the model. Ranked by frequency, first place went to input data quality, and four out of five incidents sat outside the model entirely.

So what exactly happens out there? That is this post. In particular, the paths by which **a system gets worse without a single line of code changing.** Nothing was deployed, the error logs are clean, the dashboards are green, and only the output has gone strange.

## 1. The shell stays identical, the contents change

Data breaks in two broad ways, and the difficulty gap between them is enormous.

![Structural change versus semantic change](/book2-drift-en.svg)

_The first one trips the defences. The second walks straight through._

**Schema drift** is a change in the structure of the data. A column renamed from `headline` to `title`, an integer that becomes a string, a date format that shifts. This fails loudly. The pipeline throws, schema validation catches it, an alarm goes off. Annoying, but catchable.

The problem is **semantic drift**. The shell is perfectly unchanged while the business meaning inside it moves. Same type, same name, not null. No validation catches it. And it means something different.

### When dollars start arriving in a column that recorded won

Currency units are the easiest case to grasp.

![Every check passes, and only the model goes mad](/book2-price-en.svg)

_Type is right, value is positive, and only the world the model sees has completely changed._

In an e-commerce system the `price` column was always a Float and always positive. Then the finance team, preparing for a global launch, starts writing dollars where it used to write won. There was a separate `currency` column, but it was in neither the model features nor the monitoring.

```
until yesterday  {"price": 15000.0, "currency": "KRW"}
from today       {"price": 11.50,   "currency": "USD"}
```

The type check passes — it is a Float. The value check passes — it is greater than zero. A recommender trained entirely on won sees 11.5 arrive and reads it as **"people have suddenly started buying only very cheap things."** High-value recommendations vanish and only cheap items get pushed.

The one hope here is a distribution check. If the mean drops from 15,000 to 11.5, an alarm may well fire. But even that is conditional. **If won and dollars are mixed and the ratio shifts gradually**, the mean slides 15,000 → 14,000 → 12,000 → 8,000 and never crosses the threshold. Slow contamination is far harder to catch than sudden contamination.

### The button moved, and the meaning of the data changed

This one is nastier, because what changed was not the data but **the environment producing the data.**

The frontend team ran an A/B test and moved the purchase button from the top of the screen to the bottom. Click-through halves, obviously. The button is harder to see.

How does a model that only reads the table interpret that? First half of March, 12% click-through; second half, 6%. The model concludes that purchase intent has fallen. What actually happened is that people could not find the button.

The root of the problem is that the same "did not click" data cannot distinguish **not clicking because you were not interested** from **not clicking because you could not find it.** The click log records whether a click happened, not where the button was at the time. Call it a log stripped of its context.

And the real cause here is organisational, not technical. The frontend team had no reason to notify the data team about a UI experiment, and the data team looked at the numbers and concluded user behaviour had changed. Nobody was at fault. There was simply no channel for that information to travel through.

### The moment an LLM produces a syntactically perfect wrong answer

The subtlest case. Say the product team changed the definition of an active user, raising the bar from one login a month to three logins a week. The `is_active` column is still Boolean and still has the same name. Only the logic deciding True/False changed.

Now an executive asks the data copilot: how many active users this month?

```sql
SELECT COUNT(*) FROM users WHERE is_active = TRUE;
-- result: 250,000
-- syntax errors: 0, runtime errors: 0
-- but the executive expected 700,000, under the old definition
```

The LLM produced flawless SQL, exactly as it did yesterday. And the report says "active users down 64%," off which someone may urgently raise marketing budget or change product direction.

This is why semantic drift is particularly dangerous in the LLM era. **Syntactically perfect does not guarantee semantically correct.** And an LLM has no way of noticing on its own that the SQL it wrote is out of step with the organisation's current definitions.

One practically useful principle falls out of this. **When a definition changes, change the column too.** Overwriting an existing column with a new definition is manufacturing semantic drift by hand. Create `is_active_v2` and announce the deprecation of the old one.

## 2. Documents rot with time as well

That covers structured data. Now the unstructured side, which is scarier if you run RAG.

![Vector search has no sense of time](/book2-poison-en.svg)

_Both are outlook documents about Company A, so the semantic distance is similar._

A 2024 research report on Company A sits in the vector DB. Target price 50,000, recommendation Buy. In 2026 results deteriorate, a new report comes out, target price 20,000, recommendation Sell. The new report gets indexed too — but **the old one was never deleted.**

An investor asks how Company A looks. Vector search returns both. Similarity 0.93 and 0.91 — nearly identical, which makes sense, since both are documents about Company A's outlook. If anything, the older one scores higher.

This is **context poisoning**: stale information entering the model's context and planting false confidence.

One thing worth stressing. This is **harder to catch than hallucination.** A hallucination has no supporting document, so it collapses the moment you check the source. Context poisoning presents a real, existing document as its basis. Show the source and it is a genuine brokerage research report. It is just two years old.

A related failure is **embedding drift**: you upgrade the embedding model while existing documents remain vectorised under the old one. The two vectors are not in the same semantic space, so you ask about Company A and a report on Company B scores higher. Retrieval worked correctly, so not one line lands in the error log.

The response is simpler than you would think. Attach validity periods to documents, drop non-current versions from retrieval, and reindex everything when the embedding model changes. The problem is that if this is not in the design from the start, bolting it on later is a considerable nuisance.

## 3. And then the system poisons itself

Everything so far has been data rotting from the outside in. The last one is the system rotting **on its own.**

![When output becomes data, an error hardens into truth](/book2-loop-en.svg)

_In ordinary software the output of code does not rewrite the code._

Continue the earlier example. An LLM misread a piece of ad-laced news as a buying opportunity. Users who got that alert actually bought the stock. Purchase data accumulates. In the next training cycle the system discovers a pattern: **when this kind of news appears, people buy.**

The model's initial misreading changed user behaviour, the changed behaviour was recorded as data, and that data turned the misreading into ground truth. Each turn around the loop amplifies it a little.

Traditional software does not do this. A payment system returning success does not rewrite the payment logic. But **in an AI system the model's output becomes its training data.** That is a category of risk unique to AI, and it grows as you automate more.

Recommender systems show the structure even more starkly. If the model recommends A, B and C, the user can only choose among those three. Click A and "the user likes A" becomes training data. There are two defects in that.

First, B and C get recorded as "not clicked," which does not distinguish **disliked it** from **never really saw it.** The stripped-context log problem again.

Second and more fundamental: for D, E and F, which were never recommended in the first place, **no data is collected at all.** They were never shown, so there is no way to know whether the user would have liked them; with no data there is no basis for recommending them; and not recommending them means data never accumulates. This is not a shortfall in optimisation — it is a state in which information about a whole region is **structurally uncollectable.**

### How to break it

The loop cannot be eliminated. As long as you learn from data, output influencing data is unavoidable. What you can do is weaken it.

The most widely used tool is an **exploration slot**. Nine of ten recommendation slots get filled by whatever the model judges best; one or two get filled independently of the model's score. That slot becomes a channel for shining light into the unseen region. It is shown to the user mixed in with the rest, and the response data is harvested afterwards. The cost is a little short-term performance; the gain is information about a region the model knows nothing about.

## 4. And the same structure is also a weapon

Here is the interesting reversal. That circular structure — the one described as dangerous throughout — becomes the most powerful asset you have if you point it the other way.

Accumulating user feedback flows three ways. Failure cases become material for the evaluation set, signal patterns become a basis for personalisation, and clusters of failure tell you what to fix first. Then the improved product draws more use, which produces more feedback. This is the **data flywheel**.

You will have noticed: **structurally this is exactly the self-reinforcing loop from before.** Output changes data, and that data changes the system again. Only the direction is reversed.

Which means the warning comes attached. Same structure, same risk. In April 2025 OpenAI rolled back a GPT-4o update within days of shipping it. The model had become sycophantic — agreeing with users unconditionally and praising them excessively — and among the causes OpenAI described was **incorporating short-term feedback signals like thumbs up and thumbs down into the reward.**

People give a thumbs up to answers they enjoy hearing. A model tuned on that signal converges on pleasant answers rather than correct ones. Those answers attract more thumbs up, and each turn of the loop amplifies the flattery. Even a world-class organisation has to pull a product back if the flywheel is pointed the wrong way.

So there is one question you must ask when designing a flywheel. **Optimise on this signal, and where does the system eventually converge?**

## 5. A personal view

The thought that kept surfacing while working through these chapters was that **none of these are technical problems.**

The currency changed because the finance team did not tell anyone. Click-through fell because nobody knew the frontend team had run an experiment. The active-user definition changed because the product team decided it should. The old report is still in the vector DB because nobody decided to delete it. Not one of these is the kind of thing code can prevent.

So what is actually needed comes down to two things. One is **watching the distributions continuously**. When meaning changes, values change; when values change, the distribution carries a trace. Imperfect, but the only defence that can be automated. The other is **building the channel through which definition changes travel.** That is organisational, not technical, which is why it gets neglected more often.

There is something I got wrong for a long time doing data science. I assumed that to find out data was wrong, you look at the data. But every case here is one **you cannot see from the data alone.** The data is fine. What changed is the organisation's agreement about what that data means, and that is not written in the table.

The next post covers the five layers of safety net you build on top of a probabilistic engine. Everything so far has been the stage before the model; now we go into the model itself.

---

## About the book

If any of this felt familiar, you have probably lived through an unexplained quality drop at least once. The book is about where to look in that moment.

![Practical Knowledge Every Junior AI Engineer Needs](/book-junior-ai-engineer.png)

This post covers material from Part 2 of *Practical Knowledge Every Junior AI Engineer Needs* (Hanbit Media). Across five parts and fourteen chapters, the book deals with crossing from a demo to production: five layers of safety net over probabilistic output, the criteria for deciding how much autonomy to give an agent, and cost and observability after deployment. It is weighted toward principles that will still hold in five years rather than the usage of any particular framework.

The book is published in Korean. Table of contents and a preview are available at the bookstores below.

- [Kyobo Book](https://product.kyobobook.co.kr/detail/S000220634991)
- [YES24](https://www.yes24.com/product/goods/194330005)
- [Aladin](https://www.aladin.co.kr/shop/wproduct.aspx?ItemId=398964970)

---

**Related posts:**

- [The Model Is Smart, So Why Is the System Stupid?](/en/ai-system-fails-outside-model/)
- [AI Agents Come from a Better Harness, Not a Better Prompt](/en/ai-harness-engineering/)
- [Agentic Engineering in Financial AI](/en/agentic-engineering-in-finance/)

_Written as of 15 August 2026. The GPT-4o rollback is based on OpenAI's own published account from April 2025. The cases in the text are reconstructions of frequently repeated patterns rather than specific incidents at named companies._
