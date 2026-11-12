---
name: commit
description: Create a focused git commit using this repository's commit conventions. Use when the user asks to commit changes or invokes $commit; accepts --no-verify.
---

# Commit

Create a clean, focused commit using an emoji and Conventional Commit format.

## Language

- Communicate with the user in Japanese, including progress and any questions.
- Keep the commit message (`type`, subject, and body) in English.
- Preserve technical terms, command names, and file paths as written.

## Commit types

- ✨ `feat`: new feature
- 🐛 `fix`: bug fix
- 📝 `docs`: documentation changes
- ♻️ `refactor`: restructuring without behavior changes
- 🎨 `style`: formatting or visual-only changes
- ⚡️ `perf`: performance improvement
- ✅ `test`: add or fix tests
- 🧑‍💻 `chore`: tooling, configuration, or maintenance
- 🚧 `wip`: work in progress
- 🔥 `remove`: remove code or files
- 🚑 `hotfix`: urgent fix
- 🔒 `security`: security improvement

## Workflow

1. Inspect `git status` and the staged diff. Understand all existing staged and unstaged changes before acting.
2. If changes are already staged, commit only those staged changes. Do not stage unrelated or pre-existing unstaged changes.
3. If nothing is staged, identify the files that belong to this requested commit and stage only those. Never stage secrets such as `.env` files or credentials.
4. If changes have distinct purposes, explain the split and commit one coherent group at a time; do not combine unrelated work.
5. Unless the user supplied `--no-verify`, run the repository's applicable pre-commit checks (lint, build, and documentation generation when configured). If a check is unavailable or fails, report that and do not bypass it.
6. Choose the commit type from the diff. Add a scope when useful: `type(scope): description`.
7. Write a concise, imperative English subject that says what changed. Add a body for complex changes to explain why.
8. Do not add a co-authorship footer.
9. Commit the reviewed staged changes. Do not push unless explicitly asked.

Example:

```text
✨ feat(scope): add concise imperative summary

Optional body explaining why.
```

## Invocation arguments

- `$commit`: perform the workflow with pre-commit checks.
- `$commit --no-verify`: skip pre-commit checks only when the user explicitly supplied `--no-verify`.
