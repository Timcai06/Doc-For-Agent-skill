from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parents[2] / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from doc_for_agent_generator.analysis import analyze_repo
from doc_for_agent_generator.builders import build_layered_implementation_plan, build_workflows


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


if __name__ == "__main__":
    unittest.main()
