#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def repo_root_from(path: Path) -> Path:
    current = path.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "src/doc_for_agent").exists():
            return candidate
    package_root = current.parent
    if (package_root / "platforms").exists() and (package_root / "scripts").exists():
        return package_root
    raise FileNotFoundError("Could not locate doc-for-agent content root")


def default_dest(ai: str, cwd: Path) -> Path:
    mapping = {
        "codex": Path.home() / ".codex/skills/doc-for-agent",
        "claude": cwd / ".claude/skills/doc-for-agent",
        "cursor": cwd / ".cursor/skills/doc-for-agent",
        "continue": cwd / ".continue/skills/doc-for-agent",
        "windsurf": cwd / ".windsurf/skills/doc-for-agent",
    }
    return mapping[ai]


def copy_tree(src: Path, dst: Path, force: bool) -> None:
    if dst.exists():
        if not force:
            raise FileExistsError(f"Destination already exists: {dst}")
        shutil.rmtree(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns(".DS_Store", "__pycache__", "*.pyc"))


def run_sync(repo_root: Path) -> None:
    sync_script = repo_root / "scripts/sync_platform_adapters.py"
    if sync_script.exists():
        subprocess.run([sys.executable, str(sync_script)], check=True)

def content_root(repo_root: Path) -> Path:
    src_root = repo_root / "src/doc_for_agent"
    if src_root.exists():
        return src_root
    return repo_root


def build_adapter_bundle(content: Path, ai: str, staging_root: Path) -> Path:
    platform_root = content / "platforms" / ai
    bundle_root = staging_root / ai
    shutil.copytree(platform_root, bundle_root)

    scripts_dst = bundle_root / "scripts"
    refs_dst = bundle_root / "references"
    scripts_dst.mkdir(parents=True, exist_ok=True)
    refs_dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(content / "scripts/init_agents_docs.py", scripts_dst / "init_agents_docs.py")
    shutil.copy2(content / "references/agents-structure.md", refs_dst / "agents-structure.md")
    return bundle_root


def install_target(ai: str, cwd: Path, dest: str | None) -> Path:
    if dest:
        return Path(dest).expanduser().resolve()
    return default_dest(ai, cwd)


def cmd_init(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).expanduser().resolve()
    cwd = Path.cwd()
    content = content_root(repo_root)

    run_sync(repo_root)

    targets = ["codex", "claude", "cursor", "continue", "windsurf"] if args.ai == "all" else [args.ai]
    with tempfile.TemporaryDirectory(prefix="doc-for-agent-install-") as tmpdir:
        staging = Path(tmpdir)
        for ai in targets:
            src = build_adapter_bundle(content, ai, staging)
            dst = install_target(ai, cwd, args.dest if len(targets) == 1 else None)
            copy_tree(src, dst, force=args.force)
            print(f"Installed {ai} adapter to: {dst}")

    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).expanduser().resolve()
    run_sync(repo_root)
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    repo_root = Path(args.repo_root).expanduser().resolve()
    content = content_root(repo_root)
    checks = {
        "content_root": content,
        "platform_codex": content / "platforms/codex/SKILL.md",
        "platform_claude": content / "platforms/claude/SKILL.md",
        "platform_cursor": content / "platforms/cursor/SKILL.md",
        "platform_continue": content / "platforms/continue/SKILL.md",
        "platform_windsurf": content / "platforms/windsurf/SKILL.md",
        "generator": content / "scripts/init_agents_docs.py",
        "reference": content / "references/agents-structure.md",
    }
    failures = []
    for label, path in checks.items():
        exists = path.exists()
        print(f"{label}: {'OK' if exists else 'MISSING'} - {path}")
        if not exists:
            failures.append(label)
    return 1 if failures else 0


def build_parser(default_repo_root: Path) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Installer and maintenance CLI for doc-for-agent.")
    parser.set_defaults(func=None)
    parser.add_argument(
        "--repo-root",
        default=str(default_repo_root),
        help="Path to the doc-for-agent repository root.",
    )

    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Install a platform adapter into a target environment.")
    init_parser.add_argument(
        "--ai",
        choices=["codex", "claude", "cursor", "continue", "windsurf", "all"],
        required=True,
        help="Which adapter to install.",
    )
    init_parser.add_argument("--dest", help="Optional explicit install destination for single-target installs.")
    init_parser.add_argument("--force", action="store_true", help="Overwrite an existing destination.")
    init_parser.set_defaults(func=cmd_init)

    sync_parser = subparsers.add_parser("sync", help="Sync adapter files from source-of-truth.")
    sync_parser.set_defaults(func=cmd_sync)

    doctor_parser = subparsers.add_parser("doctor", help="Check that source and adapter files exist.")
    doctor_parser.set_defaults(func=cmd_doctor)

    return parser


def main() -> int:
    repo_root = repo_root_from(Path(__file__))
    parser = build_parser(repo_root)
    args = parser.parse_args()
    if args.func is None:
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
