# Tasks: DRC解消後の基板設計の収束

**入力**: [spec.md](spec.md)、[plan.md](plan.md)、[research.md](research.md)、[data-model.md](data-model.md)、[契約](contracts/design-and-verification.md)  
**設計正本**: `hardware/kicad/mini4wd-motor-driver/`。一時ファイルは操作の検証に限り使用し、正本と取り違えない。  
**現状**: 過去のDRC/ERC 0件は変更前の基準値。Q2の回路図とPCBの端子修正後、暫定DRC/ERCとパッド照合は0件。5 A、機構、部品照合などは未完了で、旧Gerberプレビューは製造不可。未実施の項目を完了扱いにしない。

## Phase 1: Setup

- [x] T001 正規設計と変更前のDRC/ERC結果を `specs/003-resolve-pcb-drc/verification/remaining-work.md` に記録する
- [x] T002 変更前の全チェック有効DRC/ERCを `specs/003-resolve-pcb-drc/verification/drc-all.rpt` と `specs/003-resolve-pcb-drc/verification/erc.rpt` に保存する
- [x] T003 変更前の設計・ライブラリのハッシュ、KiCad版、作業ツリーを `specs/003-resolve-pcb-drc/verification/design-baseline.md` に記録する
- [x] T004 KiCad MCP 2.8.3 のWSL起動方法、使用したMCP操作、依存と再現手順を `specs/003-resolve-pcb-drc/verification/design-baseline.md` に追記し、正規プロジェクトをMCPで開けることを確認する

## Phase 2: Foundational

- [ ] T005 元BOMと現回路図の部品を突き合わせ、24部品の記述と基板実装22部品との差、アノテーション警告、Q1/U1の資料URL修正を `specs/003-resolve-pcb-drc/verification/parts-evidence.md` に根拠とともに記録する
- [ ] T006 [P] 実装候補全品のメーカー・MPN・定格・資料を照合し、未選定品とL1の型番相違を `specs/003-resolve-pcb-drc/verification/bom-selection.md` に記録する
- [ ] T007 [P] 1 oz前提、製造銅厚・ビアめっき、動作波形と許容温度上昇の条件・不足情報を `specs/003-resolve-pcb-drc/verification/current-budget.md` に記録する
- [x] T008 [P] Q2の1–3=S、4=G、5–8=Drainというメーカー端子と現回路図・PCBを照合し、5番の修正途中状態と必要な配線変更を `specs/003-resolve-pcb-drc/verification/q2-repair.md` に記録する
- [x] T009 `specs/003-resolve-pcb-drc/verification/q2-repair.md` に、MCP `sync_schematic_to_board` が `/I2C_SDA`・`/I2C_SCL` の先頭スラッシュを落とす問題と、正規設計に適用する前の局所修正・ネット比較手順を記録する

## Phase 3: US1 基板の違反を解消する（P1）

**目標**: Q2誤接続を除き、機能を保持して全DRCを解消する。  
**独立検証**: 全チェック・銅箔再充填・パリティを有効にしたDRCで違反・未接続・不一致0件。

- [ ] T010 [US1] `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sym` と `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sch` のQ2シンボルについて、5番をDrainに変更した既存修正をメーカー端子と図記号の見やすさまで照合する
- [x] T011 [US1] `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` のQ2 pad 5をMOTOR_MINUSに接続し、既存VBAT配線との接触を除去してMOTOR_MINUS側へ再配線する。I²Cなど他ネットは意図せず変更しない
- [x] T012 [US1] Q2 1–3=VBAT、4=GATE_DRIVE、5–8・重複Drainパッド=MOTOR_MINUS、および他の全パッドの対応を `specs/003-resolve-pcb-drc/verification/q2-repair.md` に記録する
- [ ] T013 [US1] 再配置・再配線後に `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` で全DRCを実行し、`specs/003-resolve-pcb-drc/verification/drc-final.rpt` にエラー・警告・未接続・パリティ不一致0件を記録する

## Phase 4: US2 修正を確認できる（P2）

**目標**: 変更理由、版、検査結果と未確定事項を追跡可能にする。  
**独立検証**: 変更ファイルのハッシュと最終検証記録から結果を再現できる。

