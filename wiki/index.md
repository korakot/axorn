---
okf_version: "0.2"
---
# axorn wiki

Why axorn is built the way it is, how it came about, and what comes next. The README covers how to use it; this wiki keeps the reasoning and the evidence.

* [Plan](plan.md) - What's next, with resume pointers: web demo live on GitHub Pages, npm/PyPI next with current names, other scripts parked ~1 year; Chinese out of scope
* [History](history.md) - From Kora's notebooks (pitaka.lk port, tipitaka.app) to axorn: the converters compared and why the name
* [Design](design.md) - Roman as the hub, one JSON table per script, Python and JS mirrored line for line, how each direction works
* [VRI conventions](vri-conventions.md) - What VRI's Thai text does and the evidence: -iṃ as ิํ, vowel placement, a·u, the two kinds of dot, …pe…
* [Orthography layer (planned)](orthography.md) - Script ≠ orthography: an `axorn.ortho` module (roman → roman) before the one-to-one converter; edition direction joins PTS sandhi into Thai-script Pāli (ชินารพฺภ, กงฺขํ, เอตทพฺรวิ), lookup direction restores words for dpd; from an expert review of anag (issue #1)
* [Log](log.md) - Dated changes
