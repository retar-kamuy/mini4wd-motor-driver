/**
 * Web Bluetooth GATT UUID 定数
 */

export const BLE_UUID = {
  service:       '12345678-1234-5678-1234-56789abcdef0',
  command:       '12345678-1234-5678-1234-56789abcdef4',
  status:        '12345678-1234-5678-1234-56789abcdef5',
  seg:           '12345678-1234-5678-1234-56789abcdef6',
  speed:         '12345678-1234-5678-1234-56789abcdefa',
  params:        '12345678-1234-5678-1234-56789abcdf00',
  rules:         '12345678-1234-5678-1234-56789abcdefd',
  bulk:          '12345678-1234-5678-1234-56789abcdefc',
  telemetry:     '12345678-1234-5678-1234-56789abcdf01',
  adaptiveBrake: '12345678-1234-5678-1234-56789abcdf02',
  firmwareInfo:  '12345678-1234-5678-1234-56789abcdf03',
  deviceName:    '12345678-1234-5678-1234-56789abcdf04',
} as const;

export const CMD = {
  RUN: 1,
  STOP: 2,
  SAVE_FLASH: 3,
  LOG_REQUEST: 4,
  LOG_GET: 7,
  LOG_ABORT: 8,
  CALIBRATE: 9,
} as const;

export const RECOMMENDED_FW_VERSION = 'v3.58-r10';

