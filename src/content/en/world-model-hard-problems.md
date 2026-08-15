---
title: "World Models (3) Why a Game Is the Harshest Test Bed"
description: "Real-time response, long-run consistency, many users, controllability. The four gates a world model has to pass to go from spectacle to something useful. A game demands all four at once at extreme settings, which is why it became the frontier — and those gates translate almost directly into the robot's problems. Part three of three."
pubDatetime: 2026-07-21T22:20:00Z
koSlug: world-model-hard-problems
tags:
  - world-model
  - engineering
  - machine-learning
---

[Part one](/en/world-model-101/) covered the promise and the holes; [part two](/en/roblox-reality-hybrid/) covered the hybrid design splitting work between engine and model. The remaining question is the most practical one. When and how does this actually run?

One view that settled while reading. World model demos are plentiful. Between a demo and a product, though, sit four gates — **real-time response, long-run consistency, many users, controllability** — and the stage demanding all four at once, at the harshest settings, is a game. It has to respond in tens of milliseconds, sessions run for hours, tens of thousands share one world, and it has to obey the rules a creator set. A lab demo tests none of these properly. A game company becoming the frontier of world models is not coincidence; it is where the test conditions are hardest. This part follows how Roblox tries to pass each gate and draws out the general character of each.

![Four hard problems between design and production](/wm-four-problems-en.svg)

_The four gates and the approach to each. A game demands all four at once._

## 1. Real-time: seconds down to 30 milliseconds

A game has to respond the moment a player acts. Click and get the result seconds later and it is not a game. But most video models generate an entire clip in one offline pass, computing back and forth along the time axis, which takes seconds. What is needed is one frame every few tens of milliseconds — roughly two orders of magnitude to cut.

The key Roblox took is **self-forcing**: converting a model that computed a whole clip into an autoregressive model producing the next single frame conditioned on the frames just generated. The output becomes a continuous stream, so the screen can flow without waiting. The same structural shift as an LLM emitting tokens one at a time instead of showing the answer once finished — and Roblox acquired Morpheus AI, the company of the founder behind the technique.

![Offline generation vs self-forcing](/self-forcing-en.svg)

_Seconds for a whole clip versus per-frame streaming. Video generation goes autoregressive._

Self-forcing alone does not finish the job, so every lever gets pulled. Make the model smaller, compress the KV cache — the working memory during inference, described as a necessary condition for cost not to explode at high resolution — and run generation itself on H200- and B200-class GPUs in edge data centres right beside the game engine instance, near the player, cutting the network round trip too. Treating model optimisation and infrastructure placement inside a single latency budget was the impressive part, given how many organisations discuss inference cost separately in the model team and the infra team.

## 2. Long-run consistency: a world slowly losing itself

The data model from part two suppresses drift between frames. Time is the harder problem. As a session lengthens, small errors accumulate and the world slowly loses itself. It has to hold for minutes and hours, not frames.

What is needed is the model holding far more of its own history — long context. A scene generated ten minutes ago has to condition the scene being generated now. The long-context race that played out in LLMs repeats in video, and at higher difficulty, because frames are far heavier than tokens. Roblox chose to acquire the capability rather than build it: the same Morpheus AI brought long-context world model research along with self-forcing, and the work now is extending the context window.

## 3. Many users: drawing a crowd versus running one

Multiplayer is where a video model's limits show most sharply. The model can draw a crowd of 500. But that is pixels, not 500 people each with a position, an inventory and behaviour. Managing a world where 20,000 people react in real time means tracking 20,000 individual states — a different kind of problem from generating a plausible crowd. Even at small scale the requirement is subtle. If I move an object, it has to move on the screen of every other player who can see it. An action is not only what I did but the effect it leaves in everyone else's world.

The skeleton of the solution is role separation. The engine, as server authority, computes the one shared truth state, and each player's video model generates only its own view conditioned on that shared state. Screens differ in viewpoint and agree on fact. For responsiveness, immediate actions are first handled by a fast predictive simulation on the player's device, with the server confirming the authoritative result shortly after. Rendering only the player's own avatar locally and laying it over the streamed frame is also under consideration — making the motion people feel most acutely respond instantly. Doing this at a scale of tens of thousands is described as an active research area rather than a solved feature.

