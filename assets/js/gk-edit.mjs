/* gk-edit.mjs — the in-page editor (opened as <page>?edit from the panel).
   Tap a text to change it · tap a photo to replace it · tap a block to drag it, copy it or delete it · «Δημοσίευση» publishes.
   Live site: saves to /api/save (Netlify Blobs, 0 credits). Draft: trial mode, kept only in this browser. */
import { applyDom, clean, pageIdFromPath } from "./gk-core.mjs";
import { PAGES } from "./gk-pages.mjs";

const D = document, W = window, PID = pageIdFromPath(location.pathname.replace(/^\/arthro\/.*/, "/arthro"));
const PASS = sessionStorage.getItem("gk-pass") || "";
let LIVE = false; try { LIVE = (await fetch("/api/status", { cache: "no-store" })).ok; } catch {}
if (!PASS) { location.href = "admin.html?back=" + encodeURIComponent(location.pathname.replace(/^\//, "") + "?edit"); throw 0; }

/* ---------- styles ---------- */
const css = `
html.gk-ed [data-e]{outline:1px dashed transparent;outline-offset:3px;border-radius:3px;cursor:text;transition:outline-color .15s}
html.gk-ed [data-e]:hover{outline-color:rgba(176,72,40,.55)}
html.gk-ed [data-e].gk-on{outline:2px solid #B04828;background:rgba(255,250,240,.9);color:#1d2420;cursor:text}
html.gk-ed [data-e].gk-dirty:not(.gk-on){outline:1px solid rgba(46,125,50,.6)}
html.gk-ed img[data-ei]{cursor:pointer;outline:2px dashed transparent;outline-offset:-2px}
html.gk-ed img[data-ei]:hover{outline-color:rgba(176,72,40,.7)}
html.gk-ed .gk-item{outline:2px solid rgba(176,72,40,.85)!important;outline-offset:4px;border-radius:6px}
html.gk-ed .gk-drop{outline:2px dashed #2e7d32!important}
html.gk-ed body{padding-bottom:110px}html.gk-ed .mbar,html.gk-ed .totop,html.gk-ed #advon-consent-box,html.gk-ed .advon-ck{display:none!important}
.gk-ui,.gk-ui *{box-sizing:border-box;font:500 15px/1.35 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;letter-spacing:0;text-transform:none}
.gk-bar{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:2147483000;display:flex;gap:6px;align-items:center;padding:8px;border-radius:18px;background:#1d2420;color:#fff;box-shadow:0 12px 40px rgba(0,0,0,.35);max-width:calc(100vw - 16px)}
.gk-bar button,.gk-sheet button,.gk-tb button,.gk-ctl button{appearance:none;border:0;border-radius:12px;padding:11px 14px;min-height:44px;background:#2c3530;color:#fff;cursor:pointer;white-space:nowrap}
.gk-bar .gk-pub{background:#B04828}.gk-bar .gk-pub[disabled]{opacity:.45}
.gk-bar .gk-name{padding:0 8px;max-width:30vw;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;opacity:.85}
.gk-tb{position:absolute;z-index:2147483001;display:flex;gap:4px;padding:6px;border-radius:14px;background:#1d2420;box-shadow:0 8px 24px rgba(0,0,0,.3)}
.gk-tb button{min-width:44px;padding:8px 10px}.gk-tb .gk-ok{background:#2e7d32}
.gk-tb input{border:0;border-radius:10px;padding:8px 10px;min-width:180px}
.gk-ctl{position:absolute;z-index:2147483000;display:flex;gap:4px;padding:5px;border-radius:14px;background:#B04828;box-shadow:0 8px 22px rgba(0,0,0,.25)}
.gk-ctl button{background:rgba(0,0,0,.18);padding:8px 12px}.gk-ctl .gk-h{cursor:grab;touch-action:none}
.gk-add{position:absolute;z-index:2147482999}
.gk-add button{background:#2e7d32;border:0;color:#fff;border-radius:999px;padding:10px 16px;min-height:44px;box-shadow:0 6px 18px rgba(0,0,0,.2);cursor:pointer}
.gk-veil{position:fixed;inset:0;z-index:2147483002;background:rgba(20,24,22,.55);display:flex;align-items:flex-end;justify-content:center}
.gk-sheet{background:#fff;color:#1d2420;width:min(560px,100%);max-height:88vh;overflow:auto;border-radius:22px 22px 0 0;padding:20px 18px calc(18px + env(safe-area-inset-bottom))}
@media (min-width:700px){.gk-veil{align-items:center}.gk-sheet{border-radius:22px}}
.gk-sheet h3{margin:0 0 6px;font-weight:700;font-size:19px}.gk-sheet p{margin:0 0 14px;color:#4b554f}
.gk-sheet img{display:block;max-width:100%;max-height:42vh;margin:0 auto 14px;border-radius:12px;object-fit:contain}
.gk-sheet label{display:block;font-size:13px;color:#4b554f;margin:10px 0 4px}
.gk-sheet input[type=text]{width:100%;border:1px solid #cfd6d1;border-radius:12px;padding:12px}
.gk-sheet .gk-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}.gk-sheet .gk-row button{flex:1}
.gk-sheet .gk-main{background:#B04828}.gk-sheet .gk-sec{background:#e9ecea;color:#1d2420}.gk-sheet .gk-del{background:#fbe9e6;color:#9b2d16}
.gk-pages a{display:block;padding:13px 12px;border-radius:12px;color:#1d2420;text-decoration:none}.gk-pages a:hover,.gk-pages a.on{background:#f3efe7}
.gk-toast{position:fixed;left:50%;top:52px;transform:translateX(-50%);z-index:2147483003;background:#1d2420;color:#fff;padding:12px 16px;border-radius:14px;box-shadow:0 10px 30px rgba(0,0,0,.3);max-width:92vw}
.gk-ghost{position:fixed;z-index:2147483004;pointer-events:none;opacity:.85;transform:rotate(1.5deg);box-shadow:0 18px 40px rgba(0,0,0,.3)}
@media (max-width:640px){.gk-bar{left:8px;right:8px;transform:none;justify-content:space-between}.gk-bar .gk-name{display:none}.gk-bar button{padding:11px 12px}.gk-bar .gk-pub{flex:1}}
.gk-trial{position:fixed;top:0;left:0;right:0;z-index:2147482998;background:#fff3cd;color:#5b4300;text-align:center;padding:6px 10px;font:500 13px system-ui,sans-serif}
`;
D.head.insertAdjacentHTML("beforeend", `<style id="gk-edit-css">${css}</style>`);
D.documentElement.classList.add("gk-ed"); D.documentElement.classList.remove("js");

const ui = (html) => { const t = D.createElement("template"); t.innerHTML = html.trim(); return t.content.firstChild; };
const toast = (msg, ms = 2600) => { const n = ui(`<div class="gk-ui gk-toast"></div>`); n.textContent = msg; D.body.appendChild(n); setTimeout(() => n.remove(), ms); };
const zoneOf = (k) => (k[0] === "f" ? "*" : PID);

/* ---------- state ---------- */
const PKEY = "gk-pend-" + PID;
let pend = {}; try { pend = JSON.parse(localStorage.getItem(PKEY) || "{}"); } catch {}
const Z = (k) => { const z = zoneOf(k); pend[z] = pend[z] || { t: {}, i: {}, l: {} }; return pend[z]; };
const count = () => Object.values(pend).reduce((n, p) => n + Object.keys(p.t || {}).length + Object.keys(p.i || {}).length + Object.keys(p.l || {}).length, 0);
const savePend = () => { try { localStorage.setItem(PKEY, JSON.stringify(pend)); } catch { toast("Η φωτογραφία είναι πολύ μεγάλη για τη δοκιμή."); } bar.upd(); };

async function loadPublished() {
  if (LIVE) { try { return await (await fetch("/api/content", { cache: "no-store" })).json(); } catch { return {}; } }
  try { return JSON.parse(localStorage.getItem("gk-trial") || "{}"); } catch { return {}; }
}

/* ---------- the model: the page as written (with published edits), never touched by the site's animations ---------- */
const srcUrl = location.pathname + location.search.replace(/([?&])edit(=[^&]*)?&?/, "$1").replace(/[?&]$/, "");
const model = new DOMParser().parseFromString(await (await fetch(srcUrl, { cache: "no-store" })).text(), "text/html");
const published = await loadPublished();
if (!LIVE) applyDom(model, PID, published, false);
for (const z of Object.keys(pend)) applyDom(model, z === "*" ? "__" : PID, { pages: { [z === "*" ? "*" : PID]: pend[z] } }, false);

// show exactly the model inside every editable zone (undoes letter-splitting etc.)
const outer = (sel) => [...D.querySelectorAll(sel)].filter((el) => !el.parentElement.closest("[data-el]"));
for (const el of outer("[data-el]")) { const m = model.querySelector(`[data-el="${el.dataset.el}"]`); if (m) el.innerHTML = m.innerHTML; }
for (const el of D.querySelectorAll("[data-e]")) { const m = model.querySelector(`[data-e="${el.dataset.e}"]`); if (m && el.innerHTML !== m.innerHTML) el.innerHTML = m.innerHTML; }
for (const el of D.querySelectorAll("img[data-ei]")) { const m = model.querySelector(`img[data-ei="${el.dataset.ei}"]`); if (m) { ["src", "srcset", "sizes", "alt", "width", "height"].forEach((a) => m.hasAttribute(a) ? el.setAttribute(a, m.getAttribute(a)) : el.removeAttribute(a)); el.loading = "eager"; } }
D.querySelectorAll("[data-e]").forEach((el) => { if (pend[zoneOf(el.dataset.e)]?.t?.[el.dataset.e] != null) el.classList.add("gk-dirty"); });

/* ---------- text ---------- */
let cur = null, base = "", tb = null;
const markers = (k) => [D.createComment(`e:${k}`), D.createComment(`/e:${k}`)];
function stripComments(el) { [...el.childNodes].forEach((n) => n.nodeType === 8 && n.remove()); }
function tidy(h) {
  return clean(h).replace(/<div>(.*?)<\/div>/g, "<br>$1").replace(/\s(style|class|contenteditable|data-gk[\w-]*)="[^"]*"/g, "")
    .replace(/<(\/?)(strong)>/g, "<$1b>").replace(/<span>(.*?)<\/span>/g, "$1").replace(/(<br>)+$/, "").trim();
}
function startText(el, ev) {
  if (cur === el) return; endText(); cur = el; stripComments(el); base = el.innerHTML;
  el.contentEditable = "true"; el.classList.add("gk-on"); el.focus();
  if (ev && D.caretRangeFromPoint) { const r = D.caretRangeFromPoint(ev.clientX, ev.clientY); if (r && el.contains(r.startContainer)) { const s = getSelection(); s.removeAllRanges(); s.addRange(r); } }
  showToolbar(el); selectItem(el);
}
function endText() {
  if (!cur) return; const el = cur; cur = null; el.contentEditable = "false"; el.classList.remove("gk-on");
  const v = tidy(el.innerHTML); const k = el.dataset.e;
  if (!v) { el.innerHTML = base; toast("Το κείμενο δεν μπορεί να μείνει κενό — για να το αφαιρέσετε, διαγράψτε το μπλοκ."); }
  else if (v !== tidy(base)) {
    el.innerHTML = v; Z(k).t[k] = v; el.classList.add("gk-dirty");
    D.querySelectorAll(`[data-e="${k}"]`).forEach((o) => { if (o !== el) o.innerHTML = v; });
    const m = model.querySelector(`[data-e="${k}"]`); if (m) m.innerHTML = `<!--e:${k}-->${v}<!--/e:${k}-->`;
    savePend();
  }
  const [a, b] = markers(k); el.prepend(a); el.append(b);
  tb && tb.remove(); tb = null;
}
function showToolbar(el) {
  tb && tb.remove();
  tb = ui(`<div class="gk-ui gk-tb"><button data-c="bold" title="Έντονα"><b>B</b></button><button data-c="italic" title="Πλάγια"><i>I</i></button><button data-c="link" title="Σύνδεσμος">🔗</button><button class="gk-ok" data-c="ok">✓ Τέλος</button></div>`);
  D.body.appendChild(tb); place();
  tb.addEventListener("mousedown", (e) => e.preventDefault());
  tb.addEventListener("click", (e) => {
    const c = e.target.closest("button")?.dataset.c; if (!c) return;
    if (c === "ok") return endText();
    if (c === "link") {
      const sel = getSelection(); const range = sel.rangeCount ? sel.getRangeAt(0).cloneRange() : null;
      tb.innerHTML = `<input class="gk-l" type="text" placeholder="https://… ή email ή τηλέφωνο"><button class="gk-ok" data-c="setlink">OK</button><button data-c="nolink">Χωρίς</button>`;
      const inp = tb.querySelector("input"); inp.focus();
      tb.onclick = (ev2) => {
        const c2 = ev2.target.closest("button")?.dataset.c; if (!c2) return; el.focus();
        if (range) { sel.removeAllRanges(); sel.addRange(range); }
        if (c2 === "nolink") D.execCommand("unlink");
        else { let u = inp.value.trim(); if (/^[\w.+-]+@[\w-]+\.[\w.]+$/.test(u)) u = "mailto:" + u; else if (/^[+\d][\d ]{7,}$/.test(u)) u = "tel:" + u.replace(/\s/g, ""); else if (u && !/^(https?:|mailto:|tel:|#|\w[\w-]*\.html)/.test(u)) u = "https://" + u; if (u) D.execCommand("createLink", false, u); }
        tb.onclick = null; showToolbar(el);
      };
      return;
    }
    D.execCommand(c);
  });
}
function place() {
  if (tb && cur) { const r = cur.getBoundingClientRect(); const y = r.top + scrollY - tb.offsetHeight - 10; tb.style.top = Math.max(scrollY + 8, y < scrollY + 8 ? r.bottom + scrollY + 10 : y) + "px"; tb.style.left = Math.min(Math.max(8, r.left + scrollX), scrollX + innerWidth - tb.offsetWidth - 8) + "px"; }
  placeCtl();
}
addEventListener("scroll", () => requestAnimationFrame(place), { passive: true }); addEventListener("resize", place);
D.addEventListener("keydown", (e) => {
  if (!cur) return;
  if (e.key === "Enter") { e.preventDefault(); D.execCommand("insertLineBreak"); }
  if (e.key === "Escape") { cur.innerHTML = base; endText(); }
});
D.addEventListener("paste", (e) => { if (!cur) return; e.preventDefault(); D.execCommand("insertText", false, (e.clipboardData || W.clipboardData).getData("text/plain")); });

/* ---------- blocks (repeating items: conferences, cards, photos, questions…) ---------- */
let item = null, ctl = null, addBtn = null;
function itemsOf(list) {
  const kids = [...list.children]; const cnt = {};
  kids.forEach((k) => { const s = k.tagName + "." + (k.getAttribute("class") || "").split(" ")[0]; cnt[s] = (cnt[s] || 0) + 1; });
  const top = Object.entries(cnt).sort((a, b) => b[1] - a[1])[0]?.[0]; const tag = top && top.split(".")[0];
  return kids.filter((k) => k.tagName === tag && !k.classList.contains("cf-line") && !k.classList.contains("gk-arc"));
}
function itemFor(node) {
  let el = node; while (el && el !== D.body) { const p = el.parentElement; if (p && p.dataset.el && itemsOf(p).includes(el)) return el; el = p; } return null;
}
function selectItem(node) {
  const it = itemFor(node); if (it === item) return; item && item.classList.remove("gk-item"); item = it;
  ctl && ctl.remove(); addBtn && addBtn.remove(); ctl = addBtn = null;
  if (!item) return; item.classList.add("gk-item");
  ctl = ui(`<div class="gk-ui gk-ctl"><button class="gk-h" title="Σύρετε για αλλαγή σειράς">⠿ Μετακίνηση</button><button data-a="copy" title="Αντίγραφο">⧉</button><button data-a="del" title="Διαγραφή">✕</button></div>`);
  addBtn = ui(`<div class="gk-ui gk-add"><button>+ Προσθήκη νέου</button></div>`);
  D.body.append(ctl, addBtn); placeCtl();
  ctl.addEventListener("click", (e) => { const a = e.target.closest("button")?.dataset.a; if (a === "copy") copyItem(item, true); if (a === "del") delItem(item); });
  addBtn.addEventListener("click", () => { const its = itemsOf(item.parentElement); copyItem(its[its.length - 1], false); });
  ctl.querySelector(".gk-h").addEventListener("pointerdown", startDrag);
}
function placeCtl() {
  if (!item || !ctl) return; const r = item.getBoundingClientRect();
  ctl.style.top = r.top + scrollY - ctl.offsetHeight - 8 + "px"; ctl.style.left = Math.max(8, Math.min(r.right + scrollX - ctl.offsetWidth, scrollX + innerWidth - ctl.offsetWidth - 8)) + "px";
  const its = itemsOf(item.parentElement); const last = its[its.length - 1].getBoundingClientRect();
  addBtn.style.top = last.bottom + scrollY + 10 + "px"; addBtn.style.left = Math.max(8, last.left + scrollX) + "px";
}
const listKeyOf = (it) => it.parentElement.dataset.el;
const mList = (it) => model.querySelector(`[data-el="${listKeyOf(it)}"]`);
const idx = (it) => itemsOf(it.parentElement).indexOf(it);
function mItems(it) { const ml = mList(it); const live = itemsOf(it.parentElement)[0]; return [...ml.children].filter((k) => k.tagName === live.tagName && !k.classList.contains("cf-line") && !k.classList.contains("gk-arc")); }
function storeList(it) {
  const ml = mList(it).cloneNode(true); const k = listKeyOf(it); ml.querySelectorAll(".gk-arc").forEach((n) => n.remove());
  const h = ml.innerHTML.replace(new RegExp(`^<!--l:${k}-->|<!--/l:${k}-->$`, "g"), "");
  Z(k).l[k] = h; savePend(); setTimeout(placeCtl, 30);
}
function rekey(root) {
  const sfx = "-n" + Math.random().toString(36).slice(2, 6); const map = {};
  root.querySelectorAll("[data-e],[data-ei],[data-el]").forEach((el) => {
    for (const a of ["e", "ei", "el"]) if (el.dataset[a]) { const n = el.dataset[a].replace(/-n\w{4}$/, "") + sfx; map[el.dataset[a]] = n; el.dataset[a] = n; }
  });
  const tw = D.createTreeWalker(root, NodeFilter.SHOW_COMMENT); const cs = []; while (tw.nextNode()) cs.push(tw.currentNode);
  cs.forEach((c) => { const m = c.nodeValue.match(/^(\/?[eil]):(.+)$/); if (m && map[m[2]]) c.nodeValue = `${m[1]}:${map[m[2]]}`; });
  return sfx;
}
function copyItem(it, after) {
  endText(); const i = idx(it); const mi = mItems(it)[i];
  const mc = mi.cloneNode(true); const sfx = rekey(mc); mi.after(mc);
  const lc = it.cloneNode(true); lc.classList.remove("gk-item");
  // give the live copy the same new keys as the model copy
  const ml = [...mc.querySelectorAll("[data-e],[data-ei],[data-el]")]; const ll = [...lc.querySelectorAll("[data-e],[data-ei],[data-el]")];
  ll.forEach((el, n) => { for (const a of ["e", "ei", "el"]) if (el.dataset[a] && ml[n]) el.dataset[a] = ml[n].dataset[a]; });
  it.after(lc); storeList(it); selectItem(lc); lc.scrollIntoView({ block: "center", behavior: "smooth" });
  toast(after ? "Έγινε αντίγραφο — αλλάξτε τα κείμενα και τις φωτογραφίες του." : "Προστέθηκε νέο — αλλάξτε τα κείμενα και τις φωτογραφίες του.");
}
function delItem(it) {
  sheet(`<h3>Διαγραφή;</h3><p>Θα αφαιρεθεί αυτό το μπλοκ από τη σελίδα. Αν το μετανιώσετε, πατήστε «Ακύρωση αλλαγών» πριν τη δημοσίευση.</p><div class="gk-row"><button class="gk-sec" data-x>Όχι</button><button class="gk-del" data-ok>Ναι, διαγραφή</button></div>`, (s, close) => {
    s.querySelector("[data-ok]").onclick = () => {
      if (itemsOf(it.parentElement).length < 2) { toast("Πρέπει να μείνει τουλάχιστον ένα."); return close(); }
      const i = idx(it); const list = it; mItems(it)[i].remove(); const parent = it.parentElement; it.remove();
      item = null; ctl && ctl.remove(); addBtn && addBtn.remove(); ctl = addBtn = null;
      const mlc = mList({ parentElement: parent }).cloneNode(true); mlc.querySelectorAll(".gk-arc").forEach((n) => n.remove());
      Z(parent.dataset.el).l[parent.dataset.el] = mlc.innerHTML.replace(new RegExp(`^<!--l:${parent.dataset.el}-->|<!--/l:${parent.dataset.el}-->$`, "g"), "");
      savePend(); close(); toast("Διαγράφηκε.");
    };
  });
}
function startDrag(e) {
  e.preventDefault(); endText(); const it = item; if (!it) return;
  const list = it.parentElement; const r = it.getBoundingClientRect();
  const ghost = it.cloneNode(true); ghost.classList.add("gk-ghost"); ghost.style.width = r.width + "px"; ghost.style.left = r.left + "px"; ghost.style.top = r.top + "px"; D.body.appendChild(ghost);
  const dx = e.clientX - r.left, dy = e.clientY - r.top; it.style.opacity = ".35"; let target = null, before = true;
  const move = (ev) => {
    ghost.style.left = ev.clientX - dx + "px"; ghost.style.top = ev.clientY - dy + "px";
    if (ev.clientY < 70) scrollBy(0, -14); if (ev.clientY > innerHeight - 110) scrollBy(0, 14);
    const its = itemsOf(list).filter((x) => x !== it); let best = null, bd = 1e9;
    for (const x of its) { const q = x.getBoundingClientRect(); const d = Math.hypot(ev.clientX - (q.left + q.width / 2), ev.clientY - (q.top + q.height / 2)); if (d < bd) { bd = d; best = x; } }
    its.forEach((x) => x.classList.remove("gk-drop")); target = best;
    if (best) { best.classList.add("gk-drop"); const q = best.getBoundingClientRect(); const horiz = q.width < list.getBoundingClientRect().width * 0.7;
      before = horiz ? ev.clientX < q.left + q.width / 2 : ev.clientY < q.top + q.height / 2; }
  };
  const up = () => {
    removeEventListener("pointermove", move); removeEventListener("pointerup", up); ghost.remove(); it.style.opacity = "";
    itemsOf(list).forEach((x) => x.classList.remove("gk-drop"));
    if (target) {
      const mi = mItems(it); const from = idx(it), to = idx(target); const mFrom = mi[from], mTo = mi[to];
      if (before) { target.before(it); mTo.before(mFrom); } else { target.after(it); mTo.after(mFrom); }
      storeList(it); toast("Η σειρά άλλαξε.");
    }
  };
  addEventListener("pointermove", move); addEventListener("pointerup", up);
}

/* ---------- photos ---------- */
function shrink(file, max) {
  return new Promise((res, rej) => {
    const img = new Image(); img.onload = () => {
      const s = Math.min(1, max / Math.max(img.naturalWidth, img.naturalHeight)); const c = D.createElement("canvas");
      c.width = Math.round(img.naturalWidth * s); c.height = Math.round(img.naturalHeight * s); c.getContext("2d").drawImage(img, 0, 0, c.width, c.height);
      c.toBlob((b) => (b ? res({ blob: b, w: c.width, h: c.height, url: c.toDataURL("image/webp", LIVE ? 0.85 : 0.78) }) : rej()), "image/webp", 0.85);
    }; img.onerror = rej; img.src = URL.createObjectURL(file);
  });
}
function photo(img) {
  endText(); selectItem(img);
  const k = img.dataset.ei;
  sheet(`<h3>Φωτογραφία</h3><img src="${img.currentSrc || img.src}" alt=""><button class="gk-main" data-pick style="width:100%">Επιλογή νέας φωτογραφίας</button><input type="file" accept="image/*" hidden>
    <label>Περιγραφή της φωτογραφίας (τη διαβάζει η Google)</label><input type="text" value="${(img.alt || "").replace(/"/g, "&quot;")}">
    <div class="gk-row"><button class="gk-sec" data-x>Άκυρο</button><button class="gk-main" data-ok>Εφαρμογή</button></div>`, (s, close) => {
    const file = s.querySelector("input[type=file]"); let next = null;
    s.querySelector("[data-pick]").onclick = () => file.click();
    file.onchange = async () => {
      const f = file.files[0]; if (!f) return; s.querySelector("[data-pick]").textContent = "Ετοιμάζεται…";
      try { next = await shrink(f, LIVE ? 2000 : 1400); s.querySelector("img").src = next.url; s.querySelector("[data-pick]").textContent = "Άλλη φωτογραφία"; }
      catch { toast("Δεν άνοιξε αυτή η φωτογραφία. Δοκιμάστε JPG ή PNG."); s.querySelector("[data-pick]").textContent = "Επιλογή νέας φωτογραφίας"; }
    };
    s.querySelector("[data-ok]").onclick = async () => {
      const alt = s.querySelector("input[type=text]").value.trim(); const v = { alt };
      if (next) {
        v.w = next.w; v.h = next.h;
        if (LIVE) {
          s.querySelector("[data-ok]").textContent = "Ανέβασμα…";
          try { const r = await fetch("/api/upload", { method: "POST", headers: { "x-pass": PASS, "content-type": "image/webp" }, body: next.blob }); const j = await r.json(); if (!j.ok) throw 0; v.src = j.url; }
          catch { toast("Το ανέβασμα δεν έγινε. Ελέγξτε τη σύνδεση και ξαναδοκιμάστε."); s.querySelector("[data-ok]").textContent = "Εφαρμογή"; return; }
        } else v.src = next.url;
      }
      const prev = Z(k).i[k] || {}; Z(k).i[k] = { ...prev, ...v };
      const set = (el) => { el.removeAttribute("srcset"); el.removeAttribute("sizes"); if (v.src) { el.src = v.src; if (el.dataset.lb) el.dataset.lb = v.src; } el.alt = alt; if (v.w) { el.width = v.w; el.height = v.h; } };
      D.querySelectorAll(`img[data-ei="${k}"]`).forEach(set); model.querySelectorAll(`img[data-ei="${k}"]`).forEach(set);
      const it = itemFor(img); if (it) storeList(it); savePend(); close(); toast("Η φωτογραφία άλλαξε.");
    };
  });
}

/* ---------- sheets, bar ---------- */
function sheet(html, init) {
  const v = ui(`<div class="gk-ui gk-veil"><div class="gk-sheet" role="dialog" aria-modal="true"></div></div>`);
  v.firstChild.innerHTML = html; D.body.appendChild(v);
  const close = () => v.remove();
  v.addEventListener("click", (e) => { if (e.target === v || e.target.closest("[data-x]")) close(); });
  init && init(v.firstChild, close); return v;
}
const bar = (() => {
  const b = ui(`<div class="gk-ui gk-bar"><button data-b="pages" title="Σελίδες">☰</button><span class="gk-name"></span><button data-b="undo" title="Ακύρωση αλλαγών">↺ Ακύρωση</button><button class="gk-pub" data-b="pub">Δημοσίευση</button><button data-b="out" title="Πίνακας">✕</button></div>`);
  D.body.appendChild(b);
  const me = PAGES.find((p) => p.id === PID); b.querySelector(".gk-name").textContent = me ? me.name : D.title.split("|")[0];
  if (!LIVE) D.body.appendChild(ui(`<div class="gk-ui gk-trial">Δοκιμή στο draft: οι αλλαγές μένουν μόνο σε αυτή τη συσκευή. Στην κανονική ιστοσελίδα δημοσιεύονται για όλους.</div>`));
  b.addEventListener("click", (e) => {
    const a = e.target.closest("button")?.dataset.b;
    if (a === "pages") sheet(`<h3>Σελίδες</h3><div class="gk-pages">${PAGES.map((p) => `<a href="${p.url}?edit" class="${p.id === PID ? "on" : ""}">${p.name}</a>`).join("")}</div>`, (s) => s.querySelectorAll("a").forEach((x) => x.addEventListener("click", (ev) => { if (count()) { ev.preventDefault(); toast("Πατήστε πρώτα «Δημοσίευση» ή «Ακύρωση αλλαγών»."); } })));
    if (a === "undo") { if (!count()) return toast("Δεν υπάρχουν αλλαγές."); sheet(`<h3>Ακύρωση αλλαγών;</h3><p>Θα χαθούν οι αλλαγές αυτής της σελίδας που δεν δημοσιεύσατε.</p><div class="gk-row"><button class="gk-sec" data-x>Όχι</button><button class="gk-del" data-ok>Ναι</button></div>`, (s) => s.querySelector("[data-ok]").onclick = () => { localStorage.removeItem(PKEY); location.reload(); }); }
    if (a === "pub") publish();
    if (a === "out") { if (count()) return toast("Έχετε αλλαγές που δεν δημοσιεύσατε."); location.href = "admin.html"; }
  });
  return { upd() { const n = count(); const p = b.querySelector(".gk-pub"); p.disabled = !n; p.textContent = n ? `Δημοσίευση (${n})` : "Δημοσίευση"; } };
})();
bar.upd();

async function publish() {
  endText(); if (!count()) return;
  const btn = D.querySelector(".gk-pub"); btn.disabled = true; btn.textContent = "Δημοσίευση…";
  const c = await loadPublished(); c.pages = c.pages || {};
  for (const [z, p] of Object.entries(pend)) { const q = (c.pages[z] = c.pages[z] || { t: {}, i: {}, l: {} }); for (const s of ["t", "i", "l"]) q[s] = { ...(q[s] || {}), ...(p[s] || {}) }; }
  if (LIVE) {
    try { const r = await fetch("/api/save", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ pass: PASS, action: "publish", content: c }) }); const j = await r.json(); if (!j.ok) throw j; }
    catch (e) { bar.upd(); return toast(e && e.error === "pass" ? "Ο κωδικός άλλαξε — συνδεθείτε ξανά από τον πίνακα." : "Η δημοσίευση δεν έγινε. Ελέγξτε τη σύνδεση και ξαναδοκιμάστε.", 4000); }
  } else { try { localStorage.setItem("gk-trial", JSON.stringify(c)); } catch { bar.upd(); return toast("Η δοκιμή γέμισε (πολλές φωτογραφίες). Στην κανονική σελίδα δεν υπάρχει όριο.", 5000); } }
  localStorage.removeItem(PKEY); toast("Δημοσιεύτηκε! ✓", 1800); setTimeout(() => location.reload(), 900);
}

/* ---------- clicks: edit instead of navigating ---------- */
D.addEventListener("click", (e) => {
  if (e.target.closest(".gk-ui")) return;
  const t = e.target.closest("[data-e]"); const im = e.target.closest("img[data-ei]");
  if (t || im || e.target.closest("a,summary,button,[data-lb]")) { e.preventDefault(); e.stopImmediatePropagation(); }
  if (t) return startText(t, e);
  if (im) return photo(im);
  if (cur && !cur.contains(e.target)) endText();
  selectItem(e.target);
}, true);
addEventListener("beforeunload", (e) => { if (cur) endText(); });
toast(count() ? `Έχετε ${count()} αλλαγές που δεν δημοσιεύσατε ακόμα.` : "Πατήστε σε ένα κείμενο ή μια φωτογραφία για να το αλλάξετε.", 3600);
