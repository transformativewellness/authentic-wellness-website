#!/usr/bin/env python3
"""One-off generator for programs/*.html and blog/*.html. Run from repo root: python3 scripts/generate-aw-pages.py"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://transformativewellness.github.io/authentic-wellness-website"

# slug -> (title, h1, tagline, monthly_str, quarterly_str|None, what_paras, who_bullets, injectable_note, extra_compliance, faqs, related)
# monthly_str like "$249/mo" or "from $299/mo (starter)"
PROGRAMS: dict[str, dict] = {}


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def nav_sub() -> str:
    """Nav for pages under /programs/ — relative links."""
    return """
      <div class="nav-links">
        <div class="nav-item nav-dropdown">
          <button type="button" class="nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true" id="programs-menu-btn">Programs <span class="nav-caret" aria-hidden="true"></span></button>
          <div class="nav-dropdown-menu" id="programs-menu" role="menu" aria-label="Program categories">
            <div class="nav-dropdown-grid">
              <div class="nav-dropdown-col">
                <span class="nav-dropdown-heading">Performance</span>
                <a href="perform.html" role="menuitem">Perform</a>
                <a href="renew.html" role="menuitem">Renew</a>
                <a href="recovery.html" role="menuitem">Recovery</a>
                <a href="tesamorelin.html" role="menuitem">Tesamorelin</a>
              </div>
              <div class="nav-dropdown-col">
                <span class="nav-dropdown-heading">Longevity</span>
                <a href="longevity.html" role="menuitem">NAD+</a>
                <a href="epithalon.html" role="menuitem">Epithalon</a>
                <a href="mots-c.html" role="menuitem">MOTS-C</a>
                <a href="methylene-blue.html" role="menuitem">Methylene Blue</a>
                <a href="ghk-cu.html" role="menuitem">GHK-Cu</a>
              </div>
              <div class="nav-dropdown-col">
                <span class="nav-dropdown-heading">Cognitive</span>
                <a href="focus-calm.html" role="menuitem">Focus &amp; Calm</a>
                <span class="nav-dropdown-heading nav-dropdown-heading-spaced">Weight loss</span>
                <a href="glp1-sema.html" role="menuitem">GLP-1 Sema</a>
                <a href="glp1-tirz.html" role="menuitem">GLP-1 Tirz</a>
                <a href="ldn.html" role="menuitem">LDN</a>
                <a href="metformin.html" role="menuitem">Metformin</a>
              </div>
              <div class="nav-dropdown-col">
                <span class="nav-dropdown-heading">Sexual wellness</span>
                <a href="pt-141.html" role="menuitem">PT-141</a>
                <a href="ed-sildenafil.html" role="menuitem">ED Sildenafil</a>
                <a href="ed-tadalafil.html" role="menuitem">ED Tadalafil</a>
                <span class="nav-dropdown-heading nav-dropdown-heading-spaced">Hair &amp; skin</span>
                <a href="male-hair-loss.html" role="menuitem">Male hair loss</a>
                <a href="female-hair-loss.html" role="menuitem">Female hair loss</a>
                <a href="discovery.html" class="nav-dropdown-discovery" role="menuitem">Discovery Consult ($49)</a>
              </div>
            </div>
          </div>
        </div>
        <a href="../blog/index.html">Blog</a>
        <a href="../how-it-works.html">How It Works</a>
        <a href="../about.html">About</a>
        <a href="../faq.html">FAQ</a>
        <a href="../contact.html">Contact</a>
        <div class="nav-cta">
          <a href="../how-it-works.html#start" class="btn btn-primary" style="padding:0.625rem 1.5rem;font-size:0.85rem;">See If You Qualify</a>
          <p class="cta-microcopy">Full refund if not approved by your physician.</p>
        </div>
      </div>"""


def nav_root() -> str:
    return nav_sub().replace('href="', 'href="programs/').replace('href="programs/../', 'href="').replace('href="programs/perform.html"', 'href="programs/perform.html"').replace(
        'href="programs/../blog/', 'href="blog/'
    ).replace(
        'href="programs/../how-it-works.html"', 'href="how-it-works.html"'
    ).replace(
        'href="programs/../about.html"', 'href="about.html"'
    ).replace(
        'href="programs/../faq.html"', 'href="faq.html"'
    )


# Fix nav_root: the naive replace breaks. Build explicitly.
def nav_root_explicit() -> str:
    return """
      <div class="nav-links">
        <div class="nav-item nav-dropdown">
          <button type="button" class="nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true" id="programs-menu-btn">Programs <span class="nav-caret" aria-hidden="true"></span></button>
          <div class="nav-dropdown-menu" id="programs-menu" role="menu" aria-label="Program categories">
            <div class="nav-dropdown-grid">
              <div class="nav-dropdown-col">
                <span class="nav-dropdown-heading">Performance</span>
                <a href="programs/perform.html" role="menuitem">Perform</a>
                <a href="programs/renew.html" role="menuitem">Renew</a>
                <a href="programs/recovery.html" role="menuitem">Recovery</a>
                <a href="programs/tesamorelin.html" role="menuitem">Tesamorelin</a>
              </div>
              <div class="nav-dropdown-col">
                <span class="nav-dropdown-heading">Longevity</span>
                <a href="programs/longevity.html" role="menuitem">NAD+</a>
                <a href="programs/epithalon.html" role="menuitem">Epithalon</a>
                <a href="programs/mots-c.html" role="menuitem">MOTS-C</a>
                <a href="programs/methylene-blue.html" role="menuitem">Methylene Blue</a>
                <a href="programs/ghk-cu.html" role="menuitem">GHK-Cu</a>
              </div>
              <div class="nav-dropdown-col">
                <span class="nav-dropdown-heading">Cognitive</span>
                <a href="programs/focus-calm.html" role="menuitem">Focus &amp; Calm</a>
                <span class="nav-dropdown-heading nav-dropdown-heading-spaced">Weight loss</span>
                <a href="programs/glp1-sema.html" role="menuitem">GLP-1 Sema</a>
                <a href="programs/glp1-tirz.html" role="menuitem">GLP-1 Tirz</a>
                <a href="programs/ldn.html" role="menuitem">LDN</a>
                <a href="programs/metformin.html" role="menuitem">Metformin</a>
              </div>
              <div class="nav-dropdown-col">
                <span class="nav-dropdown-heading">Sexual wellness</span>
                <a href="programs/pt-141.html" role="menuitem">PT-141</a>
                <a href="programs/ed-sildenafil.html" role="menuitem">ED Sildenafil</a>
                <a href="programs/ed-tadalafil.html" role="menuitem">ED Tadalafil</a>
                <span class="nav-dropdown-heading nav-dropdown-heading-spaced">Hair &amp; skin</span>
                <a href="programs/male-hair-loss.html" role="menuitem">Male hair loss</a>
                <a href="programs/female-hair-loss.html" role="menuitem">Female hair loss</a>
                <a href="programs/discovery.html" class="nav-dropdown-discovery" role="menuitem">Discovery Consult ($49)</a>
              </div>
            </div>
          </div>
        </div>
        <a href="blog/index.html">Blog</a>
        <a href="how-it-works.html">How It Works</a>
        <a href="about.html">About</a>
        <a href="faq.html">FAQ</a>
        <a href="contact.html">Contact</a>
        <div class="nav-cta">
          <a href="how-it-works.html#start" class="btn btn-primary" style="padding:0.625rem 1.5rem;font-size:0.85rem;">See If You Qualify</a>
          <p class="cta-microcopy">Full refund if not approved by your physician.</p>
        </div>
      </div>"""


def nav_blog() -> str:
    return nav_root_explicit().replace('href="blog/index.html"', 'href="index.html"')


def footer_sub() -> str:
    return f"""
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <a href="../index.html" class="footer-mark" aria-label="Authentic Wellness home">
            <img src="../logo-light.svg" width="220" height="34" alt="Authentic Wellness">
          </a>
          <p style="margin-top:0.5rem;">Physician-prescribed performance and longevity programs — backed by science, built for people who take their health seriously.</p>
          <p style="margin-top:0.75rem;">info@authenticwellness.com</p>
        </div>
        <div>
          <p class="footer-col-title">Programs</p>
          <p class="compliance-disclaimer" style="margin-bottom:0.75rem;">Compounded medications are not FDA-approved. Prepared by licensed 503A/503B pharmacies.</p>
          <div class="footer-links">
            <a href="perform.html">Perform Program</a>
            <a href="longevity.html">Longevity Program</a>
            <a href="../programs.html">All programs</a>
          </div>
        </div>
        <div>
          <p class="footer-col-title">Company</p>
          <div class="footer-links">
            <a href="../how-it-works.html">How It Works</a>
            <a href="../about.html">About</a>
            <a href="../faq.html">FAQ</a>
            <a href="../blog/index.html">Blog</a>
          </div>
        </div>
        <div>
          <p class="footer-col-title">Legal</p>
          <div class="footer-links">
            <a href="../privacy.html">Privacy Policy</a>
            <a href="../terms.html">Terms of Service</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 Authentic Wellness — Evolving Wellness LLC. All rights reserved.</p>
        <p>Medical Director: Joshua Yang M.D. Inc (Dr. Joshua Yang, MD) · CA License A167038 · NPI 1851549232</p>
        <p>Physician-prescribed programs. Medications sourced from licensed 503A/503B compounding pharmacies.</p>
        <p>Compounded medications are not FDA-approved. Prepared by licensed 503A/503B pharmacies. Results may vary. Physician approval required.</p>
        <p>Authentic Wellness is not a medical practice. We facilitate access to independent licensed physicians via Qualiphy.</p>
        <p>Authentic Wellness is affiliated with <a href="https://transformativemedspa.com">Transformative Wellness</a> in Vista, CA.</p>
        <p>In-clinic programs available at Transformative Wellness — Vista, CA → <a href="https://transformativemedspa.com">transformativemedspa.com</a></p>
      </div>
    </div>
  </footer>

  <div id="cookie-banner" class="cookie-banner" role="region" aria-label="Cookie notice">
    <div class="cookie-inner">
      <p>We use essential cookies to run this site and optional analytics to improve it. By continuing, you agree to our <a href="../privacy.html">Privacy Policy</a>.</p>
      <button type="button" id="cookie-dismiss" class="cookie-btn">Accept</button>
    </div>
  </div>

  <script src="../js/main.js"></script>"""


def footer_root() -> str:
    return footer_sub().replace("../", "").replace('href="index.html"', 'href="index.html"').replace(
        'src="logo-light.svg"', 'src="logo-light.svg"'
    )
    # broken - footer_sub uses ../ - for root we need different. Build footer_root separately.


def footer_root_explicit() -> str:
    return """
  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <a href="index.html" class="footer-mark" aria-label="Authentic Wellness home">
            <img src="logo-light.svg" width="220" height="34" alt="Authentic Wellness">
          </a>
          <p style="margin-top:0.5rem;">Physician-prescribed performance and longevity programs — backed by science, built for people who take their health seriously.</p>
          <p style="margin-top:0.75rem;">info@authenticwellness.com</p>
        </div>
        <div>
          <p class="footer-col-title">Programs</p>
          <p class="compliance-disclaimer" style="margin-bottom:0.75rem;">Compounded medications are not FDA-approved. Prepared by licensed 503A/503B pharmacies.</p>
          <div class="footer-links">
            <a href="programs/perform.html">Perform Program</a>
            <a href="programs/longevity.html">Longevity Program</a>
            <a href="programs.html">All programs</a>
          </div>
        </div>
        <div>
          <p class="footer-col-title">Company</p>
          <div class="footer-links">
            <a href="how-it-works.html">How It Works</a>
            <a href="about.html">About</a>
            <a href="faq.html">FAQ</a>
            <a href="contact.html">Contact</a>
            <a href="blog/index.html">Blog</a>
          </div>
        </div>
        <div>
          <p class="footer-col-title">Legal</p>
          <div class="footer-links">
            <a href="privacy.html">Privacy Policy</a>
            <a href="terms.html">Terms of Service</a>
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; 2026 Authentic Wellness — Evolving Wellness LLC. All rights reserved.</p>
        <p>Medical Director: Joshua Yang M.D. Inc (Dr. Joshua Yang, MD) · CA License A167038 · NPI 1851549232</p>
        <p>Physician-prescribed programs. Medications sourced from licensed 503A/503B compounding pharmacies.</p>
        <p>Compounded medications are not FDA-approved. Prepared by licensed 503A/503B pharmacies. Results may vary. Physician approval required.</p>
        <p>Authentic Wellness is not a medical practice. We facilitate access to independent licensed physicians via Qualiphy.</p>
        <p>Authentic Wellness is affiliated with <a href="https://transformativemedspa.com">Transformative Wellness</a> in Vista, CA.</p>
        <p>In-clinic programs available at Transformative Wellness — Vista, CA → <a href="https://transformativemedspa.com">transformativemedspa.com</a></p>
      </div>
    </div>
  </footer>

  <div id="cookie-banner" class="cookie-banner" role="region" aria-label="Cookie notice">
    <div class="cookie-inner">
      <p>We use essential cookies to run this site and optional analytics to improve it. By continuing, you agree to our <a href="privacy.html">Privacy Policy</a>.</p>
      <button type="button" id="cookie-dismiss" class="cookie-btn">Accept</button>
    </div>
  </div>

  <script src="js/main.js"></script>"""


def footer_blog() -> str:
    # Blog pages live in /blog/; program deep links must include ../programs/
    return (
        footer_sub()
        .replace('href="perform.html"', 'href="../programs/perform.html"')
        .replace('href="longevity.html"', 'href="../programs/longevity.html"')
    )


def faq_schema(faqs: list[tuple[str, str]]) -> str:
    entities = []
    for q, a in faqs:
        entities.append(
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
        )
    return json.dumps(
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities},
        indent=2,
    )


def build_program_page(
    slug: str,
    meta: dict,
    nav_html: str,
    footer_html: str,
    path_prefix: str,
) -> str:
    title = meta["title"]
    h1 = meta["h1"]
    tagline = meta["tagline"]
    monthly = meta["monthly"]
    quarterly = meta.get("quarterly")
    what = meta["what"]
    who = meta["who"]
    inject_note = meta.get("inject_note", False)
    extra = meta.get("extra", "")
    faqs = meta["faqs"]
    related = meta["related"]
    price_badge = meta.get("price_badge", monthly)
    hero_micro = meta.get("hero_cta_microcopy", "Full refund if not approved by your physician.")
    pricing_micro = meta.get("pricing_cta_microcopy", hero_micro)
    compliance_bar = meta.get(
        "compliance_bar",
        "Compounded medications are not FDA-approved. Prepared by licensed 503A/503B pharmacies. Results may vary. Physician approval required.",
    )
    included_lines = meta.get(
        "included_lines",
        [
            "Virtual physician consultation",
            "3-month supply",
            "Ships from licensed 503A/503B pharmacy",
            "Ongoing support",
        ],
    )
    compounded_line = meta.get(
        "compounded_footer_line",
        "Compounded medications are not FDA-approved. Prepared by licensed 503A/503B pharmacies.",
    )

    what_html = "".join(f"<p>{esc(p)}</p>" for p in what)
    who_html = "".join(f"<li>{esc(b)}</li>" for b in who)
    faq_html = ""
    for i, (q, a) in enumerate(faqs):
        faq_html += f"""
        <div class="faq-item">
          <button class="faq-question" id="fq-{slug}-{i}" type="button">{esc(q)}</button>
          <div class="faq-answer">{esc(a)}</div>
        </div>"""

    related_html = ""
    for rslug, rtitle, rprice in related:
        related_html += f"""
        <a href="{rslug}.html" class="related-card">
          <h4>{esc(rtitle)}</h4>
          <p class="related-card-price">{esc(rprice)}</p>
          <span class="related-card-link">View program</span>
        </a>"""

    quarterly_block = ""
    if quarterly:
        quarterly_block = f"""
          <p class="program-page-quarterly">Quarterly: <strong>{quarterly}</strong> (save 10%)</p>"""

    inject_block = ""
    if inject_note:
        inject_block = """
      <section class="section-white">
        <div class="container" style="max-width:720px;">
          <p class="program-note text-center">Prefer not to inject? Nasal spray and sublingual options available — ask during your consultation.</p>
        </div>
      </section>"""

    extra_block = f'<p class="compliance-disclaimer text-center">{esc(extra)}</p>' if extra else ""

    included_html = "".join(f"<li>{esc(line)}</li>" for line in included_lines)

    what_compliance = (
        ""
        if meta.get("skip_compounded_what_line")
        else f'<p class="compliance-disclaimer">{esc(compounded_line)}</p>'
    )

    og_url = f"{BASE_URL}/programs/{slug}.html"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)} | Authentic Wellness</title>
  <meta name="description" content="{esc(tagline)} Physician-prescribed program. Virtual consultation and pharmacy shipping.">
  <link rel="canonical" href="{og_url}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(title)} | Authentic Wellness">
  <meta property="og:description" content="{esc(tagline)}">
  <meta property="og:url" content="{og_url}">
  <meta property="og:image" content="{BASE_URL}/logo-mark.svg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="../favicon.ico" sizes="any">
  <link rel="icon" href="../logo-mark.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Playfair+Display:wght@400;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/style.css">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "MedicalBusiness",
    "name": "Authentic Wellness",
    "url": "{og_url}",
    "image": "{BASE_URL}/logo-mark.svg",
    "logo": "{BASE_URL}/logo-dark.svg",
    "email": "info@authenticwellness.com"
  }}
  </script>
  <script type="application/ld+json">
  {faq_schema(faqs)}
  </script>
</head>
<body class="program-subpage">

  <nav class="navbar">
    <div class="container nav-inner">
      <a href="../index.html" class="nav-logo" aria-label="Authentic Wellness home">
        <img src="../logo-dark.svg" width="220" height="34" alt="Authentic Wellness">
      </a>
{nav_html}
      <button class="nav-toggle" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>

  <header class="program-page-hero">
    <div class="container">
      <p class="program-page-kicker">Authentic Wellness</p>
      <h1>{esc(h1)}</h1>
      <p class="program-page-tagline">{esc(tagline)}</p>
      <div class="price-badge-amber">{esc(price_badge)}</div>
      <a href="../how-it-works.html#start" class="btn btn-primary program-page-cta">See If You Qualify</a>
      <p class="cta-microcopy program-page-hero-micro">{esc(hero_micro)}</p>
      <p class="hero-tagline program-page-aw-tagline">Optimized from the inside out.</p>
    </div>
  </header>

  <section class="section-linen">
    <div class="container program-page-section">
      <h2>What it is</h2>
      {what_html}
      {what_compliance}
    </div>
  </section>

  <section class="section-white">
    <div class="container program-page-section">
      <h2>Who it&apos;s for</h2>
      <ul class="program-page-bullets">
        {who_html}
      </ul>
    </div>
  </section>

  <section class="section-linen">
    <div class="container program-page-section">
      <h2>What&apos;s included</h2>
      <ul class="program-page-checklist">
        {included_html}
      </ul>
    </div>
  </section>

  <section class="section-white">
    <div class="container program-page-section">
      <h2>Expected timeline</h2>
      <ul class="program-page-timeline">
        <li><strong>Weeks 1–2:</strong> Adjustment to routine; your care team checks in.</li>
        <li><strong>Weeks 3–4:</strong> Many people notice early shifts in how they feel or perform.</li>
        <li><strong>Weeks 8–12:</strong> Deeper effects often show up as your protocol matures — individual responses vary.</li>
      </ul>
      <p class="compliance-disclaimer">Physician approval required. Results may vary.</p>
    </div>
  </section>

  <section class="section-linen program-page-pricing">
    <div class="container text-center">
      <h2>Pricing</h2>
      <p class="program-page-price-large">{esc(monthly)}</p>
      {quarterly_block}
      <a href="../how-it-works.html#start" class="btn btn-primary">See If You Qualify</a>
      <p class="cta-microcopy">{esc(pricing_micro)}</p>
    </div>
  </section>
{inject_block}

  {f'<section class="section-white"><div class="container">{extra_block}</div></section>' if extra_block else ''}

  <section class="faq-strip section-linen">
    <div class="container" style="max-width:780px;">
      <h2 class="text-center">Common questions</h2>
      {faq_html}
    </div>
  </section>

  <section class="section-white">
    <div class="container">
      <h2 class="text-center">Related programs</h2>
      <div class="related-programs-grid">
        {related_html}
      </div>
    </div>
  </section>

  <section class="program-compliance-bar">
    <div class="container">
      <p>{esc(compliance_bar)}</p>
    </div>
  </section>

{footer_html}
</body>
</html>"""


