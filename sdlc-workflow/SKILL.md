---
name: sdlc-workflow
description: Follow the software development lifecycle, initialize projects on request, and maintain the project knowledge base. Use only when the user explicitly invokes this skill.
---

# SDLC Workflow

## Workflow and capabilities

Intent → requirements → technical design → implementation.

- Once enabled, determine required stages from the user's goal. Fill missing or invalid prerequisites within the current task scope in requirements → technical design → implementation order, without requiring separate invocation for each stage.
- Reuse requirements, designs, and decisions still applicable in context and existing materials. Judge whether they support subsequent work; do not repeat work solely because no standalone document exists.
- When prerequisites are met, proceed continuously through the stage requested by the user. Do not ask for confirmation at every stage or automatically expand beyond it. Handle critical ambiguity under the relevant stage's clarification rules and major tradeoffs under Delivery quality; pause only affected work.

Read and follow the reference for each stage actually performed:

- Intent → requirements: [requirements](references/intent-to-requirements.md).
- Technical design: [technical design](references/requirements-to-technical-design.md).
- Implementation: [implementation requirements](references/implementation.md).

The following independent, optional capabilities require explicit user requests; entering a main workflow stage must not trigger them automatically:

- Project initialization: [project initialization](references/project-initialization.md). Establish goals, scope, and a knowledge base before a minimal verifiable engineering skeleton.
- Knowledge-base review: [knowledge-base review](references/project-knowledge-base-review.md). Do not trigger it through routine knowledge-base reading or updates.

## General rules

### Applicability

- These general rules govern conversational answers and deliverables produced while executing this skill. Deliverables mean code, documents, and other artifacts, excluding ordinary conversational answers. Each section applies to its stated objects.

### Terms and expression in answers

- This section and Explanation and communication govern conversational answers only. Document artifacts follow Instruction and Documentation Design Principles through the read-on-demand rules.

- Prefer project- or document-defined terms; otherwise use standard industry terms. Explain first-use terms when needed for understanding.
- Use one standard term per concept and one concept per term; do not rotate synonyms merely for variety.
- Identify the actual meaning of original wording and use standard expression rather than mechanically copying it.
- Clarify meaning, applicability, and distinctions where terms are ambiguous or definitions conflict.
- State necessary actors, objects, prerequisites, constraints, and expected results; remove ambiguity.
- Preserve factual accuracy, logical clarity, and complete meaning. Remove filler, repetition, and ineffective embellishment while retaining necessary background, causality, tradeoffs, and uncertainty.
- Organize logically, clarify negation, and distinguish possible from confirmed causes.
- Retain already clear, accurate, compliant wording. Revise only to correct issues, remove ambiguity, or adapt to requirements; avoid oversimplification.

### Explanation and communication

- Start from what readers know. Supply background, reasons, and key concepts needed to understand the topic; do not assume specialized prior knowledge beyond what is reasonable for the reader.
- Explain processes and mechanisms in causal order, bridging logical gaps: why this is so, how it happens, and the result. Use plain language and concrete examples, with detail proportionate to reader needs.

### Delivery quality

- Prioritize correctness, completeness, and maintainability of the final deliverable, choosing a reasonable solution directly.
- Revise existing deliverables incrementally, retaining valid structure and information.
- For code, configuration, and other non-document artifacts, correct errors within scope; replace obsolete, conflicting, or superseded parts and remove duplicated or unrelated content. Document changes follow Instruction and Documentation Design Principles through the read-on-demand rules.
- Proceed with necessary organization and responsibility changes within authorization. Ask only for choices exceeding authorization, changing requirements, or involving major tradeoffs requiring the user. Reuse existing authorization.
- Remove ineffective code, documents, configuration, and tests left by trial and error, misunderstandings, corrections, rollbacks, or abandoned approaches. Retain necessary historical records and verification evidence.

## Read on demand

- When designing, writing, modifying, or reviewing document artifacts, read and follow [Instruction and Documentation Design Principles](../sdlc-instr-doc-design/SKILL.md).
- For operational or troubleshooting answers, reuse only the [operating instructions](../sdlc-instr-doc-design/references/document-design.md#operating-instructions) or [troubleshooting instructions](../sdlc-instr-doc-design/references/document-design.md#troubleshooting-instructions) sections as needed; do not enable the main skill or full documentation rules.
- Read the user-designated project knowledge base as needed throughout. Determine its location under initialization rules during initialization; otherwise, if needed but unspecified, ask the user to designate it.
- When using a project knowledge base, read [project knowledge-base conventions](references/project-knowledge-base.md) and apply rules for the actual activity. Follow specific confirmation requirements before changing protected documents.
