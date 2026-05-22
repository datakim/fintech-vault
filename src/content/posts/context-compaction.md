---
title: "컨텍스트 압축(Context Compaction): 에이전트에게 전부 넣지 말고 필요한 것만 남기기"
description: "LLM 에이전트에게 매번 전체 대화·로그·tool 결과를 다 넣을 수는 없음. 다음 판단에 필요한 작업 상태만 남기는 컨텍스트 압축 기법을 예시로 정리함."
pubDatetime: 2026-05-22T09:00:00Z
tags:
  - context
  - llm
  - ai-agent
  - harness
  - engineering
---

## 문제: 대화가 길어지면 전부 넣을 수 없음

에이전트는 한 번에 끝나지 않음. tool을 호출하고, 결과를 받고, 다시 판단하고, 또 호출함. 이게 수십 번 반복되면 대화 로그가 모델의 context window를 금방 넘김.

설령 window 안에 들어가더라도 문제임. 쓸데없는 로그가 잔뜩 끼면 모델이 정작 중요한 정보에 집중하지 못하고, 비용과 응답 속도도 같이 나빠짐.

그래서 필요한 게 컨텍스트 압축(context compaction)임. 핵심은 한 문장임.

> 다음 판단에 필요한 것만 남기고, 나머지는 버린다.

참고로 이건 "프롬프트 압축(prompt compression)"과는 다름. 프롬프트 압축은 문장을 토큰 단위로 줄이는 기법(예: LLMLingua)에 가깝고, 여기서 말하는 건 에이전트의 대화·작업 상태를 관리하는 컨텍스트 압축임.

가장 단순한 형태는 시스템 프롬프트와 사용자 요청은 유지하고, 중간 대화는 버리고, 최근 메시지 몇 개만 남기는 방식임.

압축 전:

```
[System Prompt]
[User Task]
... 오래된 중간 로그들 ...
[최근 메시지 1]
[최근 메시지 2]
```

압축 후:

```
[System Prompt]
[User Task]
[최근 메시지 1]
[최근 메시지 2]
```

이건 가장 기본 뼈대고, 실무에서는 보통 더 정교하게 함. 단계별로 봄.

## 1. 최근 메시지만 유지 (sliding window)

가장 단순한 방식임. 예를 들어 에이전트가 tool call을 20번 했으면, 전부 넣지 않고 최근 5개만 유지함.

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

장점은 단순하고 빠름. 단점은 과거의 중요한 정보가 같이 날아갈 수 있음. 예를 들어 3번째 단계에서 정한 중요한 제약을 그냥 까먹어 버림.

## 2. 요약 압축 (summarization)

중간 로그를 버리는 대신 요약함.

원래 로그가 이렇다면:

```
1. Agent opened Hacker News.
2. Agent clicked upvote.
3. Redirected to login page.
4. Agent said success, but URL was /login.
5. Verification failed.
```

압축 후에는 이렇게 만듦.

```
Summary so far:
- 에이전트가 Hacker News를 열었음.
- upvote 클릭 시 로그인 페이지로 리다이렉트됨.
- 직전의 "성공" 주장은 거짓이었음.
- 다음 시도는 로그인을 처리한 뒤 upvote를 검증해야 함.
```

sliding window보다 훨씬 실무적임. 무엇을 했고 무엇이 실패했는지가 살아남기 때문임.

## 3. 구조화 압축 (structured state)

에이전트 시스템에서는 자유로운 자연어 요약보다, 구조화해서 남기는 게 더 안전함.

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

이게 좋은 이유는, 모델이 다시 읽었을 때 헷갈릴 여지가 줄어듦. 자연어 요약은 해석이 흔들리지만, 구조화된 필드는 그대로 읽힘.

## 4. Tool 결과 압축

실무에서 context를 가장 많이 잡아먹는 건 보통 tool 결과임. SQL 결과, PDF 검색 결과, 브라우저 DOM, API 응답 같은 것들임.

원본:

