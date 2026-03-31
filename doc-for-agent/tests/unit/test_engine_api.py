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
    build_analysis_explanation_lines,
    build_generation_plan,
    effective_profile_for_mode,
    execute_engine_request,
    validate_output_contract,
    write_strategy_for_mode,
)


class EngineApiTests(unittest.TestCase):
    def test_engine_request_defaults_to_dual_output_mode(self) -> None:
        request = EngineRequest(root=Path("/tmp/doc-for-agent-default-output"))
        self.assertEqual(request.output_mode, "dual")
        self.assertEqual(request.human_locale, "en")
        self.assertEqual(request.human_template_variant, "paired-core")

    def test_mode_semantics_helpers_are_stable(self) -> None:
        self.assertEqual(write_strategy_for_mode("refresh"), "refresh")
        self.assertEqual(write_strategy_for_mode("generate"), "init")
        self.assertEqual(effective_profile_for_mode("migrate", "bootstrap"), "layered")
        self.assertEqual(effective_profile_for_mode("refresh", "bootstrap"), "bootstrap")

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
            explanation = build_analysis_explanation_lines(plan)
            self.assertTrue(any(line.startswith("Analysis for: ") for line in explanation))
            self.assertTrue(any("Suggested command:" in line for line in explanation))
            self.assertTrue(any("Recommended output mode: `dual`" in line for line in explanation))
            self.assertTrue(any("--output-mode dual" in line for line in explanation if line.startswith("Suggested command:")))
            self.assertTrue(any("Human locale: `en`" in line for line in explanation))
            self.assertTrue(any("Human template variant: `paired-core`" in line for line in explanation))
            self.assertTrue(any("Audience-locale mapping:" in line for line in explanation))
            self.assertTrue(any("Paired template/path contract:" in line for line in explanation))

    def test_quad_plan_writes_four_view_roots(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-engine-quad-") as tmpdir:
            sandbox_root = Path(tmpdir) / "dual_mode_app"
            shutil.copytree(TEST_ROOT / "fixtures" / "dual_mode_app", sandbox_root)

            plan = build_generation_plan(
                EngineRequest(
                    root=sandbox_root,
                    mode="generate",
                    output_mode="quad",
                    profile="layered",
                )
            )

            self.assertTrue(any(path.endswith("/AGENTS/00-entry/AGENTS.md") for path in plan.files))
            self.assertTrue(any(path.endswith("/AGENTS.zh/00-entry/AGENTS.md") for path in plan.files))
            self.assertTrue(any(path.endswith("/docs/overview.md") for path in plan.files))
            self.assertTrue(any(path.endswith("/docs.zh/overview.md") for path in plan.files))
            result = execute_engine_request(
                EngineRequest(
                    root=sandbox_root,
                    mode="generate",
                    output_mode="quad",
                    profile="layered",
                ),
                dry_run=False,
            )
            self.assertIn("four-view docs", result.summary)
            self.assertTrue((sandbox_root / "AGENTS" / "00-entry" / "AGENTS.md").exists())
            self.assertTrue((sandbox_root / "AGENTS.zh" / "00-entry" / "AGENTS.md").exists())
            self.assertTrue((sandbox_root / "docs" / "overview.md").exists())
            self.assertTrue((sandbox_root / "docs.zh" / "overview.md").exists())

    def test_validate_output_contract_rejects_asymmetric_quad_plan(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-engine-quad-contract-") as tmpdir:
            root = Path(tmpdir)
            files = {
                str(root / "AGENTS" / "00-entry" / "AGENTS.md"): "agent en",
                str(root / "AGENTS.zh" / "00-entry" / "AGENTS.md"): "agent zh",
                str(root / "docs" / "overview.md"): "human en",
                str(root / "docs.zh" / "architecture.md"): "human zh mismatch",
            }
            with self.assertRaises(ValueError):
                validate_output_contract(root, "quad", files)

    def test_migrate_mode_uses_refresh_write_mode(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-engine-migrate-") as tmpdir:
            sandbox_root = Path(tmpdir) / "layered_product_app"
            shutil.copytree(TEST_ROOT / "fixtures" / "layered_product_app", sandbox_root)

            result = execute_engine_request(
                EngineRequest(
                    root=sandbox_root,
                    mode="migrate",
                    output_mode="agent",
                    profile="layered",
                ),
                dry_run=True,
            )

            self.assertEqual(result.plan.write_mode, "refresh")
            self.assertEqual(result.plan.request.profile, "layered")
            self.assertIn("Dry run: would migrate AGENTS docs", result.summary)
            self.assertTrue(any("AGENTS/00-entry/AGENTS.md" in line for line in result.planned_actions))

    def test_refresh_and_generate_share_outputs_but_different_write_strategy(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-engine-mode-compare-") as tmpdir:
            sandbox_root = Path(tmpdir) / "dual_mode_app"
            shutil.copytree(TEST_ROOT / "fixtures" / "dual_mode_app", sandbox_root)

            refresh_plan = build_generation_plan(
                EngineRequest(
                    root=sandbox_root,
                    mode="refresh",
                    output_mode="dual",
                    profile="layered",
                )
            )
            generate_plan = build_generation_plan(
                EngineRequest(
                    root=sandbox_root,
                    mode="generate",
                    output_mode="dual",
                    profile="layered",
                )
            )

            self.assertEqual(set(refresh_plan.files.keys()), set(generate_plan.files.keys()))
            self.assertEqual(refresh_plan.write_mode, "refresh")
            self.assertEqual(generate_plan.write_mode, "init")

    def test_execute_engine_request_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-engine-apply-") as tmpdir:
            sandbox_root = Path(tmpdir) / "human_no_docs"
            shutil.copytree(TEST_ROOT / "fixtures" / "human_no_docs", sandbox_root)

            result = execute_engine_request(
                EngineRequest(
                    root=sandbox_root,
                    mode="generate",
                    output_mode="human",
                    profile="bootstrap",
                ),
                dry_run=False,
            )

            self.assertTrue((sandbox_root / "docs/overview.md").exists())
            self.assertTrue((sandbox_root / "docs/architecture.md").exists())
            self.assertFalse((sandbox_root / "AGENTS").exists())
            self.assertIn("Generated human docs in:", result.summary)

    def test_dual_refresh_preserves_manual_blocks_for_agents_and_human_docs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-engine-dual-manual-") as tmpdir:
            sandbox_root = Path(tmpdir) / "dual_mode_app"
            shutil.copytree(TEST_ROOT / "fixtures" / "dual_mode_app", sandbox_root)

            execute_engine_request(
                EngineRequest(
                    root=sandbox_root,
                    mode="generate",
                    output_mode="dual",
                    profile="layered",
                ),
                dry_run=False,
            )

            manual_block = "\n".join(
                [
                    "<!-- doc-for-agent:manual-start -->",
                    "- Human maintained note: keep release gate unchanged until CI parity is proven.",
                    "<!-- doc-for-agent:manual-end -->",
                ]
            )
            agents_path = sandbox_root / "AGENTS" / "01-product" / "002-prd.md"
            overview_path = sandbox_root / "docs" / "overview.md"
            agents_path.write_text(agents_path.read_text(encoding="utf-8").rstrip() + "\n\n" + manual_block + "\n", encoding="utf-8")
            overview_path.write_text(overview_path.read_text(encoding="utf-8").rstrip() + "\n\n" + manual_block + "\n", encoding="utf-8")

            execute_engine_request(
                EngineRequest(
                    root=sandbox_root,
                    mode="refresh",
                    output_mode="dual",
                    profile="layered",
                ),
                dry_run=False,
            )

            self.assertIn(manual_block, agents_path.read_text(encoding="utf-8"))
            self.assertIn(manual_block, overview_path.read_text(encoding="utf-8"))

    def test_dual_generate_then_refresh_is_idempotent_for_key_outputs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-engine-dual-idempotent-") as tmpdir:
            sandbox_root = Path(tmpdir) / "dual_mode_app"
            shutil.copytree(TEST_ROOT / "fixtures" / "dual_mode_app", sandbox_root)

            execute_engine_request(
                EngineRequest(
                    root=sandbox_root,
                    mode="generate",
                    output_mode="dual",
                    profile="layered",
                ),
                dry_run=False,
            )
            first_agents = (sandbox_root / "AGENTS" / "03-execution" / "008-implementation-plan.md").read_text(encoding="utf-8")
            first_overview = (sandbox_root / "docs" / "overview.md").read_text(encoding="utf-8")

            execute_engine_request(
                EngineRequest(
                    root=sandbox_root,
                    mode="refresh",
                    output_mode="dual",
                    profile="layered",
                ),
                dry_run=False,
            )
            second_agents = (sandbox_root / "AGENTS" / "03-execution" / "008-implementation-plan.md").read_text(encoding="utf-8")
            second_overview = (sandbox_root / "docs" / "overview.md").read_text(encoding="utf-8")

            self.assertEqual(first_agents, second_agents)
            self.assertEqual(first_overview, second_overview)

    def test_layered_human_docs_reference_paired_agent_docs(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-engine-layered-human-pairs-") as tmpdir:
            sandbox_root = Path(tmpdir) / "dual_mode_app"
            shutil.copytree(TEST_ROOT / "fixtures" / "dual_mode_app", sandbox_root)

            result = execute_engine_request(
                EngineRequest(
                    root=sandbox_root,
                    mode="generate",
                    output_mode="human",
                    profile="layered",
                ),
                dry_run=False,
            )

            self.assertIn("Generated human docs in:", result.summary)
            overview = (sandbox_root / "docs" / "overview.md").read_text(encoding="utf-8")
            architecture = (sandbox_root / "docs" / "architecture.md").read_text(encoding="utf-8")
            workflows = (sandbox_root / "docs" / "workflows.md").read_text(encoding="utf-8")
            self.assertIn("## Paired Agent Docs (Dual Mode)", overview)
            self.assertIn("AGENTS/01-product/001-core-goals.md", overview)
            self.assertIn("AGENTS/02-architecture/007-architecture-compatibility.md", architecture)
            self.assertIn("AGENTS/03-execution/008-implementation-plan.md", workflows)
            self.assertIn("## Output Boundary (Human vs Agent)", overview)
            self.assertIn("## Output Boundary (Human vs Agent)", architecture)
            self.assertIn("## Output Boundary (Human vs Agent)", workflows)
            self.assertIn("## Dual Pairing Contract (Rules)", overview)
            self.assertIn("## Dual Pairing Contract (Rules)", architecture)
            self.assertIn("## Dual Pairing Contract (Rules)", workflows)
            self.assertIn("## Paired Refresh Rules", overview)
            self.assertIn("## Paired Refresh Rules", architecture)
            self.assertIn("## Paired Refresh Rules", workflows)
            self.assertIn("## Dual View Rationale", overview)
            self.assertIn("## Dual View Rationale", architecture)
            self.assertIn("## Dual View Rationale", workflows)
            self.assertIn("Template rule: human template variant `paired-core`", overview)
            self.assertNotIn("(sources:", overview)
            self.assertNotIn("(sources:", architecture)
            self.assertNotIn("(sources:", workflows)

    def test_human_locale_zh_writes_docs_zh_output_root(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-engine-human-zh-") as tmpdir:
            sandbox_root = Path(tmpdir) / "dual_mode_app"
            shutil.copytree(TEST_ROOT / "fixtures" / "dual_mode_app", sandbox_root)

            result = execute_engine_request(
                EngineRequest(
                    root=sandbox_root,
                    mode="generate",
                    output_mode="dual",
                    human_locale="zh",
                    human_template_variant="paired-core",
                    profile="layered",
                ),
                dry_run=False,
            )

            self.assertIn("AGENTS + human docs", result.summary)
            self.assertTrue((sandbox_root / "docs.zh" / "overview.md").exists())
            self.assertTrue((sandbox_root / "docs.zh" / "architecture.md").exists())
            self.assertFalse((sandbox_root / "docs" / "overview.md").exists())
            overview = (sandbox_root / "docs.zh" / "overview.md").read_text(encoding="utf-8")
            self.assertIn("`docs.zh/` and `AGENTS/` are two views generated from the same repository analysis", overview)
            self.assertIn("Locale-output rule: human locale `zh` maps to `docs.zh/`.", overview)

    def test_invalid_human_template_variant_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-engine-template-invalid-") as tmpdir:
            sandbox_root = Path(tmpdir) / "dual_mode_app"
            shutil.copytree(TEST_ROOT / "fixtures" / "dual_mode_app", sandbox_root)

            with self.assertRaises(ValueError):
                build_generation_plan(
                    EngineRequest(
                        root=sandbox_root,
                        mode="generate",
                        output_mode="human",
                        human_template_variant="unknown-template",
                        profile="layered",
                    )
                )


if __name__ == "__main__":
    unittest.main()
