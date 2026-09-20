import type { Context } from "@netlify/functions";
import { createHmac, timingSafeEqual } from "node:crypto";

declare const Netlify: { env: { get(key: string): string | undefined } };

const COOKIE_NAME = "zn_session";
const SESSION_MS = 30 * 24 * 60 * 60 * 1000; // 30 days

function json(body: unknown, status = 200, extraHeaders: Record<string, string> = {}): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json", ...extraHeaders }
  });
}

function sign(secret: string, message: string): string {
  return createHmac("sha256", secret).update(message).digest("hex");
}

function safeEqual(a: string, b: string): boolean {
  const bufA = Buffer.from(a, "utf8");
  const bufB = Buffer.from(b, "utf8");
  if (bufA.length !== bufB.length) return false;
  return timingSafeEqual(bufA, bufB);
}

export default async (req: Request, _context: Context) => {
  if (req.method !== "POST") {
    return json({ error: "Method not allowed" }, 405);
  }

  const secret = Netlify.env.get("SESSION_SECRET");
  const expected = Netlify.env.get("PORTAL_PASSWORD");
  if (!secret || !expected) {
    return json({ error: "Portal is not configured yet. Set SESSION_SECRET and PORTAL_PASSWORD." }, 500);
  }

  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return json({ error: "Invalid request" }, 400);
  }

  const password = typeof (body as { password?: unknown })?.password === "string"
    ? (body as { password: string }).password
    : "";

  if (!password || !safeEqual(password, expected)) {
    return json({ error: "Incorrect password" }, 401);
  }

  const expiry = Date.now() + SESSION_MS;
  const sig = sign(secret, String(expiry));
  const cookieValue = `${expiry}.${sig}`;

  return json({ ok: true }, 200, {
    "Set-Cookie": `${COOKIE_NAME}=${cookieValue}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${Math.floor(SESSION_MS / 1000)}`
  });
};