# --- Related program cards (slug -> three slugs) ---
RELATED_SLUGS: dict[str, list[str]] = {
    "perform": ["renew", "recovery", "tesamorelin"],
    "renew": ["perform", "metformin", "discovery"],
    "longevity": ["metformin", "epithalon", "mots-c"],
    "glp1-sema": ["glp1-tirz", "metformin", "ldn"],
    "glp1-tirz": ["glp1-sema", "metformin", "ldn"],
    "ldn": ["metformin", "longevity", "focus-calm"],
    "metformin": ["longevity", "ldn", "discovery"],
    "recovery": ["perform", "renew", "tesamorelin"],
    "epithalon": ["longevity", "ghk-cu", "mots-c"],
    "mots-c": ["longevity", "methylene-blue", "perform"],
    "focus-calm": ["methylene-blue", "longevity", "ldn"],
    "methylene-blue": ["longevity", "focus-calm", "mots-c"],
    "ed-sildenafil": ["ed-tadalafil", "pt-141", "discovery"],
    "ed-tadalafil": ["ed-sildenafil", "pt-141", "discovery"],
    "male-hair-loss": ["female-hair-loss", "ghk-cu", "discovery"],
    "female-hair-loss": ["male-hair-loss", "ghk-cu", "discovery"],
    "pt-141": ["ed-tadalafil", "ed-sildenafil", "discovery"],
    "ghk-cu": ["epithalon", "male-hair-loss", "longevity"],
    "discovery": ["perform", "longevity", "glp1-sema"],
    "tesamorelin": ["perform", "renew", "recovery"],
}

