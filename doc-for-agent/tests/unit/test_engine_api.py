from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

TEST_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = TEST_ROOT.parents[1]
SCRIPTS_ROOT = REPO_ROOT / "doc-for-agent" / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from doc_for_agent_generator.engine import (  # noqa: E402
    EngineRequest,
    apply_generation_plan,
    build_generation_plan,
    plan_dry_run_actions,
    plan_title,
)


class EngineApiTests(unittest.TestCase):
    def test_dual_plan_exposes_agents_and_human_outputs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-engine-dual-") as tmpdir:
            sandbox_root = Path(tmpdir) / "dual_mode_app"
            shutil.copytree(TEST_ROOT / "fixtures" / "dual_mode_app", sandbox_root)

            plan = build_generation_plan(
                EngineRequest(
                    root=sandbox_root,
                    mode="generate",
                    output_mode="dual",
                    profile="layered",
                )
            )

            self.assertEqual(plan.write_mode, "init")
            self.assertIn(str(plan.agents_dir / "00-entry/AGENTS.md"), plan.files)
            self.assertTrue(any(path.endswith("/docs/overview.md") for path in plan.files))
            self.assertIn("Dry run: would generate AGENTS + human docs", plan_title(plan, dry_run=True))

    def test_migrate_mode_uses_refresh_write_mode(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-engine-migrate-") as tmpdir:
            sandbox_root = Path(tmpdir) / "layered_product_app"
            shutil.copytree(TEST_ROOT / "fixtures" / "layered_product_app", sandbox_root)

            plan = build_generation_plan(
                EngineRequest(
                    root=sandbox_root,
                    mode="migrate",
                    output_mode="agent",
                    profile="layered",
                )
            )

            self.assertEqual(plan.write_mode, "refresh")
            dry_run_lines = plan_dry_run_actions(plan)
            self.assertTrue(any("AGENTS/00-entry/AGENTS.md" in line for line in dry_run_lines))

    def test_apply_generation_plan_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-engine-apply-") as tmpdir:
            sandbox_root = Path(tmpdir) / "human_no_docs"
            shutil.copytree(TEST_ROOT / "fixtures" / "human_no_docs", sandbox_root)

            plan = build_generation_plan(
                EngineRequest(
                    root=sandbox_root,
                    mode="generate",
                    output_mode="human",
                    profile="bootstrap",
                )
            )
            apply_generation_plan(plan)

            self.assertTrue((sandbox_root / "docs/overview.md").exists())
            self.assertTrue((sandbox_root / "docs/architecture.md").exists())
            self.assertFalse((sandbox_root / "AGENTS").exists())


if __name__ == "__main__":
    unittest.main()
