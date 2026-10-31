# Project Initialization

## Execution scope and order

- Initialize projects only on explicit user request.
- Within authorization, establish project goals and scope, then the knowledge base, then a minimal verifiable engineering skeleton.
- Read applicable conventions and existing materials. Reuse valid knowledge bases, foundations, stacks, architecture, and structure in existing projects; fill gaps and redesign only unsuitable parts.
- Reuse settled or confirmed information and check unresolved items individually. Organize questions by importance and difficulty, grouping related secondary matters; provide explanations so users can answer.
- Make routine technical, foundation, tool, and rule decisions within authorization. Follow main-skill confirmation rules for choices exceeding authorization, changing requirements, or involving major user tradeoffs.

## Establish project goals and scope

- Check project users, problems to solve, and expected outcomes individually.
- Check responsibilities, capabilities, covered scenarios, and exclusions individually.
- Extract goals and scope from existing requirements and materials; reuse explicit or confirmed information without asking again. Clarify unresolved matters under Execution scope and order. Do not skip remaining items because some have already been settled; cover all elements above.

## Establish the knowledge base

### Required content

- Follow [project knowledge-base conventions](project-knowledge-base.md).
- Include the following required content, grouped by subject rather than necessarily as separate documents:
  - Project goals and scope, checked individually; reuse explicit or confirmed user information.
  - Knowledge-base directory structure, subject divisions, ownership, and navigation.
  - Technology selection: purposes, reasons, and constraints of the foundation and selected technologies.
  - Static analysis tools and rules for each stack: coverage, rule principles, execution entry points, and configuration sources.
  - Project directory structure: ownership of source, tests, configuration, development tools, and generated output.
  - Architecture responsibilities and dependency boundaries: system context, major modules, dependency directions, and collaboration at a depth proportionate to complexity.
  - Licensing and third-party notices: summarize checking and notice-maintenance mechanisms and reference their actual engineering implementations.
- Retain valid existing documents. Handle other engineering needs without automatically expanding documentation topics; retain local deployment, necessary tests, builds, and skeleton verification.
- Record valid design and constraints in the knowledge base before implementing the skeleton.

### Knowledge-base directory structure

