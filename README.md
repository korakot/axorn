# axorn

**English** | [ไทย](https://github.com/korakot/axorn/blob/main/README.th.md)

Pāli script converter, roman ↔ Thai (อักษร), for Python and JS from one shared table.

Pāli has no script of its own, so the same text is written in roman (*evaṃ me sutaṃ*) and in Thai script (เอวํ เม สุตํ). axorn converts between the two, both ways, and gives exactly the same output in Python (for backends) and JS (for web pages). It follows the conventions of the VRI Tipiṭaka (tipitaka.org), and is tested against VRI's own files.

## Use

**Try it in the browser:** <https://korakot.github.io/axorn/> — paste roman or Thai and the other follows as you type. It runs the same `axorn.js`, entirely in your browser.

Install:

```
pip install axorn
npm install @korakot/axorn
```

On npm the package is scoped (`@korakot/axorn`) because npm refuses plain `axorn` as too close to `acorn`; the code is the same.

Python:

```python
from axorn import roman_to_thai, thai_to_roman

roman_to_thai("Evaṃ me sutaṃ.")   # 'เอวํ เม สุตํฯ'
thai_to_roman("เอวํ เม สุตํฯ")     # 'evaṃ me sutaṃ.'
```

JavaScript (ES module, Node 22+ or a recent browser):

```js
import { romanToThai, thaiToRoman } from "@korakot/axorn";

romanToThai("Evaṃ me sutaṃ.");  // "เอวํ เม สุตํฯ"
thaiToRoman("เอวํ เม สุตํฯ");    // "evaṃ me sutaṃ."
```

In a web page with no build step, including a Claude artifact, import it from jsDelivr:

```js
import { romanToThai, thaiToRoman } from "https://cdn.jsdelivr.net/npm/@korakot/axorn/axorn/axorn.js";
```

Command line: `python3 -m axorn thai < roman.txt > thai.txt` (or `roman` for the other way).

Options:

- `ue` (roman → Thai): write -iṃ as ึ, as many Thai prints do (กึ), instead of VRI's ิํ (กิํ).
- `punct` (both ways, on by default): convert digits (12 ↔ ๑๒) and full stops (. ↔ ฯ). Turn it off to convert letters only.

## Conventions

Thai-script Pāli is written in more than one way. axorn writes the VRI way and reads all the common ones:

| | axorn writes (VRI) | axorn also reads |
|---|---|---|
| -iṃ, e.g. *kiṃ* | กิํ | กึ |
| e/o before a consonant cluster, e.g. *tumhe* | ตุมฺเห (before the last consonant) | ตุเมฺห (before the whole cluster) |
| *ṭ* | ฏ | ฎ |
| virama (the dot under a consonant) | ฺ (phinthu) | ๎ (yamakkan) |
| niggahita | ṃ | ṁ, ŋ in roman input |

Two Pāli facts the converter relies on:

- **a + i and a + u are two vowels.** Pāli has no *ai* or *au* diphthong, so *sauddesaṃ* (sa-uddesaṃ) is สอุทฺเทสํ, not เสาทฺเทสํ.
- **A vowel that starts a syllable takes อ**, e.g. *okkāka* → โอกฺกาก.

**Full stops.** VRI's master text is in Devanagari, which has two marks where roman has one dot. The full stop (।) is ฯ in Thai, while the abbreviation sign (॰) stays "." in Thai, as in *dī. ni.* (ที. นิ.). Going roman → Thai, axorn treats a dot as an abbreviation when it:

- touches a digit ("12.", "1.7");
- sits inside parentheses;
- comes before ")" or ",";
- is followed by a number or another short abbreviation;
- or ends a chain of them ("sī. pī. potthakesu").

Every other dot is a full stop. The elision mark *…pe…* is written …เป.… in Thai.

Thai has no capital letters, so Thai → roman returns lower case.

## Tested on

`tests/vri_check.py` converts every paragraph of a VRI book roman → Thai and Thai → roman, compares each with VRI's file in the other script, and checks that Python and JS agree. On 14 Oct 2026:

| Book | Paragraphs | Words | Mismatches (of 2 × paragraphs) |
|---|---:|---:|---:|
| Dīgha Nikāya 1 (s0101m) | 1,046 | 45,891 | 2 |
| DN 1 commentary (s0101a) | 1,477 | 61,232 | 4 |
| Jātaka verses 1 (s0513m) | 10,473 | 53,074 | 6 |
| Majjhima Nikāya 1 (s0201m) | 1,785 | 85,305 | 5 |
| Dhammasaṅgaṇī (abh01m) | 2,436 | 53,189 | 2 |
| Vinaya, Pārājika (vin01m) | 2,465 | 72,253 | 4 |

Python and JS gave identical output on all of them, and every letter matched. The 23 mismatches are all punctuation and spacing, most of them inconsistencies inside VRI's own files. For example, the Thai file has a ฯ before the *Namo tassa* title that the roman file lacks, and *…pe…* is sometimes written …เป… without the dot.

Running the tests:

```
python3 tests/test_cases.py            # 18 fixed cases, Python and JS
git clone --depth 1 --filter=blob:none --sparse https://github.com/VipassanaTech/tipitaka-xml vri
git -C vri sparse-checkout set --no-cone /romn/s0101m.mul.xml /thai/s0101m.mul.xml
python3 tests/vri_check.py vri s0101m.mul
```

## Design

`axorn/thai.json` holds the letters: consonants, vowels (with their position before or after the consonant), virama, niggahita, digits and punctuation. `__init__.py` and `axorn.js` both read it and mirror each other line for line, so a fix to the table reaches both languages at once.

Roman is the hub. Other scripts (Myanmar, Sinhala, …) can be added later as one table each, and any script → any script goes through roman. The reasoning, history and plan are in [wiki/](https://github.com/korakot/axorn/blob/main/wiki/index.md).

## Credits

axorn was written by Claude (Anthropic) for Korakot Chaovavanich in 2026. Its design builds on Korakot's 2018 notebook, a Python port of the [pitaka.lk](https://pitaka.lk/converter.html) JavaScript converter. Two ideas carry over from it: spelling each Thai syllable from a consonant + vowel pair, with เ/โ placed before the consonant, and the consonant table itself. Korakot's notebook already matched VRI exactly on DN 1, letter for letter.

[Aksharamukha](https://github.com/virtualvinodh/aksharamukha-python) served as a cross-check during development.

## License

MIT
