# DMP2008UFG-7 候補の配置・配線検証

**2026-11-18訂正・後続版:** 本書の4.782V/132mVはTPS61023基準電圧の誤算に基づく旧値で、現在の設計根拠にしない。R1/R2の精度/比率変更、新版の供給・過渡感度と限界は [電気再評価](preorder-electrical-20261118/README.md)、正規版検査は [最終レビュー](final-review.md) を参照。本書の旧CAD/モデル実行結果は履歴として保持する。

後続の [趣味用試作版の正規反映](prototype-design-release.md) でDMP2008UFG-7とGate抵抗を正規CADへ反映した。以下は候補段階の検証履歴であり、現在の正規採用状態や試作発注の条件は後続報告を参照する。

2026-11-15。Q2低電圧レビューに続き、DMP2008UFG-7を実装する候補設計を作成した。**正規設計への採用と製造承認は未実施**。正規設計の回路・PCB・設定・ライブラリを本段階で変更していないことを [hashes-candidate.json](q2-low-voltage/hashes-candidate.json) に記録した。

## 保存した候補と検査結果

候補は [candidate-design/](q2-low-voltage/candidate-design/README.md)。`hardware/kicad/mini4wd-motor-driver/` が正規設計であり、この検証コピーを発注に使わない。

| 実行した検査 | 結果・証拠 |
|---|---|
| KiCad 10.0.8 ERC、全severity・除外も報告 | 0 errors / 0 warnings。[ERC](q2-low-voltage/erc-candidate.rpt) |
| DRC、schematic-parity、refill-zones、全severity | DRC 0、未接続0、parity 0、除外なし。[DRC](q2-low-voltage/drc-candidate.rpt) |
| 新規XMLネットリストとPCBの全パッド照合 | 112パッド、不一致0。[照合記録](q2-low-voltage/connectivity-candidate.json) |
| 寸法・実装面・ビア | 55×21 mm、1.6 mm、銅2層、35部品全F.Cu。66ビア全て裏面テント |
| 候補PCB SHA-256 | `f7d738b7c00b5d24683ac951cf491587810533d4af88cd059d39d8c3f93e6b4f` |
| 正規／候補のプロジェクト設定SHA-256 | `b45ff3ffb2cd60255fbebd5003f734b688c7f039a4a8e7bfefa4b957977899f2` |

Q2は旧中心座標を維持してPowerDI3333-8に交換し、Sourceを3本の0.42 mm分岐、Drainを1.5 mm経路で接続した。Gateは既存経路を維持して端子へ延長した。干渉していた小電流VBAT昇圧分岐をB.Cuへ移し、0.6/0.3 mmのテント指定ビアを1個追加した。裏面部品は追加していない。最初のGate短縮案はDRC違反があったため採用せず、[第1回検査](q2-low-voltage/drc-iteration1.rpt)も残した。

MCPで実体フットプリント交換・配線を行い、補助的にpcbnewで候補の属性同期・ビアテント指定を行った。[交換ログ](q2-low-voltage/mcp-swap.log)、[配線ログ](q2-low-voltage/mcp-route.log)、[属性同期](q2-low-voltage/metadata-sync.json)を保存した。各保存前後で設定を照合し、今回の操作では設定上書きは発生していない。上記DRC合格は電流容量・熱・発注可否の合格を意味しない。

## 端子とランド

