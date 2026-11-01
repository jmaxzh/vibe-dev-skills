import json, subprocess, threading, queue, time, os


class RPC:
    def __init__(self, config):
        env = os.environ.copy()
        env["CODEX_HOME"] = str(config.desktop_home)
        self.p = subprocess.Popen(
            [str(config.codex_bin), "app-server", "--listen", "stdio://"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            env=env,
        )
        self.q = queue.Queue()
        self.i = 0
        self.events = []
        threading.Thread(target=self._read, daemon=True).start()
        try:
            self._initialize()
        except Exception:
            self.close()
            raise

    def _initialize(self):
        self.call(
            "initialize",
            {
                "clientInfo": {"name": "cc_connect_mirror", "version": "0.1.0"},
                "capabilities": {"experimentalApi": True},
            },
        )
        self.send({"method": "initialized", "params": {}})

    def _read(self):
        for line in self.p.stdout:
            try:
                self.q.put(json.loads(line))
            except ValueError:
                pass

    def send(self, d):
        self.p.stdin.write(json.dumps(d) + "\n")
        self.p.stdin.flush()

    def call(self, m, p, timeout=60):
        self.i += 1
        i = self.i
        self.send({"id": i, "method": m, "params": p})
        end = time.monotonic() + timeout
        while True:
            d = self.q.get(timeout=max(0.01, end - time.monotonic()))
            if d.get("id") == i:
                if "error" in d:
                    raise RuntimeError(json.dumps(d["error"]))
                return d.get("result")
            self.events.append(d)

    def close(self):
        self.p.stdin.close()
        self.p.terminate()
        try:
            self.p.wait(timeout=10)
        except subprocess.TimeoutExpired:
            self.p.kill()
            self.p.wait()
        self.p.stdout.close()