```
SELECT * FROM transactions WHERE event_date BETWEEN '2026-05-01' AND '2026-05-20';
-- 128,492 rows returned
id | event_date | amount | status | ...
... (수천 줄 생략) ...
```

압축:

```
Query result summary:
- Date range: 2026-05-01 ~ 2026-05-20
- Total transactions: 128,492
- Approval rate: 94.2%
- Main anomaly: 2026-05-13 approval rate dropped to 87.1%
- Likely related segment: mobile wallet, new users
```

에이전트에게 필요한 건 raw result 전체가 아니라, 다음 판단에 쓸 관찰값임.

## 5. Memory snapshot 방식

장기 작업에서는 매번 대화 전체를 넣는 대신, "현재 상태판" 하나를 계속 갱신함.

```
Current task state:
- Objective: Build a fraud monitoring dashboard
- Completed: Metric definition, data source mapping
- Pending: Alert threshold logic
- Constraints: Use event_date, exclude 3DS fail cases
- User preference: Keep report simple and business-readable
```

대화가 흘러가도 이 상태판만 최신으로 유지하면 됨. 코딩 에이전트, 리서치 에이전트처럼 오래 도는 작업에 특히 중요함.

## 6. 압축할 때 절대 버리면 안 되는 것

압축에서 중요한 건 무조건 줄이는 게 아님. 버려도 되는 것과 버리면 안 되는 것을 구분하는 거임.

유지해야 하는 정보:

```
1. 원래 목표
2. 사용자 제약조건
3. 이미 내린 결정
4. 실패한 시도와 그 이유
5. 현재 상태
6. 다음 액션
7. 검증 기준
8. 권한/보안 관련 조건
```

버려도 되는 정보:

```
1. 반복된 tool log
2. 긴 raw output
3. 이미 요약된 검색 결과
4. 실패했지만 의미 없는 중간 시도
5. 모델의 장황한 reasoning 흔적
```

특히 "실패한 시도와 그 이유"는 꼭 남겨야 함. 이게 날아가면 에이전트가 같은 실수를 또 반복함.

## 7. 실무 설계: compress_context()

에이전트 Harness 안에 `compress_context()` 같은 함수를 하나 두면 깔끔함.

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

조금 더 좋은 구조는 대화 대신 상태를 통째로 들고 다니는 방식임.

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

언제 압축할지도 정해두면 좋음. 보통 토큰 사용량이 일정 임계치(예: context window의 70%)를 넘으면 트리거함.

## 핵심 인사이트

컨텍스트 압축은 단순히 "짧게 줄이기"가 아님. 정확히는 이거임.

> 에이전트가 다음 행동을 결정하는 데 필요한 작업 상태는 보존하면서, 불필요한 대화와 로그만 제거하는 것.

그래서 좋은 압축의 결과물은 요약문이 아니라 작업 상태 복원 파일에 가까움. 그 파일 하나만 보고도 에이전트가 "지금 뭘 하던 중이었고, 다음에 뭘 해야 하는지"를 복원할 수 있어야 함.

예를 들어 코드 리팩터링을 맡은 에이전트라면, 전체 대화를 계속 끌고 다니는 대신 이런 상태판을 유지함.

```
사용자 의도:
결제 모듈의 레거시 콜백 코드를 async/await로 리팩터링

확정된 방침:
- 외부 API 시그니처는 변경하지 않음
- 기존 단위 테스트는 그대로 통과해야 함

현재 단계:
- payment_service.py 리팩터링 완료
- webhook_handler.py 수정 중

남은 작업:
- 통합 테스트 실행
- 에러 핸들링 경로 점검

검증 기준:
- 전체 테스트 스위트 그린(green)
- 콜백 응답 시간 기존과 동일 (±5%)
```

raw 대화 50턴을 그대로 넘기는 대신 이 상태판 하나를 넘기는 것 — 이게 진짜 컨텍스트 압축임.

---

함께 보면 좋은 글: [AI Agent는 더 좋은 프롬프트가 아니라 더 좋은 Harness에서 나온다](/posts/ai-harness-engineering/)
