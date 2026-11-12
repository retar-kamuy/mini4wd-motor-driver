# 設計変更前の基準

記録日: 2026-11-10
正規対象: `hardware/kicad/mini4wd-motor-driver/`
KiCad CLI: 10.0.8
Git 作業ツリーは記録時点ですでに変更・未追跡・削除を含む。以下は設計作業開始前の状態であり、既存変更を上書き・復元する指示ではない。

## SHA-256

```text
0dfe9dc2729c821b68c8cddb1c5d0483f302d7088d53bb94dd593aedbf117cb6  hardware/kicad/mini4wd-motor-driver/board-routed.pretty/Coilcraft_XEL4030.kicad_mod
004e05db818cfe2a501b1f9b28b58188042bed92b0b404474f569a983d8fc39c  hardware/kicad/mini4wd-motor-driver/board-routed.pretty/Molex_MicroFit30_43650-0214.kicad_mod
72aa40f6e4cbf1edc4bb67e62b4afbd752d700422d26bda9e5e7d16af06a2224  hardware/kicad/mini4wd-motor-driver/board-routed.pretty/PowerPAK_SO-8_SI7137DP.kicad_mod
ac0ca7ace575dcd8c2c5297e3b09464da67b2de6129796a644599b24d46cc586  hardware/kicad/mini4wd-motor-driver/board-routed.pretty/XIAO_MG24_Castellated_14P.kicad_mod
3c5896886e5bed48a2c1b7f3388b27dc7b01b24c28e57a3e31f2bfdf78e0bf35  hardware/kicad/mini4wd-motor-driver/fp-lib-table
22af737b0fa478d5a0c706381f563432f131907c65d8a3ec9ec54576f9ae4029  hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb
b45ff3ffb2cd60255fbebd5003f734b688c7f039a4a8e7bfefa4b957977899f2  hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pro
3357c92279a2b6f13c300878592a897cf8625dddddbefaa42467dd0742c008a7  hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sch
72f0a0c332ecacf51d2ed89ec95940924d789678d5b73c5081b2657da36bf4f9  hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sym
d298fcd70482ab59a4d7ae4edf06b1b2b70545cc7050ee2386cd398693fa223f  hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.pretty/Coilcraft_XEL4030.kicad_mod
8b575adacf9d8a11af8f2b14fd6fd288c6ddf3fe10bb289f4a8ce5b8756b3faf  hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.pretty/Molex_MicroFit30_43650-0214.kicad_mod
a5af9e8e865ebc5beb413ae63e00621384221c904c5b3cb23268c00237fd91c4  hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.pretty/PowerPAK_SO-8_SI7137DP.kicad_mod
e34b08836ef3c362e9453a3ca9d22fef29716ae67983dc55b40a8f5412e10aea  hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.pretty/XIAO_MG24_Castellated_14P.kicad_mod
e45618abfed4d115ea7719a44202e37f47615efac3c091dabf369ef4fd440e58  hardware/kicad/mini4wd-motor-driver/mini8wd-motor-driver.pretty/Molex_MicroFit30_43650-0214.kicad_mod
19a04cab3ea67da39d3078657f2f824981526e9114d19f573cd4bc9487a30d99  hardware/kicad/mini4wd-motor-driver/sym-lib-table
```

## 作業ツリー

