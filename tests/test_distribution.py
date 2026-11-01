"""Checks for supported installed combinations and distribution boundaries."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)

    def install(self, names):
        container = self.work / "installed"
        container.mkdir()
        for name in names:
            shutil.copytree(ROOT / "skills" / name, container / name)
        return container

    def test_complete_suite_and_minimum_workflow_combination(self):
        for names in (validate.SKILLS, {"sdlc-workflow", "sdlc-instr-doc-design"}):
            with self.subTest(names=names):
                container = self.install(names)
                self.assertEqual(validate.installation_errors(container), [])
                shutil.rmtree(container)

    def test_missing_dependency_is_reported(self):
        errors = validate.installation_errors(self.install({"sdlc-workflow"}))
        self.assertEqual(len(errors), 1)
        self.assertIn("requires sdlc-instr-doc-design", errors[0])
        self.assertIn("pause dependent work", errors[0])

    def test_specialists_install_independently(self):
        for name in validate.SKILLS - {"sdlc-workflow"}:
            with self.subTest(name=name):
                container = self.install({name})
                self.assertEqual(validate.installation_errors(container), [])
                shutil.rmtree(container)

    def test_package_links_cannot_escape_installation(self):
        container = self.install({"sdlc-instr-doc-design"})
        guide = container / "sdlc-instr-doc-design/SKILL.md"
        guide.write_text(guide.read_text() + "\n[unavailable](../outside.md)\n")
        self.assertTrue(any("escapes skill" in e for e in validate.installation_errors(container)))

    def test_source_contract(self):
        self.assertEqual(validate.validate(ROOT), [])

    def test_manifest_drift_and_missing_asset_fail_validation(self):
        fixture = self.work / "source"
        shutil.copytree(ROOT, fixture, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
        manifest = fixture / ".claude-plugin/plugin.json"
        manifest.write_text(manifest.read_text().replace('"version": "0.1.0"', '"version": "0.2.0"'))
        (fixture / "assets/icon.png").unlink()
        errors = validate.validate(fixture)
        self.assertIn("plugin manifest mismatch: version", errors)
        self.assertIn("Codex composerIcon: expected a bundled asset", errors)



if __name__ == "__main__":
    unittest.main()
