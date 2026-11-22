# Quickstart: 007 Web Console Development

**Feature**: 007-web-console-refactor
**Date**: 2026-11-22

## 概要
本ガイドは、`web/` 配下のWebコンソールを開発・テスト・検証するためのクイックスタート手順書です。

---

## 1. 動作確認（現行単一HTML）

現行の `web/index.html` はローカルHTTPサーバー経由で直接ブラウザから実行可能です。

```bash
# Python によるシンプルなHTTPサーバーの起動
python3 -m http.server 8080 --directory web/
```
ブラウザで `http://localhost:8080/index.html` を開きます。
（※Web Bluetooth APIは `localhost` または `https://` でのみ動作します）

---

## 2. リファクタリング後の開発手順（Vite環境導入後）

### 依存関係のインストール
```bash
npm install
```

### 開発サーバー起動（HMR有効）
```bash
npm run dev
```

### 単体テストの実行（バイナリプロトコル等）
```bash
npm test
```

### 本番ビルド（スタンドアロンHTML出力）
```bash
npm run build
```
`dist/index.html` に、配布用の単一ファイルが出力されます。

