"""Explicit deployment configuration; importing modules never discovers live data."""
from dataclasses import dataclass, fields
from contextlib import closing
import json
import os
from pathlib import Path
import re
import sqlite3


class CompatibilityError(RuntimeError):
    pass


@dataclass(frozen=True)
class Config:
    codex_bin: Path
    desktop_home: Path
    execution_home: Path
    work_dir: Path
    project_id: str
    sessions: Path
    runtime_dir: Path
    database: Path
    ipc_socket: Path
    python_bin: Path
    cc_bin: Path
    cc_config: Path
    service_prefix: str
    model: str
    reasoning_effort: str
    source_label: str
    # This identifies implemented wire/storage semantics, not a Codex release.
    adapter: str = "codex-legacy-ipc-v11"

    @classmethod
    def load(cls, path):
        data = json.loads(Path(path).read_text())
        names = {f.name for f in fields(cls)}
        if data.keys() - names:
            raise ValueError("Unknown configuration fields: " + ", ".join(sorted(data.keys() - names)))
        missing = names - {"adapter"} - data.keys()
        if missing:
            raise ValueError("Missing configuration fields: " + ", ".join(sorted(missing)))
        paths = {"codex_bin", "desktop_home", "execution_home", "work_dir", "sessions", "runtime_dir", "database", "ipc_socket", "python_bin", "cc_bin", "cc_config"}
        for key in names & data.keys():
            if not isinstance(data[key], str) or not data[key].strip():
                raise ValueError(f"{key} must be a nonempty string")
            if key in paths:
                p = Path(data[key]).expanduser()
                if not p.is_absolute():
                    raise ValueError(f"{key} must be absolute")
                data[key] = p.resolve()
        cfg = cls(**data)
        cfg.validate()
        return cfg

    def validate(self):
        if self.adapter != "codex-legacy-ipc-v11":
            raise CompatibilityError("Unsupported adapter; implement and test the target protocol first")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.-]*", self.service_prefix):
            raise ValueError("service_prefix must be a unique launchd-safe identifier")
        if self.desktop_home == self.execution_home or self.desktop_home in self.execution_home.parents or self.execution_home in self.desktop_home.parents:
            raise ValueError("Desktop and execution homes must be separate, non-nested directories")
        for home in (self.desktop_home, self.execution_home):
            if self.runtime_dir == home or self.runtime_dir in home.parents or home in self.runtime_dir.parents:
                raise ValueError("runtime_dir must be separate from both session homes")
        if self.database.parent != self.desktop_home:
            raise ValueError("database must be an explicitly selected file in desktop_home")
        if len(os.fsencode(str(self.runtime_dir / "broker.sock"))) > 103:
            raise ValueError("runtime_dir is too long for a macOS Unix socket")

    def as_dict(self):
        return {f.name: str(getattr(self, f.name)) for f in fields(self)}

    def check_files(self):
        for key in ("codex_bin", "python_bin", "cc_bin"):
            p = getattr(self, key)
            if not p.is_file() or not os.access(p, os.X_OK):
                raise ValueError(f"{key} is not an executable file: {p}")
        for key in ("sessions", "cc_config", "database"):
            if not getattr(self, key).is_file():
                raise ValueError(f"{key} does not exist")
        for key in ("desktop_home", "execution_home", "work_dir"):
            if not getattr(self, key).is_dir():
                raise ValueError(f"{key} does not exist")
        if not (self.desktop_home / "thread-writer-locks").is_dir():
            raise CompatibilityError("Missing desktop thread-writer-locks directory")

    def check_database(self):
        """Read-only open: never create a missing database or migrate its schema."""
        required = {"id", "rollout_path", "archived", "has_user_event", "updated_at", "updated_at_ms", "recency_at", "recency_at_ms", "title", "first_user_message", "preview", "model", "reasoning_effort"}
        with closing(self.connect_database(readonly=True)) as db:
            found = {row[1] for row in db.execute("PRAGMA table_info(threads)")}
        if not required <= found:
            raise CompatibilityError("Incompatible threads schema; missing: " + ", ".join(sorted(required - found)))

    def connect_database(self, readonly=False):
        # mode=rw also refuses to create a missing database.
        return sqlite3.connect(self.database.as_uri() + ("?mode=ro" if readonly else "?mode=rw"), uri=True, timeout=10)

    def check_source(self):
        data = json.loads(self.sessions.read_text())
        if not isinstance(data.get("sessions"), dict):
            raise CompatibilityError("Expected CC Connect sessions object")
        for s in data["sessions"].values():
            if s.get("agent_type") != "codex":
                continue
            if not all(k in s for k in ("created_at", "agent_session_id")):
                raise CompatibilityError("Source session identity fields are missing")
            for m in s.get("history", []):
                if not all(isinstance(m.get(k), str) for k in ("role", "content", "timestamp")):
                    raise CompatibilityError("Only timestamped text history is supported")

    def checked_rollout(self, path, tid):
        p = Path(path).resolve()
        roots = [(self.desktop_home / f).resolve() for f in ("sessions", "archived_sessions")]
        if not any(p.is_relative_to(root) for root in roots) or not p.is_file():
            raise CompatibilityError("Missing rollout or path outside desktop session directories")
        rows = [json.loads(line) for line in p.read_text().splitlines()]
        if not rows or rows[0].get("type") != "session_meta" or rows[0].get("payload", {}).get("id") != tid:
            raise CompatibilityError("Rollout session_meta does not match mirror identity")
        return p, rows
