---
title: "Why AI Coding Tools Are Moving to Rust: Copilot, Bun and Codex CLI"
description: "GitHub moved the Copilot runtime from about 430,000 lines of TypeScript to 830,000 lines of Rust in 14.5 weeks, and Bun, which Claude Code runs on, went from 535,000 lines of Zig to Rust in 11 days. What makes Rust different, explained from memory management up, and how AI brought forward a switch that used to be too costly to attempt."
pubDatetime: 2026-10-28T21:00:00Z
koSlug: ai-tools-move-to-rust
tags:
  - ai-coding
  - developer-tools
  - engineering
  - rust
---

In April 2023, data scientist Bojan Tunguz posted on X that "AGI will be built with Python." Elon Musk replied with one word: "Rust". ([X](https://x.com/elonmusk/status/1649603943033450496))

It read like a joke at the time. Then in February this year Musk wrote that xAI's code is mostly Rust and that X is rapidly replacing legacy Twitter Scala code with Rust. ([X](https://x.com/elonmusk/status/2024565280169677297)) Nobody outside the companies can check those numbers, so it is best taken as his own claim.

There are other cases that can be checked. This year GitHub moved Copilot's agent runtime to Rust, and Bun, the JavaScript runtime that Claude Code runs on, was rewritten in Rust. OpenAI's Codex CLI started moving to Rust last year and is now 97% Rust. Here is why AI tools are piling into a language famous for being hard to learn, starting with what Rust actually is.

## 1. Rust handles memory differently

While a program runs, it keeps data in memory and hands that space back when it is done. Who does the handing back, and when, differs from language to language, and that is exactly where Rust parts ways with the others.

![Three ways to clean up memory](/rust-memory-en.svg)

_How a language returns memory shapes much of its character._

In C and C++ the developer does it by hand. That is fast and light, but touch memory that has already been freed, or free it twice, and the program crashes or opens a security hole. Microsoft has said that about 70% of the vulnerabilities it assigns a CVE each year are memory safety issues of this kind. ([MSRC](https://www.microsoft.com/en-us/msrc/blog/2019/07/a-proactive-approach-to-more-secure-code))

Python, Java and Go hand the job to a garbage collector. The runtime periodically finds memory nobody uses and clears it, so there is less room for mistakes. The price is that the program can stall briefly while it cleans. Discord had a Go service whose latency and CPU spiked roughly every two minutes because of the garbage collector, and the spikes went away when the same service was rewritten in Rust. ([Discord](https://discord.com/blog/why-discord-is-switching-from-go-to-rust))

Rust takes a third route. Every value has exactly one owner, and when the owner is done with it, the memory is freed right there. Anything else that wants to use the value has to borrow it, and there are rules about what you can do while borrowing. The compiler checks those rules before the program ever runs, and code that breaks them is simply not turned into an executable.

```rust
let a = String::from("hello");
let b = a;            // ownership of "hello" moves from a to b
println!("{}", a);    // compile error: a no longer owns anything
```

In Python you can keep using `a` after `b = a`. In Rust, ownership has moved to `b`, so the moment you touch `a` the compiler stops with a `borrow of moved value` error. Because the checking is done before the program runs, there is no collector cleaning up at run time, and nothing slows down because of it.

Rust is also easy to ship. A Rust program usually comes out as a single executable with what it needs bundled in, so it runs without installing a separate runtime such as Node.js or Python.

The catch is that it is hard on the people writing it. A Rust Blog post from March this year, based on about 70 interviews, says that borrow checking and ownership is "a hard topic that basically every beginner struggles with." ([Rust Blog](https://blog.rust-lang.org/2026/03/20/rust-challenges)) That is why rewriting hundreds of thousands of lines of working code in Rust was something teams might want to do but rarely dared to start.

## 2. AI started doing that work

The most detailed account comes from GitHub. It moved the agent runtime shared by Copilot CLI, the Copilot app and the Copilot SDK from TypeScript to Rust, and Stephen Toub, who led the work, wrote it up at length in September. ([GitHub Blog](https://github.blog/ai-and-ml/generative-ai/migrating-the-github-copilot-runtime-to-rust-using-copilot/))

The first estimate was around 130,000 lines, but roughly 430,000 lines of TypeScript ended up passing through the port, and the result is 832,378 lines of Rust plus another 460,000 or so lines of tests. It was moved in 128 pull requests over about 14.5 weeks, from 12 May to 21 August, while the product kept shipping about 1.3 releases a day. Agents wrote most of the code, and on the human side it was mainly one developer. The humans chose the target architecture, decided which behaviour had to be preserved, split up the work, reviewed the risky parts themselves and made the merge calls. The agents wrote the code, compared old and new behaviour exhaustively, and handled CI failures and review comments. The post estimates that before agents, the job would have taken a whole team a year or two.

The results come with numbers. Under Node.js, every app using the SDK had to start its own JavaScript runtime, which cost on the order of 100 MB of memory at minimum; now the runtime is a native library that loads straight into the app's process. A scenario that creates a client, opens a session, does one turn and tears everything down went from 5.25 seconds to 0.29 seconds when run in-process. Extra memory with ten clients running at once fell from 1,383 MB to 126 MB. These were measured against a local test server returning a fixed short reply, and the author is careful to say this is not a case for moving every TypeScript program to Rust.

Bun is the more extreme case. Bun is a JavaScript runtime originally written in a language called Zig, and Anthropic acquired it in December 2025. Its creator, Jarred Sumner, moved 535,496 lines of Zig to Rust in 11 days, with up to about 64 Claude agents running at once. ([Bun](https://bun.com/blog/bun-in-rust)) The first Rust release, v1.4.0, passed the existing test suite on every platform and fixed 128 bugs that reproduced in the last Zig version. In a test that runs 2,000 builds in a row, memory that used to climb to 6,745 MB now levels off at 609 MB. Claude Code has run on this Rust build of Bun since v2.1.181, released on 17 June, so if you use a recent Claude Code you are already using the rewritten Bun. That said, Zig's creator publicly called the result unreviewed, and later security review found behaviour differences introduced by the mechanical translation. ([The Register](https://www.theregister.com/devops/2026/07/14/zig-creator-calls-buns-claude-rust-rewrite-unreviewed-slop/5270743), [InfoQ](https://www.infoq.com/news/2026/09/bun-AI-rewrite-zig-rust-4-months/))

OpenAI's reasons for Codex CLI were more practical. The original TypeScript version needed Node.js 22 or later, and the maintainers felt that requirement put some users off. So in 2025 they began moving it to Rust, citing a zero-dependency install, performance without garbage collection, and OS-level sandboxing. ([DevClass](https://devclass.com/2025/06/02/node-js-frustrating-and-inefficient-openai-rewrites-ai-coding-tool-in-rust/)) Today the `openai/codex` repository is 97% Rust by GitHub's language statistics.

## 3. Python is not being pushed out

In AI, Python is still the language people write code in. What is changing is the part underneath that does the heavy computation.

![Python on top, Rust underneath](/rust-layers-en.svg)

_Many libraries you import in Python run Rust inside._

Hugging Face's `tokenizers` repository is 95% Rust, and the core tokenising logic in OpenAI's `tiktoken` is written in Rust too. In both cases you simply import them from Python. Pydantic, the data validation library, rewrote its validation logic in Rust as a separate package, `pydantic-core`, for v2 and announced it as 5 to 50 times faster than v1. ([Pydantic](https://pydantic.dev/articles/pydantic-v2-alpha)) Its earlier plan also credited the restructured validation objects, not only the change of language. ([Pydantic](https://pydantic.dev/articles/pydantic-v2))

The trend is reaching GPU code as well. In September NVIDIA announced CUDA Rust for writing GPU kernels in Rust, though both public projects, cuda-oxide and cutile-rs, are described as experimental. ([NVIDIA](https://developer.nvidia.com/cuda/rust), [MarkTechPost](https://www.marktechpost.com/2026/09/08/nvidia-announces-cuda-rust-with-cuda-oxide-simt-and-cutile-rs-tile-for-compile-time-safe-gpu-kernels/))

## 4. My view

The reasons to want Rust were always there: it is fast, uses less memory and catches mistakes before the program runs. What held teams back was the human effort of moving existing code. AI has cut that effort sharply, and I think that is why switches people kept putting off are now actually happening.

It is also interesting how well Rust's strict compiler suits agents. The fussy error messages that put people off are useful feedback for an agent that will tirelessly read an error, fix it and run again. I once wrote that [productivity in AI coding comes from decomposition and feedback loops](/en/ai-coding-workflow/), and in the GitHub case the human work was exactly that: splitting the job, deciding which behaviour had to hold, and verifying the results.

Translation is not the finish line, though. The GitHub post says this round was a straight port and that redesigning for Rust comes next, and Bun drew criticism over whether such a fast job was checked thoroughly enough. Both relied on safety nets such as test suites with over a million assertions or exhaustive comparisons against the old version. Try the same thing on a codebase with thin tests and you may end up copying the bugs into a new language.

As someone who works in data and ML, I am not sure everyone needs to learn Rust right now. Python is enough for most work, and we already use Rust libraries without noticing. Still, if I need to build a speed-sensitive internal tool, I no longer have to rule Rust out just because learning it from scratch used to be such a burden.

Whether Musk's one-word reply turns out to be right is still an open question. What can be checked is that many of the AI coding tools we use every day already run on Rust.

---

**Related posts:**

- [Productivity in AI Coding Comes from Decomposition and Feedback Loops, Not Better Prompts](/en/ai-coding-workflow/)
- [Better Agents Come From a Better Harness, Not a Better Prompt](/en/ai-harness-engineering/)

## References

- [Elon Musk's reply to Bojan Tunguz (X, 2023-04)](https://x.com/elonmusk/status/1649603943033450496)
- [Elon Musk on xAI code and X replacing Scala (X, 2026-02-19)](https://x.com/elonmusk/status/2024565280169677297)
- [A proactive approach to more secure code (Microsoft MSRC, 2019-07)](https://www.microsoft.com/en-us/msrc/blog/2019/07/a-proactive-approach-to-more-secure-code)
- [Why Discord is switching from Go to Rust (Discord, 2020-02-04)](https://discord.com/blog/why-discord-is-switching-from-go-to-rust)
- [What we heard about Rust's challenges (Rust Blog, 2026-03-20)](https://blog.rust-lang.org/2026/03/20/rust-challenges)
- [Migrating the GitHub Copilot runtime to Rust, using Copilot (GitHub Blog, 2026-09-16)](https://github.blog/ai-and-ml/generative-ai/migrating-the-github-copilot-runtime-to-rust-using-copilot/)
- [Rewriting Bun in Rust (Bun, 2026-07-08)](https://bun.com/blog/bun-in-rust)
- [Claude Code uses Bun written in Rust now (Simon Willison, 2026-07-19)](https://simonwillison.net/2026/Jul/19/claude-code-in-bun-in-rust/)
- [Zig creator calls Bun's Claude Rust rewrite 'unreviewed slop' (The Register, 2026-07-14)](https://www.theregister.com/devops/2026/07/14/zig-creator-calls-buns-claude-rust-rewrite-unreviewed-slop/5270743)
- [Bun Rewrites 535K Lines of Zig into Rust (InfoQ, 2026-09)](https://www.infoq.com/news/2026/09/bun-AI-rewrite-zig-rust-4-months/)
- [OpenAI rewrites AI coding tool in Rust (DevClass, 2025-06-02)](https://devclass.com/2025/06/02/node-js-frustrating-and-inefficient-openai-rewrites-ai-coding-tool-in-rust/)
- [openai/codex (GitHub)](https://github.com/openai/codex)
- [huggingface/tokenizers (GitHub)](https://github.com/huggingface/tokenizers), [openai/tiktoken (GitHub)](https://github.com/openai/tiktoken)
- [Pydantic V2 alpha (Pydantic, 2023)](https://pydantic.dev/articles/pydantic-v2-alpha), [Pydantic V2 Plan (Pydantic, 2022)](https://pydantic.dev/articles/pydantic-v2)
- [CUDA Rust (NVIDIA)](https://developer.nvidia.com/cuda/rust), [NVIDIA Announces CUDA Rust (MarkTechPost, 2026-09-08)](https://www.marktechpost.com/2026/09/08/nvidia-announces-cuda-rust-with-cuda-oxide-simt-and-cutile-rs-tile-for-compile-time-safe-gpu-kernels/)

_Written on 29 October 2026 from public sources. Performance figures were measured by each company in its own environment. GitHub's benchmarks used a local test server, and repository language shares are from GitHub's language statistics as of 29 October 2026. Musk's statements about xAI and X have not been confirmed beyond his own posts._
