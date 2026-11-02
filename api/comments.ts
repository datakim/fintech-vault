/*
 * GET  /api/comments?thread=<slug>  공개된 댓글 목록
 * POST /api/comments                새 댓글 (바로 공개된다. 관리 비밀번호가 있으면 글쓴이 답글로 표시)
 */
import { db, ipHash, isAdmin, json, sameSite, THREAD_RE } from "./_lib";

export const config = { runtime: "edge" };

const MIN_FILL_MS = 3000; // 페이지를 연 지 3초 안에 보낸 글은 봇으로 본다
const MAX_FILL_MS = 1000 * 60 * 60 * 24;
const RATE_MAX = 3; // 같은 IP에서 10분에 3개까지

export default async function handler(req: Request): Promise<Response> {
  const d = db();
  if (!d) return json({ error: "not_configured" }, 503);
  await d.ready;
  const { sql } = d;

  if (req.method === "GET") {
    const thread = new URL(req.url).searchParams.get("thread") ?? "";
    if (!THREAD_RE.test(thread)) return json({ error: "bad_thread" }, 400);
    const rows = await sql`
      SELECT id, name, body, is_author, created_at
      FROM comments
      WHERE thread = ${thread} AND status = 'approved'
      ORDER BY created_at ASC
      LIMIT 500`;
    return json({ comments: rows }, 200, {
      "cache-control": "public, max-age=0, s-maxage=20, stale-while-revalidate=120",
    });
  }

  if (req.method !== "POST") return json({ error: "method" }, 405);
  if (!sameSite(req)) return json({ error: "origin" }, 403);
  if (Number(req.headers.get("content-length") ?? 0) > 12_000) {
    return json({ error: "too_large" }, 413);
  }

  let input: Record<string, unknown>;
  try {
    input = await req.json();
  } catch {
    return json({ error: "bad_json" }, 400);
  }
  const str = (v: unknown) => (typeof v === "string" ? v : "");
  const thread = str(input.thread);
  const name = str(input.name).replace(/\s+/g, " ").trim();
  const body = str(input.body).replace(/\r\n/g, "\n").trim();
  const lang = str(input.lang) === "en" ? "en" : "ko";
  const admin = isAdmin(req);

  if (!THREAD_RE.test(thread)) return json({ error: "bad_thread" }, 400);
  if (name.length < 1 || name.length > 30) return json({ error: "bad_name" }, 400);
  if (body.length < 2 || body.length > 2000) return json({ error: "bad_body" }, 400);

  if (!admin) {
    // 사람에게는 보이지 않는 칸을 채웠거나 너무 빨리 보냈으면 받은 척만 한다.
    const elapsed = Date.now() - Number(input.t ?? 0);
    if (str(input.website) || elapsed < MIN_FILL_MS) return json({ ok: true });
    if (!(elapsed < MAX_FILL_MS)) return json({ error: "stale" }, 400);
    if ((body.match(/https?:\/\//g) ?? []).length > 2) return json({ error: "too_many_links" }, 400);
  }

  const hash = await ipHash(req);
  if (!admin && hash) {
    const [{ n }] = await sql`
      SELECT count(*)::int AS n FROM comments
      WHERE ip_hash = ${hash}
        AND created_at > now() - interval '10 minutes'`;
    if (n >= RATE_MAX) return json({ error: "rate_limited" }, 429);
  }

  await sql`
    INSERT INTO comments (thread, name, body, lang, status, is_author, ip_hash)
    VALUES (${thread}, ${name}, ${body}, ${lang},
            'approved', ${admin}, ${hash})`;
  return json({ ok: true });
}
