# 正規試作設計の検証記録（2026-11-19）

正規対象は `hardware/kicad/mini4wd-motor-driver/`。PCB SHA-256 **a7aaab20cce23e1311411c16d31d7868e5d10233389f3a2941676cce5c175094**。38部品全F.Cu、55×21×1.6mm/2層、82ビア全裏面テント。33個の電力ビアとJ1/J2の端子・位置・ネット、既存電力バスを維持した。`.kicad_pro`はb45ff3ff…99f2で変更なし。

- 正規全チェック[ERC](return-path-20261119/erc.rpt)/[DRC](return-path-20261119/drc.rpt)、未接続・回路図パリティは全て0、Ignored checks None。[118パッド照合](return-path-20261119/connectivity.json)は不一致0。
- R107=2.2kΩ追加、R106=33Ω、C105=22µF10V、L1の同中心180°回転、SW短縮と局所GND面を反映。[差分監査](return-path-20261119/geometry-delta.json)、[根拠と限界](return-path-20261119/README.md)。R107は従来の楽観的ENA喪失順序を外した電荷保持感度への対策である。
- [同一版製造プレビュー](prototype-preview-20261119/)にGerber8層/Excellon/IPC/BOM28行38品/CPL38行/PDF、実Gerberの上下銅箔・穴・外形SVG/PNGを保存。Gerber指摘0、B.Mask描画オブジェクト0。[出力対CAD](return-path-20261119/output-correspondence.json)の値・MPN・メーカー・位置・回転・側の不一致0。入力20ファイル/成果物のハッシュを保存した。
- 回路図/PCB/cross/cross-verify、受動SPICE、EMC、熱、Gerber解析を実行。受動SPICE6pass/3info、EMC40指摘は[全分類と限界](return-path-20261119/README.md)/[EMC処置](emc-review.md)、熱は定量入力不足でSKIPPED。EMC指摘0や5A熱合格とはしない。構造化datasheet全品再抽出・lifecycle再照会は今回省略し、主要部品は引用一次資料と生CADで照合。前回lifecycle全unknownは在庫/現役品の証拠ではない。

- 追加で[5A主経路/PWM/熱の定量予算](power-thermal-20261119/README.md)を実施。実配線1D抵抗網7経路、基板放熱216条件、反復ブレーキ324条件を保存。35µm/20°Cの駆動銅損は5Aで約0.766W。1kHz/5A一定のD1予算60.5mWに対し20kHzでは1.21Wとなるため、20kHzを基板全体の認定条件としない。[公式core調査](pwm-core-research.md)の1kHzを条件付き代表とし、core版/ビルドと実キャリアは未確定。熱analyzerのSKIPPEDと、別途実行した境界条件付きの手計算/数値評価を区別する。
- [論理/C105の追加一次資料整理](power-thermal-20261119/logic-capacitor-review.md)で、UCCの起動4.65V、停止4.4V、推奨4.5Vを区別。C105実効2µFの既存感度は最小4.588Vで推奨下限を上回る。Murata当該品のReference Sheetは初期/温度特性が無バイアス試験であり、DC下の実効最小保証にはならない。全PVTや起動/安定性へ結論を拡張しない。

C105の全温度/バイアス/経年の実効最小、TPS閉ループ安定性/起動、5V時の全PVT入力閾値と電圧低下中の論理、残る高周波帰路、実波形・温度/EMC/無線は未保証。机上の代表条件改善と全PVT認定を区別する。組立後にしかできない測定を試作発注前の循環要件にしない。初回は電流制限し、BOOST/XIAO入力5.5V超、Gate/VDS定格超、UVLO反復や不意な駆動があれば中止/改版する。

PCBA業者の全38品供給/SMT受入、XIAO castellated module、Q1ドレイン6個のパッド内ビア平坦化、銅厚/めっき、パネル/支持/fiducial/デパネル、CPLライブラリ補正、枚数と見積は未確認。外部への送信・発注は行っていない。[現在の発注条件](order-readiness.md)。

## 2026-11-18の検証履歴（旧版）

以下の37部品・75ビア・e7152f9…という数値と解析は前回の版に対応し、現版の検査結果へ読み替えない。


**正規対象は `hardware/kicad/mini4wd-motor-driver/`。** PCB SHA-256は `e7152f915355a188716b45264bc74a34fdb6dc9e5e9074a5caea470124906ac7`。本書は現在の試作検討版のCAD・出力検査であり、業者DFM受入、5 A連続実証、全モーター適合や実機測定の完了を宣言しない。

## 結果と出力

