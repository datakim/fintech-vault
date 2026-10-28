import { getCollection, type CollectionEntry } from "astro:content";
import dayjs from "dayjs";
import { postFilter } from "./postFilter";
import { getPostSlug, getPostUrl } from "./getPostPaths";

/**
 * 지식 지도 데이터.
 *
 * 글 본문에 있는 내부 링크(영문은 `/en/<slug>/`, 한국어는 `/posts/<slug>/`)를
 * 모아 글 사이의 연결을 만들고, 태그로 주제를 정한 뒤 노드 위치를 빌드할 때 한 번
 * 계산한다. 위치 계산은 시드가 고정된 간단한 힘 기반 배치라서 빌드마다 같은 그림이
 * 나온다. 사이트 기본 언어는 영어(2026-10-26)라서 홈과 /graph/는 영문 그래프를 쓴다.
 */

export type GraphLang = "en" | "ko";

export type TopicId =
  | "finance-ai"
  | "payments"
  | "llm"
  | "ai-coding"
  | "world-model"
  | "notes";

export type Topic = {
  id: TopicId;
  label: string;
  labelEn: string;
  eyebrow: string;
  color: string;
};

export const TOPICS: Topic[] = [
  {
    id: "finance-ai",
    label: "금융 AI · FDS",
    labelEn: "Financial AI & fraud",
    eyebrow: "Financial AI",
    color: "#c8d4aa",
  },
  {
    id: "payments",
    label: "결제 · 커머스",
    labelEn: "Payments & commerce",
    eyebrow: "Payments",
    color: "#e6c99b",
  },
  {
    id: "llm",
    label: "LLM · 에이전트",
    labelEn: "LLMs & agents",
    eyebrow: "LLM Systems",
    color: "#9fc7cc",
  },
  {
    id: "ai-coding",
    label: "AI 코딩",
    labelEn: "AI coding",
    eyebrow: "AI Coding",
    color: "#8fd1b2",
  },
  {
    id: "world-model",
    label: "월드 모델",
    labelEn: "World models",
    eyebrow: "World Models",
    color: "#cbbfe0",
  },
  {
    id: "notes",
    label: "노트",
    labelEn: "Notes",
    eyebrow: "Notes",
    color: "#efece0",
  },
];

// 위에서부터 처음 맞는 규칙으로 주제를 정한다. 새 태그를 쓰면 여기에 더한다.
const TOPIC_RULES: [TopicId, string[]][] = [
  ["world-model", ["world-model"]],
  ["finance-ai", ["fds", "fraud-detection"]],
  [
    "payments",
    [
      "payments",
      "agentic-commerce",
      "stripe",
      "embedded-finance",
      "alipay",
      "china",
      "wechat",
      "tencent",
      "cbdc",
      "e-cny",
      "digital-currency",
      "super-app",
      "mini-program",
    ],
  ],
  ["finance-ai", ["financial-ai", "fintech", "time-series", "credit"]],
  [
    "ai-coding",
    [
      "ai-coding",
      "claude-code",
      "codex",
      "ccusage",
      "tokens",
      "tdd",
      "workflow",
      "rust",
    ],
  ],
  [
    "llm",
    [
      "llm",
      "ai-agent",
      "harness",
      "context",
      "ai-engineering",
      "data-analytics",
      "engineering",
    ],
  ],
];

const topicById = new Map(TOPICS.map(t => [t.id, t]));

export function topicOf(tags: string[] = []): Topic {
  for (const [id, ruleTags] of TOPIC_RULES) {
    if (tags.some(tag => ruleTags.includes(tag))) return topicById.get(id)!;
  }
  return topicById.get("notes")!;
}

export type GraphNode = {
  id: string;
  title: string;
  tags: string[];
  /** 다른 언어판 주소 (있을 때만) */
  alt?: string;
  short: string;
  description: string;
  url: string;
  date: string;
  topic: TopicId;
  out: string[];
  in: string[];
  degree: number;
  /** 0~1로 정규화한 위치 */
  x: number;
  y: number;
};

export type GraphTopic = Topic & {
  /** 이 그래프 언어로 된 주제 이름 */
  name: string;
  count: number;
  /** 주제 이름표 위치 (0~1) */
  lx: number;
  ly: number;
};

