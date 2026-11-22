# Data Model & Protocol Entities: 007 Web Console

**Feature**: 007-web-console-refactor
**Date**: 2026-11-22

## 1. Core Enums

### 1.1 Segment Enum (`SEG`)
```typescript
export enum Segment {
  NONE = 0,
  STRAIGHT = 1,
  RIGHT = 2,
  LEFT = 4,
  WAVE = 6,
  LEFT_PEAK = 7,
  RIGHT_PEAK = 8,
  STRAIGHT_HOLD = 9,
  LEFT_HOLD = 10,
  RIGHT_HOLD = 11,
  WILDCARD = 14,
  LAP = 15,
  RUN_START = 16,
  RUN_STOP = 17,
  VOLTAGE = 18
}
```

### 1.2 Action Enum (`ACTION`)
```typescript
export enum ActionType {
  NONE = 0,
  BRAKE = 1,
  SPEED = 2,
  STOP = 4,
  WAIT = 5,
  LOCK = 6,
  CANCEL = 7
}
```

### 1.3 Trigger Mode Enum (`TRIG`)
```typescript
export enum TriggerMode {
  EVERY = 0,
  ODD = 1,
  EVEN = 2,
  EVERY_N = 3,
  ONLY_N = 4
}
```

---

## 2. Core Entities

### 2.1 Action Item
```typescript
export interface RuleAction {
  type: ActionType;
  durationMs: number;  // 0〜65535 (STOPの場合は0)
  strength: number;    // 0〜255 (Duty%またはブレーキ強度)
}
```

### 2.2 Rule Definition
```typescript
export interface Rule {
  id?: string;
  pattern: Segment[];         // 最大8要素
  actions: RuleAction[];      // 最大5要素
  loopMode: boolean;          // ループ実行
  triggerMode: TriggerMode;
  triggerN: number;           // 1〜255
  triggerPhase: number;       // 1〜triggerN
  priority: number;           // 1〜255 (デフォルト100)
  peakAfterMs?: number;       // 0xFFFFで未設定
  straightHoldMs?: number;    // 0xFFFFで未設定
  curveLongMs?: number;       // 0xFFFFで未設定
  wildcardMs?: number;        // ★待機時間 (0〜2000ms)
  confirmMs?: number;         // 発火前確認時間 (0〜500ms)
  confirmCancelMask?: number; // 確認中キャンセルマスク
  _guideMeta?: {
    sentence?: string;
    targetPlace?: string;
    userIntent?: string;
  };
}
```

### 2.3 Bulk Log Row
```typescript
export interface BulkLogRow {
  t: number;          // 走行開始からの経過時間 (ms)
  seg: Segment;       // 認識セグメント
  rule: number;       // 発火ルール番号 (0xFF = なし)
  act: ActionType;    // 実行アクション
  gz: number;         // ジャイロ角速度 (dps)
  peak: number;       // ピーク角速度 (dps)
  dur: number;        // セグメント継続時間 (ms)
  vbatMv: number;     // バッテリー電圧 (mV)
  sagMv: number;      // 電圧サグ (mV)
  temp10: number;     // 基板温度 (°C * 10)
}
```

