---
title: "How Do You Grade an LLM? Eleven Evaluation Methods, Sorted into Four Families"
description: "LLM evaluation starts diverging the moment a correct answer scores zero. From BLEU, ROUGE and BERTScore through LLM judges and juries to agent trajectory scoring and safety gates — eleven methods grouped into four families, with what each is for and where each falls over."
pubDatetime: 2026-07-25T23:00:00Z
koSlug: llm-evaluation-methods
tags:
  - llm
  - machine-learning
  - engineering
  - ai-agent
---

Back when I was building classifiers, "did it work?" was not a hard question. The answer was fixed, so you counted right and wrong, threw out an accuracy or an F1, and the conversation was over. Then I started shipping features with an LLM in them and it got awkward fast. Was that a good summary? Is the tone of that reply all right? Did the agent actually do its job? All I had was "seems fine?" I would eyeball twenty outputs, decide they looked okay, and move on — and I knew perfectly well that calling this evaluation was a stretch.

So I sat down and worked through the evaluation methods. The trouble is that the names tell you nothing about how they relate. BLEU, ROUGE, G-Eval, DAG — they all look like they belong to separate universes. After staring at them for a while I grouped them into four clusters of my own, and only then did a map appear. These are those notes: what each one treats as ground truth, when to use it, and where it falls over.

## 1. A correct answer that scores zero?

One example is enough to see why there are so many methods.

![The moment the same meaning scores zero](/eval-why-hard-en.svg)

_The same answer scores zero or full marks depending on the grader._

Ask "what is the capital of France?" and the model says "France's capital? Paris, of course." To a human that is a faultless answer. But if the reference reads "Paris is the capital of France" and the grading method is word overlap, that answer scores close to zero. Different word order, different phrasing.

Traditional machine learning rarely runs into this, because spam or not, churn or not, the answer lands cleanly. Natural language has dozens of ways to carry the same meaning, and what even counts as a good answer changes with the situation. In summarisation, not leaving things out matters. In translation, exact phrasing matters. In a support reply, tone matters. One yardstick cannot measure all of it.

So having many methods is not because one is best and the rest are inferior. Each rests on a different assumption about what ground truth is, which means they are answering different questions to begin with. See that and there is much less to memorise.

## 2. Four clusters

Group the eleven by what they treat as the basis for correctness and it comes out like this.

![Eleven LLM evaluation methods grouped into four families](/eval-map-en.svg)

_The families split on one question: what counts as the ground truth?_

Compare against a reference. Hand the grading to another model. Have people or rules nail the standard down. And look at how the system ran rather than at the answer. Going down, the question shifts from "did it get it right" to "does this work as a product." One at a time.

## 3. Comparing against a reference

The oldest and the easiest to grasp. Write a model answer in advance and count how far the model's output strays from it. The three in this family stay straight in your head if you remember them by arrow direction.

![Three ways of comparing against a reference](/eval-reference-based-en.svg)

_BLEU asks from the answer toward the reference; ROUGE asks from the reference toward the answer._

**BLEU** asks from the model's output. "This phrasing you used — is it in the reference?" That is precision. Use it where the answer is nearly fixed, like translation. It carries a length penalty so a model cannot game it by writing short and dodging risk, and the standard practice is to compute it over a whole corpus rather than averaging per-sentence scores. Where several answers are legitimate, supply several references.

**ROUGE** points the other way. From the reference: "this content here — is it in your answer?" That is recall. Use it where leaving something out hurts more than padding does, like summarisation or information extraction. Recall alone rewards length, so read it alongside a precision metric. Variants like ROUGE-L forgive some reordering.

**BERTScore** exists to catch what the other two miss. It compares in embedding space — meaning — rather than characters. Which is how "Paris, of course" gets counted as correct. The catch is that its scores bunch into a narrow band at the high end, so a number like 0.85 must not be read as if it were accuracy. Use it comparatively: model A scores higher than model B. And check that the embedding model suits your domain and language.

By this point the limit is visible. All three need a reference, and most real tasks are ones where you cannot build one. How would you write a reference answer for whether a support reply was polite enough?

