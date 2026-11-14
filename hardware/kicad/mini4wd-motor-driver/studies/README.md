# 回路検討シート

`gate-control.kicad_sch` と同名の `.kicad_pro` は分離ゲート回路の設計検討用プロジェクトです。主回路へは未統合で、製造対象ではありません。実装正本は親ディレクトリの `mini4wd-motor-driver.kicad_sch` とPCBです。

- PWM_DRIVE: MCUからのPWM。
- MCU_3V3 / BOOST_5V / GND: 主回路からの電源。
- GATE_N / GATE_P: Q1 / Q2へ渡す個別出力。
- U101: LTC6994-2 S6候補。DIV=GND、SET=499 kΩで約9.98 µsの検討値。
- U104: UCC27524A候補。標準UCC27524Dシンボルを端子互換性の照合に基づき使用。
- U105: TLV809EA30DBZR候補。RESET_OKを0 ΩリンクR103経由でENAへ接続し、R104=2.2 kΩでプルダウン。

J101は上記6ネットの外部接続条件を表す検査用インターフェースで、BOM・PCBから除外しています。指定したピンヘッダのフットプリントは検査用で、主基板への実装追加ではありません。PWR_FLAGはこの境界から3.3 V・5 V・GNDが供給されることを示します。実際の統合時には主回路側の電源源・MOSFETへ接続し、検査用インターフェースと重複する電源フラグを引き継がないでください。

全ERC項目有効・除外なしでエラー0、警告0を確認しました。レポートは `specs/003-resolve-pcb-drc/verification/deadtime/study-erc-all.rpt`。独自ライブラリはプロジェクト内の `sym-lib-table` と `gate-study.kicad_sym` で解決します。

ERC合格は電源順序、遅延の実部品公差、過渡、熱、配置・製造の検証完了を意味しません。
