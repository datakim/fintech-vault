import { fontData, experimental_getFontFileURL } from "astro:assets";
import satori from "satori";
import sharp from "sharp";
import { getFontPathByWeight } from "@/utils/getFontPathByWeight";
import {
  TOPICS,
  topicOf,
  type GraphLang,
  type KnowledgeGraph,
} from "@/utils/knowledgeGraph";
import config from "@/config";

/*
 * 링크 미리보기(OG) 이미지 (2026-10-29)
 * 사이트 다크 팔레트(딥그린·크림·세이지)에 지식 지도를 깔고,
 * 글 이미지에서는 그 글의 점과 연결선만 밝힌다.
 */

const W = 1200;
const H = 630;
const BG = "#152c30";
const FG = "#f2f0e6";
const SAGE = "#cbd8ad";
const MUTED = "#a9b8b0";
const LINE = "#2b4a4b";

type Font = {
  name: string;
  data: ArrayBuffer;
  weight: 400 | 700;
  style: "normal";
};

let fontsPromise: Promise<Font[]> | undefined;

function loadFonts(url: URL): Promise<Font[]> {
  fontsPromise ??= (async () => {
    const sets = [
      { name: "DM Sans", cssVariable: "--font-dm-sans" },
      { name: "Noto Sans KR", cssVariable: "--font-noto-sans-kr" },
    ] as const;
    const fonts: Promise<Font>[] = [];
    for (const { name, cssVariable } of sets) {
      for (const weight of [400, 700] as const) {
        const path = getFontPathByWeight(fontData[cssVariable], weight);
        if (path === undefined) {
          throw new Error(`Cannot find the ${name} ${weight} font path.`);
        }
        fonts.push(
          fetch(experimental_getFontFileURL(path, url))
            .then(res => res.arrayBuffer())
            .then(data => ({ name, data, weight, style: "normal" }))
        );
      }
    }
    return Promise.all(fonts);
  })();
  return fontsPromise;
}

const svgUri = (svg: string) =>
  `data:image/svg+xml;base64,${Buffer.from(svg).toString("base64")}`;

const BRAND_MARK = svgUri(
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="none"><path d="M7 22 15 9l10 6-10 7Z" stroke="${SAGE}" stroke-opacity=".45" stroke-width="1.4"/><circle cx="7" cy="22" r="3" fill="${SAGE}"/><circle cx="15" cy="9" r="3.6" fill="${SAGE}"/><circle cx="25" cy="15" r="2.6" fill="${SAGE}"/><circle cx="15" cy="22" r="1.8" fill="${SAGE}" fill-opacity=".6"/></svg>`
);

const topicColor = new Map(TOPICS.map(t => [t.id, t.color]));

/** 지식 지도를 오른쪽에 깐다. focus가 있으면 그 글과 이웃만 밝힌다. */
function graphLayer(
  graph: KnowledgeGraph,
  box: { x: number; y: number; w: number; h: number },
  focus?: string
) {
  const pos = new Map(
    graph.nodes.map(n => [
      n.id,
      { x: box.x + n.x * box.w, y: box.y + n.y * box.h },
    ])
  );
  const center = focus ? graph.nodes.find(n => n.id === focus) : undefined;
  const near = new Set(center ? [...center.out, ...center.in] : []);
  const parts: string[] = [];

  for (const e of graph.edges) {
    const a = pos.get(e.source)!;
    const b = pos.get(e.target)!;
    const hot = center && (e.source === center.id || e.target === center.id);
    const color = hot ? topicColor.get(center.topic) : SAGE;
    const opacity = hot ? 0.7 : center ? 0.09 : 0.2;
    parts.push(
      `<line x1="${a.x.toFixed(1)}" y1="${a.y.toFixed(1)}" x2="${b.x.toFixed(1)}" y2="${b.y.toFixed(1)}" stroke="${color}" stroke-opacity="${opacity}" stroke-width="${hot ? 2 : 1.2}"/>`
    );
  }

  for (const n of graph.nodes) {
    if (n.id === center?.id) continue;
    const p = pos.get(n.id)!;
    const r = 3 + Math.sqrt(n.degree) * 1.7;
    const opacity = !center ? 0.85 : near.has(n.id) ? 0.85 : 0.26;
    parts.push(
      `<circle cx="${p.x.toFixed(1)}" cy="${p.y.toFixed(1)}" r="${r.toFixed(1)}" fill="${topicColor.get(n.topic)}" fill-opacity="${opacity}"/>`
    );
  }

  if (center) {
    const p = pos.get(center.id)!;
    const color = topicColor.get(center.topic);
    const r = 8 + Math.sqrt(center.degree) * 1.7;
    parts.push(
      `<circle cx="${p.x}" cy="${p.y}" r="${r + 26}" fill="${color}" fill-opacity="0.08"/>`,
      `<circle cx="${p.x}" cy="${p.y}" r="${r + 10}" fill="none" stroke="${FG}" stroke-opacity="0.55" stroke-width="1.5"/>`,
      `<circle cx="${p.x}" cy="${p.y}" r="${r}" fill="${color}"/>`
    );
  }

  return svgUri(
    `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">${parts.join("")}</svg>`
  );
}

