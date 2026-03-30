#!/usr/bin/env python3
"""One-off patcher for Authentic Wellness static HTML (repo root only)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

QUALIPHY_CSS = """  <!-- Qualiphy Quidget Part 1 — stylesheet -->
  <link rel="stylesheet" href="https://firebasestorage.googleapis.com/v0/b/qualiphy-web-d918b.appspot.com/o/style-v4.css?alt=media&token=34735782-16e8-4a2f-9eaa-426d65af48b2" />
"""

QUALIPHY_SCRIPTS = """  <!-- Qualiphy Quidget Part 3 — before </body> -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.1/moment.min.js"></script>
  <script id="qualiphy-script" type="text/javascript"
    src="https://www.app.qualiphy.me/scripts/quidget_disclosure.js"
    data-formsrc='https://www.app.qualiphy.me/qualiphy-widget?clinic=Authentic Wellness&clinicId=6456&first_name=&last_name=&email=&phone_number=&gender=&exams=4194,4198,4199,4200,4202,4203,4204,4205,4207,2769,3702,2745,3703,4171,4172,4173,4174,1702,1008,1009,4106,4208,1904,1906,4226,1618,2488,2120,2316,2315,2129,1620,2121,2314,2130,1623,2248,4313,4334,2131,1690,2122,4314,4335,2565,2567,2755,2702,2861,2862,2863,2756,2864,2791,1900,3389,3388,4022,3538,116,2962,2247,3306,2075,3297,3298,3300,3299,3301,3302,3304,3305,3307,3308,3309,3310,3311,623,1486,1634,1808,1619,1621,1575,1640,3390,3990&tele_state_required=true&token=e97111808226681a2f307629007e908f0f719bd7'
    data-timezone='-7'
    data-examhours='[{"SUN":{"FROM":"00:00","TO":"23:59","isDaySelected":true}},{"MON":{"FROM":"00:00","TO":"23:59","isDaySelected":true}},{"TUE":{"FROM":"00:00","TO":"23:59","isDaySelected":true}},{"WED":{"FROM":"00:00","TO":"23:59","isDaySelected":true}},{"THU":{"FROM":"00:00","TO":"23:59","isDaySelected":true}},{"FRI":{"FROM":"00:00","TO":"23:59","isDaySelected":true}},{"SAT":{"FROM":"00:00","TO":"23:59","isDaySelected":true}}]'>
  </script>
