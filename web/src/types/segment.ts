/**
 * セグメント定義 (走行状態認識)
 * 車載IMU(ジャイロ・加速度)により車体ファームウェアがリアルタイム認識するセグメント
 */

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
  VOLTAGE = 18,
}

export const SEG = {
  STRAIGHT: Segment.STRAIGHT,
  RIGHT: Segment.RIGHT,
  LEFT: Segment.LEFT,
  WAVE: Segment.WAVE,
  LEFT_PEAK: Segment.LEFT_PEAK,
  RIGHT_PEAK: Segment.RIGHT_PEAK,
  STRAIGHT_HOLD: Segment.STRAIGHT_HOLD,
  LEFT_HOLD: Segment.LEFT_HOLD,
  RIGHT_HOLD: Segment.RIGHT_HOLD,
  WILDCARD: Segment.WILDCARD,
  LAP: Segment.LAP,
  RUN_START: Segment.RUN_START,
  RUN_STOP: Segment.RUN_STOP,
  VOLTAGE: Segment.VOLTAGE,
} as const;

export const SEG_NAME: Record<number, string> = {
  0: '—',
  1: 'STRAIGHT',
  2: 'RIGHT',
  4: 'LEFT',
  6: 'WAVE',
  7: 'LEFT_PEAK',
  8: 'RIGHT_PEAK',
  9: 'STRAIGHT_HOLD',
  10: 'LEFT_HOLD',
  11: 'RIGHT_HOLD',
  14: 'WILDCARD',
  15: 'LAP',
  16: 'RUN_START',
  17: 'RUN_STOP',
  18: 'VOLTAGE',
};

export interface SegmentMeta {
  icon: string;
  label: string;
  className: string;
}

export const SEG_META: Record<number, [string, string, string]> = {
  1: ['直', '直線', 'seg-line'],
  2: ['右', '右C', 'seg-right'],
  4: ['左', '左C', 'seg-left'],
  6: ['波', 'ウェーブ', 'seg-wave'],
  7: ['左ピーク', '左ピーク後', 'seg-peak-l'],
  8: ['右ピーク', '右ピーク後', 'seg-peak-r'],
  9: ['直継続', '直線継続', 'seg-straight-hold'],
  10: ['左継続', '左C継続', 'seg-hold-l'],
  11: ['右継続', '右C継続', 'seg-hold-r'],
  14: ['★', '時間待機', 'seg-wildcard'],
  15: ['周', '本体ラップ', 'seg-system'],
  16: ['開始', '走行開始', 'seg-system'],
  17: ['停止', '走行停止', 'seg-system'],
};

export interface SegmentGroup {
  label: string;
  kind: 'left' | 'right' | 'straight' | 'wildcard';
  segs: Segment[];
}

export const SEG_GROUPS: SegmentGroup[] = [
  { label: '左C類', kind: 'left', segs: [Segment.LEFT, Segment.LEFT_HOLD, Segment.LEFT_PEAK] },
  { label: '右C類', kind: 'right', segs: [Segment.RIGHT, Segment.RIGHT_HOLD, Segment.RIGHT_PEAK] },
  { label: '直線類', kind: 'straight', segs: [Segment.STRAIGHT, Segment.STRAIGHT_HOLD, Segment.WAVE] },
  { label: '時間待機', kind: 'wildcard', segs: [Segment.WILDCARD] },
];

