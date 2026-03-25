from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parents[2] / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from doc_for_agent_generator.analysis import analyze_repo
from doc_for_agent_generator.builders import build_workflows


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


if __name__ == "__main__":
    unittest.main()
