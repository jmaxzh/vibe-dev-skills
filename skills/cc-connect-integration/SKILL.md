---
name: cc-connect-integration
description: Deploy, configure, maintain, or troubleshoot CC Connect integrations between messaging platforms and local coding agents, including optional Codex desktop transcript mirrors.
license: MIT
---

# CC Connect Integration

Connect messaging platforms to local coding tools through CC Connect, optionally synchronizing completed exchanges into desktop copies. Use for initial deployment, maintenance, migration, upgrades, and troubleshooting.

A "source session" is the execution-side session processing messages. A "desktop copy" is its synchronized, view-only desktop session. "Desktop mirroring" means the synchronization that creates and updates those copies.

## Environment and capability selection

- Inspect the actual OS, CC Connect and coding-tool executables and versions, configuration and services, working directories, authentication backend, and session storage first. Respect explicit user choices; ask only for consequential decisions that cannot be determined from the environment.
- Verify supported platforms and tools against installed-version help, configuration examples, and official sources. Discover or explicitly configure paths, models, reasoning effort, project IDs, session filenames, and service labels. Do not reuse example values or unconditionally install the latest version.
- Determine whether desktop mirroring is needed. Verify messaging first, then optional mirroring. If mirroring is unavailable, explain limits and continue the independently usable messaging integration.

## Deployment and maintenance

Follow [deployment and maintenance](references/deployment-and-maintenance.md) for authentication, messaging, session isolation, startup, and troubleshooting. Install or maintain within authorization without reinitializing existing session storage.

- Always use `quiet` conversation display mode. Feishu groups must use topic mode with source sessions isolated by topic. See [fixed configuration](references/deployment-and-maintenance.md#fixed-configuration) for setup and acceptance.
- Choose models and permission modes according to needs; do not grant full access by default.
- Distinguish messaging-platform app secrets, coding-tool login, and optional platform CLI authorization. Share credential files only when the actual backend supports it and verification passes. Shared credentials do not remove source/copy storage isolation.
- Use the target OS's appropriate service manager. Identify existing services first to avoid duplicates. Specify executable paths, working directories, and background environment rather than relying on interactive shell initialization.
- Preserve source sessions, mirror mappings, and persistent logs during maintenance. Back up configuration and state before upgrades; restore services after compatibility checks.

## Optional desktop mirroring

For Codex, read [Codex mirror implementation](references/codex-mirror-example.md) and use bundled scripts to generate configuration and check compatibility. They support only the documented legacy session format and IPC v11 adapter; nearby versions are not automatically compatible.

For other tools, inspect export, import, subscription, and concurrent-write support before choosing synchronization. Codex databases, locks, and internal protocols cannot be reused by changing a tool name. If no suitable interface exists, explain desktop synchronization is unavailable; do not modify unknown storage structures.

## Acceptance and delivery

Verify actual deployment scope and distinguish configuration checks, isolated tests, and target-machine validation:

- Messaging: verify actual sending/receiving, the target working directory, and selected coding tool.
- Desktop mirroring: verify multi-turn append, session separation, continued source conversation while a copy is open, restart recovery, archiving, and manual unarchiving.
- Startup: separately verify service startup after user logout and login.

Deliver actual parameters, service management, log/state locations, recovery steps, and unverified scope, excluding credentials and real chat text. Historical package results do not replace current or target-machine verification.
