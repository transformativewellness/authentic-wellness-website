#!/usr/bin/env python3
"""Inject BreadcrumbList JSON-LD, missing Product schema, fix logos, titles, focus-calm URLs."""
from __future__ import annotations

import html as html_lib
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]

AW_HTML = (
    [ROOT / n for n in [
        "index.html", "programs.html", "about.html", "contact.html", "faq.html",
        "privacy.html", "terms.html", "how-it-works.html", "quality.html",
        "gym-intake.html", "checkout-success.html", "checkout-cancel.html", "404.html",
    ]]
    + list((ROOT / "programs").glob("*.html"))
    + list((ROOT / "blog").glob("*.html"))
)

BASE = "https://www.authenticwellness.com"
OLD_LOGO = '"logo": "https://www.authenticwellness.com/assets/img/og/og-default.jpg"'
NEW_LOGO = '"logo": "https://www.authenticwellness.com/logo-dark.svg"'

TITLE_SUFFIX = " — Physician-Prescribed Telehealth"

CAT_SLUGS = frozenset({
    "weight-loss", "muscle-performance", "recovery-healing",
    "longevity", "sexual-health", "hair-skin",
})

CAT_LABEL = {
    "weight-loss": "Weight loss",
    "muscle-performance": "Muscle & performance",
    "recovery-healing": "Recovery & healing",
    "longevity": "Longevity",
    "sexual-health": "Sexual health",
    "hair-skin": "Hair & skin",
}

SLUG_TO_CAT: dict[str, str] = {}
for s in [
    "glp1-sema", "glp1-tirz", "semaglutide-oral", "semaglutide-drops",
    "tirzepatide-oral", "tirzepatide-drops", "stella-weight-loss",
]:
    SLUG_TO_CAT[s] = "weight-loss"
for s in [
    "cjc-1295-ipamorelin", "sermorelin-injectable", "sermorelin-nasal-spray",
    "tesamorelin", "mots-c",
]:
    SLUG_TO_CAT[s] = "muscle-performance"
for s in ["bpc-157", "bpc-tb-recovery-stack", "ghk-cu", "ss-31", "thymosin-alpha-1"]:
    SLUG_TO_CAT[s] = "recovery-healing"
for s in ["nad-injectable", "nad-nasal-spray", "epithalon", "ldn", "metformin", "focus-calm"]:
    SLUG_TO_CAT[s] = "longevity"
for s in ["pt-141", "ed-sildenafil", "ed-tadalafil"]:
    SLUG_TO_CAT[s] = "sexual-health"
for s in ["female-hair-loss", "male-hair-loss", "mens-hair-loss-topical"]:
    SLUG_TO_CAT[s] = "hair-skin"

COGNITIVE = frozenset({"selank", "semax", "cognitive-stack", "methylene-blue"})
STUBS = frozenset({"perform", "renew", "recovery", "discovery"})

ROOT_PAGE_LABEL = {
    "index.html": "Home",
    "programs.html": "Programs",
    "about.html": "About",
    "contact.html": "Contact",
    "faq.html": "FAQ",
    "privacy.html": "Privacy Policy",
    "terms.html": "Terms of Service",
    "how-it-works.html": "How It Works",
    "quality.html": "Quality & compliance",
    "gym-intake.html": "Gym intake",
    "checkout-success.html": "Checkout success",
    "checkout-cancel.html": "Checkout canceled",
    "404.html": "Page not found",
}


def page_url(rel: pathlib.Path) -> str:
    if rel.as_posix() == "index.html":
        return f"{BASE}/"
    return f"{BASE}/{rel.as_posix()}"


def extract_title(text: str) -> str:
    m = re.search(r"<title>(.*?)</title>", text, re.I | re.DOTALL)
    if not m:
        return "Page"
    return html_lib.unescape(re.sub(r"\s+", " ", m.group(1).strip()))


def extract_meta_description(text: str) -> str:
    m = re.search(
        r'<meta\s+name="description"\s+content="([^"]*)"',
        text,
        re.I,
    )
    return html_lib.unescape(m.group(1)) if m else "Physician-prescribed telehealth program."


def extract_price(text: str) -> str | None:
    m = re.search(r'price-badge-amber">\s*\$([0-9]+)', text)
    return m.group(1) if m else None


def product_category_label(slug: str) -> str:
    cat = SLUG_TO_CAT.get(slug, "Programs")
    if cat in CAT_LABEL:
        return CAT_LABEL[cat]
    return "Programs"


