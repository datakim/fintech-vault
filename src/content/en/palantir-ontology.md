---
title: "Is Palantir's Ontology Really an Ontology?"
description: "Palantir puts the word Ontology at the centre of its product. It uses none of the W3C standards and does no logical inference, which has drawn a sharp charge: that this is database modelling in philosophical packaging. Taking the objects, links and actions apart, then measuring them against the classical definition."
pubDatetime: 2026-08-01T06:00:00Z
koSlug: palantir-ontology
tags:
  - ai-agent
  - engineering
  - world-model
  - llm
---

After [writing about ontologies](/en/norms-are-not-in-the-data/), one thing kept nagging: there is a company that puts the word at the dead centre of its product. Palantir calls the core of its Foundry platform, simply, the Ontology.

Search for two minutes and the pushback is loud. That is not an ontology, the argument runs — it is database modelling wearing philosophical clothes. Which made me curious. **Is it a real ontology, or just a well-chosen name?**

The previous post already laid out the classical definition and the four axes, so I had a ruler handy. I picked it up.

## 1. What the thing actually is

In one line, Palantir's Ontology is an **operational layer that puts how an organisation actually runs into a form software can handle**. It sits on top of integrated datasets and models and ties that data back to real-world counterparts — physical assets like plants and equipment, and concepts like customer orders or financial transactions.

Three pieces. **Object Type** defines the nouns, **Link Type** connects them, and **Action Type** actually changes them. **Functions** carry arbitrary logic alongside.

Those sort into three layers.

![Nouns, verbs, and the grammar between them](/palantir-layers-en.svg)

_Most data platforms stop at the first layer._

Palantir describes the semantic elements as the organisation's nouns and the kinetic elements as its verbs, with a dynamic layer on top that decides permissions at run time.

You will find write-ups that describe the kinetic layer as "where data is mapped to the actual database." Going by the official docs, that is wrong. **Kinetic means actions, functions and dynamic security — the execution side.** Data mapping belongs to the backing datasets under the semantic layer. Blur that distinction and the point of the product goes with it.

## 2. Actions are the interesting part

The piece worth attention here is not the objects. Palantir defines an action not as a function but as a **governed operation**.

![An action is not just a function](/palantir-action-en.svg)

_The amber boxes separate a button a person may press from one they may not._

Press "schedule maintenance" and it collects input from the user, runs validation rules, checks permissions, executes, writes back to the source system, and records who did it and why. All of it as one bundle.

That is the whole difference from a plain function. A function knows **what can be done**. An action carries **what may be done** with it. The line between alethic and deontic from the previous post, drawn inside a product.

## 3. Two common misreadings

Two kept coming up while reading around.

**It is not a giant knowledge graph that generates itself, GraphRAG-style.** A person designs it, and reasonably clean data has to exist first. Throw raw data at it and no world assembles itself.

**It is not a graph database either.** Not something you traverse with Cypher, but closer to an abstraction layer with objects indexed on top.

## 4. So — is it an ontology?

Time to rule. Against the classical test the answer is fairly clear.

**It uses none of the W3C standards.** No RDF, no OWL, no SPARQL — a proprietary representation instead. So you cannot export a Foundry ontology as an OWL file and have another platform reason over it.

**There is no logical inference.** No OWL-style reasoning. Every relationship has to be modelled explicitly; the platform infers nothing on your behalf. Declare that A is part of B and B is part of C and have A-part-of-C follow for free — that is the charm of a classical ontology, and it is absent.

**So by the academic definition, no.** Up to here the critics are right. The harder version of the charge goes further: Object Type is a table, Property is a column, Link is a foreign key, Action is a stored procedure. Conceptually no different from Peter Chen's 1976 entity-relationship model, dressed in vocabulary that makes it harder for executives to interrogate.

## 5. But change the ruler

Stopping there is why this post would not be worth writing, because a different ruler flips the picture.

The previous post laid out the four axes of a symbolic world model. What exists, what state it is in, what changes are allowed, what is forbidden. Measure both ontologies on those.

![The two ontologies, measured on four axes](/palantir-axes-en.svg)

