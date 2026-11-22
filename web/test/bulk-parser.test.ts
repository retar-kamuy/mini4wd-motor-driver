import { parseBulkLog } from "../src/ble/bulk-parser";
import type { BulkLogRow } from "../src/types/telemetry";

test("parseBulkLog returns object for valid JSON", () => {
  const json = JSON.stringify({
    t: 123,
    seg: { type: "STRAIGHT", length: 5 },
    rule: 2,
    act: 1,
    gz: 0,
    peak: 0,
    dur: 100,
    sagMv: 0,
    vbatMv: 5000,
    temp10: 250
  } as Partial<BulkLogRow>);
  const result = parseBulkLog(json);
  expect(result).not.toBeNull();
  if (result) {
    expect(result.t).toBe(123);
    expect(result.rule).toBe(2);
  }
});

test("parseBulkLog returns null for invalid JSON", () => {
  const result = parseBulkLog("not a json");
  expect(result).toBeNull();
});

