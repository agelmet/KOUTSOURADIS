/* gk-core.mjs — Advon in-page editor, shared core.
   Used by: the live edge function (applies the published edits to every page before it is sent, so Google and AI read them),
            the editor and the admin (draft trial mode, previews).
   Content shape (one JSON document):
   { v:1, updated,
     pages:   { "<page>": { t:{key:html}, i:{key:{src,alt,w,h}}, l:{key:html} }, "*": {...footer...} },
     contact: { phone, email },
     articles:[ { id, slug, title, sub, tag, quote, date, body, img, alt, hidden } ] } */

export const ORIG = { phone: "+30 698 588 0004", email: "gkoutsouradis.therapist@gmail.com" };
export const SITE = "https://gkoutsouradis.gr";
export const TPL_ARTICLE = "arthro-neo.html";

const esc = (s) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const reEsc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

/* Strip anything that could run code. Applied on save (server) and on paste (browser). */
export function clean(html) {
  return String(html ?? "")
    .replace(/<\s*(script|style|iframe|object|embed|form|textarea|select|noscript|template)\b[\s\S]*?<\/\s*\1\s*>/gi, "")
    .replace(/<\/?\s*(script|style|iframe|object|embed|link|meta|base|form|input|textarea|select|noscript|template)\b[^>]*>/gi, "")
    .replace(/\s(on\w+|srcdoc|formaction)\s*=\s*("[^"]*"|'[^']*'|[^\s>]+)/gi, "")
    .replace(/(href|src|xlink:href)\s*=\s*(["'])\s*(javascript|data(?!:image\/(png|jpe?g|webp|gif)))[^"']*\2/gi, '$1="#"');
}

export function slugify(t) {
  const map = { α:"a",ά:"a",β:"v",γ:"g",δ:"d",ε:"e",έ:"e",ζ:"z",η:"i",ή:"i",θ:"th",ι:"i",ί:"i",ϊ:"i",ΐ:"i",κ:"k",λ:"l",μ:"m",ν:"n",ξ:"x",ο:"o",ό:"o",π:"p",ρ:"r",σ:"s",ς:"s",τ:"t",υ:"y",ύ:"y",ϋ:"y",ΰ:"y",φ:"f",χ:"ch",ψ:"ps",ω:"o",ώ:"o" };
  return String(t || "").toLowerCase().replace(/ου/g, "ou").replace(/αυ/g, "av").replace(/ευ/g, "ev")
    .split("").map((c) => map[c] ?? c).join("").replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 70) || "arthro";
}

const telDigits = (p) => { let d = String(p || "").replace(/\D/g, ""); if (d.length === 10) d = "30" + d; return d; };
const telShow = (p) => { const d = telDigits(p); return d.length === 12 ? `+${d.slice(0, 2)} ${d.slice(2, 5)} ${d.slice(5, 8)} ${d.slice(8)}` : String(p); };

function applyContact(html, c) {
  const ct = (c && c.contact) || {};
  if (ct.phone && telDigits(ct.phone) !== telDigits(ORIG.phone)) {
    const od = telDigits(ORIG.phone), nd = telDigits(ct.phone), nshow = telShow(ct.phone);
    html = html.split(ORIG.phone).join(nshow)
      .split("+" + od).join("+" + nd)
      .split(od.slice(2).replace(/(\d{3})(\d{3})(\d{4})/, "$1 $2 $3")).join(nshow.slice(4))
      .split(od.slice(2)).join(nd.slice(2));
  }
  if (ct.email && ct.email.trim() && ct.email.trim() !== ORIG.email) html = html.split(ORIG.email).join(esc(ct.email.trim()));
  return html;
}

function applyImg(tag, v) {
  let t = tag.replace(/\s(srcset|sizes)="[^"]*"/g, "");
  if (v.src) { t = t.replace(/\ssrc="[^"]*"/, ` src="${esc(v.src)}"`); t = t.replace(/\sdata-lb="[^"]*"/, ` data-lb="${esc(v.src)}"`); }
  if (v.alt != null) t = t.replace(/\salt="[^"]*"/, ` alt="${esc(v.alt)}"`);
  if (v.w && v.h) { t = t.replace(/\swidth="\d+"/, ` width="${+v.w}"`).replace(/\sheight="\d+"/, ` height="${+v.h}"`); }
  return t;
}

/* The page edits, as text replacements between the markers that mark.py wrote. */
export function applyPage(html, pid, c) {
  if (!c || !c.pages) return applyContact(html, c);
  for (const id of [pid, "*"]) {
    const p = c.pages[id]; if (!p) continue;
    for (const [k, v] of Object.entries(p.l || {})) {
      html = html.replace(new RegExp(`<!--l:${reEsc(k)}-->[\\s\\S]*?<!--/l:${reEsc(k)}-->`), () => `<!--l:${k}-->${v}<!--/l:${k}-->`);
    }
    for (const [k, v] of Object.entries(p.t || {})) {
      html = html.replace(new RegExp(`<!--e:${reEsc(k)}-->[\\s\\S]*?<!--/e:${reEsc(k)}-->`, "g"), () => `<!--e:${k}-->${v}<!--/e:${k}-->`);
    }
    for (const [k, v] of Object.entries(p.i || {})) {
      html = html.replace(new RegExp(`<img\\b[^>]*\\sdata-ei="${reEsc(k)}"[^>]*>`, "g"), (tag) => applyImg(tag, v));
    }
  }
  if (pid === "arthra") html = applyArticleCards(html, c);
  return applyContact(html, c);
}

/* ---------- articles ---------- */
export const visibleArticles = (c) => ((c && c.articles) || []).filter((a) => !a.hidden && a.slug && a.title)
  .sort((a, b) => String(b.date || "").localeCompare(String(a.date || "")));
export const articleUrl = (a, live) => (live ? `/arthro/${a.slug}` : `${TPL_ARTICLE}?a=${encodeURIComponent(a.slug)}`);
const ICON_MK = '<svg class="mk arc-mk" viewBox="0 0 260 236" aria-hidden="true"><use href="#mk"/></svg>';
const ICON_GO = '<svg class="bi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path pathLength="1" d="M5 12h14M13 6l6 6-6 6"/></svg>';
export function plain(html) { return String(html || "").replace(/<[^>]+>/g, " ").replace(/&nbsp;/g, " ").replace(/\s+/g, " ").trim(); }
export function excerpt(a, n = 260) { const t = plain(a.body); return t.length > n ? t.slice(0, n).replace(/\s\S*$/, "") + "…" : t; }
const readMin = (a) => Math.max(2, Math.round(plain(a.body).split(" ").length / 200));
export function cardHtml(a, live) {
  const q = a.quote || a.sub || "";
  const art = a.img ? `<img class="arc-img" src="${esc(a.img)}" alt="${esc(a.alt || a.title)}" loading="lazy">` : `${ICON_MK}<span class="arc-q">${esc(q)}</span>`;
  const tag = [a.tag, `περίπου ${readMin(a)} λεπτά`].filter(Boolean).join(" · ");
  return `<a class="arc gk-arc" href="${articleUrl(a, live)}"><div class="arc-art${a.img ? " has-img" : ""}">${art}</div><div class="arc-t"><span class="tag">${esc(tag)}</span><h2>${esc(a.title)}</h2>${a.sub ? `<p class="arc-sub">${esc(a.sub)}</p>` : ""}<p>${esc(excerpt(a))}</p><span class="sc-go">Διαβάστε το άρθρο ${ICON_GO}</span></div></a>`;
}
export function applyArticleCards(html, c, live = true) {
  const list = visibleArticles(c); if (!list.length) return html;
  const cards = list.map((a) => cardHtml(a, live)).join("");
  return html.replace(/(<div class="wrap"[^>]*data-el="[\w-]+"[^>]*>\s*<!--l:[\w-]+-->)/, `$1${cards}`);
}
export function renderArticle(tpl, a, live = true) {
  const d = a.date ? new Date(a.date) : new Date();
  const dateGr = d.toLocaleDateString("el-GR", { day: "numeric", month: "long", year: "numeric" });
  const desc = a.sub ? `${a.sub}. ${excerpt(a, 120)}` : excerpt(a, 150);
  const url = `${SITE}/arthro/${a.slug}`;
  const img = a.img ? `<figure class="ar-fig"><img src="${esc(a.img)}" alt="${esc(a.alt || a.title)}" loading="eager"></figure>` : "";
  const ld = JSON.stringify({ "@context": "https://schema.org", "@type": "BlogPosting", headline: a.title, description: desc, datePublished: d.toISOString().slice(0, 10),
    dateModified: (a.updated || d.toISOString()).slice(0, 10), inLanguage: "el", url, mainEntityOfPage: url,
    author: { "@type": "Person", name: "Γιώργος Κουτσουραδής", url: SITE + "/poios-eimai" },
    publisher: { "@type": "Person", name: "Γιώργος Κουτσουραδής" }, image: a.img ? (a.img.startsWith("http") ? a.img : SITE + a.img) : undefined });
  const map = { TITLE: esc(a.title), TITLE_T: esc(a.title), DESC: esc(desc), URL: url, TAG: esc(a.tag || "Άρθρο"), SUB: esc(a.sub || ""),
    DATE: esc(dateGr), DATE_ISO: d.toISOString().slice(0, 10), IMG: img, BODY: a.body || "", LD: ld.replace(/</g, "\\u003c") };
  let out = tpl.replace(/\{\{(\w+)\}\}/g, (m, k) => (k in map ? map[k] : m));
  if (live) out = out.replace("<head>", '<head><base href="/">');
  if (!a.sub) out = out.replace(/<p class="display h-words[^"]*"[^>]*>\s*<\/p>/, "");
  return out;
}
export function sitemapAdd(xml, c) {
  const arts = visibleArticles(c); if (!arts.length) return xml;
  const add = arts.map((a) => `<url><loc>${SITE}/arthro/${a.slug}</loc><lastmod>${String(a.updated || a.date || "").slice(0, 10)}</lastmod></url>`).join("");
  return xml.replace("</urlset>", add + "</urlset>");
}

/* ---------- browser (draft trial + editor preview): same edits applied to the live DOM ---------- */
export function applyDom(doc, pid, c, live = false) {
  if (!c) return;
  for (const id of [pid, "*"]) {
    const p = c.pages && c.pages[id]; if (!p) continue;
    for (const [k, v] of Object.entries(p.l || {})) { const el = doc.querySelector(`[data-el="${k}"]`); if (el) el.innerHTML = `<!--l:${k}-->${v}<!--/l:${k}-->`; }
    for (const [k, v] of Object.entries(p.t || {})) doc.querySelectorAll(`[data-e="${k}"]`).forEach((el) => { el.innerHTML = `<!--e:${k}-->${v}<!--/e:${k}-->`; });
    for (const [k, v] of Object.entries(p.i || {})) doc.querySelectorAll(`img[data-ei="${k}"]`).forEach((el) => {
      el.removeAttribute("srcset"); el.removeAttribute("sizes"); if (v.src) { el.src = v.src; if (el.dataset.lb) el.dataset.lb = v.src; }
      if (v.alt != null) el.alt = v.alt; if (v.w && v.h) { el.width = v.w; el.height = v.h; } });
  }
  if (pid === "arthra" && c.articles) {
    const wrap = doc.querySelector(".ar-list [data-el]");
    if (wrap) { wrap.querySelectorAll(".gk-arc").forEach((n) => n.remove()); const t = doc.createElement("template"); t.innerHTML = visibleArticles(c).map((a) => cardHtml(a, live)).join(""); wrap.insertBefore(t.content, wrap.firstChild && wrap.firstChild.nextSibling); }
  }
  const ct = c.contact || {};
  if ((ct.phone && telDigits(ct.phone) !== telDigits(ORIG.phone)) || (ct.email && ct.email !== ORIG.email)) {
    const walker = doc.createTreeWalker(doc.body, NodeFilter.SHOW_TEXT);
    const nodes = []; while (walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach((n) => { const v = applyContact(n.nodeValue, c); if (v !== n.nodeValue) n.nodeValue = v; });
    doc.querySelectorAll("a[href^='tel:'],a[href^='mailto:']").forEach((a) => { a.setAttribute("href", applyContact(a.getAttribute("href"), c)); });
  }
}

export function pageIdFromPath(p) {
  p = decodeURIComponent(p || "/").replace(/^.*\//, "").replace(/\.html$/, "");
  return p || "index";
}
