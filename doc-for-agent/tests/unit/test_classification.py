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
    def test_supporting_doc_synthesis_extracts_quickstart_commands_and_platform_facts(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-supporting-synthesis-") as tmpdir:
            root = Path(tmpdir) / "doc-system-repo"
            root.mkdir(parents=True)
            (root / "README.md").write_text(
                (
                    "# Doc System Repo\n\n"
                    "This project supports human, agent, and dual documentation workflows.\n\n"
                    "## Quickstart\n\n"
                    "```bash\n"
                    "docagent init --ai codex\n"
                    "docagent refresh --output-mode dual\n"
                    "npm run test\n"
                    "```\n\n"
                    "## Platform Coverage\n\n"
                    "- Supports Codex, Claude Code, Continue, and Copilot through a unified CLI surface.\n"
                ),
                encoding="utf-8",
            )

            analysis = analyze_repo(root, "Doc System Repo")
            execution_confirmed = analysis.supporting_doc_insights.get("execution", {}).get("confirmed", [])
            product_confirmed = analysis.supporting_doc_insights.get("product", {}).get("confirmed", [])
            architecture_confirmed = analysis.supporting_doc_insights.get("architecture", {}).get("confirmed", [])

            self.assertTrue(any("docagent init --ai codex" in line for line in execution_confirmed))
            self.assertTrue(any("Execution contract:" in line for line in execution_confirmed))
            self.assertTrue(any("Verification gate:" in line for line in execution_confirmed))
            self.assertTrue(
                any("human, agent, and dual documentation workflows" in line for line in product_confirmed)
                or any("Product positioning:" in line for line in product_confirmed)
            )
            self.assertTrue(any("unified CLI surface" in line for line in architecture_confirmed))
            self.assertTrue(
                "unified CLI surface" in architecture_confirmed[0]
                or "CLI boundary: keep `docagent` as the single entry surface" in architecture_confirmed[0]
            )
            self.assertIn("README.md", analysis.supporting_doc_provenance.get("execution", []))

    def test_architecture_distribution_synthesis_normalizes_markdown_table_rows(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-platform-table-") as tmpdir:
            root = Path(tmpdir) / "platform-table-repo"
            root.mkdir(parents=True)
            (root / "README.md").write_text(
                (
                    "# Platform Table Repo\n\n"
                    "| Agent | Command |\n"
                    "| --- | --- |\n"
                    "| Codex | docagent init --ai codex --target <repo-root> |\n"
                    "| Claude Code | docagent init --ai claude --target <repo-root> |\n"
                ),
                encoding="utf-8",
            )

            analysis = analyze_repo(root, "Platform Table Repo")
            architecture_confirmed = analysis.supporting_doc_insights.get("architecture", {}).get("confirmed", [])

            self.assertTrue(any("Codex uses docagent init --ai codex --target <repo-root>" in line for line in architecture_confirmed))
            self.assertFalse(any(line.strip().startswith("|") for line in architecture_confirmed))
            self.assertTrue(any("Distribution structure:" in line for line in architecture_confirmed))

    def test_synthesis_emits_product_positioning_and_source_of_truth_boundary(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-synthesis-rules-") as tmpdir:
            root = Path(tmpdir) / "synthesis-rules-repo"
            root.mkdir(parents=True)
            (root / "README.md").write_text(
                (
                    "# Synthesis Rules Repo\n\n"
                    "Docagent is the unified CLI entry for Codex and Claude coding-agent workflows.\n\n"
                    "Use source of truth files before editing distribution behavior:\n"
                    "- `README.md`\n"
                    "- `package.json`\n\n"
                    "This project serves human, agent, and dual documentation workflows.\n"
                ),
                encoding="utf-8",
            )

            analysis = analyze_repo(root, "Synthesis Rules Repo")
            product_confirmed = analysis.supporting_doc_insights.get("product", {}).get("confirmed", [])
            architecture_confirmed = analysis.supporting_doc_insights.get("architecture", {}).get("confirmed", [])

            self.assertTrue(any("Product positioning:" in line for line in product_confirmed))
            self.assertTrue(any("Source-of-truth boundary:" in line for line in architecture_confirmed))

    def test_dogfooding_synthesis_prefers_rule_style_conclusions(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-dogfooding-synthesis-") as tmpdir:
            root = Path(tmpdir) / "dogfooding-repo"
            (root / "docs").mkdir(parents=True)
            (root / "README.md").write_text(
                (
                    "# Dogfooding Repo\n\n"
                    "doc-for-agent is a CLI coding-agent workflow tool.\n"
                    "Source of truth files include `README.md` and `package.json`.\n"
                    "Keep adapter and distribution wiring aligned with the docagent CLI boundary.\n"
                    "It should initialize sparse repos, migrate messy docs, and refresh existing AGENTS/docs.\n"
                    "Supports human, agent, and dual output modes through docagent.\n\n"
                    "```bash\n"
                    "docagent init --ai codex --target <repo-root>\n"
                    "docagent refresh --output-mode dual --target <repo-root>\n"
                    "docagent doctor --target <repo-root>\n"
                    "npm run test\n"
                    "```\n"
                ),
                encoding="utf-8",
            )
            (root / "docs/platforms.md").write_text(
                (
                    "# Distribution\n\n"
                    "Keep platform adapters and distribution notes aligned with the main CLI contract.\n"
                    "Codex and Claude use docagent as entrypoint.\n"
                    "Source of truth files include `README.md` and `package.json`.\n"
                    "| Agent | Command |\n"
                    "| --- | --- |\n"
                    "| Codex | docagent init --ai codex --target <repo-root> |\n"
                ),
                encoding="utf-8",
            )

            analysis = analyze_repo(root, "Dogfooding Repo")
            execution_confirmed = analysis.supporting_doc_insights.get("execution", {}).get("confirmed", [])
            architecture_confirmed = analysis.supporting_doc_insights.get("architecture", {}).get("confirmed", [])
            product_confirmed = analysis.supporting_doc_insights.get("product", {}).get("confirmed", [])

            self.assertTrue(any("Execution contract:" in line for line in execution_confirmed))
            self.assertTrue(any("Execution constraints:" in line for line in execution_confirmed))
            self.assertTrue(any("Verification gate:" in line for line in execution_confirmed))
            self.assertTrue(any("on failures," in line for line in execution_confirmed if line.startswith("Execution constraints:")))
            self.assertTrue(any("prioritize lifecycle commands" in line for line in execution_confirmed if line.startswith("Execution constraints:")))
            self.assertTrue(any("roll back to the last known-good generated docs state" in line for line in execution_confirmed if line.startswith("Execution constraints:")))
            self.assertTrue(any("if `docagent doctor` fails" in line for line in execution_confirmed if line.startswith("Execution constraints:")))
            self.assertTrue(any("CLI boundary:" in line for line in architecture_confirmed))
            self.assertTrue(any("Source-of-truth boundary:" in line for line in architecture_confirmed))
            self.assertTrue(any("build-path anchors" in line for line in architecture_confirmed if line.startswith("Source-of-truth boundary:")))
            self.assertTrue(any("Build-path rule:" in line for line in architecture_confirmed))
            self.assertTrue(any("Distribution structure:" in line for line in architecture_confirmed))
            self.assertTrue(any("`Codex` -> `docagent init --ai codex --target <repo-root>`" in line for line in architecture_confirmed))
            self.assertTrue(any("Product positioning:" in line for line in product_confirmed))
            self.assertTrue(any("Repository adaptation scope:" in line for line in product_confirmed))
            self.assertTrue(any("not one-off documentation scans" in line for line in product_confirmed if line.startswith("Repository adaptation scope:")) or any("initialize, migrate, and refresh" in line for line in product_confirmed if line.startswith("Repository adaptation scope:")))
            self.assertTrue(any("Retention value:" in line for line in product_confirmed))
            self.assertTrue(any("init -> refresh -> doctor" in line for line in product_confirmed if line.startswith("Retention value:")))
            self.assertTrue(any("not a one-shot" in line.lower() for line in product_confirmed if line.startswith("Retention value:")))
            self.assertFalse(
                any("(sources:" in line for line in execution_confirmed if line.startswith("Execution "))
            )
            self.assertFalse(
                any("(sources:" in line for line in architecture_confirmed if line.startswith("CLI boundary:"))
            )
            self.assertFalse(
                any("(sources:" in line for line in product_confirmed if line.startswith("Product positioning:"))
            )

    def test_execution_command_facts_are_prioritized_over_generic_doc_noise(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-command-priority-") as tmpdir:
            root = Path(tmpdir) / "command-priority-repo"
            root.mkdir(parents=True)
            (root / "README.md").write_text(
                (
                    "# Command Priority Repo\n\n"
                    "- This repository contains broad project context and documentation notes.\n"
                    "- Another long descriptive line intended to look like generic documentation text.\n"
                    "- A third descriptive line that could otherwise crowd the synthesis result window.\n"
                    "- Additional documentation context line for stability checks in summary extraction.\n"
                    "- Yet another descriptive documentation statement used for extraction pressure.\n"
                    "- Final descriptive line before command examples are listed.\n\n"
                    "## Quickstart\n\n"
                    "```bash\n"
                    "docagent init --ai codex\n"
                    "docagent refresh --output-mode dual\n"
                    "```\n"
                ),
                encoding="utf-8",
            )

            analysis = analyze_repo(root, "Command Priority Repo")
            execution_confirmed = analysis.supporting_doc_insights.get("execution", {}).get("confirmed", [])

            self.assertTrue(execution_confirmed)
            self.assertTrue(any("docagent init --ai codex" in line for line in execution_confirmed))
            self.assertTrue(any("docagent refresh --output-mode dual" in line for line in execution_confirmed))
            self.assertFalse(any("broad project context" in line for line in execution_confirmed))

    def test_rule_conclusions_are_ranked_before_generic_summary_snippets(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-rule-priority-") as tmpdir:
            root = Path(tmpdir) / "rule-priority-repo"
            root.mkdir(parents=True)
            (root / "README.md").write_text(
                (
                    "# Rule Priority Repo\n\n"
                    "docagent is the CLI entry for coding-agent workflows.\n"
                    "Supports human, agent, and dual outputs.\n"
                    "Use source of truth files before distribution updates.\n\n"
                    "```bash\n"
                    "docagent init --ai codex\n"
                    "docagent refresh --output-mode dual\n"
                    "npm run test\n"
                    "```\n\n"
                    "- This repository contains broad project context and documentation notes.\n"
                    "- Another long descriptive line intended to look generic.\n"
                    "- Additional descriptive line that should not outrank rule conclusions.\n"
                ),
                encoding="utf-8",
            )

            analysis = analyze_repo(root, "Rule Priority Repo")
            execution_confirmed = analysis.supporting_doc_insights.get("execution", {}).get("confirmed", [])

            self.assertTrue(execution_confirmed)
            self.assertTrue(execution_confirmed[0].startswith(("Execution contract:", "Verification gate:")))

    def test_transition_style_summary_lines_are_filtered_from_confirmed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-transition-filter-") as tmpdir:
            root = Path(tmpdir) / "transition-filter-repo"
            root.mkdir(parents=True)
            (root / "README.md").write_text(
                (
                    "# Transition Filter Repo\n\n"
                    "This project appears to support multiple agent workflows.\n"
                    "It likely works as a broad documentation helper.\n"
                    "Inferred context: this repository may be useful for many teams.\n\n"
                    "```bash\n"
                    "docagent init --ai codex\n"
                    "docagent refresh --output-mode dual\n"
                    "npm run test\n"
                    "```\n"
                ),
                encoding="utf-8",
            )

            analysis = analyze_repo(root, "Transition Filter Repo")
            product_confirmed = analysis.supporting_doc_insights.get("product", {}).get("confirmed", [])
            execution_confirmed = analysis.supporting_doc_insights.get("execution", {}).get("confirmed", [])

            self.assertFalse(any("appears to" in line.lower() for line in product_confirmed))
            self.assertFalse(any("likely" in line.lower() for line in product_confirmed))
            self.assertFalse(any("inferred context" in line.lower() for line in product_confirmed))
            self.assertTrue(any("Execution contract:" in line for line in execution_confirmed))

    def test_architecture_conflicts_emit_source_of_truth_arbitration_rule(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-architecture-conflict-rule-") as tmpdir:
            root = Path(tmpdir) / "architecture-conflict-rule"
            (root / "docs/architecture").mkdir(parents=True)
            (root / "README.md").write_text(
                (
                    "# Architecture Conflict Rule\n\n"
                    "Source of truth files include `README.md` and `package.json`.\n"
                    "Docagent is the CLI entry for Codex workflows.\n"
                ),
                encoding="utf-8",
            )
            (root / "docs/architecture/runtime.md").write_text(
                (
                    "# Runtime\n\n"
                    "- Runtime framework: FastAPI.\n"
                    "- Runtime framework: Flask.\n"
                    "- Conflict: runtime choice differs across architecture drafts.\n"
                ),
                encoding="utf-8",
            )

            analysis = analyze_repo(root, "Architecture Conflict Rule")
            architecture_conflicting = analysis.supporting_doc_insights.get("architecture", {}).get("conflicting", [])

            self.assertTrue(any(line.startswith("Conflict rule:") for line in architecture_conflicting))
            self.assertTrue(any("`README.md`" in line or "`package.json`" in line for line in architecture_conflicting))

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
