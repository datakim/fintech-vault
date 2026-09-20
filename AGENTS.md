# AGENTS.md: Fintech Vault 블로그 인수인계 (Codex용)

이 문서는 Claude Code에서 하던 블로그 작업을 Codex로 넘기기 위한 인수인계다. 2026-09-20 기준.
`CLAUDE.md`와 겹치는 내용이 있는데, 둘이 다르면 **이 문서가 우선**한다. 이 문서 하나만 읽으면 글 하나를 기획하고 쓰고 올리는 데 필요한 건 다 있어야 한다. 부족하면 이 문서를 고쳐라.

---

## 1. 이게 뭔가

- **Fintech Vault**: 김태헌(Elliot)의 개인 테크 블로그. 라이브 https://fintech-vault.vercel.app
- 저자: 이커머스 핀테크 조직의 데이터 사이언티스트, 아주대 AI대학원 겸임교수(금융 AI), 캐글 그랜드마스터. 저서 『주니어 AI 엔지니어가 반드시 알아야 할 실무 지식』(한빛미디어, 2026), Manning 『Financial AI in Practice』(MEAP).
- 목적: 저자가 공부하고 생각한 걸 저장·공유하는 곳. 뉴스레터 요약 채널이 아니다. 글의 중심은 **저자의 인사이트**이고 사례·기사는 재료다. 책 홍보 연재(간접, 하단 링크만)도 일부 있다.
- 스택: AstroPaper v6 / Astro, pnpm. `main`에 push하면 Vercel이 자동 배포.
- 원격: https://github.com/datakim/fintech-vault (공개 저장소라는 걸 항상 염두에 둘 것)

## 2. 저장소 구조

```
src/content/posts/*.md      한국어 글 (25편 커밋됨)
src/content/en/*.md         영문 글 (24편). frontmatter의 koSlug로 한국어 글과 짝
src/content/pages/about.md, about-en.md
src/content/books/          책 연습문제 해답 코너 (별도 섹션)
src/pages/en/               영문 라우트 (/en/, /en/<slug>/, /en/about/)
src/components/Header.astro 상단 탭: Posts(KR) · Posts(ENG) · Books · Tags · About
public/*.svg, *.png         이미지. 마크다운에서 /파일명 으로 참조
tools/diagrams/             손그림 스타일 SVG 다이어그램 생성기 (아래 8절)
CLAUDE.md                   이전 도구용 가이드. 내용은 이 문서에 흡수됨
```

## 3. 뭐가 올라가 있는지 보는 법

- 라이브 목록: https://fintech-vault.vercel.app/posts/ (한국어), https://fintech-vault.vercel.app/en/ (영문)
- 로컬: `ls src/content/posts/` / `ls src/content/en/`. 제목만 훑으려면
  `grep -h '^title:' src/content/posts/*.md`
- 한·영 짝 확인: `grep -l 'koSlug: <slug>' src/content/en/*.md`
- 최근 작업 이력: `git log --oneline -30`
- 어떤 글이 어떤 톤인지 감 잡으려면 이 셋을 먼저 읽어라:
  `reviewed-by-ai.md`(잡담체), `fde-forward-deployed-engineer.md`(분석), `analyst-deliverables.md`(가장 최근, 피드백 다 반영된 상태)

## 4. 글 하나 올리는 절차 (반드시 이 순서)

1. **기획안 먼저.** 긴 글은 쓰기 전에 구성안(도입·절 제목·핵심 주장·그림 계획·제목 후보 3~4개)을 보여주고 승인받는다. 저자가 이 절차를 좋아한다. 제목은 저자가 고른다.
2. **초안 작성** → `src/content/posts/<slug>.md`. 그림이 있으면 8절대로 만든다.
3. **자동 검사** (7절) 전부 통과.
4. **저자 확인.** 초안을 보여주고 "올려줘" 소리를 들은 뒤에만 배포한다. 저자가 "별로"라고 하면 어디가 걸리는지 듣고 고친다. 보통 두 번은 고친다.
5. **커밋은 파일을 지정해서.** `git add -A` 금지 (10절). 커밋 메시지 예: `Add post: <영문 요약>`
6. `git push` → Vercel 자동 배포.
7. **라이브 확인**: 아래 스크립트로 200 뜰 때까지 폴링한 뒤 그림 URL과 `**` 노출을 본다. 배포 직후 404는 CDN 전파 지연이라 10초 간격으로 다시 본다.

