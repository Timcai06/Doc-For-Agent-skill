from __future__ import annotations

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


TEST_ROOT = Path(__file__).resolve().parents[1]
INSTALLER_ROOT = TEST_ROOT.parents[0] / "installer"

if str(INSTALLER_ROOT) not in sys.path:
    sys.path.insert(0, str(INSTALLER_ROOT))

from docagent import collect_doctor_statuses, main, render_doctor_report


class InstallerCliTests(unittest.TestCase):
    def test_collect_doctor_statuses_reports_install_targets(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-doctor-") as tmpdir:
            target_root = Path(tmpdir)
            statuses = collect_doctor_statuses(target_root, ["codex", "claude"])

            self.assertEqual([status.platform for status in statuses], ["codex", "claude"])
            self.assertFalse(statuses[0].installed)
            self.assertEqual(statuses[0].install_root, target_root / ".codex" / "skills" / "doc-for-agent")

    def test_render_doctor_report_mentions_continue(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-doctor-") as tmpdir:
            target_root = Path(tmpdir)
            report = render_doctor_report(target_root, collect_doctor_statuses(target_root, ["continue"]))

            self.assertIn("Continue (continue)", report)
            self.assertIn("assistant folder will be created", report)

    def test_install_command_writes_platform_bundle(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-install-") as tmpdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["install", "--platform", "codex", "--target", tmpdir])

            self.assertEqual(exit_code, 0)
            install_root = Path(tmpdir) / ".codex" / "skills" / "doc-for-agent"
            self.assertTrue((install_root / "SKILL.md").exists())
            self.assertTrue((install_root / "installer" / "docagent.py").exists())
            self.assertIn(str(install_root), stdout.getvalue())

    def test_doctor_command_prints_summary(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-install-") as tmpdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["doctor", "--platform", "claude", "--target", tmpdir])

            self.assertEqual(exit_code, 0)
            report = stdout.getvalue()
            self.assertIn("doc-for-agent doctor", report)
            self.assertIn("Claude Code (claude)", report)


if __name__ == "__main__":
    unittest.main()
