# Deployment and Maintenance

This reference is for CC Connect integration maintainers. The primary path is messaging platform → CC Connect → local coding tool; desktop mirroring is an independent optional feature.

## Discovery and configuration

Inspect installation source, executables, versions, arguments, working directories, authentication backend, configuration, session data, and existing background processes. Prefer installed-version documentation; do not copy another project's identifiers or credentials.

Before configuration, establish the platform, coding tool, allowed users, project directory, and permission mode. Configure model and reasoning effort only when supported and needed. Follow fixed display and Feishu topic rules below. Topic isolation gives topics independent context, with behavior depending on platform and version; do not confuse topic IDs, platform user IDs, and coding-tool session IDs.

Choose installation and integrations using version-specific sources, not a historical example's version. This shows structure only, not deployable configuration; verify fields for the selected adapter:

```toml
[[projects]]
name = "example-project"

[projects.agent]
type = "<actually supported coding-tool type>"

[projects.agent.options]
work_dir = "<actual absolute project directory>"

[[projects.platforms]]
type = "<actually supported messaging-platform type>"

[projects.platforms.options]
# Supply platform app identity, allowed users, and event configuration.
```

Start with CC Connect's [configuration example](https://github.com/chenhg5/cc-connect/blob/main/config.example.toml) and [usage guide](https://github.com/chenhg5/cc-connect/blob/main/docs/usage.md). Consult versions matching the deployment rather than assuming main is always applicable.

## Fixed configuration

- Set global `[display]` to `mode = "quiet"`. Check project-level settings do not override it with another mode.
- Feishu groups must use topic mode, with `thread_isolation = true` in the Feishu adapter's `[projects.platforms.options]`. Check group mode and adapter configuration separately; enabling isolation alone does not establish topic mode.

Merge these fragments into the relevant tables; do not recreate existing tables:

```toml
[display]
mode = "quiet"

# Inside the relevant Feishu [projects.platforms.options] table:
# thread_isolation = true
```

The official example above is the field reference; still verify installed-version support. If unsupported, report the blocker and address compatibility rather than silently switching modes.

For acceptance, verify Feishu messages are organized by topic, conversations continue within a topic, and different topics have isolated source sessions. Verify `quiet` display without reasoning or tool-progress messages. Other messaging platforms require `quiet`; configure topic isolation according to their requirements.

## Authentication and session storage

Platform app secrets connect the bot; coding-tool authentication enables model calls; optional platform CLI login enables additional resource operations. They are not interchangeable. Receiving a platform message alone does not require installing or using its CLI.

If execution and desktop could open the same source session concurrently, inspect the tool's concurrent-write constraints first. With mirroring, execution stores source sessions and desktop stores view-only copies, which must not be used to continue task execution.

For Codex file authentication, credential-file symlinks may be suitable. First verify the target exists and the version's read/write/refresh behavior supports this approach. For keychain, API-key, or other backends, use a supported mechanism.

- Link only credentials requiring sharing, not the entire session-data directory.
- Inspect existing targets; do not force overwrite. Plan existing-session migration separately.
- Log in again at the designated source. Logout within an isolated execution directory may delete the link; recheck after maintenance.
- Login-status checks do not prove server-side validity. Within authorization, a minimal non-mutating request may verify it. Concurrent successful requests do not prove concurrent token refresh is safe.

Protect secret-bearing configuration and chat-bearing logs, caches, and databases; do not include them in skills, repositories, or diagnostic attachments.

## Initial integration

1. Configure the platform app or bot with version-specific permissions, event subscriptions, receiving method, and allowed users, completing required publication or authorization.
2. Independently verify the coding tool in the target directory with expected authentication and permission mode.
3. Write actual CC Connect configuration.
4. Start one foreground instance and inspect its environment and logs.
5. In the user-designated test conversation, verify real messaging, directory, model, and topic behavior. Repair authentication or platform-permission failures on the primary path first.
6. Stop the foreground instance.
7. Deploy with an appropriate OS service manager. Choose either CC Connect background management or an external manager to avoid duplicates.

User-level launchd is an option on macOS; choose appropriate mechanisms elsewhere rather than copying plist files or a fixed three-service layout. Explicitly configure background PATH, variables, and executables, including wrapper runtimes.

## Maintenance, migration, and recovery

Before changes, identify instance ownership and active configuration/data, and back up affected configuration and persistent state. Compare generated arguments and diffs, stop affected instances, install changes, and restore services. Do not overwrite source sessions or initialize another machine by copying desktop databases.

For sync-only changes, prefer restarting only sync. For the bundled Codex implementation's broker order, generation, and startup, see [Codex mirror implementation](codex-mirror-example.md). After desktop, CLI, or CC Connect upgrades, repeat compatibility checks and key acceptance. On failure, disable mirroring while retaining logs/mappings, then restore a compatible deployment or adapt first.

Disabling mirroring does not require disabling CC Connect. Preserve source sessions and mirror logs when removing startup services; deletion of chat data requires a separate user decision.

## Troubleshooting order

| Symptom | Checks and judgment | Recovery and verification |
| --- | --- | --- |
| No platform messages | Event subscriptions, publication, bot visibility, permissions, allowed users | Fix platform errors and test messaging in the designated conversation |
| Platform receives but tool fails | Executable, directory, permissions, execution-environment authentication | Fix tool configuration, verify tool, then messaging |
| Revoked auth or refresh failure | Credential source and symlink; avoid repeated stale overwrites | Log in at designated source, restart if needed, verify an actual request |
| Session write-lock conflict | Execution using desktop storage or duplicate instances | Restore isolation and test continuation; do not delete locks or kill unrelated processes |
| Foreground works, background command missing | Executable path, PATH, wrapper dependencies, variables | Correct service and restart only its instance |
| Messaging works, copies fail | Source file, project ID, compatibility, logs, subscriptions | Use Codex-specific reference or the other tool's own implementation |

For delivery or support, retain versions, redacted errors, and status summaries; exclude credentials, full chat logs, and databases.
