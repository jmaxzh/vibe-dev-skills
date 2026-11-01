import unittest, uuid
from service import completed, render
from types import SimpleNamespace

CONFIG = SimpleNamespace(model="example-model", reasoning_effort="example-effort")


class MirrorTests(unittest.TestCase):
    def message(self, role, text):
        return {"role": role, "content": text, "timestamp": "2026-10-24T01:00:00.12345+08:00"}

    def test_pending_user_waits_for_reply(self):
        self.assertEqual(list(completed([self.message("user", "pending")])), [])

    def test_repeated_poll_has_same_identity(self):
        h = [self.message("user", "u"), self.message("assistant", "a")]
        self.assertEqual(list(completed(h)), list(completed(h)))

    def test_retention_does_not_create_assistant_only_turn(self):
        h = [self.message("assistant", "old"), self.message("user", "u"), self.message("assistant", "a")]
        groups = list(completed(h))
        self.assertEqual(len(groups), 1)
        self.assertEqual([m["content"] for m in groups[0][1]], ["u", "a"])

    def test_same_mirror_and_turn_ids_after_restart(self):
        tid = str(uuid.uuid4())
        d = {
            "thread": {"id": tid, "name": "mirror", "cwd": "/tmp", "createdAt": 1, "path": "/tmp/mirror"},
            "initial": [],
            "groups": list(completed([self.message("user", "u"), self.message("assistant", "a")])),
        }
        rows, a = render(d, CONFIG)
        _, b = render(d, CONFIG)
        self.assertEqual(a["id"], tid)
        self.assertEqual(
            next(iter(a["turnHistory"]["history"]["entitiesByKey"].values()))["turnId"],
            next(iter(b["turnHistory"]["history"]["entitiesByKey"].values()))["turnId"],
        )
        self.assertEqual(next(iter(a["turnHistory"]["history"]["entitiesByKey"].values()))["items"][1]["text"], "a")
        self.assertEqual(rows[-1]["payload"]["type"], "task_complete")


if __name__ == "__main__":
    unittest.main()
