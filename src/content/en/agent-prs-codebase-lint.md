---
title: "What It Takes for a Codebase to Survive 11,000 Agent Pull Requests a Month (feat. Lauren Tan from SpaceX)"
description: "The Grok Bot team at SpaceXSI, a SpaceX subsidiary, shipped 11,000 pull requests in a month while keeping the revert rate around 0.5%. This post follows how they turned every correction to their agents into a lint rule or a verification step until there was little left to review, and what the same approach looks like in data and financial code."
pubDatetime: 2026-11-15T20:45:00Z
koSlug: agent-prs-codebase-lint
tags:
  - ai-coding
  - ai-agent
  - engineering
---

One team shipped 11,000 pull requests to production last month, and only about 0.5% of them were reverted. Lauren Tan gave the figure in a talk published on the AI Engineer channel on 14 November. She works on Grok Bot at SpaceXSI (formerly xAI), the SpaceX subsidiary that makes Grok. SpaceXSI also owns Cursor, which is why Cursor's history and features come up throughout the talk. Grok Bot is a desktop app released in beta in August that hands work to agents, each with its own computer.

Tan herself shipped 3,000 pull requests last month, many of them merged while she slept, and says it took six months to get there. Nobody can read hundreds of pull requests a day, so the talk's answer is less about reviewing faster and more about leaving less to review, by turning each correction to an agent into an automatic check. She separates this from blind trust and describes it as investing in the agents' environment until you can trust them to do the right thing.

## 1. 11,000 pull requests in a month, 0.5% reverted

The team figures are 11,000 pull requests shipped last month and a new stable release roughly once a day. In October 227 people contributed at least one pull request, many of them drive-by contributors without much context. At that pace the revert rate held at around half a percent and fell in relative terms. Startup, typing, opening new chats and switching between them have all become faster since launch, which is no small thing for an app still built on Electron, a framework that runs desktop apps on web technology.

Tan explains where to spend time on an agent's environment with an inverted pyramid. The widest layer at the top is the code itself: API design, architecture and refactoring. Below it come deterministic checks, which always give the same result for the same code: lint rules, type systems, compilers and tests. Together these two layers constrain what agents can do, so that the easiest path an agent can take is also the right one.

The third layer is verification, runtime and formal, which checks the properties the system has to keep and whether the agent understood what you meant. Prose that needs judgement (rules, skills, AGENTS.md) sits in the narrowest layer at the bottom, and there should be little of it.

![Four layers stacked as an inverted pyramid. The widest, at the top, layer 1, is the code itself: API design, architecture and refactoring, with the examples ban useEffect and split main and renderer. Layer 2 is deterministic checks: lint rules, types, compiler and tests, with the examples import boundaries and no timer patches. Layer 3 is verification, runtime and formal, with the examples run videos, TLA+, Lean and Bombadil. The narrowest, at the bottom, layer 4, is prose that needs judgement: rules, skills and AGENTS.md, kept to a minimum.](/agentpr-pyramid-en.svg)

_The talk's trust pyramid, redrawn. The wider the layer, the more time it deserves._

In practice this order tends to get flipped. When an agent makes a mistake, someone adds one more "don't do this" line to AGENTS.md, and the file keeps growing until it runs to hundreds of lines. Tan's rule runs the other way: with every correction, first ask whether it can become a deterministic check. A rule that lives in code gives the same result every time, while a rule written in prose has to be read and interpreted by the agent, so the outcome varies.

## 2. Agents copy what is already in the codebase

An agent's output follows its input, and the biggest part of that input is the codebase. In 2024, Tan says, she would arrive at work and review the three pull requests her colleagues had written; today the number is closer to 300. Each engineer now runs a team of hundreds of agents, so code no longer arrives a few pull requests at a time but as something close to a continuous stream.

