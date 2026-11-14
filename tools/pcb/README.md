# PCB配置・配線の検証補助

設計正本は `hardware/kicad/mini4wd-motor-driver/`。ここにあるスクリプトは
配置候補・配線の取り込み・ネット照合を補助する。製造承認は行わない。
WSL/LinuxのshとKiCadの`pcbnew`を提供するPythonを使う。

- `pack_candidate.py SOURCE OUTPUT`: 別の出力先へ検証対象を複製し、旧銅箔を除去して全部品を配置する。Courtyardの矩形による探索であり、メーカー推奨配置・アンテナ禁止領域・熱を保証しない。`sexpdata`が必要。
- `add_power_backbone.py BOARD`: 指定配置専用の電力経路と層間接続を追加し、ロックしてDSNへ出力する。配置と未配線状態を確認し、`.cache/routing/`以外を拒否する。汎用ルータではない。
- `import_route_trial.py BOARD SESSION`: 非空SESを候補へ取り込む。固定した経路の形状が残ることを照合し、ビアの裏面テントを指定する。取り込み後のDRCは別途必須。
- `audit_connectivity.py BOARD XML REPORT`: KiCad CLIが出力したXMLネットリストと全パッドを照合し、基板寸法・層数・ビア・ネット別配線幅と長さをJSONへ記録する。メーカー端子図との照合は別途必要。

実行例（リポジトリルートから）:

```sh
PYTHONPATH=.cache/routing/pydeps /usr/bin/python3 tools/pcb/pack_candidate.py \
  hardware/kicad/mini4wd-motor-driver .cache/routing/trial
/usr/bin/python3 tools/pcb/add_power_backbone.py \
  .cache/routing/trial/mini4wd-motor-driver.kicad_pcb
```

固定座標は2026-11-14の配置候補に依存する。入力の設計版や部品順が変わり、
別の配置が選ばれた場合は適用を中止して配置を検討し直す。
配線処理が終了するまでSESを取り込まず、空のSESや取り込み失敗を成功と扱わない。

Freerouting v2.0.1では診断送信とAPIサーバーを無効にする設定を使用した。
サンドボックス外実行は利用者の明示許可に基づく。
ネット接続が完了しても、5 A電流容量、ゲート駆動、EMC、BOM、ランド、
ビア実装方式および製造データの適合性が確認できるまでは製造に使用しない。