| 項目 | 実施結果 / 根拠 |
|---|---|
| ERC | 全severity・除外も報告して0件。[レポート](preorder-electrical-20261118/erc.rpt) |
| DRC・未接続・回路図パリティ | 全チェック・全配線エラー・銅箔再充填で全て0件、Ignored checks None。[レポート](prototype-preview-20261118/drc.rpt) |
| 新規XMLと全PCBパッド | 116パッド、不一致0、37部品全F.Cu。[照合](preorder-electrical-20261118/connectivity.json) |
| 基板 | 55×21 mm、1.6 mm、銅2層、75ビア全裏面テント |
| BOM | 29行/37部品、MPN・メーカー・資料URL全行あり。調達在庫・業者受入は別。[解析](preorder-electrical-20261118/bom-analysis.json) |
| CPL | 全37個、基板内の位置/回転/側を元CADと機械照合。業者の原点・ライブラリ回転補正は未確認。[出力](prototype-preview-20261118/cpl-front.csv) |
| Gerber・Excellon | F/B.Cu、F/B.Mask、F/B.Silk、F.Paste、Edge.Cuts、ドリルを同一版から生成。[ZIP](prototype-preview-20261118/mini4wd-prototype-20261118-preview.zip) |
| Gerber解析・可視確認 | analyzerは指摘0。Gerbonaraで実Gerberの上下銅箔・ドリル・外形を描画して照合、B.Mask描画オブジェクト0で裏面開口なし。業者CAM/DFMの代替ではない |
| IPC-D-356A | 同一正規PCBから出力。[IPC](prototype-preview-20261118/mini4wd-prototype.ipc) |
| 版追跡 | 主/階層回路図、PCB/pro、ローカルsymbol/footprint・lib-tableの20ファイルをハッシュ固定。[入力](prototype-preview-20261118/source-sha256.txt) / [成果物](prototype-preview-20261118/artifact-sha256.txt) |

`.kicad_pro` は変更前後とも `b45ff3ffb2cd60255fbebd5003f734b688c7f039a4a8e7bfefa4b957977899f2`。MCP Save As前に同じ設定を候補へ複製し、正規への保存後も確認した。規則緩和や違反除外は行っていない。旧製造データを上書きせず、新しい確認用プレビューへ保存した。

## 設計の差分

- 2026-11-18: 昇圧分圧をR1=75kΩ/R2=10kΩ、各0.1%/25ppmへ変更（Yageo RT0603BRD0775KL / RT0603BRD0710KL）。従来の下限4.782V/余裕132mVはPWM基準電圧の誤算であり、使用しない。新案は抵抗温度感度と25°Cリーク感度で約4.904～5.213V。XIAOの5V端子が内蔵D1後段VINであることと、VINのTPS628438推奨上限5.5Vを一次図面で照合した。[詳細・仮定・限界](preorder-electrical-20261118/README.md)。2個の値/4属性以外のPCB/回路図S式、全配線・ネット・配置・階層回路図とproを保全した。

- Molex 43650-0214の固定ランド・端子1の向きの不一致をメーカー図面に合わせて修正。pin1正極とケーブル互換を維持して引き直し、両端外向きを保持した。全体の本体投影長は約62.04 mmで、55 mmは基板本体寸法。[機械照合](pcba-bom-stage/mechanical-findings.md)。
- XIAO MG24 Sense（ヘッダなし、102010610）の14端子を公式ランド寸法2.0×2.75 mmへ拡大。USB左向きの機能対応と独自番号を維持。モジュール投影内のビアは表裏テント。
- 未記入19 BOM行へメーカー・MPN・資料を反映。L1は完全型番XEL4030-102MEC、R101は499kΩ/0.1%候補RT0603BRD07499KLとした。[候補と根拠](pcba-bom-stage/README.md)。公称容量だけでMLCC実効容量を保証しない。
- 電力ビア0.8/0.4 mmは旧35部品検証版25個、37部品途中候補9個、最終37部品版33個と版を区別。残る42個は0.6/0.3、最小環幅0.15 mm。[比較・電流経路](pcba-bom-stage/power-via-review.md)。Q2 MOTORのF.Cu1.4 mm、J2 MOTORのF.Cu1.5 mmバスを補強し、33個全ての中心がF.Cu/B.Cuの同ネット配線に接続することを確認した。

## 実施した解析と指摘の扱い

実行したのはKiCad CLI ERC/DRC/XML/CPL/IPC/Gerber、`audit_connectivity.py`、kicad skillの `analyze_schematic.py`、`analyze_pcb.py --full --schematic`、`cross_analysis.py`、`cross_verify.py`、`analyze_gerbers.py`、bom skillの再帰BOM解析・CSV出力。今回も同じ解析を再実行し、JSONは [preorder-electrical-20261118/](preorder-electrical-20261118/) に保存。前回ランド/ビアの形状根拠は [pcba-bom-stage/](pcba-bom-stage/) を参照。

