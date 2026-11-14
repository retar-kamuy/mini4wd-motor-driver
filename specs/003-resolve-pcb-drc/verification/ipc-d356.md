# IPC-D-356の出力確認

KiCad CLI 10.0.8 の `pcb export ipcd356` が利用可能であり、正規基板から出力に成功した。

```sh
kicad-cli pcb export ipcd356 --output /tmp/m4-current.ipc hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb
```

[現行版の出力例](current-preview.ipc) のヘッダはIPC-D-356A、I²Cのローカルネット名、部品・パッド、ビアのレコードを含む。これは製造未承認の途中版。最終設計確定後、同コマンドで `hardware/kicad/mini4wd-motor-driver/manufacturing/mini4wd-motor-driver.ipc` を再生成し、ネット照合とハッシュを最終レビューに記録すること。既存FR-011は出力機能の不足を理由に除外する必要がない。
