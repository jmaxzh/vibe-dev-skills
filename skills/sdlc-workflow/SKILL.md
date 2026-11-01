---
name: sdlc-workflow
description: Follow the software development lifecycle, initialize projects on request, and maintain the project knowledge base. Use only when the user explicitly invokes this skill.
license: MIT
---

# SDLC Workflow

## Workflow and capabilities

Intent → requirements → technical design → implementation.

- Once explicitly invoked, determine the required stages from the user's goal. Complete missing prerequisite work or revise prerequisite results that no longer apply, in requirements → technical design → implementation order and within the current task scope. Do not require a separate invocation for each stage.
- Reuse requirements, designs, and decisions still applicable in context and existing materials. Judge whether they support subsequent work; do not repeat work solely because no standalone document exists.
- When prerequisites are met, continue through completion of the stage requested by the user. Do not ask for confirmation at every stage or automatically continue into later stages. Handle critical ambiguity under the relevant stage's clarification rules and major tradeoffs under Delivery quality; pause only affected work.

Read and follow the reference for each stage actually performed:

- Intent → requirements: [requirements](references/intent-to-requirements.md).
- Technical design: [technical design](references/requirements-to-technical-design.md).
- Implementation: [implementation requirements](references/implementation.md).

The following independent, optional capabilities require explicit user requests; entering a main workflow stage must not trigger them automatically:

- Project initialization: [project initialization](references/project-initialization.md). Establish goals, scope, and a knowledge base before a minimal verifiable engineering skeleton.
- Knowledge-base review: [knowledge-base review](references/project-knowledge-base-review.md). Do not trigger it through routine knowledge-base reading or updates.

## General rules

### Applicability

- These general rules apply while executing this skill. Conversational answers are responses in chat; deliverables are code, documents, and other artifacts. Each section applies to the objects it names.

### Conversational answers

These rules govern chat responses. Document artifacts follow the installed Instruction and Documentation Design Principles under [Read on demand](#read-on-demand).

- Use project- or document-defined terms; otherwise use standard industry terms. Use one standard term per concept and one concept per term; clarify ambiguous meanings, boundaries, or conflicting definitions. Explain unfamiliar terms when needed for understanding.
- Express the intended meaning in standard terms. Make necessary actors, objects, prerequisites, constraints, and outcomes explicit; clarify references and the scope of negation.
- Organize explanations from the reader's existing knowledge in causal order: why, how, and with what result. Supply necessary background and bridge logical gaps with plain language and examples as needed.
- Preserve facts, complete meaning, tradeoffs, and uncertainty; distinguish possible from confirmed causes. Remove filler and repetition, retaining wording that is already clear and accurate.

### Delivery quality

- Prioritize correctness, completeness, and maintainability of the final deliverable, choosing a reasonable solution directly.
- Revise existing deliverables incrementally, retaining valid structure and information.
- For code, configuration, and other non-document artifacts, correct errors within scope; replace obsolete, conflicting, or superseded parts and remove duplicated or unrelated content. Document changes follow Instruction and Documentation Design Principles through the read-on-demand rules.
- Proceed within existing authorization with necessary changes to structure and responsibility boundaries. Ask the user only for decisions that exceed authorization, change requirements, or involve major tradeoffs requiring their judgment.
- Remove ineffective code, documents, configuration, and tests left by trial and error, misunderstandings, corrections, rollbacks, or abandoned approaches. Retain necessary historical records and verification evidence.

## Skill dependencies

- Document artifact work requires the installed `sdlc-instr-doc-design` skill. Resolve it through the runtime's skill catalog and load it with the available skill mechanism, using its actual registered name and namespace. Without a skill loader, read the entry and relevant resources at the discovered installed location. Do not assume a checkout path, user directory, or namespace.
- If the required skill or resource cannot be loaded, identify the missing dependency and pause only work requiring its rules. Continue independent work. Do not claim the rules were applied, silently skip them, or download/install dependencies automatically.
- Explain that the full Vibe Dev Skills plugin includes this dependency. For skills CLI installations, the minimum combination is `npx skills add jmaxzh/vibe-dev-skills --skill sdlc-workflow --skill sdlc-instr-doc-design`. Present this as installation guidance, not an instruction to run it without authorization.
- The UI, MySQL, and CC Connect skills retain their own applicability and activation rules; installing the suite does not activate every skill for every task.

## Read on demand

- When designing, writing, modifying, or reviewing document artifacts, resolve and follow the installed `sdlc-instr-doc-design` skill under [Skill dependencies](#skill-dependencies).
- For operational or troubleshooting answers, locate the installed `sdlc-instr-doc-design` resources under [Skill dependencies](#skill-dependencies) and read only the Operating instructions or Troubleshooting instructions section of its `references/document-design.md` as needed; do not activate its main workflow or full documentation rules.
- Read the user-designated project knowledge base as needed throughout. Determine its location under initialization rules during initialization; otherwise, if needed but unspecified, ask the user to designate it.
- When using a project knowledge base, read [project knowledge-base conventions](references/project-knowledge-base.md) and apply rules for the actual activity. Follow specific confirmation requirements before changing protected documents.