```bash
SLUG=<slug>
for i in $(seq 1 40); do
  code=$(curl -s -o /dev/null -w '%{http_code}' https://fintech-vault.vercel.app/posts/$SLUG/)
  if [ "$code" = "200" ]; then echo "live after $i"; \
    curl -s https://fintech-vault.vercel.app/posts/$SLUG/ | grep -o '\*\*' | wc -l; break; fi
  sleep 10
done
```

8. 저자에게 URL과 반영 내용, 확인 필요한 부분을 짧게 보고.

## 5. Frontmatter

```yaml
---
title: "제목"
description: "미리보기에 뜨는 2~3문장. 핵심 수치나 결론을 담는다."
pubDatetime: 2026-09-20T03:00:00Z   # date -u 로 확인한 실제 시각. 미래면 예약 글로 숨겨진다!
tags:
  - financial-ai
---
```

- `pubDatetime`은 반드시 `date -u '+%Y-%m-%dT%H:%M:%SZ'`로 확인해서 **현재보다 과거**로 넣는다. 미래 시각을 넣으면 빌드에서 빠지고 아무 에러도 안 난다 (실제로 한 번 당했다).
- slug는 영문 소문자·하이픈. 예: `kyc-to-kya`, `analyst-deliverables`.
- tags는 기존 것에서 고른다: `financial-ai fintech ai-agent payments engineering agentic-commerce llm ai-coding claude-code alipay china super-app cbdc machine-learning world-model ai-engineering data-analytics`. 새 태그는 꼭 필요할 때만.
- 영문 글은 `src/content/en/<같은 slug>.md`에 두고 `koSlug: <slug>`를 추가한다.

## 6. 톤앤매너 (가장 중요, 여기서 제일 많이 반려된다)

### 하드 룰
- **평서체.** ~이다/~한다. 존댓말(~습니다/~요) 금지. 검사: `grep -nE '습니다|입니다|합니다' <file>`
- **em dash(—) 금지.** 본문·캡션·참고자료·그림 텍스트 전부. 삽입구는 괄호나 쉼표, 아니면 문장을 끊는다. 참고자료 목록은 `[제목 (매체)](URL)`.
- **도입부 "> 핵심 요약:" 박스 금지.** 바로 본문으로 시작한다.
- **출처를 서사로 드러내지 않는다.** "이 글을 읽고 정리해봤다", "X를 재료로 썼다" 금지. 출처는 인라인 `([매체](URL))`와 하단 `## 참고 자료`로만. 단, 어떤 글 자체를 다루는 글(앤드류 응 스킬맵, 앤트로픽 데이터팀)은 그 글을 주제로 직접 언급해도 된다.
- **개인 의견은 `## N. 개인적인 견해`** 한 절로. "핵심 인사이트", "인사이트 1/2/3" 금지.
- **마무리를 한 줄 슬로건으로 끝내지 않는다.** 자연스러운 두어 문장으로 닫는다.
- **팩트와 해석 분리.** 회사 발표 수치는 "발표 기준", 보도는 "보도 기준"으로 낮춘다. 확정 단정("완전히 대체했다") 금지. 글 끝에 이탤릭 작성기준 노트: `_본 글은 YYYY년 M월 D일 기준 …_`
- **날짜 정합성.** 오늘 나온 자료를 "며칠 들여다봤다"고 쓰면 안 된다. 실제로 한 번 지적받았다.

