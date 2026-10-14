// axorn — Pāli script converter, roman ↔ Thai. Mirrors __init__.py line for
// line and reads the same thai.json, so both give the same output.
//   import { romanToThai, thaiToRoman } from "axorn";
//   romanToThai("Evaṃ me sutaṃ.")  // "เอวํ เม สุตํฯ"
import T from "./thai.json" with { type: "json" };

const R2T_CONS = new Map(T.consonants);
const T2R_CONS = new Map([...T.consonants.map(([r, t]) => [t, r]), ...Object.entries(T.consonants_thai_alt)]);
const R2T_VOW = new Map(T.vowels.map(([r, pre, post]) => [r, [pre, post]]));
const PRE = new Map(T.vowels.filter(([, pre]) => pre).map(([r, pre]) => [pre, r]));
const POST = new Map(T.vowels.filter(([, , post]) => post).map(([r, , post]) => [post, r]));
const CARRIER = T.vowel_carrier;
const VIRAMA = T.virama;
const VIRAMAS = new Set([VIRAMA, ...T.virama_thai_alt]);
const [NIG_R, NIG_T] = T.niggahita;
const NIG_R_ALL = [NIG_R, ...T.niggahita_roman_alt];
const UE = T.i_niggahita_ligature;
const [DIG_R, DIG_T] = T.digits;
const [STOP_R, STOP_T] = T.full_stop;
const [PE_R, PE_T] = T.peyyala; // the elision mark "…pe…", also "… pe…"
// Escape a literal for use in a RegExp.
const esc = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const PE_RE_R = new RegExp("(…\\s?)" + esc(PE_R), "gu");
const PE_RE_T = new RegExp("(…\\s?)" + esc(PE_T), "gu");

// Longest letters first, so "kh" wins over "k".
const letters = [...R2T_CONS.keys(), ...R2T_VOW.keys(), ...NIG_R_ALL].sort((a, b) => b.length - a.length);
const R_TOKEN = new RegExp(letters.map(esc).join("|") + "|[\\s\\S]", "gu");

const isDigitR = (t) => t.length === 1 && DIG_R.includes(t);
const NEXT_IS_ABBREV = /\s*\d|\s+\p{L}{1,4}\./uy;
const PREV_IS_ABBREV = /[\s(]\p{L}{1,4}\.\s+\p{L}{1,4}$/u;

// Roman "." is two marks in VRI's Devanagari master: a full stop (।), written ฯ
// in Thai, and an abbreviation sign (॰), kept as "." in Thai. Same rule as
// _thai_punct in __init__.py.
function thaiPunct(s) {
  const out = [];
  let depth = 0;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if (c === "(") depth++;
    else if (c === ")") depth = Math.max(depth - 1, 0);
    if (isDigitR(c)) {
      out.push(DIG_T[DIG_R.indexOf(c)]);
    } else if (c === STOP_R) {
      const prev = s[i - 1] ?? "", nxt = s[i + 1] ?? "";
      NEXT_IS_ABBREV.lastIndex = i + 1;
      const abbrev = /\d/.test(prev) || /\d/.test(nxt) || (nxt !== "" && "),".includes(nxt))
        || depth > 0 || NEXT_IS_ABBREV.test(s)
        || PREV_IS_ABBREV.test((i < 30 ? " " : "") + s.slice(Math.max(0, i - 30), i));
      out.push(abbrev ? STOP_R : STOP_T);
    } else {
      out.push(c);
    }
  }
  return out.join("").replace(PE_RE_R, (_, a) => a + PE_T);
}

export function romanToThai(text, { ue = false, punct = true } = {}) {
  text = text.normalize("NFC").toLowerCase();
  if (punct) text = thaiPunct(text);
  const toks = text.match(R_TOKEN) || [];
  const out = [];
  for (let i = 0; i < toks.length; i++) {
    const tok = toks[i];
    if (R2T_CONS.has(tok)) {
      const nxt = toks[i + 1];
      if (R2T_VOW.has(nxt)) {
        const [pre, post] = R2T_VOW.get(nxt);
        out.push(pre + R2T_CONS.get(tok) + post);
        i++;
      } else {
        out.push(R2T_CONS.get(tok) + VIRAMA);
      }
    } else if (R2T_VOW.has(tok)) {
      const [pre, post] = R2T_VOW.get(tok);
      out.push(pre + CARRIER + post);
    } else if (NIG_R_ALL.includes(tok)) {
      const last = out.length ? out[out.length - 1] : "";
      if (ue && last.endsWith("ิ")) out[out.length - 1] = last.slice(0, -1) + UE;
      else out.push(NIG_T);
    } else {
      out.push(tok);
    }
  }
  return out.join("");
}

export function thaiToRoman(text, { punct = true } = {}) {
  if (punct) text = text.replace(PE_RE_T, (_, a) => a + PE_R);
  const out = [];
  let pending = ""; // a prefix vowel (เ/โ) waiting for its consonant
  const n = text.length;
  for (let i = 0; i < n; i++) {
    const c = text[i];
    if (PRE.has(c)) {
      pending = PRE.get(c);
    } else if (T2R_CONS.has(c) || c === CARRIER) {
      const base = T2R_CONS.get(c) ?? "";
      const nxt = i + 1 < n ? text[i + 1] : "";
      if (VIRAMAS.has(nxt)) {
        out.push(base); // pending vowel belongs to a later consonant
        i++;
      } else if (POST.has(nxt)) {
        out.push(base + POST.get(nxt));
        pending = "";
        i++;
      } else if (nxt === UE) {
        out.push(base + "i" + NIG_R);
        pending = "";
        i++;
      } else {
        out.push(base + (pending || "a"));
        pending = "";
      }
    } else {
      if (pending) { out.push(pending); pending = ""; } // a stray เ/โ
      if (c === NIG_T) out.push(NIG_R);
      else if (punct && DIG_T.includes(c)) out.push(DIG_R[DIG_T.indexOf(c)]);
      else if (punct && c === STOP_T) out.push(STOP_R);
      else out.push(c);
    }
  }
  if (pending) out.push(pending);
  return out.join("");
}
