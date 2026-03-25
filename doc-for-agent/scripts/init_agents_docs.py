#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict

from doc_for_agent_generator import (
    MANUAL_END,
    MANUAL_START,
    analyze_repo,
    generate_docs as generate_docs_from_analysis,
    infer_project_name,
    merge_markdown,
    read_text,
    write_file,
)

__all__ = [
    "MANUAL_END",
    "MANUAL_START",
    "generate_docs",
    "main",
    "merge_markdown",
    "read_text",
    "write_file",
]


def generate_docs(root: Path, project_name: str) -> Dict[str, str]:
    # Keep the historical entrypoint shape while delegating to the modular core.
    return generate_docs_from_analysis(analyze_repo(root, project_name))


def resolve_output_content(path: Path, generated: str, mode: str) -> str:
    if mode == "refresh" and path.exists():
        return merge_markdown(read_text(path), generated)
    return generated


def describe_dry_run(root: Path, mode: str, files: Dict[str, str]) -> None:
    agents_dir = root / "AGENTS"
    print(f"Dry run: would {mode} AGENTS docs in: {agents_dir}")

    for name, generated in files.items():
        path = agents_dir / name
        resolved = resolve_output_content(path, generated, mode)
        if not path.exists():
            action = "create"
        elif read_text(path) == resolved:
            action = "unchanged"
        else:
            action = "update"
        print(f"- {action} AGENTS/{name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize or refresh an AGENTS documentation directory.")
    parser.add_argument("--root", required=True, help="Repository root where AGENTS/ should be created or refreshed.")
    parser.add_argument("--project-name", help="Optional explicit project name.")
    parser.add_argument("--mode", choices=["init", "refresh"], default="refresh", help="Whether to initialize or refresh AGENTS docs.")
    parser.add_argument("--dry-run", action="store_true", help="Preview AGENTS file changes without writing anything.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    project_name = infer_project_name(root, args.project_name)
    files = generate_docs(root, project_name)

    if args.dry_run:
        describe_dry_run(root, args.mode, files)
        return

    agents_dir = root / "AGENTS"
    agents_dir.mkdir(parents=True, exist_ok=True)

    for name, content in files.items():
        path = agents_dir / name
        write_file(path, resolve_output_content(path, content, args.mode))

    print(f"{args.mode.capitalize()}ed AGENTS docs in: {agents_dir}")


if __name__ == "__main__":
    main()
