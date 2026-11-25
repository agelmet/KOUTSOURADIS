/* gk-trial.mjs — on the DRAFT only (drafts.advonmedia.com): shows the edits saved by the panel's trial mode in this browser.
   On the live site the server applies the edits itself, so this file is never loaded there. */
import { applyDom, renderArticle, visibleArticles, pageIdFromPath } from "./gk-core.mjs";
let c = null; try { c = JSON.parse(localStorage.getItem("gk-trial") || "null"); } catch {}
if (c) {
  const pid = pageIdFromPath(location.pathname);
  if (pid === "arthro-neo") {
    const slug = new URLSearchParams(location.search).get("a");
    const a = visibleArticles(c).find((x) => x.slug === slug);
    if (a) { const tpl = await (await fetch(location.pathname, { cache: "no-store" })).text(); const out = renderArticle(tpl, a, false).replace(/<script id="gk-boot">[\s\S]*?<\/script>/, "");
      D(out); }
  } else applyDom(document, pid, c, false);
  if (!document.querySelector(".gk-trial-n")) {
    const n = document.createElement("div"); n.className = "gk-trial-n";
    n.style.cssText = "position:fixed;left:10px;bottom:10px;z-index:2147483000;background:#fff3cd;color:#5b4300;font:500 12px system-ui,sans-serif;padding:6px 10px;border-radius:10px;box-shadow:0 4px 14px rgba(0,0,0,.15)";
    n.textContent = "Δοκιμή πίνακα: βλέπετε τις αλλαγές αυτής της συσκευής"; document.body.appendChild(n);
  }
}
function D(html) { document.open(); document.write(html); document.close(); }