- [x] T014 [US2] 基準時の対象、検証済みと残件を `specs/003-resolve-pcb-drc/implementation.md` と `specs/003-resolve-pcb-drc/verification/remaining-work.md` に記録する
- [x] T015 [US2] Q2修正、MCPによる変更、採用した仮定と残る制約を `specs/003-resolve-pcb-drc/implementation.md` と `specs/003-resolve-pcb-drc/verification/remaining-work.md` に更新する
- [ ] T016 [US2] 最終設計・ライブラリ・成果物のハッシュ、実行した検査、結果と未検証事項を `specs/003-resolve-pcb-drc/verification/final-review.md` にまとめる

## Phase 5: US3 電源・駆動経路と昇圧部を再設計する（P1）

**目標**: 5 A設計目標の経路と昇圧部の配置・帰路を根拠付きで設計する。  
**独立検証**: 動作モード別の経路、狭窄・ビア・部品定格、昇圧ループとEMC指摘の根拠を確認できる。

- [ ] T017 [US3] J1/J2、Q1/Q2、D_FLYのメーカー端子と回路図を照合し、駆動・ブレーキ・還流・検出分岐およびVBAT/MOTOR_PLUSの関係を `specs/003-resolve-pcb-drc/verification/current-budget.md` に記録する
- [ ] T018 [US3] 主経路の幅・銅厚・狭窄・層・実際に並列分担するビア・めっき・温度前提を `specs/003-resolve-pcb-drc/verification/current-budget.md` に示し、5 A目標を評価する
- [ ] T019 [US3] Q1/Q2の共有ゲートについて電池電圧範囲、起動・停止、切替時の同時導通、駆動能力と損失を `specs/003-resolve-pcb-drc/verification/drive-review.md` に評価し、必要な回路変更を正規回路図へ反映する
- [ ] T020 [US3] J1/J2とU2/L1/CIN/COUT/U1を共同で再配置し、メーカー推奨ループ・帰路を `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` と `specs/003-resolve-pcb-drc/verification/layout-decisions.md` に反映する
- [ ] T021 [US3] 主電流経路を1.5～2.0 mm幅または専用銅箔で再設計し、端子の狭窄と層間遷移を `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` と `specs/003-resolve-pcb-drc/verification/current-budget.md` に反映する
- [ ] T022 [US3] SW_BOOST、FB_BOOST、GATE_DRIVEおよび検出信号を再配線し、ループ・帰路・分離の根拠を `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` と `specs/003-resolve-pcb-drc/verification/layout-decisions.md` に記録する
- [ ] T023 [US3] 最新設計でEMC解析を再実行し、各指摘の対応・誤検出・未測定を `specs/003-resolve-pcb-drc/verification/emc-review.md` に記録する

## Phase 6: US4 部品と機構を整合させる（P1）

**目標**: 部品資料、基板形状と両端コネクタを一致させる。  
**独立検証**: 全品の端子・ランド・MPNとコネクタ位置・向きをメーカー資料と比較できる。

- [ ] T024 [US4] Molex 43650-0214、XIAO MG24 Sense、L1、Q1/Q2、U1/U2の適用型番・端子・パッケージ・定格を `specs/003-resolve-pcb-drc/verification/parts-evidence.md` に資料とページ付きで照合する
- [ ] T025 [US4] `hardware/kicad/mini4wd-motor-driver/board-routed.pretty/` のXIAO、Molex、L1、Q2を優先してランド・マスク・Courtyard・端子をメーカー図面と比較し、必要な修正と根拠を `specs/003-resolve-pcb-drc/verification/parts-evidence.md` に反映する
- [ ] T026 [US4] T020の共同配置でJ1/J2を反対端・外向きとし、基板端・嵌合・保持タブ・禁止銅の条件を `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` と `specs/003-resolve-pcb-drc/verification/layout-decisions.md` に反映する
- [ ] T027 [US4] 照合済みメーカー・MPNを `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sch` に反映し、調達・実装可否を `specs/003-resolve-pcb-drc/verification/bom-selection.md` に記録する
- [ ] T028 [US4] 55 × 21 mm、1.6 mm厚、2銅層、表面実装と裏面テントを `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` で確認し、`specs/003-resolve-pcb-drc/verification/final-review.md` に記録する

## Phase 7: US5 検証して製造用データを整える（P2）

