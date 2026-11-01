# Project Knowledge-Base Conventions

## Document design and expression

- Follow the installed `sdlc-instr-doc-design` skill (see [dependency resolution](../SKILL.md#skill-dependencies)) when writing, modifying, or reviewing documents. These conventions add knowledge-base-specific organization, sources of truth, and maintenance requirements.

- Name code identifiers according to their programming language's conventions, with clear mappings to document terminology.
- Maintain standard definitions, code names, and necessary aliases in a glossary as needed. Give consistent brief explanations in content where useful; do not create separate definitions.
- When terminology differs, first distinguish name differences from conceptual differences, then correct documents and code within scope. Preserve necessary compatibility for public APIs, persisted fields, and external protocols, and state mappings.
- Identify readers by document purpose: product instructions for users, development and maintenance instructions for the corresponding maintainers. Organize operations around reader-executable tasks and observable outcomes; implementation details do not replace necessary steps.

## Document responsibilities

- Choose one Diátaxis type as each content page's primary responsibility. Retain brief background needed for it without mixing independent content of other types.

| Type | Orientation | Answers | Examples |
| --- | --- | --- | --- |
| **Tutorial** | Learning | How do I get started? | Onboarding, quick start |
| **How-to** | Tasks | How do I accomplish X? | Procedures, configuration guides |
| **Reference** | Information | What is X's exact specification? | API reference, configuration inventory |
| **Explanation** | Understanding | Why is it designed this way? | Current architecture, stable tradeoffs |

- Cross-link independent content of other types rather than embedding full tutorials, specifications, or explanations.
- Use arc42 only as needed for Explanations about architecture, current design principles, or stable tradeoffs.
- Use arc42 to organize individual architecture documents, not to determine document types, directory structure, or filenames.
- Select arc42 sections as needed: Introduction & Goals, Constraints, Scope, Solution Strategy, Building Block, Runtime, Deployment, Cross-cutting, Quality, Risks, Glossary.

## Naming

- Use `tutorial-`, `howto-`, `ref-`, and `expl-` for Tutorial, How-to, Reference, and Explanation respectively.
- Use `index.md` for navigation, exempt from type classification and filename prefixes.

## Directory design principles

- Divide directories by stable domains or functions, not as mirrors of code directories.
- Apply consistent criteria among peers; child directories refine parent scope.
- Group different document types for the same subject; distinguish types with filename prefixes.
- Give each subject one owner; maintain shared knowledge centrally and reference it.
- Split subtopics as needed; avoid empty directories and meaningless levels.
- Keep directories and navigation consistent; update references when paths change.

Use these examples as guidance and name by project semantics, not by copying the layout:

- A function with specifications, explanations, and procedures → group in `search/`, using `ref-`, `expl-`, and `howto-`.
- Authorization rules shared by functions → define in `authorization/`; each function references them and adds its own behavior.
- Growing `operations/` content → split stable subtopics such as `deployment/` and `backup/`, not `part-1/` or `part-2/`.

## Organization

- Read `index.md` first and use it to locate related documents.
- Keep each file focused on one subject.
- Keep each file within 500 nonblank lines.
- Keep each directory within 8 Markdown files, including `index.md`; split subdirectories when exceeded.
- Provide a domain overview, core navigation, and quick-start links in `index.md`, without embedding tutorials or details.
- Add a subject overview at the start of content pages as needed.
- If publication navigation configuration exists, use it as the sole source of publication hierarchy and visibility; update it and related indexes when adding pages. Otherwise use directory `index.md` navigation without creating extra configuration.
- Verify documented paths, commands, interfaces, configuration, and behavior at the relevant application's root in an applicable environment. For multi-application projects, choose the root of the application discussed.

## Formatting

- Add YAML frontmatter.
- Provide a nonempty `title`.
- Add `summary` and `read_when` as needed.
- Label fenced code blocks with a language.
- Prefer paragraphs and lists; simple Markdown tables suit comparisons, mappings, and parameter lists.
- Use single-level table headers and short cells, without long explanations, nested lists, or procedures.
- Use diagrams and screenshots as needed.
- Do not number headings.
- Use ordered lists only when sequence matters.

## Visual references

- Keep primary knowledge, rules, and constraints in Markdown. Images and standalone HTML are references; they do not independently define or change rules.
- Prefer images for static appearance, layouts, and visual comparisons; use standalone HTML for component states, responsiveness, and interaction demos. Visual references are optional; reuse valid existing materials first.
- Embed images or link HTML at the relevant location in the owning document, explaining purpose and necessary conditions. Text need not restate every visual detail.
- By default, standalone HTML should open locally without installation or build, with inline styles and necessary demo scripts; images may use relative paths.
- State demonstration scope; do not treat demos as implemented capability.
- When facts change, inspect and update affected references and links.

## Implementation status

- Mark only product capabilities and design solutions as `Planned` or `Implemented`.
- Place status below the relevant section heading; split sections mixing statuses.
- Include only approved, current plans needing long-term maintenance.
- Do not describe planned functionality as existing capability.
- Do not force implementation status onto terminology, conventions, or explanations of principles.

## Content boundaries

- Record only current, reusable knowledge with clear ownership and long-term value. Update existing authoritative documents first; create a page only for an independent subject that does not fit existing ones.
- Include facts fitting the document's purpose, subject, and responsibility; remove out-of-responsibility content even if correct.
- Use non-exhaustive examples for explanation, not as complete inventories.
- Extract current constraints, necessary rationale, and applicability from evidence by knowledge value, without excluding sources by type. Do not archive raw process materials or automatically create architecture decision records (ADRs) or historical copies. Handle existing archives within task scope; do not automatically delete them.
- Follow the Revision and review rules in the installed `sdlc-instr-doc-design` skill’s `references/document-design.md` (see [dependency resolution](../SKILL.md#skill-dependencies)) for content changes, cross-document rules, and necessary summaries. The following rules address factual responsibilities and derived content.
- Separate responsibilities of documentation, code, and dedicated contracts. Assign each fact one normative source: the document, code declaration, or dedicated contract that defines it.
- Define product requirements, user-observable behavior, public constraints, design intent, boundaries, invariants, and stable tradeoffs in documents.
- Document task goals, necessary operating paths, and usage of public APIs, commands, and configuration.
- Define exact interface, configuration, and data specifications in code declarations or dedicated contracts, including signatures, schemas, defaults, and full value ranges.
- Generate references from normative sources as needed, or provide necessary verifiable summaries with source links and non-exhaustive examples. Do not independently define or change specifications in derived content.
- When updating derived documentation, check consistency with normative sources. Update generated content through generation.
- Avoid enumerating volatile implementation details. Choose abstraction by purpose; explain component responsibilities, dependencies, key interactions, and mechanisms necessary for understanding, usage, or maintenance. Reference code or contracts for exact implementation.
- Cite official specifications for external protocols.
- Determine content ownership by purpose, subject, and factual responsibility, not code structure, internal names, or implementation enumerations.
- Do not mechanically update documents for code changes. Update affected documents when requirements, observable behavior, public contracts, or design constraints change. Correct errors, omissions, and maintenance problems within scope even when the system has not changed.
- Use behavior-preserving refactoring to detect implementation leakage: if only internals change and requirements, observable behavior, contracts, constraints, and documented facts remain the same, do not mechanically rewrite content. If it merely enumerates internals, remove, abstract, or replace it with source references according to responsibility. Still update obsolete paths, symbols, and locators; locator updates are not implementation leakage.

## Updates and rule changes

- Obtain user confirmation before knowledge-base updates outside implementation, unless explicitly requested already. For protected documents, follow the specific confirmation requirements under Human acceptance.
- Compare specification and implementation only when they describe the same fact. Report documentation deviations, implementation deviations, or rule conflicts against normative sources; do not automatically overwrite either side.
- Consult Git commits, diffs, and discussions as needed before changing long-term rules.
- Explain conflicts and impacts in the current chat. Ask only for missing necessary information or user decisions on rule tradeoffs; continue independent work.
- After confirmation, update affected rules, explanations, and references to current valid content without embedding discussion history.
- Mark uncertain matters when evidence is missing or conflicting. Do not guess or record unconfirmed conclusions.

## Human acceptance

- These rules take priority over conflicting update, cleanup, formatting, or automatic-fix rules in this skill.
- Inspect content, frontmatter, and related notes. Treat the entire document as protected when it declares completed human validation, such as "human-verified," "human acceptance passed," or "human-confirmed." Quotes or examples explaining this rule do not count, nor do pending or unconfirmed statements. If unclear, verify first and leave the document unchanged meanwhile.
- Before modifying, moving, renaming, or deleting a protected document, show concrete proposed changes and reasons, then wait for explicit user confirmation. Protection includes content, formatting, headings, and paths; do not remove protection markers yourself.
- Apply the same specific confirmation requirement to changes, moves, renames, or deletion of visual references affecting protected-document expression.
- General authorization to organize, review, or fix does not confirm specific changes.
- Execute only confirmed changes; submit additional changes for renewed confirmation.
- While awaiting confirmation, continue read-only review and independent work.

## Review entry points

- For wording, structure, or expression review only, use Instruction and Documentation Design Principles and applicable document conventions here, without a dedicated knowledge-base audit.
- Load [knowledge-base review](project-knowledge-base-review.md) for explicit audit, verification, or review of the knowledge base. Do not trigger it merely for knowledge extraction, filing suggestions, updates, or evidence reading.
