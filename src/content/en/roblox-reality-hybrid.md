---
title: "World Models (2) Why Not Hand the Whole World to the Model"
description: "One enormous model that learns everything, or a model that does only what it is good at while a system takes the rest? Dissecting the hybrid architecture Roblox chose at that fork — the game engine holding truth while a world model paints realism, and the design principle of separating state from appearance underneath it."
pubDatetime: 2026-07-21T22:10:00Z
koSlug: roblox-reality-hybrid
tags:
  - world-model
  - engineering
  - machine-learning
---

[Part one](/en/world-model-101/) covered what makes video world models attractive and their two holes — no memory of the world, and pixels are not understanding. This part looks at what answer a company hitting those holes at service scale produced. Roblox.

There is a reason for picking Roblox. It is a platform that has hit 45 million concurrent users, and most of its games are built not by the company but by creators. The company provides only tools and infrastructure. So "technology only a well-equipped large studio can use" is not an option here, and that constraint is baked straight into the architecture. Designs produced under extreme conditions tend to have more to teach.

## 1. A game has to do two jobs at once

People praise games by talking about graphics, but graphics are the most visible part and, in engineering terms, the smaller one. Making a game a game splits into two jobs.

One is **keeping the world consistent for everyone**. Persistent state remembering what is where and what happened, rules applied identically to everyone, physics that moves and collides as expected, real-time sync letting thousands share one world, and immediacy — the world reacting the moment you act. In a racing game the track, the score, the penalties, each car's handling and every other car's position all have to be exact, and every player has to see the same thing at the same moment. Get one wrong and players notice immediately.

The other is **making it look real**. Grass moving in the wind, dust behind a car, light shifting across a surface. The level of realism players now take for granted.

![The two jobs that make a game a game](/game-two-jobs-en.svg)

_Game engines are strong at consistency, world models at realism. They are strong at exactly opposite ends._

As part one showed, world models are strong at the second and helpless at the first. What is interesting is that game engines are exactly the reverse. Engines are mature technology for tracking state, enforcing rules and computing physics, and they collapse in front of photorealism. Looking real requires explicitly rendering high-resolution textures, complex lighting and light scattering, and cost climbs steeply as realism rises. So engines bake lighting in advance, swap distant objects for simplified versions, or flee into a stylised look where the missing detail is not visible. Which is why most games still look like games rather than like reality.

Worse, the cost falls on people rather than servers. Producing detail takes creator skill and time; running it takes a good device. A large studio can absorb that; a two-person team and an ordinary phone cannot. For a platform whose creator ecosystem is the company, that is a fatal constraint.

When two technologies are strong at exactly opposite ends, the next question narrows to one thing. How do you join them?

## 2. The temptation of one giant model, and the choice of division of labour

Here is the fork. One road says keep growing the model and eventually it will learn state, rules and physics too — the one-giant-model road. It fits the AGI story, and lab demos come out this way. The other road holds that reasoning about the world does not have to live inside a neural network. Exact state, rules and physics are what game engines have been refining for decades, so leave them there and let the model spend its whole capacity on the pixels it is best at.

Roblox bet on the second and calls the system Roblox Reality. Three parts.

![The three pieces of Roblox Reality](/roblox-reality-en.svg)

_The engine and the cloud hold consistency; the world model handles realism._

**The game engine** is the part that knows what actually exists. At its centre is a structured ledger called the **data model**, recording every object and property in the world — where the car is, how fast, which heading, what it is made of — and computing physics and rules identically on top of that every time. Because the computation is exact and repeatable, the engine can serve as the source of truth every player's screen must agree with.

**The cloud** is the base that runs that engine at scale. It persists each world's state so the game is intact when you come back days later, and it runs millions of live sessions in data centres near the player. Fast, fair multiplayer requires the authoritative state to sit beside the player rather than on the other side of the planet.

**The Super Upsampler** is the video world model, and the name is the role. It does not imagine a world from nothing. The engine first renders a draft frame — accurate in shape, position and camera motion, simple in texture and lighting; flat, in other words. The model takes that draft and upsamples it to photoreal. Being a large video model post-trained for this task, it already knows what the visual world looks like and only needs to fill in details: raindrops on a windscreen, leaves shaking as a car passes. **The engine decides what is in the scene; the model decides only how it looks.** The exact, cheap part goes to the engine and only the expensive, fuzzy part to the model, which costs less than either extreme.

