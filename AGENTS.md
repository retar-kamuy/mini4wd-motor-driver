# KiCad design workflow

## Language

- Respond to the user, provide progress updates, and explain plans, designs, reports, and summaries in Japanese by default.
- Keep technical terms, component part numbers, and standards in their accurate original forms where appropriate.

## PCB design delegation

- Delegate PCB design, KiCad schematic or layout changes, and hardware design validation to the `pcb_design` subagent, which uses GPT-6.1 Sol. Give it clear ownership and coordinate shared files.
- Use the `git_ops` subagent for Git operations as already requested by the user.

When creating, editing, reviewing, or validating a KiCad project in this repository, use the installed `kicad` skill. Read its `SKILL.md` before starting the KiCad work and follow its analysis and validation workflow.

Also use the installed supporting skills when their scope applies:

- `bom` for BOM creation or updates, component sourcing, distributor searches, BOM export, or fabrication preparation.
- `datasheets` when extracting or verifying component specifications from datasheets.
- `jlcpcb` or `pcbway` when preparing for the respective manufacturer's fabrication or assembly process.
- `digikey`, `mouser`, `lcsc`, or `element14` when sourcing parts from those distributors.
- `emc` for EMC/EMI risk reviews and pre-compliance planning.
- `spice` when simulating or validating analog subcircuits.

Installed skill files are available under `~/.codex/skills/<skill-name>/SKILL.md`. Select the relevant supporting skills for each task and read their instructions before using them. Do not claim DRC/ERC, simulation, sourcing, or manufacturing readiness without actually running the applicable checks and reporting their results.

## Web application and TypeScript workflow

- Keep `web/index.html` as the existing Mini 4WD console entry. Add new React screens through a separate entry point defined by the relevant feature specification.
- Before React work, read the applicable project skills under `.agents/skills/`, such as `react-best-practices`, `composition-patterns`, or `react-view-transitions`. Use `web-design-guidelines` for UI reviews and `react-native-skills` only for React Native or Expo work.
- Before TypeScript work, read the relevant skill under `.agents/skills/`: `typescript-project-setup`, `typescript-strict`, `typescript-build-references`, `typescript-publish-types`, `typescript-update`, or `typescript-report-issue`.
- Read `.agents/skills/electron/SKILL.md` when automating or testing an Electron application.
- Follow the applicable vehicle protocol contract and verify binary compatibility before connecting a new web UI to hardware. Do not treat JSON examples or placeholder components as a complete implementation.
