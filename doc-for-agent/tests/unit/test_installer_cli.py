from __future__ import annotations

import io
import json
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
    def test_help_mentions_v1_primary_and_legacy_commands(self) -> None:
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            with self.assertRaises(SystemExit) as context:
                main(["--help"])

        self.assertEqual(context.exception.code, 0)
        text = stdout.getvalue()
        self.assertIn("usage: docagent", text)
        self.assertNotIn("usage: docagent.py", text)
        self.assertIn("Product CLI v1", text)
        self.assertIn("primary commands: init, refresh, doctor, generate, update, versions", text)
        self.assertIn("legacy compatibility: install, all", text)
        self.assertIn("30-second start:", text)
        self.assertIn("docagent init --ai <claude|codex|continue|copilot|all> --target <repo-root>", text)

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
            self.assertIn("Compatibility mode", stdout.getvalue())
            self.assertIn("Next steps:", stdout.getvalue())

    def test_init_command_installs_selected_platform(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-init-") as tmpdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["init", "--ai", "claude", "--target", tmpdir])

            self.assertEqual(exit_code, 0)
            install_root = Path(tmpdir) / ".claude" / "skills" / "doc-for-agent"
            self.assertTrue((install_root / "SKILL.md").exists())
            text = stdout.getvalue()
            self.assertIn("doc-for-agent init", text)
            self.assertIn("Selected AI platforms: claude", text)
            self.assertIn("Recommended next commands:", text)

    def test_doctor_command_prints_summary(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-install-") as tmpdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["doctor", "--platform", "claude", "--target", tmpdir])

            self.assertEqual(exit_code, 0)
            report = stdout.getvalue()
            self.assertIn("doc-for-agent doctor", report)
            self.assertIn("Claude Code (claude)", report)

    def test_doctor_command_can_inspect_global_install_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-global-doctor-") as tmpdir:
            main(["global-install", "--ai", "codex", "--global-root", tmpdir])
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["doctor", "--platform", "codex", "--global", "--global-root", tmpdir])

            self.assertEqual(exit_code, 0)
            report = stdout.getvalue()
            self.assertIn("doc-for-agent doctor", report)
            self.assertIn("Codex (codex): installed", report)
            self.assertIn(str((Path(tmpdir) / ".codex" / "skills" / "doc-for-agent").resolve()), report)

    def test_all_command_installs_every_supported_platform(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-install-") as tmpdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["all", "--target", tmpdir])

            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(tmpdir) / ".codex" / "skills" / "doc-for-agent" / "SKILL.md").exists())
            self.assertTrue((Path(tmpdir) / ".claude" / "skills" / "doc-for-agent" / "SKILL.md").exists())
            self.assertTrue((Path(tmpdir) / ".continue" / "skills" / "doc-for-agent" / "SKILL.md").exists())
            self.assertTrue((Path(tmpdir) / ".github" / "prompts" / "doc-for-agent" / "PROMPT.md").exists())
            self.assertIn("Platforms: claude, codex, continue, copilot", stdout.getvalue())

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

    def test_versions_command_can_inspect_global_install_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-global-versions-") as tmpdir:
            main(["global-install", "--ai", "codex", "--global-root", tmpdir])
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["versions", "--platform", "codex", "--global", "--global-root", tmpdir])

            self.assertEqual(exit_code, 0)
            report = stdout.getvalue()
            self.assertIn("doc-for-agent versions", report)
            self.assertIn("Codex (codex): 0.2.0.dev0", report)

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
            self.assertIn("Run `init --ai all` first", stdout.getvalue())

    def test_version_flag_prints_product_version(self) -> None:
        with self.assertRaises(SystemExit) as context:
            main(["--version"])

        self.assertEqual(context.exception.code, 0)

    def test_npm_wrapper_surface_exists(self) -> None:
        repo_root = TEST_ROOT.parents[1]
        package_json = repo_root / "package.json"
        self.assertTrue(package_json.exists())

        payload = json.loads(package_json.read_text(encoding="utf-8"))
        self.assertEqual(payload["bin"]["docagent"], "doc-for-agent/installer/node/docagent.js")
        self.assertEqual(payload["bin"]["doc-for-agent"], "doc-for-agent/installer/node/docagent.js")
        self.assertEqual(payload["scripts"]["prepack"], "python3 doc-for-agent/installer/sync_assets.py")
        self.assertEqual(payload["scripts"]["quickstart"], "node doc-for-agent/installer/node/docagent.js quickstart")
        self.assertTrue((repo_root / payload["bin"]["docagent"]).exists())

        wrapper_text = (repo_root / payload["bin"]["docagent"]).read_text(encoding="utf-8")
        self.assertIn('if (forwardedArgs.length === 0)', wrapper_text)
        self.assertIn('forwardedArgs.push("quickstart")', wrapper_text)
        self.assertIn('npm install -g doc-for-agent', wrapper_text)

    def test_user_facing_docs_have_bilingual_counterparts(self) -> None:
        repo_root = TEST_ROOT.parents[1]
        required_pairs = [
            (repo_root / "README.md", repo_root / "README.zh.md"),
            (repo_root / "docs" / "quickstart.md", repo_root / "docs" / "quickstart.zh.md"),
            (repo_root / "docs" / "platforms.md", repo_root / "docs" / "platforms.zh.md"),
            (repo_root / "docs" / "landing-page.md", repo_root / "docs" / "landing-page.zh.md"),
        ]
        for english, chinese in required_pairs:
            self.assertTrue(english.exists(), f"Missing English doc: {english}")
            self.assertTrue(chinese.exists(), f"Missing Chinese doc: {chinese}")

            english_text = english.read_text(encoding="utf-8")
            chinese_text = chinese.read_text(encoding="utf-8")
            if english.name == "landing-page.md":
                self.assertIn("install", english_text)
                self.assertIn("install", chinese_text)
            else:
                self.assertIn("docagent init --ai", english_text)
                self.assertIn("docagent init --ai", chinese_text)

    def test_quickstart_command_prints_unified_entry_guidance(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-quickstart-") as tmpdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["quickstart", "--target", tmpdir])

            self.assertEqual(exit_code, 0)
            text = stdout.getvalue()
            self.assertIn("doc-for-agent quickstart", text)
            self.assertIn("Node users: `npm install -g doc-for-agent`", text)
            self.assertIn("Node one-off start: `npx -y doc-for-agent init --ai all --target <repo-root>`", text)
            self.assertIn("Single-platform option: replace `all` with `claude`, `codex`, `continue`, or `copilot`.", text)
            self.assertIn("Python users: `pipx install doc-for-agent`", text)
            self.assertIn("docagent init --ai <claude|codex|continue|copilot|all>", text)
            self.assertIn("<repo-root>", text)
            self.assertIn("docagent init --ai all --target <repo-root>", text)
            self.assertIn("docagent init --ai claude --target <repo-root>", text)
            self.assertIn("CodeBuddy users usually start with `--ai codex`.", text)
            self.assertIn("Output mode map: `agent` -> `AGENTS/`, `human` -> `docs/`, `dual` -> both", text)
            self.assertIn("Not AGENTS-only: choose output mode based on your docs audience", text)
            self.assertIn("Supported `--ai` values: claude, codex, continue, copilot, all", text)
            self.assertIn("docs/landing-page.md (EN) / docs/landing-page.zh.md (ZH)", text)
            self.assertIn("docs/quickstart.md (EN) / docs/quickstart.zh.md (ZH)", text)
            self.assertIn("docs/platforms.md (EN) / docs/platforms.zh.md (ZH)", text)

    def test_generate_command_executes_generator_dry_run(self) -> None:
        fixture_root = TEST_ROOT / "fixtures" / "backend_service"
        agents_dir = fixture_root / "AGENTS"
        if agents_dir.exists():
            self.fail(f"Fixture unexpectedly contains AGENTS directory: {agents_dir}")

        exit_code = main(["generate", "--root", str(fixture_root), "--dry-run", "--output-mode", "dual"])

        self.assertEqual(exit_code, 0)
        self.assertFalse(agents_dir.exists())

    def test_refresh_command_executes_refresh_mode_dry_run(self) -> None:
        fixture_root = TEST_ROOT / "fixtures" / "cli_tool"
        agents_dir = fixture_root / "AGENTS"
        if agents_dir.exists():
            self.fail(f"Fixture unexpectedly contains AGENTS directory: {agents_dir}")

        exit_code = main(["refresh", "--root", str(fixture_root), "--dry-run", "--output-mode", "agent"])

        self.assertEqual(exit_code, 0)
        self.assertFalse(agents_dir.exists())


if __name__ == "__main__":
    unittest.main()
