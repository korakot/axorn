---
type: plan
title: "Plan"
description: "What's next for axorn, with resume pointers: web demo live on GitHub Pages, npm/PyPI next with current names, other scripts parked ~1 year; Chinese out of scope"
tags: [plan]
status: draft
generated: {by: claude-opus-5-5, at: 2026-10-14}
sources:
  - {id: s1, resource: "https://claude.ai/code/session_01PvCxrqAVyYE7nvuAULgx7A", title: "Claude Code session that built axorn 0.1.0 (14 Oct 2026)", last_modified: 2026-10-14}
  - {id: s2, resource: "https://claude.ai/code/session_017UQaAboga3Y59zY8wvPTVA", title: "Claude Code session that reordered the plan and built the web demo (14 Oct 2026)", last_modified: 2026-10-14}
---

# Plan

axorn 0.1.0 converts Pāli between roman and Thai in Python and JS, and matches the VRI Thai edition (see [history](history.md)). Each item below says where it stands and what the next step would be, so either Kora or a new Claude chat can pick it up.[^s1]

**Status, 14 Oct 2026:** items 1 and 2 are done; 0.1.0 is on PyPI (`axorn`) and npm (`@korakot/axorn`). **Order, decided 14 Oct 2026:** web demo, then npm and PyPI, then other scripts. Kora doesn't expect to need another script for about a year, so publishing no longer waits for the API to settle around more scripts.[^s2]

## 1. Web demo on GitHub Pages — live

**Why:** let people paste text and convert it in the browser, as a demo and as a small online service. Nothing is sent to a server, because the converter is pure JS.

**Stands at:** built and published at <https://korakot.github.io/axorn/>, served from `index.html` at the repo root on `main`. The page imports `axorn/axorn.js` by relative path, so every push to `main` updates the demo with the library's own code; no npm or build step is involved.

**How it works:** two textareas, roman and Thai, styled as palm leaves on one cord. Editing either one converts into the other as you type, and the two options (`ue`, `punct`) re-run the conversion from the leaf last edited. Text converted from Thai comes back lower case, since Thai has no capitals.

**Known limit:** the JSON import in `axorn.js` (`import … with { type: "json" }`) needs a browser from 2024 or later (Chrome 123+, Safari 17.2+, Firefox 138+). Older browsers get a message asking them to update. If that turns out to matter, add a tiny build step that inlines the table.

## 2. Publish to npm and PyPI — done (0.1.0)

**Why:** GitHub installs already work for the MBU backend and our own scripts:

```
pip install git+https://github.com/korakot/axorn
npm install github:korakot/axorn
```

npm matters for one reason: Claude artifacts and widgets only load scripts from jsDelivr's `/npm/` path, not its GitHub path. Being on npm is what lets an artifact `import` axorn from `cdn.jsdelivr.net/npm/@korakot/axorn`.

**Names:** PyPI is `axorn`. npm is `@korakot/axorn`, because npm rejected plain `axorn` on 14 Oct 2026 as too similar to the existing `acorn` package; a scope keeps the name, and scoped packages are free when published public.

**Stands at:** `package.json` and `pyproject.toml` are ready at version 0.1.0, and `.github/workflows/publish.yml` is in place: on a `v*` tag it runs the tests, checks the tag matches both versions, then publishes to both registries. The demo footer already shows `pip install axorn` / `npm install @korakot/axorn`, so publishing is what makes those lines true.

**Released 14 Oct 2026:** 0.1.0 on npm (published by hand, since trusted publishing needs the package to exist) and on PyPI (first run of the workflow; npm skipped the existing version). Setup on the registries: PyPI trusted publisher for `korakot/axorn` + `publish.yml` + environment `pypi`; npm trusted publisher for `korakot/axorn` + `publish.yml`, allowed action `npm publish` only (not `dist-tag`), so tags publish directly rather than through npm's staged publishing; npm publishing access set to require 2FA with no bypass tokens.

**To release a new version:** bump the version in both `pyproject.toml` and `package.json`, commit to `main`, then on Kora's Mac `git tag vX.Y.Z && git push origin vX.Y.Z`. Claude Code sessions can push branches but not tags (the session's git proxy returns 403), so the tag push is Kora's.

**Decision:** publish with the current names (`roman_to_thai`, `thai_to_roman`, `romanToThai`, `thaiToRoman`). When another script arrives, add a general `convert(text, from_, to)` beside them and keep the old names as thin aliases, so nothing published breaks.

**How:** GitHub Actions with trusted publishing on both registries, so no tokens need handling. Kora has to register the trusted publisher once on each registry's website (npmjs.com and pypi.org); the workflow does the rest.

## 3. More scripts: Sinhala, then Myanmar — parked

**Stands at:** not needed for about a year (Kora, 14 Oct 2026).[^s2] The design notes stay here so the work can resume without rediscovery.

**Why:** Pāli texts circulate in these scripts too, and VRI publishes every book in each, so the same test method works.

**Design:** roman stays the hub. Add one table per script (`sinhala.json`, `myanmar.json`) next to `thai.json`, and any script → any script goes through roman. See [design](design.md).

**What's different from Thai:**
- Both scripts store vowels in spoken order, while Thai writes เ/โ before the consonant.
- Both have their own independent vowel letters instead of Thai's อ carrier.
- Myanmar also stacks consonants (U+1039) and writes y/r/v/h clusters as medials (ျ ြ ွ ှ), so it needs rule flags beyond a plain table.

**API questions it will raise:** how scripts are named in `convert` (plain names like `"sinhala"` or ISO 15924 codes like `Sinh`), and how the Thai-only options (`ue`, and `punct`'s ฯ rule) become per-script options.

**First step when resumed:** fetch one VRI book in `romn/` and `sinh/`, look at how clusters are written, then draft the table and generalise `tests/vri_check.py` to any script pair. Sinhala goes first because it is closer to Thai (plain virama, no medials), so it tests the generic design before Myanmar's harder rules.

## 4. Orthography layer — next (issue #1)

An `axorn.ortho` module (Python and JS), roman → roman, run before the converter, which stays one-to-one. It has two directions: "edition" (PTS → Thai-script Pāli: join elisions and sandhi, final m → ṃ) and "lookup" (split and restore words for dpd). A working verse/edition version is in anag's `scripts/thai_style.py`; move it here with the expert's examples as tests. Design in [orthography](orthography.md).

## Out of scope: Chinese

Chinese does not spell Pāli sound by sound. It uses conventional transcriptions chosen term by term, often from Sanskrit (涅槃 for *nibbāna*), or translates by meaning. Mapping Pāli to Chinese is a dictionary task, not a script conversion, so it does not belong in axorn. If it's needed, it fits the pali wiki's Chinese Tipiṭaka work instead.

## Smaller items

- **Option to keep roman capitals** when going Thai → roman, e.g. by copying case from a reference text. Only if a real use appears.
- **More VRI books in the test.** Six books pass (see [vri-conventions](vri-conventions.md)). Running the whole canon once would confirm the dot rule at scale.

[^s1]: Claude Code session that built axorn 0.1.0 (14 Oct 2026) — https://claude.ai/code/session_01PvCxrqAVyYE7nvuAULgx7A
[^s2]: Claude Code session that reordered the plan and built the web demo (14 Oct 2026) — https://claude.ai/code/session_017UQaAboga3Y59zY8wvPTVA
