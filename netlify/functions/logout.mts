import type { Context } from "@netlify/functions";

export default async (req: Request, _context: Context) => {
  const loginUrl = new URL("/portal/login.html", req.url);
  return new Response(null, {
    status: 302,
    headers: {
      Location: loginUrl.toString(),
      "Set-Cookie": "zn_session=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0"
    }
  });
};