- schematic analyzer: 20件（error2/info18）。N_COMMAND/P_COMMANDの5 V→3.3 Vという指摘は方向の誤認。実際は3.3 Vロジック出力→UCC27524AのTTL互換入力。既存のメーカー閾値照合と回路図のI/O方向を根拠に追加レベル変換は不要とした。
- PCB analyzer: 34件（error4/warning15/info15）。J1/J2のcourtyard張り出しは外向きコネクタの意図した形状。全銅パッドは端クリアランスに合格。Q1の端から約0.42 mm、fiducialなしは業者のパネル/キャリア設計条件として残す。近端部品の1 mm推奨値は本プロジェクトのDRC値とは別。
- 狭いMOTOR_MINUS 0.15 mmはR5の検出枝であり5 A主経路ではない。GATE_P/DRIVE_ENABLE/N_COMMANDの0.127 mm区間は小電流/ゲート配線で、主電流経路には使わない。ゲートの実波形は未測定。
- cross verifyのGATE_P/GATE_N差動ペア不一致は命名による誤検出。2本はMOSFET用の独立ゲート出力で、差動信号ではない。
- cross analysisのBOOST_5V 0.5 Aは出力容量からの推定で実負荷値ではない。0.15 mm枝を含む5 V配線の電圧降下/起動余裕は、既存の負荷予算・修正後の静的/受動過渡感度と合わせ、動的確認を残す。
- MCU_3V3の「5 ICに4 capacitor」はXIAO自身を含む個数推定。外付け4 ICにはC101/C102/C103/C106があり、XIAOには搭載済み部品がある。Q2直下熱ビア0は実形状の情報として保持し、一般的な推奨本数だけで温度合格とはしない。
- GerbonaraはKiCad ExcellonのG90記載位置とRoundRectマクロ余剰引数に構文警告を出したが、描画は完了した。B.Pasteなしは片面実装のため正常。

## 電気・熱・EMCの今回の評価

- [受動PDN 96ケース](preorder-electrical-20261118/pdn-results.json): 新案の代表Gate電荷80/100nC全16条件はU104供給4.779V以上。300/300nC予算はC105実効1µF以上なら4.698V以上。ただしC105実効容量とFBリーク全温度上限は保証値ではない。TPS61023制御/起動の閉ループ合格とは区別する。
- [実MOSFET/Driver典型モデル](preorder-electrical-20261118/driver-results.json): 新供給下限/上限と仮定電源順序の8代表ケース完走。閾値重なり7件0、低供給・Q1追加1.8nF感度の5V喪失1件は2ns（解析刻み2ns）。VGS/VDSは使用条件で各絶対最大内だが、全PVT・実電源・SOAの認定ではない。
- [受動SPICE](preorder-electrical-20261118/passive-spice-final.json): 9件、6pass/3info、warn/fail/skip0。理想分圧等の計算照合であり、実コンバータ性能の保証ではない。
- [EMC](emc-review.md): 23件全件を分類。GATE_P/Nの差動対指摘2件は誤検出。GNDプレーンなし、昇圧/Gate帰路は実在する設計リスクとして保持。52/100を認証適合結果としない。
- [熱analyzer](preorder-electrical-20261118/thermal.json): 実行したが0部品評価でSKIPPED。U2 below_min_pdiss、MOSFETの損失/熱モデルを自動評価できていない。先行の手計算/単発・繰返し熱感度と段階試験を適用し、5A連続を合格としない。
- [Lifecycle](preorder-electrical-20261118/lifecycle.json): LCSC-onlyの26品照会は全unknown。このソースのstatus未提供による限界で、現役品/在庫確認の代わりにしない。

## 発注前に残るもの

1. 37部品全品の供給・調達/支給、特にXIAO castellated module、LT/ADI品、コネクタを含む一括実装の業者受入と必要枚数での見積。現在在庫や価格は未確定。
2. Q1ドレイン6個のパッド内ビアの穴埋め/キャップ・平坦性/はんだ吸い込み、最小めっき厚・銅厚、裏面テントを工程仕様として確認する。テントだけで穴埋め済みとしない。
3. パネル枠fiducial、工具穴/支持、コネクタ張り出しと端付近部品を避けるデパネル方法、CPLのメーカーライブラリに対する原点・回転。業者のパネル処理へ依頼する条件であり、架空の受入回答を記録しない。
4. 選定MLCCの実効容量・TPS閉ループ過渡/起動・全温度リークは未保証。GND/昇圧/Gate帰路の改善余地と5A連続の熱目標は残る。今回の分圧修正と受動/典型モデル感度は試作を進める机上根拠であり、無条件の動作認定とはしない。初回測定と不合格時の改版条件を定め、実機が必要な測定を発注前の循環要件にしない。

## 未実施 / レビュー範囲

今回、上記の熱/SPICE/EMC・Lifecycleを再実行した。熱はSKIPPED、Lifecycleはunknownである。未実施は全ICデータシートの構造化再抽出、3D積層高さ、実電流分担、起動停止/PWMのGate/VDS実波形、部品温度・NTC追従、実車取付の実測、試験所のEMC測定。先行モデルの85°C PWM収束失敗や、UCCモデルがA品/SOICの保証モデルでないことも未解決のまま残す。新しい代表条件と限界は [電気再評価](preorder-electrical-20261118/README.md)、既存の受入手順は [代表条件](prototype-design-release.md) を参照。

試作後でなければ取得できない波形・温度は、試作前完了を要求しない。試作前には試験手順・測定対象・動作限界・未評価範囲を定め、組立後に電流制限した初回通電と段階評価を実施する。**CADと同一版の確認用出力は揃ったが、PCBA業者の発注受入は未確認。**