CARD_NAMES: dict[str, tuple[str, str]] = {
    "perform": ("Perform Program", "$249/mo"),
    "renew": ("Renew Program", "$229/mo"),
    "longevity": ("Longevity Program", "$279/mo"),
    "glp1-sema": ("GLP-1 Sema Program", "from $299/mo"),
    "glp1-tirz": ("GLP-1 Tirz Program", "from $349/mo"),
    "ldn": ("LDN Program", "$129/mo"),
    "metformin": ("Metformin Program", "$89/mo"),
    "recovery": ("Recovery Add-on", "$149/mo"),
    "epithalon": ("Epithalon Program", "$149/mo"),
    "mots-c": ("MOTS-C Program", "$229/mo"),
    "focus-calm": ("Focus & Calm Protocol", "$199/mo"),
    "methylene-blue": ("Methylene Blue Program", "$179/mo"),
    "ed-sildenafil": ("ED Sildenafil Program", "$129/mo"),
    "ed-tadalafil": ("ED Tadalafil Program", "$179/mo"),
    "male-hair-loss": ("Male Hair Loss Program", "$199/mo"),
    "female-hair-loss": ("Female Hair Loss Program", "$179/mo"),
    "pt-141": ("PT-141 Program", "$149/mo"),
    "ghk-cu": ("GHK-Cu Program", "$179/mo"),
    "discovery": ("Discovery Consult", "$49"),
    "tesamorelin": ("Tesamorelin Program", "$199/mo"),
}