## 4. Handing the grading to a model

Without a reference the fallback is human grading, and humans are slow and expensive. Hence the approach of handing the grading to a different LLM entirely.

![Three ways of handing grading to a model](/eval-judge-pipeline-en.svg)

_Unfold criteria into steps and score, pit two against each other and pick a winner, or pool several judges._

**G-Eval** takes your evaluation criteria, has the judge model unfold them into grading steps, then walks the steps one at a time assigning a score. Use it for subjective criteria with no reference — tone, instruction-following. One practical note here: write the criterion as an adjective ("must be friendly") and scores wobble; write it as a checklist ("does it contain a sentence restating the customer's question?") and they come out far more consistent. Before I knew that I kept writing criteria abstractly and wondering why the scores would not settle. Run the judge model at a low temperature.

**LLM-as-Judge** is usually used in a pairwise form: set two answers side by side and have the model choose. Absolute scores move between runs, but "which of these two is better" is comparatively stable, which makes it practical for comparing two models or two prompt versions.

**An LLM jury** runs several judges separately and averages their scores, because any single judge has consistent habits. One thing matters here: running the same model three times is not a jury. You have to mix models from different families. And several small models beating one large one is a fairly common outcome.

### But the grader is a model too

The thing to watch most carefully in this family is the judge's habits. Three of them are well documented.

![Three habits of judge models](/eval-judge-bias-en.svg)

_Order, length, own-family preference. None of the three disappear by averaging over runs._

A judge model picks the answer shown first more often, gives higher scores to longer answers even when the content is no better, and favours answers written by models from its own family. Hence the advice: randomise A/B order, control for length, and build juries from different families.

One thing worth pressing on. These three are not noise; they are a lean in one direction. Noise cancels when you average over runs. A lean survives averaging — and you end up with a wrong score held more confidently for having been repeated. The thing everyone learns in statistics, that variance and bias are different problems, applies exactly here. So adopting a judge model requires first building a small human-graded set and checking how well the judge's scores agree with it. An extra layer appears: evaluating the evaluator.

## 5. People nailing the standard down

Two things hold you steady when automatic grading wobbles.

**Human evaluation** is ultimately the reference point every automatic metric has to match. Evaluators score against fixed dimensions, and that becomes the calibration set for validating a judge model. It gets used in two places: checking whether a judge can be trusted, and as the last gate before release. The important principles are to fix the rubric before you start, and to measure how much evaluators agree with each other. Low agreement does not mean the evaluators are strange; it means the criteria are vague. Anyone who has run a data-labelling project will recognise this, and it repeats identically here.

**DAG** grades with a decision tree. Each node asks one narrow question, the answer branches to the next node, and a leaf carries the score. Use it for things that must hold: was the format respected, are the required fields present, is the disclaimer there. Because the branching is deterministic, the same input always gets the same score. Put the cheap rule checks near the top of the tree and answers that will fail get filtered before any model call, saving cost too.

## 6. Watching behaviour, not the answer

The character changes here. You are looking at how the system ran rather than at a single line of output. Once you start building agents this becomes mandatory.

**Trajectory accuracy** captures the whole ordered sequence of an agent's thoughts, tool calls and observations, and compares it against the expected path. An example makes the need obvious.

![Two agents with the same result and different paths](/eval-agent-path-en.svg)

_The same final answer can come from completely different processes._

Both produced the same correct answer. One got there cleanly in three steps; the other wandered through twelve, burned four times the tokens, and touched a tool it was not allowed to touch. Score only the result and both get full marks. A lucky answer is covering for a broken execution path, and that kind of thing surfaces only after deployment. So score path and result separately. Note that this requires execution tracing to be in place first — with no record there is no path to grade.

**Multi-turn evaluation** treats a whole conversation as one unit and grades persona consistency, memory of earlier content, and coherence. Grading turn by turn misses failures that only emerge with time: quietly violating a constraint the user set five turns ago, or contradicting something it said earlier. This is only meaningful run against real conversation logs rather than synthetic two-turn examples. Forgetting a rule is a problem that shows up once a conversation gets deep.

