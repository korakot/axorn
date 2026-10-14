// Reads JSON lines {"dir": "thai"|"roman", "text": ...} on stdin, writes converted text as JSON lines.
import { romanToThai, thaiToRoman } from "../axorn/axorn.js";
import { createInterface } from "node:readline";
for await (const line of createInterface({ input: process.stdin })) {
  const { dir, text } = JSON.parse(line);
  console.log(JSON.stringify(dir === "thai" ? romanToThai(text) : thaiToRoman(text)));
}
