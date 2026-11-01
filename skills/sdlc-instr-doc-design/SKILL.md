---
name: sdlc-instr-doc-design
description: Design, write, revise, and review instructions, prompts, skills, and instructional or explanatory documents. Use for document artifacts, including knowledge-base documents, not ordinary conversational answers. Knowledge-base factual audits follow the applicable knowledge-base rules.
license: MIT
---

# Instruction and Documentation Design Principles

## Applicability

- Apply this skill to designing, writing, modifying, and reviewing instructions, prompts, skills, and document artifacts; not to ordinary conversational answers.
- Follow the target artifact's established domain rules, format, and maintenance permissions. Do not extend project- or knowledge-base-specific requirements to other artifacts.

## Shared expression rules

- Prefer terms already defined by the project or document; otherwise use established industry terms. Explain concepts that affect understanding as needed.
- Use one standard term per concept and one concept per term. Do not alternate synonyms merely to vary wording.
- Identify the intended meaning of original wording and express it in standard terms rather than copying it mechanically. Clarify meaning, scope, and distinctions when terms are ambiguous or definitions conflict.
- Remove ambiguous references, clarify the scope of negation, and distinguish possible from confirmed causes.
- Organize content logically, retaining factual accuracy and complete meaning. Do not lose necessary conditions, negation, or causal relationships through compression.

## Read by content purpose

- When designing or reviewing instructions, prompts, skills, or model execution rules within documents, read the [Prompt Design Guidelines](references/prompt-design.md).
- For documents that help readers understand, operate, or troubleshoot something, read the [Documentation Design Principles](references/document-design.md). Imperative wording or steps alone do not require loading the prompt reference.
- If a document also contains model instructions that need design or review, combine both references for the relevant content. Do not load all references by default.

## Working modes

Select a mode from the user's request: create for new artifacts; review only without changing target artifacts when only a review is requested; review and revise for changes to existing artifacts.

Before starting, establish the scope, document purpose, and applicable conventions, then load references by content purpose.

### Create

- Write the artifact for its goals, audience, and applicable conventions, checking content and expression against the relevant references.
- Check content completeness, explicit conditions and constraints, and consistency with related documents. Correct issues before delivery.

### Review only

- Organize the review appropriately for the task; document-by-document execution is not required.
- Report specific locations, problems, impacts, and revision suggestions. Distinguish confirmed issues, matters needing confirmation, and unverified scope.

### Review and revise

Work document by document. Related documents may be read in advance for context, but each document being changed must complete revision, comparison, and integration, and pass acceptance before changes begin on the next document. Do not revise multiple documents first and compare or integrate them afterward as a batch.

Before revising a document, preserve a retrievable original, identify actual issues, and set revision goals. Explain why documents needing no change are left unchanged.

1. **Revise**: address identified issues; leave content unchanged when no change is needed.
2. **Compare**: compare original and revised versions, explicitly assessing their strengths and weaknesses. Check retention of useful information, necessary explanations, conditions, constraints, and behavioral boundaries. Decide what to retain, restore, or adjust. Viewing a diff alone does not complete this step; reach specific conclusions.
3. **Integrate**: retain useful improvements and restore or integrate valuable original content omitted from the revision. Resolve conflicts according to document goals, facts, and applicable constraints. If no additional edit is needed, explicitly explain how original strengths were retained and why no adjustment is necessary. Do not skip this step.

After these steps, compare the integrated result with the original for acceptance. Finish the document if it meets the completion criteria. Otherwise, if a clear improvement is possible, revise again and repeat comparison, integration, and acceptance. If a satisfactory revision cannot be produced, restore the original and report unresolved issues and reasons.

Before moving to the next document, briefly record changes, comparison conclusions, integration decisions, and acceptance results. A progress update is sufficient; no separate report file is required. Record concrete findings, not just claims that comparison or integration occurred.

After all documents are complete, check cross-document consistency. Apply the same process to any documents requiring follow-up changes.

### Completion criteria and reporting

- New artifacts must meet task goals and applicable conventions. Revisions must solve target issues, retain valid original content, and introduce no omissions, ambiguity, contradictions, or redundancy.
- Removing content with evidence that it is wrong, obsolete, unrelated, or duplicated is not information loss.
- Briefly report major improvements, strengths retained or integrated through comparison, unresolved issues, and verification limits. Do not claim lossless revision for unverified content.

## Review boundaries

- Use the prompt reference's final checklist for prompt reviews and the documentation reference for reader-facing document reviews. Do not force prompt dimensions onto the latter.
- For knowledge-base expression reviews, select references by content purpose and follow target-document conventions; do not automatically expand into factual audits. For dedicated knowledge-base audits, follow the applicable knowledge-base rules for sources of truth, content ownership, implementation status, and cross-document consistency.
