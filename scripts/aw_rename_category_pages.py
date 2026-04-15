#!/usr/bin/env python3
"""Generate compound-first category pages and deprecation stubs for Authentic Wellness root site."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROG = ROOT / "programs"

NAV = r"""  <nav class="navbar">
    <div class="container nav-inner">
      <a href="../index.html" class="nav-logo" aria-label="Authentic Wellness home">
        <img src="../logo-dark.svg" width="220" height="50" alt="Authentic Wellness">
      </a>
      <div class="nav-links" id="primary-navigation">
        <div class="nav-item nav-dropdown">
          <button type="button" class="nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true" id="programs-menu-btn">Programs <span class="nav-caret" aria-hidden="true"></span></button>
          <div class="nav-dropdown-menu" id="programs-menu" role="menu" aria-label="Program categories">
            <div class="nav-dropdown-grid">
            <div class="nav-dropdown-overview">
                <a href="../programs.html" class="nav-dropdown-all" role="menuitem">Browse all programs</a>
                <p class="nav-dropdown-overview-copy">Physician-evaluated compounds — shop by category.</p>
                <a href="../programs.html" class="nav-dropdown-discovery nav-dropdown-overview-discovery" role="menuitem">Get Started</a>
              </div>
              <div class="nav-dropdown-col">
                <span class="nav-dropdown-heading">Categories</span>
                <span class="nav-dropdown-subhead">Compound-first catalog</span>
                <a href="weight-loss.html" role="menuitem">Weight loss</a>
                <a href="muscle-performance.html" role="menuitem">Muscle &amp; performance</a>
                <a href="recovery-healing.html" role="menuitem">Recovery &amp; healing</a>
                <a href="longevity.html" role="menuitem">Longevity</a>
                <a href="sexual-health.html" role="menuitem">Sexual health</a>
                <a href="hair-skin.html" role="menuitem">Hair &amp; skin</a>
              </div>
 </div>
          </div>
        </div>
        <a href="../blog/">Blog</a>
        <a href="../how-it-works.html">How It Works</a>
        <a href="../about.html">About</a>
        <a href="../faq.html">FAQ</a>
        <a href="../contact.html">Contact</a>
        <div class="nav-cta">
          <button type="button" class="btn btn-primary" style="padding:0.625rem 1.5rem;font-size:0.85rem;" onclick="window.location.href='../programs.html'">Get Started</button>
        </div>
      </div>
      <button class="nav-toggle" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
      </button>
    </div>
  </nav>"""

FOOTER = r"""  <footer class="footer">
    <div class="container">
      <div class="footer-grid">
        <div>
          <a href="../index.html" class="footer-mark" aria-label="Authentic Wellness home">
            <img src="../logo-light.svg" width="220" height="50" alt="Authentic Wellness">
          </a>
          <p style="margin-top:0.5rem;">Physician-prescribed programs — compound-first catalog with independent licensed physicians.</p>
          <p style="margin-top:0.75rem;">info@authenticwellness.com</p>
        </div>
        <div>
          <p class="footer-col-title">Programs</p>
          <p class="compliance-disclaimer" style="margin-bottom:0.75rem;">Compounded medications are not FDA-approved. Prepared by a licensed U.S. pharmacy.</p>
          <div class="footer-links">
            <a href="weight-loss.html">Weight loss</a>
            <a href="muscle-performance.html">Muscle &amp; performance</a>
            <a href="recovery-healing.html">Recovery &amp; healing</a>
            <a href="longevity.html">Longevity</a>
            <a href="sexual-health.html">Sexual health</a>
            <a href="hair-skin.html">Hair &amp; skin</a>
            <a href="../programs.html">All programs</a>
          </div>
        </div>
        <div>
          <p class="footer-col-title">Company</p>
          <div class="footer-links">
            <a href="../how-it-works.html">How It Works</a>
            <a href="../about.html">About</a>
            <a href="../faq.html">FAQ</a>
            <a href="../contact.html">Contact</a>
            <a href="../blog/">Blog</a>
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
        <p class="footer-medical-director">Medical Director: Joshua Yang, MD · CA License A167038 · NPI 1851549232</p>
        <p>Physician-prescribed programs. Medications are fulfilled through a licensed U.S. pharmacy when prescribed.</p>
        <p>Compounded medications are prepared by a licensed U.S. pharmacy when prescribed and are not FDA-approved. These medications are prescribed by independent licensed physicians based on individual patient needs. Authentic Wellness does not manufacture, compound, or dispense any medications. Results may vary. Physician approval required.</p>
        <p>Telehealth services may not be available in all states. Eligibility is determined during your consultation.</p>
        <p>Authentic Wellness is a wellness platform, not a medical practice. All medical decisions, prescriptions, and treatment plans are made solely by independent licensed physicians through Qualiphy. Authentic Wellness does not provide medical advice, diagnoses, or treatment. We facilitate access to independent licensed physicians via Qualiphy.</p>
        <p>In-clinic care: <a href="https://transformativemedspa.com">Transformative Wellness</a> — Vista, CA (<a href="https://transformativemedspa.com">transformativemedspa.com</a>).</p>
      </div>
    </div>
  </footer>

  <div id="cookie-banner" class="cookie-banner" role="region" aria-label="Cookie notice">
    <div class="cookie-inner">
      <p>We use essential cookies to run this site and optional analytics. Click Accept to allow analytics, or continue without. See our <a href="../privacy.html">Privacy Policy</a>.</p>
      <button type="button" id="cookie-dismiss" class="cookie-btn">Accept</button>
    </div>
  </div>
  <script src="../js/main.js" defer></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.1/moment.min.js" defer></script>
  <script id="qualiphy-script" defer type="text/javascript"
    src="https://www.app.qualiphy.me/scripts/quidget_disclosure.js"
    data-formsrc='https://www.app.qualiphy.me/qualiphy-widget?clinic=Authentic Wellness&clinicId=6456&first_name=&last_name=&email=&phone_number=&gender=&exams=4194,4198,4199,4200,4202,4203,4204,4205,4207,2769,3702,2745,3703,4171,4172,4173,4174,1702,1008,1009,4106,4208,1904,1906,4226,1618,2488,2120,2316,2315,2129,1620,2121,2314,2130,1623,2248,4313,4334,2131,1690,2122,4314,4335,2565,2567,2755,2702,2861,2862,2863,2756,2864,2791,1900,3389,3388,4022,3538,116,2962,2247,3306,2075,3297,3298,3300,3299,3301,3302,3304,3305,3307,3308,3309,3310,3311,623,1486,1634,1808,1619,1621,1575,1640,3390,3990&tele_state_required=true&token=e97111808226681a2f307629007e908f0f719bd7'
    data-timezone='-7'
    data-examhours='[{"SUN":{"FROM":"00:00","TO":"23:59","isDaySelected":true}},{"MON":{"FROM":"00:00","TO":"23:59","isDaySelected":true}},{"TUE":{"FROM":"00:00","TO":"23:59","isDaySelected":true}},{"WED":{"FROM":"00:00","TO":"23:59","isDaySelected":true}},{"THU":{"FROM":"00:00","TO":"23:59","isDaySelected":true}},{"FRI":{"FROM":"00:00","TO":"23:59","isDaySelected":true}},{"SAT":{"FROM":"00:00","TO":"23:59","isDaySelected":true}}]'>
  </script>"""


def card(eyebrow: str, name: str, mech: str, price: str, href: str, cta: str = "Get Started", note: str = "") -> str:
    note_html = f'<p class="category-card-note">{note}</p>' if note else ""
    if price.startswith("$"):
        price_html = f"""      <p class="category-hub-card-price">From {price}<a href="../programs.html#pricing-disclosure" class="pricing-dagger" aria-label="Pricing footnote">&dagger;</a></p>"""
    else:
        price_html = f"""      <p class="category-hub-card-price">{price}</p>"""
    return f"""    <article class="category-hub-card">
      <span class="program-category-eyebrow">{eyebrow}</span>
      <h2 class="category-hub-card-title">{name}</h2>
      <p class="category-hub-card-mech">{mech}</p>
{price_html}
      <a href="{href}" class="btn btn-primary">{cta}</a>
      {note_html}
    </article>"""


PAGES = {
    "weight-loss.html": {
        "title": "Weight loss programs | Authentic Wellness",
        "desc": "Semaglutide and tirzepatide physician-prescribed programs — compound-first GLP-1 catalog.",
        "h1": "Weight loss",
        "cards": [
            (
                "Weight loss",
                "Semaglutide Program",
                "GLP-1 receptor agonist that reduces appetite and supports weight loss when medically appropriate.",
                "$299/mo",
                "glp1-sema.html",
            ),
            (
                "Weight loss",
                "Tirzepatide Program",
                "Dual GIP/GLP-1 agonist for metabolic weight management under physician supervision.",
                "$349/mo",
                "glp1-tirz.html",
            ),
        ],
        "extra": """ <section class="section-linen">
    <div class="container" style="max-width:720px;">
      <p class="text-center">Oral capsules, sublingual drops, and metabolic support options live on the <a href="../programs.html">full programs hub</a>.</p>
    </div>
  </section>""",
    },
    "muscle-performance.html": {
        "title": "Muscle &amp; performance programs | Authentic Wellness",
        "desc": "CJC-1295 + ipamorelin, sermorelin, and tesamorelin — growth-hormone pathway peptides, physician-prescribed.",
        "h1": "Muscle &amp; performance",
        "cards": [
            (
                "Muscle &amp; performance",
                "CJC-1295 + Ipamorelin Program",
                "Growth-hormone secretagogue pair for recovery, sleep, and body composition support.",
                "$249/mo",
                "cjc-1295-ipamorelin.html",
            ),
            (
                "Muscle &amp; performance",
                "Sermorelin Program",
                "Gentler GH-releasing peptide analog focused on sleep quality and daily vitality.",
                "$229/mo",
                "sermorelin-injectable.html",
            ),
            (
                "Muscle &amp; performance",
                "Tesamorelin Program",
                "GHRH analog often used for visceral adiposity and body composition when prescribed.",
                "$199/mo",
                "tesamorelin.html",
                "Get Started",
                "Confirm standing orders with your physician; formulary-dependent.",
            ),
        ],
        "extra": """  <section class="section-linen">
    <div class="container" style="max-width:720px;">
      <p class="text-center">Nasal and blend options are listed on the <a href="../programs.html">programs hub</a>.</p>
    </div>
  </section>""",
    },
    "recovery-healing.html": {
        "title": "Recovery &amp; healing programs | Authentic Wellness",
        "desc": "BPC-157, TB-500, and GHK-Cu — tissue repair and recovery peptides when medically appropriate.",
        "h1": "Recovery &amp; healing",
        "cards": [
            (
                "Recovery &amp; healing",
                "BPC-157 Program",
                "Body-protective peptide discussed for tissue and gut recovery — availability subject to physician and formulary review.",
                "Clinical consultation",
                "bpc-157.html",
                "Clinical consultation required",
                "Clinical consultation required — public enrollment may be limited by formulary status.",
            ),
            (
                "Recovery &amp; healing",
                "TB-500 Program",
                "Tissue repair peptide often paired in recovery protocols — subject to physician and formulary review.",
                "Clinical consultation",
                "bpc-tb-recovery-stack.html",
                "Clinical consultation required",
                "Offered as part of our BPC-157 + TB-500 stack page; confirm eligibility with your physician.",
            ),
            (
                "Recovery &amp; healing",
                "GHK-Cu Program",
                "Copper tripeptide for collagen-related repair and skin quality pathways when prescribed.",
                "$179/mo",
                "ghk-cu.html",
            ),
        ],
        "extra": "",
    },
    "longevity.html": {
        "title": "Longevity programs | Authentic Wellness",
        "desc": "NAD+, epitalon, and related longevity-focused compounds — physician-prescribed telehealth programs.",
        "h1": "Longevity",
        "cards": [
            (
                "Longevity",
                "NAD+ Program",
                "Supports cellular energy (NAD+/NADH) pathways associated with healthy aging.",
                "$279/mo",
                "nad-injectable.html",
            ),
            (
                "Longevity",
                "Epitalon Program",
                "Peptide discussed in telomerase and cellular aging research contexts.",
                "$169/mo",
                "epithalon.html",
            ),
            (
                "Longevity",
                "NAD+ nasal spray",
                "Needle-free NAD+ option when your physician selects this route.",
                "$319/mo",
                "nad-nasal-spray.html",
            ),
        ],
        "extra": """  <section class="section-linen">
    <div class="container" style="max-width:720px;">
      <p class="text-center text-muted">Additional mitochondrial and immune peptides (MOTS-C, SS-31, and others) are on the <a href="../programs.html">full programs hub</a>. Glutathione may be added when on formulary — ask your care team.</p>
    </div>
  </section>""",
    },
    "sexual-health.html": {
        "title": "Sexual health programs | Authentic Wellness",
        "desc": "PT-141 and standard ED medications — physician-prescribed sexual wellness catalog.",
        "h1": "Sexual health",
        "cards": [
            (
                "Sexual health",
                "PT-141 Program",
                "Bremelanotide melanocortin agonist for desire and arousal pathways when prescribed.",
                "$179/mo",
                "pt-141.html",
            ),
            (
                "Sexual health",
                "Tadalafil Program",
                "Daily or as-needed PDE5 support for erectile function when medically appropriate.",
                "$199/mo",
                "ed-tadalafil.html",
            ),
            (
                "Sexual health",
                "Sildenafil Program",
                "On-demand PDE5 support when prescribed by your physician.",
                "$129/mo",
                "ed-sildenafil.html",
            ),
        ],
        "extra": """  <section class="section-linen">
    <div class="container" style="max-width:720px;">
      <p class="text-center text-muted">Kisspeptin and other hormone-signaling peptides may be available through consultation when on formulary — coordinate with your physician.</p>
    </div>
  </section>""",
    },
    "hair-skin.html": {
        "title": "Hair &amp; skin programs | Authentic Wellness",
        "desc": "Hair loss protocols and GHK-Cu — compound-first dermatology-adjacent telehealth programs.",
        "h1": "Hair &amp; skin",
        "cards": [
            (
                "Hair &amp; skin",
                "GHK-Cu Program",
                "Copper peptide for tissue repair and skin quality — may be prescribed for topical or injectable routes.",
                "$179/mo",
                "ghk-cu.html",
            ),
            (
                "Hair &amp; skin",
                "Men&apos;s hair loss (oral)",
                "Finasteride + minoxidil protocol when prescribed for androgenic alopecia.",
                "$55/mo",
                "male-hair-loss.html",
            ),
            (
                "Hair &amp; skin",
                "Men&apos;s hair loss (topical)",
                "Topical minoxidil/finasteride when your physician selects this formulation.",
                "$79/mo",
                "mens-hair-loss-topical.html",
            ),
            (
                "Hair &amp; skin",
                "Women&apos;s hair loss",
                "Oral minoxidil/spironolactone options when medically appropriate.",
                "$55/mo",
                "female-hair-loss.html",
            ),
        ],
        "extra": """  <section class="section-linen">
    <div class="container" style="max-width:720px;">
      <p class="text-center text-muted">Peptide-based hair protocols: route standing-order hair peptide requests through Dr. Yang until coverage is finalized.</p>
    </div>
  </section>""",
    },
}


def build_page(fname: str, spec: dict) -> str:
    h1 = spec["h1"]
    title = spec["title"]
    desc = spec["desc"]
    parts = [
        f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://authenticwellness.com/programs/{fname}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Authentic Wellness">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="https://authenticwellness.com/programs/{fname}">
  <meta property="og:image" content="https://authenticwellness.com/og-default.png">
  <link rel="icon" href="../favicon.ico" sizes="any">
  <link rel="icon" href="../logo-mark.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Playfair+Display:wght@400;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/style.css">
  <link rel="stylesheet" href="https://firebasestorage.googleapis.com/v0/b/qualiphy-web-d918b.appspot.com/o/style-v4.css?alt=media&token=34735782-16e8-4a2f-9eaa-426d65af48b2" />
</head>
<body class="program-subpage category-hub-page">
  <a href="#main-content" class="skip-link">Skip to main content</a>
{NAV}
  <main id="main-content">
  <section class="page-header">
    <div class="container">
      <h1>{h1}</h1>
      <p>Each card names the compound you may be prescribed after an independent physician review.</p>
      <p class="compliance-disclaimer" style="max-width:720px;margin:0.75rem auto 0;">Compounded medications are not FDA-approved. Prepared by a licensed U.S. pharmacy when prescribed.</p>
    </div>
  </section>
  <section class="section-white category-hub-grid-section">
    <div class="container">
      <div class="category-hub-grid">
""",
    ]
    for c in spec["cards"]:
        parts.append(card(*c))
        parts.append("\n")
    parts.append("""      </div>
    </div>
  </section>
""")
    if spec.get("extra"):
        parts.append(spec["extra"] + "\n")
    parts.append(
        """  <section class="program-compliance-bar">
    <div class="container">
      <p>Compounded medications are not FDA-approved. Prepared by a licensed U.S. pharmacy. Results may vary. Physician approval required.</p>
    </div>
  </section>
  </main>
"""
    )
    parts.append(FOOTER)
    parts.append("\n</body>\n</html>\n")
    return "".join(parts)


STUB = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="refresh" content="0; url=/programs.html">
  <meta name="robots" content="noindex, nofollow">
  <title>Moved | Authentic Wellness</title>
  <link rel="canonical" href="https://authenticwellness.com/programs.html">
</head>
<body>
  <p>This program has been renamed. You&apos;ll be redirected to our updated programs page.
  <a href="/programs.html">Click here if you aren&apos;t redirected.</a></p>
</body>
</html>
"""


def main() -> None:
    for fname, spec in PAGES.items():
        (PROG / fname).write_text(build_page(fname, spec), encoding="utf-8")
        print("wrote", fname)
    for stub in ("perform.html", "renew.html", "recovery.html", "discovery.html"):
        (PROG / stub).write_text(STUB, encoding="utf-8")
        print("stub", stub)


if __name__ == "__main__":
    main()