"""

FOOTER_OLD = """        <p>Physician-prescribed programs. Medications sourced from licensed 503A/503B compounding pharmacies.</p>
        <p>Compounded medications are not FDA-approved. Prepared by licensed 503A/503B pharmacies. Results may vary. Physician approval required.</p>
        <p>Authentic Wellness is not a medical practice. We facilitate access to independent licensed physicians via Qualiphy.</p>"""

FOOTER_NEW = """        <p>Physician-prescribed programs. Medications sourced from licensed 503A/503B compounding pharmacies.</p>
        <p>Compounded medications are prepared by state-licensed 503A/503B compounding pharmacies and are not FDA-approved. These medications are prescribed by independent licensed physicians based on individual patient needs. Authentic Wellness does not manufacture, compound, or dispense any medications. Results may vary. Physician approval required.</p>
        <p>Telehealth services may not be available in all states. Eligibility is determined during your consultation.</p>
        <p>Authentic Wellness is a wellness platform, not a medical practice. All medical decisions, prescriptions, and treatment plans are made solely by independent licensed physicians through Qualiphy. Authentic Wellness does not provide medical advice, diagnoses, or treatment. We facilitate access to independent licensed physicians via Qualiphy.</p>"""

REFUND_OLD = "Full refund if not approved by your physician."
REFUND_NEW = "Full medication refund if not approved by your physician. Consultation fee is non-refundable."


def aw_html_files() -> list[Path]:
    out: list[Path] = []
    for p in ROOT.glob("*.html"):
        out.append(p)
    for sub in ("programs", "blog"):
        d = ROOT / sub
        if d.is_dir():
            out.extend(sorted(d.glob("*.html")))
    return out


def inject_qualiphy_head(text: str) -> str:
    if "quidget_disclosure.js" in text or "style-v4.css" in text:
        return text
    if "href=\"css/style.css\"" in text:
        return text.replace(
            "<link rel=\"stylesheet\" href=\"css/style.css\">",
            "<link rel=\"stylesheet\" href=\"css/style.css\">\n" + QUALIPHY_CSS,
            1,
        )
    if "href=\"../css/style.css\"" in text:
        return text.replace(
            "<link rel=\"stylesheet\" href=\"../css/style.css\">",
            "<link rel=\"stylesheet\" href=\"../css/style.css\">\n" + QUALIPHY_CSS,
            1,
        )
    return text


def inject_qualiphy_body(text: str) -> str:
    if "quidget_disclosure.js" in text:
        return text
    if "<script src=\"js/main.js\"></script>" in text:
        return text.replace(
            "<script src=\"js/main.js\"></script>",
            "<script src=\"js/main.js\"></script>\n" + QUALIPHY_SCRIPTS,
            1,
        )
    if "<script src=\"../js/main.js\"></script>" in text:
        return text.replace(
            "<script src=\"../js/main.js\"></script>",
            "<script src=\"../js/main.js\"></script>\n" + QUALIPHY_SCRIPTS,
            1,
        )
    return text


def patch_ctas(text: str) -> str:
    # See If You Qualify — any how-it-works / #start href
    text = re.sub(
        r'<a href="how-it-works\.html(?:#start)?" class="btn btn-primary"([^>]*)>(See If You Qualify)</a>',
        r'<button type="button" class="btn btn-primary"\1 onclick="showDisclosureModal()">\2</button>',
        text,
    )
    text = re.sub(
        r'<a href="\.\./how-it-works\.html#start" class="btn btn-primary"([^>]*)>(See If You Qualify)</a>',
        r'<button type="button" class="btn btn-primary"\1 onclick="showDisclosureModal()">\2</button>',
        text,
    )
    text = re.sub(
        r'<a href="\.\./how-it-works\.html#start" class="btn btn-primary program-page-cta">(See If You Qualify)</a>',
        r'<button type="button" class="btn btn-primary program-page-cta" onclick="showDisclosureModal()">\1</button>',
        text,
    )
    text = re.sub(
        r'<a href="\.\./how-it-works\.html#start" class="btn btn-primary">(See If You Qualify)</a>',
        r'<button type="button" class="btn btn-primary" onclick="showDisclosureModal()">\1</button>',
        text,
    )
    text = re.sub(
        r'<a href="#start" class="btn btn-primary" style="padding:0\.625rem 1\.5rem;font-size:0\.85rem;">(See If You Qualify)</a>',
        r'<button type="button" class="btn btn-primary" style="padding:0.625rem 1.5rem;font-size:0.85rem;" onclick="showDisclosureModal()">\1</button>',
        text,
    )
    # Start My Program (amber)
    text = re.sub(
        r'<a href="how-it-works\.html(?:#start)?" class="btn btn-amber" style="font-size:1\.05rem;padding:1rem 2\.5rem;">Start My Program →</a>',
        r'<button type="button" class="btn btn-amber" style="font-size:1.05rem;padding:1rem 2.5rem;" onclick="showDisclosureModal()">Start My Program →</button>',
        text,
    )
    text = re.sub(
        r'<a href="#start" class="btn btn-amber" style="font-size:1\.05rem;padding:1rem 2\.5rem;">Start My Program →</a>',
        r'<button type="button" class="btn btn-amber" style="font-size:1.05rem;padding:1rem 2.5rem;" onclick="showDisclosureModal()">Start My Program →</button>',
        text,
    )
    return text


def main() -> None:
    for path in aw_html_files():
        text = path.read_text(encoding="utf-8")
        if "Authentic Wellness" not in text and "authenticwellness" not in text.lower():
            continue
        orig = text
        text = text.replace(REFUND_OLD, REFUND_NEW)
        text = text.replace(FOOTER_OLD, FOOTER_NEW)
        text = re.sub(
            r'\s*<p style="display:none" id="not-available">Not available!</p>\s*',
            "\n",
            text,
        )
        text = patch_ctas(text)
        text = inject_qualiphy_head(text)
        text = inject_qualiphy_body(text)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            print("updated", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
