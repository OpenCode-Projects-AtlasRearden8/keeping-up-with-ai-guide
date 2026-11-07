# STATUS.md — Keeping Up With AI (Calmly)

Last updated: 2026-11-07

## What was built

A complete, beginner-friendly manual for following AI news calmly instead of doomscrolling, plus a generated static site.

- **docs/** — 9 Markdown documents (source of truth):
  - `index.md` — overview: the whole guide in five lines, chapter map
  - `01` — trustworthy free sources (primary sources, honest aggregators, digests, skip list, a copy-this starter stack of five)
  - `02` — skimming changelogs in minutes (a 5-minute method, pattern cheat sheet, worked example)
  - `03` — hype words to discount (decoder tables, the 3-question discount method)
  - `04` — one experiment a month (habit, queue, rules, a sample year)
  - `05` — quarterly toolbox refresh (60-minute keep/cut/upgrade checklist in 4 blocks)
  - `06` — boundaries on AI worry posts (7 written-down boundaries)
  - `07` — RSS recipes (reader picks, 3 feed stacks, folder layout, email fallback)
  - `08` — newsletter recipes (cadence rule, pickup list, folder/filter rules, combined stack)
- **build.py** — static site generator (Python stdlib + the `markdown` package). Renders every `docs/*.md` to `site/*.html` with shared template, sticky table of contents, prev/next chapter links, stylesheet, and a copied LICENSE. Rewrites intra-doc `.md` links to `.html`.
- **site/** — generated static site: 9 HTML pages + `style.css` + `LICENSE`. No JavaScript, no trackers, no external font/network requests.
- **tests/test_build.py** — 16 verification tests (content, links, template, attribution, secrets scan).
- **README.md** — overview, run/rebuild/test instructions, credits to Asdale Dynamics, LLC.
- **LICENSE** — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`.

## How to run it

```bash
# View the site
python3 -m http.server 8080 --directory site   # then open http://localhost:8080

# Rebuild the site from docs/
python3 -m pip install markdown    # one-time dependency
python3 build.py                   # or: python3 build.py --clean

# Run the tests
python3 -m unittest discover -s tests -v
```

## Verification results (this date, on this machine)

- `python3 build.py` — OK: builds 11 files (9 HTML pages, style.css, LICENSE) into `site/`.
- `python3 -m unittest discover -s tests -v` — OK: **16/16 tests passed**, covering:
  - every `docs/*.md` produces a matching HTML page (9 pages)
  - all internal nav/prev/next links point to existing pages; no stray raw Markdown links or `.md` hrefs in built pages
  - site title and DOCTYPE/article structure present on every page; first-page "current" TOC marking works
  - LICENSE copied into site; exact copyright line present in LICENSE exactly once
  - README credits Asdale Dynamics, LLC
  - no secret patterns (API keys, tokens, PEM blocks) anywhere in docs/site/README/LICENSE
  - no TODO/TBD/placeholder text; all required topics present
- Live smoke test: `http.server` on port 8741 returned HTTP 200 for `index.html`, a chapter page, and `style.css`.
- Git: initialized and committed in-folder with the existing identity; nothing pushed, no remote.

## Known gaps / notes

- Feed URLs in Chapters 1, 7–8 are correct as of writing; provider RSS endpoints occasionally change — the recipes include feed-finder fallbacks for that case.
- `- [ ]` checklist items render as literal `[ ]` text (tracked input styling was skipped deliberately to keep the build stdlib-only).
- The site has no search; the sticky chapter list and per-page tables of contents are the only navigation aids.
- Newsletter/feed names are editorial picks, not endorsements by any provider; all sources listed are free tiers.
- No CI configured; run the unittest command above after edits (intended as a local-first project).
- Educational content only — not legal, financial, medical, or professional advice.
