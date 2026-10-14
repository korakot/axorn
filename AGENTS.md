# axorn

Pāli script converter (roman ↔ Thai), one shared table for Python and JS. README.md (Thai, the default on GitHub and npm) and README.en.md (English, also the PyPI page) explain the conventions and the test results.

Conventions (with why):
- `axorn/__init__.py` and `axorn/axorn.js` mirror each other line for line, and both read `axorn/thai.json`. Change them together. Users pick the language by where they run (backend vs browser) and must get identical output.
- Put letters and marks in the table, not in code, so they reach both languages and future script tables (roman is the hub; one JSON per script).
- Before committing, run `python3 tests/test_cases.py` (fixed cases, both languages), and `tests/vri_check.py` on a few VRI books when changing rules. Update the "Tested on" table if the numbers move, in both README.md (Thai) and README.en.md (English); Thai readers are the main audience, so README.md is Thai, and the two stay in step. Add a case to `tests/cases.json` for every bug fixed.
- Commit straight to `main`; Kora is the only reviewer.
- `wiki/` keeps the reasoning (plan, history, design, VRI conventions); start at `wiki/index.md`. Pages use OKF 0.2 frontmatter and footnote sources, like korakot/pali. List new pages in `wiki/index.md` and add a dated line to `wiki/log.md`.
