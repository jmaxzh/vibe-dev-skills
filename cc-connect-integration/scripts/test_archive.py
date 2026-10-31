from contextlib import closing
import fcntl
import json
import sqlite3
import tempfile
import unittest
import uuid
from pathlib import Path
from unittest.mock import Mock, patch
import service
from types import SimpleNamespace


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        for folder in ("sessions", "archived_sessions", "thread-writer-locks", "journal"):
            (self.root / folder).mkdir()
        self.tid = str(uuid.uuid4())
        self.active = self.root / "sessions/mirror.jsonl"
        self.active.write_text("initial\n")
        self.archived = self.root / "archived_sessions/mirror.jsonl"
        with closing(sqlite3.connect(self.root / "state_5.sqlite")) as c, c:
            c.execute("CREATE TABLE threads (id TEXT PRIMARY KEY, rollout_path TEXT, archived INTEGER)")
            c.execute("INSERT INTO threads VALUES (?, ?, 0)", (self.tid, str(self.active)))
        self.doc = {"key": "s1|time", "thread": {"id": self.tid, "path": str(self.active)}, "groups": []}
        self.worker = service.Service.__new__(service.Service)
        self.worker.config = SimpleNamespace(desktop_home=self.root, connect_database=lambda: sqlite3.connect(self.root / "state_5.sqlite"), checked_rollout=lambda path, tid: None)
        self.worker.root = self.root / "journal"
        self.worker.states = {}
        self.worker.ipc = Mock()
        self.worker.index = Mock()
        self.render = patch.object(service, "render", return_value=([{"copy": "latest"}], {"id": self.tid}))
        self.render.start()

    def tearDown(self):
        self.render.stop()
        self.tmp.cleanup()

    def assert_lock_free(self):
        with (self.root / "thread-writer-locks" / f"{self.tid}.lock").open("a") as f:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)

    def move(self, archived):
        old, new = (self.active, self.archived) if archived else (self.archived, self.active)
        old.replace(new)
        with closing(sqlite3.connect(self.root / "state_5.sqlite")) as c, c:
            c.execute("UPDATE threads SET rollout_path=?, archived=? WHERE id=?", (str(new), int(archived), self.tid))

    def test_idle_lock_released_after_sync_and_exception(self):
        self.assertTrue(self.worker.project(self.doc))
        self.assert_lock_free()
        with patch.object(service, "render", side_effect=RuntimeError("test write failure")):
            with self.assertRaises(RuntimeError):
                self.worker.project(self.doc)
        self.assert_lock_free()

    def test_archived_copy_updates_in_place_and_is_not_relisted(self):
        self.assertTrue(self.worker.project(self.doc))
        self.move(True)
        self.assertTrue(self.worker.project(self.doc))
        self.worker.publish(self.doc)
        self.assertFalse(self.active.exists())
        self.assertEqual(json.loads(self.archived.read_text()), {"copy": "latest"})
        self.assertTrue(self.doc["archived"])
        self.worker.ipc.snapshot.assert_not_called()
        self.worker.ipc.broadcast.assert_not_called()
        with closing(sqlite3.connect(self.root / "state_5.sqlite")) as c, c:
            self.assertEqual(c.execute("SELECT archived FROM threads").fetchone()[0], 1)
        # A restarted worker sees the same archived decision and location.
        restored = json.loads(next(self.worker.root.glob("mirror-*.json")).read_text())
        self.assertTrue(self.worker.project(restored))
        self.worker.publish(restored)
        self.worker.ipc.broadcast.assert_not_called()
        self.assert_lock_free()

    def test_user_unarchive_resumes_same_copy(self):
        self.move(True)
        self.worker.project(self.doc)
        self.move(False)
        self.worker.project(self.doc)
        self.worker.publish(self.doc)
        self.assertFalse(self.doc["archived"])
        self.worker.ipc.snapshot.assert_called_once_with(self.tid)
        self.assertTrue(all(c.args[0] != "thread-unarchived" for c in self.worker.ipc.broadcast.call_args_list))

    def test_competing_writer_is_respected(self):
        with (self.root / "thread-writer-locks" / f"{self.tid}.lock").open("a") as f:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.assertFalse(self.worker.project(self.doc))
            self.assertEqual(self.active.read_text(), "initial\n")

    def test_deleted_copy_is_not_recreated(self):
        with closing(sqlite3.connect(self.root / "state_5.sqlite")) as c, c:
            c.execute("DELETE FROM threads")
        self.active.unlink()
        self.assertFalse(self.worker.project(self.doc))
        self.worker.publish(self.doc)
        self.assertFalse(self.active.exists())
        self.worker.ipc.snapshot.assert_not_called()


if __name__ == "__main__":
    unittest.main()
