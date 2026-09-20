import type { Context } from "@netlify/functions";
import { getStore } from "@netlify/blobs";

const RECORDS_KEY = "records";
const MAX_BODY_BYTES = 2 * 1024 * 1024; // 2MB safety cap

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" }
  });
}

export default async (req: Request, _context: Context) => {
  const store = getStore("zinlea-crm");

  if (req.method === "GET") {
    const records = await store.get(RECORDS_KEY, { type: "json" });
    return json(Array.isArray(records) ? records : []);
  }

  if (req.method === "PUT") {
    const raw = await req.text();
    if (raw.length > MAX_BODY_BYTES) {
      return json({ error: "Payload too large" }, 413);
    }

    let body: unknown;
    try {
      body = JSON.parse(raw);
    } catch {
      return json({ error: "Invalid JSON" }, 400);
    }

    if (!Array.isArray(body)) {
      return json({ error: "Expected an array of records" }, 400);
    }

    await store.setJSON(RECORDS_KEY, body);
    return json({ ok: true });
  }

  return json({ error: "Method not allowed" }, 405);
};
