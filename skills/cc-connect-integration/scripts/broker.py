"""Long-lived Desktop subscription owner; worker restarts do not drop IPC."""

from pathlib import Path
import json, socket, threading, logging, os, fcntl
from mirror_ipc import IPC



class RemoteIPC:
    def __init__(self, states, socket_path):
        self.states = states
        self.socket_path = socket_path

    def request(self, msg):
        with socket.socket(socket.AF_UNIX) as s:
            s.settimeout(10)
            s.connect(str(self.socket_path))
            s.sendall(json.dumps(msg, ensure_ascii=False).encode() + b"\n")
            f = s.makefile("rb")
            r = json.loads(f.readline())
            if r.get("error"):
                raise RuntimeError(r["error"])
            return r

    @property
    def cid(self):
        try:
            return self.request({"op": "ping"}).get("cid")
        except (OSError, ValueError):
            return None

    def run(self):
        pass

    def snapshot(self, tid, targets=None):
        self.request({"op": "snapshot", "tid": tid, "state": self.states[tid], "targets": targets})

    def broadcast(self, method, params, version, targets=None):
        self.request({"op": "broadcast", "method": method, "params": params, "version": version, "targets": targets})


def main(config):
    ROOT = config.runtime_dir
    SOCKET = ROOT / "broker.sock"
    ROOT.mkdir(parents=True, exist_ok=True, mode=0o700)
    guard = (ROOT / "broker.lock").open("a")
    fcntl.flock(guard, fcntl.LOCK_EX | fcntl.LOCK_NB)
    states = {}
    saved = ROOT / "broker-state.json"
    if saved.exists():
        states.update(json.loads(saved.read_text()))
    ipc = IPC(states, config.ipc_socket)
    threading.Thread(target=ipc.run, daemon=True).start()
    SOCKET.unlink(missing_ok=True)
    with socket.socket(socket.AF_UNIX) as server:
        server.bind(str(SOCKET))
        SOCKET.chmod(0o600)
        server.listen(8)
        while True:
            conn, _ = server.accept()
            with conn:
                try:
                    conn.settimeout(10)
                    q = json.loads(conn.makefile("rb").readline())
                    op = q["op"]
                    if op == "snapshot":
                        states[q["tid"]] = q["state"]
                        tmp = saved.with_suffix(".tmp")
                        tmp.write_text(json.dumps(states, ensure_ascii=False))
                        tmp.chmod(0o600)
                        os.replace(tmp, saved)
                        ipc.snapshot(q["tid"], q.get("targets"))
                    elif op == "broadcast":
                        ipc.broadcast(q["method"], q["params"], q["version"], q.get("targets"))
                    conn.sendall(json.dumps({"cid": ipc.cid}).encode() + b"\n")
                except Exception as e:
                    logging.exception("broker request failed")
                    try:
                        conn.sendall(json.dumps({"error": str(e)}).encode() + b"\n")
                    except OSError:
                        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    import argparse
    from config import Config
    from compatibility import check
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    config = Config.load(parser.parse_args().config)
    check(config, probe_ipc=False)
    main(config)
