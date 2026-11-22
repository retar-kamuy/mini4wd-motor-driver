# Research: Web Console Refactoring Architecture

**Feature**: 007-web-console-refactor
**Date**: 2026-11-22

## 1. ビルドツール選定: Vite vs バニラES Modules

### 検討課題
現行の `web/index.html` はビルド不要でブラウザから直接開ける利点があるが、11,300行の単一ファイルであるため、AIや開発者が安全に改修できない。

### 決定: Vite + TypeScript (静的シングルHTML出力対応)
- **選定理由**:
  1. **高速な開発体験**: ローカル開発サーバー起動が瞬時（ESMネイティブ）。
  2. **型安全性**: バイナリパケット（Uint8Array, DataView）のオフセットや型不整合をコンパイル時に検知可能。
  3. **スタンドアロンHTML出力 (vite-plugin-singlefile)**: 必要に応じて従来の「1つのHTMLを開くだけで動く」配布形態もビルド成果物として生成可能。
  4. **テスト環境の親和性**: Vitest をそのまま併用でき、Node環境でプロトコルテストを即座に実行可能。

## 2. Web Bluetooth のテスタビリティとモック戦略

### 検討課題
Web Bluetooth API は物理的なBluetoothアダプタとミニ四駆実機が必要なため、CI環境や実機なしの開発・テストが困難。

### 決定: `BleTransport` 抽象インターフェースの導入
- GATT操作を直接 `navigator.bluetooth` で呼ぶのではなく、`BleTransport` インターフェースを挟む。
- **実装形態**:
  - `WebBluetoothTransport`: 実ブラウザ用（`navigator.bluetooth` を利用）
  - `MockBluetoothTransport`: 開発・テスト用。仮想のミニ四駆ファームウェア（仮想IMU角速度、仮想テレメトリ、走行ステータス遷移）をエミュレート。
- **効果**: ブラウザ上で「仮想ミニ四駆に接続」ボタンを設けることで、実機なしでもUI挙動、アニメーション、ログ受信のE2Eテストが可能になる。

## 3. 外部ライブラリ（qrious, jsQR, lz-string）の移行

- 現行はスクリプトタグ内に Minified コードが直接貼り付けられている。
- npm パッケージ（`lz-string`, `jsqr`, `qrious`）へ移行し、Vite バンドルで管理。
- バンドルサイズの最適化とコードベースのクリーン化を実現。

