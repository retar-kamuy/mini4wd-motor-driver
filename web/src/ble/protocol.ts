// BLE protocol utilities for Mini4WD web console
// NOTE: This is a minimal placeholder implementation sufficient for compilation.
// Real encoding/decoding should follow the device specification.

import type { Rule } from "../types/rule";
import type { AdaptiveBrakeConfig } from "../types/rule";

/** Encode an array of rules into a Uint8Array for BLE transmission.
 *  The actual binary format is device‑specific; here we simply JSON‑stringify
 *  and encode as UTF‑8 bytes so the TypeScript compiler is satisfied.
 */
export function encodeRules(rules: Rule[]): Uint8Array {
  const json = JSON.stringify(rules);
  const encoder = new TextEncoder();
  return encoder.encode(json);
}

/** Encode adaptive‑brake configuration.
 *  Placeholder that JSON‑encodes the config.
 */
export function encodeAdaptiveBrake(config: AdaptiveBrakeConfig): Uint8Array {
  const json = JSON.stringify(config);
  const encoder = new TextEncoder();
  return encoder.encode(json);
}

/** Decode BLE text payload back to string (UTF‑8).
 *  In practice the device may send UTF‑8 already; we just return the input.
 */
export function decodeBleText(buf: Uint8Array): string {
  const decoder = new TextDecoder();
  return decoder.decode(buf);
}

/** Example helper to split a large payload into BLE‑size chunks (max 20 bytes).
 */
export function chunkPayload(data: Uint8Array, chunkSize: number = 20): Uint8Array[] {
  const chunks: Uint8Array[] = [];
  for (let i = 0; i < data.length; i += chunkSize) {
    chunks.push(data.subarray(i, i + chunkSize));
  }
  return chunks;
}

