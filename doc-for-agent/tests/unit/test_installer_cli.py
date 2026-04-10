from __future__ import annotations

import io
import json
import os
import shutil
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
        self.assertIn("doc-for-agent skill package", text)
        self.assertIn("primary commands: init, refresh, doctor, generate, update, versions", text)
        self.assertIn("compatibility commands: install, all", text)
        self.assertIn("Quick start:", text)
        self.assertIn("npm install -g doc-for-agent", text)
        self.assertIn("docagent init --ai codex", text)
        self.assertIn("docagent init --ai claudecode", text)

    def test_collect_doctor_statuses_reports_install_targets(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-doctor-") as tmpdir:
            target_root = Path(tmpdir)
            statuses = collect_doctor_statuses(target_root, ["codex", "claudecode"])

            self.assertEqual([status.platform for status in statuses], ["codex", "claudecode"])
            self.assertFalse(statuses[0].installed)
            self.assertEqual(statuses[0].install_root, target_root / ".codex" / "skills" / "doc-for-agent")
            self.assertIsNone(statuses[0].installed_version)

    def test_render_doctor_report_mentions_continue(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-doctor-") as tmpdir:
            target_root = Path(tmpdir)
            report = render_doctor_report(target_root, collect_doctor_statuses(target_root, ["continue"]))

            self.assertIn("Continue (continue)", report)
            self.assertIn("assistant folder will be created", report)
            self.assertIn("Version: 0.4.0", report)

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
                exit_code = main(
                    ["init", "--ai", "claudecode", "--target", tmpdir, "--global-root", tmpdir]
                )

            self.assertEqual(exit_code, 0)
            install_root = Path(tmpdir) / ".claude" / "skills" / "doc-for-agent"
            self.assertTrue((install_root / "SKILL.md").exists())
            text = stdout.getvalue()
            self.assertIn("doc-for-agent init", text)
            self.assertIn("Selected AI platforms: claudecode", text)
            self.assertIn("Install scope: global assistant discovery first", text)
            self.assertIn("Recommended next commands:", text)

    def test_init_without_target_wires_current_directory_by_default(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-init-default-local-") as tmpdir:
            global_root = Path(tmpdir) / "global-root"
            repo_root = Path(tmpdir) / "repo-root"
            global_root.mkdir(parents=True, exist_ok=True)
            repo_root.mkdir(parents=True, exist_ok=True)

            previous_cwd = Path.cwd()
            try:
                os.chdir(repo_root)
                stdout = io.StringIO()
                with redirect_stdout(stdout):
                    exit_code = main(["init", "--ai", "codex", "--global-root", str(global_root)])
            finally:
                os.chdir(previous_cwd)

            self.assertEqual(exit_code, 0)
            self.assertTrue((global_root / ".codex" / "skills" / "doc-for-agent" / "SKILL.md").exists())
            self.assertTrue((repo_root / ".codex" / "skills" / "doc-for-agent" / "SKILL.md").exists())
            self.assertIn(f"Repository target root: {repo_root.resolve()}", stdout.getvalue())

    def test_init_command_global_only_skips_repository_wiring(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-init-no-local-") as tmpdir:
            tmp_path = Path(tmpdir)
            global_root = tmp_path / "global-root"
            repo_root = tmp_path / "repo-root"
            global_root.mkdir(parents=True, exist_ok=True)
            repo_root.mkdir(parents=True, exist_ok=True)

            current_dir = Path.cwd()
            try:
                os.chdir(repo_root)
                stdout = io.StringIO()
                with redirect_stdout(stdout):
                    exit_code = main(["init", "--ai", "codex", "--global-root", str(global_root), "--global"])
            finally:
                os.chdir(current_dir)

            self.assertEqual(exit_code, 0)
            self.assertTrue((global_root / ".codex" / "skills" / "doc-for-agent" / "SKILL.md").exists())
            self.assertFalse((repo_root / ".codex" / "skills" / "doc-for-agent").exists())
            self.assertNotIn("Repository target root:", stdout.getvalue())
            self.assertIn(f"Global target root: {global_root.resolve()}", stdout.getvalue())
            self.assertIn("Recommended next commands:", stdout.getvalue())

    def test_init_global_command_writes_platform_bundle_under_global_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-global-install-") as tmpdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["init", "--ai", "codex", "--global-root", tmpdir, "--global"])

            self.assertEqual(exit_code, 0)
            install_root = Path(tmpdir) / ".codex" / "skills" / "doc-for-agent"
            self.assertTrue((install_root / "SKILL.md").exists())
            self.assertTrue((install_root / "scripts").is_dir())
            self.assertTrue((install_root / "INSTALLATION.json").exists())
            text = stdout.getvalue()
            self.assertIn("doc-for-agent init", text)
            self.assertIn(f"Global target root: {Path(tmpdir).resolve()}", text)
            self.assertIn("Recommended next commands:", text)
            self.assertIn("docagent doctor --global --platform codex", text)
            self.assertNotIn("Repository target root:", text)

    def test_init_global_non_default_platform_keeps_explicit_ai_flag(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-global-install-claude-") as tmpdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["init", "--ai", "claudecode", "--global-root", tmpdir, "--global"])

            self.assertEqual(exit_code, 0)
            text = stdout.getvalue()
            self.assertIn("Selected AI platforms: claudecode", text)
            self.assertIn("docagent doctor --global --platform claudecode", text)

    def test_doctor_command_prints_summary(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-install-") as tmpdir:
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                exit_code = main(["doctor", "--platform", "claudecode", "--target", tmpdir])

            self.assertEqual(exit_code, 0)
            report = stdout.getvalue()
            self.assertIn("doc-for-agent doctor", report)
            self.assertIn("Claude Code (claudecode)", report)

    def test_doctor_command_can_inspect_global_install_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-global-doctor-") as tmpdir:
            main(["init", "--ai", "codex", "--global-root", tmpdir, "--global"])
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
            self.assertIn("Platforms: codex, claudecode, continue, copilot", stdout.getvalue())

    def test_versions_report_reads_installed_receipt(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-install-") as tmpdir:
            main(["install", "--platform", "codex", "--target", tmpdir])
            report = render_versions_report(Path(tmpdir), collect_doctor_statuses(Path(tmpdir), ["codex"]))

            self.assertIn("Source version: 0.4.0", report)
            self.assertIn("Codex (codex): 0.4.0", report)

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
            self.assertIn("Skill package flow: install -> init -> refresh", text)
            self.assertIn("npm install -g doc-for-agent", text)
            self.assertIn("npx -y doc-for-agent init --ai codex", text)
            self.assertIn("docagent init --ai <codex|claudecode|continue|copilot|all>", text)
            self.assertIn("<repo-root>", text)
            self.assertNotIn("docagent init --ai all --target <repo-root>", text)
            self.assertIn("docagent init --ai claudecode", text)
            self.assertIn("Output mode map: `agent` -> `dfa-doc/AGENTS/`, `human` -> `dfa-doc/handbook/`, `dual` -> both, `quad` -> `dfa-doc/AGENTS/`, `dfa-doc/AGENTS.zh/`, `dfa-doc/handbook/`, `dfa-doc/handbook.zh/`", text)
            self.assertIn("Four-view mode establishes structure for bilingual agent/human docs; it does not claim bilingual content polish is complete.", text)
            self.assertIn("Supported `--ai` values: codex, claudecode, continue, copilot, all", text)
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

    def test_refresh_command_rejects_dual_after_quad_footprint_exists(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-refresh-quad-guard-") as tmpdir:
            sandbox_root = Path(tmpdir) / "dual_mode_app"
            source_fixture = TEST_ROOT / "fixtures" / "dual_mode_app"
            shutil.copytree(source_fixture, sandbox_root)

            quad_exit = main(["refresh", "--root", str(sandbox_root), "--output-mode", "quad"])
            self.assertEqual(quad_exit, 0)

            dual_exit = main(["refresh", "--root", str(sandbox_root), "--output-mode", "dual"])
            self.assertNotEqual(dual_exit, 0)


if __name__ == "__main__":
    unittest.main()
