# Distribution verification

Verification date: 2026-11-01. Implementation commit `41f0c4e` was reviewed, fast-forwarded into `main`, and pushed to GitHub. Local and remote checks are distinguished below.

| Check | Status and evidence |
| --- | --- |
| Codex local marketplace and plugin installation | Passed in a temporary `CODEX_HOME`; `codex-cli 0.166.0-alpha.5.1` |
| Codex runtime discovery | App-server `skills/list` returned five enabled skills belonging to `vibe-dev-skills@vibe-dev-skills`; installed resources were readable |
| Claude Code native validation/install | Passed in temporary `CLAUDE_CONFIG_DIR`; `2.1.267`; strict manifest checks passed and component inventory contained five skills |
| Source, translations, and local links | Passed `scripts/validate.py`: five English entries, source-linked maintenance translations, local paths/anchors, consistent notices/manifests |
| Supported installation combinations and release archive | 8 distribution tests passed; suite/pair/specialists, missing dependency, escaping links, manifest/asset failures, deterministic English-only ZIP, and output preservation |
| skills CLI discovery/install | Pinned `skills@1.7.4` passed default/full-depth discovery, suite, workflow pair, four specialists, and expected missing-dependency detection in temporary projects; telemetry disabled |
| CC Connect isolated regression suite | 28 tests passed; all 12 Python source/test files byte-identical to pre-migration originals |
| Model execution and dependency compliance | Not run: inventory/file checks do not prove a model loads the dependency or pauses correctly when absent |
| CC Connect real messaging and desktop behavior | Not run on a deployment target |
| Remote GitHub installation | GitHub API and HTTPS `ls-remote` confirmed `main` at `41f0c4efc9c63b71406cbbe18d505660942b83be`. The exact skills CLI remote-source smoke check timed out at discovery on two attempts; remote installation is not accepted as passed |
| CI on GitHub | [Run 41294750749](https://github.com/jmaxzh/vibe-dev-skills/actions/runs/41294750749) completed successfully for implementation commit `41f0c4e` |
| skills.sh / SkillsMP listing | Not submitted or verified for this revision |
| OpenAI / Anthropic public directories | OpenAI login succeeded, but upload was blocked by the explicit requirement for a verified developer identity. Anthropic requires login. No package uploaded or submitted |

Reproduce the automated checks using [distribution instructions](distribution.md). The smoke report distinguishes local CLI installation, namespaced discovery, and missing-dependency file checks from model behavior. Perform the fresh-session positive/negative model checks before claiming behavioral acceptance or submitting a public listing.

The complete smoke script passed 12 recorded checks, including actual native installs and the Codex namespaced runtime inventory. The locally built review ZIP is `dist/vibe-dev-skills-0.1.0.zip`; `dist/install-report.json` contains the machine-readable smoke result. Neither artifact has been uploaded.
