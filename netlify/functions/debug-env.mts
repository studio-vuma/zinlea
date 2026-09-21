import type { Context } from "@netlify/functions";

export default async (_req: Request, _context: Context) => {
  const secret = process.env.SESSION_SECRET;
  const password = process.env.PORTAL_PASSWORD;

  return new Response(JSON.stringify({
    hasSessionSecret: !!secret,
    sessionSecretLength: secret ? secret.length : 0,
    hasPortalPassword: !!password,
    portalPasswordLength: password ? password.length : 0,
    nodeVersion: process.version,
    allEnvKeysContainingPORTAL: Object.keys(process.env).filter(k => k.includes("PORTAL") || k.includes("SESSION"))
  }), {
    headers: { "Content-Type": "application/json" }
  });
};
