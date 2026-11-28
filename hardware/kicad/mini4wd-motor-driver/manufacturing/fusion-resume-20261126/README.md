# 004再開・3D復元記録とFusion準備状況

2026-11-26。ユーザー指示で006を一旦停止し、Seeed Studio Fusionの実装を前提に004へ戻した。

## 正規版と復元したデータ

- 正規版: `../../mini4wd-motor-driver.kicad_pro`。55×21 mm、厚1.6 mm、2層、22フットプリント。
- ブランチ移動前の38フットプリント版: `../../candidates/pre-switch-ecad-20261126/`。元の対応回路図・pro・ローカルライブラリも一式保存した別候補。004正規版の回路図と混ぜない。
- 元のSTEP2点は `../../3dmodels/` に復元した。Zone.Identifierは含めていない。
- 正規版のMCU1・J1・J2と、そのローカルフットプリントへ3D参照だけ追加。モデル要素を除いたS式を変更前後で比較し全一致した。ネット・パッド・配線・外形・ルールは変えていない。回路図・proは未変更。
- 既存のロックは削除していない。KiCadを既に開いていた場合は、古い画面から保存せずファイルを開き直す。

## 3Dの開き方

正規版の `mini4wd-motor-driver.kicad_pro` を開き、PCBエディターから **表示 → 3Dビューアー（Alt+3）** を開く。プロジェクトフォルダーと `3dmodels` を一緒に保つ。KiCadの標準3Dモデルライブラリも必要。

この実行環境では `pcbnew --help` も `Unable to initialize GTK+, is DISPLAY set properly?` で終了したためGUI操作はできなかった。KiCad CLIの3D描画は成功し、XIAOと2個のMolexコネクターの配置・向きを上面画像で確認した。コネクターは004の既存どおり両方が右向き。3D復元による配置移動はしていない。

- [004上面・USB修正後](004-3d-usb-out-final.png)
- [004上面・修正前の記録](004-3d-top.png)
- [004斜視](004-3d-perspective.png)
- [移動前ECAD上面・USB左向き修正後](pre-switch-3d-usb-left.png)
- [移動前ECAD上面・修正前の記録](pre-switch-3d-top.png)

`model-audit.json` にファイル参照の有無を保存した。復元直後は004の既存U2・Q1・Q2の標準STEP3点が見つからず、L1はモデル未設定だった。U2は後述の標準モデルへ変更済み。保存候補はQ1が欠落、L1が未設定。供給されたXIAO STEPはMG24モデルで、Sense下面部品の細部・機構クリアランスの認定には使っていない。画像上のモデル表示と製造ランドの適合は別の確認事項。

## 実施したチェック

KiCad 10.0.8。正規版でERC 0件、3D追加後の全項目DRC 0件・未接続0件・schematic parity 0件。保存候補も対応する回路図でERC 0件・DRC 0件・未接続0件・parity 0件。JSONを本ディレクトリへ保存した。

これは3Dデータ復元と既存接続の確認であり、全面的な電気設計再審査ではない。熱、EMC、SPICE、ライフサイクル、製造元DFMを今回新規には実施していない。旧Gerberは今回の3D復元に伴い再生成していない。

## Fusion依頼に向けて残る作業

