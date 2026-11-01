import socket, struct, json, uuid, threading, time, logging
from pathlib import Path


class IPC:
    def __init__(self, states, socket_path):
        self.socket_path = socket_path
        self.states = states
        self.cid = None
        self.sock = None
        self.lock = threading.Lock()
        self.followers = {}
        self.revision = 1

    def send(self, x):
        b = json.dumps(x, ensure_ascii=False).encode()
        with self.lock:
            self.sock.sendall(struct.pack("<I", len(b)) + b)

    def broadcast(self, method, params, version, targets=None):
        if not self.cid:
            return
        x = {"type": "broadcast", "method": method, "sourceClientId": self.cid, "version": version, "params": params}
        if targets:
            x["targetClientIds"] = targets
        self.send(x)

    def snapshot(self, tid, targets=None):
        if tid in self.states:
            self.revision += 1
            self.broadcast(
                "thread-stream-state-changed",
                {
                    "conversationId": tid,
                    "hostId": "local",
                    "change": {"type": "snapshot", "revision": self.revision, "conversationState": self.states[tid]},
                },
                11,
                targets,
            )
            logging.info("snapshot %s rev=%s targets=%s", tid, self.revision, targets)

    def run(self):
        while True:
            try:
                self.connect()
            except Exception as e:
                logging.warning("IPC reconnect: %s", e)
            self.cid = None
            if self.sock:
                self.sock.close()
            time.sleep(2)

    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX)
        self.sock.connect(str(self.socket_path))
        self.send(
            {
                "type": "request",
                "requestId": str(uuid.uuid4()),
                "sourceClientId": "initializing-client",
                "version": 0,
                "method": "initialize",
                "params": {"clientType": "cc-connect-mirror"},
            }
        )

        def exact(n):
            b = b""
            while len(b) < n:
                c = self.sock.recv(n - len(b))
                if not c:
                    raise EOFError()
                b += c
            return b

        while True:
            x = json.loads(exact(struct.unpack("<I", exact(4))[0]))
            ty = x.get("type")
            m = x.get("method")
            p = x.get("params", {})
            if ty == "response" and m == "initialize":
                if x.get("resultType") == "error" or not x.get("result", {}).get("clientId"):
                    raise RuntimeError("Incompatible IPC initialize response")
                self.cid = x["result"]["clientId"]
                logging.info("IPC registered %s", self.cid)
                for tid in self.states:
                    self.broadcast(
                        "thread-stream-following-status-requested", {"conversationId": tid, "hostId": "local"}, 1
                    )
            elif ty == "client-discovery-request":
                q = x["request"]
                tid = q.get("params", {}).get("conversationId")
                can = tid in self.states and (
                    q["method"] == "thread-owner-discovery" or q["method"].startswith("thread-follower-")
                )
                self.send(
                    {"type": "client-discovery-response", "requestId": x["requestId"], "response": {"canHandle": can}}
                )
                if can:
                    logging.info("discovery %s %s", tid, q["method"])
            elif ty == "request":
                tid = p.get("conversationId")
                ans = {"type": "response", "requestId": x["requestId"], "method": m, "handledByClientId": self.cid}
                if tid in self.states and m == "thread-owner-discovery":
                    ans.update(resultType="success", result={"supportsUntrustedAppInput": False})
                elif tid in self.states and m == "thread-follower-load-complete-history":
                    self.snapshot(tid, [x["sourceClientId"]])
                    ans.update(resultType="success", result={"revision": self.revision})
                else:
                    ans.update(resultType="error", error="此会话是消息平台的只读副本，请在来源平台继续对话。")
                self.send(ans)
                logging.info("request %s %s", tid, m)
            elif (
                ty == "broadcast" and m == "thread-stream-following-changed" and p.get("conversationId") in self.states
            ):
                tid = p["conversationId"]
                logging.info("following %s %s %s", tid, p.get("following"), x["sourceClientId"])
                if p.get("following"):
                    self.snapshot(tid, [x["sourceClientId"]])


