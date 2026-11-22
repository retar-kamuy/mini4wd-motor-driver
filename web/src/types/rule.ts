import { Segment } from './segment';
import { ActionType } from './action';

export enum TriggerMode {
  EVERY = 0,
  ODD = 1,
  EVEN = 2,
  EVERY_N = 3,
  ONLY_N = 4,
}

export const TRIG = {
  EVERY: TriggerMode.EVERY,
  ODD: TriggerMode.ODD,
  EVEN: TriggerMode.EVEN,
  EVERY_N: TriggerMode.EVERY_N,
  ONLY_N: TriggerMode.ONLY_N,
} as const;

export const TRIG_NAME: Record<number, string> = {
  0: '毎回',
  1: '奇数回',
  2: '偶数回',
  3: 'くり返し',
  4: 'N回目のみ',
};

export interface RuleAction {
  type: ActionType;
  durationMs: number; // 実行時間 ms (0〜65535, STOPは0)
  strength: number;   // 出力/強度 (0〜255)
}

export interface RuleGuideMeta {
  sentence?: string;
  targetPlace?: string;
  userIntent?: string;
  [key: string]: unknown;
}

export interface Rule {
  pattern: Segment[];         // 最大8要素
  actions: RuleAction[];      // 最大5要素
  loopMode?: boolean;         // ループ実行
  triggerMode?: TriggerMode;  // トリガー種別 (0:毎回, 1:奇数, 2:偶数, 3:N回ごと, 4:N回目のみ)
  triggerN?: number;          // N回 (1〜255)
  triggerPhase?: number;      // 対象位相 (1〜triggerN)
  priority?: number;          // 優先度 (1〜255, デフォルト100)
  peakAfterMs?: number;       // ピーク後判定時間 (0xFFFFで無効/共通設定使用)
  straightHoldMs?: number;    // 直線継続判定時間 (0xFFFFで無効/共通設定使用)
  curveLongMs?: number;       // カーブ長判定時間 (0xFFFFで無効/共通設定使用)
  wildcardMs?: number;        // ★待機時間 (0〜2000ms, デフォルト1000)
  confirmMs?: number;         // 発火前確認時間 (0〜500ms)
  confirmCancelMask?: number; // キャンセルマスク
  _guideMeta?: RuleGuideMeta; // ウィザード・自然文用のメタ情報
}

export interface AdaptiveBrakeConfig {
  sagCompEnabled?: boolean;
  sagTargetMv?: number;
  sagGainPct?: number;
  vbatCompEnabled?: boolean;
  vbatTargetMv?: number;
  vbatGainPct?: number;
}

