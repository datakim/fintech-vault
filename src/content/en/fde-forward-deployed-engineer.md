---
title: "Thinking About the FDE: Ten Names, One Job"
description: "Forward Deployed Engineer, solutions architect, resident SA, customer success engineer, deployment strategist, applied AI engineer. The names keep multiplying, and laid out together there are only two axes. Why AI companies are now racing to hire the role Palantir invented, and what the actual core of it is."
pubDatetime: 2026-08-02T06:00:00Z
koSlug: fde-forward-deployed-engineer
tags:
  - engineering
  - ai-agent
  - llm
---

The term FDE turns up a lot lately. Forward Deployed Engineer. Palantir invented the role, and OpenAI, Anthropic and Google are all hiring under that name.

Digging further, though, there was not one name but many. Solutions architect. Solutions engineer. Resident solutions architect. Customer success engineer. Deployment strategist. Applied AI engineer. Every company calls it something different, and read the job postings and what they are asking for looks much the same.

So I spent a while reading talks and articles about it. Worth writing down, since it will probably be useful later.

## 1. Starting with the names

First, the names actually in use.

**Forward Deployed Engineer (FDE) / Forward Deployed Software Engineer (FDSE)** — Palantir's name for it. They sit inside the customer's organisation and write production code.

**Deployment Strategist** — Palantir's other role, and the FDSE's counterpart. Scopes the problem and manages stakeholders before code gets written. The usual framing is that **the strategist owns "why" and "what" while the FDSE owns "how"**, though in practice the boundary is said to blur often.

**Applied AI Engineer** — Anthropic's name. The FDE function sits under the applied AI team.

**Solutions Architect / Solutions Engineer** — widely used at AWS, Databricks and elsewhere. Owns the design, and usually hands the build off.

**Resident Solutions Architect** — Databricks' professional services organisation. Resident, as the name says, at the customer.

**Customer Success Engineer** — also at Databricks, fielding technical questions from customers already running in production.

**Sales Engineer** — the oldest name. Owns everything from first demo to signature.

## 2. Laid out together, there are only two axes

Ten or so names, and sorting them by what the work actually consists of leaves only two distinguishing axes.

![Many names, and underneath only two axes](/fde-map-en.svg)

_The names differ; what varies is the mix._

**The first axis is when they come in.** A sales engineer runs from first demo to signature, a solutions architect from technical review through initial design, an FDE from kickoff through production and renewal, and a customer success engineer arrives after operations have started.

**The second axis is how much code they write.** The figures vary by source, but broadly a solutions architect spends something like 20% of their time in an IDE, and an FDE up to 70%.

Put them on those two axes and the names simply occupy different positions; the character of the work is the same. **Sit next to the customer, write code, own the outcome.** Only the proportions differ.

### So why are there so many names?

Reading across the sources, the impression I formed is that the name is often set less by the work than by **which organisation the role sits in.**

Sit in sales and you are a sales engineer or a solutions engineer; sit in professional services and you are a resident architect; sit in engineering and you are an FDE. Databricks in fact groups these roles under an organisation literally called Field Engineering.

Same job, different name depending on which account the cost lands in. A slightly cynical observation, but scan a few org charts and that is how it reads.

## 3. So what is the core?

That is the naming out of the way; from here is the part I actually wanted to work out. Three personal conclusions after going through the talks and articles.

### One. The essence of the role is ownership, not translation

Articles introducing the role usually describe it as "a bridge between technology and business." I think that description is inaccurate. If bridging is the job, a consultant is a bridge and so is a PM. It does not explain why this role came into being separately.

Comparing the sources, the real difference that stood out was this. **A solutions architect hands over the design and leaves; an FDE is on the hook for it actually running.** In one source's phrasing, the FDE owns the outcome in production while the solutions architect owns a design somebody else will operate.

Invert the order and it gets easier to see. It is not that writing a lot of code makes you responsible; it is that **being responsible leaves you no choice but to write the code.** If it running in production is mine, I cannot hand it off and walk out. The 70% figure is a consequence, not a cause.

### Two. Without a platform, the role does not exist

This is the most useful diagnostic I found.

A former Palantir person said in a talk that if every FDE builds from bare ground, that is not an FDE organisation — it is a **dev shop**. And they added that a dev shop is fine, a profitable business even, but a different kind of business.

![Looks like the same job, and the outcomes split](/fde-platform-en.svg)

_There is only one diagnostic question._

The difference is a single thing. **An FDE does not write code from bare ground.** They assemble pieces that already exist. Without that, every new customer adds a repository, and maintenance cost either eats the P&L or the engineers quit before it gets there.

And here it meets [the earlier post on ontologies](/en/palantir-ontology/) exactly. **That layer of assemblable pieces is precisely where the Ontology sits.** With objects and actions defined as types, you are not rebuilding per customer — you are laying something on top.

