# Tasks: DRC解消後の基板設計の収束

**入力**: [spec.md](spec.md)、[plan.md](plan.md)、[research.md](research.md)、[data-model.md](data-model.md)、[契約](contracts/design-and-verification.md)  
**設計正本**: `hardware/kicad/mini4wd-motor-driver/`。一時ファイルは操作の検証に限り使用し、正本と取り違えない。  
**発注条件**: [verification/order-readiness.md](verification/order-readiness.md) に、発注前に必要な根拠と発注後の実機確認を整理する。  
**現状（2026-11-19）**: 正規38部品版へR107=2.2kΩの入力放電経路、R106=33Ω、C105=22µF/10V、L1の180°回転とSW短縮・局所GND面を反映。全118パッド一致、全チェックERC/DRC・未接続・パリティ0、全品F.Cu、82ビア全裏面テント。電力33個0.8/0.4mmを維持、残り49個0.6/0.3mm。BOM28行すべてMPN/メーカー/資料あり。PCB a7aaab20…5094のGerber/BOM/CPL/IPC/PDFを `verification/prototype-preview-20261119/` に保存。試作前の改善・モデル感度と限界は `verification/return-path-20261119/README.md`。全PVTの入力閾値余裕、MLCC実効最小/閉ループ起動、局所面で未解消の帰路/熱は未保証。業者受入・在庫・見積・パネル/パッド内ビア処理も未確認。実機が必要な測定を発注前の循環条件にしない。追加の1D主経路/216条件の基板熱/324条件の反復ブレーキ、1kHz条件のD1損失と論理/MLCC資料整理は `verification/power-thermal-20261119/`。T017の主要端子照合を完了した。

## Phase 1: Setup

- [x] T001 正規設計と変更前のDRC/ERC結果を `specs/003-resolve-pcb-drc/verification/remaining-work.md` に記録する
- [x] T002 変更前の全チェック有効DRC/ERCを `specs/003-resolve-pcb-drc/verification/drc-all.rpt` と `specs/003-resolve-pcb-drc/verification/erc.rpt` に保存する
- [x] T003 変更前の設計・ライブラリのハッシュ、KiCad版、作業ツリーを `specs/003-resolve-pcb-drc/verification/design-baseline.md` に記録する
- [x] T004 KiCad MCP 2.8.3 のWSL起動方法、使用したMCP操作、依存と再現手順を `specs/003-resolve-pcb-drc/verification/design-baseline.md` に追記し、正規プロジェクトをMCPで開けることを確認する

## Phase 2: Foundational

- [x] T005 元BOMと現回路図の部品を突き合わせ、24部品の記述と基板実装22部品との差、アノテーション警告、Q1/U1の資料URL修正を `specs/003-resolve-pcb-drc/verification/parts-evidence.md` に根拠とともに記録する
- [ ] T006 [P] PCBA対象となる全実装部品のBOMを作り、メーカー・MPNまたは確定仕様・定格・資料・業者調達可否とL1の型番相違を `specs/003-resolve-pcb-drc/verification/bom-selection.md` に記録する。複数調達先の確保は行わない
- [x] T007 [P] 1 oz前提、製造銅厚・ビアめっき、動作波形と許容温度上昇の条件・不足情報を `specs/003-resolve-pcb-drc/verification/current-budget.md` に記録する
- [x] T008 [P] Q2の1–3=S、4=G、5–8=Drainというメーカー端子と現回路図・PCBを照合し、5番の修正途中状態と必要な配線変更を `specs/003-resolve-pcb-drc/verification/q2-repair.md` に記録する
- [x] T009 `specs/003-resolve-pcb-drc/verification/q2-repair.md` に、MCP `sync_schematic_to_board` が `/I2C_SDA`・`/I2C_SCL` の先頭スラッシュを落とす問題と、正規設計に適用する前の局所修正・ネット比較手順を記録する

## Phase 3: US1 基板の違反を解消する（P1）

**目標**: Q2誤接続を除き、機能を保持して全DRCを解消する。  
**独立検証**: 全チェック・銅箔再充填・パリティを有効にしたDRCで違反・未接続・不一致0件。

