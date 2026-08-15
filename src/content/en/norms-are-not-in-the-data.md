---
title: "Norms Are Not in the Data: The Two Lineages of World Models"
description: "World models come in two lineages, and only one of them gets talked about. Reading the four axes of a symbolic world model as families of formalism turns up three layers of a different kind — and the last one asks a question the other three never touch. On why a model that learns from observation cannot, in principle, learn what is permitted."
pubDatetime: 2026-08-01T04:00:00Z
koSlug: norms-are-not-in-the-data
tags:
  - world-model
  - ai-agent
  - engineering
  - machine-learning
---

When people talk about world models, they mostly picture the same thing. A robot simulating the next moment in its head, a video model painting the next frame, a self-driving car predicting where the car ahead will go. I spent three posts on exactly that — the lineage that learns dynamics from data and predicts the next state, usually called the learned or neural world model.

But there is a second lineage. It is much older, and it is running right now anywhere the cost of failure is high. Digital twins on factory floors, clinical pathways in hospitals, rules and policy engines, the order-payment-shipping state machine behind every commerce site. None of these systems ever called themselves world models. They went by domain model, state transition system, PDDL specification.

In *AI 에이전트 실행 세계*, Josh (Juhwan Lee) names this lineage the **symbolic world model** and lays out the four axes such a world is expressed in.

1. What exists? (entities, objects)
2. What state is it in? (state, properties)
3. What changes are allowed? (transitions, actions)
4. What is forbidden or restricted? (constraints, policies)

Those four stuck with me for a while. They are clean, but the more I pulled at them the less they looked like a four-item checklist. What follows is what happened when I held them up against the older formalisms. The short version: these are **three layers of a different kind**, and the last one is not the same sort of thing as the other three at all.

## 1. Not one flat list

Rename each axis with the formalism that owns it and the families separate on their own.

![The four axes, read as families of formalism](/onto-axes-en.svg)

_Three layers of a different kind, stacked — not four items in a row._

**1 and 2 are an ontology problem.** "What exists" is close to the literal definition of the word. Philosophy has asked it under that name for a long time, and Quine's version — to be is to be the value of a bound variable — is the same question in a tighter suit. Move to computing and it splits into a layer for concepts and taxonomy (TBox) and a layer for the actual individuals and their facts (ABox). What kinds of things are there, and which of them are currently in what state.

**At 3, ontology alone runs out.** A static ontology will tell you that an order exists and that it has a state. It will not tell you that an order can move from *paid* to *preparing shipment* but never back. Handling change requires an action formalism. Classically that is situation calculus; the version closest to practice is PDDL, where an action is defined by its preconditions and its effects. What must be true for this to be possible, and what becomes true once it happens.

**4 is a different animal.** Integrity constraints, access control policies, and — climbing back up to logic — deontic logic. Ever since von Wright set out a logic of obligation, permission and prohibition in 1951, this has developed separately from the logic of what is possible.

That separation is where this post actually starts. Axes 1 through 3 ask **what can happen**. Axis 4 asks **what may happen**. In modal terms, the first three are alethic and the last is deontic.

## 2. The line observation cannot cross

Why does the distinction matter? Because it decides what a neural world model can and cannot learn.

![A line no amount of observation crosses](/onto-gap-en.svg)

_You cannot derive an ought from an is._

A ball falls when dropped. A payment fails when the balance is short. This API usually answers within three seconds. All of these are facts about the world, and with enough observation they can be learned. This is precisely what neural world models are good at.

Now: may this transaction be approved? May this customer record be read? May this refund go through without a human looking at it? No amount of watching the world produces these. A norm is not a property of the world; it is something we decided. Observational data records **what people actually did**, never **what they should have done**.

This is the gap Hume pointed at in 1739 — that any argument stepping from statements of fact to statements of obligation has an unjustified jump hiding in it somewhere. An old philosophical complaint, and it turns out to have a very practical consequence.

**A neural world model does not fail to learn norms because it lacks data.** It fails because norms are the wrong category of thing. Growing the model and adding data does not move this line. It is not the kind of problem scale solves.

There is an obvious objection. Norms show up in behaviour, so wouldn't enough examples teach them? To a degree, yes. But what gets learned is not the norm — it is **the distribution of traces left where the norm was followed**. The difference shows up at the violation. Hand the model a new violation that never appeared in training and it cannot tell a breach from a merely rare case, because norms are not defined by frequency.

In finance or medicine, where regulation is dense, that difference tends to announce itself as a single incident rather than a gradual decline. I wrote earlier about [two agents reaching the same correct answer while one of them touched a tool it had no business touching](/en/llm-evaluation-methods/) — grade the output and it is invisible; grade the path and it is not. That is this same category of failure.

## 3. A world specified, not a world learned

So the symbolic lineage treats the world differently at the root. In Josh's phrasing, the world is not something to be **learned and matched** but something to be **specified and operated**. Before imagining what is possible, you fix what is permitted.

The centre of gravity shifts from prediction to enforcement. State lives in records rather than free text, change is bounded by transition rules rather than description, and exceptions are blocked by policy rather than left to probability.

An e-commerce order flow makes this concrete and familiar. An order exists (1). It can be awaiting payment, paid, shipping, delivered, or cancelled (2). Paid can move to shipping, but delivered cannot move back to awaiting payment (3). A shipped order cannot be cancelled by the customer alone (4). Nobody called this a world model, but all four axes are there.

