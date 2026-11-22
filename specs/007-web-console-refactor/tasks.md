# Tasks: 007 Web Console Refactoring and Modularization

**Input**: Design documents from `/specs/007-web-console-refactor/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

- **[P]**: 並行実行可能（異なるファイル、依存関係なし）
- **[Story]**: 対象ユーザーストーリー（US1, US2, US3）

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: リファクタリング用ビルド環境とテスト環境の初期化

- [ ] T001 `web/package.json` を作成し、Vite, TypeScript, Vitest, `@types/web-bluetooth` を定義
- [ ] T002 `web/tsconfig.json` を作成し、ES2022 / DOM 型環境を設定
- [ ] T003 [P] `web/vite.config.ts` を作成（静的ビルド設定およびVitest環境設定）

---

## Phase 2: Foundational (Core Types & Enums)

**Purpose**: すべてのモジュールが依存する共通データ型と定数の定義

- [ ] T004 [P] `web/src/types/segment.ts` に `SEG` 定数と `Segment` 列挙型を定義
- [ ] T005 [P] `web/src/types/action.ts` に `ACTION` 定数と `ActionType` 列挙型を定義
- [ ] T006 [P] `web/src/types/rule.ts` に `Rule`, `RuleAction`, `TriggerMode` インターフェースを定義
- [ ] T007 [P] `web/src/types/telemetry.ts` に `TelemetrySample`, `BulkLogRow` 型を定義
- [ ] T008 [P] `web/src/ble/constants.ts` に サービスUUIDおよびキャラクタリスティックUUID定数を定義

**Checkpoint**: 基礎型定義完了 - 各ユーザーストーリーの実装に着手可能

---

## Phase 3: User Story 1 - 仕様・プロトコルの完全理解と仕様書化 (Priority: P1) 🎯 MVP

**Goal**: Codexおよび開発者が迷わず改修できるよう、プロトコル仕様とテストベクタを整備

### Implementation for User Story 1

- [ ] T009 [US1] `specs/007-web-console-refactor/contracts/vehicle-app-protocol.md` の仕様を検証し、各キャラクタリスティックのバイナリフォーマット定義を最終確定
- [ ] T010 [US1] 現行 `web/index.html` の `encodeRules` から抽出したテスト用ルールセット（期待バイナリ）のテストベクタ `web/test/fixtures/rules-fixture.json` を作成
- [ ] T011 [US1] 現行 `web/index.html` の `parseBulkRowsFromPacket` 用のサンプルパケットベクタ `web/test/fixtures/bulk-packets.json` を作成

**Checkpoint**: US1完了 - プロトコル仕様と正解データ（テストベクタ）が確定

---

## Phase 4: User Story 2 - バイナリプロトコル & ルール処理の独立モジュール化とテスト整備 (Priority: P2)

**Goal**: 車体ファームウェアとの通信互換性を保証する純粋関数モジュールと単体テストの構築

### Tests for User Story 2

- [ ] T012 [P] [US2] `web/test/protocol.test.ts` に `encodeRules` のバイナリ互換性テストを作成（テストベクタと1バイト単位で完全一致すること）
- [ ] T013 [P] [US2] `web/test/bulk-parser.test.ts` に `parseBulkRowsFromPacket` の可変長パケット復元テストを作成
- [ ] T014 [P] [US2] `web/test/rule-sentence.test.ts` に自然文サマリ生成（`buildRuleSentence`）の出力テストを作成

### Implementation for User Story 2

- [ ] T015 [US2] `web/src/ble/protocol.ts` を実装（`encodeRules`, `encodeAdaptiveBrake`, `decodeBleText` 等の純粋関数）
- [ ] T016 [US2] `web/src/ble/bulk-parser.ts` を実装（バルクログのパケットデコード処理）
- [ ] T017 [US2] `web/src/rules/sentence.ts` を実装（ルールの自然文生成・日本語ラベル変換）
- [ ] T018 [US2] `web/src/ble/queue.ts` を実装（Web Bluetooth GATT排他制御キュー）

**Checkpoint**: US2完了 - 実機なしでプロトコル互換性とルール変換が100%単体テストで保証される

---

## Phase 5: User Story 3 - 静的アセット・UI・ライブラリのディレクトリ分離 (Priority: P3)

**Goal**: 単一ファイルからCSS、外部ライブラリ、UIパーツを論理分割し、保守性を向上

### Implementation for User Story 3

- [ ] T019 [P] [US3] `web/src/styles/theme.css` にカラー変数・グラデーション・アニメーションを分離
- [ ] T020 [P] [US3] `web/src/styles/layout.css` にヘッダー・ワークスペース・サイドバーのレイアウトスタイルを分離
- [ ] T021 [P] [US3] `web/src/styles/components.css` にカード・ボタン・モーダルのスタイルを分離
- [ ] T022 [US3] 外部ライブラリ（`lz-string`, `jsqr`, `qrious`）をインラインから npm 依存関係へ移行
- [ ] T023 [US3] `web/src/components/header.ts` にヘッダーUI更新・接続インジケータ処理を分離
- [ ] T024 [US3] `web/src/components/rules-editor.ts` にルール設定カードUIを分離
- [ ] T025 [US3] `web/src/components/lap-timer.ts` に周回タイマー・セクション比較UIを分離
- [ ] T026 [US3] `web/src/components/wizard.ts` にかんたん設定ウィザードUIを分離

**Checkpoint**: US3完了 - 各機能が独立したTypeScript/CSSファイルに分割され、LLMが安全に編集可能になる

---

## Phase 6: Polish & Cross-Cutting Concerns

- [ ] T027 [P] `web/README.md` に新構成のアーキテクチャと開発ガイドを整備
- [ ] T028 全体ビルド（`npm run build`）を実行し、生成されたHTMLが既存ブラウザでエラーなく起動することを確認
- [ ] T029 既存の `web/index.html` との機能差分・退行（リグレッション）がないかを総合検証

---

## Dependencies & Execution Order

1. **Phase 1 (Setup)** → **Phase 2 (Foundational)**: 順次実行
2. **Phase 3 (User Story 1)**: プロトコル仕様と正解ベクタの確定
3. **Phase 4 (User Story 2)**: テスト先行（T012〜T014）→ 実装（T015〜T018）
4. **Phase 5 (User Story 3)**: スタイル・UIの分割
5. **Phase 6 (Polish)**: 総合ビルド・検証

