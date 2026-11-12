# KiCad design workflow

## Language

- Respond to the user, provide progress updates, and explain plans, designs, reports, and summaries in Japanese by default.
- Keep technical terms, component part numbers, and standards in their accurate original forms where appropriate.

When creating, editing, reviewing, or validating a KiCad project in this repository, use the installed `kicad` skill. Read its `SKILL.md` before starting the KiCad work and follow its analysis and validation workflow.

Also use the installed supporting skills when their scope applies:

- `bom` for BOM creation or updates, component sourcing, distributor searches, BOM export, or fabrication preparation.
- `datasheets` when extracting or verifying component specifications from datasheets.
- `jlcpcb` or `pcbway` when preparing for the respective manufacturer's fabrication or assembly process.
- `digikey`, `mouser`, `lcsc`, or `element14` when sourcing parts from those distributors.
- `emc` for EMC/EMI risk reviews and pre-compliance planning.
- `spice` when simulating or validating analog subcircuits.

Installed skill files are available under `~/.codex/skills/<skill-name>/SKILL.md`. Select the relevant supporting skills for each task and read their instructions before using them. Do not claim DRC/ERC, simulation, sourcing, or manufacturing readiness without actually running the applicable checks and reporting their results.
