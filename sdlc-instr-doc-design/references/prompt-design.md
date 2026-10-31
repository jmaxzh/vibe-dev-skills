# Prompt Design Guidelines

When designing, writing, modifying, or reviewing instructions, prompts, skills, or execution rules that constrain model behavior, use these principles together with the main skill's [shared expression rules](../SKILL.md#shared-expression-rules).

## General principles

1. Minimum sufficient instructions: retain only instructions affecting execution or results; avoid repetition, filler, and unnecessary constraints.
2. Explicit and actionable: use concise, clear imperatives; retain actors, conditions, operations, and outcomes necessary to understand the task.
3. Avoid repeating general knowledge: do not restate basic knowledge or capabilities the model already has, but retain task-specific constraints.
4. Load by need: general dimensions always apply; scenario-specific dimensions apply only when their activation conditions hold.
5. Clear boundaries: separate instructions from data; constrain evidence, permissions, and uncertainty only as required by the task.
6. Outcome-oriented: specify necessary results and constraints first; do not restrict processing steps without reason.

## General design dimensions

These dimensions apply to all prompts and help assess sufficiency. They do not require separate instructions for every dimension; do not add requirements already explicit in the task or context.

| Dimension | Recommended | Avoid | Reason and applicability |
| --- | --- | --- | --- |
| Task definition | Specify goals, objects, outcomes, and completion criteria as needed | Vague goals, unclear objects, unrelated background | Makes task and completion requirements understandable |
| Instruction clarity | Use concise, executable instructions with necessary actors, conditions, operations, and results | Ambiguity, missing conditions, non-operational wording | Reduces ambiguity and unnecessary inference |
| Instruction length | Use minimum sufficient instructions; retain conditions affecting execution or outcomes | Synonymous repetition, basic knowledge, generic admonitions, filler | Reduces redundancy and overconstraint without losing specific rules |
| Input organization | Separate instructions and content; use fields or separators when necessary | Mixing instructions with data or forcing structure onto simple input | Clarifies the processing object without meaningless structure |
| Output constraints | Specify required content and necessary format, length, or structure | Missing usage-critical requirements or unnecessary formatting constraints | Ensures usable results without gratuitous restrictions |

## Scenario-specific dimensions

Add instructions for these dimensions only when the scenario applies and existing wording does not express the requirement sufficiently.

| Dimension | Activation scenario | Recommended | Avoid |
| --- | --- | --- | --- |
| Task decomposition | Distinct stages or clear dependencies | Split necessary steps with goals and outcomes | Requiring stepwise execution indiscriminately |
| Instruction hierarchy | Different sources, priorities, or uses of instructions and materials | Clarify roles, priority, and applicability | Mixing instructions with data or letting lower-priority content override higher-priority rules |
| Reasoning guidance | A particular analytical method, reasoning framework, or verification process is required | Specify necessary analytical perspectives, methods, and verifiable outcomes | Universally requiring step-by-step reasoning or full internal chains of thought |
| Few-shot examples | Rules alone do not clarify classification boundaries, criteria, or output form | Use a few representative positive, negative, or boundary examples consistent with rules; explain their purpose | Repeated, irrelevant, contradictory examples, or incidental details becoming constraints |
| Evidence use | Designated sources, factual checks, or citations are required | Specify evidence scope, citation requirements, and source-conflict handling | Unsupported facts, fabricated evidence, or ignored conflicts |
| Exceptions and uncertainty | Missing information, invalid input, or source conflicts may affect results | Specify necessary exceptions, uncertainty responses, and requirements | Unconditional certainty or hypothetical exception rules without evidence |
| Tool-use instructions | External tools are allowed or required | Specify activation, purpose, use of results, and necessary confirmation | Fabricated results, guessed required parameters, or expanded permissions |
| Templates and parameters | Reuse, batch processing, or dynamic filling | Use meaningful variables; separate fixed instructions and variable data | Ambiguous placeholders or ad hoc data concatenation |
| Roles and audience | Professional responsibilities, audience, or register affect outcomes | Specify necessary responsibilities, audience, and expression requirements | Ineffective expert roleplay or lengthy identity descriptions |

## Instruction maintenance

Apply these principles when adding, revising, compressing, or removing prompt content.

| Operation | Principle |
| --- | --- |
| Add | Require an explicit task need, identifiable risk, or actual problem; prioritize missing conditions and boundaries |
| Revise | Remove ambiguity, contradiction, and unclear execution boundaries first; do not expand scope gratuitously |
| Compress | Remove repetition, filler, and basic-knowledge reminders; retain necessary information |
| Remove | Remove instructions with no effect on execution or outcomes; do not remove necessary constraints merely because the model knows them |
| Merge | Merge rules with the same applicability and expected behavior; retain independent rules with distinct conditions, objects, or effects |
| Retain | Keep instructions materially affecting correctness, evidence boundaries, permissions, or necessary exception handling |

## Final checklist

- Are the task goals, objects, and outcomes clear?
- Are there ambiguous, repetitive, generic, or unnecessary instructions?
- Is basic knowledge or capability unnecessarily repeated?
- Are necessary conditions, constraints, and behavioral boundaries retained?
- Are scenario-specific dimensions included only when needed?
- Are instructions, data, and examples clearly separated?
- Are examples representative, consistent, and free of accidental constraints?
- Are there unnecessary processing steps, formats, structures, or roles?

Core principle: use minimum sufficient instructions, explicit goals and necessary boundaries, and scenario-specific additions only as needed. Do not repeat general knowledge or add instructions for formal completeness.
