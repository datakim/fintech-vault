---
title: "How the Two Lineages of World Models Got Here: Seventy Years, Made Simple"
description: "Fine, there are neural and symbolic lineages of world models — but where did each start, and how did it arrive here? The one that tried to write the world down in logic and the one that tried to learn it from data, the walls each hit, and where each turned. Written to be readable with no background."
pubDatetime: 2026-08-01T07:30:00Z
koSlug: world-model-two-histories
tags:
  - world-model
  - machine-learning
  - ai-agent
  - engineering
---

I wrote earlier about [there being two lineages of world models](/en/norms-are-not-in-the-data/) — the neural one that learns from data, and the symbolic one where people write down the rules. After finishing it I was a bit unsatisfied, because I had given the conclusion while leaving out **where each started and how it got here.**

The history makes it much easier to understand. Neither lineage went the way it was first imagined; each turned direction every time it hit a wall, and that is how they ended up looking as they do. Knowing what those walls were makes the current shape follow naturally.

Written to be read with no background.

## They started from the same question

The two lineages actually diverged from one question.

![It started from one shared question](/lineage-fork-en.svg)

_One question, two answers, and seventy years since that fork._

**"How do you put how the world works inside a machine?"**

One side answered: people can write down the rules. The other answered: let the machine look and learn for itself. The two roads out of that fork are meeting again now.

Start with the side that writes it down.

## Symbolic — a history of narrowing what to write down

![A timeline of the symbolic lineage](/lineage-symbolic-en.svg)

_Every time it hit a wall, it narrowed the scope of what it would write down._

### Stage 1. Maybe we can just write it in logic (1950s–60s)

The first idea was simple. Write facts about the world as logical statements and the machine can combine them and infer. Put in "birds can fly" and "a sparrow is a bird" and "a sparrow can fly" falls out on its own.

### Stage 2. Writing actions down (1971)

The big turn happens here. STRIPS, built at Stanford to drive a robot called Shakey, laid out a way to write down **actions**. It goes like this.

> **Open the door**
> Preconditions: you are at the door, and the door is not locked
> Effects: the door is in an open state

A move from writing facts to writing actions. This is the ancestor of today's planning languages, and the axis I described in the earlier post — what changes are permitted — was born here.

**And then it hits a wall.** Writing what changes when a door opens is easy; the problem was writing what **does not** change. Opening a door leaves the room's colour the same, your position the same, the other doors the same, the windows the same. All of that has to be written down for the machine not to get confused, and the moment the world grows even slightly, the list of things that stay put becomes unmanageable. This is the frame problem.

### Stage 3. Give up the world, take one narrow field (1970s–80s)

So the goal was lowered. If the whole world cannot be written down, **write down one very narrow field.** Diagnosing blood infections, say, or configuring computer orders. These were called expert systems, and they made money. Companies adopted them eagerly.

**And a wall arrives here too.** A few hundred rules was fine; past a few thousand nobody could touch it. Add a rule to handle an exception and an exception to that exception appears; fix one rule and you cannot tell what broke. Maintenance costs became unbearable, many systems were abandoned, and this was a major cause of the so-called AI winter of the late 1980s.

### Stage 4. Make a standard and share it (1990s–2000s)

The next idea was collaboration. Build **standards** so that knowledge each party creates can be used by others. RDF and OWL came from this period, leading to the Semantic Web plan of making the whole web machine-readable.

**Blocked again.** Nobody tagged anything. From the perspective of someone building a web page there was no reason to add separate markup for machines to read, and specifying an open-ended world was never possible in the first place.

### Stage 5. A practical retreat (2012–)

Google's Knowledge Graph changed the current. Perfect logical inference was set aside in favour of a **practical goal**: showing an information card next to search results. And that is what survived.

Meanwhile, independent of the academic argument, the approach kept running in narrow places where failure is expensive. Medical terminology systems, financial data standards, digital twins in factories, order-state management in payment systems. Nobody called any of it a world model.

## Neural — a history of drawing less and less

Now the other road.

![A timeline of the neural lineage](/lineage-neural-en.svg)

_This side kept reducing what it would predict._

### Stage 1. The root was engineering, not AI (1960)

Unexpectedly, the ancestor here is control engineering rather than AI. There is a thing called the Kalman filter, and structurally it is a complete world model. Write down how the world moves **as equations**, estimate the current state from imperfect observations, and predict what comes next. It flew to the moon on Apollo.

**The limit was clear.** A person has to write those equations. A rocket's trajectory can be written as equations; "the world in which you pick up a cup in a kitchen" cannot.

### Stage 2. So let the equations be learned (1990)

Then why not have a neural network learn the equations from data? The idea was already there around 1990. The direction was right and the timing was far too early. There was neither the compute to run it nor the data to train on.

