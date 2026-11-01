# Knowledge-Base Review

- Limit this review to systematic checking of content ownership, factual accuracy, normative sources, and cross-document consistency within the designated scope, distinct from routine update checks.
- Use the installed `sdlc-instr-doc-design` skill (see [dependency resolution](../SKILL.md#skill-dependencies)) for content design and expression, and [project knowledge-base conventions](project-knowledge-base.md) for knowledge-base rules. This file defines evidence checking and dedicated review procedures. Do not trigger it for expression review alone.

## Lock the scope

- Follow the user-designated scope: for a knowledge-base root or subdirectory, cover all Markdown documents recursively; for specified documents, review only those.
- Divide targets into batches of 1–3 Markdown documents. Count in-scope documents participating in comparisons as targets; do not enlarge batches through evidence reading. Out-of-scope evidence documents do not count toward batch size.
- Check referenced images and standalone HTML with their target documents as supporting materials, not independent batch documents.
- Read and cite out-of-scope documents as evidence as needed without treating them as targets or reporting separate issues against them.
- When tracing from code changes, extract changed objects and locate direct references, behavior descriptions, and higher-level workflow documents.

## Operating boundaries

- For review-only requests, report issues and suggestions without editing files.
- With revision authorization, first reach evidence-supported conclusions, then complete per-document revision, comparison, integration, and acceptance under the installed `sdlc-instr-doc-design` skill (see [dependency resolution](../SKILL.md#skill-dependencies)). Do not repeat authorization requests within the existing scope.
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

## Batching and delegation

- Batch by topic, content volume, and evidence dependencies. Create one dedicated subagent per batch; never assign multiple batches to one subagent. Return evidence supplementation and corrections to the same agent.
- The main agent is limited to batching, scheduling, tracking, and consolidation; it must not review documents or decide facts.
- Supply applicable rules, user conventions, targets, and evidence leads. Schedule within concurrency limits, queuing instead of merging batches or using main-agent review. Report incomplete scope if subagents are unavailable.
- Each batch returns scope, major claims and normative sources, issues and evidence, cross-document relationships, pending matters, and unverified scope. Retain passed items for cross-review.
- For resumability, save checkpoints in a temporary work directory, recording progress and evidence indexes: scope, issues, paths, lines, necessary claim summaries, and relationships. Do not copy raw materials or write checkpoints into the knowledge base.
- On resume, read checkpoints and return changed files to the corresponding batch agent to revisit affected conclusions.

## Cross-review

- After initial review, consolidate claims and relationships. Create topic-based cross-batch review batches with at most 3 target documents each and a new dedicated subagent per batch. Split topics spanning more than 3 documents by related facts to cover all claims.
- Review multiple sources of truth, duplication, terminology, implementation status, responsibilities, and reference consistency. Read original content and normative sources; summaries alone cannot establish conclusions.
- For shared facts, verify source and ownership recommendations under [content boundaries](project-knowledge-base.md#content-boundaries) and consistency across batches. Mark insufficient evidence or unresolved authority as needs confirmation; do not arbitrarily select an authority.
- Assign conflicting conclusions to cross-review agents and evidence supplementation to original batches. Spot-check passed items as needed, add cross-review batches for omissions, and revise conclusions with reasons when new evidence emerges.

## Output

- Present final results in the current chat.
- Summarize scope and major conclusions, then issues and revision suggestions.
- Retain all four categories in this order; write "None" for empty ones:
  1. `Conflicts requiring user action`: unclear normative sources, conflicting evidence, or rule tradeoffs requiring information or a decision between documentation and code.
  2. `Documentation content and organization issues`: expression, content, or organization problems without document/code factual differences.
  3. `Document/code mismatch: revise documentation`: clear evidence supports code or dedicated contracts, with obsolete or incorrect documentation.
  4. `Document/code mismatch: change code`: clear evidence supports documented requirements, constraints, or intent, with deviating implementation.
- When the correct side to change is unresolved, retain needs-confirmation status. Use Conflicts requiring user action only if a user decision is necessary; do not choose independently.
- In code-change recommendations, group as `p0` for severe security, data-loss, or unavailability risks requiring immediate action, `p1` for key behavior or contract impacts, and `p2` for other confirmed deviations. Explain impact and handling order for each.
- Use this output skeleton:

```markdown
## Conflicts requiring user action

## Documentation content and organization issues

## Document/code mismatch: revise documentation

## Document/code mismatch: change code
### p0
### p1
### p2
```

- End with a batch and evidence index listing initial and cross-review batches, document counts, and agent mappings. Check coverage and report incomplete scope.
- List verification outcomes, pending matters, and unverified scope. Put pending matters in Conflicts requiring user action only when user information or rule decisions are needed; otherwise explain missing evidence and follow-up checks. For code-change tracing, also list relevance statuses.

### Issue entries

- Give each issue its own section with a short, plain description of the deviation. Split unrelated issues rather than compressing them into long entries.
- Explain impacts, priority, and order in prose; priority tags or batch identifiers alone are insufficient. Keep batch identifiers in the evidence index.
- Use separate paragraphs labeled **Problem**, **Recommendation**, and **Location and evidence**, with blank lines. Do not use issue tables.
- **Problem:** summarize the claim, verified facts, and impacts. Retain verification status and distinguish confirmed deviations from unresolved rule choices.
- **Recommendation:** specify revision actions. Mark choices between specification and implementation as "Rules must be decided first" rather than presenting unsettled options as executable conclusions.
- **Location and evidence:** collect target, normative source, and detailed evidence links at the end of each entry, using readable labels and accurate locations or lines. Avoid scattering paths, commands, or batch IDs through problem and recommendation prose.

## Cautions

- Do not infer authority from filenames.
- A corresponding implementation does not establish documentation correctness.