export type KnowledgeGraph = {
  nodes: GraphNode[];
  edges: { source: string; target: string }[];
  topics: GraphTopic[];
};

const linkRe = (prefix: string) =>
  new RegExp(
    `\\]\\(\\s*(?:https?:\\/\\/(?:www\\.financialailab\\.com|fintech-vault\\.vercel\\.app))?\\/${prefix}\\/([A-Za-z0-9_-]+)\\/?(?:#[^)\\s]*)?\\s*\\)`,
    "g"
  );

function shortTitle(title: string): string {
  const head = title.split(/[:：]/)[0].trim();
  return head.length > 24 ? `${head.slice(0, 23)}…` : head;
}

// 시드 고정 난수 (mulberry32)
function rng(seed: number) {
  let a = seed;
  return () => {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function layout(
  nodes: GraphNode[],
  edges: { source: string; target: string }[],
  topics: GraphTopic[]
) {
  const rand = rng(20261026);
  const present = topics.filter(t => t.count > 0);
  const centers = new Map<TopicId, { x: number; y: number }>();
  present.forEach((t, i) => {
    const a = -Math.PI / 2 + (i / present.length) * Math.PI * 2;
    centers.set(t.id, {
      x: 0.5 + 0.36 * Math.cos(a),
      y: 0.5 + 0.36 * Math.sin(a),
    });
  });

  const idx = new Map(nodes.map((n, i) => [n.id, i]));
  const pos = nodes.map(n => {
    const c = centers.get(n.topic)!;
    return {
      x: c.x + (rand() - 0.5) * 0.12,
      y: c.y + (rand() - 0.5) * 0.12,
    };
  });

  const ITER = 600;
  for (let it = 0; it < ITER; it++) {
    const alpha = 1 - it / ITER;
    const f = pos.map(() => ({ x: 0, y: 0 }));

    // 노드끼리 밀어내기
    for (let i = 0; i < pos.length; i++) {
      for (let j = i + 1; j < pos.length; j++) {
        const dx = pos[i].x - pos[j].x;
        const dy = pos[i].y - pos[j].y;
        const d2 = Math.max(dx * dx + dy * dy, 0.0004);
        const k = 0.00028 / d2;
        f[i].x += dx * k;
        f[i].y += dy * k;
        f[j].x -= dx * k;
        f[j].y -= dy * k;
      }
    }

    // 링크된 글끼리 당기기
    for (const e of edges) {
      const i = idx.get(e.source)!;
      const j = idx.get(e.target)!;
      const dx = pos[j].x - pos[i].x;
      const dy = pos[j].y - pos[i].y;
      const d = Math.sqrt(dx * dx + dy * dy) || 0.001;
      const k = ((d - 0.13) * 0.035) / d;
      f[i].x += dx * k;
      f[i].y += dy * k;
      f[j].x -= dx * k;
      f[j].y -= dy * k;
    }

    // 같은 주제끼리 모이기
    nodes.forEach((n, i) => {
      const c = centers.get(n.topic)!;
      f[i].x += (c.x - pos[i].x) * 0.07;
      f[i].y += (c.y - pos[i].y) * 0.07;
    });

    pos.forEach((p, i) => {
      const step = 0.03 * alpha + 0.002;
      p.x += Math.max(-step, Math.min(step, f[i].x));
      p.y += Math.max(-step, Math.min(step, f[i].y));
    });
  }

  // 0~1 범위로 다시 맞춘다
  const xs = pos.map(p => p.x);
  const ys = pos.map(p => p.y);
  const [minX, maxX] = [Math.min(...xs), Math.max(...xs)];
  const [minY, maxY] = [Math.min(...ys), Math.max(...ys)];
  nodes.forEach((n, i) => {
    n.x = (pos[i].x - minX) / (maxX - minX || 1);
    n.y = (pos[i].y - minY) / (maxY - minY || 1);
  });

  // 주제 이름표는 무리의 바깥쪽 가장자리 너머에 둔다
  for (const t of topics) {
    const members = nodes.filter(n => n.topic === t.id);
    if (members.length === 0) continue;
    const cx = members.reduce((s, n) => s + n.x, 0) / members.length;
    const cy = members.reduce((s, n) => s + n.y, 0) / members.length;
    let dx = cx - 0.5;
    let dy = cy - 0.5;
    const len = Math.sqrt(dx * dx + dy * dy) || 1;
    dx /= len;
    dy /= len;
    const reach = Math.max(
      0,
      ...members.map(n => (n.x - cx) * dx + (n.y - cy) * dy)
    );
    t.lx = Math.max(0.02, Math.min(0.98, cx + dx * (reach + 0.09)));
    t.ly = Math.max(-0.06, Math.min(1.06, cy + dy * (reach + 0.1)));
  }
}

type Entry = {
  id: string;
  title: string;
  description: string;
  pubDatetime: Date;
  tags: string[];
  body: string;
  url: string;
  alt?: string;
};

async function loadEntries(lang: GraphLang): Promise<Entry[]> {
  const enPosts = await getCollection("en", ({ data }) => !data.draft);
  const koPosts = (await getCollection("posts")).filter(postFilter);
  const koSlug = (p: CollectionEntry<"posts">) =>
    getPostSlug(p.id, p.filePath).replace(/^\//, "");
  const koIds = new Set(koPosts.map(koSlug));

  if (lang === "en") {
    return enPosts.map(p => ({
      id: p.id,
      title: p.data.title,
      description: p.data.description,
      pubDatetime: p.data.pubDatetime,
      tags: p.data.tags,
      body: p.body ?? "",
      url: `/en/${p.id}/`,
      alt:
        p.data.koSlug && koIds.has(p.data.koSlug)
          ? `/posts/${p.data.koSlug}/`
          : undefined,
    }));
  }

  const enByKo = new Map(
    enPosts.filter(p => p.data.koSlug).map(p => [p.data.koSlug!, p.id])
  );
  return koPosts.map(p => {
    const id = koSlug(p);
    return {
      id,
      title: p.data.title,
      description: p.data.description,
      pubDatetime: p.data.pubDatetime,
      tags: p.data.tags,
      body: p.body ?? "",
      url: getPostUrl(p.id, p.filePath, "ko").replace(/\/?$/, "/"),
      alt: enByKo.has(id) ? `/en/${enByKo.get(id)}/` : undefined,
    };
  });
}

async function build(lang: GraphLang): Promise<KnowledgeGraph> {
  const entries = (await loadEntries(lang)).sort(
    (a, b) =>
      new Date(a.pubDatetime).getTime() - new Date(b.pubDatetime).getTime()
  );
  const known = new Set(entries.map(e => e.id));

  const nodes: GraphNode[] = entries.map(e => ({
    id: e.id,
    title: e.title,
    tags: e.tags,
    alt: e.alt,
    short: shortTitle(e.title),
    description: e.description,
    url: e.url,
    date: dayjs(e.pubDatetime).format("YYYY.MM.DD"),
    topic: topicOf(e.tags).id,
    out: [],
    in: [],
    degree: 0,
    x: 0.5,
    y: 0.5,
  }));
  const byId = new Map(nodes.map(n => [n.id, n]));

  const re = linkRe(lang === "en" ? "en" : "posts");
  const edges: { source: string; target: string }[] = [];
  const seen = new Set<string>();
  for (const e of entries) {
    for (const m of e.body.matchAll(re)) {
      const target = m[1];
      const key = `${e.id}>${target}`;
      if (target === e.id || !known.has(target) || seen.has(key)) continue;
      seen.add(key);
      edges.push({ source: e.id, target });
      byId.get(e.id)!.out.push(target);
      byId.get(target)!.in.push(e.id);
    }
  }
  for (const n of nodes) n.degree = new Set([...n.out, ...n.in]).size;

  const topics: GraphTopic[] = TOPICS.map(t => ({
    ...t,
    name: lang === "en" ? t.labelEn : t.label,
    count: nodes.filter(n => n.topic === t.id).length,
    lx: 0.5,
    ly: 0.5,
  }));

  layout(nodes, edges, topics);
  return { nodes, edges, topics };
}

const cache = new Map<GraphLang, Promise<KnowledgeGraph>>();

export function getKnowledgeGraph(
  lang: GraphLang = "en"
): Promise<KnowledgeGraph> {
  if (!cache.has(lang)) cache.set(lang, build(lang));
  return cache.get(lang)!;
}