She compares this to a garden. The constraints and guardrails in the codebase are the concrete foundations, and the new code agents write grows around them. Any workarounds, anti-patterns, deprecated code or tech debt left lying around look to the next agent like the established pattern, so it copies them, and they spread like weeds before anyone notices.

My own version of the picture is a kitchen where 300 part-time cooks work at once, quick with their hands but learning by watching. They take whatever is in the fridge and copy whatever the person next to them is doing, so one spoiled ingredient ends up in 300 plates. Throwing it out of the fridge works better than taping a "do not use" note to the wall.

## 3. Once a lint rule blocks it, review never has to catch it

A linter reads code without running it and flags any pattern the team has banned. It is a bit like a spell checker in a word processor, except the team writes the rules. Common tools are ESLint for JavaScript and TypeScript, and Ruff or Pylint for Python.

Violations show up as red underlines in the editor and as failures in the CI checks that run when a pull request is opened, so a pull request that breaks a rule cannot be merged. If type checking catches mistakes in data types and tests check what the code does when it runs, linting catches the shape of code that the team has decided not to write.

The Grok Bot team applied this through Dune, its own client framework. Tan describes it as something like Next.js for Electron apps and says it is not technically interesting; what matters is that the lessons the team learned building desktop apps are encoded in it as constraints and lint rules. One of those lessons is that anything that needs nuance to use well tends to end up as slop, code that works but is full of patches and excuses.

React's useEffect, the hook for running side effects, is her example. It has its uses, but it is misused far more often than not, and agents are bad at it. The team banned it in product code and allowed it only in a few places inside Dune's own APIs, and the problem has not needed catching in code review since.

At Cursor, another Electron app, agents often imported main-process code into the renderer, the part that draws the screen, causing long tasks and jank. In Grok Bot and Dune the two top-level directories are literally called electron-main and electron-renderer, so the folder structure itself carries the rule, and imports between them are blocked by a dependency graph analyser and lint rules. Written with ESLint's built-in rules, the same constraint looks roughly like this; it is an example built for this post, not a slide from the talk.

```js
// eslint.config.js
export default [
  {
    files: ["src/electron-renderer/**"],
    rules: {
      "no-restricted-imports": ["error", {
        patterns: [{
          group: ["**/electron-main/**"],
          message: "Don't import main-process code into the renderer. Send a request over a channel in ipc.ts.",
        }],
      }],
    },
  },
];
```

An agent that breaks the rule gets this message back.

```
src/electron-renderer/chat.tsx
  3:1  error  Don't import main-process code into the renderer. Send a request over a channel in ipc.ts.  no-restricted-imports
```

The error message deserves attention. To a person it is a warning, but to an agent it is an instruction about what to do next, so a message that says why the code was blocked and what to use instead sends the agent straight back onto the right path. Put the same sentence in AGENTS.md and the agent has to decide whether to follow it; turn it into a lint rule and a pull request that ignores it simply does not pass.

## 4. An agent's comments become the next agent's excuse

The surprising part of the talk is how agents treat markdown and comments. They use documentation, code comments, rules and skills as a place to write down why they did not do the right thing, and they also over-rotate on a small correction, treating it as a hard rule that can never be broken again.

The example comes from Cursor. Agents loved imperative timers such as setTimeout, requestAnimationFrame and requestIdleCallback as quick fixes, when what they were really doing was papering over a clash between VS Code's imperative style and React's declarative one. Tan explains that timers created and destroyed in rapid succession cause a lot of major garbage collection, which makes the app lag.

Each time, the agents left a comment justifying the patch, and the next agent read the comment and applied the same patch. Before long timers had spread everywhere and the app's performance suffered badly.

Having learned that lesson, the Grok Bot team banned 99% of comments. Comments go stale quickly, people rarely read them anyway, and they give agents an escape hatch from the hard fix. Above all they cannot be enforced, so even a well-meant note telling the next agent not to do something is nothing you can trust. Lint rules now do that job, with error messages that tell the agent to fix the root cause rather than patch around it.

