from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


TEST_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_ROOT = TEST_ROOT.parents[0] / "scripts"

if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from render_platform_adapter import (
    available_platforms,
    install_platform,
    load_platform_config,
    load_product_metadata,
    render_adapter,
)


class PlatformAdapterTests(unittest.TestCase):
    def test_supported_platforms_include_codex_and_claudecode(self) -> None:
        platforms = available_platforms()
        self.assertIn("codex", platforms)
        self.assertIn("claudecode", platforms)
        self.assertNotIn("claude", platforms)
        self.assertIn("continue", platforms)
        self.assertIn("copilot", platforms)

    def test_rendered_codex_adapter_uses_codex_paths(self) -> None:
        config = load_platform_config("codex")
        content = render_adapter(config)

        self.assertIn('name: "doc-for-agent"', content)
        self.assertIn("python3 .codex/skills/doc-for-agent/scripts/init_agents_docs.py", content)
        self.assertIn("- Platform: Codex", content)

    def test_install_platform_writes_self_contained_adapter_tree(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-adapter-") as tmpdir:
            target_root = Path(tmpdir)
            install_root = install_platform(target_root, load_platform_config("claudecode"))
            receipt_path = install_root / load_product_metadata().install_receipt_filename

            self.assertTrue((install_root / "SKILL.md").exists())
            self.assertTrue((install_root / "scripts" / "init_agents_docs.py").exists())
            self.assertTrue((install_root / "references" / "agents-structure.md").exists())
            self.assertTrue((install_root / "agents" / "openai.yaml").exists())
            self.assertTrue((install_root / "templates" / "platforms" / "codex.json").exists())
            self.assertTrue((install_root / "installer" / "docagent.py").exists())
            self.assertTrue((install_root / "installer" / "node" / "docagent.js").exists())
            self.assertTrue(receipt_path.exists())

            skill_text = (install_root / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("python3 .claude/skills/doc-for-agent/scripts/init_agents_docs.py", skill_text)

            receipt_text = receipt_path.read_text(encoding="utf-8")
            self.assertIn('"platform": "claudecode"', receipt_text)
            self.assertIn('"version": "0.3.0.dev1"', receipt_text)

    def test_rendered_continue_adapter_uses_continue_paths(self) -> None:
        config = load_platform_config("continue")
        content = render_adapter(config)

        self.assertIn("python3 .continue/skills/doc-for-agent/scripts/init_agents_docs.py", content)
        self.assertIn("- Platform: Continue", content)

    def test_rendered_copilot_adapter_uses_prompt_paths(self) -> None:
        config = load_platform_config("copilot")
        content = render_adapter(config)

        self.assertIn("python3 .github/prompts/doc-for-agent/scripts/init_agents_docs.py", content)
        self.assertIn("- Platform: GitHub Copilot", content)
        self.assertIn("- Adapter type: prompt", content)


if __name__ == "__main__":
    unittest.main()