**目標**: 同じ最終設計版から検証済み製造データを整える。  
**独立検証**: 全ERC/DRC・ネット照合とGerber・穴・BOM・CPLの一致を再現できる。

- [ ] T029 [US5] 正規回路図と基板の全チェック有効ERC・DRC・パリティを再実行し、`specs/003-resolve-pcb-drc/verification/erc-final.rpt` と `specs/003-resolve-pcb-drc/verification/drc-final.rpt` に結果を記録する
- [ ] T030 [US5] 最終回路図ネットリストとPCB全パッドをメーカー端子と照合し、Q2の根拠ある変更とI²C名を含む差分を `specs/003-resolve-pcb-drc/verification/final-review.md` に記録する
- [ ] T031 [US5] 同一最終版から `hardware/kicad/mini4wd-motor-driver/manufacturing/gerber/` にGerber・Excellonを生成し、ビューアで層・穴・外形・底面マスクを照合する
- [ ] T032 [US5] 確定した部品から `hardware/kicad/mini4wd-motor-driver/manufacturing/bom.csv` と `hardware/kicad/mini4wd-motor-driver/manufacturing/cpl.csv` を生成し、座標・回転・JLCPCB供給と組立可否を照合する
- [ ] T033 [P] [US5] 既存FR-011のIPC-D-356要求と出力可否を調査し、必要な `hardware/kicad/mini4wd-motor-driver/manufacturing/mini4wd-motor-driver.ipc` または未解決理由を `specs/003-resolve-pcb-drc/verification/ipc-d356.md` に記録する
- [ ] T034 [US5] 同一版で回路図・PCB・相互照合・熱・SPICE・Gerber解析を実施し、適用範囲・実行できない項目・誤検出を `specs/003-resolve-pcb-drc/verification/final-review.md` に記録する
- [ ] T035 [US5] 製造先のファイル検証、EMC・電流・部品の限界、未実施実測、成果物ハッシュを `specs/003-resolve-pcb-drc/verification/final-review.md` に記録する

## Phase 8: 全体の整合性

- [ ] T036 `specs/002-port-to-kicad/progress-summary.md` と `specs/003-resolve-pcb-drc/implementation.md` を最終版の根拠に更新し、過去の完了記録と区別する
- [ ] T037 `specs/003-resolve-pcb-drc/quickstart.md` の手順を最終版で実行し、結果と未解決事項を `specs/003-resolve-pcb-drc/verification/final-review.md` に記録する

## 依存関係と並行作業

- 基準 T001–T004 → 基礎調査 T005–T009 → Q2復旧 T010–T012。Q2は回路図だけ修正済みのため、PCBとの一致を回復するまで製造データを使わない。
- T006・T007・T008は別ファイルで並行調査できる。T009はT008とMCP同期の調査結果に依存する。
- T017–T019とT024–T025の資料調査を先に行い、T020/T026の共同配置 → T021/T022配線 → T023/T028検証の順に進める。同じPCBまたは記録ファイルへの編集は直列化する。
- 最終配置・配線完了後にT013・T029/T030を実行し、T031/T032/T034/T035で同一版の製造・解析結果を揃える。T033の出力可否調査は他のUS5作業と並行可能。
- US2のT015はQ2復旧後に独立して更新でき、T016は最終検証の結果を待つ。T036/T037は各ストーリーの作業後に実施する。

## ストーリー別の並行例

- US1: T010の回路図照合と、別ファイルに記すT008の資料照合を並行できる。T011/T012/T013は順に実施する。
- US2: T015の変更記録をT017の経路調査と並行できる。最終レビューT016は検証後。
- US3: T017の電流経路とT019の駆動回路は、別記録ファイルへの調査を並行できる。PCB編集T020–T022は直列化する。
- US4: T024のメーカー資料とT006のBOM候補は別ファイルで並行調査できる。共同配置T026はT020と一体で行う。
- US5: T033のIPC出力調査はT029/T030と並行できる。製造データT031/T032は最終設計の検査後に作る。

## 実装戦略

まずPhase 1・2とUS1のQ2修正を行い、DRCと回路図・PCB整合性を回復する。これをMVPとするが、5 A、部品、機構、EMCや製造の完了は意味しない。その後US3・US4の配置と配線を共同で完成させ、再検査した同一版についてUS2・US5と全体整合性を完了する。
