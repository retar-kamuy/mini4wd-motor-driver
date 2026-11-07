---
description: Create a git commit
argument-hint: "[--no-verify]"
---

# Commit

絵文字付き conventional commit で、整ったコミットを作成する。

## Language
- ユーザーへの説明・進捗報告・確認はすべて日本語で行う
- コミットメッセージ本文（type / subject / body）は英語のままにする
- 技術用語・コマンド名・ファイルパスはそのまま使う

## Features:
- デフォルトで pre-commit チェックを実行（lint, build, generate docs）
- staged がなければ適切なファイルを自動で stage
- 説明的な絵文字付き conventional commit 形式を使う
- 関心が分かれる変更はコミット分割を提案する

## Usage:
- `/commit` - pre-commit チェック付きの通常コミット
- `/commit --no-verify` - ユーザー入力に `--no-verify` が含まれる場合はチェックをスキップ

## Commit Types:
- ✨ feat: 新機能
- 🐛 fix: バグ修正
- 📝 docs: ドキュメント変更
- ♻️ refactor: 挙動を変えない再構成
- 🎨 style: フォーマットなど見た目の修正
- ⚡️ perf: パフォーマンス改善
- ✅ test: テストの追加・修正
- 🧑‍💻 chore: ツール・設定・メンテ
- 🚧 wip: 作業中
- 🔥 remove: コードやファイルの削除
- 🚑 hotfix: 緊急修正
- 🔒 security: セキュリティ改善

## Process:
1. staged 変更を確認する（`git status`）
2. staged がなければ内容を確認して適切なファイルを stage する
3. `--no-verify` でない限り pre-commit チェックを実行する
4. 差分から commit type を決める
5. 説明的なコミットメッセージを作る
6. 必要なら scope を付ける: `type(scope): description`
7. 複雑な変更は why を説明する body を付ける
8. Claude の co-authorship footer は付けない
9. コミットを実行する

メッセージ例:
```
✨ feat(scope): add concise imperative summary

Optional body explaining why.
```

## Best Practices:
- コミットは atomic で焦点を絞る
- 命令形で書く（"Add feature"、"Added feature" ではない）
- what だけでなく why を書く
- 関連する issue / PR があれば参照する
- 無関係な変更は分割する
- 明示されない限り push しない
- 秘密情報（`.env`、credentials など）は stage しない
