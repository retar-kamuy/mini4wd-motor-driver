---
title: Spec Kit 初期化時に Git extension を導入する
tags:
  - speckit
  - git
  - development
---

# Spec Kit 初期化時に Git extension を導入する

Spec Kit の Git extension は、feature branch の作成・命名確認、Git remote の検出、Git 初期化、任意の自動コミットを Spec Kit の workflow に加える拡張機能です。

## 初期化と同時に導入する

新しいプロジェクトを作成する場合は、`specify init` に `--extension git` を付けます。

```sh
specify init my-project --integration codex --extension git
```

現在のディレクトリに初期化する場合:

```sh
specify init --here --integration codex --extension git
```

agent の対話選択を使わず実行する例:

```sh
specify init my-project --non-interactive --integration codex --extension git
```

`--extension` は複数回指定でき、他の extension と同時に導入できます。

```sh
specify init my-project --integration codex --extension git --extension selftest
```

## 既存の Spec Kit プロジェクトに追加する

初期化後に追加する場合は、プロジェクトのルートで実行します。

```sh
specify extension add git
```

導入状態は次のコマンドで確認できます。

```sh
specify extension list
specify extension info git
```

無効化・再有効化:

```sh
specify extension disable git
specify extension enable git
```

## 自作 extension を初期化時に渡す

extension をローカルで用意し、そのディレクトリのパスを `--extension` に渡します。

```sh
specify init my-project --integration codex --extension ./my-extensions/my-git-workflow
```

extension の形式や必須ファイルは、使用する Spec Kit CLI の extension 開発仕様に合わせます。公開 URL から導入する場合は HTTPS URL を指定します。非対話実行で URL を使うときは、信頼を明示する `--trust-extension-urls` が必要です。

## Git extension が提供するもの

この Git extension は、Spec Kit の workflow に以下のコマンドや hook を登録します。

- `speckit.git.initialize`: Git repository の初期化
- `speckit.git.feature`: feature branch の作成
- `speckit.git.validate`: branch 名の規則確認
- `speckit.git.remote`: Git remote の検出
- `speckit.git.commit`: 任意の自動コミット

branch 番号は連番または timestamp を選べます。自動コミットは既定で無効です。設定ファイル `.specify/extensions/git/git-config.yml` で番号方式、branch 名の形式、commit message、workflow ごとの自動コミットを調整できます。

このリポジトリでは Git extension が `.specify/extensions/git/` に導入済みで、`.specify/extensions/.registry` 上も有効です。extension の概要と設定例は [extension README](../.specify/extensions/git/README.md) を参照してください。