type Node = {
  type: string;
  props: { style?: Record<string, unknown>; children?: unknown; src?: string };
};

const el = (
  type: string,
  style: Record<string, unknown>,
  children?: unknown
): Node => ({ type, props: { style, children } });

const img = (src: string, style: Record<string, unknown>): Node => ({
  type: "img",
  props: { src, style },
});

/** 한글은 한 글자 폭, 라틴 문자는 0.56 정도로 어림한다. */
function textUnits(text: string) {
  let units = 0;
  for (const ch of text) units += /[ᄀ-ᇿ㄰-㆏가-힯]/.test(ch) ? 1 : 0.56;
  return units;
}

function titleSize(text: string, width: number, lines: number) {
  for (const size of [66, 60, 54, 48, 44]) {
    if (textUnits(text) * size <= width * lines * 0.86) return size;
  }
  return 40;
}

/**
 * 띄어쓰기 단위로만 줄을 바꾼다. satori의 keep-all은 "할까?"의 물음표까지
 * 따로 떼어 다음 줄로 넘기기 때문에 단어를 직접 나눠 감싼다.
 */
function words(
  text: string,
  lines: number,
  style: { fontSize: number; lineHeight: number } & Record<string, unknown>
) {
  const gap = Math.round(style.fontSize * 0.26);
  return el(
    "div",
    {
      ...style,
      display: "flex",
      flexWrap: "wrap",
      marginRight: -gap,
      maxHeight: Math.ceil(style.fontSize * style.lineHeight * lines) + 2,
      overflow: "hidden",
    },
    text.split(/\s+/).map(w => el("span", { marginRight: gap }, w))
  );
}

function frame(graphSrc: string, fadeTo: number, children: Node[]) {
  return el(
    "div",
    {
      width: "100%",
      height: "100%",
      display: "flex",
      flexDirection: "column",
      position: "relative",
      background: BG,
      color: FG,
      fontFamily: "DM Sans",
      padding: "60px 72px 52px",
    },
    [
      img(graphSrc, {
        position: "absolute",
        top: 0,
        left: 0,
        width: W,
        height: H,
      }),
      // 글자 쪽(왼쪽)은 지도를 덮어 읽기 쉽게 한다.
      el("div", {
        position: "absolute",
        top: 0,
        left: 0,
        width: W,
        height: H,
        backgroundImage: `linear-gradient(90deg, ${BG} 0%, ${BG} ${fadeTo - 16}%, rgba(21,44,48,0) ${fadeTo}%)`,
      }),
      el("div", { display: "flex", alignItems: "center", gap: 14 }, [
        img(BRAND_MARK, { width: 34, height: 34 }),
        el(
          "span",
          { fontSize: 28, fontWeight: 700, letterSpacing: "-0.03em" },
          config.site.title
        ),
        el("span", {
          width: 1,
          height: 22,
          background: LINE,
          marginLeft: 6,
          marginRight: 6,
        }),
        el(
          "span",
          {
            fontSize: 17,
            letterSpacing: "0.16em",
            color: MUTED,
            textTransform: "uppercase",
          },
          "Research Notes"
        ),
      ]),
      ...children,
    ]
  );
}

function footer(left: string, right: string) {
  return el(
    "div",
    {
      display: "flex",
      justifyContent: "space-between",
      alignItems: "center",
      borderTop: `1px solid ${LINE}`,
      paddingTop: 22,
      fontSize: 22,
      color: MUTED,
    },
    [el("span", {}, left), el("span", {}, right)]
  );
}

