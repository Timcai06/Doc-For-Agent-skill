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


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize or refresh an AGENTS documentation directory.")
    parser.add_argument("--root", required=True, help="Repository root where AGENTS/ should be created or refreshed.")
    parser.add_argument("--project-name", help="Optional explicit project name.")
    parser.add_argument("--mode", choices=["init", "refresh"], default="refresh", help="Whether to initialize or refresh AGENTS docs.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    agents_dir = root / "AGENTS"
    agents_dir.mkdir(parents=True, exist_ok=True)

    project_name = infer_project_name(root, args.project_name)
    files = generate_docs(root, project_name)

    for name, content in files.items():
        path = agents_dir / name
        if args.mode == "refresh" and path.exists():
            merged = merge_markdown(read_text(path), content)
            write_file(path, merged)
        else:
            write_file(path, content)

    print(f"{args.mode.capitalize()}ed AGENTS docs in: {agents_dir}")


if __name__ == "__main__":
    main()
