# WSL/Linuxでの開発

リポジトリを取得し、ルートを作業ディレクトリにします。利用資料は [README.md](README.md)、現行基板の残課題は [specs/003-resolve-pcb-drc/tasks.md](specs/003-resolve-pcb-drc/tasks.md) を参照してください。

使用するもの:

- GitとBash
- KiCad 10.0系、`kicad-cli`、KiCad付属のPython/pcbnew
- 適用する回路解析に応じてngspice
- KiCad MCPを使う場合はLinuxのNode.js、npmとサーバーのPython依存
- Spec Kitを使う場合は既存の `.specify/scripts/bash/` と `.agents/skills/`

現在の検証記録はKiCad 10.0.8によるものです。バージョンが異なる環境では結果を再確認してください。KiCad MCPの利用記録は [design-baseline.md](specs/003-resolve-pcb-drc/verification/design-baseline.md) にあります。

```sh
kicad-cli version
python3 -c 'import pcbnew; print(pcbnew.GetBuildVersion())'
bash .specify/scripts/bash/check-prerequisites.sh --json
```

基板を変更したら [検証手順](specs/003-resolve-pcb-drc/quickstart.md) を実行します。リポジトリの整理だけでは基板の製造承認は更新されません。

`origin` は自分のフォーク、`upstream` は元プロジェクトを参照します。開発成果は作業ブランチにpushして確認します。
