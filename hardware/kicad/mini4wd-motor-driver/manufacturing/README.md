> **製造禁止:** 旧版には Q2 5番パッドのメーカー端子との不一致があり、Q2修正後も電流・機構・部品などの設計検証が未完了である。詳細は `specs/003-resolve-pcb-drc/verification/parts-evidence.md` を参照。Gerber プレビューは修正前の記録である。

# Gerber出力

`gerber/` には、現在の基板から生成した確認用Gerber 8層とExcellonドリルがあります。`gerber-preview.zip` はその9ファイルをまとめたものです。`gerber/drc-report.rpt` と `gerber/source-sha256.txt` は出力時のDRC結果と入力ファイルのハッシュです。

## 再生成

WSL/Linuxのリポジトリルートから実行します。`kicad-cli` とPython 3が必要です。

```sh
hardware/kicad/mini4wd-motor-driver/manufacturing/export-gerbers.sh /tmp/mini4wd-gerber-next
```

引数のディレクトリへ出力し、その隣に `-preview.zip` を作成します。引数を省略すると `manufacturing/gerber/` を使用します。既存の出力を上書きしないため、空のディレクトリを指定してください。実行時に全項目有効のDRC、銅箔再充填、全配線の検査、回路図とのパリティを確認します。

## 設計上の残件

この出力は製造承認済みではありません。5 A電流経路の評価、コネクタの反対端への配置、昇圧回路のレイアウト、部品のメーカー資料との照合が未完了です。発注前には修正後の設計から再出力し、Gerberビューアと製造先の検証を行ってください。詳細は `specs/003-resolve-pcb-drc/verification/remaining-work.md` を参照してください。
