#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Optional

from doc_for_agent_generator import (
    EngineRequest,
    MANUAL_END,
    MANUAL_START,
    SUPPORTED_DOC_PROFILES,
    SUPPORTED_ENGINE_ACTIONS,
    SUPPORTED_OUTPUT_MODES,
    SUPPORTED_REPO_TYPES,
    apply_generation_plan,
    analyze_repo,
    build_generation_plan,
    generate_docs as generate_docs_from_analysis,
    merge_markdown,
    plan_dry_run_actions,
    plan_title,
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


def print_analysis_explanation(analysis, output_mode: str) -> None:
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
        f"python3 doc-for-agent/scripts/init_agents_docs.py --root {analysis.root} --mode refresh --profile {suggested_profile} --output-mode {output_mode}"
    )
    print("Suggested source-of-truth files:")
    for line in infer_source_of_truth_lines(analysis)[:6]:
        print(f"- {line}")
    print("Supporting-doc synthesis summary:")
    for role in ("product", "architecture", "execution", "memory"):
        role_insights = analysis.supporting_doc_insights.get(role, {})
        role_sources = analysis.supporting_doc_provenance.get(role, [])
        confirmed_count = len(role_insights.get("confirmed", []))
        conflicting_count = len(role_insights.get("conflicting", []))
        unresolved_count = len(role_insights.get("unresolved", []))
        print(
            f"- {role}: confirmed={confirmed_count}, conflicting={conflicting_count}, unresolved={unresolved_count}, sources={len(role_sources)}"
        )

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
    parser = argparse.ArgumentParser(description="Initialize or refresh documentation outputs for AGENTS and/or docs.")
    parser.add_argument("--root", required=True, help="Repository root where AGENTS/ should be created or refreshed.")
    parser.add_argument("--project-name", help="Optional explicit project name.")
    parser.add_argument(
        "--mode",
        choices=SUPPORTED_ENGINE_ACTIONS,
        default="refresh",
        help="Engine action to execute: init, refresh, migrate, or generate.",
    )
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
    parser.add_argument(
        "--output-mode",
        choices=SUPPORTED_OUTPUT_MODES,
        default="agent",
        help="Choose which documentation system to generate: agent, human, or dual.",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    plan = build_generation_plan(
        EngineRequest(
            root=root,
            mode=args.mode,
            output_mode=args.output_mode,
            profile=args.profile,
            project_name=args.project_name or "",
            repo_type_override=args.repo_type,
        )
    )
    analysis = plan.analysis

    if args.explain:
        print_analysis_explanation(analysis, args.output_mode)

    if args.dry_run:
        print(plan_title(plan, dry_run=True))
        for line in plan_dry_run_actions(plan):
            print(line)
        return

    apply_generation_plan(plan)
    print(plan_title(plan, dry_run=False))


if __name__ == "__main__":
    main()
