#!/usr/bin/env python3
"""Build the static site for docs/.

Converts every *.md file in docs/ into a standalone HTML page in site/,
with a shared template, table of contents, and stylesheet.

Usage:
    python3 build.py            # build site/ from docs/
    python3 build.py --out DIR  # build into a custom directory

Requires the `markdown` package:  python3 -m pip install markdown
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"

SITE_TITLE = "Keeping Up With AI (Calmly)"
SITE_TAGLINE = "A manual for following AI news without doomscrolling"
FOOTER = (
    "Keeping Up With AI (Calmly) — built as part of The Massive AI Manual "
    "by Asdale Dynamics, LLC. Educational content, not professional advice. "
    'Licensed under the <a href="https://opensource.org/licenses/MIT">MIT License</a>.'
)


def ordered_docs() -> list[Path]:
    """docs/index.md first, then numbered chapters in filename order."""
    files = sorted(DOCS.glob("*.md"), key=lambda p: p.name)
    index = [p for p in files if p.stem == "index"]
    chapters = [p for p in files if p.stem != "index"]
    return index + chapters


def extract_title(text: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else "Untitled"


def chapter_label(path: Path) -> str:
    return "Overview" if path.stem == "index" else f"Chapter {path.stem.split('-')[0]}"


def build_template(title: str, chapter: str, body: str, prev, nxt, pages, current: Path) -> str:
    """pages: list of (out_path, label); prev/nxt: (out_path, label) or None."""
    nav_items = "\n".join(
        f'<a href="{html.escape(out.name)}" class="{"current" if out == current else ""}">'
        f"{html.escape(label)}</a>"
        for out, label in pages
    )

    def link(page: tuple[Path, str] | None, direction: str) -> str:
        if page is None:
            return f'<span class="nav-{direction} empty"></span>'
        label, out = page
        return (
            f'<a class="nav-{direction}" href="{html.escape(out.name)}">'
            f"{direction.capitalize()}: {html.escape(label)}</a>"
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{html.escape(SITE_TAGLINE)}">
<title>{html.escape(title)} — {html.escape(SITE_TITLE)}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="site-header">
  <p class="site-title"><a href="index.html">{html.escape(SITE_TITLE)}</a></p>
  <p class="site-tagline">{html.escape(SITE_TAGLINE)}</p>
</header>
<div class="layout">
<nav class="toc" aria-label="Chapters">
{nav_items}
</nav>
<main>
<p class="chapter-label">{html.escape(chapter)}</p>
<article>
{body}
</article>
<nav class="pager" aria-label="Prev/next chapter">
{link(prev, "prev")}
{link(nxt, "next")}
</nav>
</main>
</div>
<footer>
<p>{FOOTER}</p>
<p>Prompted toward calm by Dylan Asdale · Further reading at
<a href="https://dylanasdale.github.io">dylanasdale.github.io</a></p>
</footer>
</body>
</html>
"""


