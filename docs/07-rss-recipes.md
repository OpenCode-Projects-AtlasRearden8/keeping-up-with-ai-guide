# 7. RSS recipes

RSS is the single best anti-doomscroll technology: news comes **to** a quiet reader on **your** schedule, with no algorithm deciding what you see and no infinite feed. This chapter is copy-paste-style recipes for setting up an AI news reader in about 20 minutes, once.

## Quick primer

An RSS **feed** is a webpage a site publishes that lists its recent posts (title, date, link, sometimes a summary). An RSS **reader** is an app that collects feeds from many sites into one list. You add a feed by pasting a URL; from then on, new posts appear automatically. No account tracking, no engagement ranking.

## Pick a reader (5 minutes)

Any of these is fine — the recipe works the same in all:

- **Thunderbird** (desktop, free): you already may use it for email; add "Feeds" account.
- **Feedbro**: a browser extension reader; zero extra apps to install.
- **NetNewsWire** (Mac/iOS; open source) or **FeedMe** (Android): polished, free.
- **FreshRSS** (self-hosted): local-first if you like running tiny services.
- **Miniflux / Readwise Reader / Feedbin**: hosted and paid, but the cheapest tiers are fine.

> One reader. Not two. Feeds sync across tools poorly until you get a hosted one — start single-device.

## Recipe A — The minimal five-feed stack (recommended)

Add these five, done:

1. `https://openai.com/blog/rss.xml` — OpenAI announcements.
2. `https://www.anthropic.com/rss.xml` or their news page feed — Anthropic releases. (If the raw URL fails, search the reader's built-in feed finder for "Anthropic news.")
3. `https://www.simonwillison.net/atom/by-date/` (or just his homepage feed) — everyday practitioner notes.
4. Your chosen weekly digest's feed — for example, search your reader's feed finder for **"The Batch"** (DeepLearning.AI) and subscribe. Weekly, calm, five minutes.
5. `https://www.tldr.tech/ai/rss.xml` — TLDR AI's daily three-minute roundup.

That's a ~5-minutes-a-week feed diet. Start here even if you add more later.

## Recipe B — The practitioner's expanded stack

Add on top of Recipe A if you like reading:

- `https://huggingface.co/blog/feed.xml` — Hugging Face blog.
- `https://arxiv.org/rss/cs.CL` — new computational-linguistics papers, title-only skim. (See triage rules below.)
- `https://www.interconnects.ai/feed` — open-models commentary.
- Mistral and Meta AI news feeds (search their news pages in your reader's finder).
- `https://blog.google/technology/ai/rss/` — Google AI blog.

**arXiv triage rule:** titles only, 20 seconds, mark-all-read daily. Read **one** paper's abstract a week max. arXiv is a firehose of drafts, not news; treat titles like weather radar, not like homework.

## Recipe C — Folder layout (10 seconds, saves hours)

In your reader, make three folders:

- **00 - Must** (the five feeds of Recipe A) — you read these.
- **01 - Skim** (expanded stack) — read *titles only*; open at most one item.
- **02 - Collapse** (r/LocalLLaMA, forums, aggregators) — open once a week knowing it might contain nothing.

Read in that order. When you run out of time, folders 01 and 02 get **Select All → Mark Read** with zero guilt. Marking all read is the *point* of a reader, not a failure of it.

## Recipe D — Twitter/X and Reddit, without the feeds

Both have nonstandard or restricted feeds. Calm alternatives:

- Use reader-friendly mirrors sparingly, or subscribe to **community roundups** instead: r/LocalLLaMA's weekly recap posts, Hugging Face papers-of-the-week.
- If you must follow real-time coverage, window it: site opens at set times (say, Tuesday/Thursday lunch), never on the home screen of your phone.

## Recipe E — Email fallback (Blogtrottr style)

If you live in email already, tools like Blogtrottr, Feedly's email digests, or mailbrew can turn RSS feeds into digest emails. Use one shared convention:

- Send digests to a **dedicated folder** via your mail rules (Chapter 8's folder setup), each daily or weekly.
- The digest rule: **email digests arrive summarized**; you read headlines, open one, done.

## Monthly RSS maintenance (2 minutes)

- Any feed with 0 items opened in 30 days → delete it (or demote to folder 02).
- Any feed spewing >20 items/day you never open → delete; it's noise displacement.
- Found yourself opening the same site outside the reader? Add its feed instead.

> The reader is a **river without a dam**: posts flow past, you cup your hands when convenient, and everything you didn't catch is *gone tomorrow* — and that's fine. That expiry is the feature.