def fq(q, a):
    return (q, a)


META: dict[str, dict] = {
    "perform": {
        "title": "Perform Program",
        "h1": "The Perform Program",
        "tagline": "Optimize growth hormone release for lean muscle, faster recovery, and performance.",
        "monthly": "$249/mo",
        "quarterly": "$672/quarter",
        "price_badge": "$249/mo",
        "what": [
            "The Perform Program is a physician-prescribed plan built around a well-studied growth-hormone secretagogue pair. It is designed for adults who want structured support for recovery, body composition, and training quality.",
            "Your independent physician reviews your history and goals in a virtual consultation. If appropriate, medication is prepared by a licensed compounding pharmacy and shipped to you.",
            "This page is educational. Only a licensed physician can decide whether this program is appropriate for you.",
        ],
        "who": [
            "Athletes and active adults who want faster recovery between sessions",
            "People noticing muscle loss or slower recovery with age",
            "Anyone wanting better sleep and body composition support alongside training",
            "Patients who want natural growth-hormone pathway support without synthetic hGH",
        ],
        "inject_note": True,
        "faqs": [
            fq("How is the Perform Program prescribed?", "You complete a virtual physician consultation. An independent licensed physician reviews your information and determines whether a prescription is appropriate."),
            fq("How long is a typical supply?", "Many plans are written around a 90-day supply, but your physician determines what is appropriate for you."),
            fq("Is this the same as synthetic hGH?", "No. This program works through your body's natural signaling pathways. Your physician can explain what that means for you."),
            fq("Can I travel with my medication?", "Follow the pharmacy instructions included with your shipment and ask your care team if you have specific travel questions."),
            fq("What if I am not approved?", "If your physician does not approve care, you may qualify for a full refund. See our Terms of Service for details."),
        ],
    },
    "renew": {
        "title": "Renew Program",
        "h1": "The Renew Program",
        "tagline": "Support natural growth hormone production for sleep, recovery, and vitality.",
        "monthly": "$229/mo",
        "quarterly": "$618/quarter",
        "price_badge": "$229/mo",
        "what": [
            "Renew is a physician-prescribed program centered on a growth-hormone-releasing peptide analog. It is often chosen by adults who want a gentler entry point focused on sleep, recovery, and daily energy.",
            "Care is coordinated through a virtual consultation, and medications are dispensed by a licensed compounding pharmacy when prescribed.",
            "Outcomes depend on the individual. Your physician helps you set realistic expectations.",
        ],
        "who": [
            "Adults 30+ who feel their energy or recovery is not what it used to be",
            "People with sleep quality they want to improve",
            "Those interested in longevity-style support with medical oversight",
            "Patients seeking a gentler growth-hormone secretagogue option",
        ],
        "inject_note": True,
        "faqs": [
            fq("How is Renew different from Perform?", "Both are physician-prescribed peptide programs with different prescribing considerations. Your physician can recommend the better fit."),
            fq("How soon might I notice sleep changes?", "Some people notice shifts within a couple of weeks; others take longer. Responses vary."),
            fq("Do I need labs?", "Your physician will tell you if labs or other steps are needed before prescribing."),
            fq("Is Renew appropriate for athletes?", "That depends on your health history and goals. Your physician makes the decision."),
            fq("What does compounded mean?", "Compounded medications are prepared by a licensed pharmacy for an individual patient. They are not FDA-approved."),
        ],
    },
    "longevity": {
        "title": "Longevity Program (NAD+)",
        "h1": "The Longevity Program",
        "tagline": "Restore cellular energy and support healthy aging at the molecular level.",
        "monthly": "$279/mo",
        "quarterly": "$753/quarter",
        "price_badge": "$279/mo",
        "what": [
            "The Longevity Program focuses on NAD+, a molecule involved in cellular energy chemistry. It is popular among people who want structured longevity support with physician oversight.",
            "If prescribed, your medication ships from a licensed compounding pharmacy with instructions and care-team support.",
            "This program does not replace healthy habits; it is meant to complement them when your physician agrees it is appropriate.",
        ],
        "who": [
            "People who feel mentally foggy or low on steady energy",
            "Anyone focused on long-term health optimization with medical guidance",
            "Athletes interested in cellular recovery support",
            "Patients who want evidence-informed longevity options",
        ],
        "inject_note": True,
        "faqs": [
            fq("Why is NAD+ discussed for longevity?", "NAD+ plays a role in cellular energy pathways. Research is ongoing; your physician can contextualize what is known today."),
            fq("Is NAD+ a stimulant?", "It is not a stimulant in the caffeine sense. Ask your physician how it may feel for you."),
            fq("How is NAD+ supplied?", "Formulation and route depend on your prescription and pharmacy. Your shipment includes instructions."),
            fq("Can I combine Longevity with other AW programs?", "Stacking depends on medical judgment. Your physician will advise."),
            fq("What if I am not a candidate?", "If your physician does not approve care, you may qualify for a full refund. See our Terms of Service for details."),
        ],
    },
    "glp1-sema": {
        "title": "GLP-1 Sema Program",
        "h1": "Semaglutide GLP-1 Program",
        "tagline": "Physician-prescribed weight loss — sustainable, clinically proven, ships to your door.",
        "monthly": "from $299/mo (starter) · $349 (mid) · $399 (high)",
        "quarterly": None,
        "price_badge": "from $299/mo",
        "what": [
            "This program offers physician-prescribed GLP-1 support using compounded semaglutide when appropriate. Pricing reflects common dose tiers; your actual price follows your physician-approved plan.",
            "You complete a virtual consultation. If a prescription is issued, your pharmacy prepares patient-specific medication and ships it to you.",
            "Weight change is individual. This program works best alongside nutrition, movement, sleep, and follow-up with your physician.",
        ],
        "who": [
            "Adults with elevated BMI who want structured medical weight support",
            "People who have struggled with diet and exercise alone",
            "Patients who want telehealth convenience and pharmacy delivery",
            "Adults interested in weekly injection plans when prescribed",
        ],
        "inject_note": True,
        "extra": "Price adjusts with physician-prescribed dose.",
        "faqs": [
            fq("Why are there starter, mid, and high tiers?", "Tiers reflect common dosing bands used in prescribing. Your physician selects what is appropriate for you."),
            fq("Is compounded semaglutide FDA-approved?", "Compounded medications are not FDA-approved. They are prepared by licensed 503A/503B pharmacies."),
            fq("How often do I check in?", "Follow-up timing depends on your plan. Your physician and care team will outline what to expect."),
            fq("What side effects are common?", "Many GLP-1 plans can cause GI symptoms early on. Report concerning symptoms to your physician."),
            fq("Can I switch programs later?", "Your physician can discuss whether another plan is a better fit over time."),
        ],
    },
    "glp1-tirz": {
        "title": "GLP-1 Tirz Program",
        "h1": "Tirzepatide GLP-1 Program",
        "tagline": "Dual-action weight loss — the next generation of GLP-1 therapy.",
        "monthly": "from $349/mo (starter) · $399 (mid) · $449 (high)",
        "quarterly": None,
        "price_badge": "from $349/mo",
        "what": [
            "This program uses compounded tirzepatide when prescribed. It is selected for some patients based on medical history, goals, and physician judgment.",
            "Tirzepatide acts on more than one incretin-related pathway compared with semaglutide alone. Your physician can explain what that means in plain language.",
            "Compounded medications are prepared for you individually and are not FDA-approved.",
        ],
        "who": [
            "Adults seeking physician-led weight support who may benefit from tirzepatide",
            "Patients who want structured follow-up and dose adjustments over time",
            "People who prefer home delivery from a licensed pharmacy",
            "Adults who understand GLP-1 therapy requires consistency and monitoring",
        ],
        "inject_note": True,
        "extra": "Price adjusts with physician-prescribed dose. Dual GLP-1/GIP mechanism.",
        "faqs": [
            fq("How is tirzepatide different from semaglutide?", "They are not the same molecule and may feel different. Your physician chooses based on your evaluation."),
            fq("Is compounded tirzepatide FDA-approved?", "No. Compounded medications are not FDA-approved. Prepared by licensed 503A/503B pharmacies."),
            fq("Do I need labs?", "Sometimes. Your physician will tell you if labs are part of your plan."),
            fq("What if I miss a dose?", "Follow your pharmacy instructions and ask your physician for personalized guidance."),
            fq("Can I pause my plan?", "Membership and fulfillment depend on your enrollment terms. Ask our care team for help."),
        ],
    },
    "ldn": {
        "title": "LDN Program",
        "h1": "Low Dose Naltrexone (LDN) Program",
        "tagline": "Immune modulation and metabolic support — emerging research for longevity and wellness.",
        "monthly": "$129/mo",
        "quarterly": "$348/quarter",
        "price_badge": "$129/mo",
        "what": [
            "Low dose naltrexone (LDN) is a physician-prescribed option some adults explore for immune balance and wellness goals. Evidence and use cases continue to evolve.",
            "Dosing is typically far below standard naltrexone strengths used for other indications. Your physician determines whether LDN is appropriate for you.",
            "LDN is not a promise of any specific outcome; responses vary widely.",
        ],
        "who": [
            "People with autoimmune conditions they want to discuss with a licensed physician",
            "Patients seeking immune optimization with structured medical oversight",
            "Adults interested in longevity medicine conversations that include LDN when appropriate",
            "Patients who have not found sufficient support with other approaches and want a careful review",
        ],
        "inject_note": True,
        "faqs": [
            fq("What doses are common?", "Many LDN plans use very low nightly doses, but your prescription is individualized."),
            fq("Can LDN cause vivid dreams?", "Some people notice sleep changes. Tell your physician if anything feels off."),
            fq("Is LDN compounded?", "It may be, depending on your prescription and pharmacy. Compounded medications are not FDA-approved."),
            fq("Do I take it with food?", "Follow your prescription label and physician guidance."),
            fq("How do I know if LDN is right for me?", "Only your physician can decide after a consultation."),
        ],
    },
    "metformin": {
        "title": "Metformin Longevity Program",
        "h1": "Metformin Longevity Program",
        "tagline": "The longevity medication — decades of safety data, emerging anti-aging evidence.",
        "monthly": "$89/mo",
        "quarterly": "$240/quarter",
        "price_badge": "$89/mo",
        "what": [
            "Metformin is a prescription medication with a long history of use for metabolic support. Some longevity-focused patients discuss it with physicians as part of a broader plan.",
            "This program is only for people who are appropriate candidates after a virtual consultation.",
            "It can be a practical entry program to combine with other AW plans when your physician agrees.",
        ],
        "who": [
            "Adults interested in metabolic health and prevention-focused conversations",
            "People with insulin sensitivity concerns they want to discuss with a physician",
            "Longevity-focused patients who want an approachable monthly option",
            "Patients looking for a simple oral protocol when prescribed",
        ],
        "inject_note": False,
        "extra": "Lowest price point — great entry program to stack with others when appropriate.",
        "faqs": [
            fq("Is metformin compounded?", "Your prescription and pharmacy determine formulation. Ask your physician."),
            fq("Who should not use metformin?", "There are medical reasons to avoid metformin. Your physician screens for those."),
            fq("Do I need labs?", "Your physician may order labs depending on your history."),
            fq("Can I use metformin with a GLP-1 program?", "Only your physician can decide if combined prescribing is appropriate."),
            fq("What will I receive?", "Your prescription and pharmacy determine the exact product. Compounded medications are not FDA-approved. Prepared by licensed 503A/503B pharmacies."),
        ],
    },
    "recovery": {
        "title": "Recovery Add-on",
        "h1": "Recovery Add-on",
        "tagline": "Accelerate tissue repair and recovery — designed to stack with performance programs.",
        "monthly": "$149/mo add-on",
        "quarterly": None,
        "price_badge": "$149/mo add-on",
        "included_lines": [
            "Virtual physician consultation for add-on eligibility",
            "Monthly add-on supply when prescribed with a qualifying performance program",
            "Ships from licensed 503A/503B pharmacy",
            "Ongoing support from our care team",
        ],
        "what": [
            "Recovery is an add-on plan built around a peptide commonly discussed for tissue recovery. It is intended to complement performance programs when a physician agrees.",
            "Add-ons still require physician approval and pharmacy dispensing.",
            "Availability can change with regulatory updates.",
        ],
        "who": [
            "Active adults who want extra recovery support alongside training",
            "People recovering from soft-tissue irritation who want a physician-guided option",
            "Patients already in a performance program who may benefit from stacking",
            "Anyone who wants pharmacy-prepared medication with clear instructions",
        ],
        "inject_note": True,
        "extra": "Availability subject to current regulatory status. Your physician will advise.",
        "faqs": [
            fq("Can I buy Recovery without another program?", "Recovery is positioned as an add-on; your physician decides what is appropriate."),
            fq("Is BPC-157 always available?", "Regulatory status can change. Your physician will advise based on current rules."),
            fq("How do I inject?", "Your shipment includes instructions; our care team can help with logistics questions."),
            fq("Can I travel with it?", "Follow pharmacy guidance and physician advice."),
            fq("What if I am not approved?", "If your physician does not approve care, you may qualify for a full refund. See our Terms of Service for details."),
        ],
    },
    "epithalon": {
        "title": "Epithalon Program",
        "h1": "Epithalon Anti-Aging Program",
        "tagline": "Telomere support and cellular anti-aging — one of longevity medicine's most studied peptides.",
        "monthly": "$149/mo",
        "quarterly": "$402/quarter",
        "price_badge": "$149/mo",
        "what": [
            "Epithalon is a peptide frequently discussed in longevity circles. This program offers physician-prescribed access when appropriate, with pharmacy preparation.",
            "Research is ongoing; this page is not a claim of specific anti-aging results.",
            "Your physician helps you understand realistic expectations.",
        ],
        "who": [
            "Adults focused on longevity and cellular aging topics",
            "People who want peptide options beyond NAD+",
            "Patients who prefer structured medical oversight",
            "Anyone curious about epithalon with a licensed physician guiding decisions",
        ],
        "inject_note": True,
        "faqs": [
            fq("How is epithalon used?", "Your prescription defines dosing and schedule. Follow your pharmacy label."),
            fq("Is epithalon FDA-approved?", "Compounded medications are not FDA-approved. Prepared by licensed 503A/503B pharmacies."),
            fq("Can I combine epithalon with NAD+?", "Only your physician can decide."),
            fq("What should I expect in the first month?", "Responses vary. Some people notice subtle shifts; others do not."),
            fq("How do I qualify?", "Complete a virtual consultation for physician review."),
        ],
    },
    "mots-c": {
        "title": "MOTS-C Program",
        "h1": "MOTS-C Metabolic Program",
        "tagline": "Mitochondrial optimization and metabolic regulation — the exercise-mimicking peptide.",
        "monthly": "$229/mo",
        "quarterly": "$618/quarter",
        "price_badge": "$229/mo",
        "what": [
            "MOTS-C is a mitochondrial-derived peptide discussed for metabolic fitness and energy regulation. It is sometimes called an exercise-mimicking peptide in longevity conversations.",
            "Access is prescription-only through a virtual physician consultation.",
            "Outcomes vary; this is not a guarantee of performance gains.",
        ],
        "who": [
            "Adults interested in metabolic resilience and energy stability",
            "People who train regularly and want physician-guided peptide support",
            "Longevity-focused patients exploring mitochondrial tools",
            "Patients who want pharmacy-prepared medication with oversight",
        ],
        "inject_note": True,
        "faqs": [
            fq("Is MOTS-C the same as GLP-1?", "No. They are different classes of therapies with different considerations."),
            fq("Do I need to exercise?", "Movement supports metabolic health; your physician can personalize guidance."),
            fq("Is MOTS-C compounded?", "If prescribed, it is typically prepared by a licensed compounding pharmacy."),
            fq("What if I feel unwell?", "Contact your physician for medical concerns; contact our care team for logistics."),
            fq("How do I start?", "Book a consultation through our qualification flow."),
        ],
    },
    "focus-calm": {
        "title": "Focus & Calm Protocol",
        "h1": "Focus &amp; Calm Protocol",
        "tagline": "Cognitive enhancement meets stress resilience — a nootropic peptide stack.",
        "monthly": "$199/mo",
        "quarterly": "$537/quarter",
        "price_badge": "$199/mo",
        "what": [
            "Focus & Calm pairs two peptides often discussed for mental clarity and calm focus. It is designed for high performers who want support without traditional stimulants.",
            "Prescribing requires a physician evaluation; not everyone is a candidate.",
            "Effects are individual and may be subtle at first.",
        ],
        "who": [
            "High performers who want sharper focus during demanding work",
            "People managing everyday stress who want physician-guided options",
            "Those who prefer non-stimulant cognitive support when appropriate",
            "Patients interested in neurosupport conversations with a licensed physician",
        ],
        "inject_note": True,
        "faqs": [
            fq("Is this like a stimulant?", "It is not a stimulant product. Your physician explains what to expect."),
            fq("Can I use it with caffeine?", "Ask your physician about combinations."),
            fq("Are these peptides compounded?", "If prescribed, medications are prepared by a licensed compounding pharmacy."),
            fq("How quickly does it work?", "Some people notice changes within weeks; others take longer."),
            fq("What if I am anxious starting peptides?", "Our care team can help with onboarding questions; medical questions go to your physician."),
        ],
    },
    "methylene-blue": {
        "title": "Methylene Blue Program",
        "h1": "Methylene Blue Program",
        "tagline": "Mitochondrial support and cognitive clarity — a unique longevity conversation.",
        "monthly": "$179/mo",
        "quarterly": "$483/quarter",
        "price_badge": "$179/mo",
        "what": [
            "Methylene blue has a long history in medicine and is discussed today for mitochondrial and cognitive support in some longevity protocols.",
            "This program is prescription-based and not appropriate for everyone. Your physician reviews safety considerations carefully.",
            "Follow your prescription exactly; some medications and supplements interact.",
        ],
        "who": [
            "Adults interested in mitochondrial support under medical supervision",
            "People who want a different longevity tool beyond peptides alone",
            "Patients who can follow precise pharmacy instructions",
            "Anyone who wants a physician to screen for interactions and contraindications",
        ],
        "inject_note": False,
        "faqs": [
            fq("Why is methylene blue prescription-only here?", "We route all programs through licensed physicians for safety and compliance."),
            fq("Can it interact with medications?", "Yes. Your physician and pharmacy guidance are essential."),
            fq("Will my mouth turn blue?", "Some formulations can cause harmless discoloration. Ask your pharmacy what to expect."),
            fq("Is it compounded?", "Your prescription determines the product you receive."),
            fq("What if I am not approved?", "If your physician does not approve care, you may qualify for a full refund. See our Terms of Service for details."),
        ],
    },
    "ed-sildenafil": {
        "title": "ED Sildenafil Program",
        "h1": "ED Care (Sildenafil)",
        "tagline": "Physician-prescribed ED treatment — discreet, effective, delivered to your door.",
        "monthly": "$129/mo",
        "quarterly": "$348/quarter",
        "price_badge": "$129/mo",
        "what": [
            "This program offers physician-prescribed compounded sildenafil when appropriate. Care is handled professionally and shipped in plain packaging.",
            "A virtual consultation helps your physician understand your health history and safety considerations.",
            "Sexual wellness concerns are common; the goal is practical, respectful medical support.",
        ],
        "who": [
            "Adults seeking prescription support for erectile function",
            "Patients who want telehealth convenience and pharmacy delivery",
            "People who prefer a calm, clinical tone without hype",
            "Adults who can share an accurate medication and health history",
        ],
        "inject_note": False,
        "faqs": [
            fq("Is compounded sildenafil FDA-approved?", "Compounded medications are not FDA-approved. Prepared by licensed 503A/503B pharmacies."),
            fq("What information will my physician need?", "A full health history, current medications, and cardiovascular risk factors matter for safety."),
            fq("How is privacy handled?", "We use discreet packaging and professional processes. See our Privacy Policy for details."),
            fq("Can I use nitrates with this medication?", "No — that combination can be dangerous. Tell your physician everything you take."),
            fq("What if this is not appropriate for me?", "Your physician may recommend a different approach."),
        ],
    },
    "ed-tadalafil": {
        "title": "ED Tadalafil Program",
        "h1": "ED Care (Tadalafil Daily)",
        "tagline": "Daily low-dose tadalafil — always ready, physician-prescribed.",
        "monthly": "$179/mo",
        "quarterly": "$483/quarter",
        "price_badge": "$179/mo",
        "what": [
            "Daily tadalafil is prescribed for some adults who want a steady-dose approach. Your physician determines dose and suitability.",
            "Medication is prepared by a licensed pharmacy when prescribed and shipped to your home.",
            "Safety screening matters, especially for heart health and drug interactions.",
        ],
        "who": [
            "Adults interested in daily-dose ED support when prescribed",
            "Patients who prefer planning less around timing",
            "People who want discreet delivery and physician oversight",
            "Adults who can follow medical guidance closely",
        ],
        "inject_note": False,
        "faqs": [
            fq("Is daily tadalafil safe for everyone?", "No. Your physician evaluates cardiovascular risk and interactions."),
            fq("Is compounded tadalafil FDA-approved?", "Compounded medications are not FDA-approved. Prepared by licensed 503A/503B pharmacies."),
            fq("What side effects are common?", "Headache, flushing, and GI upset can occur. Report anything severe to your physician."),
            fq("Can I drink alcohol?", "Ask your physician how alcohol fits your plan."),
            fq("How do refills work?", "Our care team can explain fulfillment timing based on your plan."),
        ],
    },
    "male-hair-loss": {
        "title": "Male Hair Loss Program",
        "h1": "Male Hair Loss Program",
        "tagline": "Physician-prescribed hair support — proven ingredients, delivered.",
        "monthly": "$199/mo",
        "quarterly": "$537/quarter",
        "price_badge": "$199/mo",
        "what": [
            "This program combines commonly used topical ingredients in a physician-directed plan. Your prescription reflects your pattern of loss and medical history.",
            "Hair changes take months; consistency matters more than quick fixes.",
            "Physician approval is required; not everyone is a candidate.",
        ],
        "who": [
            "Men noticing thinning or receding hair who want medical guidance",
            "Patients who want a structured topical plan instead of guessing OTC products",
            "Adults who can commit to months of consistent use",
            "People who want pharmacy-prepared medication when prescribed",
        ],
        "inject_note": False,
        "faqs": [
            fq("When will I see changes?", "Many people evaluate progress around 3–6 months; individual timelines vary."),
            fq("Are topical solutions compounded?", "Often yes. Compounded medications are not FDA-approved."),
            fq("What if I stop using it?", "Benefits may fade if you stop. Ask your physician what to expect."),
            fq("Can women use this program?", "This page is for the male program; see the female hair loss program for other options."),
            fq("Do I need a consultation?", "Yes — prescribing requires a virtual physician evaluation."),
        ],
    },
    "female-hair-loss": {
        "title": "Female Hair Loss Program",
        "h1": "Female Hair Loss Program",
        "tagline": "Physician-prescribed hair restoration for women — targeted, thoughtful, effective.",
        "monthly": "$179/mo",
        "quarterly": "$483/quarter",
        "price_badge": "$179/mo",
        "what": [
            "Female pattern thinning can have hormonal contributors. This program offers physician-prescribed topical options when appropriate.",
            "Your physician may ask about cycles, hormones, and other factors that matter for safety.",
            "Progress is gradual; photos and follow-up help track change over time.",
        ],
        "who": [
            "Women noticing widening part lines or diffuse thinning",
            "Patients who want physician oversight rather than self-experimentation",
            "Adults who can follow a consistent application routine",
            "People interested in a discreet, home-delivered plan",
        ],
        "inject_note": False,
        "faqs": [
            fq("Is finasteride used for women?", "Some plans may include finasteride in specific contexts. Your physician decides what is appropriate."),
            fq("How long is a typical evaluation?", "Your virtual consultation covers history, goals, and safety screening."),
            fq("Are results guaranteed?", "No. Results may vary; physician approval required."),
            fq("Is the solution compounded?", "If prescribed, it is typically prepared by a licensed compounding pharmacy."),
            fq("What about postpartum shedding?", "Tell your physician; timing and causes matter for planning."),
        ],
    },
    "pt-141": {
        "title": "PT-141 Program",
        "h1": "Sexual Wellness (PT-141)",
        "tagline": "Physician-prescribed sexual wellness — the only peptide targeting central arousal pathways.",
        "monthly": "$149/mo",
        "quarterly": None,
        "price_badge": "$149/mo",
        "what": [
            "PT-141 (bremelanotide) is prescribed for some adults as part of sexual wellness plans. It works through a different pathway than PDE5 medications for some patients.",
            "A physician evaluates blood pressure, cardiovascular history, and other safety factors.",
            "This program is discreet, clinical, and focused on appropriate prescribing.",
        ],
        "who": [
            "Adults seeking physician-guided sexual wellness support",
            "Patients who want options beyond traditional ED medications when appropriate",
            "People who can follow timing and safety instructions carefully",
            "Adults who value privacy and pharmacy-prepared medication",
        ],
        "inject_note": True,
        "faqs": [
            fq("Is PT-141 compounded?", "If prescribed, it may be prepared by a licensed compounding pharmacy."),
            fq("What are common side effects?", "Nausea and flushing can occur. Your physician explains what to watch for."),
            fq("Who should not use PT-141?", "People with certain cardiovascular risks may not be candidates. Your physician screens you."),
            fq("How is it taken?", "Follow your prescription label; routes and schedules vary."),
            fq("Is compounded PT-141 the same as every commercial product?", "Compounded PT-141 is not FDA-approved. Prepared by licensed 503A/503B pharmacies. Your physician explains how prescribing applies to you."),
        ],
    },
    "ghk-cu": {
        "title": "GHK-Cu Program",
        "h1": "GHK-Cu Anti-Aging Program",
        "tagline": "Copper peptide therapy — wound healing, collagen synthesis, and anti-aging at the cellular level.",
        "monthly": "$179/mo",
        "quarterly": None,
        "price_badge": "$179/mo",
        "what": [
            "GHK-Cu is a copper peptide discussed for skin quality, repair signaling, and healthy aging aesthetics. Access is prescription-based through AW.",
            "Your physician determines whether injections or another format fits your plan.",
            "Cosmetic and wellness results vary widely between individuals.",
        ],
        "who": [
            "Adults interested in skin quality and healthy aging support",
            "Patients exploring peptide aesthetics with medical oversight",
            "People who want pharmacy-prepared products rather than unregulated sources",
            "Anyone who prefers a physician to screen safety and expectations",
        ],
        "inject_note": True,
        "faqs": [
            fq("Is GHK-Cu injected?", "Many plans use injection, but your physician decides what is appropriate."),
            fq("Is GHK-Cu FDA-approved?", "Compounded medications are not FDA-approved. Prepared by licensed 503A/503B pharmacies."),
            fq("When will I see skin changes?", "Some people notice texture changes over weeks to months."),
            fq("Can I use retinoids too?", "Ask your physician about combining therapies."),
            fq("How do I qualify?", "Complete a virtual consultation for physician review."),
        ],
    },
    "discovery": {
        "title": "Discovery Consult",
        "h1": "Discovery Consult",
        "tagline": "Not sure where to start? A licensed physician reviews your history and recommends a path.",
        "monthly": "$49 one-time",
        "quarterly": None,
        "price_badge": "$49",
        "skip_compounded_what_line": True,
        "hero_cta_microcopy": "Full refund if no program is right for you.",
        "pricing_cta_microcopy": "Full refund if no program is right for you.",
        "included_lines": [
            "Virtual physician consultation",
            "Personalized program recommendation based on your history and goals",
            "$49 credited toward enrollment when you start a qualifying program",
            "Care team support for next steps",
        ],
        "what": [
            "The Discovery Consult is a one-time visit designed to help you choose the right program. A licensed physician reviews your health history and goals, then suggests next steps.",
            "If you enroll in a program, the consult fee is credited toward enrollment as described at checkout.",
            "If no program is a fit, you can receive a full refund — see current terms at enrollment.",
        ],
        "who": [
            "People comparing peptide, GLP-1, and longevity options",
            "Anyone who wants medical guidance before committing to a shipment plan",
            "Patients with complex histories who need a careful first conversation",
            "Adults who value a structured recommendation rather than guessing online",
        ],
        "inject_note": False,
        "extra": "Full refund if no program is right for you (see terms at checkout).",
        "faqs": [
            fq("What happens after I book?", "You complete intake and join a virtual physician consultation."),
            fq("How long is the visit?", "Length varies by complexity; plan for a full conversation."),
            fq("Do I get a prescription in the consult?", "Only if your physician determines a prescription is appropriate."),
            fq("Is the fee applied if I enroll?", "Yes — credited toward enrollment when you start a qualifying program."),
            fq("What if I am not sure about peptides?", "That is exactly what the Discovery Consult is for."),
        ],
    },
    "tesamorelin": {
        "title": "Tesamorelin Program",
        "h1": "Tesamorelin Program",
        "tagline": "Growth-hormone releasing peptide support — often discussed for metabolic and body-composition goals.",
        "monthly": "$199/mo",
        "quarterly": "$537/quarter",
        "price_badge": "$199/mo",
        "what": [
            "Tesamorelin is a prescription peptide discussed in performance and metabolic medicine. It is not appropriate for everyone and requires physician screening.",
            "If prescribed, medication is prepared by a licensed compounding pharmacy and shipped with instructions.",
            "Your physician explains monitoring expectations and whether this option fits your history.",
        ],
        "who": [
            "Adults exploring advanced GH-axis support under medical supervision",
            "Patients who want a physician to compare tesamorelin with other secretagogue options",
            "People already in structured training or longevity plans",
            "Anyone who needs clear safety screening before starting",
        ],
        "inject_note": True,
        "faqs": [
            fq("How is tesamorelin different from sermorelin?", "They are different options with different prescribing considerations. Your physician compares them for your case."),
            fq("Is tesamorelin compounded?", "If prescribed, it is typically prepared by a licensed compounding pharmacy."),
            fq("Do I need monitoring?", "Your physician may recommend labs or follow-up based on your profile."),
            fq("Can I stack tesamorelin with Recovery?", "Only your physician can decide about combinations."),
            fq("What if I am not approved?", "If your physician does not approve care, you may qualify for a full refund. See our Terms of Service for details."),
        ],
    },
}