def breadcrumb_json(rel: pathlib.Path, raw: str) -> dict:
    items: list[dict] = []
    pos = 1
    items.append({
        "@type": "ListItem",
        "position": pos,
        "name": "Home",
        "item": f"{BASE}/",
    })
    pos += 1
    title = extract_title(raw)

    if rel.as_posix() == "index.html":
        return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

    if rel.parts[0] == "blog":
        items.append({
            "@type": "ListItem",
            "position": pos,
            "name": "Blog",
            "item": f"{BASE}/blog/",
        })
        pos += 1
        if rel.name == "index.html":
            items[-1]["name"] = "Blog"
            return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
        short = title.split("|")[0].strip() if "|" in title else rel.stem.replace("-", " ").title()
        items.append({
            "@type": "ListItem",
            "position": pos,
            "name": short,
            "item": page_url(rel),
        })
        return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

    if rel.parts[0] == "programs" and rel.suffix == ".html":
        items.append({
            "@type": "ListItem",
            "position": pos,
            "name": "Programs",
            "item": f"{BASE}/programs.html",
        })
        pos += 1
        slug = rel.stem
        if slug in STUBS:
            items.append({
                "@type": "ListItem",
                "position": pos,
                "name": title.split("|")[0].strip(),
                "item": page_url(rel),
            })
            return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
        if slug in CAT_SLUGS:
            items.append({
                "@type": "ListItem",
                "position": pos,
                "name": CAT_LABEL[slug],
                "item": f"{BASE}/programs/{slug}.html",
            })
            return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}
        cat = SLUG_TO_CAT.get(slug)
        if cat:
            items.append({
                "@type": "ListItem",
                "position": pos,
                "name": CAT_LABEL[cat],
                "item": f"{BASE}/programs/{cat}.html",
            })
            pos += 1
        short = title.split("|")[0].strip()
        items.append({
            "@type": "ListItem",
            "position": pos,
            "name": short,
            "item": page_url(rel),
        })
        return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}

    label = ROOT_PAGE_LABEL.get(rel.name, rel.stem.replace("-", " ").title())
    items.append({
        "@type": "ListItem",
        "position": pos,
        "name": label,
        "item": page_url(rel),
    })
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def inject_breadcrumb(text: str, rel: pathlib.Path) -> str:
    if "BreadcrumbList" in text:
        return text
    crumb = json.dumps(breadcrumb_json(rel, text), indent=2)
    block = f'  <script type="application/ld+json">\n{crumb}\n  </script>\n'
    if "<!-- aw-medical-org -->" in text:
        return text.replace("<!-- aw-medical-org -->", block + "<!-- aw-medical-org -->", 1)
    return text.replace("</head>", block + "</head>", 1)


def inject_product(text: str, rel: pathlib.Path) -> str:
    if rel.parent.name != "programs" or rel.suffix != ".html":
        return text
    slug = rel.stem
    if slug in COGNITIVE | STUBS | CAT_SLUGS:
        return text
    if '"@type": "Product"' in text or "'@type': 'Product'" in text:
        return text
    price = extract_price(text)
    if not price:
        return text
    title = extract_title(text)
    name = title.split("|")[0].strip()
    if not name.lower().endswith("program"):
        name = f"{name} Program"
    desc = extract_meta_description(text)
    cat = product_category_label(slug)
    product = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": name,
        "description": desc,
        "brand": {"@type": "Brand", "name": "Authentic Wellness"},
        "category": cat,
        "offers": {
            "@type": "Offer",
            "price": price,
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "url": page_url(rel),
        },
    }
    block = f'  <script type="application/ld+json">\n{json.dumps(product, indent=2)}\n  </script>\n'
    if "<!-- aw-medical-org -->" in text:
        return text.replace("<!-- aw-medical-org -->", block + "<!-- aw-medical-org -->", 1)
    return text.replace("</head>", block + "</head>", 1)


def normalize_title(text: str) -> str:
    def repl(m: re.Match[str]) -> str:
        inner = m.group(1)
        if TITLE_SUFFIX.strip(" —") in inner:
            return m.group(0)
        if inner.rstrip().endswith("| Authentic Wellness"):
            return f"<title>{inner.rstrip()}{TITLE_SUFFIX}</title>"
        return m.group(0)

    return re.sub(r"<title>(.*?)</title>", repl, text, count=1, flags=re.I | re.DOTALL)


def fix_focus_calm(text: str, rel: pathlib.Path) -> str:
    if rel.as_posix() != "programs/focus-calm.html":
        return text
    text = text.replace(
        "https://www.authenticwellness.com/programs/cognitive-stack.html",
        "https://www.authenticwellness.com/programs/focus-calm.html",
    )
    return text


def enrich_cognitive_head(text: str, rel: pathlib.Path) -> str:
    if rel.parent.name != "programs" or rel.stem not in COGNITIVE:
        return text
    if '<meta property="og:type"' in text:
        return text
    slug = rel.stem
    url = f"{BASE}/programs/{slug}.html"
    title = extract_title(text)
    desc = extract_meta_description(text)
    et = html_lib.escape(title, quote=True)
    ed = html_lib.escape(desc, quote=True)
    block = f"""  <meta name="theme-color" content="#2d4a3e">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{et}">
  <meta property="og:description" content="{ed}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{BASE}/assets/img/og/og-default.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Authentic Wellness — branded preview graphic (illustrative, not a patient photo).">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{et}">
  <meta name="twitter:description" content="{ed}">
  <meta name="twitter:image" content="{BASE}/assets/img/og/og-default.jpg">
  <meta name="twitter:image:alt" content="Authentic Wellness — physician-prescribed telehealth programs (branded preview).">
"""
    return text.replace(
        '<link rel="canonical"',
        block + '  <link rel="canonical"',
        1,
    )


def ensure_robots(text: str, rel: pathlib.Path) -> str:
    if re.search(r'<meta\s+name="robots"\s', text, re.I):
        return text
    if rel.as_posix() == "404.html":
        return text
    insert = '  <meta name="robots" content="index, follow">\n'
    m = re.search(r'(<meta\s+name="viewport"[^>]*>\s*\n)', text, re.I)
    if m:
        return text.replace(m.group(1), m.group(1) + insert, 1)
    m2 = re.search(r"(<meta\s+charset=\"UTF-8\">\s*\n)", text, re.I)
    if m2:
        return text.replace(m2.group(1), m2.group(1) + insert, 1)
    return text


def main() -> None:
    for path in AW_HTML:
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        text = text.replace(OLD_LOGO, NEW_LOGO)
        text = fix_focus_calm(text, rel)
        text = enrich_cognitive_head(text, rel)
        text = normalize_title(text)
        text = ensure_robots(text, rel)
        text = inject_breadcrumb(text, rel)
        text = inject_product(text, rel)
        path.write_text(text, encoding="utf-8")
        print(rel)


if __name__ == "__main__":
    main()