### 저자가 "AI 티"라고 지적한 것 (원문 그대로)
- "'결론은 명확하다' 이런 어투가 좀 AI가 작성한 것 같아서 별로" → "분명하다/명확하다/~가 핵심이다"로 문단을 여닫지 않는다.
- "이 글은 그 판정 기록이다 ← 이런 건 좀 너무 인공지능 티가 많이 남" → 글 자체에 대한 메타 서술 금지.
- "굳이 놓친 걸 알았다고 할 필요는 없고" → "예전에 놓쳤던 걸 깨달았다" 식 자기 서사 금지.
- "6월엔 입구를 만들었고, 8월엔 반대쪽을 깔았다 ← 이런 표현은 너무 AI 같음" → **대구(對句), 대칭 구조 금지.** 소제목도 평범한 서술이나 질문으로.
- "— 이거는 AI가 많이 쓰는 거라 빼줘" → em dash.
- "약간의 구어체는 섞여 들어가야 할 듯. ~한다. ~이다. 뚝뚝 끊어지는 게 좀 있어" → 종결어미를 섞는다: `~거든`, `~잖나`, `~하니까`, `~더라`, `~지 싶다`, `~인 셈이다`, `~해버린다`. 단, 한 형태가 너무 반복돼도 지적받는다 ("종결어미가 너무 일관되게 ~거다 ~이다"). 한 절짜리 문장을 마침표로 계속 끊지 말고 이어 붙여서 리듬을 만든다.
- "갑자기 전에 쓴 블로그들 내용이 어거지로 들어가 있는 느낌" → **예전 글 링크를 근거로 끌어오지 않는다.** 정말 같은 사례일 때 하나 정도만. 한 절에 다섯 개 링크는 반려된다.
- "글도 뚝뚝 끊기고 난잡해. 로지컬하지 않은 듯" → 절마다 하는 일이 하나여야 하고, 다음 절이 앞 절에서 나와야 한다. 결론이 앞에서 준비되지 않은 채 튀어나오면 안 된다.

### 그 외 피할 것 (humanizer 스킬 기준, 12절)
"정리하면 / 짚고 넘어가면 / 하나씩 보자" 같은 예고 · "솔직히 / 분명히 해두면 / 한 가지 덧붙이면" 같은 정직함 연출 · "오해 없도록, ~라는 뜻은 아니다"처럼 없는 반론과 싸우기 · 세 개짜리 나열 강박 · 문단마다 마무리 요약 · "또한/게다가/더 나아가" 연결어 쌓기 · "~의 시대가 열렸다" 의미 부풀리기 · "데이터가 말해준다" 허위 행위자 · 목록 항목마다 굵은 라벨+콜론 · 짧은 조각 문장으로 극적 효과. 검사: `grep -nE '핵심은|본질은|분명하다|명확하다|정리하면|짚고 넘어|솔직히|한 가지 덧붙|또한|게다가|더 나아가' <file>`

### 제목
통과한 제목(사람 말 같은 것):
- `[잡담] 요즘 내 보고서를 제일 먼저 읽는 건 팀장이 아니다`
- `AI 시대의 일 (feat. 약간의 철학 리서치)` ← 저자가 "제일 사람 같다"고 고른 것
- `앤트로픽 데이터팀을 보며: 분석가가 내놓는 게 달라지고 있다`
- `KYC 다음은 KYA다: 에이전트가 결제할 때 확인해야 하는 것`
- `FDE에 대한 고찰: 이름은 열 개인데 하는 일은 하나다`

반려된 제목(AI스럽다고 한 것): `직업 말고, 세상에 개입하는 방식으로 나눠보면`, `만드는 게 싸지면 무엇이 남나`. 물음표 제목, "X 말고 Y로" 대조, 추상명사 덩어리를 피한다. 후보 3~4개를 주면 저자가 고른다.

### 길이와 구조
- 보통 절 5~7개, 각 절에 한 가지. `## 1. 제목` 번호 형식.
- 그림 캡션은 그림 바로 아래 이탤릭 한 줄. 캡션도 슬로건 금지.
- 하단: `**함께 보면 좋은 글:**` 2~3개(억지로 채우지 않는다) → `## 참고 자료` → 이탤릭 작성기준 노트.
- 책 홍보 연재 글은 본문 뒤에 `## 책 소개` 절, 서점 링크 위에 한 줄 CTA, 그 앞에 본문과 책을 잇는 다리 문단 하나.

## 7. 자동 검사 (커밋 전에 전부)