def state(t, config):
    turns = []
    for turn in t["turns"]:
        items = turn["items"]
        user = next((i for i in items if i["type"] == "userMessage"), {})
        turns.append(
            {
                "turnId": turn["id"],
                "rootTurnId": turn.get("rootTurnId"),
                "params": {
                    "threadId": t["id"],
                    "input": user.get("content", []),
                    "model": config.model,
                    "cwd": t["cwd"],
                    "attachments": [],
                },
                "permissionParamsSource": "inferred",
                "turnStartedAtMs": (turn.get("startedAt") or 0) * 1000,
                "durationMs": turn.get("durationMs"),
                "finalAssistantStartedAtMs": (turn.get("completedAt") or 0) * 1000,
                "status": turn["status"],
                "error": turn.get("error"),
                "diff": None,
                "items": items,
                "completedItemIds": {i["id"]: True for i in items},
                "itemsPagination": {"olderCursor": None, "isLoadingOlder": False, "hasLoadedOldest": True},
            }
        )
    result = {
        "id": t["id"],
        "sessionId": t["id"],
        "hostId": "local",
        "turns": turns,
        "requests": [],
        "createdAt": t["createdAt"] * 1000,
        "updatedAt": t["updatedAt"] * 1000,
        "recencyAt": t["updatedAt"] * 1000,
        "title": t["name"],
        "originator": "cc-connect-mirror",
        "source": "vscode",
        "historyMode": "legacy",
        "canonicalVoiceHistory": False,
        "modelProvider": "openai",
        "latestModel": config.model,
        "latestReasoningEffort": config.reasoning_effort,
        "hasUnreadTurn": False,
        "threadRuntimeStatus": {"type": "idle"},
        "rolloutPath": t["path"],
        "resumeState": "resumed",
        "workspaceKind": "project",
        "cwd": t["cwd"],
        "turnsPagination": {
            "olderCursor": None,
            "oldestLoadedTurnId": None,
            "isLoadingOlder": False,
            "hasLoadedOldest": True,
        },
        "latestCollaborationMode": {
            "mode": "default",
            "settings": {"model": config.model, "reasoning_effort": config.reasoning_effort, "developer_instructions": None},
        },
    }

    result["turnHistory"] = {
        "kind": "canonical",
        "history": {
            "generation": 0,
            "isComplete": True,
            "entitiesByKey": {"turn:" + x["turnId"]: x for x in turns},
            "islands": [
                {
                    "id": "tail:0",
                    "entries": [{"key": "turn:" + x["turnId"], "value": "turn:" + x["turnId"]} for x in turns],
                    "olderBoundary": {"status": "exhausted", "boundaryId": "tail:0:older"},
                    "newerBoundary": {"status": "exhausted", "boundaryId": "tail:0:newer"},
                }
            ],
        },
    }
    result["turns"] = []
    result.update(
        ephemeral=False,
        mode="default",
        threadStartKind="default",
        threadSource=None,
        environments=[{"environmentId": "local", "cwd": t["cwd"], "runtimeWorkspaceRoots": [t["cwd"]]}],
    )
    return result


def probe(path):
    """Check framing and initialization only; this cannot prove all v11 semantics."""
    from config import CompatibilityError
    with socket.socket(socket.AF_UNIX) as sock:
        sock.settimeout(5)
        sock.connect(str(path))
        rid = str(uuid.uuid4())
        payload = json.dumps({"type": "request", "requestId": rid, "sourceClientId": "initializing-client", "version": 0, "method": "initialize", "params": {"clientType": "cc-connect-mirror-probe"}}).encode()
        sock.sendall(struct.pack("<I", len(payload)) + payload)
        def exact(n):
            data = b""
            while len(data) < n:
                chunk = sock.recv(n - len(data))
                if not chunk:
                    raise CompatibilityError("IPC closed during handshake")
                data += chunk
            return data
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            size = struct.unpack("<I", exact(4))[0]
            if size > 16 * 1024 * 1024:
                raise CompatibilityError("Unexpected IPC frame size")
            reply = json.loads(exact(size))
            if reply.get("requestId") == rid and reply.get("method") == "initialize":
                if not reply.get("result", {}).get("clientId") or reply.get("resultType") == "error":
                    raise CompatibilityError("Incompatible IPC initialize response")
                return
        raise CompatibilityError("IPC initialize response not received")
