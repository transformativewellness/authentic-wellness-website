#!/usr/bin/env node
/**
 * Creates/updates Stripe Products and Prices from scripts/stripe-products.json.
 *
 * Usage:
 *   STRIPE_SECRET_KEY=sk_test_... node scripts/sync-stripe.js
 *   STRIPE_SECRET_KEY=sk_test_... node scripts/sync-stripe.js --dry-run
 *
 * Never deletes prices; deactivates archived prices when replacing (optional).
 * Archives legacy AW products that have metadata authentic_wellness=1 but slug not in catalog.
 */
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import Stripe from "stripe";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(__dirname, "..");
const JSON_PATH = path.join(ROOT, "scripts", "stripe-products.json");

const dryRun = process.argv.includes("--dry-run");

function log(...args) {
  console.log(new Date().toISOString(), ...args);
}

function loadJson() {
  const raw = fs.readFileSync(JSON_PATH, "utf8");
  return JSON.parse(raw);
}

function saveJson(data) {
  fs.writeFileSync(JSON_PATH, JSON.stringify(data, null, 2) + "\n", "utf8");
}

function compliantDescription(name) {
  return `Physician-evaluated wellness program: ${name}. Compounded medications may be used when prescribed; prepared by licensed U.S. compounding pharmacies when applicable. Not FDA-approved as compounded.`;
}

async function main() {
  const secret = process.env.STRIPE_SECRET_KEY;
  if (!secret && !dryRun) {
    console.error("Missing STRIPE_SECRET_KEY. Use --dry-run to preview without API calls.");
    process.exit(1);
  }

  const stripe = secret ? new Stripe(secret) : null;
  const data = loadJson();
  const catalogSlugs = new Set(data.products.map((p) => p.slug));

  if (dryRun) {
    log("[dry-run] Would process", data.products.length, "products");
    for (const p of data.products) {
      log(
        "[dry-run] product:",
        p.slug,
        p.name,
        "monthly:",
        p.monthly_amount_cents ?? "n/a",
        "qtr:",
        p.quarterly_total_cents ?? "n/a",
        "once:",
        p.one_time_amount_cents ?? "n/a",
      );
    }
  }

  // Archive legacy products tracked by our metadata but not in current catalog
  if (stripe && !dryRun) {
    let startingAfter;
    for (;;) {
      const list = await stripe.products.list({
        limit: 100,
        active: true,
        starting_after: startingAfter,
      });
      for (const prod of list.data) {
        const md = prod.metadata || {};
        if (md.authentic_wellness === "true" && md.slug && !catalogSlugs.has(md.slug)) {
          log("[archive] product not in catalog:", prod.id, prod.name, "slug:", md.slug);
          await stripe.products.update(prod.id, { active: false });
        }
      }
      if (!list.has_more) break;
      startingAfter = list.data[list.data.length - 1].id;
    }
  } else if (dryRun) {
    log("[dry-run] Would scan Stripe for products to archive (authentic_wellness metadata, unknown slug)");
  }

  for (const product of data.products) {
    let productId = product.stripe_product_id;

    if (!productId) {
      if (dryRun) {
        log("[dry-run] Would create Product:", product.name, product.slug);
        productId = "prod_DRYRUN";
      } else {
        const created = await stripe.products.create({
          name: product.name,
          description: compliantDescription(product.name),
          metadata: {
            slug: product.slug,
            category: product.category ?? "",
            delivery_method: product.delivery_method ?? "",
            pharmacy: product.pharmacy ?? "",
            requires_consultation: String(!!product.requires_consultation),
            authentic_wellness: "true",
            catalog_version: data.catalog_version ?? "",
          },
        });
        productId = created.id;
        product.stripe_product_id = productId;
        log("[create] product", product.slug, productId);
      }
    } else if (!dryRun) {
      await stripe.products.update(productId, {
        name: product.name,
        description: compliantDescription(product.name),
        metadata: {
          slug: product.slug,
          category: product.category ?? "",
          delivery_method: product.delivery_method ?? "",
          pharmacy: product.pharmacy ?? "",
          requires_consultation: String(!!product.requires_consultation),
          authentic_wellness: "true",
          catalog_version: data.catalog_version ?? "",
        },
      });
      log("[update] product metadata", product.slug, productId);
    }

    // One-time (Discovery)
    if (product.one_time_amount_cents != null) {
      if (!product.stripe_price_id_one_time) {
        if (dryRun) {
          log("[dry-run] Would create one-time price", product.one_time_amount_cents, "usd");
        } else {
          const price = await stripe.prices.create({
            product: productId,
            currency: "usd",
            unit_amount: product.one_time_amount_cents,
            nickname: `${product.name} (one-time)`,
            metadata: { slug: product.slug, billing: "one_time", authentic_wellness: "true" },
          });
          product.stripe_price_id_one_time = price.id;
          log("[create] price one_time", product.slug, price.id);
        }
      }
      continue;
    }

    // Monthly subscription
    if (!product.stripe_price_id_monthly && product.monthly_amount_cents != null) {
      if (dryRun) {
        log("[dry-run] Would create monthly price", product.monthly_amount_cents);
      } else {
        const price = await stripe.prices.create({
          product: productId,
          currency: "usd",
          unit_amount: product.monthly_amount_cents,
          recurring: { interval: "month" },
          nickname: `${product.name} (Monthly)`,
          metadata: { slug: product.slug, billing: "monthly", authentic_wellness: "true" },
        });
        product.stripe_price_id_monthly = price.id;
        log("[create] price monthly", product.slug, price.id);
      }
    }

    // Quarterly: billed every 3 months
    if (!product.stripe_price_id_quarterly && product.quarterly_total_cents != null) {
      if (dryRun) {
        log("[dry-run] Would create quarterly price total", product.quarterly_total_cents);
      } else {
        const price = await stripe.prices.create({
          product: productId,
          currency: "usd",
          unit_amount: product.quarterly_total_cents,
          recurring: { interval: "month", interval_count: 3 },
          nickname: `${product.name} (Quarterly — Save 10%)`,
          metadata: { slug: product.slug, billing: "quarterly", authentic_wellness: "true" },
        });
        product.stripe_price_id_quarterly = price.id;
        log("[create] price quarterly", product.slug, price.id);
      }
    }
  }

  if (!dryRun) {
    saveJson(data);
    log("Wrote", JSON_PATH);
  } else {
    log("[dry-run] No file changes.");
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
