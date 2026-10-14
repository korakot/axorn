---
type: concept
title: "VRI conventions"
description: "What VRI's Thai text does and the evidence: -iṃ as ิํ, vowel placement, a·u, the two kinds of dot, …pe…"
tags: [conventions, evidence]
status: draft
generated: {by: claude-opus-5-5, at: 2026-10-14}
sources:
  - {id: s1, resource: "https://claude.ai/code/session_01PvCxrqAVyYE7nvuAULgx7A", title: "Claude Code session that built axorn 0.1.0 (14 Oct 2026)", last_modified: 2026-10-14}
  - {id: vri, resource: "https://github.com/VipassanaTech/tipitaka-xml", title: "VRI Tipiṭaka XML — the same books in romn/, thai/, mymr/, sinh/ and more", last_modified: 2026-10-14}
---

# VRI conventions

axorn writes the convention of the VRI Tipiṭaka (tipitaka.org), because VRI publishes every book in both roman and Thai script.[^vri] That makes it a test set: convert one file, compare with the other. All findings below come from comparing six books in both directions: DN 1, its commentary, Jātaka verses 1, MN 1, Dhammasaṅgaṇī and Vinaya Pārājika, about 370,000 words.[^s1]

VRI's master text is in Devanagari, and its roman and Thai files are generated from it by VRI's own converters. So the Thai file follows rules, not a printed edition, and its quirks come from Devanagari.

## Letters

**-iṃ is ิํ, not ึ.** For example *kiṃ* = กิํ and *saddhiṃ* = สทฺธิํ. Many Thai printed editions write ึ instead. This was the most common difference between Aksharamukha's default and VRI.

**เ/โ go before the last consonant of a cluster.** For example *tumhe* = ตุมฺเห, *tasseta* = ตสฺเสตํ, *pañho* = ปญฺโห. The other habit, putting the vowel before the whole cluster (ตุเมฺห), appears in some prints and in Aksharamukha.

**a + i and a + u are two vowels.** Pāli has no *ai* or *au* diphthong, so *sauddesaṃ* (*sa-uddesaṃ*) is สอุทฺเทสํ. A Sanskrit-minded converter writes เสาทฺเทสํ.

**ṭ is ฏ.** Some older Thai sources use ฎ, which axorn reads as ṭ.

With these, every letter of all six books matched in both directions.

## Punctuation: one roman dot, two Thai marks

Devanagari has a full stop (।) and an abbreviation sign (॰). VRI's roman text writes both as ".", while its Thai text writes the full stop as ฯ and keeps the abbreviation sign as ".". So going roman → Thai, a converter has to work out which dot is which.

Counting every dot in the six books by context showed clear cues:

| Context of the roman "." | VRI Thai has |
|---|---|
| right after a digit ("12.") | "." every time (about 6,600) |
| before ")" or "," | "." almost always (about 3,050 vs 1) |
| at the end of a paragraph | ฯ every time (about 9,550) |
| inside parentheses, before a space | "." every time (about 2,700) |
| before a number ("dī. ni. 1.1") | "." every time |
| outside parentheses, before a word | mostly ฯ; "." only for short words that are abbreviations |

axorn's rule follows from that table. A dot is an abbreviation when it:

- touches a digit;
- is inside parentheses;
- comes before ")" or ",";
- is followed by a number or another short abbreviation (up to 4 letters plus a dot);
- or ends a chain of them ("sī. pī. potthakesu").

Every other dot becomes ฯ.

Other punctuation:

- **The elision mark** *…pe…* is written …เป.… in Thai, keeping the abbreviation dot. Before this was handled, it was the largest single source of mismatches: fixing it removed about 1,500 in the Abhidhamma and Vinaya books alone.
- **Digits** become Thai digits; other punctuation (, ; ? ‘ ’ – …) is the same in both scripts.

## What's left

23 mismatches remained out of about 78,000 paragraph conversions (both directions), all punctuation or spacing:

- The *Namo tassa* title line has a ฯ in front in Thai but nothing in roman. This accounts for one or two per book.
- *…pe…* is occasionally written …เป… without the dot, or with a space before *pe*.
- A few dots that are genuinely ambiguous, such as a single abbreviation before a long word ("sī. potthake"), or a full stop inside parentheses.
- Double spaces present in one file but not the other.

Most are inconsistencies inside VRI's own files, so no rule could get them all.

[^s1]: Claude Code session that built axorn 0.1.0 (14 Oct 2026) — https://claude.ai/code/session_01PvCxrqAVyYE7nvuAULgx7A
[^vri]: VRI Tipiṭaka XML — the same books in romn/, thai/, mymr/, sinh/ and more — https://github.com/VipassanaTech/tipitaka-xml
