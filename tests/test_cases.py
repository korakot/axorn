"""Fixed cases from tests/cases.json, run on both Python and JS.  python3 tests/test_cases.py"""
import json, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from axorn import roman_to_thai, thai_to_roman

JS = """
import { romanToThai, thaiToRoman } from "../axorn/axorn.js";
import cases from "./cases.json" with { type: "json" };
console.log(JSON.stringify(cases.map(c => [
  romanToThai(c.roman, { ue: !!c.ue }), thaiToRoman(c.thai)])));
"""

def main():
    cases = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))
    tmp = HERE / "_cases_run.mjs"
    tmp.write_text(JS, encoding="utf-8")
    try:
        js = json.loads(subprocess.run(["node", str(tmp)], capture_output=True, text=True, check=True).stdout)
    finally:
        tmp.unlink()
    fails = 0
    for c, (js_t, js_r) in zip(cases, js):
        checks = []
        if not c.get("reverse_only"):
            checks += [("py r→t", roman_to_thai(c["roman"], ue=c.get("ue", False)), c["thai"]), ("js r→t", js_t, c["thai"])]
        if not c.get("oneway"):
            checks += [("py t→r", thai_to_roman(c["thai"]), c["roman"]), ("js t→r", js_r, c["roman"])]
        for name, got, want in checks:
            if got != want:
                fails += 1
                print(f"FAIL {name}: {got!r} != {want!r}  ({c.get('note', '')})")
    print(f"{len(cases)} cases, {fails} failures")
    sys.exit(1 if fails else 0)

main()