So when a company says it wants to build an FDE organisation, the question comes down to one. **"What are your FDEs assembling on top of right now?"** No answer, and it is an FDE in name only.

### Three. It is rising not because of AI, but because products became customisable

I want the causality exactly right. This role is not rising because AI is fashionable.

The talk I mentioned laid out the conditions that create the need as a quadrant, and it was fairly clear-cut.

![Only one square actually needs an FDE](/fde-quadrant-en.svg)

_The first question is not "do we want this" but "are we in this square."_

If what you sell is complex and the buyer is technical, the buyer absorbs the complexity themselves. GitHub and Datadog work like that. If what you sell is simple, it was never a problem. Slack and Jira need configuring, not building.

**Only in the square where something complex has to be sold to someone non-technical** does the role become necessary. Palantir sat exactly there.

And here is the crux. The speaker's hypothesis was that the world did not suddenly realise Palantir's approach was good — rather, **the nature of the software business itself changed.** The logic runs like this.

> nearly every product is agentic now → so nearly every product is customisable → so the customer does not know what they can do with it

Build an agentic product and you are automatically in that square. A feature list used to be the product, and the customer could judge it. Now "it handles it for you" is the product, and what it can actually do is invisible to the buyer.

Which makes AI companies hiring for this role a structural result rather than a fashion. Of everything I read, that explanation was the most persuasive.

## 4. One paradox

Something I found funny while writing this up.

I looked at a course curriculum for this role, and the final chapter was titled **"The FDE's work that isn't code."** Inside it: stakeholder alignment, scoping, handoff. Having established that code is 70% of the job, the course ends by saying what remains is the part that is not code.

It looks like a contradiction, and on reflection it is natural. **AI keeps driving down the cost of writing code, so the remaining value gets pushed toward what is not code.** Deciding what to build, drawing the line around where a project ends, handing something over so the customer can run it after you leave. None of that has got cheap yet.

So writing code well is a qualification for the role, but it is not the **value** of the role. One talk defined the job in a single line: **a customer-facing software engineer.** Someone you would hire as an engineer who can also be put in front of a customer. The second condition is the scarce one, and that is where the compensation comes from — not the first.

## 5. A personal view

I paid attention to this because it overlaps a lot with a shift I feel as a data scientist.

Most of the job used to be receiving a well-defined problem and building a model. These days the model-building time has shrunk and **the time spent deciding what the problem is and drawing its boundaries** has grown. How far to automate and where a human checks, what counts as a single entity — get those wrong and everything downstream is misaligned. What an FDE does looks like the same thing.

Which is why I no longer read the role as somebody else's story. More people will end up responsible for bolting AI features onto something at their company, and the instincts they will need do not look far off what is written down here.

One more thing: recruiting-market material frequently notes that compensation for this role sits quite high. Those figures mostly come from hiring platforms, though, so I would not take them at face value. Better than the numbers is the question of **why this combination is scarce.** Plenty of people can write code, plenty of people can talk in front of a customer, and people who will do both while owning the outcome are genuinely rare.

---

**Related posts:**

- [Is Palantir's Ontology Really an Ontology?](/en/palantir-ontology/)
- [Norms Are Not in the Data: The Two Lineages of World Models](/en/norms-are-not-in-the-data/)
- [The Model Is Smart, So Why Is the System Stupid?](/en/ai-system-fails-outside-model/)

## References

- [Why OpenAI and Anthropic are hiring forward deployed engineer teams — The New Stack](https://thenewstack.io/forward-deployed-engineers-ai/)
- [Forward Deployed Engineer vs. Solutions Architect — Exponent](https://www.tryexponent.com/blog/forward-deployed-engineer-vs-solutions-architect)
- [Forward-Deployed Engineer vs. Deployment Strategist — Paraform](https://www.paraform.com/blog/forward-deployed-engineer-vs-deployment-strategist)
- [A Day in the Life of a Palantir Forward Deployed Software Engineer — Palantir Blog](https://blog.palantir.com/a-day-in-the-life-of-a-palantir-forward-deployed-software-engineer-45ef2de257b1)
- [A Day in the Life of a Palantir Deployment Strategist — Palantir Blog](https://blog.palantir.com/a-day-in-the-life-of-a-palantir-deployment-strategist-951cb59a5a96)
- [Day in the Life of a Databricks Customer Success Engineer — Databricks Blog](https://www.databricks.com/blog/2022/05/19/day-in-the-life-of-a-customer-success-engineer.html)
- [Databricks Careers](https://www.databricks.com/company/careers) — for the composition of the field engineering organisation

_Compiled from talks and material published as of 2 August 2026. I have never worked in this role; this is an outsider reading and organising the sources. Role definitions and scope vary greatly between companies, so there are limits to generalising. Figures such as the share of coding time or compensation levels come from recruiting-market material and should be read as indicative only._
