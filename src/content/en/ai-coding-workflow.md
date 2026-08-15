---
title: "Productivity in AI Coding Comes from Decomposition and Feedback Loops, Not Better Prompts"
description: "Notes from an AI-coding workshop. The point is not that a one-line spec produces working code. It is that you accept the context limits of an LLM, split human judgement from the AI's repetitive execution, and run the work as vertical slices on top of a fast feedback loop."
pubDatetime: 2026-06-06T20:00:00Z
koSlug: ai-coding-workflow
tags:
  - ai-coding
  - claude-code
  - engineering
  - tdd
  - workflow
  - developer-tools
---

In [an earlier post on harness engineering](/en/ai-harness-engineering/) I argued that the next competitive edge for agents is not a better prompt but the ability to design the harness around one. A workshop video made much the same argument, narrowed to coding work, and enough of it transfers directly to real code that it is worth writing down.

## 1. An LLM has a smart zone and a dumb zone

The first thing the speaker points at is that context length itself cuts both ways. Longer context looks like it should mean a smarter model, but past some point the attention relationships get tangled and judgement degrades. Sharp early, increasingly likely to make a wrong call as the session drags on.

Which is why throwing a big task at the model wholesale does not work. You have to cut it into pieces the model can actually hold. The speaker compares an LLM to the protagonist of *Memento*: **accept that it keeps resetting, and design the workflow around that fact.**

In practice this splits two ways.

- Keep compacting and stitching context forward → the longer it gets, the blurrier it gets.
- Clear it out, then re-load only the structured information you actually need → every stretch starts sharp.

The speaker prefers the second. That lines up exactly with the principle from [the context compaction post](/en/context-compaction/) — keep only the working state the next decision needs, drop the rest. Ported to a coding tool: do not drag a session forward with compaction. Clear often, re-lay the information you need, and note that this is also the cheaper path.

## 2. The first thing to do is not coding, it is alignment

One of the biggest failure modes when coding with an AI is misalignment — the human and the model are not looking at the same picture. So the speaker does not jump into plan mode or specs-to-code. First he runs a skill like "grill me" that **makes the AI interrogate the user relentlessly.** Functional requirements, exception cases, design decisions, test criteria — squeezed out one at a time.

The flow he argues against will be familiar.

> write a spec → AI generates code → code looks wrong → edit the spec → generate again

Call it specs-to-code, or vibe coding. His diagnosis is blunt. **The code is the actual battlefield, and this pattern looks away from it.** The AI can write the code, but the developer still has to hold the structure and the design decisions.

## 3. Humans stay on judgement, the AI runs the implementation loop

He splits work into two categories.

**Human-in-the-loop tasks** — requirements, product direction, design calls, domain decisions. Anything a human must be present for. The grill-me session, the PRD, breaking work into issues.

**AFK tasks (away from keyboard)** — anything the AI can grind on while you are not at the desk. Implementation, running tests, typechecking, small refactors.

Planning and alignment need a human. Implementation, once it is cut up properly, can be handed off. The overall shape looks roughly like this.

```
idea
  → AI interrogates the human until requirements align
  → PRD documents the destination
  → Kanban / issues break the work down
  → agents implement AFK
  → tests · typecheck · QA close the feedback loop
```

The picture here is the same conclusion as [the harness engineering post](/en/ai-harness-engineering/). You are not giving the model more freedom. You are laying more precise structure around it.

## 4. The PRD is the destination document, the Kanban is the journey

Once the grill-me session has produced enough alignment, the result gets written up as a PRD (product requirements document). His phrasing is nicely direct: **the PRD is a destination document.** It nails down where we are going. Problem statement, solution, user stories, implementation decisions, testing decisions.

The next step is the interesting one. He deliberately does **not** turn the PRD into a sequential multi-phase plan. Phase 1 → phase 2 → phase 3 is convenient for a single agent working in order, but it cannot express dependencies between tasks accurately.

Instead the work becomes **independent issues on a Kanban board**, with blocking relationships made explicit. That gives you a structure several agents can work in parallel. The PRD says where; the Kanban says how.

## 5. Vertical slices, not horizontal ones

The most immediately useful piece is the vertical slice — or tracer bullet — idea.

Left alone, an AI tends to slice work horizontally.

```
phase 1: all the DB schema
phase 2: all the API
phase 3: all the frontend
```

Go this way and you only find out whether the feature actually works at the very last phase. **The feedback arrives far too late.** You build a long way on top of a wrong assumption, and learn about it afterwards.

What he proposes instead is a thin slice that works end to end. Adding a gamification feature, say: the very first task threads part of the schema, part of the service, and a minimal dashboard UI into one line, so that **something visibly works first.** That way the AI gets feedback fast and does not run a long way in the wrong direction.

When you hand a large feature to an AI, do not split it by layer. Split it into flows that run start to finish, however small.

## 6. Your codebase and your tests set the ceiling on AI coding quality

The last point he presses hardest is codebase quality — **bad codebases make bad agents.** If the structure is a mess, the AI will likely code like a mess. For an AI to code well, the structure has to be legible and the feedback loops — tests, typecheck, lint — have to exist.

He is especially insistent about TDD. Write the test before the AI writes the code, then make it implement against that test, and it becomes much harder for the AI to cheat. Without a feedback loop the AI is effectively coding blind, and **the quality of your tests becomes the ceiling on the quality of its code.**

From a fintech backend seat this lands hard. In payments, settlement, credit scoring — anywhere a wrong output is a direct loss — weak test infrastructure means there is simply no way to verify what the AI wrote. Before adopting AI coding seriously, **testability has to come first**: domain models, dummy data, replayable fixtures, an integration test environment.

## AI coding is a reassembly of fundamentals

The message from one workshop is clear enough. Productivity in AI coding does not come from a better prompt. It comes from cutting work small, shaping it so it can be checked, and separating what a human must judge from what an AI can execute repeatedly.

Align on requirements → document the destination → break it into vertical-slice issues → run a test-backed AFK implementation loop. None of that is new. Small units of work, fast feedback, clear interfaces, solid tests — good software engineering has always said this. What is happening is a reassembly of those fundamentals for a new set of tools.

The next step is fitting this to my own environment. Pre-loading domain questions into a grill-me skill, tuning a PRD template for payment, settlement and risk workflows, working out how to pick the first vertical slice.

---

## Reference

- Original workshop video: [Mastering AI-First Coding (YouTube)](https://www.youtube.com/watch?v=-QFHIoCo-Ko)

**Related posts:**

- [AI Agents Come from a Better Harness, Not a Better Prompt](/en/ai-harness-engineering/)
- [Context Compaction: Don't Give the Agent Everything, Keep Only What It Needs](/en/context-compaction/)
- [Agentic Engineering in Financial AI](/en/agentic-engineering-in-finance/)
