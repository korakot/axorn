---
type: plan
title: "Plan"
description: "What's next for axorn, with resume pointers: web demo, npm/PyPI, Myanmar and Sinhala tables; Chinese is out of scope"
tags: [plan]
status: draft
generated: {by: claude-opus-5-5, at: 2026-10-14}
sources:
  - {id: s1, resource: "https://claude.ai/code/session_01PvCxrqAVyYE7nvuAULgx7A", title: "Claude Code session that built axorn 0.1.0 (14 Oct 2026)", last_modified: 2026-10-14}
---

# Plan

axorn 0.1.0 converts Pāli between roman and Thai in Python and JS, and matches the VRI Thai edition (see [history](history.md)). The items below are candidates in the order we discussed them. Each says where it stands and what the first step would be, so either Kora or a new Claude chat can pick it up.[^s1]

## 1. Web demo on GitHub Pages

**Why:** let people paste text and convert it in the browser, as a demo and as a small online service. Nothing is sent to a server, because the converter is pure JS.

**Stands at:** discussed, not started.

**Approach agreed so far:** an `index.html` at the repo root that imports `axorn/axorn.js` directly, so the page always runs the library's own code. GitHub Pages serves it at `korakot.github.io/axorn` and updates on every push. Put that link in the repo's About box.

**Before starting:**
- GitHub Pages on a free plan needs the repo to be public; a private repo needs GitHub Pro.
- The JSON import in `axorn.js` (`import … with { type: "json" }`) needs a recent browser (Safari 17.2+, Chrome 123+). If older browsers matter, add a tiny build step that inlines the table.

**First step:** in a new chat, attach `korakot/axorn` and ask for the page. It's a design task, so the chat can make the page with the design tools and then commit it.

## 2. Publish to npm and PyPI

**Why:** GitHub installs already work, so publishing isn't needed for the MBU backend or our own scripts:

```
pip install git+https://github.com/korakot/axorn
npm install github:korakot/axorn
```

npm matters for one reason: Claude artifacts and widgets only load scripts from jsDelivr's `/npm/` path, not its GitHub path. Being on npm is what lets an artifact `import` axorn from `cdn.jsdelivr.net/npm/axorn`.

**Stands at:** both names (`axorn`) were free on npm and PyPI on 14 Oct 2026. `package.json` and `pyproject.toml` are ready at version 0.1.0.

**When:** after the API settles, probably after the Myanmar table (item 3), because adding scripts may reshape the function names (for example a general `convert(text, from, to)`).

**How:** GitHub Actions with trusted publishing on both registries, so no tokens need handling.

## 3. More scripts: Myanmar and Sinhala

**Why:** Pāli texts circulate in these scripts too, and VRI publishes every book in each, so the same test method works.

**Design:** roman stays the hub. Add one table per script (`myanmar.json`, `sinhala.json`) next to `thai.json`, and any script → any script goes through roman. See [design](design.md).

**What's different from Thai:**
- Both scripts store vowels in spoken order, while Thai writes เ/โ before the consonant.
- Both have their own independent vowel letters instead of Thai's อ carrier.
- Myanmar also stacks consonants (U+1039) and writes y/r/v/h clusters as medials (ျ ြ ွ ှ), so it needs rule flags beyond a plain table.

So each script is a table plus a few flags, and the code gains a generic path.

**First step:** in a new chat, fetch one VRI book in `romn/` and `mymr/` (or `sinh/`), look at how clusters are written, then draft the table and run `tests/vri_check.py` generalised to any script pair.

**Order:** Sinhala first. It is closer to Thai (plain virama, no medials), so it will show whether the generic design holds before Myanmar's harder rules.

## Out of scope: Chinese

Chinese does not spell Pāli sound by sound. It uses conventional transcriptions chosen term by term, often from Sanskrit (涅槃 for *nibbāna*), or translates by meaning. Mapping Pāli to Chinese is a dictionary task, not a script conversion, so it does not belong in axorn. If it's needed, it fits the pali wiki's Chinese Tipiṭaka work instead.

## Smaller items

- **Option to keep roman capitals** when going Thai → roman, e.g. by copying case from a reference text. Only if a real use appears.
- **More VRI books in the test.** Six books pass (see [vri-conventions](vri-conventions.md)). Running the whole canon once would confirm the dot rule at scale.

[^s1]: Claude Code session that built axorn 0.1.0 (14 Oct 2026) — https://claude.ai/code/session_01PvCxrqAVyYE7nvuAULgx7A
