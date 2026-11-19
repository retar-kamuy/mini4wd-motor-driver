# Q2候補の調達状況

確認日: 2026-11-15。DMP2008UFG-7は試作版の正規設計へ反映済みだが、実機の電気・熱評価と業者の調達・実装受入は未完了であり、発注部品としての供給は未確定。[試作版の反映記録](prototype-design-release.md)を参照。

- [メーカー製品情報](https://www.diodes.com/part/view/DMP2008UFG)にPowerDI3333-8のP-channel MOSFETとして掲載され、メーカー製品情報から参照されるデータシートにはDMP2008UFG-7が記載される。公開PDFはAdvance Information表記のため、最終保証や供給状況はメーカー・実装先への確認が必要。
- [LCSCの部品ページ](https://www.lcsc.com/product-detail/C461052.html)に、メーカーDIODES、MPN DMP2008UFG-7、LCSC番号C461052、PowerDI3333-8の一致を確認。LCSC商品登録はJLCPCBの実装受入や、Seeed Fusionでの調達・実装を保証しない。
- LCSCスキルの `search_lcsc.py 'DMP2008UFG' --limit 10 --json` はDNS名前解決失敗で終了コード2。ライブ在庫・実装区分・価格は取得できなかった。ウェブ検索の在庫断片は取得時刻が古いか特定できないため、現在庫として扱わない。
- [DigiKey掲載ページ](https://www.digikey.com/en/products/detail/diodes-incorporated/DMP2008UFG-7/3720098)の取得済み検索結果は在庫切れ／取り寄せ可能と示したが、更新時点が不明。発注直前に再確認する。

採用前に、選定したPCBA業者へ実装番号・最新数量・リール/カットテープの供給・部品消耗数・PowerDI3333-8の実装/検査可否を見積で照会する。DMP2008UFG-7の選定を理由に基板部品の手はんだ後付けを前提としない。
