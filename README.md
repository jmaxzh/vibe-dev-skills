# Vibe Dev Skills

**Agent skills for the software development lifecycle — from requirements and design to implementation, testing, and delivery.**

English | [简体中文](README.zh-CN.md)

Turn a Vibe Coding idea into requirements, a technical design, and an implementation with explicit verification. The suite combines a development workflow with focused documentation, UI, MySQL, and CC Connect skills.

## Skills

| Skill | Purpose | Activation and dependencies |
| --- | --- | --- |
| [SDLC Workflow](skills/sdlc-workflow/SKILL.md) | Requirements, technical design, implementation, verification, and knowledge-base maintenance | Explicit invocation; document work requires `sdlc-instr-doc-design` |
| [Instruction and Documentation Design](skills/sdlc-instr-doc-design/SKILL.md) | Instructions, prompts, skills, and reader-facing documents | Artifact work; usable independently |
| [UI and Interaction Design](skills/sdlc-ui-interaction/SKILL.md) | Desktop, mobile, and web design and behavior | Applicable UI tasks |
| [MySQL Table and SQL Design](skills/sdlc-mysql-design/SKILL.md) | Models, SQL, indexes, transactions, and concurrency | MySQL must be established as the target database |
| [CC Connect Integration](skills/cc-connect-integration/SKILL.md) | Messaging-to-local-agent deployment and optional desktop copies | CC Connect integration tasks |

Install the complete suite by default. Installation does not activate all skills for every task. Initialization and dedicated knowledge-base audits still require explicit requests.

## Install

These GitHub commands require the distribution changes to be published to the repository. For an unpublished checkout, use its absolute path as the source; see [local verification and distribution](docs/distribution.md).

### Codex

```sh
codex plugin marketplace add jmaxzh/vibe-dev-skills
```

Install **Vibe Dev Skills** from the configured marketplace in the supported plugin UI. CLI versions providing `plugin add` also support:

```sh
codex plugin add vibe-dev-skills@vibe-dev-skills
```

### Claude Code

```sh
claude plugin marketplace add jmaxzh/vibe-dev-skills
claude plugin install vibe-dev-skills@vibe-dev-skills
```

### skills CLI

Install all five English skills and choose a supported agent:

```sh
npx skills add jmaxzh/vibe-dev-skills --skill '*'
```

The minimum complete workflow combination is:

```sh
npx skills add jmaxzh/vibe-dev-skills \
  --skill sdlc-workflow \
  --skill sdlc-instr-doc-design
```

The other four skills can be installed individually. Do not treat the workflow alone as a complete installation for document tasks. Each skill carries its own MIT notice.

### Manual installation

Copy the five directories inside `skills/` together into your agent's documented skill directory. Preserve `references/`, CC Connect's `scripts/`, and license files. Back up existing installations before replacement. Do not copy the repository root or maintenance translations into an automatically discovered skill directory.

## Use

Invoke the workflow using your agent's actual registered name or namespace:

> Use sdlc-workflow. Build a small issue tracker: clarify requirements, design the solution, then implement it with appropriate tests. Reuse existing decisions and pause only work blocked by unresolved decisions.

For a bounded stage:

> Use sdlc-workflow to turn this feature idea into requirements and acceptance criteria. Stop before technical design.

For a specialist task:

> Review this MySQL order schema and stock-deduction SQL with sdlc-mysql-design. Explain integrity and concurrency risks, distinguishing project conventions from MySQL limitations.

For integration work:

> Use cc-connect-integration to inspect my existing setup. Verify the messaging path before considering optional desktop mirroring.

When needed, the workflow loads the installed documentation skill using the runtime's actual name and namespace. Missing required resources pause dependent work; skills do not silently skip rules or install dependencies automatically. These examples are requests, not completed deployment transcripts.

## Languages and maintenance

English is the only installed instruction edition and the source of truth. [Chinese translations](translations/zh-CN/README.md) help developers understand and maintain the sources; they are not runtime skills. Instructions do not force the language of user conversations or deliverables.

Keep corresponding translations synchronized in the same change. Runtime scripts and tests have one implementation in their owning English skill. Follow [the maintenance rules](AGENTS.md).

## Distribution and license

Codex and Claude Code use the same five-skill plugin. skills.sh supports GitHub installation and discovery; SkillsMP indexes public source skills. See [distribution](docs/distribution.md) and [verification results](docs/verification.md).

[MIT](LICENSE). The owner confirmed that the adapted CC Connect mirror scripts may also be distributed under MIT; see [source and license notes](docs/provenance.md).

## Boundaries

- Skills guide an agent; permissions, integrations, and verification determine actual outcomes. They do not provide hosting, CI services, or automatic deployment themselves.
- MySQL rules include project conventions: no queries in explicit transactions, foreign keys, `CHECK`, or stored procedures. Read them before adoption.
- CC Connect mirroring is optional and view-only. Its bundled Codex adapter targets legacy sessions and IPC v11, with macOS service deployment. Real messaging, desktop rendering, login recovery, and compatibility require target-machine verification.
- Existing Chinese title handling and test fixtures remain part of the scripts. English skill instructions do not change runtime strings.
