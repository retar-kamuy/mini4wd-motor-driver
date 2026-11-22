# WSL/Linuxでの開発

リポジトリを取得し、ルートを作業ディレクトリにします。利用資料は [README.md](README.md)、現行基板の残課題は [specs/003-resolve-pcb-drc/tasks.md](specs/003-resolve-pcb-drc/tasks.md) を参照してください。

使用するもの:

- GitとBash
- KiCad 10.0系、`kicad-cli`、KiCad付属のPython/pcbnew
- 適用する回路解析に応じてngspice
- KiCad MCPを使う場合はLinuxのNode.js、npmとサーバーのPython依存
- Reactスキル導入時はLinuxのNode.jsとnpm (`npx`)
- Spec Kitを使う場合は既存の `.specify/scripts/bash/` と `.agents/skills/`

現在の検証記録はKiCad 10.0.8によるものです。バージョンが異なる環境では結果を再確認してください。KiCad MCPの利用記録は [design-baseline.md](specs/003-resolve-pcb-drc/verification/design-baseline.md) にあります。

```sh
kicad-cli version
python3 -c 'import pcbnew; print(pcbnew.GetBuildVersion())'
bash .specify/scripts/bash/check-prerequisites.sh --json
```

基板を変更したら [検証手順](specs/003-resolve-pcb-drc/quickstart.md) を実行します。リポジトリの整理だけでは基板の製造承認は更新されません。

`origin` は自分のフォーク、`upstream` は元プロジェクトを参照します。開発成果は作業ブランチにpushして確認します。

---

## React / Web UI スキル

Vercel の [`agent-skills`](https://github.com/vercel-labs/agent-skills) は Agent Skills のコレクションです。使うスキルを `npx skills add` でプロジェクトの `.agents/skills/` に導入します。

```sh
npx skills add vercel-labs/agent-skills --skill react-best-practices
npx skills add vercel-labs/agent-skills --skill composition-patterns
npx skills add vercel-labs/agent-skills --skill react-view-transitions
npx skills add vercel-labs/agent-skills --skill web-design-guidelines
```

React Native / Expo を開発するときは、次も追加します。

```sh
npx skills add vercel-labs/agent-skills --skill react-native-skills
```

## Electron スキル

Vercel Labs の [`agent-browser`](https://github.com/vercel-labs/agent-browser) リポジトリにある Electron スキルをプロジェクトへコピーします。ソースがまだない場合は取得してください。

```sh
if [ ! -d plugins/agent-browser ]; then
  git clone https://github.com/vercel-labs/agent-browser.git plugins/agent-browser
fi
mkdir -p .agents/skills
cp -R plugins/agent-browser/skill-data/electron .agents/skills/
```

`.agents/skills/electron/SKILL.md` が存在することを確認します。このスキルは Agent Skill であり、Codex プラグインマーケットプレースへの登録は不要です。

## TypeScript スキル

Microsoft の [`typescript-skills`](https://github.com/microsoft/typescript-skills) から、6つのスキルをプロジェクトへコピーします。

```sh
if [ ! -d plugins/microsoft-typescript-skills ]; then
  git clone --depth 1 https://github.com/microsoft/typescript-skills.git plugins/microsoft-typescript-skills
fi
mkdir -p .agents/skills
cp -R plugins/microsoft-typescript-skills/plugins/typescript/skills/typescript-* .agents/skills/
```

スキルの `SKILL.md` が `.agents/skills/typescript-*/SKILL.md` にあることを確認します。対象は `typescript-project-setup`、`typescript-strict`、`typescript-build-references`、`typescript-publish-types`、`typescript-update`、`typescript-report-issue` です。

Codex プラグインとして使う場合は、代わりにCodex CLIで公式マーケットプレースを追加して `/plugins` から `typescript` をインストールできます。

```sh
codex plugin marketplace add microsoft/typescript-skills
codex plugin marketplace list
```

## Web アプリの作業上の注意

`web/index.html` は既存の Mini 4WD コンソールの入口です。React UI を追加するときは既存画面を置き換えず、対象機能の仕様で定めた専用エントリを使用します。React や TypeScript のコードを編集する前に、該当する `.agents/skills/` の `SKILL.md` を読みます。
