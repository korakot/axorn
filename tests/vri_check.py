"""Check axorn (Python and JS) against the VRI Tipiṭaka, which has every book in both
roman (romn/) and Thai (thai/) script.

    git clone --depth 1 --filter=blob:none --sparse https://github.com/VipassanaTech/tipitaka-xml vri
    git -C vri sparse-checkout set --no-cone /romn/s0101m.mul.xml /thai/s0101m.mul.xml
    python3 tests/vri_check.py vri s0101m.mul

Each paragraph (markup removed) is converted roman -> Thai and Thai -> roman and must
match the other file exactly. Roman is compared in lower case, since Thai has no capitals.
Python and JS outputs must be identical; the script fails if they are not.
Mismatches against VRI are reported, not failed on: a few come from VRI's own
inconsistencies (see README, "Tested on").
"""
import json, re, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from axorn import roman_to_thai, thai_to_roman

def paras(path):
    x = path.read_bytes().decode("utf-16")
    ps = re.findall(r"<p [^>]*>(.*?)</p>", x, re.S)
    return [re.sub(r"<[^>]+>", "", p) for p in ps]

def run_js(jobs):
    inp = "".join(json.dumps({"dir": d, "text": t}, ensure_ascii=False) + "\n" for d, t in jobs)
    out = subprocess.run(["node", str(Path(__file__).with_name("convert.mjs"))], input=inp,
                         capture_output=True, text=True, check=True).stdout
    return [json.loads(l) for l in out.splitlines()]

def check(vri, book, show=5):
    R, T = paras(Path(vri, "romn", book + ".xml")), paras(Path(vri, "thai", book + ".xml"))
    assert len(R) == len(T), (len(R), len(T))
    py = [roman_to_thai(r) for r in R] + [thai_to_roman(t) for t in T]
    js = run_js([("thai", r) for r in R] + [("roman", t) for t in T])
    want = T + [r.lower() for r in R]
    bad = [(i, g, w) for i, (g, w) in enumerate(zip(py, want)) if g != w]
    drift = sum(a != b for a, b in zip(py, js))
    words = sum(len(r.split()) for r in R)
    print(f"{book}: {len(R)} paragraphs, {words} words; mismatches {len(bad)}/{2*len(R)}; python≠js {drift}")
    for i, g, w in bad[:show]:
        d = "r→t" if i < len(R) else "t→r"
        k = next((j for j, (a, b) in enumerate(zip(g, w)) if a != b), min(len(g), len(w)))
        print(f"  {d} got  …{g[max(0,k-25):k+25]}…\n      want …{w[max(0,k-25):k+25]}…")
    return drift

if __name__ == "__main__":
    sys.exit(1 if sum(check(sys.argv[1], b) for b in sys.argv[2:]) else 0)