For evidence that this is not just theory, look at [Palantir's Ontology](https://www.palantir.com/docs/foundry/ontology/overview). They describe objects, properties and links as the semantic layer and actions and dynamic security as the kinetic layer — the nouns and the verbs of an organisation. Actions there are defined not as functions but as **governed operations**, which bundles the transition and the constraint into one thing. The four axes, shipped as a commercial product.

## 4. The symbolic side has old walls too

So specify everything and be done? The lineage has been walking into three walls for decades, and they have not moved.

**The frame problem.** McCarthy and Hayes raised it in 1969. Writing down what an action changes is manageable. Writing down **what it does not change** is the hard part. Change an order's state and the customer's address stays put, and the other orders stay put, and the inventory — wait, does inventory move? Grow the world a little and the list of things that stay still explodes.

**The qualification problem.** You cannot enumerate all the preconditions. Approving a payment requires a sufficient balance, and a valid card, and remaining credit, and a merchant in good standing, and… the list never closes. This is why specifications in the field are always a bit loose somewhere.

**The symbol grounding problem.** Harnad set it out in 1990: what, exactly, does a symbol touch in reality? Inside the system `order.state = shipping` is a token. How does it stay attached to an actual box on an actual truck? Without a person continually re-tying that knot, it does not.

The neural lineage sidesteps all three. It holds no explicit state, so no frame problem. It enumerates no preconditions, so no qualification problem. It reads straight off pixels or text, so grounding comes for free. In exchange it guarantees nothing. Less a sidestep than an empty seat where the guarantee used to be.

## 5. The division of labour is not arbitrary

From here the neuro-symbolic answer stops looking like a compromise and starts looking like an inevitability, because the strengths sit on exactly opposite sides.

![Each one fills exactly the other's hole](/onto-split-en.svg)

_Neural handles grounding, symbolic handles enforcement._

Neural is strong at reading an open world: taking messy, unstructured reality and turning it into symbols, muddling through situations nobody specified. That is exactly where symbolic jams on qualification and grounding.

Symbolic is strong at guaranteeing a closed one: letting only permitted transitions through and leaving a record of what ran and why. That is exactly what neural cannot offer when a corner case shows up.

Which settles the split. **Neural takes grounding, symbolic takes enforcement.** Keep possibility wide open; keep execution narrow and safe. Recent work moves this way — [DR. WELL](https://arxiv.org/abs/2511.04646), for instance, proposes a decentralised neuro-symbolic setup where several LLM agents ground their plans in a shared symbolic world model. Each agent reasons freely, but the real state lives in the shared model and only what it validates gets executed.

## 6. Why ontology came back

For a while "ontology" was a slightly dated word, mostly because of how loudly the Semantic Web failed. The plan was to make the whole web machine-readable, and specifying an open world at that scale was never going to work.

Domain ontologies did not die, though. They survived quietly in places with a shared shape: **narrow boundaries and expensive failure**. Airline scheduling, clinical pathways, access control, payment ledgers. Small closed worlds where being wrong hurts.

And I think there is a specific reason this matters again now. Nearly every AI feature we have shipped so far has been **reading**. Summarise, classify, generate an answer. Reading is survivable without an ontology; a human filters the mistakes.

The moment agents start **writing** — cancelling orders, approving refunds, closing tickets, triggering deploys — something in the system has to be able to answer *may this happen*. And for the reason above, that is not an answer a model arrives at by learning.

## 7. What I take from this

I lean toward the symbolic side, though not out of taste. Norms are not in the observations, and you cannot train a model on something that is not there. So somewhere in the system there has to be a specification a person wrote.

Which sounds like a deflating conclusion — everything ends up hand-written after all. Specification cost is the real bottleneck for this lineage, and there is a nice irony sitting right there.

The [Text2World](https://arxiv.org/abs/2502.13092) benchmark measures precisely how well an LLM generates PDDL specifications from natural language. So LLMs may not be here to replace symbolic world models so much as to **make them cheaper to build**. The main reason ontologies never spread was that a person had to write every line; if a model drafts and a person reviews, the arithmetic changes.

Then the picture looks like this. The model does not learn the world well enough to replace the norms; it helps a person write them down. And the norms, once written, constrain what the model is allowed to do. It reads like a circle, but a human judgement sits in each step, so it does not spin.

One last thing I find interesting: this is the same shape I keep arriving at from other directions. [A game engine keeping the truth while a world model paints it](/en/roblox-reality-hybrid/), deterministic code wrapping a probabilistic model, safety nets stacked outside the model. All the same move — split the part that is good at being fuzzy from the part that has to be guaranteed, and decide where the line goes. Neuro-symbolic turns out to be one of the names already hanging on that structure.

---

**Related reading:**

- [LLM Evaluation: Eleven Methods in Four Families](/en/llm-evaluation-methods/)
- [The Model Is Innocent: Why AI Failures Start Outside the Model](/en/ai-system-fails-outside-model/)

## References

- Josh (Juhwan Lee), *AI 에이전트 실행 세계 ① 원리편* — the symbolic world model and its four axes
- [Text2World: Benchmarking Large Language Models for Symbolic World Model Generation (Hu et al., 2025)](https://arxiv.org/abs/2502.13092)
- [DR. WELL: Dynamic Reasoning and Learning with Symbolic World Model for Embodied LLM-Based Multi-Agent Collaboration (Nourzad et al., 2025)](https://arxiv.org/abs/2511.04646)
- [The Ontology — Palantir Foundry Docs](https://www.palantir.com/docs/foundry/ontology/overview)
- J. McCarthy & P. Hayes, "Some Philosophical Problems from the Standpoint of Artificial Intelligence" (1969) — the frame problem
- S. Harnad, "The Symbol Grounding Problem" (1990)
- G. H. von Wright, "Deontic Logic", *Mind* (1951)

_Written 1 August 2026. The four-axis framework is from Josh's book; reading it against the older formalisms, and everything drawn out of that reading, is mine._
