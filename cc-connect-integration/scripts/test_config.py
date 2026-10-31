from contextlib import closing
from dataclasses import replace
import json
import os
from pathlib import Path
import plistlib
import socket
import sqlite3
import struct
import tempfile
import threading
import unittest
import uuid
from unittest.mock import Mock, patch
from config import Config, CompatibilityError
from compatibility import check, check_api_schema, wait_for_desktop
from prepare import prepare
from mirror_ipc import probe
from service import Service, render, completed
from titles import topic_title, display_title


class ConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        for f in ("desktop", "executor", "project space", "desktop/thread-writer-locks", "desktop/sessions", "desktop/archived_sessions"):
            (self.root / f).mkdir(parents=True, exist_ok=True)
        exe = self.root / "tool"
        exe.write_text("#!/bin/sh\nexit 0\n")
        exe.chmod(0o700)
        self.source = self.root / "source.json"
        self.source.write_text('{"sessions": {}}')
        self.cc = self.root / "cc.toml"
        self.cc.write_text("# fixture\n")
        db = self.root / "desktop/catalog.sqlite"
        with closing(sqlite3.connect(db)) as conn, conn:
            conn.execute("CREATE TABLE threads (id TEXT PRIMARY KEY, rollout_path TEXT, archived INTEGER, has_user_event INTEGER, updated_at INTEGER, updated_at_ms INTEGER, recency_at INTEGER, recency_at_ms INTEGER, title TEXT, first_user_message TEXT, preview TEXT, model TEXT, reasoning_effort TEXT)")
        self.config = Config(exe, self.root / "desktop", self.root / "executor", self.root / "project space", "native-project", self.source, self.root / "runtime", db, self.root / "app.sock", exe, exe, self.cc, "org.example.first", "custom-model", "custom-effort", "团队消息")
        self.path = self.root / "deployment.json"
        self.path.write_text(json.dumps(self.config.as_dict()))

    def fingerprint(self):
        return {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}

    def test_prepare_is_output_only_and_propagates_config(self):
        before = self.fingerprint()
        out = prepare(self.path, self.root / "prepared", launchd=True, path_entries=[self.root])
        self.assertEqual(Config.load(out / "deployment.json"), self.config)
        for name, content in before.items():
            self.assertEqual(Path(name).read_bytes(), content)
        self.assertFalse(self.config.runtime_dir.exists())
        connect = plistlib.loads((out / "LaunchAgents/org.example.first.connect.plist").read_bytes())
        sync = plistlib.loads((out / "LaunchAgents/org.example.first.sync.plist").read_bytes())
        self.assertEqual(connect["EnvironmentVariables"]["CODEX_HOME"], str(self.config.execution_home))
        self.assertEqual(connect["ProgramArguments"], [str(self.config.cc_bin), "--config", str(self.cc)])
        self.assertIn(str(self.config.runtime_dir / "deployment.json"), sync["ProgramArguments"])
        self.assertFalse(sync["KeepAlive"])
        with self.assertRaisesRegex(ValueError, "already exists"):
            prepare(self.path, out)

    def test_missing_config_and_relative_paths_rejected(self):
        data = self.config.as_dict()
        del data["model"]
        self.path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "Missing.*model"):
            Config.load(self.path)
        data["model"] = "m"
        data["desktop_home"] = "relative"
        self.path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "absolute"):
            Config.load(self.path)

    def test_isolation_and_adapter_validation(self):
        with self.assertRaisesRegex(ValueError, "separate"):
            replace(self.config, execution_home=self.config.desktop_home).validate()
        with self.assertRaises(CompatibilityError):
            replace(self.config, adapter="unknown").validate()

    def test_instances_have_distinct_service_and_socket_paths(self):
        other = replace(self.config, runtime_dir=self.root / "second", service_prefix="org.example.second")
        other_path = self.root / "second.json"
        other_path.write_text(json.dumps(other.as_dict()))
        first = prepare(self.path, self.root / "first-bundle", launchd=True)
        second = prepare(other_path, self.root / "second-bundle", launchd=True)
        labels = []
        for out in (first, second):
            labels.append({plistlib.loads(p.read_bytes())["Label"] for p in (out / "LaunchAgents").glob("*.plist")})
        self.assertFalse(labels[0] & labels[1])
        from broker import RemoteIPC
        a = RemoteIPC({}, self.config.runtime_dir / "broker.sock")
        b = RemoteIPC({}, other.runtime_dir / "broker.sock")
        self.assertNotEqual(a.socket_path, b.socket_path)

    def test_missing_database_not_created(self):
        missing = self.root / "desktop/missing.sqlite"
        with self.assertRaises(sqlite3.OperationalError):
            replace(self.config, database=missing).check_database()
        self.assertFalse(missing.exists())

    def test_schema_failure_does_not_write_or_contact_live_interfaces(self):
        with closing(sqlite3.connect(self.config.database)) as conn, conn:
            conn.execute("ALTER TABLE threads DROP COLUMN preview")
        before = self.fingerprint()
        with patch("compatibility.RPC") as rpc, patch("compatibility.probe") as ipc:
            with self.assertRaisesRegex(CompatibilityError, "preview"):
                check(self.config)
            rpc.assert_not_called()
            ipc.assert_not_called()
        self.assertEqual(before, self.fingerprint())

    def test_bad_source_and_rollout_rejected(self):
        self.source.write_text('{"sessions": {"s": {"agent_type": "codex"}}}')
        with self.assertRaises(CompatibilityError):
            self.config.check_source()
        path = self.config.desktop_home / "sessions/test.jsonl"
        path.write_text(json.dumps({"type": "session_meta", "payload": {"id": "wrong"}}))
        with self.assertRaises(CompatibilityError):
            self.config.checked_rollout(path, "expected")

    def test_api_schema_failure_is_isolated(self):
        before = self.fingerprint()
        def generate(args, **kwargs):
            out = Path(args[-1])
            (out / "ThreadStartParams.json").write_text('{"title": "ThreadStartParams", "properties": {}}')
            self.assertEqual(kwargs["env"]["CODEX_HOME"], str(out))
        with patch("compatibility.subprocess.run", side_effect=generate):
            with self.assertRaises(CompatibilityError):
                check_api_schema(self.config)
        self.assertEqual(before, self.fingerprint())

    def test_valid_api_schema_and_readonly_preflight(self):
        def generate(args, **kwargs):
            out = Path(args[-1])
            props = {k: {} for k in ("cwd", "projectId", "model", "config", "sandbox", "approvalPolicy", "baseInstructions")}
            props["historyMode"] = {"enum": ["legacy", "new"]}
            (out / "start.json").write_text(json.dumps({"title": "ThreadStartParams", "properties": props}))
            (out / "name.json").write_text(json.dumps({"title": "ThreadSetNameParams", "properties": {"threadId": {}, "name": {}}}))
        rpc = Mock()
        rpc.call.return_value = {"data": [{"id": self.config.project_id}]}
        with patch("compatibility.subprocess.run", side_effect=generate), patch("compatibility.RPC", return_value=rpc), patch("compatibility.probe") as ipc:
            check(self.config)
            self.assertEqual(rpc.call.call_args.args[0], "project/list")
            ipc.assert_called_once_with(self.config.ipc_socket)
            rpc.close.assert_called_once()

    def test_title_and_model_use_config(self):
        topic, _ = topic_title({"name": self.config.work_dir.name, "history": [{"role": "user", "content": "修复登录失败"}]}, generic_names={self.config.work_dir.name})
        self.assertEqual(display_title(topic, "s", set(), self.config.source_label), "团队消息｜修复登录失败")
        tid = str(uuid.uuid4())
        d = {"thread": {"id": tid, "name": "mirror", "cwd": str(self.config.work_dir), "createdAt": 1, "path": "fixture"}, "initial": [], "groups": list(completed([{"role": "user", "content": "q", "timestamp": "2026-01-01T00:00:00Z"}, {"role": "assistant", "content": "a", "timestamp": "2026-01-01T00:00:01Z"}]))}
        _, state = render(d, self.config)
        self.assertEqual(state["latestModel"], self.config.model)
        self.assertEqual(state["latestReasoningEffort"], self.config.reasoning_effort)
        self.assertNotIn("258400", json.dumps(state))

    def test_worker_sync_restart_and_archive(self):
        tid = str(uuid.uuid4())
        active = self.config.desktop_home / "sessions/mirror.jsonl"
        meta = {"type": "session_meta", "payload": {"id": tid}}
        active.write_text(json.dumps(meta) + "\n")
        with closing(sqlite3.connect(self.config.database)) as db, db:
            db.execute("INSERT INTO threads (id,rollout_path,archived) VALUES (?,?,0)", (tid, str(active)))
        thread = {"id": tid, "path": str(active), "name": "", "cwd": str(self.config.work_dir), "createdAt": 1}
        rpc = Mock()
        rpc.call.side_effect = lambda method, params: {"thread": thread} if method == "thread/start" else {}
        source = {"sessions": {"s1": {"name": "default", "agent_type": "codex", "agent_session_id": "source-id", "created_at": "time", "history": [{"role": "user", "content": "修复登录失败", "timestamp": "2026-01-01T00:00:00Z"}, {"role": "assistant", "content": "完成", "timestamp": "2026-01-01T00:00:01Z"}]}}}
        self.source.write_text(json.dumps(source))
        before_source = self.source.read_bytes()
        ipc = Mock(cid=None)
        with patch("service.RPC", return_value=rpc), patch("service.IPC", return_value=ipc):
            worker = Service(self.config)
            self.addCleanup(worker.guard.close)
            worker.tick()
            worker.tick()
            doc = worker.docs["s1|time"]
            self.assertEqual(len(doc["groups"]), 1)
            self.assertEqual(doc["thread"]["id"], tid)
            starts = [c for c in rpc.call.call_args_list if c.args[0] == "thread/start"]
            self.assertEqual(len(starts), 1)
            self.assertEqual(starts[0].args[1]["model"], self.config.model)
            worker.guard.close()
            restarted = Service(self.config)
            self.addCleanup(restarted.guard.close)
            restarted.tick()
            self.assertEqual(restarted.docs["s1|time"]["thread"]["id"], tid)
            archived = self.config.desktop_home / "archived_sessions/mirror.jsonl"
            active.replace(archived)
            with closing(sqlite3.connect(self.config.database)) as db, db:
                db.execute("UPDATE threads SET rollout_path=?,archived=1 WHERE id=?", (str(archived), tid))
            ipc.reset_mock()
            restarted.tick()
            self.assertFalse(active.exists())
            self.assertTrue(restarted.docs["s1|time"]["archived"])
            ipc.snapshot.assert_not_called()
            self.assertEqual(self.source.read_bytes(), before_source)

    def test_desktop_wait_retries_unavailable_socket_but_not_bad_protocol(self):
        before = self.fingerprint()
        with patch("compatibility.probe", side_effect=[FileNotFoundError(), None]) as ipc, patch("compatibility.time.sleep") as sleep:
            wait_for_desktop(self.config)
            self.assertEqual(ipc.call_count, 2)
            sleep.assert_called_once_with(2)
        with patch("compatibility.probe", side_effect=CompatibilityError("bad handshake")), patch("compatibility.time.sleep") as sleep:
            with self.assertRaises(CompatibilityError):
                wait_for_desktop(self.config)
            sleep.assert_not_called()
        self.assertEqual(before, self.fingerprint())

    def test_ipc_rejects_bad_handshake(self):
        path = self.root / "probe.sock"
        with socket.socket(socket.AF_UNIX) as server:
            server.bind(str(path))
            server.listen(1)
            def answer():
                conn, _ = server.accept()
                with conn:
                    def exact(n):
                        data = b""
                        while len(data) < n:
                            data += conn.recv(n - len(data))
                        return data
                    n = struct.unpack("<I", exact(4))[0]
                    req = json.loads(exact(n))
                    payload = json.dumps({"requestId": req["requestId"], "method": "initialize", "resultType": "error"}).encode()
                    conn.sendall(struct.pack("<I", len(payload)) + payload)
            t = threading.Thread(target=answer)
            t.start()
            try:
                with self.assertRaises(CompatibilityError):
                    probe(path)
            finally:
                t.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
