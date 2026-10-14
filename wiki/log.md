# log

## 2026-10-14
- axorn 0.1.0: Python + JS from one table (`axorn/thai.json`), tested against 6 VRI books (~370k words; letters exact, 23 punctuation mismatches, Python = JS).
- Wiki started: plan (web demo, npm/PyPI, Sinhala then Myanmar, Chinese out of scope), history (Kora's notebooks, converters compared, the name), design, vri-conventions.
- Kora's two notebooks kept in `history/` (the tipitaka.app one with outputs stripped). Dates from Google Drive: pali_script_converter created 10 Feb 2018 (last edit 7 Mar 2018); tipi_b2t_pali_convert created 24 Oct 2022.
- Web demo live at https://korakot.github.io/axorn/ (`index.html` at repo root, imports `axorn/axorn.js` directly; palm-leaf design, converts either way as you type). Linked from both READMEs and the repo's About box.
- Plan reordered: demo → npm/PyPI (publish with current names; `convert()` + aliases later) → other scripts, parked ~1 year since Kora doesn't expect to need them sooner.
