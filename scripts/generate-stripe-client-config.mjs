#!/usr/bin/env node
/**
 * Builds js/stripe-config.js from scripts/stripe-products.json (price IDs only).
 * Publishable key + Worker URL are injected at deploy or edited manually if needed.
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, "..");
const JSON_PATH = path.join(__dirname, "stripe-products.json");
const OUT_PATH = path.join(ROOT, "js", "stripe-config.js");

const data = JSON.parse(fs.readFileSync(JSON_PATH, "utf8"));
const prices = {};

for (const p of data.products) {
  const row = {};
  if (p.stripe_price_id_monthly) row.monthly = p.stripe_price_id_monthly;
  else row.monthly = null;
  if (p.stripe_price_id_quarterly) row.quarterly = p.stripe_price_id_quarterly;
  else row.quarterly = null;
  if (p.stripe_price_id_one_time) row.oneTime = p.stripe_price_id_one_time;
  prices[p.slug] = row;
}

const cfg = {
  publishableKey: "",
  createSessionEndpoint: "",
  prices,
};

const json = JSON.stringify(cfg, null, 2);
const file = `/**
 * Public Stripe price map for static checkout (price IDs are safe to expose).
 * Regenerate: npm run generate-stripe-config
 * After deploy, set createSessionEndpoint to your Worker URL (see workers/aw-checkout-session).
 */
window.AW_STRIPE_PUBLIC = ${json};
`;

fs.writeFileSync(OUT_PATH, file, "utf8");
console.log("Wrote", OUT_PATH);
