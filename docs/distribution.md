# Validate and distribute the suite

Run commands from the repository root. Installation checks use temporary projects and plugin configurations; they do not change your normal agent configuration or call a model.

## Validate locally

```sh
python3 -B scripts/validate.py
python3 -B -m unittest discover -s tests -v
python3 -B -m unittest discover -s skills/cc-connect-integration/scripts -v
python3 -B scripts/smoke_install.py --native
```

The smoke check requires Node/npm, network access for `skills@1.7.4`, and the Codex/Claude CLIs for `--native`. It exercises default/full-depth discovery, the five-skill suite, the workflow pair, four individual specialists, and a deliberately incomplete workflow installation. Its missing-dependency result is a file/composition check, not proof of model compliance. Native checks register and install locally and inspect actual skill inventories. Codex app-server is queried without creating a model turn.

The report is written to `dist/install-report.json`. A timeout or unavailable CLI is a failure when `--native` was requested; inspect the report rather than treating skipped or failed execution as passed. GitHub Actions runs the portable checks, script tests, skills CLI smoke check, and installation-report upload; it does not claim to test native clients absent from the runner.

## Check native clients manually

Assign `CHECKOUT` to this checkout's actual absolute directory. These commands change the client configuration in which you run them; use a disposable configuration as the smoke script does when testing.

```sh
codex plugin marketplace add "$CHECKOUT"
codex plugin add vibe-dev-skills@vibe-dev-skills
claude plugin marketplace add "$CHECKOUT"
claude plugin install vibe-dev-skills@vibe-dev-skills
```

In a fresh local session, verify actual registered skill names and invoke the workflow for requirements only. Confirm that it loads the documentation skill when producing the artifact, without invoking all specialists. Then test a disposable workflow-only installation: the agent should identify missing `sdlc-instr-doc-design`, pause dependent document work, explain the pair installation, and not install anything itself. Record observed behavior separately from CLI inventory checks. Never remove your normal documentation skill to perform this negative test.

## Publish and check GitHub installation

Only after explicit authorization, publish the reviewed changes to the repository and rerun:

```sh
python3 -B scripts/smoke_install.py --source jmaxzh/vibe-dev-skills
```

The source must match the local entries being validated. Before publication the remote repository still has its previous structure; local smoke success does not establish remote success. Existing manually copied installations must be backed up and updated from the new `skills/` directories; old root skill paths are removed without compatibility symlinks.

Use [the project README](../README.md#install) for public commands. Codex and Claude Code install the entire suite. skills CLI also supports the workflow plus its documentation dependency and the four individual specialists. No custom dependency metadata or installer is used.

skills.sh tracks directory appearances through actual installation telemetry; these verification runs disable telemetry. SkillsMP indexes public GitHub `SKILL.md` files. After publication, check each English source and index link; neither site promises an immediate listing. If missing, use the site's current official feedback channel only when authorized. Do not fabricate rankings or submit duplicate Chinese skills.

Sources: [OpenAI packaging](https://developers.openai.com/plugins/build/plugins), [Claude marketplace publishing](https://code.claude.com/docs/en/plugins/publish), [skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/commands.md), [skills.sh listing](https://www.skills.sh/docs/faq), [SkillsMP](https://skillsmp.com/about).
