#!/usr/bin/env python3
"""Strip Qualiphy quidget from all HTML except thank-you.html; replace showDisclosureModal CTAs with Stripe .aw-checkout."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_NAMES = frozenset({"thank-you.html", "checkout-success.html"})

QUALIPHY_LINK_RE = re.compile(
    r"\s*<!--\s*Qualiphy Quidget Part 1[^>]*-->\s*"
    r"\n\s*<link rel=\"stylesheet\" href=\"https://firebasestorage\.googleapis\.com/v0/b/qualiphy-web-d918b[^>]+>\s*",
    re.MULTILINE,
)
QUALIPHY_LINK_BARE_RE = re.compile(
    r"\n\s*<link rel=\"stylesheet\" href=\"https://firebasestorage\.googleapis\.com/v0/b/qualiphy-web-d918b[^>]+>\s*\n",
)

QUALIPHY_FOOTER_RE = re.compile(
    r"\s*<!--\s*Qualiphy Quidget Part 3[^>]*-->\s*\n"
    r"\s*<script src=\"https://cdnjs\.cloudflare\.com/ajax/libs/moment\.js/2\.29\.1/moment\.min\.js\" defer></script>\s*\n"
    r"\s*<script id=\"qualiphy-script\"[\s\S]*?</script>\s*",
    re.MULTILINE,
)

# Pages that only have moment+quidget without Part 3 comment (e.g. some hubs)
QUALIPHY_TAIL_RE = re.compile(
    r"\n\s*<script src=\"https://cdnjs\.cloudflare\.com/ajax/libs/moment\.js/2\.29\.1/moment\.min\.js\" defer></script>\s*\n"
    r"\s*<script id=\"qualiphy-script\"[\s\S]*?</script>\s*",
    re.MULTILINE,
)


def strip_qualiphy(html: str) -> str:
    html = QUALIPHY_LINK_RE.sub("\n", html)
    # Remove bare qualiphy stylesheet links (one pass may leave none)
    prev = None
    while prev != html:
        prev = html
        html = QUALIPHY_LINK_BARE_RE.sub("\n", html)
    html = QUALIPHY_FOOTER_RE.sub("\n", html)
    html = QUALIPHY_TAIL_RE.sub("\n", html)
    return html


def fix_show_disclosure(html: str, rel_posix: str) -> str:
    if "checkout-success.html" in rel_posix:
        return html
    hero_slug = ""
    if rel_posix.endswith("programs/glp1-sema.html"):
        hero_slug = ' data-product-slug="semaglutide-starter"'
    elif rel_posix.endswith("programs/glp1-tirz.html"):
        hero_slug = ' data-product-slug="tirzepatide-starter"'
    old_hero = '<button type="button" class="btn btn-primary program-page-cta" onclick="showDisclosureModal()">Get Started</button>'
    new_hero = (
        f'<button type="button" class="btn btn-primary program-page-cta aw-checkout"{hero_slug} data-billing="monthly">Get Started</button>'
    )
    if hero_slug and old_hero in html:
        html = html.replace(old_hero, new_hero, 1)
    else:
        html = html.replace(
            old_hero,
            '<button type="button" class="btn btn-primary program-page-cta aw-checkout" data-billing="monthly">Get Started</button>',
        )
    html = html.replace(
        '<button type="button" class="btn btn-primary" onclick="showDisclosureModal()">Get Started</button>',
        '<button type="button" class="btn btn-primary aw-checkout" data-billing="monthly">Get Started</button>',
    )
    return html


def main() -> None:
    changed = []
    for path in sorted(ROOT.rglob("*.html")):
        if path.name in SKIP_NAMES:
            continue
        text = path.read_text(encoding="utf-8")
        if (
            "qualiphy-script" not in text
            and "qualiphy-web-d918b" not in text
            and "showDisclosureModal()" not in text
        ):
            continue
        rel = path.relative_to(ROOT).as_posix()
        new = strip_qualiphy(text)
        new = fix_show_disclosure(new, rel)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed.append(rel)
    for c in changed:
        print(c)
    print(f"Updated {len(changed)} files", file=sys.stderr)


if __name__ == "__main__":
    main()
