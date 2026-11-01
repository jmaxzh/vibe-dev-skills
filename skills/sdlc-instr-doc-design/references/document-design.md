# Documentation Design Principles

Use these rules when designing, writing, modifying, or reviewing documents for understanding, operation, or troubleshooting. Follow the main skill's [shared expression rules](../SKILL.md#shared-expression-rules).

Apply the operating and troubleshooting sections only to the corresponding content; conceptual explanations need not use a step structure. Other skills may reuse either section for operational or troubleshooting answers without activating the main skill or applying the remaining documentation rules.

## Content design

- Establish the document's purpose, subject, and intended use. Choose content and level of abstraction for the intended readers and their expected prior knowledge.
- Start from what readers know. Supply background, reasons, and key concepts necessary to understand the subject; do not omit explanations readers need merely because the model knows them.
- Explain processes and mechanisms in causal order: what causes them, how they work, and what results. Bridge key logical gaps; use plain language and concrete examples as needed.
- Distinguish facts, assumptions, and conclusions needing confirmation. Preserve necessary evidence, tradeoffs, and uncertainty; do not sacrifice completeness for brevity.
- Keep content that affects understanding or use; remove filler, unnecessary embellishment, and repetition. Specify format, length, and structure only when required by the document's intended use.
- Use imperative sentences for actions readers should take, and descriptive sentences for background, principles, and facts. When designing or reviewing model instructions within a document, load the prompt reference through the main skill.

## Operating instructions

- Give each step one main action. Start with a clear action and name its object.
- Present actions that must occur in sequence as ordered steps; keep simultaneous or inseparable actions in the same step.
- Before each affected action, state the prerequisites, risks, and limits readers need to know. Use a separate prerequisites section when numerous conditions apply.
- Distinguish human actions from automatic system behavior; describe automatic behavior as a system response rather than an action for the reader to perform.
- When a step's result determines what happens next, state the expected result and the conditions for continuing. Include verification when the overall outcome is not directly observable.

## Troubleshooting instructions

- Organize around the actual troubleshooting process, separating symptoms, checks, decision conditions, and recovery actions.
- For each check, state how to interpret the result and what to do next. Explain how to verify recovery and when to stop troubleshooting or escalate, as needed.

## Revision and review

- Retain accurate, clear, useful information. Correct, supplement, compress, or reorganize for actual needs; do not rewrite everything just to standardize wording.
- Remove obsolete or irrelevant content. When merging repeated explanations, retain information with distinct conditions, objects, or effects; check necessary background, causality, and evidence.
- When the same rule appears across documents, designate one document as its maintained source and reference it elsewhere. Retain necessary summaries that agree with the source and help readers of the current document.
- Check completeness, explanation order, supporting evidence, and examples against document purpose and reader needs. Do not impose prompt-specific task decomposition or tool-use dimensions.
- Report issues within the main skill's review boundaries. For knowledge-base documents, follow the applicable knowledge-base conventions and review process when checking content ownership, normative sources, implementation status, and maintenance permissions.
