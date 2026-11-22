import { encodeRules, decodeBleText } from "../src/ble/protocol";
import type { Rule } from "../src/types/rule";

test("encodeRules produces Uint8Array", () => {
  const rules: Rule[] = [];
  const result = encodeRules(rules);
  expect(result).toBeInstanceOf(Uint8Array);
});

// Simple round‑trip test
test("decodeBleText returns original string", () => {
  const txt = "hello";
  const encoder = new TextEncoder();
  const buf = encoder.encode(txt);
  const decoded = decodeBleText(buf);
  expect(decoded).toBe(txt);
});

