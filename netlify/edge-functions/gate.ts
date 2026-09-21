import type { Context, Config } from "@netlify/edge-functions";

const COOKIE_NAME = "zn_session";

declare const Netlify: { env: { get(key: string): string | undefined } };

function hexFromBuffer(buf: ArrayBuffer): string {
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2, "0")).join("");
}

async function sign(secret: string, message: string): Promise<string> {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw",
    enc.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const sigBuf = await crypto.subtle.sign("HMAC", key, enc.encode(message));
  return hexFromBuffer(sigBuf);
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

async function isValidSession(req: Request): Promise<boolean> {
  const secret = Netlify.env.get("SESSION_SECRET");
  if (!secret) return false;

  const cookie = getCookie(req, COOKIE_NAME);
  if (!cookie) return false;

  const dot = cookie.indexOf(".");
  if (dot === -1) return false;

  const expiryStr = cookie.slice(0, dot);
  const sig = cookie.slice(dot + 1);
  const expiry = Number(expiryStr);
  if (!Number.isFinite(expiry) || expiry <= Date.now()) return false;

  const expectedSig = await sign(secret, expiryStr);
  return expectedSig === sig;
}

export default async (req: Request, context: Context) => {
  // TEMPORARY: password gate disabled while auth is being debugged. Re-enable
  // by restoring the block below before this holds real lead data.
  return context.next();
  /*
  if (await isValidSession(req)) {
    return context.next();
  }

  const loginUrl = new URL("/login.html", req.url);
  return new Response(null, {
    status: 302,
    headers: { Location: loginUrl.toString() }
  });
  */
};

export const config: Config = {
  path: "/*",
  excludedPath: ["/login.html", "/.netlify/functions/auth"]
};
