from __future__ import annotations

import sys
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
