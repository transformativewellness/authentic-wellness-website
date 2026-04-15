#!/usr/bin/env node
/**
 * Read-only audit: list Stripe products + aw_category / aw_compound metadata.
 * Usage: STRIPE_SECRET_KEY=sk_live_... node scripts/audit_aw_stripe_metadata.js
 * Output: scripts/aw_stripe_audit.txt (and stdout)
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import Stripe from "stripe";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(__dirname, "aw_stripe_audit.txt");

const TW_SKU_SUBSTRINGS = [
  "Neurotoxin",
  "Botox",
  "Filler",
  "Microneedling",
  "Facial",
  "IV ",
  "Hydrafacial",
  "Laser",
  "Lip",
];

function flagTwSku(name) {
  if (!name) return false;
  return TW_SKU_SUBSTRINGS.some((s) => name.includes(s));
}

async function main() {
  const key = process.env.STRIPE_SECRET_KEY;
  if (!key) {
    const msg =
      "ERROR: STRIPE_SECRET_KEY is not set. Export your Authentic Wellness (Evolving Wellness LLC) secret key and re-run.\n";
    fs.writeFileSync(OUT, msg, "utf8");
    console.error(msg);
    process.exit(1);
  }

  const stripe = new Stripe(key);
  const lines = [];

  const account = await stripe.accounts.retrieve();
  const bizName =
    account.business_profile?.name ||
    account.settings?.dashboard?.display_name ||
    account.company?.name ||
    "(no business_profile.name)";
  const email = account.email || account.business_profile?.support_email || "(no email on account object)";
  const country = account.country || "(unknown)";

  lines.push("=== Stripe account (verify this is Evolving Wellness LLC / AW, not TW) ===");
  lines.push(`business_profile.name: ${bizName}`);
  lines.push(`email: ${email}`);
  lines.push(`country: ${country}`);
  lines.push("");

  const products = [];
  for await (const p of stripe.products.list({ limit: 100, active: true })) {
    products.push(p);
  }
  for await (const p of stripe.products.list({ limit: 100, active: false })) {
    products.push(p);
  }

  const byId = new Map();
  for (const p of products) {
    if (!byId.has(p.id)) byId.set(p.id, p);
  }
  const unique = [...byId.values()].sort((a, b) => a.name.localeCompare(b.name));

  lines.push(`=== Products (${unique.length} unique by id, active+inactive) ===`);
  for (const p of unique) {
    const cat = p.metadata?.aw_category ?? "";
    const comp = p.metadata?.aw_compound ?? "";
    const missing = !cat || !comp ? "MISSING METADATA" : "";
    const tw = flagTwSku(p.name) ? "TW SKU FLAG" : "";
    const flags = [missing, tw].filter(Boolean).join(" | ");
    lines.push(
      `id=${p.id} | name=${JSON.stringify(p.name)} | aw_category=${JSON.stringify(cat)} | aw_compound=${JSON.stringify(comp)}${flags ? ` | ** ${flags} **` : ""}`,
    );
  }

  const text = lines.join("\n") + "\n";
  fs.writeFileSync(OUT, text, "utf8");
  process.stdout.write(text);
}

main().catch((e) => {
  const msg = String(e?.message || e);
  fs.writeFileSync(OUT, `ERROR: ${msg}\n`, "utf8");
  console.error(e);
  process.exit(1);
});
