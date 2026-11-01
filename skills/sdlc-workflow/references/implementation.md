# Implementation Requirements

## Alignment

- Connect prerequisite stages under the [main workflow rules](../SKILL.md#workflow-and-capabilities). Implement applicable requirements, technical design, and acceptance plans.
- Follow this task's completion criteria. For newly discovered scenarios, assess relevance, regression impact, and safety risk first; do not automatically make them completion gates. Explain impacts and obtain necessary decisions if scope or user expectations must change.

## Inspect the current state

- Inspect existing tests affected by the change. Add tests only when necessary evidence protecting related existing behavior is missing.
- Reuse baseline evidence under Evidence reuse, running only missing or invalid necessary baseline tests. Distinguish target defects, other existing failures, and environment failures; record results.
- Pause affected work only when a test or environment failure prevents safe implementation or assessment of newly introduced regressions. Explain the blocker and continue unaffected work.

## Implementation and tests

- Test behavior and constraints the final system must support, including necessary regressions. Do not retain tests solely proving historical development operations or serving abandoned implementations. Test migration, installation, and upgrades as needed when they are supported system behavior.
- Validate high-rework risks early. For UI work, calibrate representative-page composition, shared styles, and key interactions before extensive state acceptance testing.
- Choose verification according to change nature, risk, and project conventions. Follow test-first implementation when the user or project requires test-driven development (TDD).
- For fixes, prioritize regression tests reproducing the target defect; when the tests can be run, first confirm they fail because of that defect. With TDD, confirm the initial test failure reflects missing target behavior; investigate unexpected failures first.
- Implement requirements and run proportionate tests and required project checks. Run the full suite only when required, impacts are broad or cannot reliably be bounded, or evidence indicates wider effects.
- Set reverification scope by change impact. Reuse valid evidence under Evidence reuse, recording invalidated evidence and rerun reasons. Keep applicable project checks; explain rule conflicts and impacts instead of silently bypassing them.

## Evidence reuse

- Before reusing testing or acceptance evidence, confirm that changes to relevant code, tests, configuration, dependencies, or operating conditions have not invalidated it. Prefer reuse when evidence remains valid. A changed worktree path, checkout, stage, or candidate identifier alone does not invalidate evidence or justify a full rerun.
- One body of evidence may support multiple acceptance items; retain mappings between items and evidence.
- Rerun only for missing, invalid, insufficient, or contradictory evidence, or explicit user requests, prioritizing affected items. Expand when impacts cannot reliably be bounded, broader regressions emerge, or the user or project requires wider checks. Record reused evidence, reruns, and reasons.

## Acceptance

- Complete the agreed acceptance scope and record each item's result and evidence. Group checks when they share setup or evidence. Separate acceptance items do not justify repeating identical setup and tests. Completing one item does not finish the task; sampling must not replace agreed verification.
- Prioritize fixes by impact, dependencies, and shared causes, then determine reverification under Evidence reuse. Address failures that block subsequent work or undermine evidence credibility promptly; continue unaffected checks.
- Retry only with new facts, an evidence-based new method, changed environment, or a known transient fault with reasonable prospects of success. Otherwise stop repeating attempts. Record blockers, impacts, and unverified scope while continuing independent work. Stopping retries is not passing acceptance.
- Report implementation and acceptance status separately. Mark failed or unavailable acceptance honestly with reasons; do not claim success.
- If required items have not passed, explicitly report incomplete work with blockers and impacts; request necessary scope tradeoffs. Deliver promptly once code review, fixes, reverification, and other completion criteria are met; do not expand acceptance without grounds.

## Code review

### Preparation and assignments

- This section applies to implementation changes affecting behavior, such as code, configuration, and build scripts. Review documentation-only changes under the installed `sdlc-instr-doc-design` skill (see [dependency resolution](../SKILL.md#skill-dependencies)); apply each rule to the corresponding part of mixed changes.
- Before delivery, review the implementation changes, including new untracked files, against the applicable rules and baseline. Use PR context when available; otherwise use local diffs. Give any assigned reviewers the scope, baseline, rules, and change summary.
- Choose review depth and assignments according to change risk, responsibility boundaries, and available review capabilities. Use independent reviewers for distinct risks when useful or required by the user or project; a fixed reviewer count is not required.
- Cover applicable project rules, functional defects, and constraints in code comments. Consult blame, Git history, or related historical PR comments when needed to understand intent or check recurrence of known problems.
- Report unavailable evidence and the resulting limits; missing history does not establish absence of defects. If required independent review is unavailable, report that requirement as incomplete and continue other work.
- Reuse valid build, type, and other check results. Do not rerun checks solely for review; determine verification of fixes under Implementation and tests and Evidence reuse.

### Issue verification

- For each candidate, provide location, trigger, impact, evidence, and reasoning. Rule-based issues must cite the specific applicable rule. Issues must result from this change; do not report untouched pre-existing defects as new ones.
- Exclude existing issues, style nitpicks, unsupported speculation, and expected behavior. Do not repeat problems explicitly covered by recorded valid compiler, type, lint, or other checks, while still addressing them under implementation requirements. Missing, incomplete, or failed checks do not justify exclusion. Generic quality suggestions are not defects; allowed, applicable exceptions are not violations.
- Consolidate and deduplicate candidates, then verify reality, causation, and specific rule applicability against the change and evidence. Use a reviewer independent of the reporter when available or required; otherwise disclose self-review. Score confidence from 0–100 using the following criteria and retain only issues scoring at least 80.
- Confidence measures evidence that an issue is real and introduced by this change. Describe severity and frequency separately; do not use them to alter confidence.

| Score | Verification standard |
| --- | --- |
| 0 | Not credible: a simple check excludes it as a false positive or pre-existing issue. |
| 25 | Low confidence: initial clues exist but key judgments lack verifiable evidence. |
| 50 | Moderate confidence: partial evidence, with critical trigger, outcome, or causal links unverified. |
| 75 | High confidence: main evidence supports a real introduced issue, but unresolved doubts could change the conclusion. |
| 100 | Certain: direct evidence or reproduction confirms a real introduced issue and excludes key doubts; rule-based issues have a confirmed applicable, violated provision. |

### Fixes and delivery

- Fix verified issues scoring at least 80, determine necessary tests and reverification under Evidence reuse, and review fix effectiveness and related regressions with the applicable independence requirements. Verify new candidates under the same criteria; do not restart a full review without grounds.
- For issues outside authorization or involving major tradeoffs, explain impacts and request necessary decisions instead of silently skipping them. If qualifying issues or necessary reverification remain, report incomplete work, not completion.
- Report conclusions, fix status, and unverified scope in this chat; do not automatically post PR comments. If none qualify, say "No issues met the reporting threshold," not that code has no issues. Provide precise files and lines; remote code links must use the actual repository, full commit SHA, and corresponding lines.

## Knowledge-base updates

- After implementation, update affected documentation under [project knowledge-base conventions](project-knowledge-base.md). Do not mechanically rewrite documents when only internal implementation changes and their facts remain valid. Update obsolete paths, symbols, and other locators.
