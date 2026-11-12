# Mini 4WD Motor Driver KiCad プロジェクト

Mini 4WD Motor Driver 基板の KiCad 10 ネイティブ設計プロジェクトです。回路図、PCB、プロジェクト固有フットプリントはこのディレクトリにあります。

## 主なファイル

- `mini4wd-motor-driver.kicad_pro` — 基板スタックアップと設計ルール
- `mini4wd-motor-driver.kicad_sch` — 回路図
- `mini4wd-motor-driver.kicad_pcb` — PCB レイアウト
- `mini4wd-motor-driver.pretty/` — Molex Micro-Fit、XIAO MG24 Sense、Coilcraft XEL4030 のフットプリント
- `manufacturing/` — DRC 合格後に生成する製造データ

昇圧コンバーターの L1 は、当初の設計指定に合わせて Coilcraft XEL4030-102ME（1.0 µH）を使用します。

## KiCad CLI

Windows の KiCad 10 標準インストールを使う場合は、リポジトリルートから次を実行します。

```powershell
$kicad = "C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
$project = "mini4wd-motor-driver/hardware/kicad/mini4wd-motor-driver"
$pcb = "$project/mini4wd-motor-driver.kicad_pcb"
$sch = "$project/mini4wd-motor-driver.kicad_sch"

& $kicad sch erc --severity-all --exit-code-violations $sch
& $kicad pcb drc --severity-all --exit-code-violations --output "$project/manufacturing/drc-report.txt" $pcb
```

ERC と DRC の違反を解消し、基板外形、電流経路、裏面ビアのテント状態を確認してから、KiCad のプロット機能で Gerber と Excellon を出力してください。BOM と部品配置ファイルも同じ PCB リビジョンから作成します。出力レイヤーとドリル仕様は [`manufacturing/layer-map.md`](manufacturing/layer-map.md) を参照してください。

## 製造リリースの確認

Gerber ビューアで全レイヤーの登録、外形と穴位置、部品面シルクを確認します。裏面ソルダーマスクにビア開口がないこと、ドリルデータに部品用スルーホールがないこと、BOM と CPL が搭載部品・座標・回転角に一致することを確認してから製造用パッケージとして扱います。
