#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")


def main() -> None:
    src_root = Path(__file__).resolve().parents[1]
    templates_root = src_root / "templates"
    body_root = templates_root / "bodies"
    platform_root = src_root / "platforms"
    config_root = platform_root / "configs"
    shell_template = read_text(templates_root / "platform_skill.md")

    for config_path in sorted(config_root.glob("*.json")):
        config = json.loads(read_text(config_path))
        platform = config["platform"]
        body_template_name = config["body_template"]
        body = read_text(body_root / body_template_name)
        body = body.format(**config)
        rendered = shell_template.format(
            name=config["name"],
            description=config["description"],
            body=body,
        )
        write_text(platform_root / platform / "SKILL.md", rendered)

    print("Generated platform SKILL adapters from config.")


if __name__ == "__main__":
    main()
