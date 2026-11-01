"""Check source layout, notices, manifests, translations, links, and skill composition."""
import argparse
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
SKILLS = frozenset({
    "sdlc-workflow", "sdlc-instr-doc-design", "sdlc-ui-interaction",
    "sdlc-mysql-design", "cc-connect-integration",
})


def dependency_errors(names):
    """Check the documented installation contract; never install anything."""
    if "sdlc-workflow" in names and "sdlc-instr-doc-design" not in names:
        return ["sdlc-workflow document work requires sdlc-instr-doc-design; "
                "install the full suite or both skills; pause dependent work"]
    return []


def metadata(text):
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    header = text.split("\n---\n", 1)[0][4:]
    values = {}
    for line in header.splitlines():
        key, sep, value = line.partition(":")
        if sep:
            values[key] = value.strip().strip('"\'')
    return values


def without_fences(text):
    return re.sub(r"```[^\n]*\n.*?```", "", text, flags=re.S)


def anchors(text):
    counts, result = {}, set()
    for title in re.findall(r"^#{1,6} (.+)$", without_fences(text), re.M):
        title = re.sub(r"<[^>]*>", "", title).replace("`", "").lower()
        slug = "".join(c for c in title if c in "-_" or
                       not unicodedata.category(c).startswith(("P", "S", "C")))
        slug = slug.replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        result.add(slug + (f"-{count}" if count else ""))
    return result


def link_errors(path, boundary=None):
    errors = []
    text = without_fences(path.read_text())
    for url in re.findall(r"\]\(([^)]+)\)", text):
        if "://" in url or url.startswith("mailto:"):
            continue
        name, _, fragment = unquote(url).partition("#")
        target = (path.parent / name).resolve() if name else path.resolve()
        if boundary and not target.is_relative_to(boundary.resolve()):
            errors.append(f"{path}: required file link escapes skill: {url}")
        elif not target.exists():
            errors.append(f"{path}: missing link: {url}")
        elif fragment and target.is_file() and fragment not in anchors(target.read_text()):
            errors.append(f"{path}: missing anchor: {url}")
    return errors


def installation_errors(container):
    """Validate an installed skill directory without relying on checkout siblings."""
    entries = list(container.glob("*/SKILL.md"))
    names = {p.parent.name for p in entries}
    errors = dependency_errors(names)
    for entry in entries:
        skill = entry.parent
        if not (skill / "LICENSE").is_file():
            errors.append(f"{skill}: missing license")
        for doc in skill.rglob("*.md"):
            errors.extend(link_errors(doc, skill))
    return errors


def translation_for(root, source):
    rel = source.relative_to(root)
    if rel.as_posix() == "README.md":
        return root / "README.zh-CN.md"
    if rel.as_posix() == "AGENTS.md":
        return root / "translations/zh-CN/AGENTS.zh-CN.md"
    target = root / "translations/zh-CN" / rel
    return target.with_name("SKILL.zh-CN.md") if target.name == "SKILL.md" else target


def validate(root=ROOT):
    errors = []
    entries = set(root.glob("skills/*/SKILL.md"))
    if {p.parent.name for p in entries} != SKILLS:
        errors.append("expected exactly five English skill entries")
    discovered = {p for p in root.rglob("SKILL.md")
                  if not any(x in p.relative_to(root).parts for x in (".git", "dist", "node_modules"))}
    if entries != discovered:
        errors.append("discoverable SKILL.md outside the five English skills")
    errors.extend(installation_errors(root / "skills"))
    for entry in sorted(entries):
        try:
            data = metadata(entry.read_text())
            if data.get("name") != entry.parent.name or not re.fullmatch(
                    r"[a-z0-9]+(?:-[a-z0-9]+)*", data.get("name", "")):
                errors.append(f"{entry}: invalid name")
            if len(data.get("name", "")) > 64 or not 1 <= len(data.get("description", "")) <= 1024:
                errors.append(f"{entry}: invalid metadata length")
            if data.get("license") != "MIT":
                errors.append(f"{entry}: missing MIT metadata")
        except ValueError as exc:
            errors.append(f"{entry}: {exc}")
        if (entry.parent / "LICENSE").read_bytes() != (root / "LICENSE").read_bytes():
            errors.append(f"{entry.parent}: license differs from root")
    sources = [root / "README.md", root / "AGENTS.md",
               *root.glob("skills/**/*.md"), *root.glob("docs/*.md")]
    for source in sources:
        translated = translation_for(root, source)
        if not translated.is_file():
            errors.append(f"{source}: missing maintenance translation")
        elif source.name != "README.md" and source.resolve() not in {
                (translated.parent / u).resolve() for u in re.findall(
                    r"\]\(([^)#]+)\)", without_fences(translated.read_text()))
                if "://" not in u}:
            errors.append(f"{translated}: missing English source link")
    for path in (root / "translations").rglob("*"):
        if path.is_file() and path.suffix != ".md":
            errors.append(f"{path}: translations must contain documentation only")
    for path in root.rglob("*.md"):
        if not any(x in path.relative_to(root).parts for x in (".git", "dist", "node_modules")):
            errors.extend(link_errors(path))
    portable = json.loads((root / "plugin.json").read_text())
    claude = json.loads((root / ".claude-plugin/plugin.json").read_text())
    for field in ("name", "version", "license", "author", "homepage", "repository"):
        if portable.get(field) != claude.get(field):
            errors.append(f"plugin manifest mismatch: {field}")
    if portable.get("name") != "vibe-dev-skills" or portable.get("license") != "MIT":
        errors.append("unexpected plugin identity/license")
    if not re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", portable.get("version", "")):
        errors.append("plugin version must be a stable semantic version")
    interface = portable.get("extensions", {}).get("com.openai", {}).get("interface", {})
    for field in ("composerIcon", "logo"):
        url = interface.get(field, "")
        asset = (root / url).resolve()
        if not url.startswith("./assets/") or not asset.is_relative_to(root.resolve()) or not asset.is_file():
            errors.append(f"OpenAI {field}: expected a bundled asset")
    for name in (".agents/plugins/marketplace.json", ".claude-plugin/marketplace.json"):
        market = json.loads((root / name).read_text())
        if market.get("name") != portable["name"] or len(market.get("plugins", [])) != 1:
            errors.append(f"{name}: expected one suite plugin")
            continue
        entry = market["plugins"][0]
        if entry.get("name") != portable["name"]:
            errors.append(f"{name}: plugin name mismatch")
        source = entry.get("source")
        expected = {"source": "local", "path": "./"} if name.startswith(".agents") else "./"
        if source != expected:
            errors.append(f"{name}: suite must resolve to repository root")
        if name.startswith(".claude") and (entry.get("version") != portable["version"] or
                market.get("metadata", {}).get("version") != portable["version"]):
            errors.append(f"{name}: marketplace version mismatch")
    workflow = (root / "skills/sdlc-workflow/SKILL.md").read_text()
    for phrase in ("sdlc-instr-doc-design", "actual registered name and namespace",
                   "pause only work", "download/install dependencies automatically"):
        if phrase not in workflow:
            errors.append(f"workflow missing dependency contract: {phrase}")
    return sorted(set(errors))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        errors = validate(args.root.resolve())
    except (OSError, KeyError, ValueError) as exc:
        parser.exit(1, f"Invalid source tree: {exc}\n")
    if errors:
        parser.exit(1, "\n".join(errors) + "\n")
    print("PASS: five English skills; dependency, notices, manifests, translations and links")


if __name__ == "__main__":
    main()
