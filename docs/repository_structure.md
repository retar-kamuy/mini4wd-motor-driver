# リポジトリ構成と来歴

| パス | 用途 |
|---|---|
| `hardware/kicad/mini4wd-motor-driver/` | 現行設計の唯一の正本。製造未承認 |
| `hardware/rev1/` | 設計入力、旧BOM、配線の検討資料 |
| `hardware/archive/kicad-before-consolidation/` | 集約前のKiCad設計。参照専用 |
| `firmware/` | XIAO向けファームウェア |
| `web/` | ブラウザから使用するWebアプリ |
| `docs/` | 利用・開発資料と元基板の画像 |
| `tools/` | 書込・リリースツール |
| `specs/` | 要件、判断、残課題と検証記録 |
| `.specify/`, `.agents/` | 開発ワークフロー |

元プロジェクトは https://github.com/keimyojizai/mini4wd-motor-driver 、公開先は https://github.com/retar-kamuy/mini4wd-motor-driver です。
元の `main` と開発時の `master` は異なる初期履歴でした。整理ブランチでは両履歴を親として保持し、内側の作業ツリーから利用資料・ソフトウェアと既存の未コミット変更を取り込みました。

ローカルに残した `mini4wd-motor-driver/` は移設元の作業コピーです。今後の編集対象は上表の正本です。このコピーと `tmp/`、環境固有の `Microsoft/`・`KiCad/`、ルートの試行DRCレポートは公開対象外にしました。現行の検証記録は `specs/003-resolve-pcb-drc/verification/` で管理します。

GitHub Pagesの公開対象は `web/` です。既存のWindows向けファームウェア書込ツールは利用者向けの機能として残しています。
