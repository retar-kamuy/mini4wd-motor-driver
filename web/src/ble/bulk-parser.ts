// Minimal bulk‑log parser placeholder for Mini‑4WD web console
// In a real implementation this would parse the binary BLE bulk log format.
// Here we simply expose a trivial parser that converts a JSON string
// into a BulkLogRow object – sufficient for type‑checking and test scaffolding.

import type { BulkLogRow } from "../types/telemetry";

/** Parse a bulk‑log payload (UTF‑8 JSON) into a BulkLogRow.
 *  This placeholder returns `null` if parsing fails.
 */
export function parseBulkLog(jsonStr: string): BulkLogRow | null {
  try {
    const obj = JSON.parse(jsonStr) as Partial<BulkLogRow>;
    // Very shallow validation – ensure required fields exist
    if (obj.t !== undefined && obj.seg && obj.rule !== undefined && obj.act !== undefined) {
      return obj as BulkLogRow;
    }
    return null;
  } catch (_) {
    return null;
  }
}

