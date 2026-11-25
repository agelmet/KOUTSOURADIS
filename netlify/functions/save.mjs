/* POST /api/save {pass, action:"login"}               -> {ok}
   POST /api/save {pass, action:"publish", content}    -> {ok, when}   (whole edits document)
   POST /api/save {pass, action:"undo"}                -> {ok, when}   (back to the previous publish)
   Netlify Blobs only — no Git commit, no deploy, 0 credits. Previous version kept + one dated copy per day. */
import { content, json, checkPass } from "./_lib.mjs";
import { clean } from "../../assets/js/gk-core.mjs";
function sanitize(c) {
  const out = { v: 1, pages: {}, contact: {}, articles: [] };
  for (const [pid, p] of Object.entries(c.pages || {})) {
    if (!/^[\w*-]{1,80}$/.test(pid) || !p || typeof p !== "object") continue;
    const q = { t: {}, i: {}, l: {} };
    for (const [k, v] of Object.entries(p.t || {})) if (/^[\w-]{1,40}$/.test(k)) q.t[k] = clean(String(v)).slice(0, 20000);
    for (const [k, v] of Object.entries(p.l || {})) if (/^[\w-]{1,40}$/.test(k)) q.l[k] = clean(String(v)).slice(0, 200000);
    for (const [k, v] of Object.entries(p.i || {})) if (/^[\w-]{1,40}$/.test(k) && v && typeof v === "object") {
      const src = String(v.src || ""); if (src && !/^(\/api\/img\/[\w.-]+|assets\/[\w./-]+|\/assets\/[\w./-]+)$/.test(src)) continue;
      q.i[k] = { src, alt: String(v.alt ?? "").slice(0, 300), w: +v.w || 0, h: +v.h || 0 };
    }
    out.pages[pid] = q;
  }
  const ct = c.contact || {};
  out.contact = { phone: String(ct.phone || "").replace(/[^\d+ ]/g, "").slice(0, 20), email: String(ct.email || "").replace(/[<>"'\s]/g, "").slice(0, 120) };
  for (const a of (c.articles || []).slice(0, 300)) {
    if (!a || !a.title || !/^[a-z0-9-]{1,80}$/.test(a.slug || "")) continue;
    const img = String(a.img || ""); 
    out.articles.push({ id: String(a.id || a.slug).slice(0, 40), slug: a.slug, title: String(a.title).slice(0, 200), sub: String(a.sub || "").slice(0, 300),
      tag: String(a.tag || "").slice(0, 80), quote: String(a.quote || "").slice(0, 200), date: String(a.date || "").slice(0, 10),
      updated: new Date().toISOString(), body: clean(String(a.body || "")).slice(0, 200000),
      img: /^(\/api\/img\/[\w.-]+)?$/.test(img) ? img : "", alt: String(a.alt || "").slice(0, 300), hidden: !!a.hidden });
  }
  return out;
}
export default async (req) => {
  if (req.method !== "POST") return json({ ok: false, error: "method" }, 405);
  let b; try { b = await req.json(); } catch { return json({ ok: false, error: "json" }, 400); }
  if (!(await checkPass(b.pass))) return json({ ok: false, error: "pass" }, 401);
  if (b.action === "login") return json({ ok: true });
  const st = content();
  if (b.action === "undo") {
    const prev = await st.get("content-prev.json");
    if (!prev) return json({ ok: false, error: "nothing" }, 404);
    const cur = await st.get("content.json"); await st.set("content.json", prev); if (cur) await st.set("content-prev.json", cur);
    return json({ ok: true, when: new Date().toISOString() });
  }
  if (b.action !== "publish" || !b.content || typeof b.content !== "object") return json({ ok: false, error: "action" }, 400);
  const c = sanitize(b.content); c.updated = new Date().toISOString();
  const text = JSON.stringify(c);
  if (text.length > 3_000_000) return json({ ok: false, error: "too big" }, 413);
  try {
    const prev = await st.get("content.json");
    if (prev) { await st.set("content-prev.json", prev); await st.set("history/" + c.updated.slice(0, 10) + ".json", prev); }
    await st.set("content.json", text);
  } catch { return json({ ok: false, error: "store" }, 500); }
  return json({ ok: true, when: c.updated });
};
export const config = { path: "/api/save" };
