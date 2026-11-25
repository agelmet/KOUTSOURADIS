/* GET /api/content — the edits published from the panel ({} until the first publish). */
import { content } from "./_lib.mjs";
export default async () => {
  let t = null; try { t = await content().get("content.json"); } catch {}
  return new Response(t || "{}", { headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
};
export const config = { path: "/api/content" };
