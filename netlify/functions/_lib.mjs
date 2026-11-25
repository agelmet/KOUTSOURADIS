/* Shared helpers for the Κουτσουραδής panel. Edits live in Netlify Blobs: they show at once and NEVER deploy (0 credits).
   The passcode is ONLY the Netlify environment variable ADMIN_PASS (no variable = every login refused). */
import { getStore } from "@netlify/blobs";
export const content = () => getStore({ name: "gk-content", consistency: "strong" });
export const images = () => getStore("gk-images");
export const json = (body, status = 200) => new Response(JSON.stringify(body), {
  status, headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store" } });
export async function checkPass(p) {
  const ok = typeof p === "string" && !!p && !!process.env.ADMIN_PASS && p === process.env.ADMIN_PASS;
  if (!ok) await new Promise((r) => setTimeout(r, 700)); // slow down guessing
  return ok;
}
