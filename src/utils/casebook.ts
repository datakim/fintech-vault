/*
 * 핀테크 ML 사례집 (2026-10-30)
 * 핀테크 회사들이 자기 기술 블로그에 쓴 모델 이야기를 분야·방법별로 모은다.
 * 데이터는 src/content/cases/cases.json, 합치기는 tools/casebook/merge.py.
 */

import { getCollection, type CollectionEntry } from "astro:content";

import {
  DOMAINS,
  METHODS,
  REGIONS,
  type CaseLang,
} from "@/utils/casebookVocab";

export * from "@/utils/casebookVocab";

export type Case = CollectionEntry<"cases">["data"] & {
  id: string;
  /** 같은 원문을 인용한 이 블로그 글 (영문판, 한국어판) */
  ours?: { en: string; ko?: string };
};

/** 사례집이 다루는 기간. 이보다 오래된 글은 빼고, 시작점은 시간축의 왼쪽 끝이 된다. */
export const WINDOW_START = "2024-10";

const monthIndex = (ym: string) => {
  const [y, m] = ym.split("-").map(Number);
  return y * 12 + (m - 1);
};

export function monthLabel(index: number, lang: CaseLang) {
  const y = Math.floor(index / 12);
  const m = (index % 12) + 1;
  return lang === "ko"
    ? `${String(y).slice(2)}.${String(m).padStart(2, "0")}`
    : new Date(Date.UTC(y, m - 1, 1)).toLocaleString("en-GB", {
        month: "short",
        year: "numeric",
        timeZone: "UTC",
      });
}

const normUrl = (u: string) =>
  u
    .replace(/[?#].*$/, "")
    .replace(/\/+$/, "")
    .toLowerCase();

export async function getCasebook() {
  // 원문 주소를 본문에서 인용한 이 블로그 글을 찾아 "관련 글"로 잇는다.
  const posts = (await getCollection("en", ({ data }) => !data.draft)).map(
    p => ({ p, body: (p.body ?? "").toLowerCase() })
  );
  const oursFor = (c: CollectionEntry<"cases">["data"]): Case["ours"] => {
    if (c.related) return { en: c.related };
    const hit = posts.find(({ body }) => body.includes(normUrl(c.url)));
    if (!hit) return undefined;
    return {
      en: `/en/${hit.p.id}/`,
      ko: hit.p.data.koSlug ? `/posts/${hit.p.data.koSlug}/` : undefined,
    };
  };

  const cases: Case[] = (await getCollection("cases"))
    .map(e => ({ ...e.data, id: e.id, ours: oursFor(e.data) }))
    .filter(c => c.date.slice(0, 7) >= WINDOW_START)
    .sort(
      (a, b) =>
        b.date.localeCompare(a.date) || a.company.localeCompare(b.company)
    );

  const count = <K extends string>(keys: K[]) => {
    const m = new Map<K, number>();
    for (const k of keys) m.set(k, (m.get(k) ?? 0) + 1);
    return m;
  };

  const byMethod = count(cases.flatMap(c => c.methods));
  const methods = METHODS.filter(m => byMethod.has(m.id))
    .map(m => ({ ...m, count: byMethod.get(m.id)! }))
    .sort((a, b) => b.count - a.count);

  const byDomain = count(cases.map(c => c.domain));
  const domains = DOMAINS.map(d => ({ ...d, count: byDomain.get(d.id) ?? 0 }));

  const byCompany = count(cases.map(c => c.company));
  const companies = [...byCompany]
    .map(([name, n]) => ({ name, count: n }))
    .sort((a, b) => b.count - a.count || a.name.localeCompare(b.name));

  const byRegion = count(cases.map(c => c.region));
  const regions = [...byRegion]
    .map(([id, n]) => ({
      id,
      count: n,
      ...(REGIONS[id] ?? { en: id, ko: id }),
    }))
    .sort((a, b) => b.count - a.count);

  const first = monthIndex(WINDOW_START);
  const last = Math.max(
    first,
    ...cases.map(c => monthIndex(c.date.slice(0, 7)))
  );

  return {
    cases,
    methods,
    domains,
    companies,
    regions,
    months: { first, last },
    monthOf: (c: Case) => monthIndex(c.date.slice(0, 7)),
    latest: cases[0]?.date,
  };
}

export type Casebook = Awaited<ReturnType<typeof getCasebook>>;
