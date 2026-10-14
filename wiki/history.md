---
type: history
title: "History"
description: "From Kora's notebooks (pitaka.lk port, tipitaka.app) to axorn: the converters compared and why the name"
tags: [history]
status: draft
generated: {by: claude-opus-5-5, at: 2026-10-14}
sources:
  - {id: s1, resource: "https://claude.ai/code/session_01PvCxrqAVyYE7nvuAULgx7A", title: "Claude Code session that built axorn 0.1.0 (14 Oct 2026)", last_modified: 2026-10-14}
  - {id: nb1, resource: "../history/pali_script_converter.ipynb", title: "Kora's notebook: Python port of the pitaka.lk converter (Feb–Mar 2018)", last_modified: 2026-10-14}
  - {id: nb2, resource: "../history/tipi_b2t_pali_convert.ipynb", title: "Kora's notebook: Sinhala → Thai for tipitaka.app text (Oct 2022)", last_modified: 2026-10-14}
  - {id: pitakalk, resource: "https://pitaka.lk/converter.html", title: "pitaka.lk Pāli script converter (JavaScript)", last_modified: 2026-10-14}
---

# History

## Kora's notebooks

Kora wrote two converters before axorn. Both are kept in `history/`.

**pali_script_converter.ipynb** (Feb–Mar 2018, by its Google Drive dates)[^nb1] studies the JavaScript converter on pitaka.lk.[^pitakalk] That site converts through Sinhala as a middle script: roman or Thai goes to Sinhala first, then out to the target script. Its trick is a list of every consonant + vowel pair (for example *khe* ↔ เข), which handles Thai's vowels written before the consonant without any special rule. The converter replaces the longest pairs first, then mops up independent vowels and niggahita.

Kora ported the idea to Python with roman ↔ Thai directly, keeping only Pāli letters (279 pairs). His notes say he was impressed by how well the original was written. The notebook also has a shorter rule-based version (`rom2th`) written for DPPN headwords.

When tested on 14 Oct 2026 against the VRI Tipiṭaka (DN 1, 45,105 words), the ported converter matched VRI letter for letter in both directions. It had only small gaps: it knew the niggahita only as ṁ (VRI uses ṃ), and it didn't handle capitals.

**tipi_b2t_pali_convert.ipynb** (24 Oct 2022)[^nb2] converts the Sinhala-script text of the tipitaka.app Android app to Thai, character by character. Its own output shows several letters left unmapped or mapped wrongly (ණ came out as ฆ; ඩ ඣ ඵ ූ stayed in Sinhala), so it was a start rather than a working converter.

## Looking for a converter (14 Oct 2026)

The MBU translation work needed one converter usable from both a Python backend and a JS front end.[^s1] Three were tested against VRI's Thai text:

- **Aksharamukha** (Python; AGPL-3.0). Its letters were correct once three fixes were added: split a·u, write -iṃ as ิํ, and place เ/โ before the last consonant of a cluster. But AGPL can oblige a networked service built on it to publish its source, which is awkward for a vendor-built MBU system. Its only JS form is a third-party GPL port that runs Python in the browser (17 MB).
- **Sanscript** (indic-transliteration; MIT; Python + JS). Its Thai scheme writes เ/โ after the consonant (มเ instead of เม), and on DN 1, 43% of words differed from VRI. It was built for Sanskrit, and Thai's visual vowel order was never handled.
- **Kora's pitaka.lk port**, described above: exact on DN 1, tiny, and no license problem.

The decision was to write a fresh converter, learning from Kora's notebook (consonant + vowel pairs, the consonant table) and using Aksharamukha as a cross-check. Python and JS read one shared table so they cannot drift apart. See [design](design.md).

## The name

Kora wanted a Thai-flavoured name that is easy to type and spell. Candidates, in order:

- *akkhara* (Pāli for letter): rejected as hard to spell.
- *pinthu* (พินทุ, the dot under a consonant): a close second.
- *aksorn* (อักษร): ambiguous between *aksorn* and *akson*.
- *axon*: taken on npm and PyPI, and crowded (neuron, Axon framework).

Kora proposed **axorn**: อักษร with *x* for "ks", and *-orn* as Thais usually write it. It was free on npm and PyPI and is unique in searches.

## 0.1.0 (14 Oct 2026)

Built in one session.[^s1] It was tested against six VRI books (about 370,000 words): every letter matched, Python and JS agreed everywhere, and 23 punctuation mismatches remained, mostly VRI's own inconsistencies. Getting there surfaced the [VRI conventions](vri-conventions.md), especially that roman "." is two different marks in VRI's Devanagari master.

[^s1]: Claude Code session that built axorn 0.1.0 (14 Oct 2026) — https://claude.ai/code/session_01PvCxrqAVyYE7nvuAULgx7A
[^nb1]: Kora's notebook: Python port of the pitaka.lk converter (Feb–Mar 2018) — ../history/pali_script_converter.ipynb
[^nb2]: Kora's notebook: Sinhala → Thai for tipitaka.app text (Oct 2022) — ../history/tipi_b2t_pali_convert.ipynb
[^pitakalk]: pitaka.lk Pāli script converter (JavaScript) — https://pitaka.lk/converter.html
