import { Segment } from './segment';
import { ActionType } from './action';

export enum MachineStatus {
  IDLE = 0,
  READY = 1,
  RUNNING = 2,
  STOPPED = 3,
  ERROR = 4,
}

export const STATUS_NAME: Record<number, string> = {
  0: 'IDLE',
  1: 'READY',
  2: 'RUNNING',
  3: 'STOPPED',
  4: 'ERROR',
};

/**
 * 低速テレメトリ（リアルタイム受信）
 */
export interface TelemetrySample {
  timestampMs: number;
  vbatMv: number;       // バッテリー電圧 (mV)
  midMv: number;        // 中間電圧 (mV)
  temp10: number;       // 基板温度 (°C * 10)
  speedDps?: number;    // 推定速度
  currentSeg?: Segment; // 認識セグメント
}

/**
 * 停止後バルクログ（車体Flashから高密度取得した走行ログ1行）
 */
export interface BulkLogRow {
  t: number;            // 走行開始からの経過時間 (ms)
  seg: Segment;         // 認識セグメント
  rule: number;         // 発火ルール番号 (0xFF = なし)
  act: ActionType;      // 実行アクション
  gz: number;           // ジャイロ角速度 (dps)
  peak: number;         // ピーク角速度 (dps)
  dur: number;          // セグメント継続時間 (ms)
  actionIdx?: number;
  finalMs?: number;
  vDeltaMs?: number;
  sagDeltaMs?: number;
  sagMv: number;        // 電圧サグ (mV)
  vbatMv: number;       // バッテリー電圧 (mV)
  temp10: number;       // 基板温度 (°C * 10)
  midMv?: number;
  vbatMinusMidMv?: number;
  brakeVbatMv?: number;
}