_Not an ontology by the academic test, yet fuller on the axes an agent needs._

Classical ontology dominates axis one. It builds class hierarchies and infers over them. Axis two it handles through the ABox, though largely statically.

Axes three and four are another story. **OWL has no concept of action at all.** There is no way to express "paid can move to shipping," which is why doing that requires importing a completely different formalism — PDDL, situation calculus. Axis four reaches logical integrity constraints and stops; questions like "may this person read this for this purpose" are not in scope.

Palantir is the mirror image. Weak on one, with three and four at the centre of the product.

I read that as follows. **Classical ontology was built to understand a world; Palantir's was built to operate one.** The first aims at inference, the second at enforcement. Sharing a name is genuinely confusing, but neither is the fake version of the other — they are different tools with different purposes.

## 6. The downsides are real

Balance requires the other column, and if you are evaluating this seriously these matter more than the above.

**Vendor lock-in is severe.** The deeper business logic moves into Foundry, the more expensive leaving becomes, and with no standards there is no clean export. Your operating rules end up locked inside one vendor's private format.

**Data has to come to it.** Foundry does not reference your existing operational databases in place; data gets pulled in. Integration comes first, and a weak pipeline underneath produces a weak ontology on top.

**There is a lot to learn.** Object, Link, Action, Function, Interface, OSDK — the concept count keeps climbing.

**Interoperability is limited.** There is no formal reasoning substrate to share with AI agents on other platforms.

And one more. There is an argument that Palantir's real advantage is not the Ontology as technology but the service model of embedding engineers on site, plus its government and institutional relationships. I think that is substantially correct.

## 7. What I take from this

The naming argument matters less than it seems. Call it an ontology or an operational model; what matters in practice is whether **"what may be done" is written down somewhere in the system**.

Seen that way, what Palantir did comes into focus. Technically there is not much new here. What there is, is a product that **forces the claim that data, logic, execution and security have to live in one place or automation does not happen**.

In most companies those four are scattered. Data in the warehouse, logic in service code, execution across business systems, permissions in IAM. People have been running between them all along. Agents cannot run between them — there is nowhere to attach. Handing an agent a button requires that button to already carry validation, permissions and audit, and in most companies no such button exists.

So the timeliness of this product comes from timing rather than technology. AI that only read is starting to write, and a structure that gathered those four in one place suddenly matters.

One correction to my previous post while I am here. I wrote that LLMs generating specifications would lower the cost of building an ontology. Reading around turned up an important caveat. **Hand schema generation to an LLM and the existing mess gets structured along with everything else** — the terms each department uses differently, the inconsistent state values, the columns nobody has touched in years, all promoted into objects.

The real cost of writing a specification was never the syntax. It was **deciding what counts as one thing**. That remains the work of someone who knows the domain, and probably will for a while.

---

**Related reading:**

- [Norms Are Not in the Data: The Two Lineages of World Models](/en/norms-are-not-in-the-data/)
- [Better Agents Come From a Better Harness, Not a Better Prompt](/en/ai-harness-engineering/)

## References

- [Ontology overview — Palantir Foundry Docs](https://www.palantir.com/docs/foundry/ontology/overview)
- [The Ontology system — Palantir Architecture Center](https://www.palantir.com/docs/foundry/architecture-center/ontology-system)
- [Why create an Ontology? — Palantir Foundry Docs](https://www.palantir.com/docs/foundry/ontology/why-ontology)
- [Connecting AI to Decisions with the Palantir Ontology — Palantir Blog](https://blog.palantir.com/connecting-ai-to-decisions-with-the-palantir-ontology-c73f7b0a1a72)
- [Palantir Foundry Ontology: How It Works, What Problems It Solves, and Where It Falls Short](https://badalaiworld.substack.com/p/palantir-foundry-ontology-how-it)
- [Palantir's Ontology Narrative — Vonng](https://vonng.com/en/db/ontology-bullshit/)

_Written 1 August 2026 from public documentation and third-party analysis. I have never run Foundry myself. Adoption figures circulating online mostly come from vendor material and should be read as such._
