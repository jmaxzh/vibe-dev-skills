"""Build a deterministic local plugin ZIP; never upload, submit, or publish."""
import argparse
import io
import json
from pathlib import Path
import zipfile

from validate import ROOT, SKILLS, validate


def package_files(root):
    files = [root / "LICENSE", root / "plugin.json", root / ".claude-plugin/plugin.json"]
    for name in sorted(SKILLS):
        for path in (root / "skills" / name).rglob("*"):
            if any(p.startswith(".") or p == "__pycache__" for p in path.relative_to(root).parts):
                continue
            if path.suffix in (".pyc", ".pyo"):
                continue
            if path.is_symlink():
                raise ValueError(f"Release files cannot be symlinks: {path}")
            if path.is_file():
                if path.suffix not in (".md", ".py") and path.name != "LICENSE":
                    raise ValueError(f"Unexpected skill file; review the release allowlist: {path}")
                files.append(path)
    if (root / "assets").exists():
        for path in (root / "assets").rglob("*"):
            if path.is_symlink():
                raise ValueError(f"Release assets cannot be symlinks: {path}")
            if path.is_file() and path.suffix in (".svg", ".png"):
                files.append(path)
    if any(path.is_symlink() for path in files):
        raise ValueError("Release manifests and notices must not be symlinks")
    return sorted(files, key=lambda p: p.relative_to(root).as_posix())


def build(root, output):
    errors = validate(root)
    if errors:
        raise ValueError("Source validation failed:\n" + "\n".join(errors))
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in package_files(root):
            info = zipfile.ZipInfo(path.relative_to(root).as_posix(), date_time=(2000, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    data = buffer.getvalue()
    if output.exists() and output.read_bytes() != data:
        raise ValueError("Output already exists with different content; choose a new path")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    version = json.loads((ROOT / "plugin.json").read_text())["version"]
    output = args.output or ROOT / "dist" / f"vibe-dev-skills-{version}.zip"
    try:
        print(build(ROOT, output.resolve()))
    except (OSError, ValueError) as exc:
        parser.exit(1, str(exc) + "\n")


if __name__ == "__main__":
    main()
