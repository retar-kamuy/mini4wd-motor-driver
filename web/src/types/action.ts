/**
 * アクション定義 (制御指示)
 * ルール条件合致時にモーターへ指示する制御コマンド
 */

export enum ActionType {
  NONE = 0,
  BRAKE = 1,
  SPEED = 2,
  STOP = 4,
  WAIT = 5,
  LOCK = 6,
  CANCEL = 7,
}

export const ACTION = {
  NONE: ActionType.NONE,
  BRAKE: ActionType.BRAKE,
  SPEED: ActionType.SPEED,
  STOP: ActionType.STOP,
  WAIT: ActionType.WAIT,
  LOCK: ActionType.LOCK,
  CANCEL: ActionType.CANCEL,
} as const;

export const ACTION_NAME: Record<number, string> = {
  0: 'NONE',
  1: 'BRAKE',
  2: 'SPEED',
  4: 'STOP',
  5: 'WAIT',
  6: 'LOCK',
  7: 'CANCEL',
};

export const ACTION_LABEL: Record<number, string> = {
  0: 'なし',
  1: 'ブレーキ',
  2: '速度調整',
  4: '停止',
  5: '待機',
  6: 'アクション無効',
  7: '候補キャンセル',
};

export const ACTION_CLASS: Record<number, string> = {
  0: 'act-none',
  1: 'act-brake',
  2: 'act-speed',
  4: 'act-stop',
  5: 'act-wait',
  6: 'act-lock',
  7: 'act-cancel',
};

