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

from docagent import collect_doctor_statuses, main, render_doctor_report, render_versions_report


class InstallerCliTests(unittest.TestCase):
    def test_collect_doctor_statuses_reports_install_targets(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-doctor-") as tmpdir:
            target_root = Path(tmpdir)
            statuses = collect_doctor_statuses(target_root, ["codex", "claude"])

            self.assertEqual([status.platform for status in statuses], ["codex", "claude"])
            self.assertFalse(statuses[0].installed)
            self.assertEqual(statuses[0].install_root, target_root / ".codex" / "skills" / "doc-for-agent")
            self.assertIsNone(statuses[0].installed_version)

    def test_render_doctor_report_mentions_continue(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-doctor-") as tmpdir:
            target_root = Path(tmpdir)
            report = render_doctor_report(target_root, collect_doctor_statuses(target_root, ["continue"]))

            self.assertIn("Continue (continue)", report)
            self.assertIn("assistant folder will be created", report)
            self.assertIn("Version: 0.2.0.dev0", report)

    def test_install_command_writes_platform_bundle(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-install-") as tmpdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["install", "--platform", "codex", "--target", tmpdir])

            self.assertEqual(exit_code, 0)
            install_root = Path(tmpdir) / ".codex" / "skills" / "doc-for-agent"
            self.assertTrue((install_root / "SKILL.md").exists())
            self.assertTrue((install_root / "installer" / "docagent.py").exists())
            self.assertTrue((install_root / "INSTALLATION.json").exists())
            self.assertIn(str(install_root), stdout.getvalue())
            self.assertIn("Next steps:", stdout.getvalue())

    def test_doctor_command_prints_summary(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-install-") as tmpdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["doctor", "--platform", "claude", "--target", tmpdir])

            self.assertEqual(exit_code, 0)
            report = stdout.getvalue()
            self.assertIn("doc-for-agent doctor", report)
            self.assertIn("Claude Code (claude)", report)

    def test_all_command_installs_every_supported_platform(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-install-") as tmpdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["all", "--target", tmpdir])

            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(tmpdir) / ".codex" / "skills" / "doc-for-agent" / "SKILL.md").exists())
            self.assertTrue((Path(tmpdir) / ".claude" / "skills" / "doc-for-agent" / "SKILL.md").exists())
            self.assertTrue((Path(tmpdir) / ".continue" / "skills" / "doc-for-agent" / "SKILL.md").exists())
            self.assertIn("Platforms: claude, codex, continue", stdout.getvalue())

    def test_versions_report_reads_installed_receipt(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-install-") as tmpdir:
            main(["install", "--platform", "codex", "--target", tmpdir])
            report = render_versions_report(Path(tmpdir), collect_doctor_statuses(Path(tmpdir), ["codex"]))

            self.assertIn("Source version: 0.2.0.dev0", report)
            self.assertIn("Codex (codex): 0.2.0.dev0", report)

    def test_versions_command_prints_summary(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-install-") as tmpdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["versions", "--platform", "continue", "--target", tmpdir])

            self.assertEqual(exit_code, 0)
            report = stdout.getvalue()
            self.assertIn("doc-for-agent versions", report)
            self.assertIn("Continue (continue): not installed", report)

    def test_update_command_refreshes_installed_platforms(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-install-") as tmpdir:
            main(["install", "--platform", "codex", "--target", tmpdir])

            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["update", "--platform", "codex", "--target", tmpdir])

            self.assertEqual(exit_code, 0)
            report = stdout.getvalue()
            self.assertIn("doc-for-agent update", report)
            self.assertIn("Platforms: codex", report)
            self.assertIn("Updated platform adapters:", report)

    def test_update_command_without_installs_returns_nonzero(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-install-") as tmpdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["update", "--platform", "all", "--target", tmpdir])

            self.assertEqual(exit_code, 1)
            self.assertIn("No installed platforms were detected", stdout.getvalue())

    def test_version_flag_prints_product_version(self) -> None:
        with self.assertRaises(SystemExit) as context:
            main(["--version"])

        self.assertEqual(context.exception.code, 0)

    def test_generate_command_executes_generator_dry_run(self) -> None:
        fixture_root = TEST_ROOT / "fixtures" / "backend_service"
        agents_dir = fixture_root / "AGENTS"
        if agents_dir.exists():
            self.fail(f"Fixture unexpectedly contains AGENTS directory: {agents_dir}")

        exit_code = main(["generate", "--root", str(fixture_root), "--dry-run"])

        self.assertEqual(exit_code, 0)
        self.assertFalse(agents_dir.exists())

    def test_refresh_command_executes_refresh_mode_dry_run(self) -> None:
        fixture_root = TEST_ROOT / "fixtures" / "cli_tool"
        agents_dir = fixture_root / "AGENTS"
        if agents_dir.exists():
            self.fail(f"Fixture unexpectedly contains AGENTS directory: {agents_dir}")

        exit_code = main(["refresh", "--root", str(fixture_root), "--dry-run"])

        self.assertEqual(exit_code, 0)
        self.assertFalse(agents_dir.exists())


if __name__ == "__main__":
    unittest.main()
