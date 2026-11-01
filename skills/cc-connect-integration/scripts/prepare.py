"""Generate a relocatable deployment bundle; never install or start services."""
import argparse
import json
import os
from pathlib import Path
import plistlib
import shutil
import sys
from types import SimpleNamespace
from config import Config
from codex_rpc import RPC


def prepare(config_path, output, launchd=False, path_entries=()):
    config = Config.load(config_path)
    config.check_files()
    config.check_database()
    config.check_source()
    out = Path(output).expanduser().absolute()
    if out.exists():
        raise ValueError("Output already exists; choose a new directory")
    # No changes to runtime_dir, CC config, credentials, source sessions or desktop.
    out.mkdir(parents=True, mode=0o700)
    try:
        code = out / "bin"
        code.mkdir()
        for source in Path(__file__).resolve().parent.glob("*.py"):
            shutil.copy2(source, code / source.name)
        deployment = out / "deployment.json"
        deployment.write_text(json.dumps(config.as_dict(), ensure_ascii=False, indent=2) + "\n")
        deployment.chmod(0o600)
        if launchd:
            generate_launchd(config, out, path_entries)
    except Exception:
        shutil.rmtree(out)
        raise
    return out


def generate_launchd(config, out, path_entries):
    folder = out / "LaunchAgents"
    folder.mkdir()
    runtime = config.runtime_dir
    config_path = runtime / "deployment.json"
    paths = [str(p) for p in path_entries] + [str(config.codex_bin.parent), str(config.cc_bin.parent), str(config.python_bin.parent)] + os.defpath.split(os.pathsep)
    for role, args in (
        ("connect", [str(config.cc_bin), "--config", str(config.cc_config)]),
        ("broker", [str(config.python_bin), "-u", str(runtime / "bin/broker.py"), "--config", str(config_path)]),
        ("sync", [str(config.python_bin), "-u", str(runtime / "bin/service.py"), "--config", str(config_path)]),
    ):
        label = config.service_prefix + "." + role
        env = {"PATH": os.pathsep.join(dict.fromkeys(paths))}
        if role == "connect":
            env["CODEX_HOME"] = str(config.execution_home)
        data = {
            "Label": label, "ProgramArguments": args,
            "WorkingDirectory": str(config.work_dir if role == "connect" else runtime),
            "EnvironmentVariables": env, "RunAtLoad": True,
            # Exit on compatibility failures rather than automatically retrying writes.
            "KeepAlive": False,
            "StandardOutPath": str(runtime / (role + ".log")),
            "StandardErrorPath": str(runtime / (role + ".log")),
        }
        (folder / (label + ".plist")).write_bytes(plistlib.dumps(data))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--launchd", action="store_true", help="Generate macOS user-service files only")
    parser.add_argument("--path-entry", type=Path, action="append", default=[], help="Extra absolute directory for wrappers such as Node.js")
    parser.add_argument("--list-projects", action="store_true")
    parser.add_argument("--codex-bin", type=Path)
    parser.add_argument("--desktop-home", type=Path)
    a = parser.parse_args()
    if a.list_projects:
        if not a.codex_bin or not a.desktop_home:
            parser.error("--list-projects requires --codex-bin and --desktop-home")
        config = SimpleNamespace(codex_bin=a.codex_bin.expanduser().resolve(), desktop_home=a.desktop_home.expanduser().resolve())
        if not config.codex_bin.is_file() or not config.desktop_home.is_dir():
            parser.error("Executable and desktop home must exist")
        rpc = RPC(config)
        try:
            for project in rpc.call("project/list", {}).get("data", []):
                print(json.dumps({"name": project.get("name"), "id": project["id"]}, ensure_ascii=False))
        finally:
            rpc.close()
        return
    if not a.config or not a.output:
        parser.error("--config and --output are required when preparing files")
    for path in a.path_entry:
        if not path.is_absolute() or not path.is_dir():
            parser.error("--path-entry must be an existing absolute directory")
    if a.launchd and sys.platform != "darwin":
        parser.error("Bundled service generation supports macOS launchd only")
    print("Prepared files:", prepare(a.config, a.output, a.launchd, a.path_entry))
    print("No installed files or running services were changed.")


if __name__ == "__main__":
    main()