- Follow [directory design principles](project-knowledge-base.md#directory-design-principles) and [organization](project-knowledge-base.md#organization). Determine the root from user conventions and existing layout. If still unresolved, ask the user to designate it and continue independent preparation. Organize multi-product projects by independent product knowledge domains.
- Adapt this desktop-and-website example to the target project and required content:

```text
docs/                                           # Example knowledge-base root
├── index.md                                    # Navigation and organization
├── desktop/                                    # Desktop product knowledge
│   ├── ref-product-specification.md            # Goals and scope
│   ├── expl-technical-strategy.md              # Stack and architecture
│   ├── ref-product-interface-design-system.md  # Shared visual rules
│   ├── brand/identity/                         # Brand identity
│   │   └── ref-product-logo.md
│   ├── features/discovery/                     # Discovery feature
│   │   ├── ref-discovery.md
│   │   ├── expl-discovery-technical-design.md
│   │   └── howto-accept-github-sources.md
│   ├── platform/architecture/                  # Cross-feature constraints
│   │   └── ref-feature-boundaries.md
│   └── delivery/                              # Quality and delivery
│       ├── quality/
│       │   └── howto-run-quality-checks.md
│       └── release/
│           ├── ref-quality-and-release.md
│           └── ref-software-licensing.md
└── website/                                    # Website product knowledge
    ├── ref-product-specification.md
    ├── expl-technical-strategy.md
    └── delivery/release/
        └── howto-release-website.md
```

### Open-source foundation and technology selection

- Prefer mature open-source projects whose major capabilities or engineering structure can be reused, avoiding duplicate implementation.
- Verify requirement fit, maturity, stars, maintenance, reputation, adaptation costs, and license. Requirement fit and constraints come first; stars, activity, and reputation are supporting evidence, without universal numeric thresholds.
- Use a suitable foundation's stack with necessary adaptation. In existing projects, reuse choices meeting current goals first.
- If no suitable foundation or prescribed stack exists, evaluate defaults for the actual components: Tauri for desktop, React Native for mobile, React for frontend, Go for backend. Choose alternatives with reasons if defaults do not meet constraints.
- Verify compatibility, runtimes, toolchains, and supporting technologies against official documentation for selected versions.
- Document foundations, reused parts, technology purposes, reasons, constraints, and verifiable sources.

### UI conventions and brand identity

- For projects with UI, include shared interaction conventions and a visual design system. Reuse confirmed directions and conventions; clarify unresolved items individually under Execution scope and order.
- Add images or standalone HTML for UI and brand identity as needed under [visual references](project-knowledge-base.md#visual-references).
- When a design direction must be chosen, offer popular products with similar styles or leading products in the domain, or use user references. Verify reference applicability and explain differences through intuitive examples rather than asking users in specialist terminology.
- Organize applicable navigation, feedback, component, color, typography, and layout rules from settled references and direction.
- For public-facing or distributed projects, include brand and product identity conventions. Reuse valid confirmed names, marks, usage direction, and assets; clarify unresolved matters individually. Organize applicable logo, app-icon, and asset-use rules.

### Project directory structure

- Divide implementation boundaries by application or deliverable module, organizing internals by architectural responsibilities and dependencies.
- For multi-application projects, keep shared engineering declarations, governance, and orchestration at root; keep implementation and dedicated configuration/tools within each application. Keep single-application structures simple and conventional.
- Create shared modules only for actual shared responsibilities, with explicit ownership and dependency direction.
- Organize source, tests, configuration, and development tools by stack conventions; separate maintained files, builds, caches, and verification artifacts.
- Derive names and levels from the foundation and project, not fixed layering. Adapt this example by applications and responsibilities; explain boundaries in comments.

```text
project/                         # Partial multi-application example
├── package.json                 # Shared declarations and orchestration
├── docs/                        # Knowledge organized by subject
├── apps/                        # Application and engineering boundaries
│   ├── desktop/                 # Desktop product implementation
│   │   ├── src/                 # UI modules organized by responsibility
│   │   │   ├── app/             # Assembly and shell
│   │   │   ├── features/        # User-facing features
│   │   │   └── shared/          # Actual shared cross-feature capabilities
│   │   ├── crates/              # Product business core and CLI
│   │   ├── config/              # Application configuration
│   │   └── scripts/             # Application engineering tools
│   ├── website/                 # Independent website implementation
│   │   ├── app/                 # Framework-conventional page entries
│   │   └── src/                 # Website-owned modules
│   ├── service/                 # Independent backend implementation
│   │   ├── cmd/                 # Language-conventional service entry
│   │   ├── internal/            # Service internals
│   │   └── environments/        # Service runtime configuration
│   └── release/                 # Actual cross-application delivery, if needed
│       └── scripts/             # Shared delivery tools
├── target/                      # Conventional builds and caches
└── artifacts/                   # Design and verification, separate from source
```

### Static analysis

#### Coverage and gates

- Cover maintained source and relevant engineering configuration for actual stacks, reusing foundation rules. Static checks include formatting, syntax, types, analysis, and consistency of dependencies, documents, and declarations. Behavioral tests, coverage, and runtime race detection belong to testing and acceptance.
- Distinguish production, test, development-tool, and generated code. Define category-specific coverage and gates. Exclude generated code from maintained-code size metrics, but retain applicable compilation/type checks.
- Centralize shared rules per stack and adapt compilation environment, source scope, and architecture constraints through project configuration.
- Select tools, versions, rules, and exceptions independently. Specify checked objects, tools, measurement definitions, thresholds, comparisons, failure conditions, and configuration sources. Explain inapplicable items without omitting required applicable checks.
- Maintain exact rules and parameters in engineering configuration or check implementations; explain principles and link sources in the knowledge base.
- Provide a unified static-check entry point with necessary project selection, avoiding repeated shared steps. Require zero blocking violations and explicit warning and vulnerability policies.
- Return nonzero for blocking violations, missing or failed tools, invalid reports, or uncovered required source. Report project, step, and cause; do not call it passed.

#### Required checks

- Check formatting, syntax, compilation or types for actual languages and engineering configuration.
- Check unused code, exports, and dependencies; undeclared dependencies; unhandled errors; resource closure; and applicable language/framework rules.
- Check size, complexity, duplication, function signatures, and interface size; enforce circular/forbidden dependencies, deep imports, production-to-test dependencies, and implementation boundaries.
- Check secret leaks, dangerous patterns, production dependency vulnerabilities, licenses, and third-party notices. Retain required licenses and copyright notices for reused code. Generate or collect notices for distributed dependencies and summarize the mechanism in the knowledge base.
- Validate document formatting, navigation, links, workflow syntax, and consistency among lockfiles, workspaces, and toolchain declarations.
- Choose tools by stack; possible combinations:
  - Frontend: Prettier, ESLint, TypeScript, Stylelint, Knip, dependency-cruiser for formatting, language/framework rules, types, styles, unused/undeclared code and dependencies, and dependency boundaries respectively.
  - Rust: rustfmt and Clippy for formatting, static compilation checks, and language rules.
  - Go: gofmt, goimports, golangci-lint for formatting, imports, static analysis, error handling, and resource rules.
- Use suitable syntax-tree tools for necessary structural metrics not covered by language tools; do not parse functions or interfaces with regular expressions.

#### Quantitative metrics

- Set effective lines per file/function/package and direct files per directory. Exclude blank and comment-only lines; directory counts include direct files only and distinguish code categories.
- Set cyclomatic and cognitive complexity, statements, nesting depth, parameters, consecutive same-type parameters, and interface method counts according to language and module types. Define function scope, type recognition, and embedded-interface counting.
- Set duplication ratios and block sizes; define line/token measurement, denominator, and matching conditions. Distinguish minimum detected block size from the directly blocking threshold.
- Set repeated-string counts within the same directory and category, defining included strings and exclusions.
- Record blocking counts, warning policy, vulnerability gates, and coverage. Missing checks and failed checks are not passes.

#### Reference examples

- Adapt these example thresholds to the target stack, foundation, and constraints. A means production; B means tests/development tools. Values are A/B; retain their comparison operators.

```text
JS/TS: effective file lines ≤500/1500; function lines ≤120/360; direct files/directory ≤16/48
Rust: effective file lines ≤800/2400; function lines ≤120/360; direct files/directory ≤16/48
Go: effective file lines ≤600/1200; function lines ≤100/300; package lines ≤1800/5400

All three: cyclomatic complexity ≤15/20; cognitive complexity ≤24/39
Go: statements ≤60/180; nesting ≤4/6; parameters ≤5/8
Go: consecutive same-basic-type parameters ≤2/4; interface methods including embedded ≤8/12
Go: repeated-string occurrences in same directory/category <6/10

JS/TS, Rust: duplicated-line ratio ≤5%/10%; detection minimum 60 tokens and 10 lines
Go: duplicated-token ratio ≤5%/10%; blocks reaching 60/100 tokens fail
```

- Interpret values using each tool's measurement rules. Frontend file-size checks in this example also cover CSS; function and complexity metrics use the relevant syntax.
- In this example, Rust production files containing inline tests still use the A file limit of 800 lines; test functions use the B limit of 360 lines.
- These values illustrate metrics and gates only; exact project rules belong in engineering configuration or check implementations.

## Establish the engineering skeleton

### Engineering setup

- After establishing the knowledge base, create or complete minimal structure, dependency declarations, configuration, static-check entry points, and license/third-party-notice mechanisms under [implementation requirements](implementation.md). Reuse foundations within authorization and adapt as needed to verify the skeleton, without expanding into complete business functionality.

### Local services and third-party integration

- For backend projects, deploy locally with business functionality and public contracts equivalent to the target runtime. Infrastructure and deployment may differ to simplify local setup.
- Prefer actual third-party calls. Evaluate real integration first; use mocks only when local integration is extremely difficult, such as inability to receive server callbacks or a required virtual machine. Judge applicability independently.
- With mocks, retain applicable call contracts and explain simulated scope and behavior not actually verified. Mock success is not real integration success.
- Design local deployment for established requirements and constraints; do not invent production or release plans.

## Verification and delivery

- Prepare dependencies and toolchains for the stack and target platform. Run applicable static checks, necessary tests, and build or startup verification; configuration completion is not verification success.
- Correct knowledge-base paths, source references, and implementation statuses against actual setup and verification. Do not describe unbuilt mechanisms as implemented.
- Briefly report established components, entry points, outcomes, and unfinished scope. Do not automatically start a knowledge-base audit.
