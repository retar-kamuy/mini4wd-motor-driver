# 検証手順

WSL/Linuxのシェルで正規パスのKiCad CLI、PCB解析器、ngspiceを使用する。PowerShellは不要。基板変更後は古いレポートや一時Gerberを再利用しない。

1. 回路図、基板、プロジェクト、ローカルライブラリの版・ハッシュと、設計前提・部品資料を記録する。
2. KiCadで銅箔を再充填し、全項目有効のDRCとERCを実行する。

```sh
kicad-cli pcb drc --exit-code-violations --severity-all --all-track-errors --refill-zones --save-board --schematic-parity --output specs/003-resolve-pcb-drc/verification/drc-final.rpt hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb
kicad-cli sch erc --severity-all --exit-code-violations --output specs/003-resolve-pcb-drc/verification/erc-final.rpt hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sch
```

3. 両レポートでエラー・警告・未接続・パリティ不一致0、無効チェックなしを確認。回路図ネットリストと全基板パッドを比較し、I2Cの意図したローカル名を含めて差を調査する。ネットリスト出力のアノテーション警告も扱う。
4. 主電流経路と動作モード、狭窄とビア、部品定格、メーカーランド、コネクタの端・向き、底面マスクを根拠表と実物データで確認。1.6 mm厚、55 × 21 mm、2層を確認する。
5. KiCadの回路図・PCB解析とEMC解析を同じ版で再実行し、各指摘を実データと照合する。SPICEは適用範囲を明示し、実機の熱・EMC適合の代替としない。
6. 最終版からGerber、Excellon、BOM、CPLを再生成し、ビューアで層・寸法・穴・底面テントと部品配置・向きを確認する。製造先への提出前チェックの結果と未確認項目を記録する。
