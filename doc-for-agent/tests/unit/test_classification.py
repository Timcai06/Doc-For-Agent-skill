from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


TEST_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = TEST_ROOT.parents[0] / "scripts"
FIXTURES_ROOT = TEST_ROOT / "fixtures"

if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from doc_for_agent_generator.analysis import analyze_repo


class RepoClassificationTests(unittest.TestCase):
    def test_docs_inventory_reports_initialize_when_no_agent_docs_exist(self) -> None:
        analysis = analyze_repo(FIXTURES_ROOT / "backend_service", "Event Relay")

        self.assertEqual(analysis.docs_inventory.detected_state, "initialize")
        self.assertEqual(analysis.docs_inventory.canonical_agents_root, FIXTURES_ROOT / "backend_service" / "AGENTS")
        self.assertEqual(analysis.docs_inventory.flat_agent_files, [])
        self.assertEqual(analysis.docs_inventory.layered_agent_files, [])

    def test_hybrid_skill_cli_reports_secondary_traits_and_conflict(self) -> None:
        analysis = analyze_repo(FIXTURES_ROOT / "hybrid_skill_cli", "Route Steward")

        self.assertEqual(analysis.repo_type, "skill-meta")
        self.assertEqual(analysis.classification.confidence, "medium")
        self.assertIn("CLI distribution surface is also present.", analysis.classification.secondary_traits)
        self.assertIn("JavaScript package/distribution metadata is also present.", analysis.classification.secondary_traits)
        self.assertTrue(
            any("packaged tooling signals" in conflict for conflict in analysis.classification.conflicting_signals)
        )

    def test_backend_service_detects_backend_primary_type(self) -> None:
        analysis = analyze_repo(FIXTURES_ROOT / "backend_service", "Event Relay")

        self.assertEqual(analysis.repo_type, "backend-service")
        self.assertEqual(analysis.classification.confidence, "medium")
        self.assertIn("Backend-like Python service structure detected without a separate frontend.", analysis.repo_type_reasons)
        self.assertIn("POST /events", analysis.endpoints)

    def test_monorepo_workspace_detects_monorepo_and_workspace_roots(self) -> None:
        analysis = analyze_repo(FIXTURES_ROOT / "monorepo_workspace", "Repo Fleet")

        self.assertEqual(analysis.repo_type, "monorepo")
        self.assertEqual(analysis.classification.confidence, "high")
        self.assertTrue(any("Workspace-style directories" in reason for reason in analysis.repo_type_reasons))
        self.assertEqual(str(analysis.frontend_root.relative_to(FIXTURES_ROOT / "monorepo_workspace")), "apps/web")
        self.assertEqual(str(analysis.backend_root.relative_to(FIXTURES_ROOT / "monorepo_workspace")), "services/api")

    def test_embedded_skill_markers_do_not_override_workspace_primary_type(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-embedded-skill-") as tmpdir:
            root = Path(tmpdir) / "workspace-app"
            (root / "apps/web/app").mkdir(parents=True)
            (root / "services/api/app").mkdir(parents=True)
            (root / "tool-skill/agents").mkdir(parents=True)

            (root / "README.md").write_text("# Workspace App\n\nWorkspace app with embedded skill metadata.\n", encoding="utf-8")
            (root / "pnpm-workspace.yaml").write_text("packages:\n  - 'apps/*'\n  - 'services/*'\n", encoding="utf-8")
            (root / "apps/web/package.json").write_text(
                '{"name":"workspace-web","dependencies":{"next":"14.2.0","react":"18.3.1"}}\n',
                encoding="utf-8",
            )
            (root / "apps/web/app/page.tsx").write_text("export default function Page(){return <main/>}\n", encoding="utf-8")
            (root / "services/api/requirements.txt").write_text("fastapi==0.112.0\n", encoding="utf-8")
            (root / "services/api/app/main.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")
            (root / "tool-skill/agents/openai.yaml").write_text("version: 1\n", encoding="utf-8")

            analysis = analyze_repo(root, "Workspace App")

            self.assertEqual(analysis.repo_type, "monorepo")
            self.assertIn("Embedded skill metadata is also present.", analysis.classification.secondary_traits)

    def test_repo_type_override_replaces_automatic_classification(self) -> None:
        analysis = analyze_repo(
            FIXTURES_ROOT / "hybrid_skill_cli",
            "Route Steward",
            repo_type_override="cli-tool",
        )

        self.assertEqual(analysis.repo_type, "cli-tool")
        self.assertEqual(analysis.classification.confidence, "high")
        self.assertIn("Repo type overridden via CLI: `cli-tool`.", analysis.classification.reasons)
        self.assertIn(
            "Automatic classification would have selected `skill-meta` instead.",
            analysis.classification.conflicting_signals,
        )

    def test_package_bin_metadata_promotes_cli_tool_classification(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-package-bin-") as tmpdir:
            root = Path(tmpdir) / "bin-only-cli"
            root.mkdir(parents=True)
            (root / "README.md").write_text("# Bin CLI\n\nCLI distributed through package metadata.\n", encoding="utf-8")
            (root / "package.json").write_text(
                '{"name":"bin-only-cli","version":"1.0.0","bin":{"bin-only":"dist/cli.js"}}\n',
                encoding="utf-8",
            )

            analysis = analyze_repo(root, "Bin CLI")

            self.assertEqual(analysis.repo_type, "cli-tool")
            self.assertEqual(analysis.classification.confidence, "high")
            self.assertIn(
                "Package `bin` metadata indicates a CLI distribution surface.",
                analysis.classification.reasons,
            )

    def test_web_app_envelope_is_not_overridden_by_package_bin_metadata(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-web-bin-") as tmpdir:
            root = Path(tmpdir) / "web-with-bin"
            (root / "app").mkdir(parents=True)
            (root / "backend/app").mkdir(parents=True)
            (root / "README.md").write_text("# Web With Bin\n\nWeb app with helper bin metadata.\n", encoding="utf-8")
            (root / "package.json").write_text(
                (
                    '{"name":"web-with-bin","dependencies":{"next":"14.2.0","react":"18.3.1"},'
                    '"bin":{"helper":"bin/helper.js"}}\n'
                ),
                encoding="utf-8",
            )
            (root / "app/page.tsx").write_text("export default function Page(){return <main/>}\n", encoding="utf-8")
            (root / "backend/requirements.txt").write_text("fastapi==0.112.0\n", encoding="utf-8")
            (root / "backend/app/main.py").write_text("from fastapi import FastAPI\napp = FastAPI()\n", encoding="utf-8")

            analysis = analyze_repo(root, "Web With Bin")

            self.assertEqual(analysis.repo_type, "web-app")
            self.assertIn("CLI distribution surface is also present.", analysis.classification.secondary_traits)

    def test_docs_inventory_reports_refresh_for_layered_agents_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-layered-state-") as tmpdir:
            root = Path(tmpdir) / "layered-repo"
            (root / "AGENTS/00-entry").mkdir(parents=True)
            (root / "AGENTS/01-product").mkdir(parents=True)
            (root / "README.md").write_text("# Layered Repo\n\nLayered repo.\n", encoding="utf-8")
            (root / "AGENTS/00-entry/AGENTS.md").write_text("# Entry\n", encoding="utf-8")
            (root / "AGENTS/01-product/001-core-goals.md").write_text("# Goals\n", encoding="utf-8")

            analysis = analyze_repo(root, "Layered Repo")

            self.assertEqual(analysis.docs_inventory.detected_state, "refresh")
            self.assertEqual(analysis.docs_inventory.canonical_agents_root, root / "AGENTS")
            self.assertEqual(len(analysis.docs_inventory.layered_agent_files), 2)
            self.assertEqual(analysis.docs_inventory.flat_agent_files, [])

    def test_docs_inventory_reports_migrate_for_flat_agents_and_scattered_docs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-migrate-state-") as tmpdir:
            root = Path(tmpdir) / "migrate-repo"
            (root / "AGENTS").mkdir(parents=True)
            (root / "docs/architecture").mkdir(parents=True)
            (root / "plan").mkdir(parents=True)
            (root / "README.md").write_text("# Migrate Repo\n\nNeeds migration.\n", encoding="utf-8")
            (root / "AGENTS/product.md").write_text("# Product\n", encoding="utf-8")
            (root / "AGENTS/workflows.md").write_text("# Workflows\n", encoding="utf-8")
            (root / "docs/architecture/overview.md").write_text("# Overview\n", encoding="utf-8")
            (root / "plan/roadmap.md").write_text("# Roadmap\n", encoding="utf-8")

            analysis = analyze_repo(root, "Migrate Repo")

            self.assertEqual(analysis.docs_inventory.detected_state, "migrate")
            self.assertEqual(analysis.docs_inventory.canonical_agents_root, root / "AGENTS")
            self.assertEqual(
                [path.name for path in analysis.docs_inventory.flat_agent_files],
                ["product.md", "workflows.md"],
            )
            self.assertTrue(any(path.name == "overview.md" for path in analysis.docs_inventory.reference_only_docs))
            self.assertTrue(any(path.name == "roadmap.md" for path in analysis.docs_inventory.reference_only_docs))
            self.assertEqual(
                [path.name for path in analysis.docs_inventory.archive_candidates],
                ["product.md", "workflows.md"],
            )


if __name__ == "__main__":
    unittest.main()