```bash
F=src/content/posts/<slug>.md
grep -c '—' $F                                  # 0이어야 함
grep -nE '습니다|입니다|합니다' $F                # 없어야 함
grep -nE '핵심은|본질은|분명하다|명확하다|정리하면|짚고 넘어|솔직히|한 가지 덧붙|또한|게다가|더 나아가' $F
pnpm build 2>&1 | grep -iE '^- [0-9]+ error'    # 0 errors
# ** 렌더링 함정: 닫는 **가 ) 나 " 뒤에 오고 그 뒤에 한글이 붙으면 화면에 ** 가 그대로 노출된다.
# 정규식으로는 못 잡는다. 빌드 결과물로만 확정한다. 출력이 없으면 정상.
for f in dist/posts/*/index.html; do n=$(grep -o '\*\*' "$f" | wc -l | tr -d ' '); [ "$n" != "0" ] && echo "$n  $f"; done
# 이미지·내부 링크
grep -oE 'src="/[a-z0-9-]+\.(svg|png|jpg)"' dist/posts/<slug>/index.html | sed 's|src="/||; s|"||' | while read f; do [ -f "dist/$f" ] || echo "MISSING $f"; done
grep -oE 'href="/posts/[a-z0-9-]+/"' dist/posts/<slug>/index.html | sort -u | sed 's|href="/posts/||; s|/"||' | while read s; do [ -d "dist/posts/$s" ] || echo "BROKEN /posts/$s/"; done
```

`**` 고치는 법: `**"돈을 다루는 깊이"**다` → `"**돈을 다루는 깊이**"다` (따옴표·괄호를 볼드 밖으로).

## 8. 그림 (손그림 스타일 SVG)

저자가 "그림체가 너무 AI가 바로 만든 것 같다"고 해서 만든 시스템이다. 새 글에 그림이 필요하면 이 스타일로 뽑는다. 절대 다른 스타일(선명한 인포그래픽, 이모지, 쨍한 색)로 가지 않는다.

- 공통 스타일: `tools/diagrams/style.py` (`box`, `T`, `arr`, `ul`, `wrap`, 색상 `INK BLUE RED GREEN AMBER PURPLE TEAL`, 워시 `"blue" "red" …`). 흔들리는 두 번 그은 선, 번진 채색, 도트 종이 배경, 나눔펜 손글씨.
- 생성기: `tools/diagrams/gen_<주제>.py`. 최근 것(`gen_analyst.py`, `gen_kya.py`, `gen_work.py`)을 복사해서 시작하면 된다. 캔버스는 보통 W 880~940, H 400~560. 텍스트는 `T(x, y, "…", size, color, weight="bold")`, 박스는 `box(r, x, y, w, h, wash, color, sw)`.
- 폰트 임베딩: `embed_fonts.py`가 나눔펜을 글자 단위로 서브셋해서 SVG 안에 박는다. 그래서 `<img>`로 로드돼도 손글씨가 나온다. 폰트·가상환경은 gitignore라 처음 한 번 `tools/diagrams/README.md`대로 받아야 한다.
- 실행:
  ```bash
  cd tools/diagrams
  python3 gen_<주제>.py ./out && python3 embed_fonts.py ./out ./final && cp final/*.svg ../../public/
  ```
- **반드시 렌더링해서 눈으로 본다.** 글자 겹침, 박스 캔버스 이탈, 캡션이 박스 밑변에 걸리는 일이 거의 매번 한두 개 난다. 확인 방법(브라우저 도구 없이):
  ```bash
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars \
    --window-size=900,500 --screenshot=/tmp/check.png "file://$PWD/public/<name>.svg"
  ```
  그 PNG를 열어보고 겹치면 좌표 고쳐서 다시 뽑는다.
- 자주 나는 버그: 마지막 박스가 캔버스 폭을 넘음(x + n*(w+gap) 계산), 행 레이블이 박스 테두리에 걸림(간격 24px 이상), 하단 캡션이 마지막 박스와 겹침(H를 늘리고 캡션을 내림), 영문은 한글보다 길어서 폰트를 1~2 줄여야 함.
- 그림 텍스트에도 em dash 금지. 한자·중국어는 폰트에 없으니 쓰지 않는다(한글·영문·숫자만).
- 영문판 그림은 `gen_<주제>_en.py` → `<name>-en.svg`.

## 9. 영문 섹션

