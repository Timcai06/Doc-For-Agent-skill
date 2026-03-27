from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parents[2] / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from doc_for_agent_generator.analysis import analyze_repo
from doc_for_agent_generator.builders import (
    build_layered_app_flow,
    build_layered_architecture_compatibility,
    build_layered_core_goals,
    build_layered_implementation_plan,
    build_layered_lessons,
    build_layered_prd,
    build_layered_progress,
    build_workflows,
)


class WorkflowGenerationTests(unittest.TestCase):
    def test_skill_meta_repo_includes_unit_and_verify_commands(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-workflows-") as tmpdir:
            root = Path(tmpdir) / "quality-skill"
            (root / "doc-for-agent/agents").mkdir(parents=True)
            (root / "doc-for-agent/scripts").mkdir(parents=True)
            (root / "doc-for-agent/tests/unit").mkdir(parents=True)
            (root / "doc-for-agent/tests").mkdir(parents=True, exist_ok=True)

            (root / "README.md").write_text(
                "# Quality Skill\n\nReusable skill for documenting repos.\n",
                encoding="utf-8",
            )
            (root / "doc-for-agent/SKILL.md").write_text(
                "---\nname: quality-skill\ndescription: Keep docs aligned.\n---\n",
                encoding="utf-8",
            )
            (root / "doc-for-agent/agents/openai.yaml").write_text(
                "version: 1\n",
                encoding="utf-8",
            )
            (root / "doc-for-agent/scripts/init_agents_docs.py").write_text(
                "print('refresh')\n",
                encoding="utf-8",
            )
            (root / "doc-for-agent/tests/verify_generator_snapshots.py").write_text(
                "print('verify')\n",
                encoding="utf-8",
            )
            (root / "doc-for-agent/tests/unit/test_example.py").write_text(
                "def test_example():\n    assert True\n",
                encoding="utf-8",
            )

            analysis = analyze_repo(root, "Quality Skill")
            workflows = build_workflows(analysis)

            self.assertIn(
                "python3 doc-for-agent/scripts/init_agents_docs.py --root /path/to/target-repo --mode refresh",
                workflows,
            )
            self.assertIn(
                "python3 -m unittest discover -s doc-for-agent/tests/unit -p 'test_*.py'",
                workflows,
            )
            self.assertIn(
                "python3 doc-for-agent/tests/verify_generator_snapshots.py",
                workflows,
            )
            self.assertNotIn("# TODO: add lint / test / build commands", workflows)

    def test_package_scripts_are_used_when_no_frontend_root_is_detected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-workflows-scripts-") as tmpdir:
            root = Path(tmpdir) / "scripted-cli"
            root.mkdir(parents=True)
            (root / "README.md").write_text(
                "# Scripted CLI\n\nCLI with package scripts but no frontend framework deps.\n",
                encoding="utf-8",
            )
            (root / "package.json").write_text(
                (
                    '{"name":"scripted-cli","scripts":{"start":"node cli.js","lint":"eslint .",'
                    '"test":"node --test","build":"tsup src/index.ts"}}\n'
                ),
                encoding="utf-8",
            )
            (root / "cli.js").write_text("console.log('ok')\n", encoding="utf-8")

            analysis = analyze_repo(root, "Scripted CLI")
            workflows = build_workflows(analysis)

            self.assertIn("npm install", workflows)
            self.assertIn("npm run start", workflows)
            self.assertIn("npm run lint", workflows)
            self.assertIn("npm run test", workflows)
            self.assertIn("npm run build", workflows)
            self.assertNotIn("# TODO:", workflows)

    def test_layered_implementation_plan_uses_package_scripts_without_todo_fallback(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-layered-plan-") as tmpdir:
            root = Path(tmpdir) / "layered-cli"
            root.mkdir(parents=True)
            (root / "README.md").write_text("# Layered CLI\n\nLayered profile repo with scripts.\n", encoding="utf-8")
            (root / "package.json").write_text(
                (
                    '{"name":"layered-cli","scripts":{"start":"node cli.js","lint":"eslint .","test":"node --test"}}\n'
                ),
                encoding="utf-8",
            )
            (root / "cli.js").write_text("console.log('ok')\n", encoding="utf-8")

            analysis = analyze_repo(root, "Layered CLI", doc_profile="layered")
            plan = build_layered_implementation_plan(analysis)

            self.assertIn("npm install", plan)
            self.assertIn("npm run start", plan)
            self.assertIn("npm run lint", plan)
            self.assertIn("npm run test", plan)
            self.assertNotIn("# TODO:", plan)

    def test_layered_docs_reference_scattered_repository_docs_by_role(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-layered-supporting-docs-") as tmpdir:
            root = Path(tmpdir) / "layered-docs"
            (root / "docs/architecture").mkdir(parents=True)
            (root / "specs").mkdir(parents=True)
            (root / "plan").mkdir(parents=True)
            (root / "notes").mkdir(parents=True)

            (root / "README.md").write_text("# Layered Docs\n\nProject overview.\n", encoding="utf-8")
            (root / "docs/architecture/overview.md").write_text("# Architecture\n", encoding="utf-8")
            (root / "specs/prd.md").write_text("# PRD\n", encoding="utf-8")
            (root / "plan/roadmap.md").write_text("# Roadmap\n", encoding="utf-8")
            (root / "notes/status.md").write_text("# Status\n", encoding="utf-8")

            analysis = analyze_repo(root, "Layered Docs", doc_profile="layered")
            core_goals = build_layered_core_goals(analysis)
            architecture = build_layered_architecture_compatibility(analysis)
            plan = build_layered_implementation_plan(analysis)
            lessons = build_layered_lessons(analysis)

            self.assertIn("`README.md`", core_goals)
            self.assertIn("`specs/prd.md`", core_goals)
            self.assertIn("`docs/architecture/overview.md`", architecture)
            self.assertIn("`plan/roadmap.md`", plan)
            self.assertIn("`notes/status.md`", lessons)

    def test_layered_docs_reference_readme_and_quickstart_for_execution_and_architecture(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-layered-exec-arch-docs-") as tmpdir:
            root = Path(tmpdir) / "layered-exec-arch-docs"
            (root / "docs").mkdir(parents=True)
            (root / "README.md").write_text(
                (
                    "# Layered Exec Arch Docs\n\n"
                    "Use docagent init --ai codex --target <repo-root> to install for Codex.\n"
                ),
                encoding="utf-8",
            )
            (root / "docs/quickstart.md").write_text(
                (
                    "# Quickstart\n\n"
                    "```bash\n"
                    "docagent init --ai codex --target <repo-root>\n"
                    "docagent refresh --root <repo-root>\n"
                    "```\n"
                ),
                encoding="utf-8",
            )
            (root / "docs/platforms.md").write_text(
                (
                    "# Platforms\n\n"
                    "| Agent | Command |\n"
                    "| --- | --- |\n"
                    "| Codex | docagent init --ai codex --target <repo-root> |\n"
                ),
                encoding="utf-8",
            )

            analysis = analyze_repo(root, "Layered Exec Arch Docs", doc_profile="layered")
            architecture = build_layered_architecture_compatibility(analysis)
            plan = build_layered_implementation_plan(analysis)

            self.assertIn("`README.md`", architecture)
            self.assertIn("`README.md`", plan)
            self.assertIn("`docs/quickstart.md`", plan)
            self.assertIn("`docs/platforms.md`", plan)

    def test_layered_docs_synthesize_confirmed_conflicting_and_unresolved_insights(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-layered-synthesis-") as tmpdir:
            root = Path(tmpdir) / "layered-synthesis"
            (root / "docs/product").mkdir(parents=True)
            (root / "docs/architecture").mkdir(parents=True)
            (root / "specs").mkdir(parents=True)
            (root / "plan").mkdir(parents=True)
            (root / "notes").mkdir(parents=True)

            (root / "README.md").write_text("# Layered Synthesis\n\nConflicting docs fixture.\n", encoding="utf-8")
            (root / "docs/product/vision.md").write_text(
                (
                    "# Product Vision\n\n"
                    "- Primary users are operations teams.\n"
                    "- Package manager: npm.\n"
                    "- Open question: decide whether self-hosted mode is in scope.\n"
                ),
                encoding="utf-8",
            )
            (root / "specs/prd.md").write_text(
                (
                    "# PRD\n\n"
                    "- Primary users are operations teams.\n"
                    "- Package manager: pnpm.\n"
                    "- TODO: confirm escalation policy.\n"
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
            (root / "plan/roadmap.md").write_text(
                "- Run verification with npm run test before each release candidate.\n- TBD: decide who approves release cutover.\n",
                encoding="utf-8",
            )
            (root / "notes/status.md").write_text(
                "- Keep command names stable across docs and scripts.\n- Pending: finalize the migration retrospective template.\n",
                encoding="utf-8",
            )

            analysis = analyze_repo(root, "Layered Synthesis", doc_profile="layered")
            core_goals = build_layered_core_goals(analysis)
            prd = build_layered_prd(analysis)
            app_flow = build_layered_app_flow(analysis)
            architecture = build_layered_architecture_compatibility(analysis)
            plan = build_layered_implementation_plan(analysis)
            progress = build_layered_progress(analysis)
            lessons = build_layered_lessons(analysis)

            self.assertIn("Supporting docs disagree on package manager (`npm`, `pnpm`).", core_goals)
            self.assertIn("Open question: decide whether self-hosted mode is in scope", prd)
            self.assertIn("TODO: confirm escalation policy", app_flow)
            self.assertIn("Supporting docs disagree on runtime/framework (`fastapi`, `flask`).", architecture)
            self.assertIn("TBD: decide who approves release cutover", plan)
            self.assertIn("Pending: finalize the migration retrospective template", progress)
            self.assertIn("Pending: finalize the migration retrospective template", lessons)


if __name__ == "__main__":
    unittest.main()
