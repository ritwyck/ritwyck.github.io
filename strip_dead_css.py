#!/usr/bin/env python3
"""Remove dead CSS from the portfolio page.

Usage: python3 strip_dead_css.py index.html
Writes index.clean.html next to the input and leaves the original untouched.
"""
import re
import sys
from pathlib import Path

src = Path(sys.argv[1])
html = src.read_text(encoding="utf-8")
before = len(html)

# 1. The big block of demo-preview CSS. The script replaces every
#    .workflow-preview with a <video>, so none of this ever renders.
#    It runs from the first top-level `.workflow-preview {` rule up to
#    (not including) the first top-level `.project-detail {` rule.
start_re = re.compile(r"^    \.workflow-preview \{\n      position: absolute;", re.M)
end_re = re.compile(r"^    \.project-detail \{\n      position: absolute;", re.M)

starts = start_re.findall(html)
ends = end_re.findall(html)
if len(starts) != 1 or len(ends) != 1:
    sys.exit(f"Expected one start and one end marker, found {len(starts)} and {len(ends)}. Aborting.")

s = start_re.search(html).start()
e = end_re.search(html).start()
if s >= e:
    sys.exit("Start marker appears after end marker. Aborting.")
html = html[:s] + html[e:]

# 2. `.is-closing` is never added anywhere in the JS.
html, n_closing = re.subn(
    r"[ ]*\.project-card\.is-closing \.project-detail \{[^}]*\}\n", "", html
)

# 3. Unused custom property.
html, n_pale = re.subn(r"[ ]*--pale: #f7f7f7;\n", "", html)

out = src.with_name(src.stem + ".clean" + src.suffix)
out.write_text(html, encoding="utf-8")
print(f"Removed demo block, {n_closing} .is-closing rule(s), {n_pale} unused variable(s)")
print(f"{before:,} -> {len(html):,} bytes ({before - len(html):,} saved)")
print(f"Wrote {out}")
