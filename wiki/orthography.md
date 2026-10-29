---
type: design
title: "Orthography layer (planned)"
description: "Why script conversion isn't enough for PTS-style roman sources, and the planned axorn.ortho module: roman → roman, two directions (edition joins sandhi into Thai-script Pāli conventions; lookup splits and restores words), verse vs prose, the expert's examples as tests; the converter stays one-to-one"
tags: [design, orthography, planned]
status: draft
generated: {by: claude-code, at: 2026-10-29}
sources:
  - {id: i1, resource: "https://github.com/korakot/axorn/issues/1", title: "Orthography layer before script conversion", last_modified: 2026-10-29}
  - {id: pali, resource: "https://github.com/korakot/pali/blob/main/wiki/thai-script-orthography.md", title: "pali wiki: Thai-script Pāli orthography for roman sources", last_modified: 2026-10-29}
---

# Orthography layer (planned)

axorn converts **script**: one table, every letter mapped, exact round trips ([design](design.md)). That stays. A PTS-style roman edition also differs from Thai-script Pāli in **orthography**: how sandhi and elision are written. Converting it letter by letter gives Thai that Thai Pāli readers find foreign. An expert reader showed this on korakot/anag's first Thai-script edition (29 Oct 2026). The rules and their reasons are in pali `wiki/thai-script-orthography.md`.[^pali] This page is the plan for building them into axorn.[^i1]

## Shape

A separate module, e.g. `axorn.ortho` in Python and the same in JS, that works **roman → roman** and runs before `roman_to_thai`. The converter itself never changes.

**Direction "edition"** (PTS → Thai-script Pāli), each rule one function, verse mode first:

| PTS roman | after ortho | Thai |
|---|---|---|
| *jin' ārabbha* | *jinārabbha* | ชินารพฺภ |
| *vitthāren' eva 'haṃ* | *vitthārenevahaṃ* | วิตฺถาเรเนวหํ (verse; prose lengthens: …วาหํ) |
| *c'eva* | *ceva* | เจว |
| *kaṅkham attano* | *kaṅkhaṃ attano* | กงฺขํ อตฺตโน |
| *etad abravi* | *etadabravi* | เอตทพฺรวิ |
| *odātañ ca* | *odātañca* | โอทาตญฺจ |
| *kāmesv ādīnavaṃ* | *kāmesvādīnavaṃ* | กาเมสฺวาทีนวํ |

There is also a class-nasal rule for Thai learners: *saṃpannā* → *sampannā* (สมฺปนฺนา), *saṃgha* → *saṅgha* (สงฺฆ), only before a stop and only inside a printed word. It was adopted in anag with exceptions taken from evidence, not a blanket rule: anag's `data/nasal-evidence.tsv` counts both spellings in the VRI and Siam Tipiṭaka, the dictionaries and wbw. Only *sayaṃjāta* kept ṃ. The module should take its exceptions from the same kind of table.

**Direction "lookup"** (PTS → dictionary forms): split elisions and restore whole words: *jin'* → *jinaṃ*, *'haṃ* → *ahaṃ*, *'va* → *iva*, *'ti* → *iti*, *etad* → *etaṃ*, *odātañ* → *odātaṃ*, *kāmesv* → *kāmesu*, final *m* → *ṃ*. `korakot/dpd` needs this for PTS texts (dpd#1). Shown to readers, the split is written as whole words joined by a hyphen (อาคมาธิคเมน-เอว, the expert's notation). It is never written as the cut-off print form (…เมนฺ'), because a final consonant is ungrammatical in Pāli.

**Tests:** the expert's examples above, verbatim, plus anag's 38 elided tokens and 11 consonant-final forms. Each word's restored form is in anag's `data/words.tsv` (`restored` column).

## Status

- A working Python version, verse and edition direction only, lives in anag's `scripts/thai_style.py` (`groups`, `thai_word`, `roman_key`). It has a round-trip check against the normalised roman.
- Move it here, add the lookup direction and the JS mirror, release it, then switch anag and dpd to it.

[^i1]: Orthography layer before script conversion — https://github.com/korakot/axorn/issues/1
[^pali]: pali wiki: Thai-script Pāli orthography for roman sources — https://github.com/korakot/pali/blob/main/wiki/thai-script-orthography.md
