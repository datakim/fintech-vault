#!/usr/bin/env python3
"""사례집 데이터 합치기.

수집한 JSON 파일들(배열)을 받아 어휘·기간·중복을 검사하고
src/content/cases/cases.json 을 새로 쓴다. 기존 파일도 입력으로 넣으면 덧붙이기가 된다.

    python3 tools/casebook/merge.py src/content/cases/cases.json new-batch.json ...
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "src/content/cases/cases.json"
VOCAB = (ROOT / "src/utils/casebookVocab.ts").read_text()

WINDOW = ("2024-10-01", "2026-12-31")


def ids(const: str) -> set[str]:
    block = VOCAB.split(f"export const {const} = [", 1)[1].split("] as const", 1)[0]
    return set(re.findall(r'id: "([^"]+)"', block))


DOMAINS = ids("DOMAINS")
METHODS = ids("METHODS")
REGIONS = set(re.findall(r"^  (\w+): \{ en:", VOCAB, re.M))

KEYS = [
    "id", "company", "region", "title", "url", "date", "lang", "domain", "methods",
    "problem_en", "problem_ko", "note_en", "note_ko", "metric", "related",
]
REQUIRED = [k for k in KEYS if k not in ("metric", "related")]


def norm_url(u: str) -> str:
    return re.sub(r"[?#].*$", "", u).rstrip("/").lower()


def main(paths: list[str]) -> None:
    seen_url: dict[str, dict] = {}
    seen_id: set[str] = set()
    problems: list[str] = []

    for path in paths:
        for e in json.loads(Path(path).read_text()):
            where = f"{Path(path).name}:{e.get('id')}"
            missing = [k for k in REQUIRED if not e.get(k)]
            if missing:
                problems.append(f"{where} missing {missing}")
                continue
            if not (WINDOW[0] <= e["date"] <= WINDOW[1]):
                problems.append(f"{where} date {e['date']} outside window")
                continue
            if e["domain"] not in DOMAINS:
                problems.append(f"{where} unknown domain {e['domain']}")
                continue
            bad = [m for m in e["methods"] if m not in METHODS]
            if bad:
                problems.append(f"{where} dropped unknown methods {bad}")
                e["methods"] = [m for m in e["methods"] if m in METHODS]
            e["methods"] = list(dict.fromkeys(e["methods"]))[:4]
            if not e["methods"]:
                problems.append(f"{where} no valid methods")
                continue
            if e["region"] not in REGIONS:
                problems.append(f"{where} region {e['region']} -> Global")
                e["region"] = "Global"
            for k in ("note_en", "note_ko", "problem_en", "problem_ko", "metric"):
                if k in e and "—" in e[k]:
                    e[k] = e[k].replace(" — ", ", ").replace("—", ", ")
            key = norm_url(e["url"])
            if key in seen_url:
                problems.append(f"{where} duplicate of {seen_url[key]['id']}")
                continue
            base, n = e["id"], 2
            while e["id"] in seen_id:
                e["id"] = f"{base}-{n}"
                n += 1
            seen_id.add(e["id"])
            seen_url[key] = {k: e[k] for k in KEYS if k in e}

    out = sorted(seen_url.values(), key=lambda e: (e["date"], e["company"]), reverse=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")

    for p in problems:
        print("·", p)
    by = {}
    for e in out:
        by[e["domain"]] = by.get(e["domain"], 0) + 1
    print(f"{len(out)} cases from {len({e['company'] for e in out})} companies -> {OUT.relative_to(ROOT)}")
    print("by domain:", dict(sorted(by.items())))


if __name__ == "__main__":
    main(sys.argv[1:])