```text
 M .agents/skills/speckit-analyze/SKILL.md
 M .agents/skills/speckit-checklist/SKILL.md
 M .agents/skills/speckit-clarify/SKILL.md
 M .agents/skills/speckit-constitution/SKILL.md
 M .agents/skills/speckit-converge/SKILL.md
 M .agents/skills/speckit-implement/SKILL.md
 M .agents/skills/speckit-plan/SKILL.md
 M .agents/skills/speckit-specify/SKILL.md
 M .agents/skills/speckit-tasks/SKILL.md
 M .agents/skills/speckit-taskstoissues/SKILL.md
 D .cursor/commands/commit.md
 M .gitignore
 M .specify/init-options.json
 M .specify/integration.json
 D .specify/integrations/agy.manifest.json
 M .specify/integrations/speckit.manifest.json
 M .specify/scripts/powershell/check-prerequisites.ps1
 M .specify/scripts/powershell/common.ps1
 M .specify/scripts/powershell/setup-tasks.ps1
 M .specify/templates/checklist-template.md
 M .specify/templates/plan-template.md
 M .specify/templates/tasks-template.md
 M .specify/workflows/workflow-registry.json
 D GEMINI.md
 M hardware/kicad/mini4wd-motor-driver/fp-lib-table
 M hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pcb
 M hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_pro
 M hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sch
 M hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.pretty/Coilcraft_XEL4030.kicad_mod
 M hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.pretty/Molex_MicroFit30_43650-0214.kicad_mod
 M hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.pretty/XIAO_MG24_Castellated_14P.kicad_mod
 M hardware/kicad/mini4wd-motor-driver/mini8wd-motor-driver.pretty/Molex_MicroFit30_43650-0214.kicad_mod
 D prompt.md
 M specs/001-smt-gerber-board/checklists/requirements.md
 M specs/001-smt-gerber-board/contracts/board-interface-and-fabrication.md
 M specs/001-smt-gerber-board/plan.md
 M specs/001-smt-gerber-board/quickstart.md
 M specs/001-smt-gerber-board/research.md
 M specs/001-smt-gerber-board/spec.md
 M specs/001-smt-gerber-board/tasks.md
 M specs/002-port-to-kicad/checklists/requirements.md
 M specs/002-port-to-kicad/contracts/board-interface-and-fabrication.md
 M specs/002-port-to-kicad/data-model.md
 M specs/002-port-to-kicad/plan.md
 M specs/002-port-to-kicad/progress-summary.md
 M specs/002-port-to-kicad/quickstart.md
 M specs/002-port-to-kicad/research.md
 M specs/002-port-to-kicad/spec.md
 M specs/002-port-to-kicad/tasks.md
?? .agents/skills/commit/
?? .specify/integrations/codex.manifest.json
?? .specify/scripts/bash/
?? AGENTS.md
?? Microsoft/
?? SETUP.md
?? drc_clean.rpt
?? drc_flawless.rpt
?? drc_new.rpt
?? drc_perfect.rpt
?? drc_step11.rpt
?? drc_step12.rpt
?? drc_step8.rpt
?? drc_step9.rpt
?? drc_ultimate.rpt
?? drc_v2.rpt
?? drc_zero_cross.rpt
?? hardware/kicad/mini4wd-motor-driver/board-routed.pretty/
?? hardware/kicad/mini4wd-motor-driver/manufacturing/
?? hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.kicad_sym
?? hardware/kicad/mini4wd-motor-driver/mini4wd-motor-driver.pretty/PowerPAK_SO-8_SI7137DP.kicad_mod
?? hardware/kicad/mini4wd-motor-driver/sym-lib-table
?? mini4wd-motor-driver-drc.rpt
?? mini4wd-motor-driver-erc.rpt
?? mini4wd-motor-driver/
?? specs/003-resolve-pcb-drc/
?? tmp/
```

## KiCad MCP

このセッションの公開ツール一覧に KiCad MCP は見つからない。既存の FR-012 に基づき、利用者は KiCad MCP を提供する選択をした。MCP が接続されるまで配置・配線変更を保留し、資料調査を独立して進める。

## MCPの起動・操作記録（2026-11-12）

`/home/ubuntu/Repositories/KiCAD-MCP-Server` のKiCad MCP 2.8.3をWSL上で使用した。元のインストール先は変更せず、ソース・設定・package-lockを `/tmp/kicad-mcp-runtime` に置き、LinuxのNode.jsで `npm ci --ignore-scripts`、TypeScriptの `tsc -p tsconfig.json` を実行した。Python依存 `sexpdata kicad-skip python-dotenv colorlog pydantic requests` は同ディレクトリの `pydeps` にインストールし、`KICAD_PYTHON=/usr/bin/python3` と `PYTHONPATH=/tmp/kicad-mcp-runtime/pydeps` を指定して `node dist/index.js` をSTDIO MCPとして起動した。正規PCBを `open_board` で開き、旧配線のビア・トラックを `delete_trace` で削除し、`save_board` で保存した。

一時ディレクトリは再起動後に消えるため、再利用時は同じセットアップを再実行する。WSLのNode.jsとnpm、Python/pipおよびKiCad pcbnewが必要。詳細と操作結果は [q2-repair.md](q2-repair.md)。