- 한국어 글마다 영문판이 `src/content/en/<slug>.md`에 있다 (`koSlug`로 연결). 새 한국어 글을 올리면 영문판도 같이 만드는 게 지금까지의 관례였다 (저자가 "전체 다" 하라고 했음). 단, 반드시 저자에게 같이 올릴지 물어본다.
- 번역이 아니라 같은 글을 영어로 다시 쓰는 것에 가깝다. 영국식 철자(organisation, colour)를 써왔다. 한국 고유 맥락(교보문고, 배달의민족)은 영어 독자용으로 한 줄 설명을 붙인다.
- 그림은 영문으로 다시 뽑는다(`-en.svg`). 원본이 스크린샷·차트면 그대로 쓴다.
- 영문 글에서 내부 링크는 `/en/<slug>/`로. 아직 영문판이 없는 글은 링크하지 않는다.
- About도 한·영 분리: `about.md`(한국 책 먼저), `about-en.md`(Manning 먼저, 한국 책은 "· Korean" 표시).

## 10. 절대 하지 말 것

- **PDF를 커밋하지 않는다.** 책 원고(`수정_주니어 AI 엔지니어_*.pdf`)가 로컬에 있다. `.gitignore`에 `*.pdf`가 있지만 `git add -f`나 이름 바꿔 올리는 일도 없어야 한다. 저자 원문: "PDF는 절대 올리면 안 됨".
- **`git add -A` 금지.** 올리지 말라고 한 초안(`src/content/posts/opik-hands-on.md`와 `public/opik-*.svg`, `tools/diagrams/gen_opik.py`)이 로컬에 있어서 한 번 딸려 올라갔었다. 항상 파일을 지정해서 `git add`.
- 저자 승인 없이 배포하지 않는다. 초안 → 확인 → 배포.
- `pubDatetime`에 미래 시각을 넣지 않는다.
- 팀 사례, 수치, 인용을 지어내지 않는다. 저자가 준 것과 원문에 있는 것만.
- 블로그 제목·About 등 사이트 설정은 묻지 않고 바꾸지 않는다.

## 11. 지금 상태와 미결 (2026-09-20)

로컬에만 있고 커밋 안 된 것:
- `src/content/posts/kyc-to-kya.md` + `public/kya-*.svg` + `tools/diagrams/gen_kya.py`: 초안 완성, 저자 검토 끝남. **날짜가 8월 18일**로 돼 있어서 지금 올리면 목록 아래로 묻힌다. 올릴 때 pubDatetime과 본문 끝의 "8월 18일 기준" 노트를 배포일로 바꿀지 저자에게 물어야 한다.
- `src/content/posts/ai-era-work-1.md` + `public/work-*.svg` + `tools/diagrams/gen_work.py`: 한 번 반려("난잡, 로지컬하지 않음, 예전 글 억지 인용")돼서 다시 썼고 **재검토 대기**. 2편 "AI 시대의 일 (2) 역할마다 AI를 어떻게 쓰나"는 1편 확정 후 쓰기로 함. `work-ai-press.svg`는 2편용으로 만들어둔 그림.
- `opik-hands-on.md`: 저자가 "그닥"이라고 해서 **올리지 않는** 초안. 건드리지 말고 커밋하지 말 것.

예정된 것:
- 책 홍보 연재 3편: "확률 엔진 위에 안정성을 쌓는 다섯 겹의 안전망" (2편 말미에 예고함). 1편 `ai-system-fails-outside-model`, 2편 `data-rots-quietly` 참고.
- 집필 후기(한빛미디어 채널용 워드 문서, `~/Downloads/집필후기_주니어AI엔지니어.docx`)에 실물 책 사진 추가 예정.
- 블로그 제목이 "Elliot's 핀테크/금융 AI 블로그"인데 책은 김태헌 이름. 실명으로 바꿀지 저자가 아직 결정 안 함.

## 12. 참고

- AI 티 지우기 기준(저자가 참고하라고 지정): https://github.com/blader/humanizer , https://github.com/jooray/humanizer
- 이 문서를 고칠 때는 6절(톤)과 11절(상태)을 최신으로 유지하는 게 제일 중요하다.
