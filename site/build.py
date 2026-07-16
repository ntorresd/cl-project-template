#!/usr/bin/env python3
"""Build the GitHub Pages site: render README.md's steps into site/template.html."""
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DIST = ROOT / "dist"

readme = (ROOT / "README.md").read_text()

# Drop the leading "# Project Template" title — the page shell already has its own H1.
body = re.sub(r"^#\s+.*\n", "", readme, count=1).lstrip("\n")

html = markdown.markdown(body, extensions=["fenced_code"])

# README's "## N. Title" steps become <h2>; demote to <h3> (the shell's own
# <h2> is the section title) and pull the leading number into its own span.
html = html.replace("<h2>", "<h3>").replace("</h2>", "</h3>")
html = re.sub(
    r"<h3>(\d+)\.\s+(.*?)</h3>",
    r'<h3><span class="step-num">\1</span>\2</h3>',
    html,
)

template = (SITE / "template.html").read_text()
page = template.replace("{{STEPS_CONTENT}}", html)

DIST.mkdir(exist_ok=True)
(DIST / "index.html").write_text(page)
print(f"Wrote {DIST / 'index.html'} ({len(page)} bytes)")
