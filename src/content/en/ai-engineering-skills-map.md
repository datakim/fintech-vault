---
title: "Taking Apart Andrew Ng's AI Engineering Skills Map: Four Items Saying One Thing"
description: "Four AI engineering competencies, drawn from an analysis of ten thousand job postings. Rather than copying the list across, here is the structure underneath it. It is not a flat list but a stack, the same thing sits inside all four items, and the ability to build a model is not on the list at all."
pubDatetime: 2026-08-15T01:30:00Z
koSlug: ai-engineering-skills-map
tags:
  - ai-coding
  - engineering
  - llm
  - machine-learning
---

Andrew Ng has published an AI engineering skills map. Four competencies, drawn from analysing more than ten thousand job postings, interviewing dozens of practitioners and hiring managers, and running a survey. In his own words, a process much like running clustering over a large body of data.

- Building and deploying AI applications
- Software engineering fundamentals
- Using coding agents
- Shaping the build

I read it this morning, and since copying the list across leaves nothing behind, I read it a few more times and took the structure apart.

One caveat of his caught my eye first. He writes about **AI engineering skills** rather than the job title "AI engineer," with the analogy that every developer now needs to handle cloud while relatively few carry the title cloud engineer. Full-stack or data engineer, everyone ends up needing this. That caveat may matter more than the list.

## 1. It is a stack, not a flat list

The four are presented as though they sit at the same level. Read them and they do not.

![What you miss reading it as a flat list](/skills-layers-en.svg)

_② is not an item alongside the rest — it is the condition under which the rest hold._

Ng's own explanation gives it away. Discussing software fundamentals, he notes that without them you receive output from a coding agent with no idea what trade-offs it made — **because you do not know what context to give it.** And he adds that fundamentals are what let you steer an agent in the precise language of software engineering.

Which makes ② not an item alongside ③, but a **precondition** for ③. It is putting "drives well" and "knows the way" on the same line. Not knowing the way, driving well takes you somewhere wrong.

Restack them and it comes out like this. Fundamentals at the floor; on top of that, coding agents producing speed; on top of that, the ability to handle probabilistic parts; and at the top, deciding what to build. Ordered that way, a learning order follows naturally.

## 2. The same thing sits inside all four items

Re-reading the items one at a time, I noticed something odd. The same thing was embedded in all four.

![The same thing sits inside all four items](/skills-verify-en.svg)

_All four converge on "how do I know what is right?"_

Under **building AI apps**, the core competency he names is not picking a good model but the ability to run a disciplined evaluation and error-analysis loop.

**Software fundamentals** are described as the ability to recognise trade-offs. Knowing the trade-offs means, in the end, **knowing what can go wrong and where.**

Under **coding agents** it is stated outright. To let an agent close its own loop, "provide a verifier or an evaluation." Not giving the agent the answer — **giving it the rubric.**

**Shaping the build** is about setting specifications, and setting a specification is defining what the finished state is. Which is also a verification criterion.

Ng does not tie the four together this way, but on re-reading they all look like different faces of one question: **how do I know what is right?**

The reason is simple. Once writing code gets cheap, **making the wrong thing quickly gets cheap too.** Ten times the production speed is ten times the speed of running in the wrong direction. So the bottleneck moves from making to **judging**.

I wrote earlier, [while sorting through LLM evaluation methods](/en/llm-evaluation-methods/), that evaluation had become a modelling task in its own right. Looking at this map, that does not seem to be only a story about people who build evaluation tools.

## 3. The ability to build a model is not on the list

This is where I stopped for a moment.

Nowhere in the four is "the ability to train a model." Machine learning and deep learning are mentioned — but in the building-AI-apps item, in a list of **components to understand**, alongside LLMs, context engineering, RAG and agentic workflows. Something to understand, not to build.

Coming from data science, that is a slightly chilling passage. A few years ago the way you demonstrated skill in this field was by building good models. On this map, model training has dropped to being one **optional component**.

Some of that is a consequence of how Ng defines AI engineering, of course. Building models is closer to research, and this map is for people building applications. Still, the fact that this is what came out of ten thousand job postings means the market is already moving that way.

## 4. Where the map is drawn faintly

A map has to be read for what is not drawn as much as for what is. Three places caught my attention.

![The faint areas on the map](/skills-missing-en.svg)

_Not that things are missing — read it knowing where it is drawn faintly._

**After deployment.** The first item is "building and deploying," and deployment appears as one word with almost nothing after it. In practice, the moment you deploy, inference cost starts accruing, quality quietly degrades, and without observability you do not even notice. As I [wrote earlier](/en/ai-system-fails-outside-model/), failures usually start outside the model — and that outside is drawn thinly here.

**Domain knowledge.** Absent from all four. It brushes against the fourth item's "understanding business context and customer goals," but in practice what gets built is usually decided by the domain. Whether this transaction can be auto-approved in a financial system is not the kind of question software knowledge answers.

**And the method's own lag.** This is a point about the methodology: ten thousand job postings contain only **what the market has already agreed on.** A competency companies have not yet named does not get written into a posting. Ng says he looked for skills that matter now and in the near future, but clustering finds the centre of the data, not its edges. Which makes this map less a forecast than **a sharp photograph of what is agreed right now.**

That is a characteristic more than a flaw. For deciding what to learn now, a sharp photograph is more useful. It only becomes a problem if you read the map as saying that what is not on it does not matter.

## 5. A personal view

What this list really says, I think, is **"from maker to judge."** Three of the four are about judgement. Know what can go wrong (fundamentals), hand the agent a rubric (coding agents), define what done means (shaping the build). The part where you actually move your hands is drawn as shrinking.

It looks more plausible for the fact that the same conclusion is arriving from several directions. [Looking into the FDE role](/en/fde-forward-deployed-engineer/), the coding share was stated as 70% and what remained at the end was scoping and stakeholder alignment. Two sources starting from completely different places arriving at the same spot is usually a signal.

And a practical note. **The hardest of these to learn alone is the fourth.** There are plenty of books on fundamentals, coding agents improve with use, and evaluation has tooling. But a sense for deciding what to build does not develop without real users and real failures. Ng's point about knowing when to ship an MVP fast and when to go slow is probably the same thing.

So the map might be better used not as a study list but as **a check on whether your job has a place to practise the fourth item.** The first three you can improve almost anywhere if you decide to; the fourth has no route without the position for it.

---

**Related posts:**

- [How Do You Grade an LLM? Eleven Evaluation Methods, Sorted into Four Families](/en/llm-evaluation-methods/)
- [The Model Is Smart, So Why Is the System Stupid?](/en/ai-system-fails-outside-model/)
- [Thinking About the FDE: Ten Names, One Job](/en/fde-forward-deployed-engineer/)

## References

- Andrew Ng, [The AI Engineering Skills Map](https://www.linkedin.com/pulse/ai-engineering-skills-map-andrew-ng-m479c/) (15 August 2026)

_Written after reading the piece published on 15 August 2026. The division into four competencies and the description of each are from the original; rearranging them into a stack, reading them along an axis of verification, and the points about where the map is faint are my interpretation. The original states that each item will be expanded on in future pieces, so some of what is raised here may be covered later._
