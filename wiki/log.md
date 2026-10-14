# log

## 2026-10-14
- axorn 0.1.0: Python + JS from one table (`axorn/thai.json`), tested against 6 VRI books (~370k words; letters exact, 23 punctuation mismatches, Python = JS).
- Wiki started: plan (web demo, npm/PyPI, Sinhala then Myanmar, Chinese out of scope), history (Kora's notebooks, converters compared, the name), design, vri-conventions.
- Kora's two notebooks kept in `history/` (the tipitaka.app one with outputs stripped). Dates from Google Drive: pali_script_converter created 10 Feb 2018 (last edit 7 Mar 2018); tipi_b2t_pali_convert created 24 Oct 2022.
- Web demo live at https://korakot.github.io/axorn/ (`index.html` at repo root, imports `axorn/axorn.js` directly; palm-leaf design, converts either way as you type). Linked from both READMEs and the repo's About box.
- Plan reordered: demo → npm/PyPI (publish with current names; `convert()` + aliases later) → other scripts, parked ~1 year since Kora doesn't expect to need them sooner.
- Demo review: Thai first with a ไทย | English switch (remembered per browser, `?lang=en` overrides); footer assumes axorn is on PyPI and npm (`pip install axorn`, `npm install axorn`, jsDelivr import line), so those lines only work once published.
- Publish workflow added (`.github/workflows/publish.yml`, trusted publishing to PyPI and npm on `v*` tags); Kora's one-time registry steps listed in [plan](plan.md).
- npm rejected `axorn` as too similar to `acorn`; npm name is now `@korakot/axorn` (package.json, workflow skip check, demo footer, jsDelivr line). PyPI stays `axorn`. Workflow now skips versions already on either registry.
- Released 0.1.0: npm `@korakot/axorn` (by hand), PyPI `axorn` (workflow, all green). Release recipe and registry settings in [plan](plan.md).
