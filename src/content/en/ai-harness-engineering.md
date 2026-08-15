---
title: "Better Agents Come From a Better Harness, Not a Better Prompt"
description: "How to turn a failing agent into a working one without touching the prompt once. What harness engineering is, and why it matters more than prompt engineering the moment an agent leaves the demo."
pubDatetime: 2026-05-21T03:00:00Z
koSlug: ai-harness-engineering
tags:
  - ai-agent
  - llm
  - harness
  - engineering
---

## What is an AI harness?

The plain version: it is the runtime that keeps a model from spinning off into nothing.

The model itself is a black box. It is non-deterministic and it can make a strange call at any point. So a harness wraps a set of things around it.

- **Tool registry** — the set of tools the model is allowed to reach for
- **Context management** — compaction, keeping the recent messages that matter
- **Guardrails** — max iterations, max tool calls, failure conditions
- **Agent loop** — the think-then-call cycle the model runs in
- **Verification step** — did the thing actually succeed?
- **Deterministic handlers** — login, auth, file access, and anything else too risky to leave to the model

So a harness does not make a model smarter. It makes a model safe to work with **while it is still wrong sometimes**.

## The example that makes it click

Take a deliberately weak model — GPT-3.5 Turbo — and build a browser agent whose job is to upvote the first post on Hacker News.

At first the agent tries to click upvote, gets bounced to the login page, and then reports back that it succeeded. It did not succeed. It just said it did.

Now, without editing the prompt at all, add harness pieces.

1. **Guardrail** — stop it from looping forever
2. **Context compaction** — keep the essentials as the message history grows
3. **Verify step** — check whether the upvote actually registered
4. **Login handler** — when the agent lands on the login page, the harness logs in itself

Same prompt. The agent now logs in and upvotes for real.

## The line worth keeping

> "I did not touch the prompt once."

When an agent fails, the first instinct for most people is to write a firmer prompt. The claim here runs the other way.

**The problem may not be the prompt. It may be the runtime.**

If you want agents in production, there is something that matters more than prompt engineering, and it is **harness engineering**.

## What this means in practice

### A good agent comes from a good runtime, not a good prompt

Prompts have a ceiling. The model will tell you it did the thing when it did not. So a real system needs all of this around it:

- execution logs
- verification logic
- failure detection
- retry conditions
- stop conditions
- permissions and security handling
- a deterministic fallback

Without these, an agent looks great in a demo and is dangerous in production.

### A weak model plus a strong harness can be enough

The choice of GPT-3.5 Turbo is not incidental — it is the whole point. **A small model with a strong harness** can beat paying for a frontier model, especially on cost.

That trade matters even more inside a company:

- keeping internal data in-house
- cutting inference spend
- automating repetitive work
- shaping the runtime around one specific job

Seen this way, harness design moves the needle more than model choice does.

### Whatever the agent must not do, the harness does

Login, authentication, payments, permission checks, access to sensitive data — none of these should be left to the model's discretion.

Not "figure out how to log in," but a deterministic handler that logs in.

**The model handles judgement and planning. The harness handles execution safety and security.** That split is the useful one.

## Applied to a text-to-SQL agent

The same lens transfers directly.

A user asks for last month's revenue trend, and the model writes SQL. At production level that is nowhere near enough. The harness you actually need looks like:

- a whitelist of queryable tables
- restricted access to sensitive columns
- a dry run before execution
- a spend ceiling
- an enforced row limit
- result validation
- detection of stale or wrong metric definitions
- a consistency check against previous queries
- confirmation that the result matches what the user meant
- a rewrite loop on failure

Which reframes the question. "Can the LLM write good SQL?" is the smaller one. The bigger one:

> **When the LLM is wrong, does the system fail safely, catch it, and correct it?**

## One line

An AI harness is not a structure built on trusting the model. It is an operating framework that lets you **doubt the model and still ship**.

The next edge in agents is not a better prompt. It is the ability to design the harness — verification, tools, context, permissions, failure handling, all of it.

---

Source: [conference talk on YouTube](https://youtu.be/C_GG5g38vLU)
