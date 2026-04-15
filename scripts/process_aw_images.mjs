#!/usr/bin/env node
import sharp from "sharp";
import fs from "fs";
import path from "path";

const root = path.join(process.cwd(), "assets", "img");

async function processJpg(relPath) {
  const full = path.join(root, relPath);
  if (!fs.existsSync(full)) {
    console.warn("skip missing", relPath);
    return;
  }
  const tmp = full + ".tmp.jpg";
  await sharp(full)
    .rotate()
    .resize({ width: 1920, withoutEnlargement: true })
    .jpeg({ quality: 84, mozjpeg: true })
    .toFile(tmp);
  fs.renameSync(tmp, full);
  const webp = full.replace(/\.jpg$/i, ".webp");
  await sharp(full).webp({ quality: 82 }).toFile(webp);
  const st = fs.statSync(full);
  console.log(relPath, Math.round(st.size / 1024), "KB");
}

const files = [
  "heroes/home-hero.jpg",
  "heroes/how-it-works-hero.jpg",
  "heroes/about-hero.jpg",
  "heroes/quality-hero.jpg",
  "categories/weight-loss.jpg",
  "categories/muscle-performance.jpg",
  "categories/recovery-healing.jpg",
  "categories/longevity.jpg",
  "categories/sexual-health.jpg",
  "categories/hair-skin.jpg",
  "trust/physician-review.jpg",
  "trust/pharmacy-vials.jpg",
  "trust/laboratory.jpg",
];

for (const f of files) {
  await processJpg(f);
}

// OG placeholder (wordmark TODO in design tool)
const ogPath = path.join(root, "og", "og-default.jpg");
await sharp({
  create: { width: 1200, height: 630, channels: 3, background: "#2d4a3e" },
})
  .jpeg({ quality: 85 })
  .toFile(ogPath);
await sharp(ogPath).webp({ quality: 82 }).toFile(ogPath.replace(/\.jpg$/, ".webp"));
console.log("og/og-default.jpg (solid brand background — TODO: wordmark overlay)");