- [x] T010 [US1] `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sym` と `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sch` のQ2シンボルについて、5番をDrainに変更した既存修正をメーカー端子と図記号の見やすさまで照合する
- [x] T011 [US1] `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` のQ2 pad 5をMOTOR_MINUSに接続し、既存VBAT配線との接触を除去してMOTOR_MINUS側へ再配線する。I²Cなど他ネットは意図せず変更しない
- [x] T012 [US1] Q2 1–3=VBAT、4=GATE_DRIVE、5–8・重複Drainパッド=MOTOR_MINUS、および他の全パッドの対応を `specs/003-resolve-pcb-drc/verification/q2-repair.md` に記録する
- [x] T013 [US1] 再配置・再配線後の正規PCBで全DRCを実行し、`verification/drc-layout.rpt` にエラー・警告・未接続・パリティ不一致0件を記録する。現版の接続検査であり、製造承認ではない。後続のCAD変更後は再検査する

## Phase 4: US2 修正を確認できる（P2）

**目標**: 変更理由、版、検査結果と未確定事項を追跡可能にする。  
**独立検証**: 変更ファイルのハッシュと最終検証記録から結果を再現できる。

- [x] T014 [US2] 基準時の対象、検証済みと残件を `specs/003-resolve-pcb-drc/implementation.md` と `specs/003-resolve-pcb-drc/verification/remaining-work.md` に記録する
- [x] T015 [US2] Q2修正、MCPによる変更、採用した仮定と残る制約を `specs/003-resolve-pcb-drc/implementation.md` と `specs/003-resolve-pcb-drc/verification/remaining-work.md` に更新する
- [x] T016 [US2] 現在の正規試作版の設計・ライブラリ・成果物ハッシュ、実行した検査、結果と未検証事項を `specs/003-resolve-pcb-drc/verification/final-review.md` にまとめる。PCBA受入・実測完了とは区別する

## Phase 5: US3 電源・駆動経路と昇圧部を再設計する（P1）

**目標**: 5 A設計目標の経路と昇圧部の配置・帰路を根拠付きで設計する。  
**独立検証**: 動作モード別の経路、狭窄・ビア・部品定格、昇圧ループとEMC指摘の根拠を確認できる。

- [x] T017 [US3] J1/J2、Q1/Q2、D_FLYのメーカー端子と回路図を照合し、駆動・ブレーキ・還流・検出分岐およびVBAT/MOTOR_PLUSの関係を `specs/003-resolve-pcb-drc/verification/current-budget.md` と `verification/power-thermal-20261119/power-pin-audit.json` に記録する。現版5部品の全端子一致、D1帯側=VBATを確認。実波形/定格の評価とは区別する
- [ ] T018 [US3] 主経路の幅・銅厚・狭窄・層・実際に並列分担するビア・めっき・温度前提を `specs/003-resolve-pcb-drc/verification/current-budget.md` に示し、5 A目標を評価する。1D銅抵抗と放熱境界の定量感度は `verification/power-thermal-20261119/` に保存済み。実製造条件・面接触部の分担・5A成立は未確定
- [ ] T019 [US3] Q1/Q2の駆動について、電池電圧範囲、電源投入・切断、PWM切替時の各ゲート電圧、MOSFET過渡電圧、同時導通、駆動能力と損失を評価し、必要な回路変更を正規回路図へ反映する。電源順序・モデルや保証値の範囲・未検証条件と再現可能な結果を `specs/003-resolve-pcb-drc/verification/drive-review.md` 等へ記録する
- [ ] T038 [US3] 代表的な市販モーター（標準・高負荷など）を選び、NiMH・アルカリ各条件で起動・連続・短時間拘束・ブレーキの電流／時間包絡を試作前に利用可能な資料・仮定・計算で整理し、実測が必要な項目と試作後の測定手順を記録する。全型番の網羅保証とは区別し、5 A連続目標をピーク上限とみなさない
- [ ] T039 [US3] T038の負荷包絡に対し、サーキット走行での数秒〜数十秒のブレーキと繰返しを含む電池・MOSFET・ダイオード・コネクタ・配線の過渡／熱定格と、趣味用途に見合う保護・安全な試運転方法を決め、必要な回路変更を正規設計に反映して確認する。解析する時間・繰返し・波形は仮定を記録し、範囲外や故障時の動作、未評価のモーターを明記する
- [ ] T020 [US3] J1/J2とU2/L1/CIN/COUT/U1を共同で再配置し、メーカー推奨ループ・帰路を `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` と `specs/003-resolve-pcb-drc/verification/layout-decisions.md` に反映する
- [x] T021 [US3] 主電流経路を1.5～2.0 mm幅で再配線し、端子の狭窄と層間遷移を正規PCB、`verification/layout-power-routing.csv` と `verification/current-budget.md` に反映する。5 A適合の評価はT018に残す
- [ ] T022 [US3] SW_BOOST、FB_BOOST、GATE_DRIVEおよび検出信号を再配線し、ループ・帰路・分離の根拠を `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` と `specs/003-resolve-pcb-drc/verification/layout-decisions.md` に記録する
- [x] T023 [US3] 最新設計でEMC解析を再実行し、各指摘の対応・誤検出・未測定を `specs/003-resolve-pcb-drc/verification/emc-review.md` に記録する

