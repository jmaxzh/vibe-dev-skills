# Codex Mirror Implementation

## Capabilities and applicability

The bundled implementation adapts a user-provided CC Connect → Codex desktop mirror script package. CC Connect handles messaging and tool invocation; bundled scripts synchronize only completed textual exchanges from Codex source sessions into desktop copies, without calling a model to generate replies.

```text
Messaging platform → CC Connect → Codex source session in isolated execution environment
                         │
                         └─ Completed exchanges → Sync service → Desktop session copy
                                                      │
                                                      └─ Broker → Desktop subscription updates
```

| Script | Responsibility |
| --- | --- |
| `service.py` | Persistent mappings and exchanges, deduplication, titles, projections, list indexes, archiving |
| `broker.py` | Persistent desktop subscription and local broker socket in runtime directory |
| `mirror_ipc.py` | Internal desktop IPC frames, notifications, and display-state adaptation |
| `codex_rpc.py` | Start App Server; invoke project and session interfaces |
| `titles.py` | Prefer explicit names, otherwise first substantive request; stable titles, IDs for collisions |
| `config.py` | Load common configuration; check paths, source records, database, and copy format |
| `compatibility.py` | Check API schema, native project IDs, and desktop IPC initialization |
| `prepare.py` | Query projects or generate deployment bundles and optional macOS services; does not install |
| `test_*.py` | Test synchronization, archiving, and configuration with temporary directories and mock interfaces |

The implementation uses Python's standard library, Unix sockets, and `fcntl`. The provided deployment method is macOS user services; other operating systems are unverified, so neither generator nor synchronization scripts constitute a verified cross-platform implementation. Choose Python with the necessary standard-library APIs and run bundled tests rather than assuming an interpreter location.

`codex-legacy-ipc-v11` identifies the supported protocol and session format, not a Codex version to install. Dependencies include experimental App Server APIs, legacy rollout, internal desktop IPC v11, a `threads` table with required fields, and desktop write locks. Configuration changes cannot adapt other protocols; failed checks require code and test adaptation, not guessed database or protocol structures.

Attachments, tool traces, and bidirectional continuation are excluded. Other coding tools need independent storage/subscription adapters. The original package's reported 15 historical tests and machine validation describe only its former environment, not acceptance of this version or target machine.

## Common configuration

Run commands from this skill's `scripts/` directory or use actual absolute script paths. Replace every value in this JSON; it explains fields rather than describing an actual machine:

```json
{
  "codex_bin": "/example/tools/codex",
  "desktop_home": "/example/data/desktop",
  "execution_home": "/example/data/executor",
  "work_dir": "/example/projects/project-a",
  "project_id": "native-project-id-from-this-desktop",
  "sessions": "/example/connect/sessions/actual-project.json",
  "runtime_dir": "/example/mirror/project-a",
  "database": "/example/data/desktop/actual-state.sqlite",
  "ipc_socket": "/example/data/desktop/ipc/actual.sock",
  "python_bin": "/example/tools/python3",
  "cc_bin": "/example/tools/cc-connect",
  "cc_config": "/example/connect/config.toml",
  "service_prefix": "org.example.project-a.mirror",
  "model": "available-model-selected-for-this-project",
  "reasoning_effort": "effort-supported-by-the-selected-model",
  "source_label": "Messaging platform name",
  "adapter": "codex-legacy-ipc-v11"
}
```

- Paths expand `~` and normalize to absolute paths. Relative paths, unknown fields, and missing required fields are rejected. Executables and existing inputs must actually exist.
- `desktop_home` receives copies; `execution_home` is CC Connect's isolated Codex environment. They must neither match nor nest. Configure shared credentials separately by backend; the generator does not change them.
- `database` must identify the actual database within the selected desktop directory, not a guessed filename or highest version number. Inspect `threads` and desktop configuration before choosing. No database is created or migrated.
- `ipc_socket` is the actual desktop socket, distinct from generated `runtime_dir/broker.sock`.
- Keep `runtime_dir` separate from both session environments and short enough for macOS Unix-socket limits. Each instance requires distinct runtime directories, prefixes, and source mappings; do not synchronize one source through two instances.
- Model/effort affect copy metadata, not CC Connect execution settings; configure each side as needed. The source label names copy titles and is not Feishu-specific.
- One configuration handles one native project and one source sessions file. Use separate configuration/runtime directories for multiple projects. Existing journals belong only to their original source mapping and desktop target; changing targets requires migration.

## Query and generate

Assign uppercase shell variables before each command: discover executables and data paths on the machine; choose configuration and bundle locations for this deployment. `SCRIPTS_DIR` is this skill's absolute `scripts/` path.

Verify messaging first and open the receiving project in desktop. Identify the CLI used by that desktop, then query native project IDs using actual paths:

```sh
"$PYTHON_BIN" prepare.py --list-projects \
  --codex-bin "$CODEX_BIN" --desktop-home "$DESKTOP_HOME"
```

`project/list` returns that desktop's native project IDs, not IDs from another application's management API. Establish source sessions filenames from actual execution records.

Save substituted JSON at `CONFIG_FILE`, then generate a bundle:

```sh
"$PYTHON_BIN" prepare.py --config "$CONFIG_FILE" --output "$BUNDLE_DIR" --launchd
```

`--launchd` is allowed only on macOS; omit it to generate just scripts and configuration. Add wrapper runtimes using repeatable `--path-entry "$EXTRA_BIN_DIR"`; background PATH does not inherit terminal initialization.

