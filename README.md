# Keeping Up With AI (Calmly)

*A manual for following AI news without doomscrolling.*

You don't need to read everything to stay current. You need five trustworthy sources, a five-minute changelog habit, a working filter for hype, and a schedule for trying new tools. This guide gives you exactly that — plain English, step by step, like a friend would explain it.

## What's inside

| Chapter | What it covers |
|---|---|
| [1. Trustworthy free sources](docs/01-trustworthy-free-sources.md) | A short curated list — pick five, that's the whole stack |
| [2. Skim changelogs in minutes](docs/02-skim-changelogs-in-minutes.md) | A reusable 5-minute method for release notes |
| [3. Hype words to discount](docs/03-hype-words-to-discount.md) | What "breakthrough" actually means, and friends |
| [4. One experiment a month](docs/04-one-experiment-a-month.md) | A calm tool-testing habit instead of panic-upgrading |
| [5. Quarterly toolbox refresh](docs/05-quarterly-toolbox-refresh.md) | A 60-minute checklist to keep, cut, and upgrade |
| [6. Boundaries on AI worry posts](docs/06-worry-post-boundaries.md) | Seven rules for the anxiety side of AI discourse |
| [7. RSS recipes](docs/07-rss-recipes.md) | Copy-paste feed setups and folder layouts |
| [8. Newsletter recipes](docs/08-newsletter-recipes.md) | One daily, one weekly, one monthly — and folder rules |

Start with [the overview](docs/index.md) for the whole guide in five lines.

## Run the site locally

The `site/` directory is a plain static site — no tracker, no web fonts, no JavaScript.

```bash
# Option A: serve it (recommended, needed for relative links to look right)
python3 -m http.server 8080 --directory site
# then open http://localhost:8080

# Option B: just open the file
# open site/index.html in any browser
```

## Rebuild the site from `docs/`

```bash
python3 -m pip install markdown   # one-time dependency
python3 build.py                  # writes site/*.html + style.css + LICENSE
python3 build.py --clean          # wipe site/ before rebuilding
python3 build.py --out /tmp/site  # build somewhere else
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

The tests rebuild the site into a temp directory and verify: every chapter
renders, internal links resolve, the template is valid HTML-shaped output,
no secrets patterns appear anywhere, and the LICENSE/README contain the
required attribution.

## Repository layout

```
docs/    The guide itself (Markdown, the source of truth)
site/    Generated static site (rebuild with build.py)
tests/   Build verification tests
build.py Static site generator
```

## About

This project is maintained by **Asdale Dynamics, LLC** as part of *The Massive AI Manual* — beginner-friendly AI education in plain English. Hub site: [dylanasdale.github.io](https://dylanasdale.github.io).

It pairs well with two sibling guides: *AI Benchmarks Explained* (how to read model rankings) and *AI Personal Policy* (writing your own rules for AI use).

Everything here is educational content, **not** professional, legal, financial, or medical advice. Licensed under the MIT License — see [LICENSE](LICENSE).