**Safety evaluation** runs parallel classifiers for bias, toxicity and PII exposure and flags violations. The most important thing here is not to turn it into a score. Fold safety into an average quality score as one dimension and a violation gets buried when the other numbers are high. One PII leak is not the sort of incident a good average offsets. It belongs as a gate deciding pass or block, not as a term in a mean.

## 7. So what should I use?

Knowing all of this still leaves you stuck when it is time to pick, so here is the order I reason in.

![A guide to choosing an evaluation method](/eval-choose-en.svg)

_The big split is whether a reference exists; the bottom two layers attach whichever route you took._

Start with whether you have a reference. If you do and the wording is nearly fixed, BLEU or ROUGE; if the same meaning can be worded differently, BERTScore. With no reference, the split is what you want to know. Subjective criteria like tone or instruction-following, G-Eval; which of two versions is better, LLM-as-Judge.

And whichever route you took, the bottom two layers attach. Human evaluation as the reference point that makes automatic metrics trustworthy, DAG as the check on format that must hold, safety as a gate. Building an agent adds trajectory accuracy and multi-turn on top.

## 8. A personal view

The biggest thing left after sorting all this out is that in the LLM era, evaluation itself has become a modelling task.

Evaluation used to be closer to a verification step you performed once the model was built. The answer was given, so choosing a metric took little thought, and the arguments happened on the model side. With LLMs the order inverts. Defining what counts as a good answer is itself the work, then moving that definition into a checklist, choosing a grader, correcting the grader's habits, validating against a human-graded set. At that point it is not verification, it is design. And once you use a judge model, the evaluator is itself a trained model, which adds another layer of evaluating the evaluator.

Which is why building a good evaluation set feels like a longer-lived asset than writing a good prompt. Prompts have to be rewritten when the model changes. The standard — "this is what a good answer looks like in our domain" — and the data holding it survive a model change. It becomes the basis for judging whether you can switch models at all. In [an earlier post on harness engineering](/en/ai-harness-engineering/) I argued that the structure outside the model produces the performance; an evaluation set looks like part of that structure.

The other thing that struck me is how the target of evaluation moved from answers to behaviour as we crossed into agents. The era of "as long as the result is right" is over; you have to look at which tools were touched, how many times it wandered, whether it did something it should not have. In human terms, you have gone from reading the final report to reading the work log. As covered in [agentic engineering in financial AI](/en/agentic-engineering-in-finance/), the higher the cost of a mistake, the wider that gap gets.

## 9. If you want to try it yourself

By this point the natural question is what to actually run this with, and fortunately most of it does not need implementing. [Opik](https://github.com/comet-ml/opik), an open-source evaluation and observability tool, has a good number of the metrics covered here built in — reference-based metrics like BLEU, ROUGE and BERTScore, plus G-Eval, LLM juries, trajectory accuracy, conversation-level evaluation and moderation. More usefully, it runs on top of execution traces, which also solves the "you need tracing before you can grade a path" prerequisite mentioned above.

---

**Related posts:**

- [AI Agents Come from a Better Harness, Not a Better Prompt](/en/ai-harness-engineering/)
- [Agentic Engineering in Financial AI](/en/agentic-engineering-in-finance/)
- [Context Compaction: Don't Give the Agent Everything, Keep Only What It Needs](/en/context-compaction/)

## References

- [BLEU: a Method for Automatic Evaluation of Machine Translation (Papineni et al., 2002)](https://aclanthology.org/P02-1040/)
- [ROUGE: A Package for Automatic Evaluation of Summaries (Lin, 2004)](https://aclanthology.org/W04-1013/)
- [BERTScore: Evaluating Text Generation with BERT (Zhang et al., 2020)](https://arxiv.org/abs/1904.09675)
- [G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment (Liu et al., 2023)](https://arxiv.org/abs/2303.16634)
- [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena (Zheng et al., 2023)](https://arxiv.org/abs/2306.05685)
- [Opik — open-source LLM evaluation and observability](https://github.com/comet-ml/opik)

_Compiled from public material as of 25 July 2026. Areas still under active research, such as judge-model bias, may look different from one model generation to the next._