async function toPng(tree: Node, url: URL) {
  const svg = await satori(tree as Parameters<typeof satori>[0], {
    width: W,
    height: H,
    fonts: await loadFonts(url),
  });
  return sharp(Buffer.from(svg)).png().toBuffer();
}

export async function renderSiteOgImage(graph: KnowledgeGraph, url: URL) {
  const posts = graph.nodes.length;
  const tree = frame(graphLayer(graph, { x: 640, y: 70, w: 500, h: 470 }), 66, [
    el(
      "div",
      {
        display: "flex",
        flexDirection: "column",
        marginTop: "auto",
        maxWidth: 640,
      },
      [
        el(
          "div",
          {
            fontSize: 82,
            fontWeight: 700,
            lineHeight: 1.04,
            letterSpacing: "-0.04em",
          },
          "Notes from fintech and AI."
        ),
        el(
          "div",
          {
            fontSize: 28,
            lineHeight: 1.45,
            color: MUTED,
            marginTop: 26,
            maxWidth: 580,
          },
          "Things I run into working in fintech, and notes from studying AI on the side."
        ),
      ]
    ),
    el("div", { display: "flex", flexDirection: "column", marginTop: 48 }, [
      footer(
        new URL(config.site.url).hostname.replace(/^www\./, ""),
        `${posts} posts on the map`
      ),
    ]),
  ]);
  return toPng(tree, url);
}

export async function renderPostOgImage(
  post: { id: string; title: string; tags: string[]; pubDatetime: Date },
  graph: KnowledgeGraph,
  lang: GraphLang,
  url: URL
) {
  const topic = topicOf(post.tags);

  // "[FDS] 제목: 부제" → 꼬리표 FDS, 제목, 부제
  let title = post.title.trim();
  let label = "";
  const tag = title.match(/^\[([^\]]+)\]\s*/);
  if (tag) {
    label = tag[1];
    title = title.slice(tag[0].length);
  }
  let subtitle = "";
  const colon = title.search(/[:：]\s/);
  if (colon > 0) {
    subtitle = title.slice(colon + 1).trim();
    title = title.slice(0, colon).trim();
  }

  const date =
    lang === "ko"
      ? new Intl.DateTimeFormat("sv-SE", { timeZone: config.site.timezone })
          .format(post.pubDatetime)
          .replaceAll("-", ".")
      : new Intl.DateTimeFormat("en-GB", {
          timeZone: config.site.timezone,
          year: "numeric",
          month: "short",
          day: "numeric",
        }).format(post.pubDatetime);

  const eyebrow =
    label && label.toLowerCase() !== topic.eyebrow.toLowerCase()
      ? `${topic.eyebrow} · ${label}`
      : topic.eyebrow;

  // 제목은 왼쪽 700px 안에, 지도는 그 오른쪽에 두어 강조한 점이 가려지지 않게 한다.
  const size = titleSize(title, 700, subtitle ? 2 : 3);
  const tree = frame(
    graphLayer(graph, { x: 800, y: 80, w: 350, h: 430 }, post.id),
    66,
    [
      el(
        "div",
        {
          display: "flex",
          flexDirection: "column",
          marginTop: "auto",
          maxWidth: 710,
        },
        [
          el(
            "div",
            {
              display: "flex",
              alignItems: "center",
              gap: 12,
              fontSize: 19,
              letterSpacing: "0.16em",
              textTransform: "uppercase",
              color: SAGE,
              marginBottom: 22,
            },
            [
              el("span", {
                width: 10,
                height: 10,
                borderRadius: 5,
                background: topic.color,
              }),
              el("span", {}, eyebrow),
            ]
          ),
          words(title, subtitle ? 2 : 3, {
            fontSize: size,
            fontWeight: 700,
            lineHeight: 1.2,
            letterSpacing: lang === "ko" ? "-0.02em" : "-0.03em",
          }),
          subtitle
            ? words(subtitle, 2, {
                fontSize: 29,
                lineHeight: 1.4,
                color: MUTED,
                marginTop: 20,
              })
            : el("div", {}),
        ]
      ),
      el("div", { display: "flex", flexDirection: "column", marginTop: 40 }, [
        footer(new URL(config.site.url).hostname.replace(/^www\./, ""), date),
      ]),
    ]
  );
  return toPng(tree, url);
}
