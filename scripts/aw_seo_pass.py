#!/usr/bin/env python3
"""One-off normalization: www host, shared OG image default, MedicalOrganization JSON-LD tail injection."""
from __future__ import annotations

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

OLD_HOST = "https://authenticwellness.com"
NEW_HOST = "https://www.authenticwellness.com"

MED_ORG = """
 <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "MedicalOrganization",
    "name": "Authentic Wellness",
    "alternateName": "Evolving Wellness LLC DBA Authentic Wellness",
    "url": "https://www.authenticwellness.com",
    "logo": "https://www.authenticwellness.com/logo-dark.svg",
    "description": "Physician-prescribed peptide therapy and GLP-1 programs delivered via telehealth, overseen by a licensed California physician and compounded at FDA-registered pharmacies.",
    "medicalSpecialty": ["PreventiveMedicine", "Endocrine"],
    "sameAs": ["https://www.instagram.com/authenticwellness"]
  }
  </script>
"""

SPEAKABLE = """
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "speakable": {
      "@type": "SpeakableSpecification",
      "cssSelector": [".hero h1", ".hero .lede", ".faq-question", ".faq-answer"]
    }
  }
  </script>
"""


def main() -> None:
    for path in AW_HTML:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        text = text.replace(OLD_HOST, NEW_HOST)
        text = text.replace("http://authenticwellness.com", NEW_HOST)
        # Default OG/Twitter image to new asset
        text = re.sub(
            r'<meta property="og:image" content="https://www\.authenticwellness\.com/[^"]*">',
            '<meta property="og:image" content="https://www.authenticwellness.com/assets/img/og/og-default.jpg">',
            text,
            count=1,
        )
        text = re.sub(
            r'<meta name="twitter:image" content="https://www\.authenticwellness\.com/[^"]*">',
            '<meta name="twitter:image" content="https://www.authenticwellness.com/assets/img/og/og-default.jpg">',
            text,
            count=1,
        )
        if "MedicalOrganization" in text and '"@type": "MedicalOrganization"' in text:
            pass
        elif "<!-- aw-medical-org -->" not in text and "</head>" in text:
            text = text.replace("</head>", "<!-- aw-medical-org -->\n" + MED_ORG + "\n</head>", 1)
        path.write_text(text, encoding="utf-8")
        print(path.relative_to(ROOT))

    # Speakable: index + faq only
    for rel in ("index.html", "faq.html"):
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        if "SpeakableSpecification" in text:
            continue
        if "</head>" not in text:
            continue
        text = text.replace("</head>", SPEAKABLE + "\n</head>", 1)
        path.write_text(text, encoding="utf-8")
        print("speakable", rel)


if __name__ == "__main__":
    main()
