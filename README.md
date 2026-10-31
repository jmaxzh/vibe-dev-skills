# Vibe Dev Skills

**Agent skills for the full software development lifecycle — from requirements and design to implementation, testing, and delivery.**

English | [简体中文](README.zh-CN.md)

Turn a Vibe Coding idea into clear requirements, a technical design, and an implementation with explicit verification. Vibe Dev Skills combines an SDLC workflow with focused skills for UI, MySQL, documentation, and messaging integrations.

The workflow reuses existing decisions and evidence, fills missing prerequisites, and continues through the stage you request. You can also use the specialist skills independently.

## Skills

| Skill | What it helps with | Activation |
| --- | --- | --- |
| [SDLC Workflow](sdlc-workflow/SKILL.md) | Requirements, technical design, implementation, testing, and knowledge-base maintenance | Explicit invocation; initialization and knowledge-base audits require separate requests |
| [UI and Interaction Design](sdlc-ui-interaction/SKILL.md) | Desktop, mobile, and web interface behavior and design | Applicable UI tasks |
| [MySQL Table and SQL Design](sdlc-mysql-design/SKILL.md) | Modeling, SQL, indexes, transactions, and concurrency | MySQL must be established as the target database |
| [Instruction and Documentation Design](sdlc-instr-doc-design/SKILL.md) | Prompts, skills, instructions, and reader-facing documentation | Document artifact work, not ordinary chat |
| [CC Connect Integration](cc-connect-integration/SKILL.md) | Messaging-to-local-agent deployment and maintenance, with optional Codex desktop copies | CC Connect integration tasks |

## Install

Use a coding agent that supports `SKILL.md` skills. The repository contains instructions and references, rather than a standalone application. Agent discovery and installation paths depend on your tool; use its documented skill directory.

1. Clone the repository outside your agent's auto-discovered skill directory:

   ```sh
   git clone https://github.com/jmaxzh/vibe-dev-skills.git
   cd vibe-dev-skills
   ```

2. Choose **one** instruction language. English is the default:

   ```sh
   skill_source_dir="."
   # For Simplified Chinese instead:
   # skill_source_dir="locales/zh-CN"
   ```

3. Set the destination to your tool's actual skill directory. Keep existing installations backed up before replacing them; the commands below stop if any of these skills already exists.

   ```sh
   skill_target_dir="/absolute/path/to/your/agent/skills"
   mkdir -p "$skill_target_dir"

   for skill_name in sdlc-workflow sdlc-ui-interaction sdlc-mysql-design sdlc-instr-doc-design cc-connect-integration; do
     if [ -e "$skill_target_dir/$skill_name" ] || [ -L "$skill_target_dir/$skill_name" ]; then
       echo "Skill already exists: $skill_target_dir/$skill_name" >&2
       exit 1
     fi
   done

   for skill_name in sdlc-workflow sdlc-ui-interaction sdlc-mysql-design sdlc-instr-doc-design cc-connect-integration; do
     cp -R "$skill_source_dir/$skill_name" "$skill_target_dir/"
   done
   ```

4. Reload skills according to your agent's instructions and verify that all five skill names are available.

Install the five sibling directories together to preserve cross-skill references. Do not install the whole repository recursively or both languages together: both editions use the same skill names. Include `references/` and CC Connect's `scripts/`, not just `SKILL.md`.

## Try it

Explicitly invoke the workflow using the syntax supported by your agent, or name the skill in your request:

> Use sdlc-workflow. I want to build a small issue tracker. Clarify requirements, design the solution, then implement it with appropriate tests. Reuse the project's existing decisions and stop at unresolved decisions that block dependent work.

For a bounded stage:

> Use sdlc-workflow to turn this feature idea into requirements and acceptance criteria. Stop before technical design.

For an independent specialist task:

> Review this MySQL order schema and stock-deduction SQL with sdlc-mysql-design. Explain integrity and concurrency risks, distinguishing project conventions from MySQL limitations.

For messaging integration:

> Use cc-connect-integration to inspect my existing CC Connect setup and plan the changes needed for my chosen messaging platform. Verify the messaging path before considering optional desktop mirroring.

These are example requests, not transcripts of completed deployments or benchmark results.

## Languages and maintenance

- Root skill directories contain the default English edition. [The Chinese edition](locales/zh-CN/) includes all five skills, references, and the same CC Connect scripts.
- Instruction language does not force the language of your conversations or deliverables; state your preference in your request.
- Keep corresponding translations aligned when changing behavior, conditions, examples, or links. Preserve skill names, configuration keys, and protocol identifiers across languages.
- For contributions to skills or documentation, follow [the maintenance rules](AGENTS.md) and the linked design principles.

## Boundaries

- Skills guide an agent; tool permissions, available integrations, and actual verification determine what it can accomplish. They do not themselves provide hosting, CI, or automatic deployment.
- MySQL rules include project-specific conventions, such as no queries inside explicit transactions, no foreign keys, no `CHECK`, and no stored procedures. Read the skill before adopting these conventions.
- CC Connect desktop mirroring is optional and view-only. Its bundled Codex adapter targets the documented legacy session format and IPC v11. The provided deployment path is macOS; compatibility and real messaging/desktop behavior require target-machine verification.
- CC Connect scripts retain the same behavior in both editions, including Chinese title-handling rules and test fixtures. Documentation translation does not change their runtime strings or add a runtime language selector.
