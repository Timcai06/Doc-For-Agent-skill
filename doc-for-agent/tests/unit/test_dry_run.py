from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


TEST_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = TEST_ROOT.parents[1]
GENERATOR = REPO_ROOT / "doc-for-agent/scripts/init_agents_docs.py"
FIXTURE_ROOT = TEST_ROOT / "fixtures" / "cli_tool"


class DryRunTests(unittest.TestCase):
    def test_dry_run_reports_planned_files_without_writing_agents_directory(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-dry-run-") as tmpdir:
            sandbox_root = Path(tmpdir) / "cli_tool"
            shutil.copytree(FIXTURE_ROOT, sandbox_root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(GENERATOR),
                    "--root",
                    str(sandbox_root),
                    "--mode",
                    "refresh",
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("Dry run: would refresh AGENTS docs", result.stdout)
            self.assertIn("create AGENTS/README.md", result.stdout)
            self.assertFalse((sandbox_root / "AGENTS").exists())

    def test_explain_and_repo_type_override_can_be_combined_with_dry_run(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-explain-") as tmpdir:
            sandbox_root = Path(tmpdir) / "hybrid_skill_cli"
            shutil.copytree(TEST_ROOT / "fixtures" / "hybrid_skill_cli", sandbox_root)
            agents_root = sandbox_root / "AGENTS"
            before_files = sorted(
                str(path.relative_to(agents_root))
                for path in agents_root.rglob("*")
                if path.is_file()
            )
            before_contents = {
                relative: (agents_root / relative).read_text(encoding="utf-8")
                for relative in before_files
            }

            result = subprocess.run(
                [
                    sys.executable,
                    str(GENERATOR),
                    "--root",
                    str(sandbox_root),
                    "--mode",
                    "refresh",
                    "--repo-type",
                    "cli-tool",
                    "--explain",
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("Repo type: `cli-tool`", result.stdout)
            self.assertIn("Repo type overridden via CLI: `cli-tool`.", result.stdout)
            self.assertIn("Automatic classification would have selected `skill-meta` instead.", result.stdout)
            self.assertIn("Suggested profile: `bootstrap`", result.stdout)
            self.assertIn("Suggested command: python3 doc-for-agent/scripts/init_agents_docs.py --root", result.stdout)
            self.assertIn("Suggested source-of-truth files:", result.stdout)
            self.assertIn("has package bin metadata: no", result.stdout)
            after_files = sorted(
                str(path.relative_to(agents_root))
                for path in agents_root.rglob("*")
                if path.is_file()
            )
            after_contents = {
                relative: (agents_root / relative).read_text(encoding="utf-8")
                for relative in after_files
            }
            self.assertEqual(before_files, after_files)
            self.assertEqual(before_contents, after_contents)

    def test_layered_profile_dry_run_reports_nested_agents_files_without_writing(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-layered-dry-run-") as tmpdir:
            sandbox_root = Path(tmpdir) / "layered_product_app"
            shutil.copytree(TEST_ROOT / "fixtures" / "layered_product_app", sandbox_root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(GENERATOR),
                    "--root",
                    str(sandbox_root),
                    "--mode",
                    "refresh",
                    "--profile",
                    "layered",
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("create AGENTS/00-entry/AGENTS.md", result.stdout)
            self.assertIn("create AGENTS/04-memory/010-lessons.md", result.stdout)
            self.assertFalse((sandbox_root / "AGENTS").exists())


if __name__ == "__main__":
    unittest.main()
