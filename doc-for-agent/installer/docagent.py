#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence


INSTALLER_ROOT = Path(__file__).resolve().parent
SKILL_ROOT = INSTALLER_ROOT.parent
SCRIPTS_ROOT = SKILL_ROOT / "scripts"

if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from render_platform_adapter import (  # noqa: E402
    available_platforms,
    bundled_asset_directories,
    install_platform,
    load_platform_config,
    platform_install_root,
)


@dataclass(frozen=True)
class PlatformDoctorStatus:
    platform: str
    display_name: str
    assistant_root: Path
    install_root: Path
    installed: bool
    assistant_root_exists: bool


def resolve_target_root(target: str) -> Path:
    return Path(target).expanduser().resolve()


def collect_doctor_statuses(target_root: Path, platforms: Sequence[str] | None = None) -> List[PlatformDoctorStatus]:
    selected_platforms = list(platforms or available_platforms())
    statuses: List[PlatformDoctorStatus] = []
    for platform in selected_platforms:
        config = load_platform_config(platform)
        assistant_root = target_root / config.folder_structure["root"]
        install_root = platform_install_root(target_root, config)
        adapter_file = install_root / config.folder_structure["filename"]
        statuses.append(
            PlatformDoctorStatus(
                platform=platform,
                display_name=config.display_name,
                assistant_root=assistant_root,
                install_root=install_root,
                installed=adapter_file.exists(),
                assistant_root_exists=assistant_root.exists(),
            )
        )
    return statuses


def render_doctor_report(target_root: Path, statuses: Iterable[PlatformDoctorStatus]) -> str:
    python_path = shutil.which("python3") or shutil.which("python") or "missing"
    lines = [
        f"doc-for-agent doctor",
        f"- Target root: {target_root}",
        f"- Skill source: {SKILL_ROOT}",
        f"- Python: {python_path}",
        f"- Bundled assets: {', '.join(bundled_asset_directories())}",
    ]

    for status in statuses:
        install_state = "installed" if status.installed else "not installed"
        root_state = "assistant folder present" if status.assistant_root_exists else "assistant folder will be created"
        lines.append(
            f"- {status.display_name} ({status.platform}): {install_state}; {root_state}; target={status.install_root}"
        )
    return "\n".join(lines)


def install_selected_platforms(target_root: Path, platforms: Sequence[str]) -> List[Path]:
    installed_paths: List[Path] = []
    for platform in platforms:
        installed_paths.append(install_platform(target_root, load_platform_config(platform)))
    return installed_paths


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install doc-for-agent platform adapters into a repository-local assistant folder."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor_parser = subparsers.add_parser("doctor", help="Inspect the target repository and install destinations.")
    doctor_parser.add_argument("--target", default=".", help="Repository root where assistant folders should live.")
    doctor_parser.add_argument(
        "--platform",
        choices=available_platforms() + ["all"],
        default="all",
        help="Limit doctor output to one platform.",
    )

    install_parser = subparsers.add_parser("install", help="Install one or more platform adapters.")
    install_parser.add_argument(
        "--platform",
        choices=available_platforms() + ["all"],
        required=True,
        help="Platform adapter to install.",
    )
    install_parser.add_argument("--target", default=".", help="Repository root where assistant folders should live.")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    target_root = resolve_target_root(args.target)

    if args.command == "doctor":
        platforms = available_platforms() if args.platform == "all" else [args.platform]
        print(render_doctor_report(target_root, collect_doctor_statuses(target_root, platforms)))
        return 0

    if args.command == "install":
        platforms = available_platforms() if args.platform == "all" else [args.platform]
        installed_paths = install_selected_platforms(target_root, platforms)
        print("Installed platform adapters:")
        for path in installed_paths:
            print(f"- {path}")
        return 0

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
