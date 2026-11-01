# Implementation Requirements

## Alignment

- Connect prerequisite stages under the [main workflow rules](../SKILL.md#workflow-and-capabilities). Implement applicable requirements, technical design, and acceptance plans.
- Follow this task's completion criteria. For newly discovered scenarios, assess relevance, regression impact, and safety risk first; do not automatically make them completion gates. Explain impacts and obtain necessary decisions if scope or user expectations must change.

## Inspect the current state

- Inspect existing tests affected by the change. Add tests only when necessary evidence protecting related existing behavior is missing.
- Reuse baseline evidence under Evidence reuse, running only missing or invalid necessary baseline tests. Distinguish target defects, other existing failures, and environment failures; record results.
- Stop affected work only when failure prevents safe implementation or assessment of new regressions. Explain why and continue unaffected work.

## Implementation and tests

- Test behavior and constraints the final system must support, including necessary regressions. Do not retain tests solely proving historical development operations or serving abandoned implementations. Test migration, installation, and upgrades as needed when they are supported system behavior.
- Validate high-rework risks early. For UI work, calibrate representative-page composition, shared styles, and key interactions before extensive state acceptance testing.
- Choose verification according to change nature, risk, and project conventions. Follow test-first implementation when the user or project requires test-driven development (TDD).
- For fixes, prioritize regression tests reproducing the target defect; when executable, first confirm the failure is caused by that defect. With TDD, confirm the red result reflects missing target behavior; investigate unexpected failures first.
- Implement requirements and run proportionate tests and required project checks. Run the full suite only when required, impacts are broad or cannot reliably be bounded, or evidence indicates wider effects.
- Set reverification scope by change impact. Reuse valid evidence under Evidence reuse, recording invalidated evidence and rerun reasons. Keep applicable project checks; explain rule conflicts and impacts instead of silently bypassing them.

## Evidence reuse

- Confirm no relevant changes to code, tests, configuration, dependencies, or operating conditions affect results; reuse valid testing and acceptance evidence first. A changed worktree path, checkout, stage, or candidate identifier alone does not invalidate evidence or justify a full rerun.
- One body of evidence may support multiple acceptance items; retain mappings between items and evidence.
- Rerun only for missing, invalid, insufficient, or contradictory evidence, or explicit user requests, prioritizing affected items. Expand when impacts cannot reliably be bounded, broader regressions emerge, or the user or project requires wider checks. Record reused evidence, reruns, and reasons.

## Acceptance

- Execute agreed acceptance scope in batches and record each item's result and evidence. Separate acceptance items do not justify repeating identical setup and tests. Completing one item does not finish the task; sampling must not replace agreed verification.
- Consolidate issues and fixes, then determine reverification under Evidence reuse. Handle a failure immediately only when it blocks subsequent work or evidence credibility; continue unaffected checks.
- Retry only with new facts, an evidence-based new method, changed environment, or a known transient fault with reasonable prospects of success. Otherwise stop repeating attempts. Record blockers, impacts, and unverified scope while continuing independent work. Stopping retries is not passing acceptance.
- Report implementation and acceptance status separately. Mark failed or unavailable acceptance honestly with reasons; do not claim success.
- If required items have not passed, explicitly report incomplete work with blockers and impacts; request necessary scope tradeoffs. Deliver promptly once code review, fixes, reverification, and other completion criteria are met; do not expand acceptance without grounds.

## Code review

### Preparation and assignments

- This section applies to implementation changes affecting behavior, such as code, configuration, and build scripts. Review documentation-only changes under the installed `sdlc-instr-doc-design` skill (see [dependency resolution](../SKILL.md#skill-dependencies)); apply each rule to the corresponding part of mixed changes.
- After implementation and tests and before delivery, the main agent organizes multiple subagents to review changes; do not skip for simple changes or PR status. Give reviewers the scope, baseline, applicable rules, and summary. Use PR context when present; otherwise review local diffs, including new untracked files.
- Use five independent reviewers for the following directions, without fixing their models. Run in batches if concurrency is limited. If subagents are unavailable, explicitly report blocked review; do not substitute main-agent self-review or claim completion.
  1. Project rules: check compliance with rules actually applicable to the change.
  2. Obvious defects: inspect changes for clear functional defects without unrelated context or minor details.
  3. Git history: use blame and history to identify newly introduced issues.
  4. Historical PRs: inspect still-applicable comments on related files for recurrence.
  5. Code comments: check whether changes violate applicable comments in modified files.
- If history is unavailable, record why and the uncovered scope while continuing other review. Missing material is not evidence of no issues. Do not repeat existing build, type, or similar checks solely for review; verify fixes under Implementation and tests and Evidence reuse.

### Issue verification

- For each candidate, reviewers provide location, trigger, impact, evidence, and reasoning. Rule-based issues must cite the specific applicable rule. Issues must result from this change; do not report untouched pre-existing defects as new ones.
- Exclude existing issues, style nitpicks, unsupported speculation, and expected behavior. Do not repeat problems explicitly covered by recorded valid compiler, type, lint, or other checks, while still addressing them under implementation requirements. Missing, incomplete, or failed checks do not justify exclusion. Generic quality suggestions are not defects; allowed, applicable exceptions are not violations.
- The main agent consolidates and deduplicates candidates and assigns each to a reviewer independent of its reporter, supplying the change, claim, and rules. The reviewer checks reality, causation, and specific rule applicability, scoring confidence from 0–100 with evidence using the following criteria. Retain only issues scoring at least 80.
- Confidence measures evidence that an issue is real and introduced by this change. Describe severity and frequency separately; do not use them to alter confidence.

| Score | Verification standard |
| --- | --- |
| 0 | Not credible: a simple check excludes it as a false positive or pre-existing issue. |
| 25 | Low confidence: initial clues exist but key judgments lack verifiable evidence. |
| 50 | Moderate confidence: partial evidence, with critical trigger, outcome, or causal links unverified. |
| 75 | High confidence: main evidence supports a real introduced issue, but unresolved doubts could change the conclusion. |
| 100 | Certain: direct evidence or reproduction confirms a real introduced issue and excludes key doubts; rule-based issues have a confirmed applicable, violated provision. |

### Fixes and delivery

- Fix independently verified issues scoring at least 80, determine necessary tests and reverification under Evidence reuse, and arrange subagent review of fix effectiveness and related regressions. Verify new candidates under the same criteria; do not restart a full review without grounds.
- For issues outside authorization or involving major tradeoffs, explain impacts and request necessary decisions instead of silently skipping them. If qualifying issues or necessary reverification remain, report incomplete work, not completion.
- Report conclusions, fix status, and unverified scope in this chat; do not automatically post PR comments. If none qualify, say "No issues met the reporting threshold," not that code has no issues. Provide precise files and lines; remote code links must use the actual repository, full commit SHA, and corresponding lines.

## Knowledge-base updates

- After implementation, update affected documentation under [project knowledge-base conventions](project-knowledge-base.md). Do not mechanically rewrite documents when only internal implementation changes and their facts remain valid. Update obsolete paths, symbols, and other locators.
