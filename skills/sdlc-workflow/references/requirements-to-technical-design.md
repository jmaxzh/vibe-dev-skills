# Technical Design from Requirements

## Task and evidence boundaries

- Connect to the requirements stage under the [main workflow rules](../SKILL.md#workflow-and-capabilities). Establish goals, scope, non-goals, constraints, and unresolved choices; design to the depth and scope requested.
- Respect the user's permitted evidence scope throughout. Reuse applicable facts and investigate only missing or conflicting information affecting conclusions. If code inspection is forbidden, do not read code. Describe module-level changes and impacts without asserting exact file changes, existing implementation gaps, or precise effort.

## Feasibility and unresolved matters

- Assess whether goals can be fully achieved under necessary conditions and constraints. Distinguish fundamental impossibility, conflicting constraints, technical feasibility at excessive cost, and insufficient evidence. Complexity does not imply impossibility; insufficient evidence establishes neither feasibility nor infeasibility. State guarantees and failure boundaries; do not make conditional guarantees absolute.
- Check requirement rules, dependencies, permissions, environment, and compatibility strategy as needed. Distinguish design blockers, implementation prerequisites, and issues solvable by design. Do not require all implementation details in advance; make routine interface and module decisions independently.
- Proceed when facts, contracts, and user decisions support reasonable inference. For critical gaps, explain missing information, impact, and decision owner, then ask necessary questions. Seek confirmation for tradeoffs exceeding authorization, changing requirements, or carrying major costs. Reuse existing confirmation; data models or architecture boundaries alone do not warrant another request.
- If full implementation is infeasible or conflicts exist, explain evidence, affected goals, options, and costs. Mark unsupported judgments as uncertain. Keep choices needing confirmation unresolved until confirmed; do not implement or describe them as settled. Pause only dependent work. If the entire design is blocked, deliver causes, options, and next steps.

## Design evidence and reuse

- Prefer applicable existing project designs, then mature solutions for the same scenario and stack, then mature solutions for the same scenario across stacks. Judge maturity by actual use, verifiable implementation, and explicit boundaries, not stars as a proxy for suitability. Stop broadening searches when key decisions have sufficient evidence.
- First inspect responsibilities, semantics, dependency directions, and constraints of existing abstractions, modules, interfaces, and extension points. Reuse suitable capabilities and project style. If insufficient, assess external solutions against scenarios, constraints, and dependencies; reuse suitable parts with necessary adaptation, designing only missing parts. Avoid mixed responsibilities, inverted dependencies, or unnecessary abstractions for reuse.
- Verify APIs, configuration, runtime behavior, and stack conventions against official documentation for the relevant version regardless of the above reference priority. Cite original sources and do not invent technical facts. Across stacks, extract only domain models, boundaries, and tradeoffs that remain valid.
- Explain gaps, tradeoffs, reused parts, and necessary differences for key new or replacement decisions, linking project files, symbols, commits, or external primary sources. Include rejected options only when relevant to user judgment. Label unverified designs with assumptions and verification methods.

## Responsibilities, flows, and data

- Identify existing architecture, responsibilities, and dependencies. Retain reasonable layering and choose patterns for actual responsibilities and constraints, not directory names or a fixed layer count. Decouple business rules from UI, storage, and other implementation choices. Make ownership of interface contracts, events, and state explicit; do not assign them all to the data layer by default.
- Introduce abstractions and modules only for current responsibility boundaries, business invariants, dependency isolation, or verification. Usage count alone does not determine necessity; hypothetical future needs do not justify structure. Use a suitable existing module when no independent boundary is needed; otherwise use the smallest sufficient module design.
- Describe module responsibilities, inputs, outputs, interfaces, and dependencies. Remove duplicate responsibilities or clarify boundaries and inspect implicit coupling. Keep modules at comparable granularity in a design view; do not list a whole module alongside another's internal details.
- Inspect affected data structures, state, ownership, invariants, and read/write paths; identify additions and changes, designing consistency, concurrency, indexes, and capacity as needed. Cross-check key flows, data structures, contracts, module boundaries, and lifecycles for necessary data and constraint support. Without persistence changes, still inspect in-memory state, request/response, and message structures as needed.
- For conversion or dispatch across types, states, or events, check consumer coverage and semantics against applicable contracts and existing data. Existing branches, current configuration, or test samples do not define the entire contract.
- When contracts or existing data are affected, follow confirmed compatibility strategy and design compatibility, migration, and rollback measures for actual impacts. If strategy is missing, infer from contracts and user goals without arbitrarily dropping compatibility. If inference is unsafe, or costs or constraints change materially, follow Feasibility and unresolved matters and offer suitable compatibility or migration options and costs.

## Fix and change scope

- Design changes at the responsible boundary or core abstraction. Follow fix goals and change constraints in [intent → requirements](intent-to-requirements.md), defaulting to root-cause elimination without unrelated work. If an existing abstraction is wrong, explain user impact, cause, smallest correct change, and migration cost.
- If patching only the failure trigger retains a confirmed source of similar defects, include necessary contract, responsibility, or verification changes. Limit investigation to related call chains and shared contracts.
- For explicit urgent mitigation, or known time limits insufficient for root-cause repair and validation, prioritize local patches, isolation, or adaptation with limited change and impact scope. State affected and essential preserved behavior, remaining issues, rollback, and root-cause follow-up. Do not describe a workaround as eliminating the cause.

## Verification and delivery

- Define verification methods and criteria for key behavior and confirmed defect risks. Derive scope from requirements and contracts, not implementation alone; conditions must trigger the behavior tested. Explain how contract inconsistencies or missing branches will be detected when relevant. Reuse existing evidence; design work alone does not require running all tests. Do not describe proposed checks as passed.
- By default, deliver feasibility and prerequisites, the core approach, necessary changes, impacts, key verification, and unresolved matters. Distinguish implementation blockers, conditions to meet during implementation, and nonblocking assumptions. Explain module collaboration and key flows by responsibility, with change objects, reasons, scope, behavior, data, compatibility, and major costs. Include only what affects user judgment.
- Expand detailed design on request, rather than defaulting to field inventories, interface signatures, state machines, or section-by-section output. Separate analysis depth from delivery length; retain necessary investigation and boundary analysis without recounting all searches or repeating arguments.
