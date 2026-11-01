# Knowledge-Base Review

- Limit this review to systematic checking of content ownership, factual accuracy, normative sources, and cross-document consistency within the designated scope, distinct from routine update checks.
- Use the installed `sdlc-instr-doc-design` skill (see [dependency resolution](../SKILL.md#skill-dependencies)) for content design and expression, and [project knowledge-base conventions](project-knowledge-base.md) for knowledge-base rules. This file defines evidence checking and dedicated review procedures. Do not trigger it for expression review alone.

## Lock the scope

- Follow the user-designated scope: for a knowledge-base root or subdirectory, cover all Markdown documents recursively; for specified documents, review only those.
- Group targets by topic, volume, and evidence dependencies when useful. Keep in-scope comparison documents in the target inventory and out-of-scope evidence separate; evidence reading must not expand the review scope.
- Check referenced images and standalone HTML with their target documents as supporting materials, not independent batch documents.
- Read and cite out-of-scope documents as evidence as needed without treating them as targets or reporting separate issues against them.
- When tracing from code changes, extract changed objects and locate direct references, behavior descriptions, and higher-level workflow documents.

## Operating boundaries

- For review-only requests, report issues and suggestions without editing files.
- With revision authorization, first reach evidence-supported conclusions, then revise, compare, integrate, and verify the affected content under the installed `sdlc-instr-doc-design` skill (see [dependency resolution](../SKILL.md#skill-dependencies)). Do not repeat authorization requests within the existing scope.
- Handle confirmation under Updates and rule changes and Human acceptance in [project knowledge-base conventions](project-knowledge-base.md).

## Judgment statuses

- Record verification per claim or check: `Passed` when applicable checks are complete and evidence supports correctness; `Confirmed issue` for evidenced deviations; `Unverified` before checks; `Needs confirmation` when checked but key evidence, normative source, or conflict resolution is missing. Explain uncertainty without presuming error. Partial success does not mean the whole document passes.
- Only when tracing from code changes, record relevance separately: `Potentially related` for plausible but unconfirmed impact; `Confirmed affected` for established impact; `Unrelated` for excluded impact. Judge correctness independently; affected does not mean wrong.

## Determine content ownership

- Establish document purpose, subject, and responsibility first.
- Determine whether a claim belongs to that responsibility.
- Report out-of-responsibility content as an ownership problem before comparing it to code.
- Do not check non-exhaustive examples as complete inventories.

## Build a claim inventory

- Form verifiable claims only for content within responsibility.
- Distinguish normative definitions, generated content, derived summaries, and non-exhaustive examples.
- Locate normative sources and evidence by fact type.
- Check conflicting definitions and whether derived content faithfully reflects sources.

Locate sources by fact type rather than enumerating everything:

- Product or business behavior: product specifications and business rules.
- APIs: OpenAPI, schemas, or protocols; CLI: specification or argument definitions; configuration: schema or specification; data structures: schema, migrations, or protocols.
- Implementation and execution: code; deployment: IaC or deployment configuration; external protocols: official standards or third-party specifications.
- Explanatory content: its corresponding normative sources.

## Determine relevance

Apply this section only when tracing documents from code changes:

- First determine whether a code change alters facts owned by the document.
- Adding, deleting, renaming, or moving implementation objects alone does not establish document impact.
- Assess under the [content boundaries](project-knowledge-base.md#content-boundaries); include potentially obsolete explanations for verification.
- Record relevance under Judgment statuses. Investigate potentially related claims and verify confirmed affected ones. In change-impact-only reviews, unrelated claims may be skipped; in comprehensive reviews, still check them within scope.
- If evidence is unavailable, retain potentially related status, mark needs confirmation, identify missing evidence, and list the unverified scope.

## Verify claims

- Check definitions, defaults, value ranges, objects, conditions, behavior, and boundaries as applicable to each claim.
- Check conventions under [project knowledge-base conventions](project-knowledge-base.md) and record results under Judgment statuses.
- Check accessibility of visual references and their assets, actual rendering consistency, and [visual reference rules](project-knowledge-base.md#visual-references). If rendering cannot be viewed, mark relevant conclusions unverified and explain the uncovered scope.

## Handle out-of-boundary content

For suspected duplicate definitions or implementation restatements, follow [content boundaries](project-knowledge-base.md#content-boundaries):

1. Determine whether content belongs to the document's responsibility.
2. Recommend removal, relocation, source links, or conversion to non-exhaustive examples for content outside it.
3. Verify facts only for content chosen for retention.
4. Report ownership problems, factual errors, and implementation deviations separately; do not substitute one for another.

- Do not retain out-of-responsibility content merely because it matches code.
- Do not fill out such content merely because it differs from code.
- Apply the refactoring test under [content boundaries](project-knowledge-base.md#content-boundaries): assume only internals change while document-owned facts remain stable. Report content that merely enumerates internals; updating paths or symbols is not implementation restatement.
- Do not infer design constraints from current implementation or demand implementation conform to unsupported descriptions.
- For suspected duplicate definitions, locate definitions and sources, distinguish independent definitions from derived content, and check consistency. Propose evidence-supported revisions under [content boundaries](project-knowledge-base.md#content-boundaries).

## Review organization and progress

- Choose review units and assignments by topic, evidence dependencies, risk, and available capabilities. Delegate when useful or required; keep responsibility for complete coverage and evidence-supported conclusions explicit.
- For delegated work, provide applicable rules, user conventions, targets, and evidence leads. Each result must identify scope, major claims and normative sources, issues and evidence, cross-document relationships, pending matters, and unverified scope. Retain passed items for cross-review.
- For long or interrupted reviews, save progress and evidence indexes in a temporary work directory: scope, issues, paths, lines, necessary claim summaries, and relationships. Do not copy raw materials or write checkpoints into the knowledge base.
- On resume, check which files or evidence changed and revisit affected conclusions. Report incomplete scope and unavailable required review capabilities.

## Cross-review

- Check related claims and conclusions across documents for conflicting normative sources, duplication, terminology, implementation status, responsibilities, and reference consistency. Read original content and normative sources; summaries alone cannot establish conclusions.
- For shared facts, verify source and ownership recommendations under [content boundaries](project-knowledge-base.md#content-boundaries). Mark insufficient evidence or unresolved authority as needs confirmation; do not arbitrarily select an authority.
- Resolve conflicting conclusions through evidence supplementation and independent review when useful or required. Spot-check passed items as needed, cover omissions, and revise conclusions with reasons when new evidence warrants it.

## Output

- Present final results in the current chat.
- Summarize scope and major conclusions, then issues and revision suggestions.
- Classify issues using these categories, keeping user decisions first. Omit empty categories unless the requested format requires them:
  1. `Conflicts requiring user action`: unclear normative sources, conflicting evidence, or rule tradeoffs requiring information or a decision between documentation and code.
  2. `Documentation content and organization issues`: expression, content, or organization problems without document/code factual differences.
  3. `Document/code mismatch: revise documentation`: clear evidence supports code or dedicated contracts, with obsolete or incorrect documentation.
  4. `Document/code mismatch: change code`: clear evidence supports documented requirements, constraints, or intent, with deviating implementation.
- When the correct side to change is unresolved, retain needs-confirmation status. Use Conflicts requiring user action only if a user decision is necessary; do not choose independently.
- In code-change recommendations, group as `p0` for severe security, data-loss, or unavailability risks requiring immediate action, `p1` for key behavior or contract impacts, and `p2` for other confirmed deviations. Explain impact and handling order for each.
- Include a scope and evidence index sufficient to check coverage and resume unfinished work. For batched or delegated reviews, record document counts, assignments, and cross-review coverage. Report incomplete scope.
- List verification outcomes, pending matters, and unverified scope. Put pending matters in Conflicts requiring user action only when user information or rule decisions are needed; otherwise explain missing evidence and follow-up checks. For code-change tracing, also list relevance statuses.

### Issue entries

- Give each issue its own section with a short, plain description of the deviation. Split unrelated issues rather than compressing them into long entries.
- Explain impacts, priority, and order in prose; priority tags or batch identifiers alone are insufficient. Keep batch identifiers in the evidence index.
- Make each issue's problem, recommendation, and supporting locations and evidence easy to identify. Use the following labels when helpful.
- **Problem:** summarize the claim, verified facts, and impacts. Retain verification status and distinguish confirmed deviations from unresolved rule choices.
- **Recommendation:** specify revision actions. Mark choices between specification and implementation as "Rules must be decided first" rather than presenting unsettled options as executable conclusions.
- **Location and evidence:** collect target, normative source, and detailed evidence links at the end of each entry, using readable labels and accurate locations or lines. Avoid scattering paths, commands, or batch IDs through problem and recommendation prose.

## Cautions

- Do not infer authority from filenames.
- A corresponding implementation does not establish documentation correctness.
