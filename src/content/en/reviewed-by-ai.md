---
title: "[Notes] These Days My Manager Isn't the First to Read My Report"
description: "You file a report and your manager feeds it to GPT for a summary and a critique. If almost everything now passes through a model somewhere, you can simply reverse the order and run it yourself first. How to cross-check across models, the four questions that get you a real review, and open-source tools like promptfoo, LibreChat and llm-council."
pubDatetime: 2026-07-28T21:00:00Z
koSlug: reviewed-by-ai
tags:
  - llm
  - engineering
  - ai-coding
---

A thought that turned up recently: an awful lot of what I write is now read by an AI before it is read by a person.

It used to go like this. You write a report, you file it, your manager reads it. Their experience and taste were the standard, and you could roughly predict where the red pen would land. After a few rounds you developed a feel for it — this person looks at the numbers first.

What about now? A manager who uses AI well will drop that report straight into GPT or Claude and start with "summarise this and critique it." That is not a bad thing. I would do the same. There are ten documents stacked up and no time to read each one closely, and having a summary plus a list of concerns in hand makes a much faster first pass. Layer your own judgement on top of that and it is a decent way to work. Though if you are busy or indifferent, you might pass along what came back more or less as-is.

![The first reader of my report has changed](/review-loop-en.svg)

_More and more often, a model reads what I write before a person does._

## Everything passes through it, large and small

This is not only about reports. Job applications, code reviews, proposals, even paper reviews — each passes through this route somewhere. Even where a person makes the final call, a structure with a model layered in front of them is becoming ordinary.

Which produces a slightly odd situation. The first reader assessing my work is not a person, and yet I submit without ever having checked what that first reader makes of it.

## So reverse the order

If someone is going to run it through a model anyway, I may as well run it first. It sounds like nothing, but made into a habit the difference is substantial.

Doing this deliberately for a while taught me one thing. **What comes back depends entirely on what you ask.** Ask "what do you think of this?" and you get compliments, a hundred times out of a hundred, because a model answers in the direction of making you feel good. So you have to ask differently.

![Ask "what do you think?" and you get compliments](/review-ways-en.svg)

_What you ask for decides what comes back._

Four that I use often.

**Make it summarise.** Cheapest and most reliable. Ask for a three-line summary, and if what comes back is not what you meant, the model did not fail to understand — the writing is wrong. A conclusion summarised oddly is a signal that the structure is off.

**Make it argue back.** "Take this argument apart." "Write the strongest objection from the opposing side." Ask for an assessment and you get praise; ask for an attack and you get the weak points. The most effective question shape I have found.

**Ask what is missing.** "What should be in this piece that is not?" Fixing what is there is something you can do alone; noticing what is absent is much harder alone. Blanks are invisible.

**Grade against criteria.** Instead of a vague request for an assessment, hand over a checklist. Is there numerical evidence, is an alternative proposed, are risks mentioned. This makes results far more consistent, and lets you hold several documents to the same yardstick.

## Don't trust a single model

One step further is cross-checking, which is also not complicated. Take the critique you got from model A, feed it into model B, and ask whether it is fair and whether anything is overstated.

![Run it myself before somebody else does](/review-cross-en.svg)

_A criticism both models raise is usually a real one._

The reason this matters is that running the same model several times helps less than you would think. Every model has consistent habits, and it leans the same way however many times you run it. A model from another family catches different things.

What is fun in practice is how often the two models raise quite different points. And **a criticism both of them raise is usually a real problem.** Something only one of them flagged, meanwhile, has a decent chance of being that model's taste. So these days I have B review what A flagged, and fix only what survives.

## Some tools

Opening several windows and copy-pasting every time got tedious, so I went looking. A few open-source options are worth knowing.

**[promptfoo](https://www.promptfoo.dev/docs/guides/compare-open-source-models/)** — runs the same input against several models at once and lays the results side by side. It was built for prompt testing, but you write a model list and pass criteria into YAML, run it, and get a matrix back. If you regularly need the same document reviewed by several models, this is the most convenient.

**[LibreChat](https://github.com/danny-avila/LibreChat)** — an MIT-licensed self-hosted chat UI. You can use several providers in one screen and switch models mid-conversation, which makes putting the same question alternately to GPT and Claude easy. Open WebUI is a similar option.

**[karpathy/llm-council](https://github.com/karpathy/llm-council)** — this one is fun. A small web app by Karpathy: your question goes to several models at once, the models critique and rank each other's answers **anonymously**, and a chairman model synthesises a final answer at the end. Consider it an automation of the cross-checking above. The anonymity is the good part, since it suppresses to some degree a model's tendency to favour output from its own family.

## A personal view

The approach is not a cure-all, so a few caveats.

First, **you can only ask as much as you already know.** Asking a good question requires already knowing what matters, and judging whether the feedback that comes back is right requires the same. Without domain knowledge you get pulled along by whatever sounds plausible. Which amounts to saying the tool is only useful if you have understanding — a dull conclusion, but I think a true one.

Second, **the grading model has biases too.** It prefers what it saw first, scores long pieces generously, and favours writing from its own family. I went through this in [an earlier post](/en/llm-evaluation-methods/); it is not the kind of thing that vanishes when you average over runs, because it is a lean rather than noise. That is also why cross-checking is worth the trouble.

Third, and this is what bothers me most: **passing the AI must not become the goal.** There is a definite profile of writing that models like — clear structure, well-placed subheadings, a reasonable density of numbers. Start optimising for that and you produce something flat for human readers. The old story about a measure ceasing to be a good measure once it becomes a target repeats itself here. AI review is for filtering out mistakes, not for deciding whether something is well written.

And all of this is probably a transitional scene. In a few years this kind of checking will be built into document tools by default and there will be nothing to discuss. For now, though, the gap between people who have made it a habit and people who have not is visibly widening, so it seems worth doing deliberately for a while.

---

**Related posts:**

- [How Do You Grade an LLM? Eleven Evaluation Methods, Sorted into Four Families](/en/llm-evaluation-methods/)
- [AI Agents Come from a Better Harness, Not a Better Prompt](/en/ai-harness-engineering/)
- [The Model Is Smart, So Why Is the System Stupid?](/en/ai-system-fails-outside-model/)

_Written as of 29 July 2026. The features of the tools mentioned may change._
