---
type: concept
title: "Design"
description: "Roman as the hub, one JSON table per script, Python and JS mirrored line for line, how each direction works"
tags: [design]
status: draft
generated: {by: claude-opus-5-5, at: 2026-10-14}
sources:
  - {id: s1, resource: "https://claude.ai/code/session_01PvCxrqAVyYE7nvuAULgx7A", title: "Claude Code session that built axorn 0.1.0 (14 Oct 2026)", last_modified: 2026-10-14}
  - {id: vricode, resource: "https://github.com/VipassanaTech/tipitaka-xml/tree/main/code/converters/CstConversion", title: "VRI's own C# converters (Deva2Thai.cs, Deva2Mymr.cs, Deva2Sinh.cs, …)", last_modified: 2026-10-14}
---

# Design

## One table, two languages

The letters live in `axorn/thai.json`: consonants, vowels (each with its position before or after the consonant), the vowel carrier อ, virama, niggahita, digits, the full stop and the elision mark. `__init__.py` and `axorn.js` both read that file and mirror each other line for line.

The reason is that people pick the language by where they run, Python on a server and JS in a browser, and they must get the same answer. With one table and mirrored code, a fix to a letter reaches both at once. `tests/test_cases.py` and `tests/vri_check.py` run both languages on the same input and fail if they differ.[^s1]

## Roman → Thai

The roman text is normalised (Unicode NFC) and lower-cased. A punctuation pass then turns digits into Thai digits, decides for each "." whether it is a full stop (ฯ) or an abbreviation (".") (see [vri-conventions](vri-conventions.md)), and turns *…pe…* into …เป.….

The letter pass splits the text into letters, longest first so *kh* wins over *k*, and walks them:

- A **consonant followed by a vowel** becomes one Thai syllable with the vowel in its place: *khe* → เข, *khā* → ขา, *kha* → ข (the inherent *a* is not written).
- A **consonant with no vowel** gets the virama: *k* → กฺ. So *sacca* → สจฺจ.
- A **vowel with no consonant** gets the carrier อ: *e* → เอ, *o* → โอ.
- **ṃ** becomes ํ. With the `ue` option, *-iṃ* becomes ึ instead of ิํ.

This is Kora's consonant + vowel pair idea from his pitaka.lk port (see [history](history.md)), done as a walk over tokens instead of a list of 279 replacements.

## Thai → roman

The Thai text is read one character at a time:

- เ/โ are remembered as a waiting vowel.
- A consonant (or อ) looks at the next character:
  - a virama means no vowel; the waiting vowel stays for a later consonant, which is how ตุเมฺห (vowel before the whole cluster) still reads as *tumhe*;
  - a vowel sign gives that vowel; ึ gives *iṃ*;
  - otherwise the consonant takes the waiting vowel, or the inherent *a*.

This direction needs no guessing. It reads every Thai convention listed in the README, which is why comparing two Thai sources is best done in roman.

## Roman as the hub, one table per script

Other scripts will be added as one table each (`sinhala.json`, `myanmar.json`), and any script → any script goes through roman. That way N scripts need N tables, not N² converters.

The Thai code has two Thai-specific features: vowels written before the consonant, and อ as the carrier for vowels that start a syllable. Sinhala and Myanmar store vowels in spoken order and have their own independent vowel letters. Myanmar adds stacked consonants and medials. So adding a script means a table plus a few rule flags, and the code gains a generic path next to the Thai one. See [plan](plan.md).

VRI's own converters are a useful reference for those tables. They are C# programs that turn the Devanagari master into each script (`Deva2Thai.cs`, `Deva2Mymr.cs`, `Deva2Sinh.cs`, …), and VRI's Thai and roman text are their output.[^vricode] Check their license before borrowing code; reading them for the mappings is fine either way.

[^s1]: Claude Code session that built axorn 0.1.0 (14 Oct 2026) — https://claude.ai/code/session_01PvCxrqAVyYE7nvuAULgx7A
[^vricode]: VRI's own C# converters (Deva2Thai.cs, Deva2Mymr.cs, Deva2Sinh.cs, …) — https://github.com/VipassanaTech/tipitaka-xml/tree/main/code/converters/CstConversion
