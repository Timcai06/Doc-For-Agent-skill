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


if __name__ == "__main__":
    unittest.main()