## 3. The three reins holding the model

The division only works if players cannot feel the seam, so the real engineering is in joining the two parts. The model must not invent the world, so before generating pixels for each frame it is conditioned on materials the engine produced. For one frame of a driving game the engine produces a low-quality rendered frame, a depth map, the scene's lighting and weather, and structured information about every object — and those signals are injected along three different paths according to their character.

![The three kinds of conditioning signal](/upsampler-signals-en.svg)

_The injection path follows the geometry of the signal. Per-pixel signals attach to the grid, scene-wide signals are broadcast, text-like signals get consulted where needed._

- **Dense signals**: the roughly rendered frame and the depth map, with a value at every pixel. They share the output's grid, so they are concatenated onto the model input or injected through a ControlNet-style side network. Every generated pixel is pinned to its position and colour. (Think of ControlNet as a helper network imposing "keep this outline, this composition" on an image generation model.)
- **Global signals**: one setting for the whole scene — midday, light rain, sun low on the left. They enter as modulation, scaling and shifting the model's activations all at once. The same mechanism by which a diffusion model injects a timestep.
- **Structured signals**: compressed, text-like descriptions such as "metallic sports car, position (120, 0, 48), 40 metres per second," plus a style prompt. These enter through cross-attention so any part of the frame can consult them when needed.

From those materials the model draws the final 2K frame — gloss on wet paint, glare on the windscreen, spray off the tyres. It never moves the car or changes an object's distance. The drift problem from part one gets suppressed the same way. Because the data model says which objects exist and are fixed, a four-door car is still a four-door car in the next frame. The full game state cannot be fed in every frame, so a retrieval step selects only the objects relevant to the current render.

## 4. What to store and what to regenerate

The part of this architecture I chewed on longest is not the flashy model but the storage design. World state everyone has to agree on lives in the server's data model: shared, stable across a long session, persisted. The world's appearance lives in the model's video latent: continuously regenerated, never stored, and free to differ slightly between players. **The server decides truth; the model fills in only what is safe to differ.**

This is an old principle of software design — keep one source of truth, and make derivatives regenerable — reappearing in the generative AI era. And the sense for separating what to preserve as state from what to regenerate uses exactly the same muscle as deciding [what to keep in context and what to drop](/en/context-compaction/) when designing an LLM agent. Include the retrieval step selecting relevant objects and the whole picture will be familiar to anyone who has built RAG.

## 5. A personal view

The choice that reasoning need not all live inside the model reads as the largest-scale instance of the harness pattern mentioned at the end of part one. As an LLM agent gives the parts that must be deterministic — tool execution, state management, verification — to code and the fuzzy parts — planning, generation — to the model, here the game engine takes determinism and the world model takes pixels. Text or pixels, companies turning generative models into products keep arriving at the same-shaped answer. That is the biggest thing this case says.

A counter-argument is available, of course. The giant-model camp would say the division is a transitional crutch and a large enough model will swallow the engine too. There are LLM precedents where things solved by harness got absorbed into the model across generations, so it is not to be dismissed. But requirements like multiplayer shared state — everyone must agree on one truth — collide with probabilistic generation at the level of principle, so I expect that boundary to persist a long while. Where the boundary actually gets tested — real-time response, long-run consistency, multiplayer, control — is part three.

---

**Related posts:**

- [World Models (1) What Comes After the LLM](/en/world-model-101/)
- [World Models (3) Why a Game Is the Harshest Test Bed](/en/world-model-hard-problems/)
- [Context Compaction: Don't Give the Agent Everything, Keep Only What It Needs](/en/context-compaction/)

## References

- [Inside Roblox's Bet on World Models — ByteByteGo](https://blog.bytebytego.com/p/inside-robloxs-bet-on-world-models)
- [Introducing the Roblox Hybrid Architecture — Roblox Newsroom](https://about.roblox.com/newsroom/2026/04/roblox-reality-hybrid-architecture-democratizing-photorealistic-multiplayer-gaming)

_Written as of 21 July 2026 from public material; the Roblox content is based on the interviews and announcements in the references above. The diagrams are my own reconstructions informed by figures in that material. Implementation details are as announced and the shipped form may differ._