So the answer at this gate was not "make the model serve many people" but "keep truth in one place and let the model be each person's eyes." Probabilistic generation and shared truth collide at the level of principle, so truth was pulled out of the model entirely.

## 4. Controllability: fun comes from rules

The last gate is less technical than creative. What makes a game fun is usually the rules and logic a creator put in, not how finely it renders. A plain-looking game takes off if the gameplay underneath is good. So even when a world is generated by a model it has to run by the creator's rules — and there is no obvious way to tell a model that extracts worlds from learned weights to "change only this rule."

The piece built by the Lucid AI team that joined Roblox is a structure they call the **game cartridge harness**. It wraps the video world model in a real game engine's deterministic logic so the world looks generated while behaviour follows fixed rules. Player input reaches the model through that harness too: WASD movement is injected as a conditioning signal, so pressing forward does not merely move a character inside the engine — the generated frame itself steers accordingly. Control beyond movement — whether to direct through text prompts or through the data model — is described as an open question. Seeing even the word "harness" turn up identically hardened the thought from part two that companies turning generative models into products arrive at the same-shaped answer.

## 5. Translating into robot problems

Returning to the robotics perspective that started this series, the four gates translate almost one to one.

- **Real-time response** — robot control loops also run in tens of milliseconds. A model that takes seconds to draw the consequence of an action is unusable for control. Making video generation autoregressive is a shift robotics needs just as much.
- **Long-run consistency** — a robot's internal world model diverging from reality over time is dangerous. Same problem as maintaining your own history through long context.
- **Many users** — several robots collaborating need shared world state. "Keep truth in one place and let each generate only its own view" is exactly the requirement for fleet design.
- **Controllability** — a robot must move only under deterministic constraints of safety rules and task specification. The same reason a cartridge structure wrapping a generative model in a deterministic harness becomes necessary.

So I expect the solutions being validated in games to be reinvented in the robotics stack within a few years, or imported outright. A game is a stage where all four gates can be tested without physical-world danger, which makes it both the best training ground and the best test bed a world model has.

One operational aside I enjoyed. Because a single game can jump from 3 million to 22 million players in weeks, capacity is unpredictable — so Roblox deliberately removes capacity from production every week to find the limit first. It is an automated test any engineer can start, and executives take the same on-call rotation as engineers. I read that as evidence that shipping a world model as a live service takes as much operational muscle as model research. The announced schedule is an early version as soon as the end of this year or early next, with a first quality target of 2K at 60fps.

## 6. A personal view

Part one started from the question of how this job changes, and after writing the series the thought is a bit more concrete.

One structure repeated across all three parts: separating the fuzzy part the model is good at from the exact part a system must take, and designing the boundary between them. Keeping state on the server while regenerating pixels was that. Keeping truth in one place while generating views separately was that. Wrapping the model in a deterministic harness was that. Models themselves get better fast and get common fast. But deciding how much to leave to the model and where a system takes responsibility remains a judgement for someone who knows the domain and the cost of failure.

Which may be where a data scientist's work moves too. Time spent building models directly will shrink, while deciding what to preserve as state and what to leave to generation, which errors are tolerable and which the system must prevent, grows. I started studying world models expecting to learn a new model architecture; what I mostly learned was boundary design. That is where I intend to point my reading for a while.

---

**Related posts:**

- [World Models (1) What Comes After the LLM](/en/world-model-101/)
- [World Models (2) Why Not Hand the Whole World to the Model](/en/roblox-reality-hybrid/)
- [AI Agents Come from a Better Harness, Not a Better Prompt](/en/ai-harness-engineering/)

## References

- [Inside Roblox's Bet on World Models — ByteByteGo](https://blog.bytebytego.com/p/inside-robloxs-bet-on-world-models)
- [Introducing the Roblox Hybrid Architecture — Roblox Newsroom](https://about.roblox.com/newsroom/2026/04/roblox-reality-hybrid-architecture-democratizing-photorealistic-multiplayer-gaming)

_Written as of 21 July 2026 from public material; the Roblox content is based on the interviews and announcements in the references above. The diagrams are my own reconstructions informed by figures in that material. Schedule and specifications are as announced and may change._
