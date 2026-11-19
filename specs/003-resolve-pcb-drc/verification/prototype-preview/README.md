# 試作版の製造データ確認用プレビュー

2026-11-15。これは設計検討時の出力であり、PCBAの発注データではない。[正規KiCad設計](../../../../hardware/kicad/mini4wd-motor-driver/)からGerber・ドリル、基板表面のCPL、回路図のBOM解析を出力した。データ元のハッシュは [source-sha256.txt](source-sha256.txt)。以後の回路・基板・属性の変更後には再生成が必要。

- [Gerber／ドリルのZIP](mini4wd-prototype-preorder-20261115-preview.zip): `manufacturing/export-gerbers.sh` を空の `/tmp` ディレクトリで実行。出力時DRC・未接続・パリティ0件、無効チェックなし。
- [Gerber解析](mini4wd-prototype-gerber-analysis.json): kicad skill `analyze_gerbers.py` でエラー・警告・情報0件。外形や個々の開口の目視、業者CAM/DFM確認の代替ではない。
- [CPL](mini4wd-prototype-cpl.csv): KiCadの表面実装座標、37行。業者用の原点・回転・部品向きは未照合。
- [BOM解析](mini4wd-prototype-bom.json): 37部品・29行、うち19行がMPN未設定。業者向けBOMではなく、未選定の候補を含む。

個別部品の定格・メーカー型番、XIAOと全基板部品の業者実装受入、Gerber/CPLの向き・座標、見積・DFMは未完了。製造・注文に使わない。
