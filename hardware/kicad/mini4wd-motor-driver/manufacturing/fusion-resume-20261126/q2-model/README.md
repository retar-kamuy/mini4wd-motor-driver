# Q2 PowerPAK SO-8の3Dモデル

2026-11-26。SI7137DP-T1-GE3のQ2表示用に、[KiCad公式パッケージモデル](https://gitlab.com/kicad/libraries/kicad-packages3D/-/blob/master/Package_DFN_QFN.3dshapes/PQFN-8-EP_6x5mm_P1.27mm_Generic.step)をダウンロードし、プロジェクト内の `3dmodels/PQFN-8-EP_6x5mm_P1.27mm_Generic.step` へ保存した。STEP内部の商品名は `Vishay_PowerPAK_SO-8`。

これはKiCadのパッケージ単位モデルで、VishayがSI7137DP個別型番用に認定したモデルではない。VishayのUltra Librarianページとユーザー提供ZIPでは3Dモデルを取得できず、旧KiCadモデル名も404だったため、信頼できる公開パッケージモデルを使った。取得元・ハッシュと照合値は `model-source.json` に記録した。

[Vishayパッケージ図71655](https://www.vishay.com/docs/71655/powerpak.pdf)の公称外形6.15×5.15mm、端子ピッチ1.27mm、高さ最大1.12mmを照合した。STEPのBREP頂点から求めた外形は6.15×5.15×1.09mm。曲面制御点は除いた頂点座標の測定で、厳密な形状干渉・公差解析ではない。KiCadの対応フットプリントと現Q2の端子1〜4は負X側、端子1は負Y側にある。回転0度、オフセット0、倍率1で配置した。

変更対象は004正規PCBと `board-routed.pretty/PowerPAK_SO-8_SI7137DP.kicad_mod` のモデル参照のみ。モデル以外のS式は変更前後で全一致し、ネット・パッド・配線・外形・設計規則を保持した。別の38部品保存候補のQ2は異なる型番なので適用していない。

KiCad 10.0.8の再DRCで違反0・未接続0・回路図パリティ0。回路図は未変更。上面と斜視でQ2本体と端子の表示を確認した。これは3D表示の追加であり、部品ランド認定や電気・熱・機構の全面評価ではない。

- [上面プレビュー](004-with-q2-top.png)
- [斜視プレビュー](004-with-q2-perspective.png)

KiCadのPCBエディターで004正規PCBを開き直し、Alt+3で表示する。プロジェクトと3dmodelsを一緒に保持する。既存画面を開いたままの場合は、古い画面から保存せずファイルを開き直す。
