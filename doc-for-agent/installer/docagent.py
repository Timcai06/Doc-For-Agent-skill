#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence


INSTALLER_ROOT = Path(__file__).resolve().parent
REPO_SKILL_ROOT = INSTALLER_ROOT.parent
PACKAGED_ASSETS_ROOT = INSTALLER_ROOT / "assets"


def is_runtime_root(path: Path) -> bool:
    return (path / "templates" / "product.json").exists() and (path / "scripts" / "render_platform_adapter.py").exists()


RUNTIME_ROOT = REPO_SKILL_ROOT if is_runtime_root(REPO_SKILL_ROOT) else PACKAGED_ASSETS_ROOT
SCRIPTS_ROOT = RUNTIME_ROOT / "scripts"

if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from render_platform_adapter import (  # noqa: E402
    available_platforms,
    bundled_asset_directories,
    install_receipt_path,
    install_platform,
    load_product_metadata,
    load_platform_config,
    platform_install_root,
)
from init_agents_docs import SUPPORTED_DOC_PROFILES, SUPPORTED_REPO_TYPES  # noqa: E402


@dataclass(frozen=True)
class PlatformDoctorStatus:
    platform: str
    display_name: str
    assistant_root: Path
    install_root: Path
    installed: bool
    assistant_root_exists: bool
    installed_version: Optional[str]
    receipt_path: Path


def resolve_target_root(target: str) -> Path:
    return Path(target).expanduser().resolve()


def resolve_generator_script() -> Path:
    return RUNTIME_ROOT / "scripts" / "init_agents_docs.py"


def run_generator_command(args: Sequence[str]) -> int:
    script_path = resolve_generator_script()
    if not script_path.exists():
        print(f"Generator entrypoint not found: {script_path}")
        return 2
    python_cmd = shutil.which("python3") or shutil.which("python")
    if not python_cmd:
        print("Python is required to run the generator, but no `python3` or `python` executable was found.")
        return 2

    command = [python_cmd, str(script_path), *args]
    completed = subprocess.run(command, check=False)
    return completed.returncode


