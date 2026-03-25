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

from render_platform_adapter import available_platforms, install_platform, load_platform_config, render_adapter


class PlatformAdapterTests(unittest.TestCase):
    def test_supported_platforms_include_codex_and_claude(self) -> None:
        platforms = available_platforms()
        self.assertIn("codex", platforms)
        self.assertIn("claude", platforms)

    def test_rendered_codex_adapter_uses_codex_paths(self) -> None:
        config = load_platform_config("codex")
        content = render_adapter(config)

        self.assertIn('name: "doc-for-agent"', content)
        self.assertIn("python3 .codex/skills/doc-for-agent/scripts/init_agents_docs.py", content)
        self.assertIn("- Platform: Codex", content)

    def test_install_platform_writes_self_contained_adapter_tree(self) -> None:
        with tempfile.TemporaryDirectory(prefix="doc-for-agent-adapter-") as tmpdir:
            target_root = Path(tmpdir)
            install_root = install_platform(target_root, load_platform_config("claude"))

            self.assertTrue((install_root / "SKILL.md").exists())
            self.assertTrue((install_root / "scripts" / "init_agents_docs.py").exists())
            self.assertTrue((install_root / "references" / "agents-structure.md").exists())
            self.assertTrue((install_root / "agents" / "openai.yaml").exists())

            skill_text = (install_root / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("python3 .claude/skills/doc-for-agent/scripts/init_agents_docs.py", skill_text)


if __name__ == "__main__":
    unittest.main()
