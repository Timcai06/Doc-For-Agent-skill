#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

from doc_for_agent_generator.utils import read_text, write_file


@dataclass(frozen=True)
class PlatformConfig:
    platform: str
    display_name: str
    install_type: str
    adapter_kind: str
    folder_structure: Dict[str, str]
    frontmatter: Dict[str, str]
    default_title: str
    default_description: str
    quick_reference: bool
    script_relpath: str
    post_install_notes: List[str]


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def templates_root() -> Path:
    return skill_root() / "templates"


def load_template(name: str) -> str:
    return read_text(templates_root() / "base" / name)


def available_platforms() -> List[str]:
    configs_dir = templates_root() / "platforms"
    return sorted(path.stem for path in configs_dir.glob("*.json"))


def load_platform_config(platform: str) -> PlatformConfig:
    config_path = templates_root() / "platforms" / f"{platform}.json"
    payload = json.loads(read_text(config_path))
    return PlatformConfig(
        platform=str(payload["platform"]),
        display_name=str(payload["display_name"]),
        install_type=str(payload["install_type"]),
        adapter_kind=str(payload["adapter_kind"]),
        folder_structure={str(key): str(value) for key, value in payload["folder_structure"].items()},
        frontmatter={str(key): str(value) for key, value in (payload.get("frontmatter") or {}).items()},
        default_title=str(payload["default_title"]),
        default_description=str(payload["default_description"]),
        quick_reference=bool(payload.get("quick_reference", False)),
        script_relpath=str(payload["script_relpath"]),
        post_install_notes=[str(item) for item in payload.get("post_install_notes", [])],
    )


def render_frontmatter(frontmatter: Dict[str, str]) -> str:
    if not frontmatter:
        return ""
    lines = ["---"]
    for key, value in frontmatter.items():
        escaped = value.replace('"', '\\"')
        lines.append(f'{key}: "{escaped}"')
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def render_post_install(notes: Iterable[str]) -> str:
    items = list(notes)
    if not items:
        return "- No additional post-install notes."
    return "\n".join(f"- {item}" for item in items)


def render_adapter(config: PlatformConfig) -> str:
    template_name = "skill-content.md" if config.adapter_kind == "skill" else "workflow-content.md"
    content = load_template(template_name)
    replacements = {
        "{{FRONTMATTER}}": render_frontmatter(config.frontmatter),
        "{{TITLE}}": config.default_title,
        "{{DESCRIPTION}}": config.default_description,
        "{{SCRIPT_REL_PATH}}": config.script_relpath,
        "{{DISPLAY_NAME}}": config.display_name,
        "{{INSTALL_TYPE}}": config.install_type,
        "{{POST_INSTALL_NOTES}}": render_post_install(config.post_install_notes),
    }
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    return content


def install_platform(target_root: Path, config: PlatformConfig) -> Path:
    install_root = target_root / config.folder_structure["root"] / config.folder_structure["skill_path"]
    install_root.mkdir(parents=True, exist_ok=True)

    write_file(install_root / config.folder_structure["filename"], render_adapter(config))
    shutil.copytree(skill_root() / "scripts", install_root / "scripts", dirs_exist_ok=True)
    shutil.copytree(skill_root() / "references", install_root / "references", dirs_exist_ok=True)
    agent_manifest = skill_root() / "agents"
    if agent_manifest.exists():
        shutil.copytree(agent_manifest, install_root / "agents", dirs_exist_ok=True)
    return install_root


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a platform-specific adapter wrapper for doc-for-agent.")
    parser.add_argument(
        "--platform",
        choices=available_platforms() + ["all"],
        required=True,
        help="Platform adapter to render.",
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Project root where the platform-specific folder should be written.",
    )
    args = parser.parse_args()

    target_root = Path(args.target).expanduser().resolve()
    platforms = available_platforms() if args.platform == "all" else [args.platform]

    installed_paths: List[Path] = []
    for platform in platforms:
        installed_paths.append(install_platform(target_root, load_platform_config(platform)))

    print("Installed platform adapters:")
    for path in installed_paths:
        print(f"- {path}")


if __name__ == "__main__":
    main()
