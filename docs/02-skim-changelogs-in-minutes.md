# 2. Skim changelogs in minutes

Release notes are the best reading in AI: short, factual, and written by the people who shipped the thing. The trick is reading them like an editor, not like a worried student. Here's a five-minute method you can reuse for **any** changelog — OpenAI's, Anthropic's, VS Code's, your library's.

## The 5-minute skim

**Minute 1 — Scan the dates and version numbers.**
Changelogs are written newest-first. You only care about entries *since the last time you looked*. If the top entry predates your last visit, you're done — close the tab. That's the whole habit: verifying *nothing happened* is a legitimate, fast outcome.

**Minute 2 — Read only the item titles.**
Titles are the news; the paragraphs are the marketing. A title like *"GPT model updated — improved coding and instruction following, fixed X"* carries 90% of the signal. List in your head: new model? capability change? pricing change? bug fix?

**Minute 3 — Open at most one entry.**
Pick the single item that touches something **you actually use**. Skim its bullet list for: capabilities added, capabilities removed, price changes, known issues. You are looking for sentences with emojis removed: *does X now work, stop working, or cost differently?*

**Minute 4 — Translate to your own tools.**
One sentence, written by you: *"Claude got better at spreadsheets — fine, I already use it for that."* If nothing in the changelog touches your usage, write down nothing. **"Nothing applies to me" is a real conclusion**, and it's usually the right one.

**Minute 5 — Decide the monthly experiment.**
Does this change anything about your [one experiment a month](04-one-experiment-a-month.md)? If yes, add it to a note. If no, you're finished. Total contact time: 5 minutes, no feed, no takes.

## Patterns that save time once you know them

- **"Improved performance/reasonability/coding"** = incremental. Nothing to do.
- **"New model, same price"** = note it, let a week of other people's testing pass, then consider swapping.
- **"Deprecated / removed"** = the warrantied-action category. Check: *do I still rely on this?* If yes, this is your one change this month.
- **"Safety / usage policy update"** = skim once. Rarely changes your workflow.
- **Pricing changes** = the highest-value 30 seconds in any changelog. Always read these.

## A concrete worked example

Anthropic posts: *"Updated Claude — improved math and coding, new tool use format, deprecates old API version."*

- It touches you if you write code or use tools with Claude. Title scan says: models refresh, one deprecation. Two minutes in, you know the shape.
- You open only the deprecation note, confirm the deadline, and write: *"switch my script off `claude-3-old` before March."* That's your month's change. Five minutes, done, calm.
- You did **not** read twelve tweets about what the "improved math" means. Someone with a test suite will tell the community by Friday; you'll see it in your weekly skim.

## Why skim beats read

You are not trying to have an opinion an hour after release. You're trying to keep your tools working and notice genuine upgrades within a week. A five-minute changelog skim does both; doomscrolling does neither.

> **The one-line habit:** *reader mode, newest-first, one entry deep, one sentence of notes.*
