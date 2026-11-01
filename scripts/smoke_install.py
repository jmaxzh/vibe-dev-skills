"""Install into temporary configurations and record evidence, without model calls."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace

from validate import ROOT, SKILLS, installation_errors


def run(args, cwd, env):
    result = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, timeout=45)
    if result.returncode:
        raise RuntimeError(f"{' '.join(args)}\n{result.stdout}\n{result.stderr}")
    return re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", result.stdout)


def skills_checks(root, work, env, source):
    checks = []
    cli = ["npx", "--yes", "skills@1.7.4", "add", source]
    for extra in ([], ["--full-depth"]):
        output = run(cli + ["--list", *extra], work, env)
        if not re.search(r"Found 5 skills\b", output):
            raise RuntimeError("Expected exactly five discovered skills:\n" + output)
        checks.append("five-skill discovery" + (" (full depth)" if extra else ""))
    combinations = [("suite", SKILLS), ("workflow-pair", {"sdlc-workflow", "sdlc-instr-doc-design"})]
    combinations += [(name, {name}) for name in sorted(SKILLS - {"sdlc-workflow"})]
    combinations += [("missing-dependency", {"sdlc-workflow"})]
    for label, names in combinations:
        dest = work / label
        dest.mkdir()
        selected = ["*"] if label == "suite" else sorted(names)
        args = cli + ["--copy", "-a", "claude-code", "-y", "--skill", *selected]
        run(args, dest, env)
        container = dest / ".claude/skills"
        actual = {p.parent.name for p in container.glob("*/SKILL.md")}
        if actual != set(names):
            raise RuntimeError(f"{label}: wrong installed inventory: {actual}")
        errors = installation_errors(container)
        if label == "missing-dependency":
            if len(errors) != 1 or "requires sdlc-instr-doc-design" not in errors[0]:
                raise RuntimeError(f"Missing dependency not detected: {errors}")
        elif errors:
            raise RuntimeError("\n".join(errors))
        for name in names:
            if (container / name / "SKILL.md").read_bytes() != (root / "skills" / name / "SKILL.md").read_bytes():
                raise RuntimeError(f"{label}: entry differs from local source")
        checks.append(label + " installation and file/dependency check")
    return checks


def native_checks(root, work, env):
    results = []
    plugin = "vibe-dev-skills@vibe-dev-skills"
    if not shutil.which("codex") or not shutil.which("claude"):
        raise RuntimeError("--native requires codex and claude CLIs")
    run(["codex", "plugin", "marketplace", "add", str(root), "--json"], work, env)
    installed = json.loads(run(["codex", "plugin", "add", plugin, "--json"], work, env))
    errors = installation_errors(Path(installed["installedPath"]) / "skills")
    if errors:
        raise RuntimeError("\n".join(errors))
    results.append("Codex marketplace registration and native plugin installation")
    sys.path.insert(0, str(root / "skills/cc-connect-integration/scripts"))
    from codex_rpc import RPC
    # RPC sets CODEX_HOME from desktop_home, leaving the user's configuration intact.
    rpc = RPC(SimpleNamespace(codex_bin=Path(shutil.which("codex")), desktop_home=Path(env["CODEX_HOME"])))
    try:
        catalog = rpc.call("skills/list", {"cwds": [str(work)], "forceReload": True}, timeout=20)
        own = [s for group in catalog["data"] for s in group["skills"] if s.get("pluginId") == plugin]
        actual = {s["name"].split(":")[-1] for s in own}
        if actual != SKILLS or any(not s.get("enabled") for s in own):
            raise RuntimeError(f"Unexpected Codex runtime inventory: {actual}")
        for skill in own:
            if not Path(skill["path"]).is_file():
                raise RuntimeError("Codex returned an unreadable installed skill")
        results.append("Codex app-server catalog: five enabled namespaced skills with readable resources")
    finally:
        rpc.close()
    for target in (root / ".claude-plugin/plugin.json", root / ".claude-plugin/marketplace.json"):
        run(["claude", "plugin", "validate", str(target), "--strict", "--json"], work, env)
    run(["claude", "plugin", "marketplace", "add", str(root)], work, env)
    run(["claude", "plugin", "install", plugin], work, env)
    inventory = run(["claude", "plugin", "details", plugin], work, env)
    if "Skills (5)" not in inventory or any(name not in inventory for name in SKILLS):
        raise RuntimeError("Unexpected Claude Code component inventory:\n" + inventory)
    results.append("Claude Code strict validation, native installation, and five-skill inventory")
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native", action="store_true")
    parser.add_argument("--source", help="Optional Git URL/owner/repo for skills CLI checks; defaults to local checkout")
    parser.add_argument("--report", type=Path, default=ROOT / "dist/install-report.json")
    args = parser.parse_args()
    report = {"checks": [], "model_behavior": "not tested"}
    try:
        with tempfile.TemporaryDirectory(prefix="vibe-install-") as temp:
            work = Path(temp) / "work"
            work.mkdir()
            env = {**os.environ, "CODEX_HOME": str(Path(temp) / "codex"),
                   "CLAUDE_CONFIG_DIR": str(Path(temp) / "claude"),
                   "DISABLE_TELEMETRY": "1", "DISABLE_AUTOUPDATER": "1",
                   "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"}
            for key in ("CODEX_HOME", "CLAUDE_CONFIG_DIR"):
                Path(env[key]).mkdir()
            report["checks"].extend(skills_checks(ROOT, work, env, args.source or str(ROOT)))
            report["native_requested"] = args.native
            if args.native:
                report["versions"] = {tool: run([tool, "--version"], work, env).strip()
                                      for tool in ("codex", "claude")}
                report["checks"].extend(native_checks(ROOT, work, env))
        report["passed"] = True
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        report.update(passed=False, error=str(exc))
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
