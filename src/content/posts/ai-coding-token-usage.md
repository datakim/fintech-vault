---
title: "AI 코딩 도구 사용량은 어디에 기록될까: ccusage가 보여주는 네 가지 토큰"
description: "Claude Code, Codex 같은 코딩 에이전트는 작업할 때마다 로컬에 사용 기록을 남긴다. ccusage는 그 로그를 읽어 Input·Output·Reasoning·Cache Read 네 가지를 보여준다. 각 항목이 뭘 의미하는지, 캐시 읽기는 왜 input과 따로 잡히는지, 그게 내 컴퓨터인지 서버인지를 SQL 예시로 풀어본다."
pubDatetime: 2026-06-06T03:00:00Z
tags:
  - ai-coding
  - claude-code
  - codex
  - tokens
  - ccusage
  - developer-tools
---

> **핵심 요약:** Claude Code나 Codex로 코딩 작업을 하다 보면 "내가 도대체 얼마나 쓴 거지?" 싶은 순간이 온다. 이들은 작업할 때마다 로컬에 사용 기록을 남기고, [ccusage](https://github.com/ryoppippi/ccusage) 같은 도구가 그 로그를 읽어 Input·Output·Reasoning·Cache Read 네 가지로 보여준다. Cache Read는 넓게 보면 input의 일부지만 서버 쪽 prompt cache에서 재사용한 토큰이라 따로 잡힌다. 모델 자체는 클라우드 서버에서 돌고, 내 컴퓨터는 파일을 읽고 명령을 실행하는 쪽을 담당한다. ChatGPT 웹의 "메모리"와는 이름만 비슷할 뿐 역할이 다르다.

## 1. "내가 얼마나 쓴 거지?"

Claude Code, Codex 같은 AI 코딩 도구를 쓰다 보면 문득 이런 생각이 든다. "내가 도대체 얼마나 쓴 거지?"

겉으로 보면 그냥 채팅창에 질문하고 답을 받은 것처럼 보인다. 하지만 내부적으로는 꽤 많은 정보가 오간다. 내가 보낸 요청, AI가 읽은 파일 내용, 답변을 만들 때 사용한 토큰 수, 모델 이름, 실행 시간 같은 정보가 로컬 컴퓨터에 로그로 남는다.

이 로그를 읽어서 사용량을 보여주는 도구 중 하나가 [ccusage](https://github.com/ryoppippi/ccusage)다. 새로 뭔가를 감시하는 도구가 아니라, 이미 내 컴퓨터에 남아 있는 사용 기록을 정리해서 보기 좋게 보여주는 도구에 가깝다. 날짜별·월별·세션별로 토큰 사용량과 추정 비용을 한 화면에 정리해준다.

예를 들어 Codex 사용량을 ccusage로 보면 이런 식으로 나온다.

```
Codex total
  Input:        1,961,781
  Output:          50,986
  Reasoning:        9,965
  Cache Read:  14,458,496
  Total:       16,471,263 tokens
```

숫자는 많아 보이지만 단어 자체는 네 개다. **Input, Output, Reasoning, Cache Read.** 각각이 뭘 의미하는지 짧은 SQL 질문 하나를 깔고 풀어본다.

참고로 단위는 token이다. 토큰은 AI가 글을 읽고 쓰는 최소 단위에 가깝고, 한 글자나 한 단어와 정확히 일치하지는 않는다. 영어는 단어 조각 단위로 쪼개지는 경우가 많고, 한국어도 한 단어가 여러 토큰으로 갈리는 경우가 흔하다. 쉽게 말해 "AI가 계산하려고 문장을 잘게 쪼갠 조각"이라고 보면 된다.

## 2. 한 줄짜리 질문은 사실 한 줄이 아니다

이런 질문을 AI 코딩 도구에 던졌다고 하자.

```
orders 테이블에서 최근 7일 동안 고객별 주문 금액 합계를 구하는 SQL 쿼리를 작성해줘.
```

사람 입장에서는 한 문장이다. 그런데 Codex나 Claude Code 같은 에이전트는 이걸 그대로 모델에 보내지 않는다. 보통은 다음 같은 것들을 함께 묶어 보낸다.

```
시스템 지시사항: 너는 코딩 에이전트다. 코드를 수정할 때는 기존 스타일을 따른다.

사용자 질문: orders 테이블에서 최근 7일 동안 고객별 주문 금액 합계를 구하는 SQL 쿼리를 작성해줘.

프로젝트 정보: 이 프로젝트는 PostgreSQL을 사용한다.

관련 스키마:
  orders(id, customer_id, total_amount, created_at)
  customers(id, name, email)

이전 대화: 사용자는 날짜 조건을 한국 시간 기준으로 처리하길 원한다고 말한 적이 있다.
```

이걸 다 읽은 뒤에 답을 만든다. 답은 예를 들어 이렇게 나온다.

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

이 한 번의 주고받음 안에서 사용량은 크게 네 항목으로 나뉜다. 위에서 본 Input, Output, Reasoning, Cache Read다.

## 3. Input, Output, Reasoning — 들어가고 나오고 속으로 굴린 것

**Input**은 이번 답을 만들기 위해 AI가 읽은 모든 정보다. 위 예시로 보면 시스템 지시사항, 프로젝트 정보, DB 스키마, 이전 대화 맥락, 사용자 질문이 전부 input에 들어간다. 실제 작업할 때는 거기에 관련 코드 파일, 도구 실행 결과, 에러 로그까지 함께 붙는다. 그래서 사용자는 "SQL 좀 짜줘" 한 줄만 쳤는데도 input 토큰이 수천, 수만씩 찍히는 경우가 많다.

**Output**은 AI가 새로 써낸 결과다. 위에서는 SELECT 쿼리와 함께 붙는 설명 문장이 전부 output에 잡힌다. AI가 길게 설명할수록, 코드를 많이 만들어낼수록 output이 커진다. 반대로 "이 한 줄이면 됩니다" 정도로 답하면 output은 작다.

**Reasoning**은 AI가 답을 만들기 위해 내부적으로 굴린 추론 토큰이다. 위 SQL 예시로 치면 모델 안에서는 대략 이런 판단들이 도는 셈이다.

```
최근 7일 조건은 created_at에 걸면 되겠다.
고객별 합계니까 customer_id로 GROUP BY가 필요하다.
고객 이름까지 보이려면 customers와 JOIN해야 한다.
금액 합계는 SUM(total_amount)를 쓰면 된다.
정렬은 합계 내림차순이 자연스럽다.
```

이런 생각의 흐름이 사용자 화면에 그대로 보이지는 않는다. 그래도 답을 만들기 위한 계산은 분명히 일어나고, 일부 모델·도구는 그 양을 별도의 Reasoning 토큰으로 따로 기록한다. 모델에 따라 이 값이 표시되지 않거나 0으로 잡히기도 한다. 복잡한 코드 분석, 여러 파일 비교, 디버깅처럼 생각 단계가 많은 작업일수록 늘어난다.

세 가지를 한 줄로 묶으면, Input은 AI가 읽은 자료, Output은 AI가 써낸 결과, Reasoning은 그 사이에 속으로 굴린 계산량 정도가 된다.

## 4. 그럼 Cache Read는 결국 Input 아닌가?

여기서 자연스럽게 의문이 생긴다. "Cache Read도 결국 AI가 본 거면, 그건 input 아닌가?"

논리적으로는 맞다. 넓은 의미에서는 input의 일부다. 답을 만들 때 모델이 참고한 맥락이 맞기 때문이다. 다만 처리 방식과 비용이 일반 input과 달라서 별도 항목으로 따로 잡는다.

조금 더 풀어보면 이렇다. 첫 번째 요청에서 이런 내용이 들어갔다고 하자.

```
시스템 지시사항    5,000 토큰
프로젝트 스키마   10,000 토큰
사용자 질문         100 토큰
```

처음에는 이 앞부분을 모델 서버가 새로 처리한다. 한 번 읽고 이해해두는 작업을 거친다.

이어서 두 번째 요청이 들어온다.

```
이번에는 월별로 집계하는 쿼리로 바꿔줘.
```

질문은 100토큰짜리 한 줄이지만, 앞에 붙는 시스템 지시사항과 프로젝트 스키마는 거의 그대로다. 모델 제공사 서버는 "앞부분이 아까 본 것과 같네"라고 알아차리고 이미 처리해둔 결과를 그대로 재사용한다. 이때 재사용된 토큰이 **Cache Read**로 잡힌다. 정리하면 이런 그림이다.

```
새로 들어온 질문          → Input
재사용된 지시사항·스키마  → Cache Read
새로 써낸 SQL             → Output
```

그래서 ccusage의 Cache Read 숫자가 14,458,496처럼 어마어마하게 보여도, 그 대부분이 캐시 재사용이라면 실제 모델이 새로 처리한 작업은 그만큼 크지 않다는 뜻이다. 캐시 읽기 토큰은 일반 input 토큰보다 단가가 훨씬 싸게 매겨진다. OpenAI도 prompt caching이 반복되는 프롬프트를 더 빠르고 저렴하게 처리하기 위한 기능이며, 사용량 응답에 `cached_tokens`가 따로 표시된다고 설명한다. ([OpenAI Prompt Caching](https://platform.openai.com/docs/guides/prompt-caching)) Anthropic 쪽 사용량 리포트도 `uncached_input_tokens`, `cache_creation`, `cache_read_input_tokens`, `output_tokens`처럼 캐시 읽기를 별도 칸으로 잡는다. ([Anthropic Usage Report](https://docs.anthropic.com/en/api/admin-api/usage-cost/get-messages-usage-report))

다시 말해 Cache Read는 AI가 본 input의 일부이긴 한데, "이번에 새로 처리한" input이 아니라 "전에 처리해둔 걸 그대로 재사용한" input이기 때문에 비용 계산과 표시에서 따로 떼어둔다.

## 5. 그 캐시는 내 컴퓨터 메모리인가?

여기서 또 헷갈리기 쉬운 지점이 있다. "Cache Read라는 건 내 맥북의 RAM이나 디스크 캐시에서 읽었다는 뜻인가?"

대부분의 경우 그렇지 않다. 여기서 말하는 캐시는 모델 제공사 서버 쪽의 prompt cache다. 내 컴퓨터에 저장된 캐시가 아니라, Anthropic이나 OpenAI 서버가 잠깐 들고 있는 "최근 처리해본 프롬프트 앞부분"에 가깝다.

그래서 두 층을 깔끔히 나누는 게 편하다. 내 컴퓨터에 남는 사용 기록은 **로컬 로그**다. Claude Code와 Codex가 작업할 때마다 `.jsonl` 같은 형태로 적어두는 그 파일들이고, ccusage는 이걸 읽는다. 한편 Cache Read 자체가 일어나는 자리는 모델 서버 쪽 **prompt cache**다. 로컬 로그에 "Cache Read 1,234,567토큰"이라고 적혀 있다고 해서 내 컴퓨터에서 캐시를 읽은 건 아니다. 서버 쪽 캐시가 동작한 결과가 사용량으로 보고되어 내 로그에 적힌 것일 뿐이다.

## 6. 그럼 Claude Code랑 Codex는 어디서 도는가

여기서 한 번 더 헷갈린다. "그러면 Claude Code랑 Codex는 내 컴퓨터 자원을 쓰는 게 맞긴 한가?"

맞다. 다만 둘 다 쓴다. 도구 자체는 내 컴퓨터에서 실행되는 프로그램이고, 모델은 보통 클라우드에서 돈다.

내 컴퓨터에서 일어나는 일은 대략 이런 쪽이다. 터미널이나 앱을 띄우고, 프로젝트 파일을 찾아 읽고, 코드를 수정하고, 명령어를 실행하고, 실행 결과를 로그에 적고, 도구 사용을 제어한다. 반면 모델 서버에서 일어나는 일은 프롬프트를 이해하고, 코드를 분석하고, 답변을 만들고, 추론을 굴리고, 토큰을 세고, prompt cache를 굴리는 쪽이다. Claude Opus나 GPT 계열의 거대한 모델 자체가 내 맥북 안에서 돌아가는 건 아니다.

예를 들어 "이 SQL 쿼리 성능 좀 개선해줘"라고 던지면, 로컬 도구가 먼저 `schema.sql`, `query.sql`, 관련 README, 실행 로그 같은 걸 모은다. 그 묶음을 모델 서버로 보낸다. 서버에서 모델이 분석하고 답을 만든다. 그 답이 다시 내 컴퓨터로 돌아오고, Claude Code나 Codex가 그 결과를 받아 파일을 수정하거나 명령어를 실행한다.

그래서 ccusage가 보여주는 토큰 사용량은 결국 서버 쪽에서 일어난 모델 처리량이고, 그 결과만 내 컴퓨터에 로그로 남는다. ccusage는 그 로그를 다시 읽어 보기 좋게 정리해주는 셈이다.

## 7. ChatGPT 웹의 "메모리"와는 다른 이야기

비슷한 의문이 ChatGPT 쪽으로도 이어진다. ChatGPT에는 "메모리"라는 기능이 있는데, 이름만 보면 Cache Read와 비슷해 보일 수 있다. 하지만 둘은 다른 개념이다.

ChatGPT 메모리는 사용자의 선호·이름·작업 방식·과거 대화에서 유용한 정보 같은 걸 다음 대화에서 참고하기 위한 개인화 기능이다. ([OpenAI Memory FAQ](https://help.openai.com/en/articles/8590148-memory-faq)) 예를 들면 이런 걸 기억한다. "이 사용자는 한국어 답변을 선호한다", "이 사용자는 SQL 예시를 좋아한다", "이 사용자는 블로그 글을 '이다/한다' 문체로 쓴다" 같은 것들이다. 제품 기능으로서의 메모리에 가깝다.

반면 Cache Read는 모델 서버가 긴 프롬프트의 반복 부분을 더 싸고 빠르게 처리하기 위한 prompt cache다. 사용자에 대한 정보를 기억해두는 게 아니라, 모델이 똑같은 시스템 지시사항이나 같은 스키마를 매번 처음부터 처리하지 않도록 하는 최적화에 가깝다. 이름만 비슷할 뿐 역할이 다르다.

ChatGPT 웹 UI 내부에서도 비슷한 캐싱이나 최적화가 돌고 있을 가능성은 크다. 다만 일반 사용자가 ccusage처럼 input·output·cache read 토큰을 로컬에서 그대로 꺼내 보기는 어렵다. 웹 UI 쪽 사용 기록은 Claude Code나 Codex처럼 자세한 형태로 내 컴퓨터에 남는 구조가 아니기 때문이다.

## 8. 다음에 ccusage를 다시 켰을 때

지금까지 흐름을 머릿속에 한 번 깔아두면, 다음에 ccusage를 켜고 그 큰 숫자들을 봤을 때 훨씬 덜 어지럽다.

Claude Code나 Codex 같은 도구는 작업할 때마다 로컬에 사용 기록을 남기고, ccusage는 그걸 읽어 네 항목으로 보여준다. Input은 이번 답을 만들기 위해 AI가 읽은 자료의 양, Output은 새로 써낸 글·코드의 양, Reasoning은 답을 내기 위해 속으로 굴린 계산량, Cache Read는 서버 쪽 prompt cache에서 재사용된 input의 양이다. 도구는 내 컴퓨터에서 돌지만 모델의 두뇌는 대부분 클라우드에서 돌고, 그래서 Cache Read도 내 RAM이 아니라 서버 쪽 캐시 이야기다.

캐시 적중률을 올리는 법이나 토큰을 줄이기 위한 오픈소스 도구들은 따로 다룰 만한 주제다. 우선 "각 숫자가 뭘 의미하는지" 한 번 정리해두는 것만으로도 다음 ccusage 화면이 한결 읽힌다.

---

## 참고 자료

- [ccusage — Claude Code / Codex 사용량 리포터 (GitHub)](https://github.com/ryoppippi/ccusage)
- [Prompt caching — OpenAI Platform Docs](https://platform.openai.com/docs/guides/prompt-caching)
- [Messages usage report — Anthropic Admin API](https://docs.anthropic.com/en/api/admin-api/usage-cost/get-messages-usage-report)
- [Memory FAQ — OpenAI Help](https://help.openai.com/en/articles/8590148-memory-faq)
