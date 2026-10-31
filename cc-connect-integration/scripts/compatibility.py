"""Fail-closed structural checks for the bundled Codex adapter."""
import json
import logging
import time
import os
from pathlib import Path
import subprocess
import tempfile
from config import CompatibilityError
from codex_rpc import RPC
from mirror_ipc import probe


def check_api_schema(config):
    # Schema generation operates on temporary output, not on installed services.
    with tempfile.TemporaryDirectory(prefix="cc-mirror-schema-") as out:
        env = {**os.environ, "CODEX_HOME": out}
        subprocess.run([str(config.codex_bin), "app-server", "generate-json-schema", "--experimental", "--out", out], check=True, timeout=60, capture_output=True, env=env)
        schemas = {}
        for p in Path(out).rglob("*.json"):
            doc = json.loads(p.read_text())
            if isinstance(doc, dict):
                schemas[doc.get("title", p.stem)] = doc
                schemas.update(doc.get("definitions", {}))
                schemas.update(doc.get("$defs", {}))
        requirements = {
            "ThreadStartParams": {"cwd", "projectId", "model", "config", "sandbox", "approvalPolicy", "historyMode", "baseInstructions"},
            "ThreadSetNameParams": {"threadId", "name"},
        }
        for name, properties in requirements.items():
            if not properties <= schemas.get(name, {}).get("properties", {}).keys():
                raise CompatibilityError(f"Required experimental API schema is missing or changed: {name}")
        start = schemas["ThreadStartParams"]
        # Resolve local schema references to inspect accepted legacy history mode.
        def resolve(node):
            if isinstance(node, dict):
                ref = node.get("$ref", "").rsplit("/", 1)[-1].removesuffix(".json")
                if ref in schemas:
                    return resolve(schemas[ref])
                return {k: resolve(v) for k, v in node.items()}
            if isinstance(node, list):
                return [resolve(v) for v in node]
            return node
        if '"legacy"' not in json.dumps(resolve(start["properties"]["historyMode"])):
            raise CompatibilityError("API does not advertise legacy history mode")


def check(config, live=True, probe_ipc=True):
    config.check_files()
    config.check_database()
    config.check_source()
    if live:
        check_api_schema(config)
        # These calls list metadata only; they do not start a model turn.
        rpc = RPC(config)
        try:
            projects = rpc.call("project/list", {})
            if config.project_id not in {p["id"] for p in projects.get("data", [])}:
                raise CompatibilityError("Target native project ID is not present in desktop_home")
        finally:
            rpc.close()
        if probe_ipc:
            probe(config.ipc_socket)


def wait_for_desktop(config):
    """Wait without writing mirrors; an incompatible handshake is never retried."""
    warned = False
    while True:
        try:
            probe(config.ipc_socket)
            return
        except OSError:
            if not warned:
                logging.info("Waiting for desktop IPC at %s", config.ipc_socket)
                warned = True
            time.sleep(2)