### Stage 3. The moment it got a name (2018)

The paper that gave this field the name World Models came out in 2018. Its structure is intuitive enough to be worth describing. Three parts.

| Part | What it does | The human analogue |
|---|---|---|
| First | compresses the frame into a small bundle of numbers | eyes |
| Second | predicts the next bundle | memory and imagination |
| Third | decides what to do from that | hands |

See with your eyes, imagine what comes next, act. The most famous part is that **training happened inside imagination.** Rather than practising in the real game environment, the agent was trained inside a fake world the model imagined — and it transferred to the real environment. This is the prototype of the idea in the earlier post that a world model is a factory for training data.

### Stage 4. Into something usable (2019–2023)

DeepMind's Dreamer line refined the recipe until it solved genuinely hard problems. The latest version solves more than 150 different tasks from one configuration. This is where "learning inside imagination" crossed from lab demo to practical technique.

### Stage 5. Realising you don't have to draw it all (2020–)

An interesting fork. Reconstructing the frame exactly is enormously expensive — you have to get right where each individual leaf will sway. But does winning the game require the position of the leaves?

MuZero abandoned frame reconstruction entirely and predicted **only what the decision needs.** And it did better. LeCun goes a step further and argues for dropping pixel prediction altogether: pixels carry far too much detail that neither needs nor can be predicted, so predict at a more abstract level.

### Stage 6. And then a counter-current appears (2024–)

Just as the argument for abandoning pixels was gaining ground, video generation models that draw every pixel started producing striking results — describe a world in text and get one you can walk around in.

So opinion is now split inside the neural lineage too. **Draw the pixels, or throw them away.** The argument is unresolved.

## The two lineages are mirror images

Laid out this way, something interesting shows up.

![The two lineages are mirror images](/lineage-mirror-en.svg)

_Both are histories of learning what to give up._

Symbolic **tried to write it all down, could not, and kept narrowing the scope.** From the whole world to one field, from one field to one task.

Neural **tried to draw it all, found it too expensive, and kept narrowing the target.** From the whole frame to only what is needed, from what is needed to an abstract representation.

Opposite directions, same activity. **A history of learning what to give up.** Both started trying to contain the whole world, both failed, and each got here by shrinking its ambition in a different way.

## So why are they meeting now?

The reason the two lineages get mentioned together lately is simpler than it looks. **AI has started to act.**

Most of what we have asked AI to do has been on the reading side. Summarise, classify, produce an answer. That only needs the ability to read broadly, and the neural lineage is good at it.

But once an agent starts cancelling orders and approving refunds, the story changes. Reading broadly is not enough; you need something that reliably enforces **this is allowed and that is not.** That is what the symbolic lineage has been refining for seventy years.

Because what each gave up sits on exactly opposite sides, putting them together fills each other's holes. That is why "neurosymbolic" keeps coming up.

## A personal view

Laying the two histories side by side, what struck me most was how useful a record of failure can be.

Knowing why expert systems collapsed makes the situation of piling rules into a prompt until you can no longer touch it look familiar rather than novel. It is the same problem. Knowing why the Semantic Web failed gives you a good guess at why a plan to tidy up all of a company's data keeps fizzling out. The lesson that you have to start narrow was available thirty years ago.

The field moves so fast that everything feels like a first encounter, when in fact a fair number of these problems have been round the track once already. Knowing this history is as useful in practice as learning the newest tool. At minimum, you find out in advance where you are going to trip.

---

**Related posts:**

- [Norms Are Not in the Data: The Two Lineages of World Models](/en/norms-are-not-in-the-data/)
- [Is Palantir's Ontology Really an Ontology?](/en/palantir-ontology/)
- [The Model Is Smart, So Why Is the System Stupid?](/en/ai-system-fails-outside-model/)

## References

- D. Ha & J. Schmidhuber, ["World Models"](https://arxiv.org/abs/1803.10122) (2018) — the paper that gave the field its name
- D. Hafner et al., the Dreamer line — imagination-based training as a practical technique
- J. Schrittwieser et al., ["Mastering Atari, Go, Chess and Shogi by Planning with a Learned Model"](https://arxiv.org/abs/1911.08265) (MuZero, 2019)
- Y. LeCun, ["A Path Towards Autonomous Machine Intelligence"](https://openreview.net/forum?id=BZ5a1r-kVsf) (2022) — the JEPA proposal
- R. Fikes & N. Nilsson, "STRIPS: A New Approach to the Application of Theorem Proving to Problem Solving" (1971)
- J. McCarthy & P. Hayes, "Some Philosophical Problems from the Standpoint of Artificial Intelligence" (1969) — the frame problem

_Written as of 1 August 2026. Compressing seventy years leaves a great deal of important work out, and the years given are representative points. Read it as a way of grasping the broad shape._
