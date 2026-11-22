# WSL/Linuxでの開発

リポジトリを取得し、ルートを作業ディレクトリにします。利用資料は [README.md](README.md)、現行基板の残課題は [specs/003-resolve-pcb-drc/tasks.md](specs/003-resolve-pcb-drc/tasks.md) を参照してください。

使用するもの:

- GitとBash
- KiCad 10.0系、`kicad-cli`、KiCad付属のPython/pcbnew
- 適用する回路解析に応じてngspice
- KiCad MCPを使う場合はLinuxのNode.js、npmとサーバーのPython依存
- Spec Kitを使う場合は既存の `.specify/scripts/bash/` と `.agents/skills/`

現在の検証記録はKiCad 10.0.8によるものです。バージョンが異なる環境では結果を再確認してください。KiCad MCPの利用記録は [design-baseline.md](specs/003-resolve-pcb-drc/verification/design-baseline.md) にあります。

## kicad-happyプラグイン

本プロジェクトでは [aklofas/kicad-happy](https://github.com/aklofas/kicad-happy) v3.0.2をCodexプラグインとして使用します。KiCad解析、SPICE、EMC、データシート、BOM、部品調達、JLCPCB/PCBWay製造準備のスキルを含みます。プロジェクト内のソースは `plugins/kicad-happy/` に置き、`.agents/plugins/marketplace.json` でローカルマーケットプレイスへ登録し、`.codex/config.toml` で有効にします。

### 導入時に行った手順

1. upstreamのv3.0.2タグを取得しました。導入したタグのcommitは `6b9767e19979cdef91631573753b1547efdbeab9` です。
2. リポジトリの内容を `plugins/kicad-happy/` に配置しました。上流リポジトリの `.git` は含めず、プラグインマニフェストと11個のスキルを含むソース一式をプロジェクトで管理します。
3. `.agents/plugins/marketplace.json` に `kicad-happy` のローカルソース `./plugins/kicad-happy` を登録しました。
4. `.codex/config.toml` の `[plugins."kicad-happy@mini4wd-motor-driver"]` を `enabled = true` にしました。
5. リポジトリルートでCodex CLIからマーケットプレイスを登録し、プラグインをインストールしました。

### 別環境のCodexへの登録

このプロジェクトをチェックアウトすると、プラグインソース、マーケットプレイス定義、有効化設定も取得されます。リポジトリルートでCodex CLIへ登録します。

```sh
codex plugin marketplace add .
codex plugin add kicad-happy@mini4wd-motor-driver
codex plugin list
```

`codex plugin list` で `kicad-happy` が `installed` と `enabled` の両方で有効になっていることを確認します。プラグインはCodexのユーザーキャッシュにもインストールされます。新しいスキルが表示されない場合はCodexを再起動し、新しい会話で確認してください。

導入時に使ったupstreamソース取得手順を再現する場合は、v3.0.2タグを一時ディレクトリへcloneし、`.git` を除いて `plugins/kicad-happy/` へ配置します。配置先に既存ファイルがある場合は、上書き前に差分を確認してください。

```sh
git clone --depth 1 --branch v3.0.2 \
  https://github.com/aklofas/kicad-happy.git /tmp/kicad-happy-v3.0.2
mkdir -p plugins/kicad-happy
tar -C /tmp/kicad-happy-v3.0.2 --exclude=.git -cf - . \
  | tar -C plugins/kicad-happy -xf -
```

KiCadまたはPCB設計時は、[AGENTS.md](AGENTS.md) の指示に従い `kicad-happy` のKiCadスキルを主ワークフローとして使います。部品調達や製造準備では、該当する同梱スキルも使用してください。

## typescriptプラグイン

WebコンソールやTypeScript関連ツールの開発・リファクタリングでは、Microsoft公式の [microsoft/typescript-skills](https://github.com/microsoft/typescript-skills) をCodexプラグインとして使用します。TypeScriptプロジェクトセットアップ、strictモード移行、プロジェクト参照（インクリメンタルビルド）、型定義公開検証、バージョンアップグレードのスキルを含みます。プロジェクト内のソースは `plugins/typescript-skills/`（プラグイン実体は `plugins/typescript/`）に置き、`.agents/plugins/marketplace.json` でローカルマーケットプレイスへ登録し、`.codex/config.toml` で有効にします。

### 導入時に行った手順

1. upstreamの `https://github.com/microsoft/typescript-skills.git` を取得しました。
2. リポジトリ内容を `plugins/typescript-skills/` に配置し、上流の `.git` を除外してプロジェクトで管理します。
3. プラグイン本体ディレクトリ（`plugins/typescript-skills/plugins/typescript/`）を参照するシンボリックリンク `plugins/typescript/` を作成しました。
4. 提供されるスキル（`typescript-project-setup`, `typescript-strict`, `typescript-build-references`, `typescript-publish-types`, `typescript-update`, `typescript-report-issue`）を `.agents/skills/` に配置しました。
5. `.agents/plugins/marketplace.json` に `typescript` のローカルソース `./plugins/typescript` を登録しました。
6. `.codex/config.toml` に `[plugins."typescript@mini4wd-motor-driver"] enabled = true` を設定しました。

### 別環境のCodexへの登録

本リポジトリをチェックアウト後、リポジトリルートでCodex CLIにローカルマーケットプレイスおよびプラグインを登録します。

```sh
codex plugin marketplace add .
codex plugin add typescript@mini4wd-motor-driver
codex plugin list
```

`codex plugin list` で `typescript` が `installed` と `enabled` の両方で有効になっていることを確認します。新しいスキルがCodex上で認識されない場合は、Codexを再起動してください。

> **Note**: GitHub上の公式リポジトリから直接登録する場合は、以下のコマンドでも導入可能です。
> ```sh
> codex plugin marketplace add microsoft/typescript-skills
> ```

### 導入手順の再現

upstreamソースから手動で再配置する場合は、以下を実行します。

```sh
git clone --depth 1 \
  https://github.com/microsoft/typescript-skills.git /tmp/typescript-skills
mkdir -p plugins/typescript-skills
tar -C /tmp/typescript-skills --exclude=.git -cf - . \
  | tar -C plugins/typescript-skills -xf -
ln -s typescript-skills/plugins/typescript plugins/typescript
cp -r plugins/typescript/skills/* .agents/skills/
```


```sh
kicad-cli version
python3 -c 'import pcbnew; print(pcbnew.GetBuildVersion())'
bash .specify/scripts/bash/check-prerequisites.sh --json
```

基板を変更したら [検証手順](specs/003-resolve-pcb-drc/quickstart.md) を実行します。リポジトリの整理だけでは基板の製造承認は更新されません。

`origin` は自分のフォーク、`upstream` は元プロジェクトを参照します。開発成果は作業ブランチにpushして確認します。
