#!/usr/bin/env python3
"""Insert compound-default hero <picture> after opening program-page-hero > container if missing."""
from __future__ import annotations

import pathlib

SNIPPET = """ <div class="program-hero-media">
        <picture>
          <source srcset="../assets/img/programs/compound-default.webp" type="image/webp">
          <source srcset="../assets/img/programs/compound-default.jpg" type="image/jpeg">
          <img src="../assets/img/programs/compound-default.jpg" alt="Clinical laboratory context for physician-prescribed peptide programs" width="1920" height="1080" class="program-hero-img" loading="lazy" decoding="async">
        </picture>
      </div>
"""

SKIP = {"perform.html", "renew.html", "recovery.html", "discovery.html"}


def main() -> None:
    root = pathlib.Path(__file__).resolve().parents[1] / "programs"
    for path in sorted(root.glob("*.html")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        if "program-hero-media" in text:
            continue
        needle = '<header class="program-page-hero">\n    <div class="container">'
        if needle not in text:
            needle = '<header class="program-page-hero">\r\n    <div class="container">'
        if needle not in text:
            continue
        text = text.replace(needle, needle + "\n" + SNIPPET, 1)
        path.write_text(text, encoding="utf-8")
        print("patched", path.name)


if __name__ == "__main__":
    main()
