# KiCad design workflow

## Language

- Respond to the user, provide progress updates, and explain plans, designs, reports, and summaries in Japanese by default.
- Keep technical terms, component part numbers, and standards in their accurate original forms where appropriate.

## PCB design delegation

- Delegate PCB design, KiCad schematic or layout changes, and hardware design validation to the `pcb_design` subagent, which uses GPT-6.1 Sol. Give it clear ownership and coordinate shared files.

## Git operations

- Delegate all Git operations (including status checks, diffs, branch operations, commits, and remote operations) to the reusable `git_ops` subagent, which uses GPT-6 Luna. This delegation is independent of PCB work and applies to all repositories. Do not perform Git commands directly in the primary agent.

The `kicad-happy` Codex plugin is enabled for this repository in `.codex/config.toml`. For every KiCad or PCB design task—including schematic or layout creation, edits, review, validation, Gerber analysis, and manufacturing readiness—use the plugin's `kicad` skill at `plugins/kicad-happy/skills/kicad/SKILL.md` as the primary workflow. Read it before starting, use its analysis scripts and review requirements where applicable, and report which checks were run. The plugin package is kept under `plugins/kicad-happy/` so the project configuration and skill source stay together.

Also use the `kicad-happy` supporting skills under `plugins/kicad-happy/skills/` whenever their scope applies:

- `bom` for BOM creation or updates, component sourcing, distributor searches, BOM export, or fabrication preparation.
- `datasheets` when extracting or verifying component specifications from datasheets.
- `jlcpcb` or `pcbway` when preparing for the respective manufacturer's fabrication or assembly process.
- `digikey`, `mouser`, `lcsc`, or `element14` when sourcing parts from those distributors.
- `emc` for EMC/EMI risk reviews and pre-compliance planning.
- `spice` when simulating or validating analog subcircuits.

Read each applicable supporting skill's `SKILL.md` before using it. Do not claim DRC/ERC, simulation, sourcing, or manufacturing readiness without actually running the applicable checks and reporting their results.

## Spec 006 verification

- Use `specs/006-course-adaptive-mini4wd/verification.json` to identify checks and the evidence each requires. Continue independent checks when a physical measurement or supplier response is missing.
- Regenerate JLCPCB review files from the selected KiCad design with the command in `hardware/kicad/mini4wd-course-adaptive/manufacturing/README.md`. Keep the CAD hashes and check reports with the export. Record local CAM checks, supplier feedback, and physical measurements as separate evidence.

## TypeScript workflow and skills

The `typescript` Codex/Agent plugin (`microsoft/typescript-skills`) is installed in `plugins/typescript/` and enabled in `.codex/config.toml`. Whenever working on TypeScript code, configurations, or tooling—including project setup, strict type checking, build references, declaration output, or version updates—agents MUST use the corresponding skill from `plugins/typescript/skills/` (available under `.agents/skills/`):

- **`typescript-project-setup`**: Use whenever setting up, initializing, or configuring a TypeScript project (`tsconfig.json`, module resolution, bundlers such as Vite, and ESM configuration).
- **`typescript-strict`**: Use whenever enabling TypeScript `strict` mode or resolving compiler diagnostics and type errors. Follow its strict resolution process to achieve genuine type safety without weakening types (no arbitrary `any`, non-null assertions, or suppressed diagnostics) or altering runtime behavior.
- **`typescript-build-references`**: Use whenever configuring project references, incremental builds (`tsc -b`), composite tsconfigs, and `isolatedDeclarations`.
- **`typescript-publish-types`**: Use whenever producing or packaging TypeScript declaration files (`.d.ts`) to ensure downstream consumers resolve types properly.
- **`typescript-update`**: Use whenever updating TypeScript compiler versions.

Read the applicable skill's `SKILL.md` before beginning any TypeScript task, strictly follow its step-by-step workflow and definition of done, and report the checks performed.


