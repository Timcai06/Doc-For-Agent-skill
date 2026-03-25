#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path
from typing import Dict, Iterable, Optional

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
from doc_for_agent_generator.builders import infer_source_of_truth_lines

__all__ = [
    "MANUAL_END",
    "MANUAL_START",
    "generate_docs",
    "main",
    "merge_markdown",
    "read_text",
    "write_file",
]


LEGACY_FLAT_TO_LAYERED_TARGETS = {
    "README.md": ("00-entry/AGENTS.md",),
    "product.md": ("01-product/002-prd.md",),
    "architecture.md": ("02-architecture/007-architecture-compatibility.md",),
    "frontend.md": ("02-architecture/005-frontend-guidelines.md",),
    "backend.md": ("02-architecture/006-backend-structure.md",),
    "workflows.md": ("03-execution/008-implementation-plan.md",),
    "glossary.md": ("00-entry/AGENTS.md",),
}


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


def append_legacy_migration_notes(content: str, source_label: str, source_text: str) -> str:
    body = source_text.strip()
    if not body:
        return content
    section = "\n".join(
        [
            "## Migrated Notes",
            "",
            f"- Legacy source: `{source_label}`",
            "",
            MANUAL_START,
            body,
            MANUAL_END,
        ]
    )
    return content.rstrip() + "\n\n" + section + "\n"


def apply_layered_migration_overlays(analysis, files: Dict[str, str]) -> Dict[str, str]:
    if analysis.doc_profile != "layered":
        return files

    migrated = dict(files)
    canonical_root = analysis.docs_inventory.canonical_agents_root or (analysis.root / "AGENTS")
    for path in analysis.docs_inventory.flat_agent_files:
        targets = LEGACY_FLAT_TO_LAYERED_TARGETS.get(path.name, ())
        if not targets:
            continue
        source_text = read_text(path)
        if not source_text.strip():
            continue
        try:
            source_label = str(path.relative_to(canonical_root)).replace("\\", "/")
        except ValueError:
            source_label = path.name
        for target in targets:
            if target not in migrated:
                continue
            migrated[target] = append_legacy_migration_notes(migrated[target], f"AGENTS/{source_label}", source_text)
    return migrated


def archive_legacy_flat_files(analysis) -> None:
    if analysis.doc_profile != "layered":
        return
    canonical_root = analysis.docs_inventory.canonical_agents_root or (analysis.root / "AGENTS")
    archive_root = canonical_root / "_archive" / "flat"
    for path in analysis.docs_inventory.archive_candidates:
        if not path.exists():
            continue
        destination = archive_root / path.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
        path.unlink()


def describe_dry_run(agents_dir: Path, mode: str, files: Dict[str, str], archive_candidates: Iterable[Path]) -> None:
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
    for path in archive_candidates:
        print(f"- archive {path.name} -> AGENTS/_archive/flat/{path.name}")


def print_analysis_explanation(analysis) -> None:
    suggested_profile = (
        "layered"
        if analysis.repo_type in {"web-app", "monorepo"} or (analysis.frontend_root and analysis.backend_root)
        else "bootstrap"
    )
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
    print(f"- Suggested profile: `{suggested_profile}`")
    print(f"- Documentation state: `{analysis.docs_inventory.detected_state}`")
    if analysis.docs_inventory.canonical_agents_root:
        print(f"- Canonical AGENTS root: `{analysis.docs_inventory.canonical_agents_root}`")
    if suggested_profile != analysis.doc_profile:
        print(f"- Note: current run requested profile `{analysis.doc_profile}`.")
    print(
        "Suggested command: "
        f"python3 doc-for-agent/scripts/init_agents_docs.py --root {analysis.root} --mode refresh --profile {suggested_profile}"
    )
    print("Suggested source-of-truth files:")
    for line in infer_source_of_truth_lines(analysis)[:6]:
        print(f"- {line}")

    sections = [
        ("Reasons", analysis.classification.reasons),
        ("Secondary traits", analysis.classification.secondary_traits),
        ("Conflicting signals", analysis.classification.conflicting_signals),
        ("Open questions", analysis.classification.open_questions),
        (
            "Documentation inventory",
            [
                f"detected state: {analysis.docs_inventory.detected_state}",
                f"agent roots: {len(analysis.docs_inventory.agent_roots)}",
                f"flat agent files: {len(analysis.docs_inventory.flat_agent_files)}",
                f"layered agent files: {len(analysis.docs_inventory.layered_agent_files)}",
                f"supporting docs: {len(analysis.docs_inventory.supporting_docs)}",
                f"archive candidates: {len(analysis.docs_inventory.archive_candidates)}",
            ],
        ),
        (
            "Signals",
            [
                f"top-level dirs: {', '.join(analysis.signals.top_level_dirs) or '(none)'}",
                f"has skill file: {'yes' if analysis.signals.has_skill_file else 'no'}",
                f"has agent manifests: {'yes' if analysis.signals.has_agent_manifests else 'no'}",
                f"has workspace layout: {'yes' if analysis.signals.has_workspace_layout else 'no'}",
                f"has package.json: {'yes' if analysis.signals.has_package_json else 'no'}",
                f"has package bin metadata: {'yes' if analysis.signals.has_package_bin else 'no'}",
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
    if analysis.docs_inventory.reference_only_docs:
        print("Reference-only docs:")
        for path in analysis.docs_inventory.reference_only_docs[:6]:
            print(f"- {path}")


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
    files = apply_layered_migration_overlays(analysis, generate_docs_from_analysis(analysis))

    if args.explain:
        print_analysis_explanation(analysis)

    if args.dry_run:
        agents_dir = analysis.docs_inventory.canonical_agents_root or (root / "AGENTS")
        describe_dry_run(agents_dir, args.mode, files, analysis.docs_inventory.archive_candidates)
        return

    agents_dir = analysis.docs_inventory.canonical_agents_root or (root / "AGENTS")
    agents_dir.mkdir(parents=True, exist_ok=True)
    archive_legacy_flat_files(analysis)

    for name, content in files.items():
        path = agents_dir / name
        write_file(path, resolve_output_content(path, content, args.mode))

    print(f"{args.mode.capitalize()}ed AGENTS docs in: {agents_dir}")


if __name__ == "__main__":
    main()
