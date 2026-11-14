# 共有ゲート駆動の予備評価

対象は `hardware/kicad/mini4wd-motor-driver/`、PCB SHA-256 `c6a4986c8ed964493ffa553796c3ffb24a09a53b488ef7e7627080b6e3c0da67`。解析段階であり、動作確認または設計完了ではない。

## 構成と定常状態

Q1はN-channel低側スイッチ、Q2はP-channelブレーキスイッチ。Q1 sourceはGND、Q2 sourceはVBAT、両gateはU1のGATE_DRIVEに接続される。よって概略 `VGS(Q1)=VG`、`VGS(Q2)=VG−VBAT`。ドライバ出力highを5 V、lowを0 Vとする理想化では、high時にQ1が駆動、low時にQ2がブレーキ動作を意図する。バッテリー電圧範囲と実際のhigh/low出力電圧・損失を確定しない限り、全条件で両者が意図通りON/OFFするとは言えない。

## 同時導通の懸念

[Vishay SiSS64DN](https://www.vishay.com/docs/67294/siss64dn.pdf) p.2のQ1閾値は1.1–2.2 V、[Si7137DP](https://www.vishay.com/docs/69063/si7137dp.pdf) p.2のQ2閾値は−0.5〜−1.4 Vで、どちらも250 µA条件。例としてVBAT=3 V、VG=1.5 Vでは、Q1のVGS=1.5 V、Q2のVGS=−1.5 Vとなり、両方の閾値を超え得る。これは貫通電流の確定値ではなく、切替時に両MOSFETが同時に導通する可能性を示す。閾値は5 A時のオン電圧を示さない。

Q2のデータシートp.2はVGS=−4.5 Vでgate charge典型188 nC、最大282 nCを示す。実際の駆動電圧、寄生インダクタンス、U1の出力電流、Q1/Q2の伝達特性とPWM周波数を含め、立上り・立下り・損失を評価する。独立したデッドタイムを持たない共有ゲートのままで許容できるとまだ判定できない。

## 起動・停止

[TI UCC27511](https://www.ti.com/lit/ds/symlink/ucc27511.pdf) は4.5–18 V動作、UVLO時は出力low。[TI TPS61023](https://www.ti.com/lit/ds/symlink/tps61023.pdf) は1.8 V以上の起動入力を指定する。低電池・昇圧立上り時のgate、ブレーキ状態、復帰時の制御とXIAO出力初期状態を未評価。VBATおよび負荷の範囲を特定し、モデルと必要な保護・回路変更を検討する。

## 残作業

PWMと電池の条件確定、メーカーの部品モデルの適用可否調査、駆動・ブレーキ・過渡時の電源電流と素子損失の評価、シミュレーションまたは別の根拠に基づく回路修正。T019は未完了のまま維持する。

## ファームウェアの入力条件

`firmware/mini4ai_v358/mini4ai_v358.ino` は PC2をPWM端子に指定し、`analogWrite(PWM_PIN, d)` を呼ぶ。起動時はLOWを指定している。ソース中の200 HzはIMUからの制御ループについての記述であり、PWMキャリア周波数として扱えない。使用するボードコアの `analogWrite` 実装と設定を確認するまで、PWM周波数を未確定とする。

## 部品追加の承認

NiMHとアルカリの双方を対象とする回答を受けた。共有ゲートの過渡対策として保護・遅延回路などの追加を検討するが、利用者は必要な部品追加を許容した。回路案の採否・必要な部品・遅延時間はまだ確定していない。

## 分離ゲート案の論理検証

候補はPWM `A` とRC＋Schmittで遅延した `D` を用い、Q1用ドライバ入力を `A AND D`、Q2用ドライバ入力を `A OR D` とする。Q2はP-channelなのでgate highがOFF、lowがON。A≠Dの間は両者OFFとなる。単一PWM入力と定常的な駆動／ブレーキの対応を保持する。

候補デバイスは [SN74LVC1G17](https://www.ti.com/lit/ds/symlink/sn74lvc1g17.pdf)、[SN74LVC1G08](https://www.ti.com/lit/ds/symlink/sn74lvc1g08.pdf)、[SN74LVC1G32](https://www.ti.com/lit/ds/symlink/sn74lvc1g32.pdf) と [UCC27524A](https://www.ti.com/product/UCC27524A) の2系統ゲート駆動。これは採用前の候補であり、従来UCC27511の単純なOUTH/OUTL分離では独立した2ゲートの駆動にならない。

ngspice 45.2で [logic.cir](deadtime/logic.cir) を実行。3.3 V、RC=10 kΩ/1 nF、閾値1.65 Vの簡略論理モデルでは、40 µs周期・20 µs highで論理重なり0、立上りデッドタイム約6.94 µs、立下り約5.48 µs。パルス幅0.2/1/20/39 µs、抵抗8/10/12 kΩの12ケースも論理重なり0だった（[結果](deadtime/logic-sweep.json)）。

このモデルはヒステリシス、IC伝播遅延、出力インピーダンス、MOSFET特性、起動と電源異常を含まない。実際の最小デッドタイムや貫通電流を保証しない。次はSchmitt閾値の保証範囲、R/C公差、ゲート駆動の過渡、起動・停止と短パルスを含めて評価し、部品・回路と配置を確定する。T019は未完了。

## 短パルス再検討による方式変更

単純なRC＋Schmitt案は、RCが十分に復帰しない短パルス列で遅延が短縮され得る。前記12ケースで理想論理の重なりが0だったことは、最小OFF期間の証明ではない。この案を回路図へそのまま採用しない。

[Analog Devices LTC6994-2資料](https://www.analog.com/media/en/technical-documentation/data-sheets/LTC6994-1-6994-2.pdf) p.15は、両エッジ遅延と入力変化時のタイミング再開始、短パルス除去を記載する。RC＋Schmittをこの種の再トリガ可能な両エッジ遅延器に置き換え、AND/ORと独立2系統ドライバを使う案へ絞る。10 µsを検討値とし、最終値は部品公差・電源・駆動遅延とPWM仕様を照合して決定する。

[qualifier_sweep.py](deadtime/qualifier_sweep.py) は5種類の入力間隔（0.1/1/9.9/10.1/20 µs）を5回組み合わせた3125列について、仮定した3組のON/OFF遅延でイベントモデルを実行した。[結果](deadtime/qualifier-results.json) は9375ケースで同時ON=0。出力段は短すぎる保留遷移をキャンセルする慣性遅延として扱っている。この仮定を含め、実部品の最小パルス応答、供給電圧変化、起動、アナログ過渡は未検証。T019の完了証拠にはしない。

候補UCC27524AのSOIC-8端子は [TI資料](https://www.ti.com/lit/ds/symlink/ucc27524a.pdf) p.3より、1=ENA、2=INA、3=GND、4=INB、5=OUTB、6=VDD、7=OUTA、8=ENB。チャンネルAをQ1、BをQ2へ割り当てる案とし、両入力を共有しない。UVLOでは両出力lowとなるためQ1はOFF、Q2はブレーキ側となる。ただしQ2のgate/source電源条件と起動経過は別途評価する。

## MCPによる検討回路図の作成

`hardware/kicad/mini4wd-motor-driver/studies/gate-control.kicad_sch` をMCPのcreate_schematic、batch_add_and_connectで作成し、generate_netlistで11部品・38ピンのネットを取得した。主回路図への統合前の検討シートであり、製造対象ではない。U101はS6端子1=IN、2=GND、3=SET、4=DIV、5=V+、6=OUT。RSET=499 kΩ、DIV=GNDを検討値とした。

独立シートの [ERC](deadtime/study-erc.rpt) は電源未駆動3件とGATE_N/Pの接続先がない警告2件。主回路への統合で電源・MOSFETを接続する必要がある。検討シートのデフォルトERC設定には無効チェックもあるため、最終合格判定には使わず、統合後に正規プロジェクトの全チェックで検査する。

[遅延器資料](https://www.analog.com/media/en/technical-documentation/data-sheets/LTC6994-1-6994-2.pdf) p.16では起動期間にOUTをlowへ保持するとする。3.3 V立上り途中のロジック出力・ドライバENABLEが保証されない期間について、Q1のENAを電源監視信号で許可する対策が必要。現在の検討シートはENA/ENBをMCU_3V3に直結しており、この対策はまだ含めていない。T019は引き続き未完了。

## 起動保護の検討シートへの追加

U105にTLV809EA30DBZR（3.08 V、プッシュプルactive-low reset、200 ms遅延の候補）、C106に100 nFを追加。RESET_OKを0 ΩリンクR103経由でU104 ENAへ接続し、R104=2.2 kΩでENAをGNDへプルダウンする。ENBはMCU_3V3のまま。監視出力low時にQ1を禁止し、Q2側は既存のブレーキ側動作を意図する。

[TI監視器資料](https://www.ti.com/lit/ds/symlink/tlv803e.pdf) p.8はTLV809EのVOHをVDD=3.3 V・2 mA時0.8 VDD以上とする。R104の約1.5 mA負荷はこの条件に入る。UCC27524AのEN high最大閾値は2.3 V（[資料](https://www.ti.com/lit/ds/symlink/ucc27524a.pdf) p.6）。一方、監視器の出力保証は0.7 V未満ではなくなる。U104内蔵ENプルアップは典型200 kΩで最小値の保証を確認できておらず、3.3 V喪失時にR104が十分なlowを保証するかは未確定。全電源順序を網羅した合格とはしない。

MCPでシンボル作成とラベル変更を実行したが、独自ライブラリの部品置換が失敗したため、検討シートへのU105配置をS式編集で補正した。その後KiCad CLIのネットリスト出力が成功し、RESET_OKにU105/2とR103/1、DRIVE_ENABLEにR103/2・R104/1・U104/1が接続されることを確認した。主回路とPCBへの統合は未実施。

## Q2低電圧候補

Si7137DPは低電圧のブレーキ損失を引き続き評価する。代替候補 [Diodes DMP2008UFG](https://www.diodes.com/part/view/DMP2008UFG) はVGS=−1.8 VでRDS(on)最大13 mΩを掲載する。25°Cで5 Aを仮定すると導通損失の単純計算は0.325 W。ただし温度依存、切替・還流、パッケージ・ランド、実電流波形と熱抵抗を未確認のため採用確定ではない。PowerDI3333-8なので現Q2のPowerPAK SO-8と直接置換できない。

## 検討シートERCの解消

外部接続境界としてJ101（MCU_3V3、BOOST_5V、GND、PWM_DRIVE、GATE_N、GATE_P）を追加し、BOMとPCBから除外した。外部供給3電源のPWR_FLAGを追加。独立したgate-control.kicad_proを作成し、正規プロジェクトの全チェック有効ERCルールを適用してローカルシンボルライブラリを参照可能にした。J101のフットプリント指定も一致させた。

`kicad-cli sch erc --severity-all --exit-code-violations` を実行し、[study-erc-all.rpt](deadtime/study-erc-all.rpt) でエラー0、警告0、無効チェックなしを確認。以前の6件は解消した。これは検討回路単体での外部電源・出力先を前提とする結果で、主回路へ統合後は検査用境界を除いて再検査する。

- `gate-control.kicad_sch` SHA-256: `2d0d973ba79fceca46b736bca67de091018de6d8bdaaf5e35bfbc36adc548376`
- `gate-control.kicad_pro` SHA-256: `1298a20b4ff6885cbf95a8570dfee3e110ed6518e8c98737636ed69ba965fbb0`
- `gate-study.kicad_sym` SHA-256: `6838449d909c63f05be2ff650fe296f55b8d1be5421e81c02522f6fddb08715f`
- `sym-lib-table` SHA-256: `52a2e9d0be608e4f94bf846c36df446ea3d49e1ffe35f29684e1ec306924974d`
