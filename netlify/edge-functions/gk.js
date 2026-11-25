/* Applies the client's published edits to every page before it is sent (Google, AI and visitors all see the edited text).
   New articles are served at /arthro/<slug> from the arthro-neo.html template; the sitemap lists them too. */
import { getStore } from "@netlify/blobs";
import { applyPage, renderArticle, sitemapAdd, visibleArticles, pageIdFromPath } from "../../assets/js/gk-core.mjs";
async function load() {
  try { const t = await getStore({ name: "gk-content", consistency: "strong" }).get("content.json"); return t ? JSON.parse(t) : null; }
  catch { return null; }
}
const html = (body, res) => { const h = new Headers(res.headers); h.delete("content-length"); h.set("content-type", "text/html; charset=utf-8"); return new Response(body, { status: res.status, headers: h }); };
export default async (req, context) => {
  const url = new URL(req.url); const path = url.pathname;
  const m = path.match(/^\/arthro\/([a-z0-9-]{1,80})\/?$/);
  if (m) {
    const c = await load(); const a = c && visibleArticles(c).find((x) => x.slug === m[1]);
    if (!a) return; // falls through to the normal 404 page
    const tr = await fetch(new URL("/arthro-neo.html", url), { headers: { "x-gk-inner": "1" } });
    if (!tr.ok) return;
    let out = renderArticle(await tr.text(), a, true);
    out = applyPage(out, "arthro-" + a.slug, c);
    return new Response(out, { headers: { "content-type": "text/html; charset=utf-8", "cache-control": "public, max-age=0, must-revalidate" } });
  }
  if (req.headers.get("x-gk-inner")) return;
  if (path === "/sitemap.xml") {
    const res = await context.next(); const c = await load(); if (!c) return res;
    const h = new Headers(res.headers); h.delete("content-length");
    return new Response(sitemapAdd(await res.text(), c), { status: res.status, headers: h });
  }
  const res = await context.next();
  if (!(res.headers.get("content-type") || "").includes("text/html")) return res;
  const c = await load(); if (!c) return res;
  return html(applyPage(await res.text(), pageIdFromPath(path), c), res);
};
export const config = { path: "/*", excludedPath: ["/api/*", "/assets/*", "/admin.html", "/admin", "/odigos-panel/*", "/favicon.ico", "/*.webp", "/*.png", "/*.jpg", "/*.svg", "/*.woff2", "/*.js", "/*.mjs", "/*.css", "/*.txt", "/*.webmanifest"] };
