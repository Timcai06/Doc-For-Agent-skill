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
    def test_dry_run_defaults_to_quad_outputs_without_writing_directories(self) -> None:
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

            self.assertIn("Dry run: would refresh four-view docs", result.stdout)
            self.assertIn("create dfa-doc/AGENTS/00-entry/AGENTS.md", result.stdout)
            self.assertIn("create dfa-doc/handbook/overview.md", result.stdout)
            self.assertFalse((sandbox_root / "dfa-doc" / "AGENTS").exists())
            self.assertFalse((sandbox_root / "dfa-doc" / "handbook").exists())

    def test_dry_run_agent_mode_still_reports_agents_only(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-dry-run-agent-") as tmpdir:
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
                    "--output-mode",
                    "agent",
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("Dry run: would refresh AGENTS docs", result.stdout)
            self.assertIn("create dfa-doc/AGENTS/00-entry/AGENTS.md", result.stdout)
            self.assertNotIn("create dfa-doc/handbook/overview.md", result.stdout)
            self.assertFalse((sandbox_root / "dfa-doc" / "AGENTS").exists())
            self.assertFalse((sandbox_root / "dfa-doc" / "handbook").exists())

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
            self.assertIn("Documentation state: `migrate`", result.stdout)
            self.assertIn("Documentation inventory:", result.stdout)
            self.assertIn("agent roots: 1", result.stdout)
            self.assertIn("flat agent files: 0", result.stdout)
            self.assertIn("Suggested command: python3 doc-for-agent/scripts/init_agents_docs.py --root", result.stdout)
            self.assertIn("Human template variant: `paired-core`", result.stdout)
            self.assertIn("Suggested source-of-truth files:", result.stdout)
            self.assertIn("Supporting-doc synthesis summary:", result.stdout)
            self.assertIn("product: confirmed=", result.stdout)
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
                    "--output-mode",
                    "agent",
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("create dfa-doc/AGENTS/00-entry/AGENTS.md", result.stdout)
            self.assertIn("create dfa-doc/AGENTS/04-memory/010-lessons.md", result.stdout)
            self.assertFalse((sandbox_root / "dfa-doc" / "AGENTS").exists())

    def test_human_output_mode_creates_docs_without_agents_directory(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-human-mode-") as tmpdir:
            sandbox_root = Path(tmpdir) / "backend_service"
            shutil.copytree(TEST_ROOT / "fixtures" / "backend_service", sandbox_root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(GENERATOR),
                    "--root",
                    str(sandbox_root),
                    "--mode",
                    "refresh",
                    "--output-mode",
                    "human",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("Refreshed human docs in:", result.stdout)
            self.assertTrue((sandbox_root / "dfa-doc" / "handbook" / "overview.md").exists())
            self.assertTrue((sandbox_root / "dfa-doc" / "handbook" / "architecture.md").exists())
            self.assertTrue((sandbox_root / "dfa-doc" / "handbook" / "workflows.md").exists())
            self.assertTrue((sandbox_root / "dfa-doc" / "handbook" / "glossary.md").exists())
            overview = (sandbox_root / "dfa-doc" / "handbook" / "overview.md").read_text(encoding="utf-8")
            architecture = (sandbox_root / "dfa-doc" / "handbook" / "architecture.md").read_text(encoding="utf-8")
            workflows = (sandbox_root / "dfa-doc" / "handbook" / "workflows.md").read_text(encoding="utf-8")
            glossary = (sandbox_root / "dfa-doc" / "handbook" / "glossary.md").read_text(encoding="utf-8")
            self.assertIn("## Knowledge Status", overview)
            self.assertIn("## Top Rules (Read First)", overview)
            self.assertIn("## Document Contract", overview)
            self.assertIn("## Dual Sync Checklist", overview)
            self.assertIn("## Paired Refresh Rules", overview)
            self.assertIn("## Dual Pairing Contract (Rules)", overview)
            self.assertIn("## Paired Agent Docs (Dual Mode)", overview)
            self.assertIn("## Output Boundary (Human vs Agent)", overview)
            self.assertIn("## Dual View Rationale", overview)
            self.assertIn("dfa-doc/AGENTS/product.md", overview)
            self.assertIn("Pairing mode rule:", overview)
            self.assertIn("Rule 1:", overview)
            self.assertIn("## Provenance", overview)
            self.assertIn("### Supporting Signals", overview)
            self.assertIn("## Update Triggers", overview)
            self.assertIn("## Intended Audience", overview)
            self.assertIn("## System Map", architecture)
            self.assertIn("## Top Rules (Read First)", architecture)
            self.assertIn("## Document Contract", architecture)
            self.assertIn("## Dual Sync Checklist", architecture)
            self.assertIn("## Paired Refresh Rules", architecture)
            self.assertIn("## Dual Pairing Contract (Rules)", architecture)
            self.assertIn("## Paired Agent Docs (Dual Mode)", architecture)
            self.assertIn("## Output Boundary (Human vs Agent)", architecture)
            self.assertIn("## Dual View Rationale", architecture)
            self.assertIn("dfa-doc/AGENTS/architecture.md", architecture)
            self.assertIn("Rule 1:", architecture)
            self.assertIn("### Supporting Signals", architecture)
            self.assertIn("## Update Triggers", architecture)
            self.assertIn("## Maintenance Workflow", architecture)
            self.assertIn("## Provenance", workflows)
            self.assertIn("## Top Rules (Read First)", workflows)
            self.assertIn("## Document Contract", workflows)
            self.assertIn("## Dual Sync Checklist", workflows)
            self.assertIn("## Paired Refresh Rules", workflows)
            self.assertIn("## Dual Pairing Contract (Rules)", workflows)
            self.assertIn("## Paired Agent Docs (Dual Mode)", workflows)
            self.assertIn("## Output Boundary (Human vs Agent)", workflows)
            self.assertIn("## Dual View Rationale", workflows)
            self.assertIn("dfa-doc/AGENTS/workflows.md", workflows)
            self.assertIn("Rule 1:", workflows)
            self.assertIn("### Supporting Signals", workflows)
            self.assertIn("## Update Triggers", workflows)
            self.assertIn("## Operational Notes", workflows)
            self.assertIn("## Maintenance Workflow", workflows)
            self.assertIn("## Candidate Terms From Code Signals", glossary)
            self.assertIn("## Derived Terminology Signals", glossary)
            self.assertFalse((sandbox_root / "dfa-doc" / "AGENTS").exists())

    def test_human_output_mode_still_generates_docs_when_repo_has_no_existing_docs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-human-no-docs-") as tmpdir:
            sandbox_root = Path(tmpdir) / "human_no_docs"
            shutil.copytree(TEST_ROOT / "fixtures" / "human_no_docs", sandbox_root)

            subprocess.run(
                [
                    sys.executable,
                    str(GENERATOR),
                    "--root",
                    str(sandbox_root),
                    "--mode",
                    "refresh",
                    "--output-mode",
                    "human",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertTrue((sandbox_root / "dfa-doc" / "handbook" / "overview.md").exists())
            self.assertTrue((sandbox_root / "dfa-doc" / "handbook" / "architecture.md").exists())
            self.assertTrue((sandbox_root / "dfa-doc" / "handbook" / "workflows.md").exists())
            self.assertTrue((sandbox_root / "dfa-doc" / "handbook" / "glossary.md").exists())
            architecture = (sandbox_root / "dfa-doc" / "handbook" / "architecture.md").read_text(encoding="utf-8")
            overview = (sandbox_root / "dfa-doc" / "handbook" / "overview.md").read_text(encoding="utf-8")
            workflows = (sandbox_root / "dfa-doc" / "handbook" / "workflows.md").read_text(encoding="utf-8")
            self.assertIn("## Source Of Truth", architecture)
            self.assertIn("## Top Rules (Read First)", architecture)
            self.assertIn("## Document Contract", architecture)
            self.assertIn("## Dual Sync Checklist", architecture)
            self.assertIn("## Paired Refresh Rules", architecture)
            self.assertIn("## Dual Pairing Contract (Rules)", architecture)
            self.assertIn("## Paired Agent Docs (Dual Mode)", architecture)
            self.assertIn("Rule 1:", architecture)
            self.assertIn("## Bootstrap Backlog (When Docs Are Thin)", architecture)
            self.assertIn("## Update Triggers", architecture)
            self.assertIn("No supporting docs matched this role; content below is derived from repository structure and code signals.", overview)
            self.assertIn("## Top Rules (Read First)", overview)
            self.assertIn("## Document Contract", overview)
            self.assertIn("## Dual Sync Checklist", overview)
            self.assertIn("## Paired Refresh Rules", overview)
            self.assertIn("## Dual Pairing Contract (Rules)", overview)
            self.assertIn("## Paired Agent Docs (Dual Mode)", overview)
            self.assertIn("## Output Boundary (Human vs Agent)", overview)
            self.assertIn("## Dual View Rationale", overview)
            self.assertIn("Rule 1:", overview)
            self.assertIn("## Bootstrap Backlog (When Docs Are Thin)", overview)
            self.assertIn("## Top Rules (Read First)", workflows)
            self.assertIn("## Document Contract", workflows)
            self.assertIn("## Dual Sync Checklist", workflows)
            self.assertIn("## Paired Refresh Rules", workflows)
            self.assertIn("## Dual Pairing Contract (Rules)", workflows)
            self.assertIn("## Paired Agent Docs (Dual Mode)", workflows)
            self.assertIn("## Output Boundary (Human vs Agent)", workflows)
            self.assertIn("## Dual View Rationale", workflows)
            self.assertIn("Rule 1:", workflows)
            self.assertIn("## Maintenance Workflow", workflows)

    def test_human_locale_zh_routes_outputs_to_handbook_zh(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-human-zh-") as tmpdir:
            sandbox_root = Path(tmpdir) / "backend_service"
            shutil.copytree(TEST_ROOT / "fixtures" / "backend_service", sandbox_root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(GENERATOR),
                    "--root",
                    str(sandbox_root),
                    "--mode",
                    "generate",
                    "--output-mode",
                    "human",
                    "--human-locale",
                    "zh",
                    "--human-template",
                    "paired-core",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("Generated human docs in:", result.stdout)
            self.assertIn("dfa-doc/handbook.zh", result.stdout)
            self.assertTrue((sandbox_root / "dfa-doc" / "handbook.zh" / "overview.md").exists())
            self.assertTrue((sandbox_root / "dfa-doc" / "handbook.zh" / "architecture.md").exists())
            self.assertFalse((sandbox_root / "dfa-doc" / "handbook" / "overview.md").exists())
            overview = (sandbox_root / "dfa-doc" / "handbook.zh" / "overview.md").read_text(encoding="utf-8")
            self.assertIn("语言输出规则：人类视图语言 `zh` 映射至目录 `dfa-doc/handbook.zh/`。", overview)

    def test_dual_output_mode_dry_run_reports_agents_and_human_paths(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-dual-mode-") as tmpdir:
            sandbox_root = Path(tmpdir) / "web_app"
            shutil.copytree(TEST_ROOT / "fixtures" / "web_app", sandbox_root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(GENERATOR),
                    "--root",
                    str(sandbox_root),
                    "--mode",
                    "refresh",
                    "--output-mode",
                    "dual",
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("Dry run: would refresh AGENTS + human docs", result.stdout)
            self.assertIn("create dfa-doc/AGENTS/00-entry/AGENTS.md", result.stdout)
            self.assertIn("create dfa-doc/handbook/overview.md", result.stdout)
            self.assertFalse((sandbox_root / "dfa-doc" / "AGENTS").exists())
            self.assertFalse((sandbox_root / "dfa-doc" / "handbook").exists())

    def test_generate_mode_dry_run_reports_dual_outputs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-generate-mode-") as tmpdir:
            sandbox_root = Path(tmpdir) / "web_app"
            shutil.copytree(TEST_ROOT / "fixtures" / "web_app", sandbox_root)

            result = subprocess.run(
                [
                    sys.executable,
                    str(GENERATOR),
                    "--root",
                    str(sandbox_root),
                    "--mode",
                    "generate",
                    "--output-mode",
                    "dual",
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("Dry run: would generate AGENTS + human docs", result.stdout)
            self.assertIn("create dfa-doc/AGENTS/00-entry/AGENTS.md", result.stdout)
            self.assertIn("create dfa-doc/handbook/overview.md", result.stdout)
            self.assertFalse((sandbox_root / "dfa-doc" / "AGENTS").exists())
            self.assertFalse((sandbox_root / "dfa-doc" / "handbook").exists())

    def test_layered_migration_dry_run_reports_archive_actions(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-layered-migrate-dry-run-") as tmpdir:
            sandbox_root = Path(tmpdir) / "legacy_agents_repo"
            (sandbox_root / "AGENTS").mkdir(parents=True)
            (sandbox_root / "README.md").write_text("# Legacy Repo\n\nLegacy repo.\n", encoding="utf-8")
            (sandbox_root / "AGENTS/product.md").write_text("# Product\n\nLegacy product notes.\n", encoding="utf-8")
            (sandbox_root / "AGENTS/workflows.md").write_text("# Workflows\n\nLegacy workflow notes.\n", encoding="utf-8")

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

            self.assertIn("archive product.md -> dfa-doc/AGENTS/_archive/flat/product.md", result.stdout)
            self.assertIn("archive workflows.md -> dfa-doc/AGENTS/_archive/flat/workflows.md", result.stdout)
            self.assertFalse((sandbox_root / "dfa-doc" / "AGENTS" / "_archive").exists())

    def test_migrate_mode_forces_layered_profile_behavior(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-migrate-forced-layered-") as tmpdir:
            sandbox_root = Path(tmpdir) / "legacy_agents_repo"
            (sandbox_root / "AGENTS").mkdir(parents=True)
            (sandbox_root / "README.md").write_text("# Legacy Repo\n\nLegacy repo.\n", encoding="utf-8")
            (sandbox_root / "AGENTS/product.md").write_text("# Product\n\nLegacy product notes.\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(GENERATOR),
                    "--root",
                    str(sandbox_root),
                    "--mode",
                    "migrate",
                    "--profile",
                    "bootstrap",
                    "--output-mode",
                    "agent",
                    "--dry-run",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn("Dry run: would migrate AGENTS docs", result.stdout)
            self.assertIn("archive product.md -> dfa-doc/AGENTS/_archive/flat/product.md", result.stdout)
            self.assertIn("create dfa-doc/AGENTS/00-entry/AGENTS.md", result.stdout)

    def test_layered_migration_archives_flat_docs_and_preserves_notes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-layered-migrate-") as tmpdir:
            sandbox_root = Path(tmpdir) / "legacy_agents_repo"
            (sandbox_root / "AGENTS").mkdir(parents=True)
            (sandbox_root / "README.md").write_text("# Legacy Repo\n\nLegacy repo.\n", encoding="utf-8")
            (sandbox_root / "AGENTS/product.md").write_text(
                "# Product\n\n## Confirmed Facts\n\n- Legacy product notes.\n",
                encoding="utf-8",
            )
            (sandbox_root / "AGENTS/workflows.md").write_text(
                "# Workflows\n\n## Setup\n\n- Legacy workflow notes.\n",
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    str(GENERATOR),
                    "--root",
                    str(sandbox_root),
                    "--mode",
                    "refresh",
                    "--profile",
                    "layered",
                    "--output-mode",
                    "agent",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertFalse((sandbox_root / "AGENTS/product.md").exists())
            self.assertFalse((sandbox_root / "AGENTS/workflows.md").exists())
            self.assertTrue((sandbox_root / "dfa-doc" / "AGENTS" / "_archive/flat/product.md").exists())
            self.assertTrue((sandbox_root / "dfa-doc" / "AGENTS" / "_archive/flat/workflows.md").exists())

            prd_content = (sandbox_root / "dfa-doc" / "AGENTS" / "01-product" / "002-prd.md").read_text(encoding="utf-8")
            plan_content = (sandbox_root / "dfa-doc" / "AGENTS" / "03-execution" / "008-implementation-plan.md").read_text(encoding="utf-8")
            self.assertIn("## Migrated Notes", prd_content)
            self.assertIn("Legacy source: `AGENTS/product.md`", prd_content)
            self.assertIn("Legacy product notes.", prd_content)
            self.assertIn("Legacy source: `AGENTS/workflows.md`", plan_content)
            self.assertIn("Legacy workflow notes.", plan_content)

            subprocess.run(
                [
                    sys.executable,
                    str(GENERATOR),
                    "--root",
                    str(sandbox_root),
                    "--mode",
                    "refresh",
                    "--profile",
                    "layered",
                    "--output-mode",
                    "agent",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertFalse((sandbox_root / "AGENTS/product.md").exists())
            self.assertTrue((sandbox_root / "dfa-doc" / "AGENTS" / "_archive/flat/product.md").exists())


if __name__ == "__main__":
    unittest.main()
