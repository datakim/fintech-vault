# 손그림 다이어그램 생성기

블로그 글에 넣는 SVG 다이어그램을 만든다. 선을 두 번 그어 겹치는 러프 스케치 스타일에
채도를 낮춘 팔레트, 글씨는 나눔펜 손글씨체를 SVG 안에 직접 심는다(외부 폰트 로딩 없이
어디서 열어도 손글씨로 보인다).

## 처음 한 번 준비

폰트와 파이썬 가상환경은 용량이 커서 커밋하지 않는다. 아래로 만든다.

```bash
cd tools/diagrams
curl -sL -o NanumPen.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/nanumpenscript/NanumPenScript-Regular.ttf"
python3 -m venv fontenv
./fontenv/bin/pip install fonttools brotli
```

나눔펜은 OFL 라이선스다.

## 그림 만들기

```bash
cd tools/diagrams
python3 gen_ai_review.py ./out      # 그림 생성 (폰트 미포함)
python3 embed_fonts.py ./out ./final # 쓰인 글자만 추려 폰트를 심는다
cp final/*.svg ../../public/
```

새 글의 그림은 `gen_<주제>.py` 파일을 하나 만들어 `style.py`의 헬퍼를 쓴다.
`gen_ai_review.py`를 그대로 베껴서 시작하면 된다.

## 파일

- `style.py` — 팔레트와 그리기 헬퍼(`box`, `arr`, `T`, `ul`, `wrap`)
- `embed_fonts.py` — SVG가 실제로 쓰는 글자만 서브셋해서 인라인으로 심는다
- `gen_ai_review.py` — 예시 겸 실제로 쓰인 생성 스크립트

## 주의

- 상자 폭을 넉넉히 잡을 것. 손글씨체는 폭이 달라서 글자가 상자를 넘기 쉽다.
- 만든 뒤에는 브라우저로 열어 겹침을 눈으로 확인할 것.
