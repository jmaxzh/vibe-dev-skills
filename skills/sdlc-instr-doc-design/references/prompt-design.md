# Prompt Design Guidelines

When designing, writing, modifying, or reviewing instructions, prompts, skills, or execution rules that constrain model behavior, use these principles together with the main skill's [shared expression rules](../SKILL.md#shared-expression-rules).

## General principles

1. Minimum sufficient instructions: retain only instructions affecting execution or results; avoid repetition, filler, and unnecessary constraints.
2. Explicit and actionable: state required behavior clearly and concisely; identify the actors, objects, conditions, actions, and outcomes needed to carry out the task.
3. Avoid repeating general knowledge: do not restate basic knowledge or capabilities the model already has, but retain task-specific constraints.
4. Select dimensions as needed: assess every prompt against the general dimensions; apply scenario-specific dimensions only when their activation conditions hold.
5. Clear boundaries: separate instructions from data; specify evidence requirements, permissions, and handling of uncertainty only as required by the task.
6. Outcome-oriented: specify expected results, necessary constraints, and completion criteria.
7. Context, not Control: provide goals, relevant context, reasons for constraints, tradeoffs, and acceptance criteria so the model can choose appropriate methods. Prescribe steps, order, formats, or roles only when task dependencies, interface requirements, or identified risks justify them, or when the user or higher-priority instructions explicitly require them.

