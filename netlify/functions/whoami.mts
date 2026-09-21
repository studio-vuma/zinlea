import type { Context } from "@netlify/functions";
import { createHmac } from "node:crypto";

const COOKIE_NAME = "zn_session";

interface PortalUser {
  username: string;
  name: string;
  password: string;
}

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" }
  });
}

function sign(secret: string, message: string): string {
  return createHmac("sha256", secret).update(message).digest("hex");
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

function getCookie(req: Request, name: string): string | null {
  const header = req.headers.get("cookie") || "";
  for (const part of header.split(";")) {
    const trimmed = part.trim();
    if (trimmed.startsWith(name + "=")) {
      return trimmed.slice(name.length + 1);
    }
  }
  return null;
}

export default async (req: Request, _context: Context) => {
  const secret = process.env.SESSION_SECRET;
  const cookie = getCookie(req, COOKIE_NAME);
  if (!secret || !cookie) {
    return json({ authenticated: false }, 401);
  }

  const firstDot = cookie.indexOf(".");
  const lastDot = cookie.lastIndexOf(".");
  if (firstDot === -1 || lastDot === -1 || firstDot === lastDot) {
    return json({ authenticated: false }, 401);
  }

  const expiryStr = cookie.slice(0, firstDot);
  const username = cookie.slice(firstDot + 1, lastDot);
  const sig = cookie.slice(lastDot + 1);
  const expiry = Number(expiryStr);
  if (!Number.isFinite(expiry) || expiry <= Date.now() || !username) {
    return json({ authenticated: false }, 401);
  }

  const expectedSig = sign(secret, `${expiryStr}.${username}`);
  if (expectedSig !== sig) {
    return json({ authenticated: false }, 401);
  }

  const user = loadUsers().find(u => u.username === username);
  if (!user) {
    return json({ authenticated: false }, 401);
  }

  return json({ authenticated: true, username: user.username, name: user.name });
};
