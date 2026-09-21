import type { Context } from "@netlify/functions";

export default async (_req: Request, _context: Context) => {
  const secret = process.env.SESSION_SECRET;
  const password = process.env.PORTAL_PASSWORD;

  const canary = process.env.DEBUG_CANARY;

  return new Response(JSON.stringify({
    hasSessionSecret: !!secret,
    sessionSecretLength: secret ? secret.length : 0,
    hasPortalPassword: !!password,
    portalPasswordLength: password ? password.length : 0,
    canaryValue: canary || null,
    nodeVersion: process.version,
    deployId: process.env.DEPLOY_ID || null,
    context: process.env.CONTEXT || null,
    totalEnvVarCount: Object.keys(process.env).length
  }), {
    headers: { "Content-Type": "application/json" }
  });
};
