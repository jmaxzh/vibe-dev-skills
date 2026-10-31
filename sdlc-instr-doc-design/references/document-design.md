# Documentation Design Principles

Use these rules when designing, writing, modifying, or reviewing documents for understanding, operation, or troubleshooting. Follow the main skill's [shared expression rules](../SKILL.md#shared-expression-rules).

Apply operating and troubleshooting guidance only when writing those types of instructions; conceptual explanations need not use a step structure. Other skills may reuse just these sections for operational or troubleshooting answers without enabling the main skill or the full documentation rules.

## Content design

- Establish the document's purpose, subject, and intended use. Choose content and abstraction level for readers and their reasonable prior knowledge.
- Start from what readers know. Supply background, reasons, and key concepts necessary to understand the subject; do not omit explanations readers need merely because the model knows them.
- Explain processes and mechanisms in causal order: why they happen, how they work, and their outcomes. Bridge key logical gaps with plain language and concrete examples as needed.
- Distinguish facts, assumptions, and conclusions needing confirmation. Preserve necessary evidence, tradeoffs, and uncertainty; do not sacrifice completeness for brevity.
- Keep content that affects understanding or use; remove filler, ineffective embellishment, and repetition. Specify formats, lengths, and structures only where their purpose requires them.
- Use imperative sentences for operations, and descriptive sentences for background, principles, and facts. Do not force conceptual explanations into steps. For model instructions needing design or review, load the prompt reference through the main skill.

## Operating instructions

- Give each step one main action. Start with a clear action and name its object.
- Split sequential actions into ordered steps; retain simultaneous or inseparable actions within the same step.
- Put prerequisites, risks, and limits before the affected action. Use a separate prerequisites section when numerous conditions apply.
- Distinguish human actions from automatic system behavior; do not describe automatic behavior as a human step.
- For steps affecting subsequent actions, state expected results and conditions for continuing. Include verification when the overall outcome is not directly observable.

## Troubleshooting instructions

- Organize around the actual troubleshooting process, separating symptoms, checks, decision conditions, and recovery actions.
- Give each check decision criteria and corresponding next actions. Include recovery verification, stopping conditions, or escalation conditions as needed.

## Revision and review

- Retain accurate, clear, useful information. Correct, supplement, compress, or reorganize for actual needs; do not rewrite everything just to standardize wording.
- Remove obsolete or irrelevant content. When merging repeated explanations, retain information with distinct conditions, objects, or effects; check necessary background, causality, and evidence.
- When the same rule is maintained across documents, establish its maintenance location and reference it elsewhere. Retain necessary summaries consistent with the source and useful to current readers.
- Check completeness, explanation order, supporting evidence, and examples against document purpose and reader needs. Do not impose prompt-specific task decomposition or tool-use dimensions.
- Report issues within the main skill's review boundaries. Check knowledge-base content ownership, normative sources, implementation status, and maintenance permissions under the applicable knowledge-base conventions and review process.
