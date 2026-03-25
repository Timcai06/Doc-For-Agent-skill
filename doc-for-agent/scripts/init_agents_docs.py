#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Optional

from doc_for_agent_generator import (
    MANUAL_END,
    MANUAL_START,
    SUPPORTED_DOC_PROFILES,
    SUPPORTED_REPO_TYPES,
    analyze_repo,
    generate_docs as generate_docs_from_analysis,
    infer_project_name,
    merge_markdown,
    read_text,
    repo_type_label,
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


def generate_docs(
    root: Path,
    project_name: str,
    repo_type_override: Optional[str] = None,
    profile: str = "bootstrap",
) -> Dict[str, str]:
    # Keep the historical entrypoint shape while delegating to the modular core.
    return generate_docs_from_analysis(
        analyze_repo(root, project_name, repo_type_override=repo_type_override, doc_profile=profile)
    )


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


def print_analysis_explanation(analysis) -> None:
    print(f"Analysis for: {analysis.root}")
    print(f"- Project name: {analysis.project_name}")
    print(f"- Repo type: `{analysis.repo_type}` ({repo_type_label(analysis.repo_type)})")
    print(f"- Doc profile: `{analysis.doc_profile}`")
    print(f"- Confidence: `{analysis.classification.confidence}`")
    print(
        f"- Frontend root: `{analysis.frontend_root}`"
        if analysis.frontend_root
        else "- Frontend root: not detected"
    )
    print(
        f"- Backend root: `{analysis.backend_root}`"
        if analysis.backend_root
        else "- Backend root: not detected"
    )
    print(f"- Package manager: `{analysis.package_manager}`")

    sections = [
        ("Reasons", analysis.classification.reasons),
        ("Secondary traits", analysis.classification.secondary_traits),
        ("Conflicting signals", analysis.classification.conflicting_signals),
        ("Open questions", analysis.classification.open_questions),
        (
            "Signals",
            [
                f"top-level dirs: {', '.join(analysis.signals.top_level_dirs) or '(none)'}",
                f"has skill file: {'yes' if analysis.signals.has_skill_file else 'no'}",
                f"has agent manifests: {'yes' if analysis.signals.has_agent_manifests else 'no'}",
                f"has workspace layout: {'yes' if analysis.signals.has_workspace_layout else 'no'}",
                f"has package.json: {'yes' if analysis.signals.has_package_json else 'no'}",
                f"has Python packaging: {'yes' if analysis.signals.has_python_packaging else 'no'}",
                f"CLI entrypoints: {len(analysis.signals.cli_entrypoints)}",
                f"library entrypoints: {len(analysis.signals.library_entrypoints)}",
            ],
        ),
    ]
    for heading, items in sections:
        print(f"{heading}:")
        if items:
            for item in items:
                print(f"- {item}")
        else:
            print("- none")


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize or refresh an AGENTS documentation directory.")
    parser.add_argument("--root", required=True, help="Repository root where AGENTS/ should be created or refreshed.")
    parser.add_argument("--project-name", help="Optional explicit project name.")
    parser.add_argument("--mode", choices=["init", "refresh"], default="refresh", help="Whether to initialize or refresh AGENTS docs.")
    parser.add_argument("--dry-run", action="store_true", help="Preview AGENTS file changes without writing anything.")
    parser.add_argument(
        "--repo-type",
        choices=SUPPORTED_REPO_TYPES,
        help="Force a repo type when automatic classification is not appropriate.",
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="Print classification signals and reasoning before any write actions.",
    )
    parser.add_argument(
        "--profile",
        choices=SUPPORTED_DOC_PROFILES,
        default="bootstrap",
        help="Select the AGENTS documentation topology to generate.",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    project_name = infer_project_name(root, args.project_name)
    analysis = analyze_repo(
        root,
        project_name,
        repo_type_override=args.repo_type,
        doc_profile=args.profile,
    )
    files = generate_docs_from_analysis(analysis)

    if args.explain:
        print_analysis_explanation(analysis)

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
