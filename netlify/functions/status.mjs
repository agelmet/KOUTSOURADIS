/* GET /api/status — tells the panel it runs on the live site (not the draft). */
import { json } from "./_lib.mjs";
export default async () => json({ ok: true, live: true });
export const config = { path: "/api/status" };