def load_install_receipt(install_root: Path) -> dict[str, object]:
    try:
        return json.loads(install_receipt_path(install_root).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def collect_doctor_statuses(target_root: Path, platforms: Optional[Sequence[str]] = None) -> List[PlatformDoctorStatus]:
    selected_platforms = list(platforms or available_platforms())
    statuses: List[PlatformDoctorStatus] = []
    for platform in selected_platforms:
        config = load_platform_config(platform)
        assistant_root = target_root / config.folder_structure["root"]
        install_root = platform_install_root(target_root, config)
        adapter_file = install_root / config.folder_structure["filename"]
        receipt_path = install_receipt_path(install_root)
        receipt = load_install_receipt(install_root)
        statuses.append(
            PlatformDoctorStatus(
                platform=platform,
                display_name=config.display_name,
                assistant_root=assistant_root,
                install_root=install_root,
                installed=adapter_file.exists(),
                assistant_root_exists=assistant_root.exists(),
                installed_version=str(receipt.get("version")) if receipt.get("version") else None,
                receipt_path=receipt_path,
            )
        )
    return statuses


def render_doctor_report(target_root: Path, statuses: Iterable[PlatformDoctorStatus]) -> str:
    metadata = load_product_metadata()
    python_path = shutil.which("python3") or shutil.which("python") or "missing"
    lines = [
        f"{metadata.product_name} doctor",
        f"- Version: {metadata.version}",
        f"- Target root: {target_root}",
        f"- Skill source: {RUNTIME_ROOT}",
        f"- Python: {python_path}",
        f"- Bundled assets: {', '.join(bundled_asset_directories())}",
    ]

    for status in statuses:
        install_state = "installed" if status.installed else "not installed"
        root_state = "assistant folder present" if status.assistant_root_exists else "assistant folder will be created"
        version_state = f"version={status.installed_version}" if status.installed_version else "version=unknown"
        lines.append(
            f"- {status.display_name} ({status.platform}): {install_state}; {version_state}; {root_state}; target={status.install_root}"
        )
    return "\n".join(lines)


def install_selected_platforms(target_root: Path, platforms: Sequence[str]) -> List[Path]:
    installed_paths: List[Path] = []
    for platform in platforms:
        installed_paths.append(install_platform(target_root, load_platform_config(platform)))
    return installed_paths


def detect_installed_platforms(
    target_root: Path,
    platforms: Optional[Sequence[str]] = None,
) -> List[str]:
    statuses = collect_doctor_statuses(target_root, platforms)
    return [status.platform for status in statuses if status.installed]


def resolve_update_platforms(target_root: Path, requested_platform: str) -> List[str]:
    if requested_platform == "all":
        return detect_installed_platforms(target_root)

    statuses = collect_doctor_statuses(target_root, [requested_platform])
    if statuses and statuses[0].installed:
        return [requested_platform]
    return []


def render_versions_report(target_root: Path, statuses: Iterable[PlatformDoctorStatus]) -> str:
    metadata = load_product_metadata()
    lines = [
        f"{metadata.product_name} versions",
        f"- Source version: {metadata.version}",
        f"- Target root: {target_root}",
    ]
    for status in statuses:
        installed_version = status.installed_version or "not installed"
        lines.append(f"- {status.display_name} ({status.platform}): {installed_version}")
    return "\n".join(lines)


def render_quickstart(target_root: Path) -> str:
    metadata = load_product_metadata()
    lines = [
        f"{metadata.product_name} quickstart",
        "- Recommended entry by user type:",
        "- Node users: `npx -y doc-for-agent`",
        "- Python users: `pipx install .` or `python3 -m pip install .`",
        "- Unified product command: `docagent`",
        "- First commands:",
        f"- `docagent doctor --target {target_root}`",
        f"- `docagent all --target {target_root}`",
        f"- `docagent versions --target {target_root}`",
        "- Supported platforms:",
    ]
    for platform in available_platforms():
        config = load_platform_config(platform)
        install_root = platform_install_root(target_root, config)
        lines.append(f"- {config.display_name} ({platform}): {install_root}")
    return "\n".join(lines)


def print_install_summary(target_root: Path, platforms: Sequence[str], installed_paths: Sequence[Path]) -> None:
    metadata = load_product_metadata()
    print(f"{metadata.product_name} install")
    print(f"- Version: {metadata.version}")
    print(f"- Target root: {target_root}")
    print(f"- Platforms: {', '.join(platforms)}")
    print("Installed platform adapters:")
    for path in installed_paths:
        print(f"- {path}")
    print("Next steps:")
    print(f"- Run `{metadata.installer_command} doctor --target {target_root}` to verify the install.")
    print("- Restart the relevant assistant so the new local skill bundle is loaded.")


def print_update_summary(target_root: Path, platforms: Sequence[str], installed_paths: Sequence[Path]) -> None:
    metadata = load_product_metadata()
    print(f"{metadata.product_name} update")
    print(f"- Version: {metadata.version}")
    print(f"- Target root: {target_root}")
    print(f"- Platforms: {', '.join(platforms)}")
    print("Updated platform adapters:")
    for path in installed_paths:
        print(f"- {path}")
    print("Next steps:")
    print(f"- Run `{metadata.installer_command} versions --target {target_root}` to confirm installed versions.")
    print("- Restart the relevant assistant if it was already running.")


def build_parser() -> argparse.ArgumentParser:
    metadata = load_product_metadata()
    parser = argparse.ArgumentParser(
        description=f"Install {metadata.product_name} platform adapters into repository-local assistant folders."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{metadata.product_name} {metadata.version}",
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

    all_parser = subparsers.add_parser("all", help="Install all supported platform adapters.")
    all_parser.add_argument("--target", default=".", help="Repository root where assistant folders should live.")

    versions_parser = subparsers.add_parser("versions", help="Show source and installed platform versions.")
    versions_parser.add_argument("--target", default=".", help="Repository root where assistant folders should live.")
    versions_parser.add_argument(
        "--platform",
        choices=available_platforms() + ["all"],
        default="all",
        help="Limit version output to one platform.",
    )

    update_parser = subparsers.add_parser("update", help="Refresh installed platform adapters to the current source version.")
    update_parser.add_argument("--target", default=".", help="Repository root where assistant folders should live.")
    update_parser.add_argument(
        "--platform",
        choices=available_platforms() + ["all"],
        default="all",
        help="Update one installed platform or all installed platforms.",
    )

    generate_parser = subparsers.add_parser(
        "generate",
        help="Run the bundled AGENTS generator through a product CLI surface.",
    )
    generate_parser.add_argument("--root", default=".", help="Repository root where AGENTS docs should be generated.")
    generate_parser.add_argument("--project-name", help="Optional explicit project name.")
    generate_parser.add_argument("--mode", choices=["init", "refresh"], default="refresh")
    generate_parser.add_argument("--dry-run", action="store_true")
    generate_parser.add_argument("--repo-type", choices=SUPPORTED_REPO_TYPES)
    generate_parser.add_argument("--profile", choices=SUPPORTED_DOC_PROFILES, default="bootstrap")
    generate_parser.add_argument("--explain", action="store_true")

    refresh_parser = subparsers.add_parser(
        "refresh",
        help="Shortcut for `generate --mode refresh`.",
    )
    refresh_parser.add_argument("--root", default=".", help="Repository root where AGENTS docs should be generated.")
    refresh_parser.add_argument("--project-name", help="Optional explicit project name.")
    refresh_parser.add_argument("--dry-run", action="store_true")
    refresh_parser.add_argument("--repo-type", choices=SUPPORTED_REPO_TYPES)
    refresh_parser.add_argument("--profile", choices=SUPPORTED_DOC_PROFILES, default="bootstrap")
    refresh_parser.add_argument("--explain", action="store_true")

    quickstart_parser = subparsers.add_parser(
        "quickstart",
        help="Show recommended install and first-use commands for Node and Python users.",
    )
    quickstart_parser.add_argument("--target", default=".", help="Repository root for example install commands.")

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "doctor":
        target_root = resolve_target_root(args.target)
        platforms = available_platforms() if args.platform == "all" else [args.platform]
        print(render_doctor_report(target_root, collect_doctor_statuses(target_root, platforms)))
        return 0

    if args.command in {"install", "all"}:
        target_root = resolve_target_root(args.target)
        platforms = available_platforms() if args.command == "all" or args.platform == "all" else [args.platform]
        installed_paths = install_selected_platforms(target_root, platforms)
        print_install_summary(target_root, platforms, installed_paths)
        return 0

    if args.command == "versions":
        target_root = resolve_target_root(args.target)
        platforms = available_platforms() if args.platform == "all" else [args.platform]
        print(render_versions_report(target_root, collect_doctor_statuses(target_root, platforms)))
        return 0

    if args.command == "quickstart":
        target_root = resolve_target_root(args.target)
        print(render_quickstart(target_root))
        return 0

    if args.command == "update":
        target_root = resolve_target_root(args.target)
        platforms = resolve_update_platforms(target_root, args.platform)
        if not platforms:
            if args.platform == "all":
                print("No installed platforms were detected. Run `install` or `all` first.")
            else:
                print(
                    f"Platform `{args.platform}` is not currently installed in {target_root}. "
                    "Run `install` first."
                )
            return 1
        installed_paths = install_selected_platforms(target_root, platforms)
        print_update_summary(target_root, platforms, installed_paths)
        return 0

    if args.command in {"generate", "refresh"}:
        generator_root = resolve_target_root(args.root)
        generator_args = ["--root", str(generator_root), "--mode", "refresh" if args.command == "refresh" else args.mode]
        if args.project_name:
            generator_args.extend(["--project-name", args.project_name])
        if args.repo_type:
            generator_args.extend(["--repo-type", args.repo_type])
        if args.profile:
            generator_args.extend(["--profile", args.profile])
        if args.dry_run:
            generator_args.append("--dry-run")
        if args.explain:
            generator_args.append("--explain")

        return run_generator_command(generator_args)

    parser.error(f"Unsupported command: {args.command}")
    return 2


def cli() -> None:
    raise SystemExit(main())


if __name__ == "__main__":
    cli()
