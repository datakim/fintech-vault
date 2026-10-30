#!/usr/bin/env python3
"""사례집 후보 뽑기.

sources.json 의 피드를 읽어 최근 N일 안에 올라온 글 가운데
cases.json 과 seen.json 에 없는 것만 JSON으로 내보낸다. 판단은 하지 않는다.

    python3 tools/casebook/candidates.py --days 21 > /tmp/candidates.json
"""
import argparse
import html.entities
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/128 Safari/537.36"
ATOM = "{http://www.w3.org/2005/Atom}"

# 제목·요약에 이런 말이 있으면 먼저 볼 후보로 표시만 한다(걸러내지는 않는다).
HINT = re.compile(
    r"\b(ml|ai|llm|model|models|agent|agents|fraud|risk|credit|underwrit|recommend|"
    r"personaliz|forecast|embedding|transformer|anomal|scam|aml|machine learning|genai)\b"
    r"|머신러닝|모델|추천|이상거래|사기|신용|에이전트|예측|인공지능|LLM|AI",
    re.I,
)


def norm(u: str) -> str:
    return re.sub(r"[?#].*$", "", u).rstrip("/").lower()


def parse_date(s: str | None) -> datetime | None:
    if not s:
        return None
    s = s.strip()
    try:
        d = parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def xml_safe(raw: bytes) -> bytes:
    """XML에 없는 HTML 개체(&nbsp; 등)를 숫자 개체로 바꾼다."""
    def sub(m):
        cp = html.entities.name2codepoint.get(m.group(1))
        return f"&#{cp};" if cp else m.group(0)
    s = raw.decode("utf-8", "replace")
    return re.sub(r"&(?!(?:amp|lt|gt|quot|apos);)([A-Za-z][A-Za-z0-9]*);", sub, s).encode()


def text(el, *tags):
    for t in tags:
        x = el.find(t)
        if x is not None and (x.text or x.get("href")):
            return (x.text or x.get("href") or "").strip()
    return ""


def read_feed(src: dict) -> tuple[dict, list[dict] | str]:
    try:
        req = urllib.request.Request(src["url"], headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as r:
            root = ET.fromstring(xml_safe(r.read()))
    except Exception as e:  # 네트워크·파싱 실패는 보고만 한다
        return src, f"{type(e).__name__}: {e}"[:160]
    out = []
    for it in root.iter("item"):
        out.append({
            "title": text(it, "title"),
            "url": text(it, "link"),
            "date": parse_date(text(it, "pubDate", "{http://purl.org/dc/elements/1.1/}date")),
            "summary": re.sub(r"<[^>]+>", " ", text(it, "description"))[:300],
        })
    for it in root.iter(f"{ATOM}entry"):
        link = next((l.get("href") for l in it.findall(f"{ATOM}link") if l.get("rel") in (None, "alternate")), "")
        out.append({
            "title": text(it, f"{ATOM}title"),
            "url": link,
            "date": parse_date(text(it, f"{ATOM}published", f"{ATOM}updated")),
            "summary": re.sub(r"<[^>]+>", " ", text(it, f"{ATOM}summary", f"{ATOM}content"))[:300],
        })
    return src, out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=21)
    args = ap.parse_args()

    sources = json.loads((HERE / "sources.json").read_text())
    known = {norm(e["url"]) for e in json.loads((ROOT / "src/content/cases/cases.json").read_text())}
    known |= {norm(e["url"]) for e in json.loads((HERE / "seen.json").read_text())}
    since = datetime.now(timezone.utc) - timedelta(days=args.days)

    candidates, failed = [], []
    with ThreadPoolExecutor(10) as ex:
        for src, items in ex.map(read_feed, sources["feeds"]):
            if isinstance(items, str):
                failed.append({"feed": src["url"], "error": items})
                continue
            for it in items:
                if not it["url"] or norm(it["url"]) in known:
                    continue
                if it["date"] and it["date"] < since:
                    continue
                candidates.append({
                    "company": src["company"],
                    "title": it["title"],
                    "url": re.sub(r"\?source=rss[^#]*", "", it["url"]),
                    "date": it["date"].date().isoformat() if it["date"] else None,
                    "hint": bool(HINT.search(f"{it['title']} {it['summary']}")),
                    "summary": it["summary"].strip(),
                })

    candidates.sort(key=lambda c: (not c["hint"], c["date"] or ""), reverse=False)
    json.dump({"since": since.date().isoformat(), "candidates": candidates, "failed_feeds": failed,
               "pages": sources["pages"], "searches": sources["searches"]},
              sys.stdout, ensure_ascii=False, indent=2)
    print(f"\n{len(candidates)} candidates ({sum(c['hint'] for c in candidates)} hinted), "
          f"{len(failed)} feeds failed", file=sys.stderr)


if __name__ == "__main__":
    main()
