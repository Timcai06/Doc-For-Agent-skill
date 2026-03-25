#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path


def copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    src_root = repo_root / "src/doc_for_agent"

    copy_map = {
        src_root / "platforms/codex/SKILL.md": [
            repo_root / "doc-for-agent/SKILL.md",
        ],
        src_root / "platforms/codex/agents/openai.yaml": [
            repo_root / "doc-for-agent/agents/openai.yaml",
        ],
        src_root / "platforms/claude/SKILL.md": [
            repo_root / ".claude/skills/doc-for-agent/SKILL.md",
        ],
        src_root / "platforms/cursor/SKILL.md": [
            repo_root / ".cursor/skills/doc-for-agent/SKILL.md",
        ],
        src_root / "platforms/continue/SKILL.md": [
            repo_root / ".continue/skills/doc-for-agent/SKILL.md",
        ],
        src_root / "platforms/windsurf/SKILL.md": [
            repo_root / ".windsurf/skills/doc-for-agent/SKILL.md",
        ],
        src_root / "scripts/init_agents_docs.py": [
            repo_root / "doc-for-agent/scripts/init_agents_docs.py",
            repo_root / ".claude/skills/doc-for-agent/scripts/init_agents_docs.py",
            repo_root / ".cursor/skills/doc-for-agent/scripts/init_agents_docs.py",
            repo_root / ".continue/skills/doc-for-agent/scripts/init_agents_docs.py",
            repo_root / ".windsurf/skills/doc-for-agent/scripts/init_agents_docs.py",
        ],
        src_root / "references/agents-structure.md": [
            repo_root / "doc-for-agent/references/agents-structure.md",
            repo_root / ".claude/skills/doc-for-agent/references/agents-structure.md",
            repo_root / ".cursor/skills/doc-for-agent/references/agents-structure.md",
            repo_root / ".continue/skills/doc-for-agent/references/agents-structure.md",
            repo_root / ".windsurf/skills/doc-for-agent/references/agents-structure.md",
        ],
    }

    for source, destinations in copy_map.items():
        for destination in destinations:
            copy_file(source, destination)

    print("Synced source-of-truth files into platform adapters.")


if __name__ == "__main__":
    main()
