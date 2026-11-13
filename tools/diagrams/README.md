# 손그림 다이어그램 생성기

블로그 글에 넣는 SVG 다이어그램을 만든다. 스타일은 두 가지이고, 글씨는 쓰인 글자만 추려
SVG 안에 직접 심는다(외부 폰트 로딩 없이 어디서 열어도 같은 글씨로 보인다).

- **카드형 (`style_card.py`, 2026-11-13부터 새 글의 기본):** 크림색 바탕, 점선으로 묶은 영역,
  진한 윤곽선을 두른 파스텔 둥근 카드, 선 아이콘, 알약 모양 칩, 그림자 깐 주황 제목.
  글씨는 Gaegu 보통·굵게. 예시는 `gen_judge.py`.
- **러프 스케치 (`style.py`, 2026-11-12까지의 글):** 선을 두 번 그어 겹치는 스케치에
  채도를 낮춘 팔레트, 글씨는 나눔펜. 예전 글 그림을 고칠 때만 쓴다.

## 처음 한 번 준비

폰트와 파이썬 가상환경은 용량이 커서 커밋하지 않는다. 아래로 만든다.

```bash
cd tools/diagrams
curl -sL -o NanumPen.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/nanumpenscript/NanumPenScript-Regular.ttf"
curl -sL -o Gaegu-Regular.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/gaegu/Gaegu-Regular.ttf"
curl -sL -o Gaegu-Bold.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/gaegu/Gaegu-Bold.ttf"
python3 -m venv fontenv
./fontenv/bin/pip install fonttools brotli
```

나눔펜과 Gaegu는 OFL 라이선스다.

## 그림 만들기

```bash
cd tools/diagrams
python3 gen_judge.py ./out          # 그림 생성 (폰트 미포함)
python3 embed_fonts.py ./out ./final # 쓰인 글자만 추려 폰트를 심는다
cp final/*.svg ../../public/
```

새 글의 그림은 `gen_<주제>.py` 파일을 하나 만들어 `style_card.py`의 헬퍼
(`layer`, `card`, `chips`, `arrow`, `icon`, `title`, `wrap`)를 쓴다. `gen_judge.py`를 베껴서 시작하면 된다.
`embed_fonts.py`는 SVG 안의 자리표시자를 보고 폰트를 고른다(`__CARDFONT__`면 Gaegu, `__HANDFONT__`면 나눔펜).

## 파일

- `style_card.py`: 카드형 팔레트와 헬퍼
- `style.py`: 러프 스케치 팔레트와 헬퍼(`box`, `arr`, `T`, `ul`, `wrap`)
- `embed_fonts.py`: SVG가 실제로 쓰는 글자만 서브셋해서 인라인으로 심는다
- `gen_judge.py`: 카드형 예시 / `gen_ai_review.py`: 러프 스케치 예시

## 주의

- 상자 폭을 넉넉히 잡을 것. 손글씨체는 폭이 달라서 글자가 상자를 넘기 쉽다.
- Gaegu에는 가운뎃점(·)과 화살표(→)가 없다. `style_card.T`가 " · "를 쉼표로 바꾸고, 화살표는 `arrow()`로 그린다.
- 만든 뒤에는 열어서 겹침을 눈으로 확인할 것. 터미널에서는
  `qlmanage -t -s 1400 -o <폴더> final/그림.svg`로 PNG를 만들어 보면 빠르다.
