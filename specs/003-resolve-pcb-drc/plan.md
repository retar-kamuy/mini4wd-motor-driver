# Implementation Plan: DRC解消後の基板設計の収束

**Branch**: `master` | **Date**: 2026-11-10 | **Spec**: [spec.md](spec.md)

## Summary

正規KiCadプロジェクトに対し、全チェック有効のDRC/ERC 0件を維持しながら、既存仕様の5 A設計目標、反対端のコネクタ、昇圧部の電流ループ、部品・製造データの残課題を解消する。部品資料と電流経路の根拠を先に確定し、配置と配線をまとめて再設計した後、同一版を検証する。

## Technical Context

- **対象**: `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_{sch,pcb,pro}`、同ディレクトリのシンボル・フットプリント、製造成果物。
- **開発環境**: WSL/Linuxのシェル（Spec Kitの `sh` 設定、提供スクリプトはBash）。PowerShellおよびWindowsのパスは不要。
- **検証環境**: KiCad 10.0.8、`kicad-cli`、pcbnew、KiCad/EMC/BOM解析器、ngspice。解析結果は同じ基板版のハッシュとともに保存する。既存 `002` FR-012 はKiCad MCPの使用を要求するが、現在のセッションで該当ツールは未検出。実装前にMCPの利用可能性を再確認し、使用できなければ要件の扱いをユーザーと明確にする。
- **機構・層**: 55 × 21 mm、2銅層、1.6 mm厚、表面実装、底面ビア全数テント、J1/J2は反対端で外向き。部品干渉・嵌合・金属タブ付近の禁止銅をメーカー図面で照合。
- **設計目標**: 5 Aの駆動主経路について既存 `specs/002-port-to-kicad/spec.md` FR-008の1.5～2.0 mmまたは銅箔、狭窄とビアの根拠を満たす。検出分岐は主電流経路と別に識別する。既存設計前提1 ozは製造仕様として未確定。
- **検査**: DRC/ERC全項目有効・パリティ・全ネット照合、部品資料、底面マスク、EMCリスク、製造層・穴・BOM/CPL。製造後の独立熱認定および車体実機クリアランスを新たな必須ゲートにしない。
- **未確定条件の扱い**: 実際の製造銅厚・メッキ、許容温度上昇、電流時間波形、未選定MPNは入力と根拠を調査・明記し、証拠なしに5 A達成や製造準備完了を宣言しない。必要時は選択肢と影響を具体化して相談する。

## Constitution Check

`.specify/memory/constitution.md` は未記入テンプレートのため評価対象外。`AGENTS.md` のKiCad・datasheets・bom・emc等の適用指示と、既存specの確定済み判断を適用する。設計後も再評価する。

## Project Structure

```text
specs/003-resolve-pcb-drc/
├── spec.md, research.md, plan.md, data-model.md
├── contracts/design-and-verification.md
├── quickstart.md, tasks.md, implementation.md
└── verification/                   # 基準結果、更新後の根拠
hardware/kicad/mini4wd-motor-driver/ # 正規設計とライブラリ
```

旧 `hardware/archive/kicad-before-consolidation/...` は来歴の参照先。最新の設計対象として編集しない。

## Design and sequencing

1. **基準・前提**: KiCad MCPの利用可能性と既存FR-012を確認し、現状のDRC/ERC、73ピン照合、22実装品と旧24部品要件の差、アノテーション警告を記録する。コピーや古いレポートを最新版と扱わない。
2. **部品・機構・回路**: 全MPNとメーカー資料を照合し、J1/J2の正式な2極図面、XIAO、L1、Q1/Q2などの端子/ランド/極性/機構を確認。Q1の資料URLの型番差とBOM不足を解決する。
3. **電流モデル**: 駆動時のJ1.1→VBAT（MOTOR_PLUS相当）→J2.1、J2.2→Q1→J1.2に加え、Q2・D_FLYを含むブレーキ・還流と信号分岐を回路図・資料から検証し、状態別に台帳化する。記述は確認すべき仮説であり、記号・極性を照合してから採用する。
4. **配置・配線**: コネクタとXIAOを反対端に収める配置候補を比較し、Q1/Q2・主電流経路・U2/L1/CIN/COUT/U1バイパスを同時に最適化。メーカーの推奨ループに従いSWとFBを分離し、層を跨ぐ主電流経路・帰路を検討する。部品のCourtyardを根拠なく縮めず、既存のDRC設定を緩和しない。
5. **検証・製造**: 電流・ビアの仮定を記録し、DRC/ERC、全パッドの回路図との一致、底面テントを検証。EMCの23件は各項目を実形状と照合し、対応または根拠を記録。確定した同一版からGerber/Excellon/BOM/CPLを出力し、ビューアと製造先の入力検証を行う。

## Exit gates

- 元の73ピンの接続と意図したI2Cネット名変更を引き継ぎ、部品数差とアノテーション警告を解決または根拠付きで判定。
- 高電流主経路とビア、各動作モード、コネクタ、部品資料・BOMの根拠を記録。条件未確定ならその項目は未完了のままにする。
- 完了時点で全DRC/ERCチェック0件、未接続0件、回路図との不一致0件。再解析結果と実際に確認した製造データを紐付ける。
- EMC解析はリスク評価であり規格適合試験の代替ではない。実機熱認定・車体実機クリアランスの既存免除は維持する。