Concept references: [Netflix: Context, not Control](https://www.jobs.netflix.com/culture); [ByteDance: Context over Control](https://www.bytedance.com/about).

## General design dimensions

Use these dimensions to assess whether a prompt provides sufficient guidance. They do not require a separate instruction for each dimension; do not repeat requirements already explicit in the task or context.

| Dimension | Recommended | Avoid | Reason and applicability |
| --- | --- | --- | --- |
| Task definition | Specify goals, objects, outcomes, and completion criteria, with context and tradeoffs needed for judgment | Vague goals, unclear objects, missing decision context, unrelated background | Supports informed method choices and makes completion requirements understandable |
| Instruction clarity | Use concise, actionable instructions identifying necessary actors, objects, conditions, actions, and results | Ambiguity, missing conditions, requirements that do not guide action | Reduces ambiguity and unnecessary inference |
| Instruction length | Use minimum sufficient instructions; retain conditions affecting execution or outcomes | Repeating the same rule in different words, restating basic knowledge, generic admonitions, filler | Reduces redundancy and unnecessary constraints without losing specific rules |
| Input organization | Separate task instructions from the content to process; use fields or separators when necessary | Mixing instructions with data or imposing unnecessary structure on simple input | Makes clear what to process without unnecessary structure |
| Output constraints | Specify required content; constrain format, length, or structure only as needed for use | Omitting requirements that affect usability or adding unnecessary formatting constraints | Ensures usable results without unnecessary restrictions |

## Scenario-specific dimensions

Add instructions for these dimensions only when the activation scenario applies and the existing prompt does not adequately express the requirement.

| Dimension | Activation scenario | Recommended | Avoid |
| --- | --- | --- | --- |
| Task decomposition | Dependencies, interface requirements, or identified risks require distinct stages | Specify necessary stages and their purpose, dependencies, and outcomes; leave other method choices open | Prescribing execution order without a concrete need |
| Instruction hierarchy | Different sources, priorities, or uses of instructions and materials | Clarify roles, priority, and applicability | Mixing instructions with data or letting lower-priority content override higher-priority rules |
| Reasoning guidance | A particular analytical method, reasoning framework, or verification process is required | Specify necessary analytical perspectives, methods, and verifiable outcomes | Universally requiring step-by-step reasoning or full internal chains of thought |
| Few-shot examples | Rules alone do not clarify classification boundaries, criteria, or output form | Use a few representative positive, negative, or boundary examples consistent with rules; explain their purpose | Repeated, irrelevant, contradictory examples, or incidental details becoming constraints |
| Evidence use | Designated sources, factual checks, or citations are required | Specify evidence scope, citation requirements, and source-conflict handling | Unsupported facts, fabricated evidence, or ignored conflicts |
| Exceptions and uncertainty | Missing information, invalid input, or source conflicts may affect results | Specify how to handle relevant exceptions and respond when information is uncertain | Requiring certainty in all cases or adding exception rules without a concrete basis |
| Tool-use instructions | External tools are allowed or required | Specify when and why to use tools, how to use their results, and when confirmation is required | Fabricated results, guessed required parameters, or expanded permissions |
| Templates and parameters | Reuse, batch processing, or dynamic filling | Use meaningful variables; separate fixed instructions and variable data | Ambiguous placeholders or ad hoc data concatenation |
| Roles and audience | Professional responsibilities, audience, or register affect outcomes | Specify necessary responsibilities, audience, and expression requirements | Ineffective expert roleplay or lengthy identity descriptions |

## Instruction maintenance

Apply these principles when adding, revising, compressing, or removing prompt content, including this skill and its references when they are the revision target.

Assess both existing and proposed requirements for steps, order, formats, or roles. Identify the task need each requirement serves, then consider whether decision context and acceptance criteria would achieve the same goal while leaving method choices open. Retain requirements with a concrete justification; replace unnecessary process controls with the context and outcome requirements needed for judgment. Do not invent a justification merely to retain an existing rule.

Preserve procedures that govern the current task when explicitly required by the user or higher-priority instructions. A procedure in the text being revised is still subject to review; retain it only when justified or required for the revised artifact.

| Operation | Principle |
| --- | --- |
| Add | Require an explicit task need, identifiable risk, or actual problem; prioritize missing conditions and boundaries |
| Revise | Resolve ambiguity, contradiction, and unclear execution boundaries; replace unnecessary process controls with context for decisions and outcome requirements without unnecessarily expanding scope |
| Compress | Remove repetition, filler, and basic-knowledge reminders; retain necessary information |
| Remove | Remove instructions with no effect on execution or outcomes; do not remove necessary constraints merely because the model knows them |
| Merge | Merge rules with the same applicability and expected behavior; retain independent rules with distinct conditions, objects, or effects |
| Retain | Keep instructions materially affecting correctness, evidence boundaries, permissions, or necessary exception handling |

## Validation scope

Use textual review to assess whether the instructions support the intended goals and preserve necessary boundaries. Revisions must address unnecessary process controls alongside wording issues; remaining controls need a concrete justification or an explicit user or higher-priority requirement. If the wording leaves uncertainty, walk through representative scenarios: can unnecessary process controls be removed while necessary constraints and explicitly required procedures remain intact?

Actual model execution and before-and-after evaluations are not default completion requirements; perform them only when the user explicitly requests them. An unavailable runtime environment does not block textual revision and review. Distinguish textual findings, scenario-based inferences, file or loading checks, and any observed runtime results. Do not present inferred effects as verified runtime behavior or generalize beyond the evidence.

## Final checklist

- Are the task goals, objects, and outcomes clear?
- Are there ambiguous, repetitive, generic, or unnecessary instructions?
- Is basic knowledge or capability unnecessarily repeated?
- Are necessary conditions, constraints, and behavioral boundaries retained?
- Are scenario-specific dimensions included only when needed?
- Are instructions, data, and examples clearly separated?
- Are examples representative, consistent, and free of accidental constraints?
- Is there enough relevant context to choose methods and assess tradeoffs without unnecessary background?
- Does each prescribed step, format, structure, or role serve a concrete task need, or could context and outcome requirements replace it?
- Do conclusions stay within the evidence from review, scenario walkthroughs, or any requested runtime evaluation?

Core principle: use minimum sufficient instructions, decision-relevant context, explicit goals and necessary boundaries, and scenario-specific additions only as needed. Do not repeat general knowledge or add instructions for formal completeness.
