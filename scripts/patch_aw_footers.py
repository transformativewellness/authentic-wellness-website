#!/usr/bin/env python3
"""Normalize Authentic Wellness footer Programs column to six compound-first categories."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {"transformativemedspa-website", "transformative-wellness-website", "node_modules", ".git"}

PAT = re.compile(
    r'(<p class="footer-col-title">Programs</p>\s*(?:<p class="compliance-disclaimer"[^>]*>.*?</p>\s*)?)<div class="footer-links">.*?</div>',
    re.DOTALL,
)

REPL_ROOT = r"""\1          <div class="footer-links">
            <a href="programs/weight-loss.html">Weight loss</a>
            <a href="programs/muscle-performance.html">Muscle &amp; performance</a>
            <a href="programs/recovery-healing.html">Recovery &amp; healing</a>
            <a href="programs/longevity.html">Longevity</a>
            <a href="programs/sexual-health.html">Sexual health</a>
            <a href="programs/hair-skin.html">Hair &amp; skin</a>
            <a href="programs.html">All programs</a>
          </div>"""

REPL_PROG = r"""\1          <div class="footer-links">
            <a href="weight-loss.html">Weight loss</a>
            <a href="muscle-performance.html">Muscle &amp; performance</a>
            <a href="recovery-healing.html">Recovery &amp; healing</a>
            <a href="longevity.html">Longevity</a>
            <a href="sexual-health.html">Sexual health</a>
            <a href="hair-skin.html">Hair &amp; skin</a>
            <a href="../programs.html">All programs</a>
          </div>"""

REPL_BLOG = r"""\1          <div class="footer-links">
            <a href="../programs/weight-loss.html">Weight loss</a>
            <a href="../programs/muscle-performance.html">Muscle &amp; performance</a>
            <a href="../programs/recovery-healing.html">Recovery &amp; healing</a>
            <a href="../programs/longevity.html">Longevity</a>
            <a href="../programs/sexual-health.html">Sexual health</a>
            <a href="../programs/hair-skin.html">Hair &amp; skin</a>
            <a href="../programs.html">All programs</a>
          </div>"""


def main() -> None:
    for path in sorted(ROOT.rglob("*.html")):
        if SKIP_DIRS & set(path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        if 'footer-col-title">Programs' not in text:
            continue
        rel = path.relative_to(ROOT)
        if rel.parts[:1] == ("blog",):
            repl = REPL_BLOG
        elif len(rel.parts) >= 2 and rel.parts[0] == "programs":
            repl = REPL_PROG
        else:
            repl = REPL_ROOT
        new, n = PAT.subn(repl, text, count=1)
        if n and new != text:
            path.write_text(new, encoding="utf-8")
            print("patched", rel)


if __name__ == "__main__":
    main()
