---
title: "AI 코딩 도구들은 왜 지금 Rust로 옮겨 갈까: Copilot, Bun, Codex CLI의 경우"
description: "GitHub Copilot 런타임은 TypeScript 약 43만 줄을 14.5주 만에 Rust 83만 줄로 옮겼고, Claude Code 아래서 도는 Bun은 Zig 53만 줄을 11일 만에 Rust로 바꿨다. Rust가 무엇이 다른지 메모리 관리부터 쉽게 풀고, 배우기 어려운 이 언어로의 전환을 AI가 어떻게 앞당겼는지 정리했다."
pubDatetime: 2026-10-28T21:00:00Z
tags:
  - ai-coding
  - developer-tools
  - engineering
  - rust
---

2023년 4월, 데이터 과학자 Bojan Tunguz가 X에 "AGI는 Python으로 만들어질 것이다"라고 썼다. 일론 머스크는 여기에 "Rust" 한 단어로 답했다. ([X](https://x.com/elonmusk/status/1649603943033450496))

그때는 농담처럼 보였는데, 올해 2월 머스크는 xAI 코드가 대부분 Rust이고 X도 예전 트위터의 Scala 코드를 빠르게 Rust로 바꾸는 중이라고 썼다. ([X](https://x.com/elonmusk/status/2024565280169677297)) 회사 밖에서 확인할 수 있는 숫자는 아니라서 본인 주장 정도로 보면 된다.

확인할 수 있는 사례는 따로 있다. 올해 GitHub는 Copilot의 에이전트 런타임을 Rust로 옮겼고, Claude Code 아래서 도는 JavaScript 런타임 Bun도 Rust로 다시 쓰였다. OpenAI의 Codex CLI는 지난해부터 Rust로 옮겨 가서 지금은 코드의 97%가 Rust다. 배우기 어렵기로 유명한 언어에 AI 도구들이 한꺼번에 몰리는 이유를, Rust가 뭔지부터 풀어서 정리해 봤다.

## 1. Rust는 메모리를 다루는 방식이 다르다

프로그램은 실행되는 동안 데이터를 메모리에 올려 두고, 다 쓰면 그 자리를 반납한다. 이 반납을 누가 언제 하느냐가 언어마다 다르고, Rust가 다른 언어와 갈리는 지점도 바로 여기다.

![메모리를 치우는 세 가지 방법](/rust-memory.svg)

_메모리를 반납하는 방식에 따라 언어의 성격이 갈린다._

C와 C++는 개발자가 직접 반납한다. 빠르고 가볍지만, 이미 반납한 자리를 다시 건드리거나 두 번 반납하는 실수를 하면 프로그램이 죽거나 보안 구멍이 생긴다. 마이크로소프트는 해마다 CVE 번호를 붙이는 자사 취약점의 약 70%가 이런 메모리 안전성 문제라고 밝힌 적이 있다. ([MSRC](https://www.microsoft.com/en-us/msrc/blog/2019/07/a-proactive-approach-to-more-secure-code))

Python, Java, Go는 이 일을 가비지 컬렉터에게 맡긴다. 런타임이 주기적으로 안 쓰는 메모리를 찾아서 치우니까 개발자가 실수할 일이 줄어든다. 대신 치우는 동안 프로그램이 잠깐씩 멈칫할 수 있다. 디스코드는 Go로 짠 서비스에서 약 2분마다 지연시간과 CPU 사용량이 튀었는데, 원인이 가비지 컬렉터였고 같은 서비스를 Rust로 다시 짜자 그 현상이 사라졌다고 한다. ([Discord](https://discord.com/blog/why-discord-is-switching-from-go-to-rust))

Rust는 둘 다 아닌 세 번째 방법을 쓴다. 값마다 주인(owner)을 하나만 두고, 주인이 쓰임을 다하면 그 자리에서 메모리를 반납한다. 다른 곳에서 그 값을 쓰려면 주인에게서 빌려(borrow) 써야 하고, 빌려 쓰는 동안 지켜야 할 규칙이 있다. 이 규칙을 지켰는지는 컴파일러가 실행 전에 검사하는데, 어긴 코드는 아예 실행 파일로 만들어 주지 않는다.

```rust
let a = String::from("hello");
let b = a;            // "hello"의 주인이 a에서 b로 넘어간다
println!("{}", a);    // 컴파일 에러: a는 이제 주인이 아니다
```

Python이라면 `b = a` 뒤에도 `a`를 그대로 쓸 수 있다. Rust에서는 주인이 `b`로 넘어갔기 때문에 `a`를 쓰는 순간 컴파일러가 `borrow of moved value`라는 에러를 내고 멈춘다. 검사가 실행 전에 끝나니 실행 중에 메모리를 치우는 청소기가 필요 없고, 그 때문에 느려지지도 않는다.

배포가 쉽다는 것도 장점이다. Rust 프로그램은 보통 필요한 걸 다 묶은 실행 파일 하나로 나온다. Node.js나 Python 같은 런타임을 따로 깔지 않아도 그 파일만 있으면 돌아간다.

문제는 쓰는 사람이 힘들다는 점이다. Rust 공식 블로그가 올해 3월 개발자 약 70명을 인터뷰해 정리한 글에서도 빌림 검사와 소유권은 "거의 모든 초보자가 어려워하는 주제"라고 적혀 있다. ([Rust Blog](https://blog.rust-lang.org/2026/03/20/rust-challenges)) 그래서 이미 잘 돌아가는 수십만 줄짜리 코드를 Rust로 다시 짜는 건, 하고 싶어도 엄두가 안 나는 일이었다.

## 2. 그 일을 AI가 하기 시작했다

가장 자세히 공개된 사례는 GitHub다. Copilot CLI, Copilot 앱, Copilot SDK가 함께 쓰는 에이전트 런타임을 TypeScript에서 Rust로 옮겼는데, 작업을 이끈 스티븐 타웁이 9월에 과정을 길게 공개했다. ([GitHub Blog](https://github.blog/ai-and-ml/generative-ai/migrating-the-github-copilot-runtime-to-rust-using-copilot/))

처음에는 13만 줄 정도로 봤지만 실제로 작업을 거쳐 간 TypeScript는 약 43만 줄이었고, 결과물은 Rust 832,378줄(테스트 코드 46만여 줄 별도)이다. 5월 12일부터 8월 21일까지 약 14.5주 동안 풀 리퀘스트 128개로 나눠 옮겼고, 그 사이에도 서비스는 하루 평균 1.3번꼴로 릴리스됐다. 코드는 대부분 에이전트가 썼고, 사람 쪽은 주로 개발자 한 명이 진행했다. 사람이 한 일은 목표 구조를 정하고, 어떤 동작을 반드시 지켜야 하는지 판단하고, 일을 나누고, 위험한 부분을 직접 검토하고, 머지를 결정하는 쪽이었다. 에이전트는 코드를 쓰고, 기존 버전과 새 버전의 동작을 하나하나 비교하고, CI 실패와 리뷰 의견을 처리했다. 글에서는 에이전트가 없었다면 개발자 팀 전체가 1~2년은 걸렸을 일이라고 봤다.

결과도 숫자로 나와 있다. Node.js로 돌던 시절에는 SDK를 쓰는 앱마다 별도의 JavaScript 런타임을 띄워야 해서 최소 100MB 안팎의 메모리가 들었는데, 이제는 앱 프로세스 안에 바로 붙는 네이티브 라이브러리가 됐다. 클라이언트를 만들고 세션을 열어 한 턴 주고받은 뒤 정리하는 시나리오가 5.25초에서 0.29초(프로세스 안에서 돌 때 기준)로 줄었다. 클라이언트 10개를 동시에 돌릴 때 늘어나는 메모리도 1,383MB에서 126MB가 됐다. 로컬 테스트 서버에 고정된 짧은 응답을 받는 조건에서 잰 값이고, 글쓴이도 모든 TypeScript 프로그램을 Rust로 옮겨야 한다는 뜻은 아니라고 선을 그었다.

Bun은 더 극단적이다. Bun은 원래 Zig라는 언어로 짠 JavaScript 런타임이고, 2025년 12월 Anthropic이 인수했다. 제작자 재러드 섬너는 Zig 코드 535,496줄을 11일 동안 Rust로 옮겼는데, 많을 때는 Claude 에이전트 약 64개를 동시에 돌렸다고 밝혔다. ([Bun](https://bun.com/blog/bun-in-rust)) 첫 Rust 버전인 v1.4.0은 모든 플랫폼에서 기존 테스트를 통과했고, 직전 Zig 버전에서 재현되던 버그 128개가 고쳐졌다. 빌드를 2,000번 반복하는 테스트에서는 메모리가 6,745MB까지 늘던 것이 609MB에서 멈췄다. Claude Code는 6월 17일에 나온 v2.1.181부터 이 Rust 버전 Bun 위에서 돈다. 최신 Claude Code를 쓰고 있다면 이미 Rust로 다시 쓰인 Bun을 쓰고 있는 셈이다. 다만 Zig 창시자가 검토되지 않은 결과물이라고 공개적으로 비판했고, 이후 보안 검토 과정에서 자동 번역 때문에 생긴 동작 차이가 발견되기도 했다. ([The Register](https://www.theregister.com/devops/2026/07/14/zig-creator-calls-buns-claude-rust-rewrite-unreviewed-slop/5270743), [InfoQ](https://www.infoq.com/news/2026/09/bun-AI-rewrite-zig-rust-4-months/))

OpenAI의 Codex CLI는 동기가 조금 더 실용적이었다. 처음 나온 TypeScript 버전은 Node.js 22 이상을 깔아야 쓸 수 있었는데, 관리자들은 이 조건이 일부 사용자에게 진입 장벽이 된다고 봤다. 그래서 2025년부터 Rust로 옮기기 시작했고, 의존성 없이 바로 깔리는 실행 파일, 가비지 컬렉션이 없는 성능, 운영체제 수준의 샌드박스를 이유로 들었다. ([DevClass](https://devclass.com/2025/06/02/node-js-frustrating-and-inefficient-openai-rewrites-ai-coding-tool-in-rust/)) 지금 `openai/codex` 저장소는 GitHub 언어 통계 기준 97%가 Rust다.

## 3. 그렇다고 Python이 밀려나는 건 아니다

AI 쪽에서 Python은 여전히 사람이 코드를 쓰는 언어다. 바뀌고 있는 건 그 밑에서 무거운 계산을 맡는 부분이다.

![쓰는 쪽은 Python, 밑에서 도는 건 Rust](/rust-layers.svg)

_Python에서 import해서 쓰는 라이브러리 상당수가 속은 Rust로 돌고 있다._

Hugging Face의 `tokenizers`는 저장소 코드의 95%가 Rust이고, OpenAI의 `tiktoken`도 토큰을 나누는 핵심 부분이 Rust로 짜여 있다. 둘 다 Python에서는 그냥 import해서 쓴다. 데이터 검증 라이브러리 Pydantic은 v2에서 검증 로직을 `pydantic-core`라는 Rust 패키지로 다시 짜면서 v1보다 5~50배 빨라졌다고 발표했다. ([Pydantic](https://pydantic.dev/articles/pydantic-v2-alpha)) 앞서 개발 계획을 밝힌 글에서는 언어를 바꾼 것뿐 아니라 검증 객체의 구조를 손본 효과도 함께 들었다. ([Pydantic](https://pydantic.dev/articles/pydantic-v2))

이 흐름은 GPU 코드까지 내려가고 있다. NVIDIA는 9월에 GPU 커널을 Rust로 짜는 CUDA Rust를 발표했는데, 공개된 두 프로젝트(cuda-oxide, cutile-rs) 모두 아직 실험 단계라고 밝히고 있다. ([NVIDIA](https://developer.nvidia.com/cuda/rust), [MarkTechPost](https://www.marktechpost.com/2026/09/08/nvidia-announces-cuda-rust-with-cuda-oxide-simt-and-cutile-rs-tile-for-compile-time-safe-gpu-kernels/))

## 4. 개인적인 견해

Rust를 쓰고 싶은 이유는 원래부터 있었다. 빠르고, 메모리를 덜 쓰고, 실수를 실행 전에 잡아 준다. 막혀 있던 건 옮기는 데 드는 사람의 수고였는데, AI가 그 수고를 크게 덜어 주면서 미뤄 두던 전환이 실제로 시작됐다고 본다.

Rust의 엄격한 컴파일러가 에이전트와 잘 맞는다는 점도 흥미롭다. 사람에게는 진입 장벽인 깐깐한 에러 메시지가, 에러를 보고 고치고 다시 돌리는 일을 지치지 않고 반복하는 에이전트에게는 오히려 좋은 피드백이 된다. [AI 코딩의 생산성이 작업 분해와 피드백 루프에서 나온다](/posts/ai-coding-workflow/)는 이야기를 예전에 쓴 적이 있는데, GitHub 사례에서 사람이 맡은 일도 결국 일을 나누고, 지켜야 할 동작을 정하고, 결과를 검증하는 쪽이었다.

다만 번역이 끝은 아니다. GitHub 글도 이번 작업은 일단 그대로 옮긴 것이고 Rust에 맞게 다시 설계하는 일은 이제부터라고 했고, Bun은 빠른 속도만큼 검증이 충분했느냐는 비판을 받았다. 두 사례 모두 백만 개가 넘는 테스트 검증문이나 기존 버전과의 꼼꼼한 동작 비교 같은 안전망이 있었기 때문에 가능했다. 테스트가 빈약한 코드베이스에서 같은 걸 따라 하면 버그를 다른 언어로 옮겨 적는 데서 끝날 가능성이 크다.

데이터나 ML 일을 하는 입장에서 당장 Rust를 배워야 하는지는 잘 모르겠다. 대부분은 Python으로 충분하고, 이미 Rust로 만든 라이브러리를 모르는 사이에 쓰고 있다. 그래도 속도가 중요한 내부 도구를 새로 만들 일이 생긴다면, 예전처럼 Rust를 처음부터 배워야 한다는 부담 때문에 선택지에서 빼 버리지는 않아도 될 것 같다.

머스크의 한 단어 답글이 맞았는지는 아직 모르겠다. 다만 지금 쓰고 있는 AI 코딩 도구 상당수가 이미 Rust 위에서 돌고 있다는 건 확인할 수 있다.

---

**함께 보면 좋은 글:**

- [AI 코딩의 생산성은 프롬프트가 아니라 작업 분해와 피드백 루프에서 나온다](/posts/ai-coding-workflow/)
- [AI Agent는 더 좋은 프롬프트가 아니라 더 좋은 Harness에서 나온다](/posts/ai-harness-engineering/)

## 참고 자료

- [Bojan Tunguz의 트윗에 단 일론 머스크의 답글 (X, 2023-04)](https://x.com/elonmusk/status/1649603943033450496)
- [일론 머스크: xAI 코드와 X의 Scala 교체 (X, 2026-02-19)](https://x.com/elonmusk/status/2024565280169677297)
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

_본 글은 2026년 10월 29일 기준 공개 자료를 바탕으로 작성했다. 성능 수치는 각 회사가 자사 환경에서 잰 값이다. GitHub 벤치마크는 로컬 테스트 서버 기준이고, 저장소 언어 비율은 GitHub 언어 통계(2026년 10월 29일 조회) 기준이다. 머스크의 xAI·X 관련 발언은 본인 게시물 외에 확인된 자료가 없다._
