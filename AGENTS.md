# Skill maintenance rules

- When designing, writing, modifying, or reviewing this project's skills and related documentation, read and follow the [Instruction and Documentation Design Principles](skills/sdlc-instr-doc-design/SKILL.md).

## Language and sources

- `skills/` contains the only installable skill edition: English. English files define behavior and constraints. Do not add runtime language selection or translated `SKILL.md` discovery entries.
- Maintain `README.zh-CN.md` and `translations/zh-CN/` as Chinese developer translations only. Each translation must identify its English source. Use `SKILL.zh-CN.md` and `AGENTS.zh-CN.md` for translated entry documents.
- Update corresponding translations in the same change as English rules, conditions, examples, or references. Settle Chinese proposals in the English source first, then synchronize the translation; resolve discrepancies against English. Preserve identifiers, commands, configuration keys, and protocol names.
- Keep runtime scripts and their tests only in the owning English skill directory. Translate documentation, not executable code. This policy does not prescribe the language of user conversations or script output.

## Skill composition and distribution

- Maintain document and instruction design rules only in `sdlc-instr-doc-design`. Workflow document tasks resolve that installed skill through the runtime's actual skill name and namespace. Preserve section-only reuse for operational and troubleshooting guidance.
- If required dependency resources are unavailable, report the missing dependency and pause only dependent work. Do not silently bypass rules or automatically install skills.
- Recommend the five-skill suite. The supported minimum workflow combination includes `sdlc-workflow` and `sdlc-instr-doc-design`. Do not promise that installing only the workflow provides all document rules.
- Do not create shared-rule directories, generated rule copies, or a custom dependency installer. Plugin manifests are maintained directly and checked for identity/version/license consistency.
- Keep MIT notices in each skill for individual installation. Update fixed license copies together with the root license when necessary.
- Run `python3 -B scripts/validate.py`, distribution tests, and the existing CC Connect tests before delivery. Validate native manifests and installed inventories when the CLIs are available. Distinguish static checks, real local loading, model behavior, and target-machine deployment.
- Never infer permission to push, upload, submit for review, or publish from permission to prepare local changes or release packages.