STYLE = """/* Keeping Up With AI (Calmly) — no trackers, no fonts from the network. */
:root {
  --bg: #faf7f2;
  --ink: #2b2b28;
  --muted: #6d6a63;
  --accent: #2f6f4f;
  --accent-soft: #e3ede6;
  --card: #ffffff;
  --border: #e4dfd5;
  --code-bg: #f1ede4;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 17px;
  line-height: 1.65;
  color: var(--ink);
  background: var(--bg);
}
.site-header {
  padding: 2rem 1.5rem 1.2rem;
  background: var(--card);
  border-bottom: 3px solid var(--accent);
}
.site-title { margin: 0; font-size: 1.6rem; }
.site-title a { color: var(--ink); text-decoration: none; }
.site-tagline { margin: 0.25rem 0 0; color: var(--muted); font-style: italic; }
.layout {
  display: flex;
  gap: 2rem;
  max-width: 66rem;
  margin: 0 auto;
  padding: 1.5rem;
  align-items: flex-start;
}
nav.toc {
  flex: 0 0 14rem;
  position: sticky;
  top: 1rem;
  display: flex;
  flex-direction: column;
  border-left: 3px solid var(--accent-soft);
  padding-left: 0.75rem;
}
nav.toc a {
  color: var(--muted);
  text-decoration: none;
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-size: 0.92rem;
}
nav.toc a:hover { background: var(--accent-soft); color: var(--ink); }
nav.toc a.current { color: var(--accent); font-weight: bold; }
main { flex: 1 1 auto; min-width: 0; }
.chapter-label {
  color: var(--accent);
  font-weight: bold;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  font-size: 0.8rem;
  margin: 1rem 0 0;
}
article {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1.5rem 2rem 2rem;
  margin-top: 0.75rem;
}
h1 { font-size: 1.7rem; line-height: 1.25; margin-top: 0.25rem; }
h2 { color: var(--accent); margin-top: 2rem; }
a { color: var(--accent); }
blockquote {
  margin: 1.25rem 0;
  padding: 0.75rem 1.1rem;
  background: var(--accent-soft);
  border-left: 4px solid var(--accent);
  border-radius: 4px;
}
blockquote p { margin: 0; }
code {
  background: var(--code-bg);
  padding: 0.1em 0.35em;
  border-radius: 3px;
  font-size: 0.9em;
}
pre { background: var(--code-bg); padding: 0.75rem; border-radius: 6px; overflow-x: auto; }
pre code { padding: 0; background: none; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; font-size: 0.95rem; }
th, td { border: 1px solid var(--border); padding: 0.45rem 0.6rem; text-align: left; vertical-align: top; }
th { background: var(--accent-soft); }
input[type="checkbox"] { margin-right: 0.4rem; }
nav.pager { display: flex; justify-content: space-between; gap: 1rem; margin: 1.25rem 0 0; }
nav.pager a {
  color: var(--accent);
  text-decoration: none;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 0.45rem 0.8rem;
}
nav.pager a:hover { background: var(--accent-soft); }
nav.pager .empty { visibility: hidden; }
nav.pager a.nav-prev { margin-right: auto; }
nav.pager a.nav-next { margin-left: auto; }
footer {
  border-top: 1px solid var(--border);
  margin: 2.5rem 1.5rem 0;
  padding: 1.25rem 0 2rem;
  color: var(--muted);
  font-size: 0.9rem;
  max-width: 66rem;
  margin-left: auto;
  margin-right: auto;
}
@media (max-width: 56rem) {
  .layout { flex-direction: column; }
  nav.toc { position: static; flex-basis: auto; border-left: none; padding-left: 0; }
}
"""


def render_markdown(text: str) -> str:
    body = markdown.markdown(
        text,
        extensions=["tables", "sane_lists", "smarty", "attr_list"],
        output_format="html5",
    )
    # Rewrite intra-doc links so the built site is self-contained:
    # [x](01-chapter.md) -> 01-chapter.html ; [x](../LICENSE) -> LICENSE
    body = re.sub(r'(href=")([^"#]*?)\.md(["#])', r"\1\2.html\3", body)
    body = body.replace('href="../LICENSE"', 'href="LICENSE"')
    return body


def build(out_dir: Path) -> list[Path]:
    """Render docs/*.md into out_dir, plus stylesheet and LICENSE. Returns paths written."""
    if not DOCS.exists():
        sys.exit(f"error: docs/ not found at {DOCS}")
    out_dir.mkdir(parents=True, exist_ok=True)

    sources = ordered_docs()
    rendered = []
    for src in sources:
        text = src.read_text(encoding="utf-8")
        rendered.append(
            (src, extract_title(text), chapter_label(src), render_markdown(text))
        )

    # (label, out_path) pairs preserve reading order for TOC and prev/next links.
    page_pairs = [
        (f"{chapter_label(src)} — {title}", out_dir / f"{src.stem}.html")
        for src, title, _, _ in rendered
    ]
    # The template wants (out_path, label) tuples; used only for "current page" check.
    nav_for_template = [(out, label) for label, out in page_pairs]

    written: list[Path] = []
    for i, ((src, title, chapter, body), (_, out)) in enumerate(zip(rendered, page_pairs)):
        prev = page_pairs[i - 1] if i > 0 else None
        nxt = page_pairs[i + 1] if i + 1 < len(page_pairs) else None
        html_text = build_template(title, chapter, body, prev, nxt, nav_for_template, out)
        out.write_text(html_text, encoding="utf-8")
        written.append(out)

    (out_dir / "style.css").write_text(STYLE, encoding="utf-8")
    written.append(out_dir / "style.css")
    shutil.copyfile(ROOT / "LICENSE", out_dir / "LICENSE")
    written.append(out_dir / "LICENSE")
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "site", help="output directory")
    parser.add_argument("--clean", action="store_true", help="remove the output dir first")
    args = parser.parse_args()
    if args.clean and args.out.exists():
        shutil.rmtree(args.out)
    written = build(args.out)
    print(f"Built {len(written)} files into {args.out}:")
    for path in written:
        print(f"  {path.name}")


if __name__ == "__main__":
    main()
