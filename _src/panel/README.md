# Admin panel (in-page editor) — Advon, 25 Nov 2026
After ANY rebuild of the pages: `python3 _src/panel/mark.py .` then `python3 _src/panel/build_tpl.py .`
(the gk-boot loader + gk-site-css are added by the round-5 patch in the session notes — keep them in every page).
- Marks: texts `data-e` + `<!--e:K-->`, photos `data-ei`, repeating blocks `data-el` + `<!--l:K-->`. Keys = hash of the original content.
- Edits: Netlify Blobs store `gk-content` (content.json; previous = content-prev.json + history/<date>.json), photos in `gk-images`.
- `netlify/edge-functions/gk.js` writes the edits into every page before it is sent; new articles live at /arthro/<slug> (template arthro-neo.html).
- Passcode = Netlify env var ADMIN_PASS only (not in the repo). The draft runs a trial mode (this browser only).
