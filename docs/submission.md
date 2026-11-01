# Public-directory submission preparation

This is a prepared listing, not evidence of upload, submission, approval, or publication. Local repository installation, public GitHub distribution, directory review, and publication are separate states. See [verification results](verification.md).

## Listing copy

| Field | Prepared value |
| --- | --- |
| Name | Vibe Dev Skills |
| Package identifier / version | `vibe-dev-skills` / `0.1.0` |
| Maintainer | `jmaxzh`; verified portal identity still to be checked |
| Summary | A software development workflow with documentation, UI, MySQL, and CC Connect skills. |
| Category | Developer tools; map to the portal's actual available category |
| Source / homepage | https://github.com/jmaxzh/vibe-dev-skills |
| Support | https://github.com/jmaxzh/vibe-dev-skills/issues |
| License | MIT; fixed notices included in every skill |
| Icon | Original terminal mark in `assets/icon.png`, 256 × 256 PNG |
| Runtime | Local coding-agent execution; optional CC Connect mirrors use Python/Unix facilities and macOS services |

Description: Turn feature ideas into requirements, technical designs, implementations, and explicit verification. The suite reuses existing project decisions and combines a user-invoked workflow with independent documentation, UI, MySQL, and integration skills. Document work requires the bundled documentation skill. English instructions are the sole runtime edition; Chinese copies support developer maintenance.

Example tasks:

- Turn a feature idea into requirements and acceptance criteria, stopping before technical design.
- Review a MySQL schema and stock deduction for integrity and concurrency issues.
- Inspect an existing CC Connect setup before optional desktop mirroring.

## OpenAI directory

Use the [standard submission flow](https://developers.openai.com/plugins/deploy/submission). Upload the review ZIP as a Skills-only plugin; there is no bundled MCP server, app mapping, or hook. Root `plugin.json` contains portable metadata and OpenAI presentation. Local execution is declared with `extensions.com.openai.requires_local_executor` under the [desktop-only guidance](https://developers.openai.com/plugins/deploy/desktop-only).

Before upload, verify the submitting account's eligibility and developer/business identity. Supply actual required contact fields and confirm any desktop-only submission access. Do not claim that the GitHub handle is already a verified identity. If the portal requires different artwork sizes or additional listing fields, supply reviewed assets and truthful information before submission; do not invent privacy/legal URLs or deployment evidence. Skills-only plugins do not require MCP app test cases or a demo recording under the current standard flow.

Upload, draft validation, submission, approval, and publication must be recorded separately. An approved version is published only through an explicitly authorized portal action. Local install success does not guarantee portal validation or review approval.

## Anthropic directory

Use [Publish and distribute a plugin](https://code.claude.com/docs/en/plugins/publish). Confirm the submitting account has the required paid plan and organization role, then use the developer portal linked by that documentation. This is separate from inclusion in `claude-plugins-official`.

Provide the package/repository, listing copy, support URL, license, icon, and actual verification results. Run strict local plugin validation before submission. Check component support on target surfaces; this coding/local-integration suite must not claim browser-only execution. Supply screenshots or other materials if the portal requires them, captured from actual successful use rather than fabricated demonstrations.

## Release gates

- Review the English sources and synchronized Chinese maintenance translations.
- Validate notices, manifests, source links, dependency handling, native installs, and the release archive.
- Complete fresh-session model checks for document-skill loading and missing-dependency handling; automated file checks alone are insufficient behavioral evidence.
- Record target-machine tests for any messaging/desktop claims, or exclude those claims from the listing.
- Confirm publisher identity, submission permissions, and required assets in each portal.
- Obtain explicit authorization for remote pushes, uploads, submissions, and public releases. Do not submit to feedback forms or contact maintainers automatically.

No marketplace or directory publication was performed as part of preparing these local files. The repository's MIT rights include the owner-confirmed CC Connect scripts; see [provenance](provenance.md).
