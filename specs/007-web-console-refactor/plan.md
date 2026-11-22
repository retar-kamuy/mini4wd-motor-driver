# Implementation Plan: 007 Web Console Refactoring and Modularization

**Feature Branch**: `007-web-console-refactor`
**Feature Spec**: [spec.md](./spec.md)
**Status**: In Progress

## Technical Context

- **現行技術スタック**:
  - HTML5, CSS3 (カスタムプロパティ, Flexbox/Grid, Canvas API, SVG)
  - Vanilla JavaScript (ES2020+, Single File 11,295行)
  - Web Bluetooth API (GATT Client)
  - 外部埋め込みライブラリ: `qrious` (QR生成), `jsQR` (QR認識), `lz-string` (データ圧縮)
- **ターゲット技術スタック (リファクタリング後)**:
  - ビルドツール: Vite (高速HMR、ESモジュールバンドル)
  - 言語: TypeScript / ES Modules (型定義によるバイナリパケット安全性の確保)
  - テストフレームワーク: Vitest (Node環境でのプロトコル往復テスト・バイナリパケットテスト)
  - 通信モジュール: Web Bluetooth Client ラッパー (排他制御キュー、切断再接続)
  - スタイル: CSS 分割 (theme, layout, components)

## Constitution Check

- [x] **テストファースト原則**: プロトコルのエンコード/デコードは、コード分割前に現行 `web/index.html` との入出力一致テストを作成して保護する。
- [x] **モジュール独立性**: BLE通信・バイナリパケットパーサー・ルール自然文ジェネレータは DOM から完全に独立した純粋関数/クラスとして設計する。
- [x] **後方互換性**: 車体ファームウェアとの GATT UUID、コマンドID、パケット長、および LocalStorage キーの互換性を 100% 維持する。

## Implementation Phases

### Phase 0: リサーチ & 設計確定
- [contracts/vehicle-app-protocol.md](./contracts/vehicle-app-protocol.md) に基づき、全12種のキャラクタリスティックとバイナリパケット構造を確定。
- [research.md](./research.md) で Vite 構成、Web Bluetooth モック戦略、外部ライブラリの npm 化方針を策定。

### Phase 1: データモデル & インターフェース定義
- [data-model.md](./data-model.md) で `Rule`, `TelemetrySample`, `BulkLogRow`, `GattCommand` の TypeScript 型定義を策定。
- [quickstart.md](./quickstart.md) で開発者/Codex向けのセットアップ・テスト実行・ビルド手順を整備。

### Phase 2: コアロジックの抽出と単体テスト（Phase A）
- `src/ble/protocol.ts`: `encodeRules()`, `parseBulkRowsFromPacket()`, `decodeBleText()` などを抽出。
- `test/protocol.test.ts`: 現行 `index.html` から抽出したテストベクタによるバイナリ往復検証。

### Phase 3: アセットとスタイルの分離（Phase B）
- `web/index.html` のインライン `<style>`（3,200行）を `src/styles/` 配下の論理ファイル（theme, layout, components）へ分割。
- インライン外部ライブラリを `package.json` 依存関係へ移行。

### Phase 4: UIコンポーネント化と状態管理の分離（Phase C）
- ヘッダー、ワークスペース、ルールエディタ、ラップタイマー、ウィザードの各コンポーネントを独立。
