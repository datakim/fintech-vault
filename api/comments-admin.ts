/*
 * 댓글 관리 (Authorization: Bearer <COMMENTS_ADMIN_TOKEN>)
 * GET  /api/comments-admin                       승인 대기 + 최근 공개 댓글
 * POST /api/comments-admin {action, id}          action: approve | delete
 */
import { db, isAdmin, json, sameSite } from "./_lib";

export const config = { runtime: "edge" };

export default async function handler(req: Request): Promise<Response> {
  const d = db();
  if (!d) return json({ error: "not_configured" }, 503);
  if (!isAdmin(req)) return json({ error: "unauthorized" }, 401);
  await d.ready;
  const { sql } = d;
  const noStore = { "cache-control": "no-store" };

  if (req.method === "GET") {
    const pending = await sql`
      SELECT id, thread, name, body, lang, is_author, created_at
      FROM comments WHERE status = 'pending'
      ORDER BY created_at ASC LIMIT 200`;
    const recent = await sql`
      SELECT id, thread, name, body, lang, is_author, created_at
      FROM comments WHERE status = 'approved'
      ORDER BY created_at DESC LIMIT 50`;
    return json({ pending, recent }, 200, noStore);
  }

  if (req.method !== "POST") return json({ error: "method" }, 405);
  if (!sameSite(req)) return json({ error: "origin" }, 403);
  let input: Record<string, unknown>;
  try {
    input = await req.json();
  } catch {
    return json({ error: "bad_json" }, 400);
  }
  const id = Number(input.id);
  if (!Number.isInteger(id) || id <= 0) return json({ error: "bad_id" }, 400);

  if (input.action === "approve") {
    await sql`UPDATE comments SET status = 'approved' WHERE id = ${id}`;
  } else if (input.action === "delete") {
    await sql`DELETE FROM comments WHERE id = ${id}`;
  } else {
    return json({ error: "bad_action" }, 400);
  }
  return json({ ok: true }, 200, noStore);
}
