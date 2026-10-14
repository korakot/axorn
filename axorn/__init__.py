"""axorn — Pāli script converter, roman ↔ Thai.

    >>> from axorn import roman_to_thai, thai_to_roman
    >>> roman_to_thai("Evaṃ me sutaṃ.")
    'เอวํ เม สุตํฯ'
    >>> thai_to_roman("เอวํ เม สุตํฯ")
    'evaṃ me sutaṃ.'

Both directions read the same table (thai.json), which axorn.js also
reads, so the Python and JS versions give the same output.
The defaults follow the VRI (tipitaka.org) Thai edition; see README.md.
"""
import json
import re
import unicodedata
from pathlib import Path

__all__ = ["roman_to_thai", "thai_to_roman"]

_T = json.loads((Path(__file__).with_name("thai.json")).read_text(encoding="utf-8"))

_R2T_CONS = {r: t for r, t in _T["consonants"]}
_T2R_CONS = {t: r for r, t in _T["consonants"]} | _T["consonants_thai_alt"]
_R2T_VOW = {r: (pre, post) for r, pre, post in _T["vowels"]}
_PRE = {pre: r for r, pre, post in _T["vowels"] if pre}      # เ -> e
_POST = {post: r for r, pre, post in _T["vowels"] if post}   # า -> ā
_CARRIER = _T["vowel_carrier"]
_VIRAMA = _T["virama"]
_VIRAMAS = {_VIRAMA, *_T["virama_thai_alt"]}
_NIG_R, _NIG_T = _T["niggahita"]
_NIG_R_ALL = [_NIG_R, *_T["niggahita_roman_alt"]]
_UE = _T["i_niggahita_ligature"]
_DIG_R, _DIG_T = _T["digits"]
_STOP_R, _STOP_T = _T["full_stop"]
_PE_R, _PE_T = _T["peyyala"]  # the elision mark "…pe…", also "… pe…"
_PE_RE_R = re.compile(r"(…\s?)" + re.escape(_PE_R))
_PE_RE_T = re.compile(r"(…\s?)" + re.escape(_PE_T))

# Longest letters first, so "kh" wins over "k".
_letters = sorted([*_R2T_CONS, *_R2T_VOW, *_NIG_R_ALL], key=len, reverse=True)
_R_TOKEN = re.compile("|".join(map(re.escape, _letters)) + "|.", re.S)


def roman_to_thai(text: str, *, ue: bool = False, punct: bool = True) -> str:
    """Roman Pāli -> Thai script.

    ue    -- write -iṃ as ึ (common in Thai prints) instead of ิํ (VRI).
    punct -- digits -> Thai digits, and a sentence-ending full stop -> ฯ
             (abbreviation dots stay "."; see _thai_punct).
    """
    text = unicodedata.normalize("NFC", text).lower()
    if punct:
        text = _thai_punct(text)
    toks = _R_TOKEN.findall(text)
    out = []
    i = 0
    while i < len(toks):
        tok = toks[i]
        if tok in _R2T_CONS:
            nxt = toks[i + 1] if i + 1 < len(toks) else ""
            if nxt in _R2T_VOW:
                pre, post = _R2T_VOW[nxt]
                out.append(pre + _R2T_CONS[tok] + post)
                i += 1
            else:
                out.append(_R2T_CONS[tok] + _VIRAMA)
        elif tok in _R2T_VOW:
            pre, post = _R2T_VOW[tok]
            out.append(pre + _CARRIER + post)
        elif tok in _NIG_R_ALL:
            if ue and out and out[-1].endswith("ิ"):
                out[-1] = out[-1][:-1] + _UE
            else:
                out.append(_NIG_T)
        else:
            out.append(tok)
        i += 1
    return "".join(out)


_NEXT_IS_ABBREV = re.compile(r"\s*\d|\s+[^\W\d_]{1,4}\.")
_PREV_IS_ABBREV = re.compile(r"[\s(][^\W\d_]{1,4}\.\s+[^\W\d_]{1,4}$")


def _thai_punct(s: str) -> str:
    """Roman "." is two marks in VRI's Devanagari master: a full stop (।),
    written ฯ in Thai, and an abbreviation sign (॰), kept as "." in Thai.
    A dot counts as an abbreviation when it touches a digit ("12.", "1.7"),
    sits inside parentheses ("(sī. syā.)"), comes before ")" or ",", or is
    followed by a number or another short abbreviation ("dī. ni. 1.1"),
    or ends a chain of them ("sī. pī. potthakesu").
    Every other dot is a full stop."""
    out = []
    depth = 0
    for i, c in enumerate(s):
        if c == "(":
            depth += 1
        elif c == ")":
            depth = max(depth - 1, 0)
        if c in _DIG_R:
            out.append(_DIG_T[_DIG_R.index(c)])
        elif c == _STOP_R:
            prev = s[i - 1] if i else ""
            nxt = s[i + 1] if i + 1 < len(s) else ""
            abbrev = (prev.isdigit() or nxt.isdigit() or (nxt != "" and nxt in "),")
                      or depth > 0 or _NEXT_IS_ABBREV.match(s, i + 1)
                      or _PREV_IS_ABBREV.search((" " if i < 30 else "") + s[max(0, i - 30):i]))
            out.append(_STOP_R if abbrev else _STOP_T)
        else:
            out.append(c)
    return _PE_RE_R.sub(lambda m: m.group(1) + _PE_T, "".join(out))


def thai_to_roman(text: str, *, punct: bool = True) -> str:
    """Thai-script Pāli -> roman (lower case; Thai has no capitals).

    Reads both conventions for -iṃ (ิํ and ึ) and both placements of
    เ/โ in a cluster (ตุมฺเห and ตุเมฺห).
    punct -- Thai digits -> 0-9, and ฯ -> full stop.
    """
    if punct:
        text = _PE_RE_T.sub(lambda m: m.group(1) + _PE_R, text)
    out = []
    pending = ""  # a prefix vowel (เ/โ) waiting for its consonant
    n = len(text)
    i = 0
    while i < n:
        c = text[i]
        if c in _PRE:
            pending = _PRE[c]
        elif c in _T2R_CONS or c == _CARRIER:
            base = _T2R_CONS.get(c, "")
            nxt = text[i + 1] if i + 1 < n else ""
            if nxt in _VIRAMAS:
                out.append(base)       # pending vowel belongs to a later consonant
                i += 1
            elif nxt in _POST:
                out.append(base + _POST[nxt])
                pending = ""
                i += 1
            elif nxt == _UE:
                out.append(base + "i" + _NIG_R)
                pending = ""
                i += 1
            else:
                out.append(base + (pending or "a"))
                pending = ""
        else:
            if pending:                # a stray เ/โ with no consonant after it
                out.append(pending)
                pending = ""
            if c == _NIG_T:
                out.append(_NIG_R)
            elif punct and c in _DIG_T:
                out.append(_DIG_R[_DIG_T.index(c)])
            elif punct and c == _STOP_T:
                out.append(_STOP_R)
            else:
                out.append(c)
        i += 1
    if pending:
        out.append(pending)
    return "".join(out)