[DMP2008UFG資料 pp.1,5](https://www.diodes.com/datasheet/download/DMP2008UFG.pdf)と[メーカーの2022-04-29版パッケージ資料 p.1](https://www.diodes.com/assets/Package-Files/PowerDI3333-8.pdf)を照合した。端子1/2/3=Source、4=Gate、5/6/7/8=Drain。メーカー図の回転とTop/Bottom viewを区別し、候補の上側左を1番とするパターンに対応させた。

KiCad標準 `Diodes_PowerDI3333-8` の銅箔・マスク・ペースト・3D形状を維持した。0.65 mmピッチ、0.70×0.42 mm端子ランド、端子全幅3.70 mm、Drain幅2.37 mm・奥行2.25 mmを照合した。標準の共通5番ランド内に6/7/8番の**F.Cuのみ**の識別パッドを置いた。追加矩形は既存Drain銅箔の内部に完全に含まれ、銅箔の和集合・F.Mask・F.Paste開口は変わらない。[構造比較と包含検査](q2-low-voltage/land-audit.json)を保存した。二重のペースト開口や追加の露出ランドを作る変更ではない。

シンボルを共通5番だけに集約する案も検討したが、物理端子1～8との明示対応を保つ上記の方法を選んだ。現シンボルの機能・端子配置を利用し、Value/MPN/Descriptionを候補部品へ更新している。最終的なステンシル・リフロー・供給部品の受入はPCBA業者の確認事項。手はんだによる代替は想定しない。

## 電気条件と定量評価

[再実行可能な計算](q2-low-voltage/evaluate_bounds.py)と[数値結果](q2-low-voltage/bounds.json)を追加した。32 DC／6過渡ケースの既存SPICE結果は [低電圧レビュー](q2-low-voltage-review.md)と[results.json](q2-low-voltage/results.json)を参照する。典型モデル・仮定したモーターとドライバを使う解析であり、全モーターの保証ではない。

- VBAT=1.8 V以上でVGS≤−1.5 Vを使うには、OUTB LOWと基準GND差の合計が0.30 V以下であることが必要。DMP候補の25°C最大17 mΩから5 Aの単純導通損失は0.425 W。
- VBAT=0～3.4 V、OUTB=0～5.208 Vの静的組合せではVGS=−3.4～+5.208 Vとなり±8 V定格内。これは過渡ピーク・逆接・回生の証明ではない。
- **UCC27524ADRはSOICのDパッケージ**。[TI資料 pp.5–7](https://www.ti.com/lit/ds/symlink/ucc27524a.pdf)のUVLO立上り最大は−40～140°Cで4.65 V。DGN用4.4 Vを流用しない。昇圧出力の静的公差下限4.782 Vとの差は約132 mV。リップル、起動、負荷ドロップを含めた起動余裕は未証明。
- 熱抵抗52/137°C/Wは資料の試験基板に依存する値。本基板の値とみなさない。例として周囲40°C・137°C/W・温度によるRDS増加2倍を仮定した5 A連続ブレーキは約156°C。仮の125°C目標では約4.27 A RMSに相当するが、これは感度計算であり保護機能や保証定格ではない。
- 電源正常時のLOW/HIGHとUVLO時LOWは資料の意図を確認した。一方、5 V/3.3 Vの投入・喪失中の規定電圧未満、実ゲート重なり、Gate/Source別々の減衰、実VGS/VDSピークは未測定。OUTBの12 V電源条件のVOLを5 V全温度の保証値として代用していない。

## 補助解析と限界

schematic、full PCB、cross、EMC、thermalの各アナライザも実行し、[生の出力](q2-low-voltage/analysis/)を保存した。全体レビューの既存課題を自動的に解決したとは扱わない。

- cross: information 1件（MCU_3V3のデカップリング数）。U104はこのネットをENBとして使うため、IC数だけの不足判定を部品追加の根拠にはしない。
- thermal: **SKIPPED**。定量的損失／構造化資料が不足し、Q2の温度を算出していない。0 findingsを熱合格としない。
- EMC: 19件（error 2、warning 10、info 7）。GND面なし・Gate経路の戻り電流等は既存の設計懸念。GATE_Nを差動ペアとするDP-003は回路機能に合わない自動分類。認証適合／不適合を表す結果ではない。
- MPN・資料の全体カバレッジは部分的。Q2の端子・寸法・定格だけをメーカー資料と個別照合した。全回路の検証完了を主張しない。
- 今回は発注用Gerber/Excellon/BOM/CPLを生成していない。供給状況は親側の `q2-sourcing.md` に委ねる。

## 正規採用へ残る条件

1. ブレーキ期間・電流RMS／ピーク・周囲温度を電気的な使用範囲として定め、その条件で銅箔・Q2損失と温度を評価する。型番を限定せず、範囲外の負荷を無条件対応としない。
2. 最小電池電圧時のOUTB LOW≦0.30 V（GND差込み）、昇圧電源のUVLO余裕、投入／断・PWMのVGS/VDSと同時導通を、実ドライバを含むモデルまたは試作測定で確認する。
3. 選択PCBA業者に正確なMPN・ランド・ステンシル・実装方向を受け入れてもらう。発注数量は固定しない。
4. 以上の条件が揃った版だけを正規設計へ反映し、ERC/DRC/パリティ・ネット照合と製造出力の再生成／照合を行う。

本作業でT019/T038/T039を完了にはしていない。候補CADの製作可能な接続・クリアランスと、実動作の熱・保護評価は別の検査である。