Seeed FusionはGerberとMPN/Seeed SKU付きBOMを使って部品調達・SMT/手実装に対応する。[公式PCBA仕様](https://support.seeed.cc/portal/en/kb/articles/fusion-pcba-specification)・[公式依頼手順](https://support.seeed.cc/portal/en/kb/articles/how-do-i-place-a-seeed-fusion-pcb-assembly-pcba-order)

004のBOMを現回路図から再調査した結果は22部品/18行、MPN属性は全行空欄。旧 `hardware/rev1/manufacturing/bom.csv` は候補型番の根拠として残るが、L1は現Coilcraftランド/値と旧Würth候補が異なる。XIAO MG24 SenseのSeeed SKU、全品MPN、ランド・向き・供給を確認してからFusion用BOMを確定する。

大電流経路、共有ゲートの切替/電源順序、J1/J2の同一端配置、昇圧スイッチングループ、実装ランドのメーカー照合は `specs/003-resolve-pcb-drc/verification/remaining-work.md` の未完了事項。Fusionに依頼することだけでこれらは解消しない。依頼用の最新Gerber/BOM/CPLは設計対象版が決まった後、同一版から生成する。外部アップロード・見積依頼・発注は実施していない。

## XIAOのUSB方向の修正

メーカーの[公式上面端子図](https://files.seeedstudio.com/wiki/XIAO_MG24/Getting_Start/XIAO_MG24_Sense_front_pinout.png)で、USBと同じ端に5V/VBUSとD0があることを目視した。004のローカル番号ではpad1=5V、pad14=D0であり、両方がフットプリント左端にある。したがって現ランドはUSB左向きを示しており、復元したSTEPの表示方向が180度逆だった。

004正規版と38部品保存候補、および各board-routedライブラリのXIAOモデルだけを修正した。回転を(-90,0,180)度、オフセットを(1.8,5.3,0)mmとし、モデル以外のS式は全一致。正規版の3DではUSBが左端の外へ向くことを確認した。保存候補はXIAOが内側にあるため、修正したUSBがJ1と重なる機構問題が見える。保存候補の機構は未合格であり、電気配置を回転変更してはいない。

## 未表示モデルと入手先

| Ref | 004の値/候補MPN | Footprint | 状況・メーカー入手先 |
|---|---|---|---|
| U2 | TPS61023DRLR | Package_TO_SOT_SMD:Texas_R-PDSO-N6_DRL-6 | 欠落した固有名STEPの代わりに標準SOT-563.stepを外観用に参照。TI製品説明の1.2×1.6mm SOT563と標準ライブラリの端子順一致を確認。メーカー固有モデルは[TI CAD/3D](https://www.ti.com/product/TPS61023)から。 |
| Q1 | SiSS64DN-T1-GE3 | Package_SO:Vishay_PowerPAK_1212-8_Single | STEP欠落。[Vishay製品ページ](https://www.vishay.com/en/product/67294/)のECAD Models→Ultra Librarian。 |
| Q2 | SI7137DP-T1-GE3 | board-routed:PowerPAK_SO-8_SI7137DP | STEP欠落。[Vishay製品ページ](https://www.vishay.com/en/product/69063/)のECAD Models→Ultra Librarian。 |
| L1 | 1.0uH 9A (XEL4030-102ME) | board-routed:Coilcraft_XEL4030 | 元からモデルなし。末尾発注型番未確定。[Coilcraft XEL4030](https://www.coilcraft.com/en-us/products/power/high-voltage-inductors/xel/xel4030/)の3D Models/Resourcesから。 |

U2の参照変更は両PCBのモデルパスだけで、ランド・配線は変更していない。Q1/Q2の名前が存在しないからといって、別パッケージの形を代用していない。メーカーリンクの確認は行ったが、Q1/Q2/L1の実ファイル取得と位置合わせは未実施。

USB方向とU2モデル修正後も、両PCBの全項目DRC・未接続・schematic parityは0件（drc-final-3d.json / preserved-drc-final-3d.json）。回路図は変更しておらず、先のERC0件の入力と同一。

## Q2モデル追加（同日更新）

Q2には公式KiCadのPowerPAK SO-8パッケージSTEPをダウンロードして追加した。[モデル照合・検査と最新画像](q2-model/README.md)を参照。上記のQ2欠落記録は追加前の状態である。

## Q1・L1のモデル追加（同日更新）

残るQ1には寸法照合した公開パッケージモデル、L1にはメーカー最大寸法に基づく明示的な概形モデルを追加した。[22部品の表示確認・最新画像と限界](q1-l1-models/README.md)を参照。過去のQ1/L1モデル未設定記録は追加前の状態である。
