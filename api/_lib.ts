/*
 * 댓글 API 공통 (2026-11-03)
 * Vercel Edge 함수에서 Neon Postgres를 HTTP로 쓴다. 파일 이름이 _로 시작해서 경로로는 열리지 않는다.
 * 필요한 환경 변수: DATABASE_URL(Neon 연결 시 자동), COMMENTS_ADMIN_TOKEN(관리 비밀번호).
 */
import { neon } from "@neondatabase/serverless";

declare const process: { env: Record<string, string | undefined> };

export const env = (key: string) => process.env[key];

let ready: Promise<unknown> | undefined;

export function db() {
  const url = env("DATABASE_URL") ?? env("POSTGRES_URL");
  if (!url) return undefined;
  const sql = neon(url);
  // 처음 부를 때 한 번 테이블을 만든다.
  ready ??= (async () => {
    await sql`CREATE TABLE IF NOT EXISTS comments (
      id BIGSERIAL PRIMARY KEY,
      thread TEXT NOT NULL,
      name TEXT NOT NULL,
      body TEXT NOT NULL,
      lang TEXT,
      status TEXT NOT NULL DEFAULT 'pending',
      is_author BOOLEAN NOT NULL DEFAULT false,
      ip_hash TEXT,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )`;
    await sql`CREATE INDEX IF NOT EXISTS comments_thread_idx
      ON comments (thread, status, created_at)`;
  })();
  return { sql, ready };
}

export const json = (data: unknown, status = 200, headers: HeadersInit = {}) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", ...headers },
  });

/** 관리 비밀번호가 맞는지 본다. 설정이 없으면 언제나 false. */
export function isAdmin(req: Request) {
  const token = env("COMMENTS_ADMIN_TOKEN");
  const got = (req.headers.get("authorization") ?? "").replace(/^Bearer\s+/i, "");
  if (!token || got.length !== token.length) return false;
  let diff = 0;
  for (let i = 0; i < token.length; i++) diff |= token.charCodeAt(i) ^ got.charCodeAt(i);
  return diff === 0;
}

/** 원래 IP를 알 수 없게 소금을 쳐서 해시한다. 도배 막기에만 쓴다. */
export async function ipHash(req: Request) {
  const ip =
    req.headers.get("x-real-ip") ??
    (req.headers.get("x-forwarded-for") ?? "").split(",")[0].trim();
  if (!ip) return null;
  const salt = env("COMMENTS_SALT") ?? env("COMMENTS_ADMIN_TOKEN") ?? "fal";
  const buf = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(`${salt}:${ip}`)
  );
  return Array.from(new Uint8Array(buf).slice(0, 16), b =>
    b.toString(16).padStart(2, "0")
  ).join("");
}

export const THREAD_RE = /^[a-z0-9][a-z0-9-]{0,119}$/;

/** 이 사이트에서 온 요청만 받는다(다른 사이트가 대신 글을 올리지 못하게). */
export function sameSite(req: Request) {
  const origin = req.headers.get("origin");
  if (!origin) return true;
  try {
    const host = new URL(origin).hostname;
    return (
      host === "www.financialailab.com" ||
      host === "financialailab.com" ||
      host === "fintech-vault.vercel.app" ||
      host.endsWith("-fintech-vault.vercel.app") ||
      host === "localhost"
    );
  } catch {
    return false;
  }
}
