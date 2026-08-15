---
title: "Context Compaction: Don't Give the Agent Everything, Give It What's Left Over"
description: "You cannot hand an agent the whole conversation, every log and every tool result on each turn. Working through the compaction techniques that keep the task state a model needs for its next decision and drop the rest."
pubDatetime: 2026-05-22T09:00:00Z
koSlug: context-compaction
tags:
  - context
  - llm
  - ai-agent
  - harness
  - engineering
---

## The problem: the conversation outgrows the window

An agent does not finish in one shot. It calls a tool, reads the result, decides again, calls another. Repeat that a few dozen times and the transcript blows past the model's context window.

Even when it still fits, you have a problem. Junk logs crowd out the information that matters, and cost and latency get worse along the way.

Hence context compaction. The idea in one line:

> Keep what the next decision needs. Drop the rest.

Worth separating this from **prompt compression**, which is a different thing — techniques like LLMLingua that shrink text at the token level. What follows is about managing an agent's conversation and task state.

The crudest version keeps the system prompt and the user's request, throws away the middle, and holds on to the last few messages.

Before:

```
[System Prompt]
[User Task]
... a pile of old intermediate logs ...
[Recent message 1]
[Recent message 2]
```

After:

```
[System Prompt]
[User Task]
[Recent message 1]
[Recent message 2]
```

That is the skeleton. In practice you want more than this. Step by step.

## 1. Sliding window

The simplest approach. If the agent has made twenty tool calls, keep the last five instead of all twenty.

```
Keep:
- system prompt
- original user goal
- last 5 messages

Drop:
- old observations
- repeated tool logs
- irrelevant failed attempts
```

Fast and simple. The downside is that important old information leaves with the noise — a constraint agreed on at step three simply gets forgotten.

## 2. Summarisation

Instead of discarding the middle, compress it.

Original log:

```
1. Agent opened Hacker News.
2. Agent clicked upvote.
3. Redirected to login page.
4. Agent said success, but URL was /login.
5. Verification failed.
```

Compacted:

```
Summary so far:
- Agent opened Hacker News.
- Clicking upvote redirected to the login page.
- The earlier claim of success was false.
- Next attempt must handle login, then verify the upvote.
```

Much more practical than a sliding window, because what was tried and what failed survives.

## 3. Structured state

Inside an agent system, structured fields beat free-form summary.

```json
{
  "goal": "Upvote the first Hacker News story",
  "current_state": "Redirected to login page",
  "known_failures": [
    "Agent falsely claimed success after clicking upvote"
  ],
  "required_next_action": "Handle login, then retry upvote",
  "verification_rule": "Confirm story is actually upvoted"
}
```

The reason this is better: there is less room for the model to misread itself later. A prose summary can be interpreted loosely. A field reads as what it is.

## 4. Compacting tool results

In practice the biggest context hog is usually tool output. SQL results, PDF search hits, browser DOM, API responses.

Raw:

```
SELECT * FROM transactions WHERE event_date BETWEEN '2026-05-01' AND '2026-05-20';
-- 128,492 rows returned
id | event_date | amount | status | ...
... (thousands of lines omitted) ...
```

Compacted:

```
Query result summary:
- Date range: 2026-05-01 ~ 2026-05-20
- Total transactions: 128,492
- Approval rate: 94.2%
- Main anomaly: 2026-05-13 approval rate dropped to 87.1%
- Likely related segment: mobile wallet, new users
```

What the agent needs is not the raw result. It is the observation it will use for the next decision.

## 5. Memory snapshot

On long-running work, keep a single live status board instead of replaying the conversation.

```
Current task state:
- Objective: Build a fraud monitoring dashboard
- Completed: Metric definition, data source mapping
- Pending: Alert threshold logic
- Constraints: Use event_date, exclude 3DS fail cases
- User preference: Keep report simple and business-readable
```

The conversation keeps moving; you only keep this board current. It matters most for the agents that run long — coding agents, research agents.

## 6. What you must never drop

Compaction is not about cutting for the sake of cutting. It is about knowing what is safe to lose.

Keep:

```
1. The original goal
2. User constraints
3. Decisions already made
4. Failed attempts and why they failed
5. Current state
6. The next action
7. Verification criteria
8. Permission and security conditions
```

Safe to drop:

```
1. Repeated tool logs
2. Long raw output
3. Search results already summarised
4. Failed detours with nothing to teach
5. The model's own rambling reasoning traces
```

Item four in the keep list is the one people lose most often. Drop **failed attempts and why they failed** and the agent walks into the same wall again.

## 7. A place to put it: compress_context()

Giving the harness a single `compress_context()` function keeps this tidy.

```python
def compress_context(messages):
    system = keep_system_prompt(messages)
    user_goal = keep_original_user_task(messages)
    recent = keep_recent_messages(messages, n=5)
    summary = summarize_old_messages(messages)

    return [
        system,
        user_goal,
        summary,
        *recent,
    ]
```

A better shape carries state around instead of conversation.

```python
compressed_context = {
    "goal": original_goal,
    "constraints": extracted_constraints,
    "state": current_state,
    "completed_steps": completed_steps,
    "failed_attempts": failed_attempts,
    "open_questions": open_questions,
    "next_action": suggested_next_action,
    "recent_messages": recent_messages,
}
```

Decide when to fire it too. A common trigger is token use crossing a threshold — say 70% of the context window.

## The point

Context compaction is not "make it shorter." More precisely:

> Preserve the task state the agent needs to decide its next move, and remove only the conversation and logs that do not serve it.

Which means a good compaction output reads less like a summary and more like a **save file**. From that one artefact the agent should be able to reconstruct what it was doing and what comes next.

For an agent doing a refactor, that board looks like this rather than fifty turns of transcript:

```
User intent:
Refactor the legacy callback code in the payments module to async/await

Settled decisions:
- Do not change external API signatures
- Existing unit tests must pass unchanged

Current step:
- payment_service.py refactored
- webhook_handler.py in progress

Remaining:
- Run integration tests
- Review error handling paths

Verification:
- Full test suite green
- Callback latency within ±5% of before
```

Passing that one board instead of fifty raw turns — that is context compaction.

---

**Related reading:** [Better Agents Come From a Better Harness, Not a Better Prompt](/en/ai-harness-engineering/)
