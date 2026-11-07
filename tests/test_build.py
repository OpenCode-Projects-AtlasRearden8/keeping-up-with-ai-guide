#!/usr/bin/env python3
"""Build verification tests for Keeping Up With AI (Calmly).

Run with:
    python3 -m unittest discover -s tests -v

Builds the site into a temporary directory (never touching site/) and
checks content integrity, link integrity, template sanity, and the
required attribution lines.
"""

from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT))

import build as sitebuild  # noqa: E402

EXPECTED_Copyright = "Copyright (c) 2026 Asdale Dynamics, LLC"
SECRET_PATTERNS = [
    r"sk-[A-Za-z0-9]{20,}",  # OpenAI-style API key
    r"AKIA[0-9A-Z]{16}",  # AWS access key
    r"ghp_[A-Za-z0-9]{20,}",  # GitHub token
    r"xoxb-[0-9A-Za-z-]{10,}",  # Slack token
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",  # PEM key
]


class BuildTestCase(unittest.TestCase):
    """Tests run against a fresh build in a temp dir (classmethod setup)."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name) / "site"
        cls.written = sitebuild.build(cls.out)
        cls.pages = sorted(p for p in cls.out.glob("*.html"))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_every_doc_is_built(self):
        docs = {p.stem for p in DOCS.glob("*.md")}
        built = {p.stem for p in self.pages}
        self.assertEqual(docs, built, "every docs/*.md must produce a matching html")

    def test_pages_are_nonempty_html(self):
        for page in self.pages:
            text = page.read_text(encoding="utf-8")
            self.assertIn("<!DOCTYPE html>", text, page.name)
            self.assertIn("<article>", text, page.name)
            self.assertGreater(len(text), 500, f"{page.name} suspiciously small")

    def test_site_title_everywhere(self):
        for page in self.pages:
            text = page.read_text(encoding="utf-8")
            self.assertIn(sitebuild.SITE_TITLE, text, page.name)

    def test_number_of_chapters(self):
        md_files = list(DOCS.glob("*.md"))
        self.assertEqual(len(md_files), 9)  # index + 8 chapters
        chapters = [p for p in md_files if p.stem != "index"]
        self.assertEqual(len(chapters), 8)
        self.assertEqual(len(self.pages), 9)

    def test_stylesheet_written(self):
        css = (self.out / "style.css").read_text(encoding="utf-8")
        self.assertIn("--accent", css)

    def test_license_copied_into_site(self):
        license_text = (self.out / "LICENSE").read_text(encoding="utf-8")
        self.assertIn(EXPECTED_Copyright, license_text)

    def test_prev_next_links(self):
        first = (self.out / "index.html").read_text(encoding="utf-8")
        self.assertIn('class="nav-next" href="01-trustworthy-free-sources.html"', first)
        self.assertIn('class="nav-prev empty"', first)
        last = (self.out / "08-newsletter-recipes.html").read_text(encoding="utf-8")
        self.assertIn('class="nav-prev" href="07-rss-recipes.html"', last)
        self.assertIn('class="nav-next empty"', last)

    def test_toc_marks_first_page_current(self):
        first = (self.out / "index.html").read_text(encoding="utf-8")
        second = (self.out / "01-trustworthy-free-sources.html").read_text(encoding="utf-8")
        self.assertIn('href="index.html" class="current"', first)
        self.assertIn('href="01-trustworthy-free-sources.html" class="current"', second)

    def test_nav_links_point_to_existing_pages(self):
        for page in self.pages:
            text = page.read_text(encoding="utf-8")
            hrefs = re.findall(r'href="([A-Za-z0-9-]+\.html)"', text)
            for href in set(hrefs):
                self.assertTrue((self.out / href).exists(), f"{page.name} -> {href}")

    def test_no_broken_raw_markdown(self):
        for page in self.pages:
            text = page.read_text(encoding="utf-8")
            self.assertNotIn("](#", text, f"{page.name}: unprocessed markdown link")
            self.assertNotRegex(text, r"\]\(.*?\.md\)", f"{page.name}: .md link not converted")


class ContentTestCase(unittest.TestCase):
    """Static checks over docs/, README, LICENSE, and built text."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        sitebuild.build(Path(cls.tmp.name) / "site")
        cls.site_blobs = {
            p.name: p.read_text(encoding="utf-8")
            for p in (Path(cls.tmp.name) / "site").iterdir()
        }
        cls.doc_texts = {
            p.name: p.read_text(encoding="utf-8") for p in DOCS.glob("*.md")
        }

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def _all_project_text(self) -> str:
        blobs = list(self.doc_texts.values()) + list(self.site_blobs.values())
        blobs.append((ROOT / "README.md").read_text(encoding="utf-8"))
        blobs.append((ROOT / "LICENSE").read_text(encoding="utf-8"))
        return "\n".join(blobs)

    def test_license_copyright_line_exact(self):
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        self.assertIn(f"MIT License\n\n{EXPECTED_Copyright}", license_text)
        self.assertEqual(
            license_text.count("Asdale Dynamics"), 1,
            "copyright line appears exactly once in LICENSE",
        )

    def test_readme_credits(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Asdale Dynamics, LLC", readme)

    def test_no_secrets_anywhere(self):
        for pattern in SECRET_PATTERNS:
            self.assertNotRegex(self._all_project_text(), pattern, f"leaked secret: {pattern}")

    def test_no_placeholder_text(self):
        text = self._all_project_text()
        self.assertNotIn("TODO", text)
        self.assertNotIn("TBD", text)
        self.assertNotIn("PLACEHOLDER", text.upper())

    def test_docs_cover_required_topics(self):
        joined = " ".join(self.doc_texts.values()).lower()
        for topic in [
            "trustworthy", "changelog", "hype", "experiment",
            "quarterly", "worry", "rss", "newsletter",
        ]:
            self.assertIn(topic, joined, f"missing topic: {topic}")

    def test_each_chapter_has_at_least_one_table_or_checklist(self):
        self.assertIn("|", self.doc_texts["index.md"])          # chapter table
        self.assertIn("|", self.doc_texts["03-hype-words-to-discount.md"])  # decoder table
        self.assertIn("- [ ]", self.doc_texts["05-quarterly-toolbox-refresh.md"])  # checklist


if __name__ == "__main__":
    unittest.main(verbosity=2)
