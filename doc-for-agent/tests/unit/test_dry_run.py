from __future__ import annotations

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
            subprocess.run(["cp", "-R", str(FIXTURE_ROOT), str(sandbox_root)], check=True)

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


if __name__ == "__main__":
    unittest.main()
