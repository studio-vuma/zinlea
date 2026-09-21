import type { Context } from "@netlify/functions";
import { createHmac, timingSafeEqual } from "node:crypto";

const COOKIE_NAME = "zn_session";
const SESSION_MS = 30 * 24 * 60 * 60 * 1000; // 30 days

interface PortalUser {
  username: string;
  name: string;
  password: string;
}

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

function loadUsers(): PortalUser[] {
  const raw = process.env.PORTAL_USERS;
  if (!raw) return [];
  try {
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed.filter((u): u is PortalUser =>
      typeof u?.username === "string" && typeof u?.name === "string" && typeof u?.password === "string"
    );
  } catch {
    return [];
  }
}

export default async (req: Request, _context: Context) => {
  if (req.method !== "POST") {
    return json({ error: "Method not allowed" }, 405);
  }

  const secret = process.env.SESSION_SECRET;
  const users = loadUsers();
  if (!secret || users.length === 0) {
    return json({ error: "Portal is not configured yet. Set SESSION_SECRET and PORTAL_USERS." }, 500);
  }

  let body: unknown;
  try {
    body = await req.json();
  } catch {
    return json({ error: "Invalid request" }, 400);
  }

  const username = typeof (body as { username?: unknown })?.username === "string"
    ? (body as { username: string }).username
    : "";
  const password = typeof (body as { password?: unknown })?.password === "string"
    ? (body as { password: string }).password
    : "";

  const user = users.find(u => u.username === username);
  if (!username || !password || !user || !safeEqual(password, user.password)) {
    return json({ error: "Incorrect name or passcode" }, 401);
  }

  const expiry = Date.now() + SESSION_MS;
  const payload = `${expiry}.${user.username}`;
  const sig = sign(secret, payload);
  const cookieValue = `${payload}.${sig}`;

  return json({ ok: true, name: user.name }, 200, {
    "Set-Cookie": `${COOKIE_NAME}=${cookieValue}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=${Math.floor(SESSION_MS / 1000)}`
  });
};