The output directory must not exist. Output contains `bin/`, normalized `deployment.json`, and optional `LaunchAgents/`, without credentials. The generator checks files, database fields, and source records without starting models, installing files, creating runtime directories, or changing installed services.

## Check, install, and start

First run in the prepared bundle:

```sh
"$PYTHON_BIN" "$BUNDLE_DIR/bin/service.py" \
  --config "$BUNDLE_DIR/deployment.json" --check
```

The full check reads source/database, exports the CLI's experimental API schema in temporary `CODEX_HOME`, briefly starts App Server with the desktop directory to query projects, and initializes real desktop IPC. It creates neither copies nor model turns, but App Server may log. Open desktop first; this runtime probe is not a side-effect-free static check.

The check establishes required API fields, legacy enum values, projects, and IPC initialization, not full v11 subscription semantics; target-machine tests remain necessary. Start with [OpenAI App Server documentation](https://learn.chatgpt.com/docs/app-server) for schema export; establish experimental project fields and internal protocols from the actual CLI and target environment.

After excluding duplicate services, install generated files. On first deployment, create a restricted `runtime_dir`, place `bin/` and `deployment.json` there, and copy generated plists to the actual user LaunchAgents directory. For existing deployment, back up state and stop affected services first, selectively updating files while preserving `mirror-*.json`.

Inspect plists: `connect` uses execution home; `broker` and `sync` use desktop home. Scripts, configuration, and logs must point to final runtime paths, not temporary bundles. Install only the two mirror services if reusing an existing CC Connect service; do not duplicate `connect`.

Load each required service with `launchctl bootstrap "gui/$(id -u)" "$PLIST_FILE"`, assigning the actual plist each time, in order: messaging if absent, broker, sync. Broker and sync first check files, schema, and project; broker then connects to desktop IPC and sync waits for successful IPC initialization before writing copies. If desktop is not started or temporarily unreachable, they wait; explicit incompatibility exits. A running broker reconnects after temporary desktop disconnection; sync logs and retries short-lived connection errors.

Services start at login, but `KeepAlive` is false, so launchd does not automatically restart exited processes and repeatedly trigger writes after compatibility errors. They wait if desktop is not yet started; file/interface check failures require repair and explicit startup. Verify login recovery and desktop startup order on the target machine rather than inferring success from plists.

## Synchronization, archiving, and maintenance

Mappings combine source-session key and creation time; completed exchanges are deduplicated by content and timestamp. Persistent `mirror-*.json` stores initial copy records, mappings, and exchanges for restart recovery. Deleting it may create duplicate copies.

Sync briefly holds only the corresponding copy's write lock, not the source's. Before writing, it checks rollout identity/path. Lock conflicts retain pending work. Desktop controls archiving: read actual path and state each time, continue updating archived files, and send no unarchive notification. Manual unarchive retains the original copy ID; deleted copies are not recreated automatically.

`status.json` summarizes connection, turns, pending work, and archiving. Use `sync.log`, `broker.log`, and `connect.log` for diagnostics. `broker-state.json` and mirror journals contain chat text and must be treated as private session data. Status fields do not replace actual messaging and desktop acceptance.

- Routine sync maintenance: restart only `${service_prefix}.sync`; stop corresponding services before configuration changes.
- Broker/internal-protocol maintenance: stop sync, close desktop, restart broker, reopen desktop, then restore sync. The original implementation encountered open views failing to resubscribe after broker disconnection; follow this order and verify subscriptions. Process existence is insufficient.
- Inspect with `launchctl print "gui/$(id -u)/$SERVICE_LABEL"`, explicitly restart with `launchctl kickstart -k "gui/$(id -u)/$SERVICE_LABEL"`, and unload with `launchctl bootout "gui/$(id -u)/$SERVICE_LABEL"`. Assign the actual instance label each time.
- For schema, rollout, or API incompatibility, stop mirroring and adapt. Do not change database fields, delete locks, unarchive, or overwrite other sessions to suppress errors.

| Symptom | Checks and recovery |
| --- | --- |
| No copy | Check completed source exchanges and `agent_type=codex`, then native project ID, full check, and logs |
| Open copy stops updating | Check broker connection and recent broker restarts/desktop upgrades; test resubscription after recovery |
| Persistent pending work | Check locks, archive path, and database row; retain journals without forced overwrite/recreation |
| Archived copy reappears | Check duplicate old processes or other scripts sending unarchive notifications; this implementation does not unarchive |
| Background startup fails | Check structure, desktop availability, paths, and wrapper runtimes; explicitly start after fixing |

## Verification

Run isolated regression tests:

```sh
"$PYTHON_BIN" -B -m unittest discover -s "$SCRIPTS_DIR" -v
```

Tests use temporary directories, mocked RPC, and temporary sockets without messaging real platforms. The suite covers completed exchanges, titles, and archiving from the original package, plus configuration propagation, generation without modifying deployments, instance IDs, no creation of missing databases, schema/IPC failures, stable copies, and restart recovery.

Separately verify on the target machine:

- Messaging: test actual exchanges in the designated conversation.
- Continuous sync: after three exchanges, the copy ID is unchanged without duplicates; source conversation continues while the copy is open.
- Topic isolation: new topics receive independent copies when isolation is enabled.
- Archiving: append after archive without making the copy active; manual unarchive retains full history.
- Recovery: sync restart updates the same copy; logout/login produces expected service order and state.

Isolated tests do not guarantee concurrent token refresh, new-version compatibility, or real desktop rendering.
