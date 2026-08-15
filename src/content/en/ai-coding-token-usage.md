---
title: "Where Does AI Coding Tool Usage Get Recorded? The Four Tokens ccusage Shows You"
description: "Coding agents like Claude Code and Codex leave a usage log on your machine every time they work. ccusage reads those logs and reports four numbers — Input, Output, Reasoning, Cache Read. What each one means, why cache reads are counted separately from input, and whether that cache lives on your laptop or on a server."
pubDatetime: 2026-06-06T03:00:00Z
koSlug: ai-coding-token-usage
tags:
  - ai-coding
  - claude-code
  - codex
  - tokens
  - ccusage
  - developer-tools
---

## 1. "How much have I actually used?"

Use Claude Code or Codex for a while and the thought arrives on its own: how much have I actually used?

From the outside it looks like you asked a question in a chat box and got an answer back. Underneath, quite a lot moves. Your request, the file contents the model read, the token counts used to produce the answer, the model name, the execution time — all of it gets written to a log on your own machine.

One of the tools that reads those logs and reports usage is [ccusage](https://github.com/ryoppippi/ccusage). It is not a new monitor watching over your shoulder; it reads records that are already sitting on your disk and lays them out legibly — token usage and estimated cost by day, by month, by session.

Run it against Codex usage and you get something like this.

```
Codex total
  Input:        1,961,781
  Output:          50,986
  Reasoning:        9,965
  Cache Read:  14,458,496
  Total:       16,471,263 tokens
```

The numbers are large, but there are only four words. **Input, Output, Reasoning, Cache Read.** One short SQL question is enough to unpack all of them.

A note on units: these are tokens. A token is roughly the smallest unit an AI reads and writes in, and it does not line up neatly with a character or a word. English tends to split into word fragments; other languages often split a single word across several tokens. Think of it as the pieces a sentence gets chopped into so the model can compute over it.

## 2. A one-line question is not really one line

Say you throw this at a coding agent.

```
Write a SQL query that sums order amounts per customer over the last 7 days from the orders table.
```

To a human that is one sentence. But Codex or Claude Code does not send that alone to the model. Typically it bundles something like this.

```
System instructions: You are a coding agent. Follow existing style when editing code.

User question: Write a SQL query that sums order amounts per customer over the last 7 days from the orders table.

Project info: This project uses PostgreSQL.

Relevant schema:
  orders(id, customer_id, total_amount, created_at)
  customers(id, name, email)

Earlier conversation: the user has said they want date conditions handled in KST.
```

The model reads all of that, then produces an answer. Something like:

```sql
SELECT
  c.id   AS customer_id,
  c.name AS customer_name,
  SUM(o.total_amount) AS total_order_amount
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.created_at >= NOW() - INTERVAL '7 days'
GROUP BY c.id, c.name
ORDER BY total_order_amount DESC;
```

Usage from that single exchange breaks into the four buckets above.

## 3. Input, Output, Reasoning — what went in, what came out, what it chewed on

**Input** is everything the model read in order to produce this answer. In the example: system instructions, project info, DB schema, prior conversation, the user's question. In real work you can add relevant source files, tool execution results, and error logs. Which is why you type one line — "write me some SQL" — and see thousands or tens of thousands of input tokens.

**Output** is what the model newly wrote. Here, the SELECT statement plus whatever explanation comes with it. The more it explains and the more code it generates, the larger this gets. Answer with "this one line will do" and output stays small.

**Reasoning** is the internal thinking tokens spent getting to the answer. For the SQL above, something roughly like this is turning over inside the model.

```
The last-7-days condition goes on created_at.
Per-customer totals means GROUP BY customer_id.
To show customer names I need to JOIN customers.
The sum is SUM(total_amount).
Descending by total is the natural ordering.
```

That train of thought is not shown to you directly. The computation still happens, though, and some models and tools record its volume as a separate Reasoning count. Depending on the model this value may not appear at all, or may read as zero. It grows with tasks that involve many steps of thought — complex code analysis, comparing several files, debugging.

Summed up in one line: Input is what the model read, Output is what it wrote, Reasoning is the calculation it turned over in between.

## 4. So isn't Cache Read just Input?

The natural objection: if the model saw those cached tokens too, aren't they input?

Logically, yes. In the broad sense they are part of input — context the model consulted while producing an answer. They are counted separately because they are processed differently and priced differently.

Unpack it a little. Say the first request carried this.

```
system instructions   5,000 tokens
project schema       10,000 tokens
user question           100 tokens
```

The first time, the model server processes that prefix fresh. It reads and works through it once.

Then a second request arrives.

```
Now change it to aggregate by month instead.
```

The question is a single 100-token line, but the system instructions and project schema in front of it are essentially unchanged. The provider's server notices that the prefix matches what it saw a moment ago and reuses the already-processed result. Those reused tokens are counted as **Cache Read**. The picture:

```
the newly arrived question           → Input
reused instructions and schema       → Cache Read
the newly written SQL                → Output
```

So when ccusage shows a Cache Read figure like 14,458,496, and most of it is cache reuse, the amount of genuinely new processing the model did is nowhere near that large. Cached read tokens are priced far below ordinary input tokens. OpenAI describes prompt caching as a way to process repeated prompts faster and more cheaply, with `cached_tokens` reported separately in the usage response ([OpenAI Prompt Caching](https://platform.openai.com/docs/guides/prompt-caching)). Anthropic's usage report likewise breaks out `uncached_input_tokens`, `cache_creation`, `cache_read_input_tokens` and `output_tokens` in separate columns ([Anthropic Usage Report](https://docs.anthropic.com/en/api/admin-api/usage-cost/get-messages-usage-report)).

Put differently, Cache Read is part of the input the model saw, but it is input that was *processed earlier and reused*, not input processed this time. So it gets its own column in pricing and reporting.

## 5. Is that cache my computer's memory?

Here is a spot where it is easy to get confused. Does Cache Read mean something was read out of my MacBook's RAM or disk cache?

Mostly, no. The cache in question is the prompt cache on the provider's servers. Not something stored on your machine — closer to "the prompt prefix Anthropic or OpenAI processed recently and is briefly holding onto."

It is cleaner to keep two layers apart. What lands on your machine is the **local log** — the `.jsonl` files Claude Code and Codex write as they work, which is what ccusage reads. Where the cache read actually happens is the **prompt cache** on the model server. A local log line reading "Cache Read 1,234,567 tokens" does not mean your computer read from a cache. It means the server-side cache did its job and reported the result as usage, which then got written into your log.

## 6. So where do Claude Code and Codex actually run?

One more source of confusion. Do Claude Code and Codex use my computer's resources at all?

They do — but both sides are in play. The tool itself is a program running on your machine; the model normally runs in the cloud.

What happens locally is roughly: a terminal or app starts, project files are found and read, code gets edited, commands get executed, results get written to logs, tool use gets controlled. What happens on the model server is: the prompt is understood, code is analysed, an answer is produced, reasoning is spent, tokens are counted, the prompt cache is worked. A model the size of Claude Opus or a GPT-class model is not running inside your laptop.

Ask "improve the performance of this SQL query" and the local tool first gathers `schema.sql`, `query.sql`, the relevant README, execution logs. That bundle goes to the model server. The model analyses it there and produces an answer. The answer comes back to your machine, and Claude Code or Codex takes it and edits files or runs commands.

So the token usage ccusage shows is model processing that happened server-side, with only the result recorded locally. ccusage reads that record back and tidies it up for you.

## 7. Not the same thing as ChatGPT's "memory"

A related question comes up on the ChatGPT side. ChatGPT has a feature called "memory," and by name alone it can sound like Cache Read. They are different concepts.

ChatGPT memory is a personalisation feature — it carries preferences, your name, how you work, useful details from past conversations into later ones ([OpenAI Memory FAQ](https://help.openai.com/en/articles/8590148-memory-faq)). It remembers things like "this user prefers answers in Korean," "this user likes SQL examples," "this user writes blog posts in a plain declarative style." A product feature.

Cache Read, by contrast, is a prompt cache that lets the model server handle the repeated portion of a long prompt faster and cheaper. It is not storing facts about you; it is an optimisation so the model does not reprocess the same system instructions or the same schema from scratch every time. Similar name, different job.

Something like caching is very likely running inside the ChatGPT web UI as well. What is hard is pulling input, output and cache-read tokens out locally the way ccusage does, because the web UI does not leave a detailed per-session record on your machine the way Claude Code and Codex do.

## 8. Next time you open ccusage

With that laid out once, the big numbers are far less dizzying the next time.

Tools like Claude Code and Codex log usage locally as they work, and ccusage reads it back as four figures. Input is how much material the model read to produce this answer, Output is how much text and code it wrote, Reasoning is how much calculation it turned over internally, and Cache Read is how much input was reused from the server-side prompt cache. The tool runs on your machine, but the model's brain mostly runs in the cloud — which is why Cache Read is a story about a server cache, not your RAM.

Raising cache hit rates, and the open-source tooling for cutting token spend, are topics of their own. Just knowing what each number means makes the next ccusage screen a lot easier to read.

---

## References

- [ccusage — Claude Code / Codex usage reporter (GitHub)](https://github.com/ryoppippi/ccusage)
- [Prompt caching — OpenAI Platform Docs](https://platform.openai.com/docs/guides/prompt-caching)
- [Messages usage report — Anthropic Admin API](https://docs.anthropic.com/en/api/admin-api/usage-cost/get-messages-usage-report)
- [Memory FAQ — OpenAI Help](https://help.openai.com/en/articles/8590148-memory-faq)