def fix_related() -> None:
    fallbacks = ["discovery", "perform", "renew", "longevity", "metformin", "glp1-sema", "recovery"]
    for slug, meta in META.items():
        picks = [s for s in RELATED_SLUGS.get(slug, []) if s != slug and s in CARD_NAMES]
        for fb in fallbacks:
            if len(picks) >= 3:
                break
            if fb != slug and fb not in picks and fb in CARD_NAMES:
                picks.append(fb)
        meta["related"] = [(s, CARD_NAMES[s][0], CARD_NAMES[s][1]) for s in picks[:3]]


def _load_blog_posts() -> list[dict]:
    path = ROOT / "scripts" / "blog_data.py"
    spec = importlib.util.spec_from_file_location("aw_blog_data", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("scripts/blog_data.py is required for blog generation")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return list(mod.POSTS)


def article_json_ld(title: str, slug: str, description: str) -> str:
    url = f"{BASE_URL}/blog/{slug}.html"
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": description,
            "author": {"@type": "Organization", "name": "Authentic Wellness Medical Team"},
            "datePublished": "2026-03-01",
            "dateModified": "2026-03-01",
            "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "publisher": {"@type": "Organization", "name": "Authentic Wellness"},
        },
        indent=2,
    )


def build_blog_article(post: dict, nav: str, foot: str) -> str:
    slug = post["slug"]
    title = post["title"]
    description = post["description"]
    paras = post["paragraphs"]
    faqs = post["faqs"]
    see_also: list[tuple[str, str]] = post.get("see_also", [])
    body = "".join(f'      <p class="blog-prose">{esc(p)}</p>\n' for p in paras)
    see_block = ""
    if see_also:
        links = " · ".join(f'<a href="{h}">{esc(lab)}</a>' for h, lab in see_also)
        see_block = f"""
  <section class="section-linen">
    <div class="container blog-see-also">
      <h2>Related on Authentic Wellness</h2>
      <p class="blog-prose">{links}</p>
    </div>
  </section>"""
    faq_html = ""
    for i, (q, a) in enumerate(faqs):
        faq_html += f"""
        <div class="faq-item">
          <button class="faq-question" id="bq-{slug}-{i}" type="button">{esc(q)}</button>
          <div class="faq-answer">{esc(a)}</div>
        </div>"""
    url = f"{BASE_URL}/blog/{slug}.html"
    art_ld = article_json_ld(title, slug, description)
    faq_ld = faq_schema(faqs)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)} | The AW Journal</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{url}">
  <link rel="icon" href="../favicon.ico" sizes="any">
  <link rel="icon" href="../logo-mark.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Playfair+Display:wght@400;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/style.css">
  <script type="application/ld+json">
  {art_ld}
  </script>
  <script type="application/ld+json">
  {faq_ld}
  </script>
