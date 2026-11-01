# Intent to Requirements

## Scope and scenario analysis

- Reuse applicable facts, goals, constraints, and decisions in context. Consult and verify related information as needed.
- Apply mutation (变异): vary relevant attributes, states, relationships, and conditions of the concepts and objects involved to examine representative scenarios. Identify common requirements and boundaries beyond a single instance. Match mutation depth to complexity, impact, and risk; stay within user goals and task scope. Distinguish known facts from hypothetical scenarios; do not turn unsupported variants into new requirements.

## Requirements contract

- Write for stakeholders. Retain internal terminology and technical identifiers only when needed to understand requirements.
- Describe desired outcomes and their value, including users and scenarios as needed. Do not substitute unconfirmed implementation methods for goals or rewrite behavior requirements as implementation tasks. Select necessary elements for the scope: business objects, actors, triggers, rules, boundaries and exceptions, non-goals, constraints, dependencies, and impacts on existing behavior. State necessary quantitative criteria.
- Apply divide and conquer (分治) to requirements: decompose them by subgoal or business responsibility around the overall goal, defining boundaries and relationships. Organize the primary goal-achieving flow as the main flow (主线), with alternatives, exceptions, and boundary scenarios as branch flows (支线). Explain each branch flow's triggers and relationship to the main flow. Keep simple requirements concise without forced hierarchy. Requirements decomposition does not replace subsequent implementation task decomposition.
- Separate the requirements contract from implementation details: the contract is behavior and constraints promised to users or dependents; implementation details are internal ways to fulfill it. Retain interfaces, fields, parameters, configuration keys, and identifiers necessary to express the contract. Put paths, commits, line numbers, and other evidence locators in source notes linked to the relevant requirement.
- Retain user-specified or confirmed technical constraints and identify their sources. Do not promote candidate implementation details into constraints. Verify known constraints affecting feasibility and identify conflicts; mark matters requiring design or experimentation as needing assessment. Leave implementation choices and detailed technical reasoning to technical design, and task decomposition to later stages.

## Uncertainty and compatibility

- Identify conflicts with existing requirements, behavior, and constraints. Address missing information, conflicts, and unresolved choices affecting requirements. If critical ambiguity cannot be resolved from available context, consolidate necessary questions and continue unaffected work. For conflicts and product decisions not derivable from existing evidence, explain evidence, options, tradeoffs, impacts, and costs. Do not pass unresolved matters to later stages as settled requirements.
- When iterating existing functionality, establish existing behavior, applicable contracts, and impacts on current users or data. Derive compatibility scope and migration goals from contracts and user goals, flagging critical ambiguity. If evidence shows significant compatibility costs, explain evidence, options, and effects on contracts, current users, and migration, and mark the choice as unresolved. If costs or impacts cannot yet be judged, mark them for technical design assessment. Handle critical gaps in behavior, contracts, or compatibility scope under the clarification rules in this section. Do not presume either compatibility or a breaking change.
- For server changes that materially affect capacity, performance, or cost, obtain only metrics that change requirement boundaries or acceptance criteria. Select existing and expected data scale, growth, average and peak traffic, concurrency, or read/write frequency as needed. Identify sources and conditions. If unavailable, explain gaps and impacts: if blocking requirements, request an estimate or decision on assumptions; otherwise record uncertainty and proceed. Do not design capacity solutions in the requirements stage.

## Defect-fix strategy

- Follow explicit user strategy, goals, time constraints, and acceptable risk first. Surface tradeoffs if incompatible; do not silently change explicit requirements.
- Without an explicit strategy, default to eliminating the root cause. Avoid unrelated changes, but do not retain a known cause merely to minimize the diff. If known time limits cannot accommodate a root-cause fix and necessary verification, prioritize mitigation.
- For mitigation, restore affected functionality, limit change and impact scope, and preserve other existing behavior. Record remaining causes and follow-up root-cause work.

## Completion and delivery

- Before delivering requirements, check that each has criteria for determining whether it is satisfied. Fill gaps supported by evidence; flag for confirmation any gap that prevents this judgment and cannot reasonably be resolved by inference.
- Deliver requirements with necessary elements and acceptance criteria. Explain impacts and blocked scope of unresolved decisions or matters needing assessment.