Every time the team corrects an agent, the correction becomes a deterministic check, or the API design and architecture change so the problem cannot arise at all. Do this often enough and there is less and less to look for in review, until at some point there is nothing left and agents can merge most of their own pull requests.

In a codebase already full of patches, the order matters. The talk recommends starting with a lint rule that stops new occurrences of an anti-pattern and then cleaning up the old ones. If existing violations go into an exceptions list when the rule is switched on, and agents work that list down bit by bit, the rule and the cleanup can proceed separately. A class of problem that has been blocked once cannot come back in, so the codebase only moves in one direction, like a ratchet.

## 5. Review looks at evidence instead of code

Verification is the other axis that makes agents more autonomous and their work more trustworthy. Much of the Grok Bot team's code review has turned into looking at verification artefacts: videos, screenshots and diagrams the agents produce, and the results of formal verification.

The basic form is runtime verification, which lets an agent run the code itself and use the same debugging tools human developers use, such as the Chrome DevTools Protocol. The verification skill includes a feature map, a sitemap-style list of everything the app can do from the user's point of view. When someone says "the thing in the left sidebar", the agent does not have to guess, and people and agents call each feature by the same name.

The skill also ships custom CLIs that launch and drive the app, so agents call the same driver every time instead of writing new scripts for each check. That cuts token use, and the CLI itself can be tested.

The team has recently started on formal verification too, model checking large user flows such as notifications across devices and platforms with TLA+. TLA+ is a specification language that lays out every state a system can pass through and searches for cases where a desired property breaks. Lean, a language in which a computer checks proofs, is used on the team's own virtualisation library, which draws only the visible part of a long list, to prove that it does not flicker or jitter. Formal verification has already found a fair number of bugs, but it is no silver bullet, and the team treats it as one more layer in the agents' environment.

For the UI, the team runs property-based tests with Bombadil, an open-source tool from Antithesis. It explores the app on its own and checks properties such as "this condition always holds", and it has caught a few UI bugs as well.

Tan quotes a developer named Cindy who said six months ago that she could not trust her agents because subtle bugs kept getting merged. Cindy now spends 70% of her daily tokens on verification, and Tan says most of her own tokens go there too. None of these techniques are new. They are ordinary software engineering tools that used to be too expensive to understand, write and maintain, and because agents cut that cost so sharply, Tan calls this a golden age of testing and verification.

Put together, the path one pull request takes looks like this.

![Five stages a pull request passes through. An agent opens a pull request, which goes through automatic checks made of lint, types and tests, and is rejected automatically if it fails. If it passes, the agent runs the app itself and records videos and screenshots, a person reviews the evidence rather than every line, and with nothing left to review it merges. A dashed arrow from the human review stage back to the checks stage reads: anything a person catches becomes an automatic check next time.](/agentpr-flow-en.svg)

_The talk's approach redrawn as the path of a single pull request. The dashed arrow is the loop that keeps shrinking what is left to review._

Automation goes on top once these foundations are in place. Now, whenever the team cuts a new release, Grok Bot spins up a new Cursor project whose agents fuzz the whole app by using it like a real user. For each bug they find they open a fix and merge it automatically. The talk's warning is that doing this in the wrong order, automating a loop that produces slop, only produces more slop and burns ever more tokens covering it up.

## 6. Bringing it to data and financial code

Applied to modelling and financial code, the first places to work on are money and time. Calculating amounts in floating point lets rounding errors pile up, so amounts should only be handled through a dedicated type such as Money, and putting a bare number into an amount field should fail type checking. It is the same structure as keeping useEffect inside Dune: wrap the hard calculation in one place and leave the rest of the code a single easy path.

On the time side, a common accident in credit models is data leakage, where training uses information that would not have been known at that point in time. If feature code cannot read the current time directly and has to take an as-of date as an argument, there are fewer places for that mistake to creep in. Team-specific bans like this are a job for a tool where you can write your own rules, such as Semgrep, with an error message that names the function to use instead. The rule below is simplified to show the idea; a real one would list every clock function the team's code uses.

