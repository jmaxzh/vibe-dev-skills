"""CC Connect text transcript mirror using the legacy / IPC v11 adapter.

The source stays in its own CODEX_HOME. Only service-created legacy mirror
rollouts and their sidebar index rows are written. The durable journal is the
source of truth for mirrors; an app-owned rollout is never overwritten.
"""

from contextlib import closing
from pathlib import Path
import argparse, datetime, fcntl, hashlib, json, logging, os, threading, time, uuid
from codex_rpc import RPC
from mirror_ipc import state
from broker import RemoteIPC as IPC
from titles import topic_title, display_title
from config import Config, CompatibilityError


def atomic(path, data):
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    tmp.chmod(0o600)
    with tmp.open("r") as f:
        os.fsync(f.fileno())
    os.replace(tmp, path)


def seconds(ts):
    return int(datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp())


def completed(history):
    group = []
    for msg in history:
        if not group and msg["role"] != "user":
            continue
        group.append(msg)
        if msg["role"] == "assistant":
            if any(x["role"] == "user" for x in group):
                key = hashlib.sha256(json.dumps(group, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
                yield key, group
            group = []


def render(doc, config):
    t = doc["thread"]
    rows = list(doc["initial"])
    turns = []
    for key, group in doc["groups"]:
        tid = str(uuid.uuid5(uuid.UUID(t["id"]), key))
        start = seconds(group[0]["timestamp"])
        end = seconds(group[-1]["timestamp"])
        items = []

        def emit(ty, payload, ts):
            rows.append({"timestamp": ts, "type": ty, "payload": payload})

        emit(
            "event_msg",
            {
                "type": "task_started",
                "turn_id": tid,
                "started_at": start,
                "collaboration_mode_kind": "default",
            },
            group[0]["timestamp"],
        )
        for i, msg in enumerate(group):
            role = msg["role"]
            text = msg["content"]
            stamp = msg["timestamp"]
            iid = f"{tid}-{i}"
            if role == "user":
                emit(
                    "event_msg",
                    {"type": "user_message", "message": text, "images": [], "local_images": [], "text_elements": []},
                    stamp,
                )
                items.append(
                    {
                        "type": "userMessage",
                        "id": iid,
                        "clientId": None,
                        "content": [{"type": "text", "text": text, "text_elements": []}],
                    }
                )
            elif role == "assistant":
                emit("event_msg", {"type": "agent_message", "message": text, "phase": "final_answer"}, stamp)
                items.append(
                    {
                        "type": "agentMessage",
                        "id": iid,
                        "text": text,
                        "phase": "final_answer",
                        "memoryCitation": None,
                        "delivery": None,
                        "questions": None,
                    }
                )
        emit(
            "event_msg",
            {
                "type": "task_complete",
                "turn_id": tid,
                "last_agent_message": group[-1]["content"],
                "started_at": start,
                "completed_at": end,
                "duration_ms": max(0, end - start) * 1000,
            },
            group[-1]["timestamp"],
        )
        turns.append(
            {
                "id": tid,
                "rootTurnId": None,
                "items": items,
                "status": "completed",
                "error": None,
                "startedAt": start,
                "completedAt": end,
                "durationMs": max(0, end - start) * 1000,
            }
        )
    t = {**t, "turns": turns, "updatedAt": max(t["createdAt"], turns[-1]["completedAt"] if turns else 0)}
    return rows, state(t, config)


class Service:
    def __init__(self, config):
        self.config = config
        self.root = root = config.runtime_dir
        sessions = config.sessions
        config.check_database()
        config.check_source()
        root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.sessions = sessions
        self.guard = (root / "service.lock").open("a")
        fcntl.flock(self.guard, fcntl.LOCK_EX | fcntl.LOCK_NB)
        self.docs = {}
        self.states = {}
        self.pending = set()
        self.last_client = None
        self.ipc = IPC(self.states, config.runtime_dir / "broker.sock")
        for p in root.glob("mirror-*.json"):
            d = json.loads(p.read_text())
            self.docs[d["key"]] = d
            self.states[d["thread"]["id"]] = render(d, self.config)[1]
            self.pending.add(d["key"])
        threading.Thread(target=self.ipc.run, daemon=True).start()

    def save(self, d):
        atomic(self.root / f"mirror-{d['thread']['id']}.json", d)

    def create(self, key, s):
        r = RPC(self.config)
        try:
            t = r.call(
                "thread/start",
                {
                    "cwd": str(self.config.work_dir),
                    "projectId": self.config.project_id,
                    "model": self.config.model,
                    "config": {"model_reasoning_effort": self.config.reasoning_effort},
                    "sandbox": "read-only",
                    "approvalPolicy": "never",
                    "historyMode": "legacy",
                    "baseInstructions": "This is a read-only transcript mirror. Do not execute tools or continue the conversation. Continue in the source messaging platform.",
                },
            )["thread"]
            topic, _ = topic_title(s, generic_names={self.config.work_dir.name})
            title = display_title(topic, key.split("|", 1)[0], {d["thread"]["name"] for d in self.docs.values()}, self.config.source_label)
            r.call("thread/name/set", {"threadId": t["id"], "name": title})
            t["name"] = title
        finally:
            r.close()
        d = {
            "key": key,
            "source_id": s["agent_session_id"],
            "thread": t,
            "initial": self.config.checked_rollout(t["path"], t["id"])[1],
            "groups": [],
        }
        self.save(d)
        self.docs[key] = d
        self.states[t["id"]] = render(d, self.config)[1]
        logging.info("created mirror %s source=%s", t["id"], d["source_id"])
        return d

    def update_title(self, d, s):
        topic, meaningful = topic_title(s, d.get("topic_title"), generic_names={self.config.work_dir.name})
        others = {x["thread"]["name"] for x in self.docs.values() if x["key"] != d["key"]}
        # Keep an existing collision suffix stable across restarts.
        title = display_title(topic, d["key"].split("|", 1)[0], others, self.config.source_label)
        if d.get("topic_title") == topic and d["thread"]["name"].startswith(self.config.source_label + "｜" + topic + " · "):
            title = d["thread"]["name"]
        if d["thread"]["name"] == title and (not meaningful or d.get("topic_title") == topic):
            return
        r = RPC(self.config)
        try:
            r.call("thread/name/set", {"threadId": d["thread"]["id"], "name": title})
        finally:
            r.close()
        d["thread"]["name"] = title
        if meaningful:
            d["topic_title"] = topic
        self.save(d)
        self.pending.add(d["key"])
        self.publish(d)
        logging.info("updated topic title mirror=%s", d["thread"]["id"])

    def index(self, d):
        tid = d["thread"]["id"]
        updated = self.states[tid]["updatedAt"] // 1000
        with closing(self.config.connect_database()) as c, c:
            # Restrict every update to the exact ID AND path created by this service.
            first = next((m["content"] for _, g in d["groups"] for m in g if m["role"] == "user"), "")
            c.execute(
                "UPDATE threads SET has_user_event=1,updated_at=?,updated_at_ms=?,recency_at=?,recency_at_ms=?,title=?,first_user_message=?,preview=?,model=?,reasoning_effort=? WHERE id=? AND rollout_path=?",
                (
                    updated,
                    updated * 1000,
                    updated,
                    updated * 1000,
                    d["thread"]["name"],
                    first,
                    first[:500],
                    self.config.model,
                    self.config.reasoning_effort,
                    tid,
                    d["thread"]["path"],
                ),
            )

    def stored_thread(self, d):
        """The app owns archive status and rollout location, including moved files."""
        with closing(self.config.connect_database()) as c, c:
            row = c.execute(
                "SELECT rollout_path, archived FROM threads WHERE id=?",
                (d["thread"]["id"],),
            ).fetchone()
        if row is None:
            return None
        path = Path(row[0]).resolve()
        if not any(path.is_relative_to((self.config.desktop_home / folder).resolve()) for folder in ("sessions", "archived_sessions")):
            raise CompatibilityError("Mirror rollout is outside Codex session directories")
        changed = d["thread"]["path"] != str(path) or d.get("archived") != bool(row[1])
        d["thread"]["path"] = str(path)
        d["archived"] = bool(row[1])
        if changed:
            self.save(d)
        return row

    def project(self, d):
        tid = d["thread"]["id"]
        rows, _ = render(d, self.config)
        data = "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows)
        # Hold the writer lock only while replacing this mirror, never while idle.
        with (self.config.desktop_home / "thread-writer-locks" / f"{tid}.lock").open("a") as guard:
            try:
                fcntl.flock(guard, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return False
            if self.stored_thread(d) is None:
                return False
            path = Path(d["thread"]["path"])
            if not path.is_file():
                return False
            self.config.checked_rollout(path, tid)
            tmp = path.with_suffix(".mirror.tmp")
            try:
                tmp.write_text(data)
                tmp.chmod(0o600)
                with tmp.open("r") as f:
                    os.fsync(f.fileno())
                os.replace(tmp, path)
            finally:
                tmp.unlink(missing_ok=True)
        return True

    def publish(self, d):
        tid = d["thread"]["id"]
        if self.stored_thread(d) is None:
            return
        self.states[tid] = render(d, self.config)[1]
        self.index(d)
        if d["archived"]:
            return
        self.ipc.snapshot(tid)
        # Invalidate catalog queries without changing the user's archive decision.
        self.ipc.broadcast("query-cache-invalidate", {"queryKey": ["tasks"]}, 0)
        self.ipc.broadcast("query-cache-invalidate", {"queryKey": ["command-menu-thread-search", "local"]}, 0)

    def tick(self):
        self.config.check_database()
        self.config.check_source()
        for d in self.docs.values():
            was_archived = d.get("archived")
            old_path = d["thread"]["path"]
            if self.stored_thread(d) is not None and (was_archived != d["archived"] or old_path != d["thread"]["path"]):
                self.pending.add(d["key"])
        if self.ipc.cid and self.ipc.cid != self.last_client:
            for d in self.docs.values():
                self.publish(d)
            self.last_client = self.ipc.cid
        data = json.loads(self.sessions.read_text())
        for sid, s in data["sessions"].items():
            if s.get("agent_type") != "codex":
                continue
            groups = list(completed(s.get("history", [])))
            if not groups:
                continue
            key = sid + "|" + s["created_at"]
            d = self.docs.get(key) or self.create(key, s)
            self.update_title(d, s)
            seen = {x[0] for x in d["groups"]}
            fresh = [g for g in groups if g[0] not in seen]
            if fresh:
                d["groups"].extend(fresh)
                d["source_id"] = s["agent_session_id"]
                self.save(d)
                self.pending.add(key)
                logging.info(
                    "journal committed mirror=%s turns=%d added=%d", d["thread"]["id"], len(d["groups"]), len(fresh)
                )
                self.project(d)
                self.publish(d)
        for key in list(self.pending):
            d = self.docs[key]
            if self.project(d):
                self.publish(d)
                self.pending.discard(key)
                logging.info("projection current %s", d["thread"]["id"])
        atomic(
            self.root / "status.json",
            {
                "pid": os.getpid(),
                "updated_at": time.time(),
                "ipc_connected": self.ipc.cid is not None,
                "mirrors": [
                    {
                        "id": d["thread"]["id"],
                        "source_id": d["source_id"],
                        "turns": len(d["groups"]),
                        "projection_pending": d["key"] in self.pending,
                        "archived": d.get("archived", False),
                    }
                    for d in self.docs.values()
                ],
            },
        )

    def run(self):
        while True:
            try:
                self.tick()
            except CompatibilityError:
                raise
            except Exception:
                logging.exception("sync failed; retrying without changing source")
            time.sleep(2)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--check", action="store_true", help="Check compatibility without starting the sync worker")
    a = p.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    from compatibility import check, wait_for_desktop
    config = Config.load(a.config)
    check(config, probe_ipc=a.check)
    if a.check:
        print("Structural/API/IPC initialization checks passed; validate live display separately.")
    else:
        wait_for_desktop(config)
        Service(config).run()