## Phase 6: US4 部品と機構を整合させる（P1）

**目標**: 部品資料、基板形状と両端コネクタを一致させる。  
**独立検証**: 全品の端子・ランド・MPNとコネクタ位置・向きをメーカー資料と比較できる。

- [ ] T024 [US4] Molex 43650-0214、XIAO MG24 Sense、L1、Q1/Q2、U1/U2を含む全PCBA対象品について、端子・パッケージ・定格・業者の調達または支給部品対応を `specs/003-resolve-pcb-drc/verification/parts-evidence.md` に記録する
- [ ] T025 [US4] `hardware/kicad/mini4wd-motor-driver/board-routed.pretty/` の全フットプリントについて、特にXIAO、Molex、L1、Q1/Q2のランド・マスク・Courtyard・端子を図面または現物と比較し、必要数のSMT実装を依頼する業者の工程・支給条件に適合するか確認する。電池に向くB.Cu面に部品がないことを確認する
- [x] T040 [US4] 既存の搭載例、正規基板の外形・実装面、主要部品と嵌合コネクタの寸法を基に、電池上への搭載が一般的に現実的かを評価し、懸念と限界を `specs/003-resolve-pcb-drc/verification/chassis-clearance.md` に記録する。FM-A/SFM等のフロントモーターシャーシは対象外。各車種・カウルの適合保証や実測を完了条件としない
- [x] T026 [US4] T020の共同配置でJ1/J2を反対端・外向きとし、基板端・嵌合・保持タブ・禁止銅の条件を `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb` と `specs/003-resolve-pcb-drc/verification/layout-decisions.md` に反映する。2026-11-17のメーカー2D図面照合・pin1正極維持・固定ランド修正は `verification/pcba-bom-stage/mechanical-findings.md`
- [ ] T027 [US4] 照合済みメーカー・MPNを `hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sch` に反映し、調達・実装可否を `specs/003-resolve-pcb-drc/verification/bom-selection.md` に記録する
- [x] T028 [US4] 正規PCBで55 × 21 mm、1.6 mm厚、2銅層、38部品全F.Cuと全82ビア裏面テントを確認し、`verification/return-path-20261119/connectivity.json` と `verification/final-review.md` に記録する。電力ビア33個は0.8/0.4 mm、その他49個は0.6/0.3 mm。パッド内ビアの工程受入は残る

## Phase 7: US5 検証して製造用データを整える（P2）

**目標**: 同じ最終設計版から検証済み製造データを整える。  
**独立検証**: 全ERC/DRC・ネット照合とGerber・穴・BOM・CPLの一致を再現できる。