```yaml
rules:
  - id: no-wall-clock-in-features
    languages: [python]
    severity: ERROR
    paths:
      include: ["features/"]
    pattern-either:
      - pattern: datetime.datetime.now(...)
      - pattern: datetime.date.today()
      - pattern: pandas.Timestamp.now(...)
      - pattern: pandas.Timestamp.today(...)
      - pattern: time.time()
    message: "Don't read the current time in feature code. Take an as_of argument and use the functions in asof.py."
```

Folder boundaries can be enforced with import-linter. Split features, models and serving, and stop serving code from importing research notebook utilities, and an agent dragging a line of experimental code onto the production path gets caught before review. On the verification side, pandera can enforce schemas on input and output data, and a pull request that changes a model should carry backtest results, such as KS by period or the change in approval rate, as its evidence rather than a code diff.

## 7. My take

What stays with me longer than the 11,000 is the habit of turning corrections into checks. Automatic merging is what the team earned after months of that habit, and treating it as the goal from day one gets the order backwards. The rules in Dune were also written by people who had lived through renderer jank and timer patches at Cursor. The expertise has not disappeared; it has moved out of review comments and into rules and APIs.

The numbers deserve some caution. The pull request count and the revert rate are figures the team reported itself, and a revert rate is not a bug rate. Problems are often fixed forward with a new pull request rather than reverted, and if every release triggers fuzzing that opens and auto-merges a fix for each bug found, a good share of the 11,000 are likely to be bug fixes. Even so, app performance improving rather than degrading while the pull request count grew this much is fairly strong evidence.

When bringing this into financial code I would draw one line. In a desktop app a 0.5% revert rate can be cleaned up in the next day's release, but in code that moves money, such as payments, limits or settlement, a single error turns straight into customer losses and complaints. Those paths should keep a human approval step even after every check and piece of evidence is in place, though what that person reads should be the check results and the evidence rather than every line of code.

My [recent post on the risk function](/en/agent-bank-risk-function/) has the same structure. There, a second line that could no longer approve decisions one by one had to move to managing the system that makes the decisions and the records it keeps, and a development team that can no longer read pull requests one by one is going down the same road.

If you have given an agent the same correction twice this week, a good place to start is turning it into one lint rule with a helpful error message instead of adding another line to AGENTS.md.

---

**Related posts:**

- [Productivity in AI Coding Comes from Decomposition and Feedback Loops, Not Better Prompts](/en/ai-coding-workflow/)
- [Better Agents Come From a Better Harness, Not a Better Prompt](/en/ai-harness-engineering/)
- [What the Risk Function Has to Change When AI Agents Run Bank Work](/en/agent-bank-risk-function/)

## References

- [All Code Is Slop (Except Mine), Lauren Tan (AI Engineer, YouTube, 14 November 2026)](https://www.youtube.com/watch?v=O_zcc6Xl12g)
- [Introducing Grok Bot (SpaceXSI, 11 August 2026)](https://x.ai/news/introducing-grok-bot)
- [pstack: the speaker's Cursor plugin (GitHub)](https://github.com/cursor/plugins/tree/main/pstack)
- [Bombadil: Property-based testing for web UIs (Antithesis, GitHub)](https://github.com/antithesishq/bombadil)
- [no-restricted-imports (ESLint documentation)](https://eslint.org/docs/latest/rules/no-restricted-imports)
- [Rule syntax (Semgrep documentation)](https://semgrep.dev/docs/writing-rules/rule-syntax)
- [Import Linter (documentation)](https://import-linter.readthedocs.io/)

_This post is based on the published talk and official sources as of 16 November 2026. The pull request count, revert rate, contributor count and share of tokens are figures given by the speaker. The ESLint and Semgrep configurations and the financial code examples were built for illustration._
