---
title: "World Models (1) What Comes After the LLM: AI That Predicts the Next Frame"
description: "If predicting the next token conquered language, can predicting the next frame conquer the physical world? What world models are, why they are called the key to unlocking the robotics data bottleneck, and what they still cannot do. Part one of three."
pubDatetime: 2026-07-21T22:00:00Z
koSlug: world-model-101
tags:
  - world-model
  - machine-learning
  - engineering
---

I work as a data scientist, and a substantial part of my modelling work is already shared with an LLM. Coming up with feature ideas, writing baseline code, interpreting experiment results. Which makes me imagine fairly often how this job changes from here, and naturally makes me watch what is happening outside LLMs. What catches my eye most lately is **world models**.

Robotics is the trigger. Humanoids, self-driving cars — everything trying to move into the physical world talks about world models. I spent a while digging into why this in particular, and whether it could be the wave after LLMs. This series is that reading, in three parts: what a world model is and why it is getting attention now; what design a company actually shipping one chose; and the remaining hard problems and what they mean for robotics and data work.

## 1. A simulator in the head

Intuition before definition. Everyone carries a model of the world in their head. Throw a ball and it will arc and fall; push a cup off the edge of a table and it will hit the floor. You know without doing it, because a compressed version of how the world runs sits in your head, learned from experience. A world model is the attempt to give a machine that internal simulator — the thing that runs the outcome before you act. In one line: **a model that predicts what happens next given the current state and an action.**

The form drawing attention now is the **video world model**, predicting the world's next state as a screen — the next frame. The structure resembles an LLM to a striking degree. As an LLM looks at the tokens so far and predicts the next token, a video world model looks at the frames so far and generates the next frame. Even down to taking **conditioning signals** — a text prompt, a starting image — to steer generation.

![How a video world model takes input and gives output](/wm-io-en.svg)

_Conditioning signals go in, frames come out one at a time, and the frame just made becomes input to the next prediction._

The most interesting conditioning signal is **action**. Press the key to move forward and the next frame has advanced; turn the camera and the next frame shows that direction. This is where a world model diverges from a video generator. It stops being footage you can only watch and becomes a world you can move inside. Read it as a robot and it is directly the robot's problem: the ability to draw in advance how the world changes if the arm reaches out this way.

I read this as an experiment in transplanting the next-token-prediction formula. The LLM story was that pushing a simple objective — guess the next token — hard enough made language ability emerge. Transplant that formula from text to pixels, from a world of language to a physical world, and what emerges? That is the question on the table.

## 2. The robot's bottleneck is data, not the model

Why robotics became the catalyst is quickest to see from a data perspective. LLMs could grow because decades of text had accumulated on the internet. What a robot needs is not text but **a record of action and consequence** — I did this in this situation and this happened — and that is not on the internet. There is plenty of video on YouTube, and none of it records what command the actor issued. Collecting it directly means running robots through millions of real-world trials: slow, expensive and dangerous.

World models were summoned as a way around that bottleneck. If a model can produce a plausible virtual world, a robot can fall over and crash inside it endlessly and learn. Where LLMs grew by consuming data that already existed, a world model stands in the position of **a factory producing training data.** The model becomes data infrastructure — and for anyone whose job is data, that inversion is the most interesting thing about this field.

The moves of the past year or two all point the same way. Google DeepMind released Genie 3, generating worlds you can walk around in real time from a text description ([DeepMind](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/)). NVIDIA released Cosmos, a world foundation model platform for robotics and autonomous driving training ([NVIDIA](https://www.nvidia.com/en-us/ai/cosmos/)). Fei-Fei Li, who built ImageNet, founded the spatial intelligence company World Labs ([World Labs](https://www.worldlabs.ai/)). And Yann LeCun, who has long argued that LLMs alone cannot reach AI that understands the world, was reported to be leaving Meta to build a world model startup. Different companies, different approaches, same destination: after text comes the physical world.

## 3. But drawing is not knowing

That is the bright version. The more I looked, the more two fundamental holes appeared in today's video world models. Those holes are where the other two parts of this series start.

First, **it does not remember the world.** A video world model does not store a scene; it regenerates it each time. So in a scene with a bottle on a table, turn the camera away and back and nothing guarantees the bottle is still there. The model quietly changes it while regenerating. Inside the frame it is plausible; the moment something leaves the frame, its existence wobbles.

![Turn the camera away and back, and the world has changed](/wm-no-memory-en.svg)

_It does not remember a scene — it regenerates it each time, so whatever leaves the frame can quietly change._

Second, **pixels are not understanding.** The model can draw a flawless bottle while not knowing it is a bottle — that the cap opens, that it holds water, that it falls if you let go. It is closer to rendering the world's appearance than to modelling the world. Which is a familiar argument. The "stochastic parrot or genuine understanding" debate around LLMs is repeating itself in pixels with the modality swapped.

These two holes are not visible in a demo. A few minutes of footage tests neither memory nor understanding. They come to the front the moment you try to put this in a service where users stay for hours. And that is exactly where I got curious about what design a company facing this head-on chose.

## 4. A personal view

Part two covers it in detail, but the most interesting answer I found was not "grow the model until the holes fill in." It was "let another system fill the holes, and let the model do only what it is good at." A development already seen in LLMs. A model alone is not a product; it became usable once a harness handling tool calls, state management and verification wrapped around it. The shape I laid out in [an earlier post on harness engineering](/en/ai-harness-engineering/) reappears with the modality swapped to pixels. Less coincidence than a structural pattern that repeats whenever a generative model is turned into a product.

One more. On the question of whether prediction produces understanding, the LLM camp answered much of it with scale. Whether world models take the same route, or whether the world of pixels has a wall scale alone cannot pass, I am still holding judgement on. Either way, I have become fairly convinced that the data economy of robot learning gets inverted while the answer arrives. For someone whose job is collecting data, a model that produces data is not something to walk past.

---

**Related posts:**

- [World Models (2) Why Not Hand the Whole World to the Model](/en/roblox-reality-hybrid/)
- [World Models (3) Why a Game Is the Harshest Test Bed](/en/world-model-hard-problems/)
- [AI Agents Come from a Better Harness, Not a Better Prompt](/en/ai-harness-engineering/)

## References

- [Inside Roblox's Bet on World Models — ByteByteGo](https://blog.bytebytego.com/p/inside-robloxs-bet-on-world-models)
- [Genie 3: A new frontier for world models — Google DeepMind](https://deepmind.google/discover/blog/genie-3-a-new-frontier-for-world-models/)
- [NVIDIA Cosmos](https://www.nvidia.com/en-us/ai/cosmos/)
- [World Labs](https://www.worldlabs.ai/)

_Written as of 21 July 2026 from public material. The diagrams are my own reconstructions informed by figures in the references. Some items, such as LeCun's startup, are based on reporting and may differ from official announcements._