- [x] T029 [US5] 正規回路図・PCBの全チェック有効ERC/DRC/パリティを最終変更後に再実行し、`verification/return-path-20261119/erc.rpt` と `verification/return-path-20261119/drc.rpt` に違反・未接続・不一致0件、除外なしを記録する。以後のCAD変更後には再実行する
- [ ] T030 [US5] 最終回路図ネットリストとPCB全パッドをメーカー端子と照合し、Q2の根拠ある変更とI²C名を含む差分を `specs/003-resolve-pcb-drc/verification/final-review.md` に記録する
- [ ] T031 [US5] 同一最終版から `hardware/kicad/mini4wd-motor-driver/manufacturing/gerber/` にGerber・Excellonを生成し、ビューアで層・穴・外形・底面マスクを照合する
- [ ] T032 [US5] PCBA対象全品を含むBOMとCPLを同一の最終設計版から出力し、座標・回転・部品番号・業者の調達/支給方法とGerber・ドリルの版一致を照合する
- [x] T033 [P] [US5] 既存FR-011のIPC-D-356要求と出力可否を調査し、必要な `hardware/kicad/mini4wd-motor-driver/manufacturing/mini4wd-motor-driver.ipc` または未解決理由を `specs/003-resolve-pcb-drc/verification/ipc-d356.md` に記録する
- [ ] T034 [US5] 同一版で回路図・PCB・相互照合・適用可能な熱/SPICE・Gerber確認を行い、適用範囲・実行しない認証相当の試験・誤検出を `specs/003-resolve-pcb-drc/verification/final-review.md` に記録する
- [ ] T035 [US5] 選定した基板/SMT業者の試作向けファイル・DFM確認、必要枚数での見積・部品調達/実装数、EMC設計上の注意、電流・部品の限界、未実施の実機試験、成果物ハッシュを `specs/003-resolve-pcb-drc/verification/final-review.md` に記録する。試験所のEMC適合試験・量産検証は要求しない

## Phase 8: 全体の整合性

- [ ] T036 `specs/002-port-to-kicad/progress-summary.md` と `specs/003-resolve-pcb-drc/implementation.md` を最終版の根拠に更新し、過去の完了記録と区別する
- [ ] T037 `specs/003-resolve-pcb-drc/quickstart.md` の手順を最終版で実行し、結果と未解決事項を `specs/003-resolve-pcb-drc/verification/final-review.md` に記録する

## 依存関係と並行作業

- 基準 T001–T004 → 基礎調査 T005–T009 → Q2復旧 T010–T012。Q2の回路図・PCB整合性は回復済み。以後の設計変更後に再検査し、残課題が完了するまで途中版の製造データを使わない。
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

## 2026-11-17の完了部分と残り

- T006/T027の属性補完は完了: 全29 BOM行にメーカー・MPN・資料、L1完全型番を反映。実効容量/定格の残確認と業者調達・全品実装受入があるため、タスク全体は未完了のまま。
- T018の電力ビア比較は旧35品版25、37品途中候補9、最終33を区別。全33個の表裏配線中心接続と3/6並列の形状、抵抗の仮定計算を記録済み。温度・実分流・5 A連続実証は完了扱いにしない。
- T030の全116パッドの回路図ネット対応は合格。メーカー端子/部品全体の確認範囲は `verification/final-review.md` の記載に限定する。
- T031の同一版生成・Gerber/ドリル/裏面マスクの描画確認は `verification/prototype-preview-20261118/` で完了。既存製造データは上書きせず、業者受入後の発注用データへの昇格は残る。
- T032のBOM29行/37部品とCPL37個を同一版で出力し、位置/回転/実装面と元CADを照合済み。業者ライブラリに対する原点・回転・調達受入は未確認。
- T034は回路図/PCB/相互/Gerber解析と誤検出整理を実施。今回変更後の熱/SPICE/EMC再解析、全IC資料再抽出・3D高さ・実測は未実施。試作後測定を発注前条件へ循環させない。

## 2026-11-18の電源余裕是正

- 正規R1=75kΩ/R2=10kΩ、各0.1%/25ppmへ変更。部品数/面積/配線/ネット/proを保全し、ERC/DRC/未接続/パリティ0・全116パッド一致、BOM29行/CPL37/新Gerber/IPCを再生成した。根拠は `verification/preorder-electrical-20261118/README.md` と `verification/prototype-preview-20261118/`。
- T019: TPS61023基準580mVの下限計算を訂正、受動PDN96ケースと新供給上下限のGate/VDS典型モデル8ケースを実行。7ケース閾値重なり0、1.8nF追加Q1感度/低供給5V喪失は2nsの重なり指標。モデル/実効容量/全温度リーク/実電源の限界が残るためT019全体は完了扱いにしない。
- T023: 現版の全23指摘を `verification/emc-review.md` に分類済み。GND/昇圧/Gate帰路の実リスクはT020/T022へ残し、差動対2件のみ誤検出とする。
- T034: 熱analyzer実行はSKIPPED（0部品評価）、LCSC lifecycleは26品全unknown。指摘0を合格へ変えず、先行の熱感度と組立後測定計画を維持する。試作前に取得できない実測を発注前完了に要求しない。