</head>
<body class="blog-post-page">

  <nav class="navbar">
    <div class="container nav-inner">
      <a href="../index.html" class="nav-logo" aria-label="Authentic Wellness home">
        <img src="../logo-dark.svg" width="220" height="34" alt="Authentic Wellness">
      </a>
{nav}
      <button class="nav-toggle" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>

  <header class="page-header blog-post-header">
    <div class="container" style="max-width:720px;">
      <p class="blog-kicker"><a href="index.html">The AW Journal</a></p>
      <h1>{esc(title)}</h1>
      <p class="blog-meta">By Authentic Wellness Medical Team · March 2026</p>
      <p class="blog-deck">{esc(description)}</p>
    </div>
  </header>

  <article class="blog-article-body">
    <div class="container" style="max-width:720px;">
{body}    </div>
  </article>
{see_block}

  <section class="faq-strip section-white">
    <div class="container" style="max-width:780px;">
      <h2 class="text-center">Questions readers ask</h2>
      {faq_html}
    </div>
  </section>

{foot}
</body>
</html>"""


def build_blog_index(posts: list[dict], nav: str, foot: str) -> str:
    items = ""
    for p in posts:
        items += f"""
      <article class="blog-list-card">
        <h2><a href="{p["slug"]}.html">{esc(p["title"])}</a></h2>
        <p class="blog-meta">March 2026 · Authentic Wellness Medical Team</p>
        <p>{esc(p["description"])}</p>
        <a href="{p["slug"]}.html" class="blog-read-more">Read article</a>
      </article>"""
    list_ld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "The AW Journal",
            "description": "Articles on physician-prescribed performance and longevity programs from Authentic Wellness.",
            "url": f"{BASE_URL}/blog/index.html",
        },
        indent=2,
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The AW Journal | Authentic Wellness</title>
  <meta name="description" content="Physician-reviewed articles on peptides, GLP-1 support, NAD+, and longevity.">
  <link rel="canonical" href="{BASE_URL}/blog/index.html">
  <link rel="icon" href="../favicon.ico" sizes="any">
  <link rel="icon" href="../logo-mark.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Playfair+Display:wght@400;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/style.css">
  <script type="application/ld+json">
  {list_ld}
  </script>
</head>
<body class="blog-index-page">

  <nav class="navbar">
    <div class="container nav-inner">
      <a href="../index.html" class="nav-logo" aria-label="Authentic Wellness home">
        <img src="../logo-dark.svg" width="220" height="34" alt="Authentic Wellness">
      </a>
{nav}
      <button class="nav-toggle" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>

  <header class="page-header">
    <div class="container">
      <h1>The AW Journal</h1>
      <p class="subtitle">Science-forward perspectives on physician-prescribed programs — written for curious adults, not hype.</p>
      <p class="hero-tagline" style="margin-top:1rem;">Optimized from the inside out.</p>
    </div>
  </header>

  <section class="section-linen">
    <div class="container blog-list">
{items}
    </div>
  </section>

{foot}
</body>
</html>"""


def write_blog_pages() -> None:
    blog_dir = ROOT / "blog"
    blog_dir.mkdir(exist_ok=True)
    posts = _load_blog_posts()
    nav = nav_blog()
    foot = footer_blog()
    (blog_dir / "index.html").write_text(build_blog_index(posts, nav, foot), encoding="utf-8")
    print("wrote blog index")
    for p in posts:
        (blog_dir / f"{p['slug']}.html").write_text(build_blog_article(p, nav, foot), encoding="utf-8")
        print("wrote blog", p["slug"])


def main() -> None:
    fix_related()
    programs_dir = ROOT / "programs"
    programs_dir.mkdir(exist_ok=True)
    nav = nav_sub()
    foot = footer_sub()
    for slug, meta in META.items():
        html = build_program_page(slug, meta, nav, foot, "../")
        (programs_dir / f"{slug}.html").write_text(html, encoding="utf-8")
        print("wrote", slug)

    write_blog_pages()


if __name__ == "__main__":
    main()
