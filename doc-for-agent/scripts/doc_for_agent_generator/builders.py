from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Sequence

from .analysis import supporting_doc_roles
from .models import RepoAnalysis
from .utils import find_files, load_json, rel_path

SUPPORTED_DOC_PROFILES = ("bootstrap", "layered")
SUPPORTED_OUTPUT_MODES = ("agent", "human", "dual")


def format_bullets(items: Sequence[str], empty_line: str) -> str:
    if not items:
        return f"- {empty_line}"
    return "\n".join(f"- {item}" for item in items)


def format_path_bullets(paths: Sequence[Path], root: Path, empty_line: str) -> str:
    if not paths:
        return f"- {empty_line}"
    return "\n".join(f"- `{rel_path(path, root)}`" for path in paths)


def supporting_doc_lines(paths: Sequence[Path], root: Path) -> list[str]:
    return [f"`{rel_path(path, root)}`" for path in paths]


def supporting_doc_insight_lines(analysis: RepoAnalysis, role: str, kind: str) -> list[str]:
    role_insights = analysis.supporting_doc_insights.get(role, {})
    values = role_insights.get(kind, [])
    return [value for value in values if value]


def supporting_doc_provenance_lines(analysis: RepoAnalysis, role: str) -> list[str]:
    return [f"`{path}`" for path in analysis.supporting_doc_provenance.get(role, [])]


def synthesis_summary_lines(analysis: RepoAnalysis, role: str) -> list[str]:
    role_insights = analysis.supporting_doc_insights.get(role, {})
    role_sources = analysis.supporting_doc_provenance.get(role, [])
    confirmed_count = len(role_insights.get("confirmed", []))
    conflicting_count = len(role_insights.get("conflicting", []))
    unresolved_count = len(role_insights.get("unresolved", []))
    lines = [
        f"Sources analyzed: `{len(role_sources)}`",
        f"Synthesized statements: `{confirmed_count}` confirmed, `{conflicting_count}` conflicting, `{unresolved_count}` unresolved",
    ]
    if not role_sources:
        lines.append("No supporting docs matched this role; content below is derived from repository structure and code signals.")
    return lines


def human_audience_lines(analysis: RepoAnalysis) -> list[str]:
    lines = [
        "Repository maintainers responsible for day-to-day delivery and operational stability.",
    ]
    if analysis.repo_type == "web-app":
        lines.append("Cross-functional engineers coordinating frontend and backend changes.")
    elif analysis.repo_type == "backend-service":
        lines.append("Backend operators and API maintainers responsible for service behavior.")
    elif analysis.repo_type == "cli-tool":
        lines.append("CLI maintainers preserving command UX and script compatibility.")
    elif analysis.repo_type == "library-sdk":
        lines.append("SDK maintainers preserving public API behavior for downstream consumers.")
    elif analysis.repo_type == "skill-meta":
        lines.append("Skill maintainers keeping manifests, prompts, and generator behavior aligned.")
    return lines


def human_inferred_lines(analysis: RepoAnalysis, role: str) -> list[str]:
    lines: list[str] = []
    if role == "product":
        if analysis.summary:
            lines.append(f"Project intent from README/code signals: {analysis.summary}")
        if analysis.classification.reasons:
            lines.append(f"Repo type signal: `{repo_type_label(analysis.repo_type)}` ({analysis.classification.reasons[0]})")
        if analysis.routes:
            lines.append(f"User-facing flow includes routes such as {', '.join(f'`{route}`' for route in analysis.routes[:3])}.")
        if analysis.endpoints:
            lines.append(f"Service-facing flow includes endpoints such as {', '.join(f'`{endpoint}`' for endpoint in analysis.endpoints[:3])}.")
    elif role == "architecture":
        if analysis.frontend_root and analysis.backend_root:
            lines.append("Architecture is split between a frontend surface and a backend/runtime surface.")
        elif analysis.frontend_root:
            lines.append("Architecture is frontend-led with runtime behavior anchored in package scripts and routes.")
        elif analysis.backend_root:
            lines.append("Architecture is backend-led with runtime behavior anchored in service files and endpoints.")
        if analysis.routes:
            lines.append(f"Routing structure suggests primary interface paths under {', '.join(f'`{route}`' for route in analysis.routes[:3])}.")
        if analysis.endpoints:
            lines.append(f"Endpoint decorators suggest service contract anchors at {', '.join(f'`{endpoint}`' for endpoint in analysis.endpoints[:3])}.")
    elif role == "execution":
        package_manager_label = analysis.package_manager or "npm"
        lines.append(f"Primary command workflow centers on `{package_manager_label}` package scripts and repository-local verify commands.")
        if analysis.frontend_scripts:
            lines.append(
                f"Frontend workflows depend on scripts: {', '.join(f'`{name}`' for name in list(analysis.frontend_scripts.keys())[:4])}."
            )
        if analysis.backend_root and (analysis.backend_root / "requirements.txt").exists():
            lines.append("Backend setup requires Python dependency installation from `requirements.txt`.")
    elif role == "memory":
        if analysis.glossary_entries:
            lines.append("Canonical terminology can be seeded from detected glossary entries and then curated by maintainers.")
        if analysis.routes:
            lines.append("Route names are useful term candidates for product and operations vocabulary alignment.")
        if analysis.endpoints:
            lines.append("Endpoint labels are useful term candidates for integration and runbook language.")
    return lines


def human_maintenance_lines(analysis: RepoAnalysis, role: str, unresolved_count: int, conflicting_count: int) -> list[str]:
    lines: list[str] = [
        "Assign one maintainer owner for this document and update it in the same pull request as behavior changes.",
        "Review this document at least once per sprint or before each release cut.",
    ]
    if role == "product":
        lines.append("Update after roadmap, target user, or feature scope decisions.")
    elif role == "architecture":
        lines.append("Update after boundary, dependency, or interface contract changes.")
    elif role == "execution":
        lines.append("Update after setup/run/verify command changes or CI workflow updates.")
    elif role == "memory":
        lines.append("Update when terminology, handoff language, or project status vocabulary changes.")

    if conflicting_count:
        lines.append("Prioritize resolving conflicting statements before treating this document as canonical.")
    if unresolved_count:
        lines.append("Track unresolved items as named decisions with owner and due date.")
    if unresolved_count == 0 and conflicting_count == 0:
        lines.append("No major synthesis conflicts were detected; focus on keeping this page current with implementation changes.")
    return lines


def human_bootstrap_backlog_lines(role: str, has_supporting_provenance: bool) -> list[str]:
    if has_supporting_provenance:
        return ["Supporting docs were found; continue consolidating them into this page and archive stale duplicates."]

    if role == "product":
        return [
            "Write a one-paragraph project mission and a one-release priority list.",
            "Record primary users and success signals in concrete terms.",
            "Capture top open product decisions with owner + target date.",
        ]
    if role == "architecture":
        return [
            "Document top-level system boundaries (frontend/backend/services) in 5-8 bullets.",
            "List canonical files that define runtime behavior and public contracts.",
            "Create an initial decision backlog for unresolved architecture tradeoffs.",
        ]
    if role == "execution":
        return [
            "Verify setup/run/verify commands from a clean environment and keep only working commands.",
            "Define a minimum release checklist shared by maintainers.",
            "Record failure recovery steps for the most common local/CI breakages.",
        ]
    return [
        "Promote repeated domain terms into canonical glossary entries.",
        "Note deprecated or ambiguous terms and map them to preferred wording.",
        "Review docs for vocabulary drift each sprint.",
    ]


def human_update_trigger_lines(analysis: RepoAnalysis, role: str) -> list[str]:
    lines: list[str] = []
    if role == "product":
        lines.append("When new user-facing routes, commands, or APIs are added, update scope and audience notes.")
        lines.append("When priorities change in release planning, update the project overview and open decision list.")
    elif role == "architecture":
        lines.append("When source-of-truth files, service boundaries, or runtime dependencies change, update this page.")
        lines.append("When integration contracts change (routes/endpoints/storage), refresh architecture notes in the same PR.")
    elif role == "execution":
        lines.append("When setup/run/verify commands change, update this runbook immediately.")
        lines.append("When CI checks or release gates change, sync the Verify and Operational Notes sections.")
    elif role == "memory":
        lines.append("When teams introduce new domain terms, add canonical definitions and preferred wording.")
        lines.append("When old terms are deprecated, keep migration aliases until docs and code are fully aligned.")

    if not analysis.supporting_doc_provenance.get(role):
        lines.append("No supporting docs were found for this role; prioritize adding one maintainer-verified baseline note.")
    return lines


def normalize_evidence_line(line: str) -> str:
    without_sources = re.sub(r"\s*\(sources:\s*.*\)$", "", line).strip().lower()
    return re.sub(r"[^a-z0-9]+", " ", without_sources).strip()


def compact_human_evidence(
    confirmed: Sequence[str],
    inferred: Sequence[str],
    unresolved: Sequence[str],
    conflicting: Sequence[str],
) -> tuple[list[str], list[str], list[str], list[str]]:
    confirmed_out: list[str] = []
    inferred_out: list[str] = []
    unresolved_out: list[str] = []
    conflicting_out: list[str] = []
    seen: set[str] = set()

    for line in confirmed:
        key = normalize_evidence_line(line)
        if key and key not in seen:
            confirmed_out.append(line)
            seen.add(key)

    for line in inferred:
        key = normalize_evidence_line(line)
        if key and key not in seen:
            inferred_out.append(line)
            seen.add(key)

    for line in unresolved:
        key = normalize_evidence_line(line)
        if key and key not in seen:
            unresolved_out.append(line)
            seen.add(key)

    for line in conflicting:
        key = normalize_evidence_line(line)
        if key and key not in seen:
            conflicting_out.append(line)
            seen.add(key)

    return confirmed_out, inferred_out, unresolved_out, conflicting_out


def repo_type_label(repo_type: str) -> str:
    labels = {
        "skill-meta": "skill/meta repository",
        "cli-tool": "CLI/tool repository",
        "library-sdk": "library/SDK repository",
        "backend-service": "backend service repository",
        "web-app": "web application repository",
        "monorepo": "monorepo",
        "unknown": "repository type not confidently classified",
    }
    return labels.get(repo_type, repo_type)


def current_operating_posture(analysis: RepoAnalysis) -> str:
    postures = {
        "skill-meta": "Keep the skill definition, generator behavior, and generated documentation in sync.",
        "web-app": "Keep product surface, frontend flow, and backend contract aligned while the repository evolves.",
        "backend-service": "Preserve runtime contract stability while tightening service behavior and verification.",
        "cli-tool": "Preserve command UX and script behavior while clarifying install and verification paths.",
        "library-sdk": "Preserve public API surface and usage examples while improving implementation internals.",
        "monorepo": "Keep boundaries between packages/apps explicit before making cross-cutting edits.",
    }
    return postures.get(
        analysis.repo_type,
        "Confirm current project phase and the next safe scope of work before making broad edits.",
    )


def extend_unique(target: list[str], items: Sequence[str]) -> None:
    for item in items:
        if item not in target:
            target.append(item)


def detect_unittest_commands(root: Path) -> list[str]:
    commands: list[str] = []
    unit_dirs = []
    for pattern in ("tests/unit", "*/tests/unit", "*/*/tests/unit"):
        unit_dirs.extend(sorted(path for path in root.glob(pattern) if path.is_dir()))

    seen = set()
    for unit_dir in unit_dirs:
        normalized = str(unit_dir.resolve())
        if normalized in seen:
            continue
        seen.add(normalized)
        commands.append(
            f"python3 -m unittest discover -s {rel_path(unit_dir, root)} -p 'test_*.py'"
        )
    return commands


def detect_verify_script_commands(root: Path) -> list[str]:
    scripts = find_files(
        root,
        [
            "tests/verify*.py",
            "*/tests/verify*.py",
            "*/*/tests/verify*.py",
            "scripts/verify*.py",
            "*/scripts/verify*.py",
        ],
        limit=8,
    )
    return [f"python3 {rel_path(path, root)}" for path in scripts]


def detect_generator_script(root: Path) -> Path | None:
    matches = find_files(
        root,
        [
            "scripts/init_agents_docs.py",
            "*/scripts/init_agents_docs.py",
        ],
        limit=1,
    )
    return matches[0] if matches else None


def detect_workspace_config_paths(root: Path) -> list[Path]:
    names = ("pnpm-workspace.yaml", "turbo.json", "nx.json", "lerna.json")
    return [root / name for name in names if (root / name).exists()]


def detect_package_metadata_paths(root: Path) -> list[Path]:
    names = ("package.json", "pyproject.toml", "setup.py", "requirements.txt", "requirements-dev.txt")
    return [root / name for name in names if (root / name).exists()]


def supporting_docs_for_role(analysis: RepoAnalysis, role: str) -> list[Path]:
    role_paths: list[Path] = []
    for path in analysis.docs_inventory.reference_only_docs:
        if role in supporting_doc_roles(path, analysis.root):
            role_paths.append(path)
    return role_paths


def infer_source_of_truth_lines(analysis: RepoAnalysis) -> list[str]:
    lines: list[str] = []
    readme_path = analysis.root / "README.md"
    if readme_path.exists():
        lines.append("`README.md` for stated project goals, setup expectations, and user-facing examples")

    if analysis.repo_type == "skill-meta":
        if analysis.skill_meta.skill_file:
            lines.append(f"`{rel_path(analysis.skill_meta.skill_file, analysis.root)}` for trigger conditions and maintainer workflow")
        if analysis.skill_meta.agent_manifests:
            lines.append(
                f"`{rel_path(analysis.skill_meta.agent_manifests[0], analysis.root)}` for launcher/marketplace invocation metadata"
            )
        script_root = analysis.root / "doc-for-agent/scripts"
        if script_root.exists():
            lines.append("`doc-for-agent/scripts/` for generation behavior and repository scanning")
        reference_root = analysis.root / "doc-for-agent/references"
        if reference_root.exists():
            lines.append("`doc-for-agent/references/` for documentation structure and writing constraints")
    elif analysis.repo_type == "monorepo":
        for path in detect_workspace_config_paths(analysis.root):
            lines.append(f"`{rel_path(path, analysis.root)}` for workspace/package boundaries")
        if analysis.frontend_root:
            lines.append(f"`{rel_path(analysis.frontend_root, analysis.root)}` for frontend behavior and scripts")
        if analysis.backend_root:
            lines.append(f"`{rel_path(analysis.backend_root, analysis.root)}` for service/runtime behavior")
        root_package = analysis.root / "package.json"
        if root_package.exists():
            lines.append("`package.json` for root-level scripts and workspace orchestration")
    elif analysis.repo_type == "web-app":
        if analysis.frontend_root:
            lines.append(f"`{rel_path(analysis.frontend_root, analysis.root)}` for client routes, components, and UI scripts")
        if analysis.backend_root:
            lines.append(f"`{rel_path(analysis.backend_root, analysis.root)}` for API endpoints and runtime behavior")
        extend_unique(lines, [f"`{rel_path(path, analysis.root)}` for package/runtime metadata" for path in detect_package_metadata_paths(analysis.root)])
    elif analysis.repo_type == "backend-service":
        if analysis.backend_root:
            lines.append(f"`{rel_path(analysis.backend_root, analysis.root)}` for service logic and runtime wiring")
            extend_unique(
                lines,
                [
                    f"`{rel_path(path, analysis.root)}` for backend dependency/runtime configuration"
                    for path in detect_package_metadata_paths(analysis.backend_root)
                ],
            )
        if analysis.endpoints:
            lines.append("Backend route decorators are canonical for endpoint contract discovery")
    elif analysis.repo_type == "cli-tool":
        if analysis.cli_entrypoints:
            lines.append(f"`{rel_path(analysis.cli_entrypoints[0], analysis.root)}` as the primary command entrypoint")
        if analysis.script_files:
            lines.append("`scripts/` for operational helper commands and smoke checks")
        extend_unique(lines, [f"`{rel_path(path, analysis.root)}` for installation/distribution metadata" for path in detect_package_metadata_paths(analysis.root)])
    elif analysis.repo_type == "library-sdk":
        if analysis.library_entrypoints:
            lines.append(f"`{rel_path(analysis.library_entrypoints[0], analysis.root)}` as a likely public API entrypoint")
        extend_unique(lines, [f"`{rel_path(path, analysis.root)}` for package/runtime metadata" for path in detect_package_metadata_paths(analysis.root)])

    if not lines:
        if analysis.frontend_root:
            lines.append(f"`{rel_path(analysis.frontend_root, analysis.root)}` for frontend behavior and scripts")
        if analysis.backend_root:
            lines.append(f"`{rel_path(analysis.backend_root, analysis.root)}` for backend/runtime behavior")
    if not lines:
        lines.append("Needs human confirmation: identify the files agents should treat as canonical entrypoints")

    return lines


def detect_root_package_scripts(root: Path) -> Dict[str, str]:
    package_json = root / "package.json"
    if not package_json.exists():
        return {}
    package = load_json(package_json)
    scripts = package.get("scripts") or {}
    return {
        str(key): str(value)
        for key, value in scripts.items()
        if isinstance(key, str) and isinstance(value, str)
    }


def append_package_script_commands(lines: list[str], package_manager: str, scripts: Dict[str, str], keys: Sequence[str]) -> None:
    for key in keys:
        if key not in scripts:
            continue
        if package_manager == "yarn":
            command = f"yarn {key}"
        else:
            command = f"{package_manager} run {key}"
        if command not in lines:
            lines.append(command)


def product_entry_point_lines(analysis: RepoAnalysis) -> list[str]:
    if analysis.repo_type == "web-app" and analysis.routes:
        return [f"`{route}`" for route in analysis.routes[:8]]
    if analysis.repo_type == "backend-service" and analysis.endpoints:
        return [f"`{endpoint}`" for endpoint in analysis.endpoints[:8]]
    if analysis.repo_type == "cli-tool" and analysis.cli_entrypoints:
        return [f"`{rel_path(path, analysis.root)}`" for path in analysis.cli_entrypoints[:8]]
    if analysis.repo_type == "library-sdk" and analysis.library_entrypoints:
        return [f"`{rel_path(path, analysis.root)}`" for path in analysis.library_entrypoints[:8]]
    if analysis.repo_type == "skill-meta":
        lines: list[str] = []
        if analysis.skill_meta.skill_file:
            lines.append(f"`{rel_path(analysis.skill_meta.skill_file, analysis.root)}`")
        lines.extend(f"`{rel_path(path, analysis.root)}`" for path in analysis.skill_meta.agent_manifests[:6])
        if lines:
            return lines
    if analysis.routes:
        return [f"`{route}`" for route in analysis.routes[:8]]
    return []


def build_readme(analysis: RepoAnalysis) -> str:
    return f"""# AGENTS

## Best Used For

- Fast onboarding when a new coding agent enters this repository
- Multi-agent work where terminology, workflow, and ownership boundaries need to stay aligned
- Refreshing repo-specific context after the codebase structure changes

## Repository Classification

- Detected repo type: `{repo_type_label(analysis.repo_type)}`

## Files

- `product.md`: why this repository exists and what agents should preserve
- `architecture.md`: repository shape, source-of-truth files, and handoff boundaries
- `frontend.md`: UI/client context for frontend-facing repos, or agent-facing interface notes otherwise
- `backend.md`: service/runtime contract notes or implementation/runtime entrypoints
- `workflows.md`: setup, execution, verification, and refresh commands
- `glossary.md`: canonical names, labels, and terminology that should stay stable
"""


def build_product(analysis: RepoAnalysis) -> str:
    route_lines = format_bullets(
        product_entry_point_lines(analysis),
        "No user-facing routes or invocation entrypoints were detected automatically.",
    )
    facts = []
    if analysis.summary:
        facts.append(analysis.summary)
    if analysis.repo_type == "skill-meta":
        if analysis.skill_meta.skill_name:
            facts.append(f"Skill name declared in metadata: `{analysis.skill_meta.skill_name}`.")
        if analysis.skill_meta.skill_file:
            facts.append(f"Primary skill definition file: `{analysis.skill_meta.skill_file.name}`.")
        facts.append(
            "This repository ships reusable instructions and scripts for coding agents rather than a standalone product app."
        )

    inferences = [
        f"This repository is best understood as a `{repo_type_label(analysis.repo_type)}`.",
    ]
    if analysis.repo_type == "skill-meta":
        inferences.append(
            "Primary users are maintainers installing or evolving the skill, plus agents that consume the generated guidance."
        )
    elif analysis.repo_type in {"library-sdk", "cli-tool"}:
        inferences.append("Primary users are developers integrating or running the packaged tooling.")

    open_questions = [
        "Confirm the primary audience and the exact outcome they expect from this repository.",
        "Confirm the core success criteria agents should optimize for before making broad edits.",
    ]

    return f"""# Product

## Best Used For

- Planning work in this repository before editing code or docs
- Aligning multiple agents on what this repo is trying to preserve
- Checking whether a proposed change still matches the repository's purpose

## Confirmed Facts

{format_bullets(facts, "Needs human confirmation: add a concise repository summary from the README or maintainers.")}

## Inferences For Agents

{format_bullets(inferences, "Repository purpose could not be inferred confidently.")}

## Current Entry Points

{route_lines}

## Open Questions

{format_bullets(open_questions, "No open questions recorded.")}
"""


def build_architecture(analysis: RepoAnalysis) -> str:
    facts = [
        f"Repository root: `{analysis.root}`.",
        f"Detected repo type: `{analysis.repo_type}`.",
        f"Classification confidence: `{analysis.classification.confidence}`.",
    ]
    if analysis.frontend_root:
        facts.append(f"Frontend root: `{rel_path(analysis.frontend_root, analysis.root)}`.")
    if analysis.backend_root:
        facts.append(f"Backend root: `{rel_path(analysis.backend_root, analysis.root)}`.")

    if analysis.repo_type == "skill-meta":
        if analysis.skill_meta.skill_file:
            facts.append(f"Skill definition entrypoint: `{rel_path(analysis.skill_meta.skill_file, analysis.root)}`.")
        if analysis.skill_meta.agent_manifests:
            facts.append("Agent manifest files are present for marketplace or launcher integration.")

    source_of_truth = infer_source_of_truth_lines(analysis)

    handoff = []
    if analysis.repo_type == "skill-meta":
        handoff.extend(
            [
                "Prompt/instruction changes should stay aligned with generator behavior so agents are not told to do something the script cannot support.",
                "Generated `AGENTS/` docs are downstream artifacts; review the generator and references before hand-editing broad structure.",
            ]
        )
    else:
        handoff.extend(
            [
                "Prefer changing source code and config first, then refresh `AGENTS/` docs so agent context stays synchronized.",
                "When repo shape is ambiguous, inspect the README and build scripts before assuming ownership boundaries.",
            ]
        )

    return f"""# Architecture

## Best Used For

- Building a quick mental model of repository boundaries before editing
- Deciding which files are canonical versus generated
- Handing work between agents without losing context

## Confirmed Facts

{format_bullets(facts, "Needs human confirmation: repository boundaries were not inferred cleanly.")}

## Repo-Type Signals

{format_bullets(list(analysis.repo_type_reasons), "No strong classification signals were detected automatically.")}

## Secondary Traits

{format_bullets(list(analysis.classification.secondary_traits), "No secondary traits were detected automatically.")}

## Conflicting Signals

{format_bullets(list(analysis.classification.conflicting_signals), "No major conflicting signals were detected automatically.")}

## Source Of Truth For Agents

{format_bullets(source_of_truth, "Needs human confirmation: identify canonical files and directories.")}

## Handoff Boundaries

{format_bullets(handoff, "Needs human confirmation: add handoff and ownership notes.")}

## Open Questions

{format_bullets(list(analysis.repo_type_questions), "No open architecture questions recorded.")}
"""


def build_frontend(analysis: RepoAnalysis) -> str:
    best_used_for = [
        "UI-facing changes, route discovery, and component-level edits"
        if analysis.repo_type == "web-app"
        else "Agent-facing interface context and user entrypoint discovery",
        "Checking which screens, prompts, or interaction surfaces must stay consistent",
    ]

    facts = []
    inferences = []
    route_heading = "Routes Or Interaction Entry Points"
    component_heading = "Key Components Or Interface Files"
    manifest_heading = "Agent Manifests / Prompt Surfaces"
    route_lines = format_bullets(
        [f"`{route}`" for route in analysis.routes],
        "No browser routes were detected automatically.",
    )
    component_lines = format_bullets(
        [f"`{component}`" for component in analysis.components],
        "No component inventory was detected automatically.",
    )
    manifest_lines = format_path_bullets(
        analysis.skill_meta.agent_manifests,
        analysis.root,
        "No agent manifest files were detected automatically.",
    )

    if analysis.repo_type == "web-app":
        facts.append(f"Detected frontend stack: {analysis.frontend_stack}.")
        if analysis.routes:
            facts.append("User-facing routes were detected from app/page structure.")
        if analysis.components:
            facts.append("Top-level components were detected from common component directories.")
    elif analysis.repo_type == "skill-meta":
        if analysis.skill_meta.agent_manifests:
            facts.append("Agent-facing interface manifests are present.")
        facts.append("Primary user interaction happens through an AI assistant invoking this skill rather than a browser UI.")
        inferences.append("The closest thing to a frontend here is the installation and invocation surface exposed through skill manifests and prompts.")
    elif analysis.repo_type == "cli-tool":
        best_used_for = [
            "Understanding command entrypoints, command UX, and user-triggered scripts",
            "Checking which command names, flags, or help text must remain stable",
        ]
        route_heading = "CLI Entry Points"
        component_heading = "User-Facing Command Files"
        manifest_heading = "Install / Invocation Surfaces"
        facts.append("Primary user interaction happens through the command line rather than a browser UI.")
        if analysis.cli_entrypoints:
            facts.append("CLI entrypoint files were detected.")
        route_lines = format_path_bullets(
            analysis.cli_entrypoints,
            analysis.root,
            "No CLI entrypoints were detected automatically.",
        )
        component_lines = format_bullets([], "No additional user-facing command files were detected automatically.")
        manifest_lines = format_bullets(
            [
                "Check package metadata, README examples, and shell scripts before renaming commands or changing default behavior."
            ],
            "No install or invocation surfaces were detected automatically.",
        )
        inferences.append("For CLI repositories, the most frontend-like surface is the command syntax, help output, and install story.")
    elif analysis.repo_type == "library-sdk":
        best_used_for = [
            "Understanding public entrypoints and integration-facing surface area",
            "Checking which exported modules or examples downstream users depend on",
        ]
        route_heading = "Public Entry Points"
        component_heading = "Export Surface Files"
        manifest_heading = "Integration Surfaces"
        facts.append("Primary user interaction is likely through imports, exported helpers, or integration examples rather than an interactive UI.")
        if analysis.library_entrypoints:
            facts.append("Library entrypoint files were detected.")
        route_lines = format_path_bullets(
            analysis.library_entrypoints,
            analysis.root,
            "No public entrypoints were detected automatically.",
        )
        component_lines = format_path_bullets(
            analysis.library_entrypoints[:4],
            analysis.root,
            "No export surface files were detected automatically.",
        )
        manifest_lines = format_bullets(
            [
                "Check README usage snippets and package exports before changing names or module layout."
            ],
            "No integration surfaces were detected automatically.",
        )
        inferences.append("For library repositories, the user-facing surface is the exported API and import paths, not a browser or CLI shell.")
    else:
        facts.append(analysis.frontend_stack)

    open_questions = [
        "Confirm the primary interaction surface agents should preserve: browser UI, CLI UX, or skill prompt surface.",
        "Confirm any labels, command names, or invocation phrases that must remain stable for users.",
    ]

    return f"""# Frontend

## Best Used For

{format_bullets(best_used_for, "Needs human confirmation: define when agents should read this file.")}

## Confirmed Facts

{format_bullets(facts, "Needs human confirmation: no frontend or interaction-surface facts were detected.")}

## Inferences For Agents

{format_bullets(inferences, "No additional frontend inferences recorded.")}

## {route_heading}

{route_lines}

## {component_heading}

{component_lines}

## {manifest_heading}

{manifest_lines}

## Open Questions

{format_bullets(open_questions, "No open frontend questions recorded.")}
"""


def build_backend(analysis: RepoAnalysis) -> str:
    facts = []
    inferences = []
    runtime_heading = "Runtime Entry Points"
    endpoint_heading = "Main Services / Endpoints"
    contract_heading = "Stable Contract Fields"
    storage_heading = "Storage / Output Rules"
    runtime_files = format_path_bullets(
        analysis.skill_meta.scripts,
        analysis.root,
        "No runtime script files were detected automatically.",
    )
    endpoint_lines = format_bullets(
        [f"`{endpoint}`" for endpoint in analysis.endpoints],
        "No API endpoints were detected automatically.",
    )
    storage_lines = format_bullets(
        list(analysis.storage_rules),
        "No storage or persistence rules were detected automatically.",
    )
    contract_lines = format_bullets(
        list(analysis.contract_fields),
        "No stable result-contract fields were detected automatically.",
    )

    if analysis.repo_type in {"backend-service", "web-app"}:
        facts.append(f"Detected backend/runtime stack: {analysis.backend_stack}.")
        if analysis.endpoints:
            facts.append("HTTP endpoints were detected from router decorators.")
        if analysis.storage_rules:
            facts.append("Storage-related behavior was inferred from backend source files.")
    elif analysis.repo_type == "skill-meta":
        if analysis.skill_meta.scripts:
            facts.append("Generation or support scripts are present and act as the runtime behavior of this skill.")
        inferences.append("The most important backend-like surface is the generator script and any install/runtime commands that mutate repository docs.")
    elif analysis.repo_type == "cli-tool":
        runtime_heading = "Execution Entry Points"
        endpoint_heading = "Automation / Script Hooks"
        contract_heading = "Stable CLI Contracts"
        storage_heading = "Outputs / Side Effects"
        facts.append("Operational behavior is driven by CLI entrypoints and helper scripts rather than a networked service.")
        if analysis.cli_entrypoints:
            facts.append("CLI execution entrypoints were detected.")
        runtime_files = format_path_bullets(
            analysis.cli_entrypoints,
            analysis.root,
            "No CLI execution entrypoints were detected automatically.",
        )
        endpoint_lines = format_path_bullets(
            analysis.skill_meta.scripts,
            analysis.root,
            "No automation or helper scripts were detected automatically.",
        )
        contract_lines = format_bullets(
            [
                "Command names, positional arguments, and exit behavior should be treated as downstream-facing contracts."
            ],
            "No stable CLI contracts were detected automatically.",
        )
        storage_lines = format_bullets(
            [
                "Review shell scripts and README examples before changing output paths, environment variable names, or logging behavior."
            ],
            "No CLI side effects were detected automatically.",
        )
        inferences.append("For CLI repositories, backward compatibility often lives in command syntax and shell-facing behavior.")
    elif analysis.repo_type == "library-sdk":
        runtime_heading = "Implementation Entry Points"
        endpoint_heading = "Public Modules"
        contract_heading = "Stable API Contracts"
        storage_heading = "Side Effects / Persistence"
        facts.append("Operational behavior is likely exposed through imported modules and exported functions rather than a long-running service.")
        if analysis.library_entrypoints:
            facts.append("Library implementation entrypoints were detected.")
        runtime_files = format_path_bullets(
            analysis.library_entrypoints,
            analysis.root,
            "No implementation entrypoints were detected automatically.",
        )
        endpoint_lines = format_path_bullets(
            analysis.library_entrypoints[:6],
            analysis.root,
            "No public modules were detected automatically.",
        )
        contract_lines = format_bullets(
            [
                "Export names, import paths, and returned object shapes are likely downstream-facing contracts."
            ],
            "No stable API contracts were detected automatically.",
        )
        storage_lines = format_bullets(
            [
                "Confirm whether modules perform file I/O, network access, or config discovery before changing behavior."
            ],
            "No side effects or persistence rules were detected automatically.",
        )
        inferences.append("For library repositories, the safest unit of change is often the public API surface rather than internal implementation details.")
    else:
        facts.append(analysis.backend_stack)

    open_questions = [
        "Confirm which runtime entrypoints agents should read before changing behavior.",
        "Confirm whether there are outputs or contracts that downstream tools depend on and must not drift.",
    ]

    return f"""# Backend

## Best Used For

- Runtime, script, and service behavior changes
- Checking stable contracts before changing generated outputs
- Verifying where operational logic actually lives

## Confirmed Facts

{format_bullets(facts, "Needs human confirmation: no backend/runtime facts were detected.")}

## Inferences For Agents

{format_bullets(inferences, "No additional backend inferences recorded.")}

## {runtime_heading}

{runtime_files}

## {endpoint_heading}

{endpoint_lines}

## {contract_heading}

{contract_lines}

## {storage_heading}

{storage_lines}

## Open Questions

{format_bullets(open_questions, "No open backend questions recorded.")}
"""


def build_workflows(analysis: RepoAnalysis) -> str:
    setup_lines = []
    run_lines = []
    verify_lines = []
    refresh_lines = []
    root_package_scripts = detect_root_package_scripts(analysis.root)

    if analysis.frontend_root:
        frontend_prefix = (
            f"cd {rel_path(analysis.frontend_root, analysis.root)}"
            if analysis.frontend_root != analysis.root
            else "# already at repo root"
        )
        install_cmd = {
            "npm": "npm install",
            "pnpm": "pnpm install",
            "yarn": "yarn install",
        }.get(analysis.package_manager, "npm install")
        setup_lines.extend([frontend_prefix, install_cmd])
        if "dev" in analysis.frontend_scripts:
            run_lines.extend(
                [
                    frontend_prefix,
                    f"{analysis.package_manager} run dev"
                    if analysis.package_manager != "yarn"
                    else "yarn dev",
                ]
            )
        for key in ("lint", "test", "build"):
            if key in analysis.frontend_scripts:
                verify_lines.extend(
                    [
                        frontend_prefix,
                        f"{analysis.package_manager} run {key}"
                        if analysis.package_manager != "yarn"
                        else f"yarn {key}",
                    ]
                )
    elif root_package_scripts:
        install_cmd = {
            "npm": "npm install",
            "pnpm": "pnpm install",
            "yarn": "yarn install",
        }.get(analysis.package_manager, "npm install")
        setup_lines.append(install_cmd)
        append_package_script_commands(run_lines, analysis.package_manager, root_package_scripts, ("dev", "start"))
        append_package_script_commands(
            verify_lines,
            analysis.package_manager,
            root_package_scripts,
            ("lint", "test", "build", "typecheck", "check"),
        )

    if analysis.backend_root:
        backend_prefix = (
            f"cd {rel_path(analysis.backend_root, analysis.root)}"
            if analysis.backend_root != analysis.root
            else "# backend at repo root"
        )
        if (analysis.backend_root / "requirements-dev.txt").exists():
            setup_lines.extend([backend_prefix, "python3 -m pip install -r requirements-dev.txt"])
        elif (analysis.backend_root / "requirements.txt").exists():
            setup_lines.extend([backend_prefix, "python3 -m pip install -r requirements.txt"])
        if (analysis.backend_root / "app").exists():
            run_lines.extend([backend_prefix, "uvicorn app.main:app --reload"])

    if analysis.repo_type == "skill-meta":
        setup_lines.append("# skill repositories are usually installed by symlink or copied into a local skills directory")
        skill_script = detect_generator_script(analysis.root)
        if skill_script:
            skill_script_rel = rel_path(skill_script, analysis.root)
            run_lines.append(f"python3 {skill_script_rel} --root /path/to/target-repo --mode refresh")
            refresh_lines.append(f"python3 {skill_script_rel} --root {analysis.root} --mode refresh")
        refresh_lines.append(
            "Review generated `AGENTS/*.md` files and tighten any sections still marked as needing human confirmation."
        )

    if analysis.script_files:
        extend_unique(run_lines, [f"./{script}" for script in analysis.script_files[:6]])

    extend_unique(verify_lines, detect_unittest_commands(analysis.root))
    extend_unique(verify_lines, detect_verify_script_commands(analysis.root))

    if not setup_lines:
        setup_lines = ["Review README setup steps and install dependencies with the repository's package manager."]
    if not run_lines:
        run_lines = ["Run the primary local command from README examples (app start, CLI invocation, or generator refresh)."]
    if not verify_lines:
        verify_lines = ["Run repository verification commands from README or CI (lint/test/build equivalents)."]
    if not refresh_lines:
        refresh_lines = ["Refresh `AGENTS/` after major codebase, workflow, or terminology changes."]

    return f"""# Workflows

## Best Used For

- Getting an agent from zero context to runnable context quickly
- Running the minimum commands needed to inspect or validate changes
- Refreshing agent docs after the repository shape changes

## Setup

```bash
{chr(10).join(setup_lines)}
```

## Run

```bash
{chr(10).join(run_lines)}
```

## Verify

```bash
{chr(10).join(verify_lines)}
```

## Refresh / Handoff Notes

{format_bullets(refresh_lines, "No refresh notes recorded.")}
"""


def build_glossary(analysis: RepoAnalysis) -> str:
    facts = list(analysis.glossary_entries)
    if analysis.repo_type == "skill-meta" and analysis.skill_meta.skill_name:
        facts.append(f"- `skill`: `{analysis.skill_meta.skill_name}`")

    naming_rules = [
        "- Prefer canonical repository terms over improvised synonyms in generated docs.",
        "- When a command, file path, or manifest label is user-facing, keep it stable unless the repository intentionally renames it.",
    ]
    if analysis.repo_type == "skill-meta":
        naming_rules.append(
            "- Keep skill names, manifest display names, and installation commands aligned across README, manifests, and generator output."
        )

    return f"""# Glossary

## Best Used For

- Normalizing the terminology multiple agents should share
- Avoiding naming drift between generated docs, code, and user-facing instructions

## Confirmed Terms

{chr(10).join(facts) if facts else "- Needs human confirmation: add canonical repository terms and labels."}

## Naming Rules

{chr(10).join(naming_rules)}

## Open Questions

- Confirm which user-facing names must remain stable across documentation, manifests, and scripts.
"""


def build_layered_entry(analysis: RepoAnalysis) -> str:
    reading_order = [
        "`01-product/001-core-goals.md`",
        "`01-product/002-prd.md`",
        "`02-architecture/004-tech-stack.md`",
        "`02-architecture/006-backend-structure.md`",
        "`02-architecture/007-architecture-compatibility.md`",
        "`03-execution/008-implementation-plan.md`",
        "`04-memory/009-progress.md`",
        "`04-memory/010-lessons.md`",
    ]
    if analysis.repo_type in {"web-app", "skill-meta", "cli-tool"}:
        reading_order.insert(3, "`01-product/003-app-flow.md`")
        reading_order.insert(5, "`02-architecture/005-frontend-guidelines.md`")
    supporting_docs = supporting_docs_for_role(analysis, "product") + supporting_docs_for_role(analysis, "architecture") + supporting_docs_for_role(analysis, "execution")

    rules = [
        "Read product and architecture docs before broad refactors.",
        "Refresh `AGENTS/` after meaningful repo-shape, workflow, or terminology changes.",
        "Prefer confirmed facts over speculative roadmap language.",
        "Protect hand-maintained notes with manual blocks when refresh safety matters.",
    ]
    if analysis.repo_type == "skill-meta":
        rules.append("Keep the skill manifest, SKILL.md instructions, and generator behavior aligned.")
    elif analysis.repo_type == "web-app":
        rules.append("Treat frontend routes, backend endpoints, and result contracts as linked surfaces.")

    return f"""# AGENTS Entry

## Purpose

- Define the reading order before an agent changes code or docs
- State the operating rules that should survive session resets
- Point future agents at the repository's canonical fact sources

## Reading Order

{format_bullets(reading_order, "Add a repository-specific reading order.")}

## Rules

{format_bullets(rules, "Add repository-specific execution rules.")}

## Current Operating Posture

- {current_operating_posture(analysis)}
- Current classification: `{repo_type_label(analysis.repo_type)}` with `{analysis.classification.confidence}` confidence.

## Canonical Fact Sources

{format_bullets(list(analysis.repo_type_reasons), "Needs human confirmation: add canonical fact sources and classification reasons.")}

## Referenced Repository Docs

{format_bullets(supporting_doc_lines(supporting_docs, analysis.root), "No additional repository docs were referenced automatically.")}
"""


def build_layered_core_goals(analysis: RepoAnalysis) -> str:
    goals = []
    if analysis.summary:
        goals.append(analysis.summary)
    goals.append(f"This repository is currently best understood as a `{repo_type_label(analysis.repo_type)}`.")
    if analysis.repo_type == "skill-meta":
        goals.append("The core product is the reusable agent-documentation workflow, not only the generated files themselves.")
    elif analysis.repo_type == "web-app":
        goals.append("The core product includes both the user-facing flow and the runtime contract that supports it.")

    constraints = [
        "Avoid drifting away from the repository's real code, scripts, and naming conventions.",
        "Prefer stable entrypoints and contracts over broad structural churn.",
    ]
    if analysis.classification.conflicting_signals:
        constraints.append("Review mixed signals before collapsing the repository into a single simplistic mental model.")
    references = supporting_docs_for_role(analysis, "product")
    confirmed = supporting_doc_insight_lines(analysis, "product", "confirmed")
    conflicting = supporting_doc_insight_lines(analysis, "product", "conflicting")
    unresolved = supporting_doc_insight_lines(analysis, "product", "unresolved")

    return f"""# Core Goals

## Confirmed Facts

{format_bullets(goals, "Needs human confirmation: add a concise project goal statement.")}

## Constraints To Preserve

{format_bullets(constraints, "Add repository-specific constraints.")}

## Supporting Doc Synthesis (Product)

### Confirmed

{format_bullets(confirmed, "No clear product facts were synthesized from supporting docs.")}

### Conflicting

{format_bullets(conflicting, "No direct product conflicts were synthesized from supporting docs.")}

### Unresolved

{format_bullets(unresolved, "No unresolved product items were synthesized from supporting docs.")}

## Referenced Repository Docs

{format_bullets(supporting_doc_lines(references, analysis.root), "No additional product-oriented repository docs were referenced automatically.")}

## Open Questions

{format_bullets(list(analysis.repo_type_questions), "Confirm the top-level success criteria and non-goals for this repository.")}
"""


def build_layered_prd(analysis: RepoAnalysis) -> str:
    users = [
        f"Primary classification: `{repo_type_label(analysis.repo_type)}`.",
    ]
    if analysis.repo_type == "skill-meta":
        users.append("Likely users are maintainers evolving the skill plus agents that consume its generated guidance.")
    elif analysis.repo_type == "web-app":
        users.append("Likely users are product operators using the app and engineers maintaining the full stack.")
    elif analysis.repo_type in {"cli-tool", "library-sdk"}:
        users.append("Likely users are developers integrating or operating the tooling.")

    journeys = []
    if analysis.routes:
        journeys.extend([f"Route or entry surface: `{route}`" for route in analysis.routes[:8]])
    elif analysis.cli_entrypoints:
        journeys.extend([f"CLI entrypoint: `{rel_path(path, analysis.root)}`" for path in analysis.cli_entrypoints[:6]])
    elif analysis.skill_meta.agent_manifests:
        journeys.extend(
            [f"Agent surface: `{rel_path(path, analysis.root)}`" for path in analysis.skill_meta.agent_manifests[:4]]
        )
    references = supporting_docs_for_role(analysis, "product")
    confirmed = supporting_doc_insight_lines(analysis, "product", "confirmed")
    conflicting = supporting_doc_insight_lines(analysis, "product", "conflicting")
    unresolved = supporting_doc_insight_lines(analysis, "product", "unresolved")

    return f"""# PRD

## Best Used For

- Aligning agents on who this repository serves
- Checking whether a change still supports the intended user journey

## Likely Users And Outcomes

{format_bullets(users, "Needs human confirmation: describe the primary users and outcomes.")}

## Current Entry Surfaces

{format_bullets(journeys, "No obvious user entry surfaces were detected automatically.")}

## Supporting Doc Synthesis (Product)

### Confirmed

{format_bullets(confirmed, "No clear product facts were synthesized from supporting docs.")}

### Conflicting

{format_bullets(conflicting, "No direct product conflicts were synthesized from supporting docs.")}

### Unresolved

{format_bullets(unresolved, "No unresolved product items were synthesized from supporting docs.")}

## Supporting Repository Docs

{format_bullets(supporting_doc_lines(references, analysis.root), "No additional product docs were detected outside AGENTS/.")}

## Questions To Resolve

- Confirm the primary audience and the exact outcome they expect from this repository.
- Confirm which behaviors or labels must remain stable for downstream users.
"""


def build_layered_app_flow(analysis: RepoAnalysis) -> str:
    stages = []
    if analysis.routes:
        stages.extend([f"Browser route: `{route}`" for route in analysis.routes[:8]])
    if analysis.components:
        stages.extend([f"Component surface: `{component}`" for component in analysis.components[:6]])
    if analysis.cli_entrypoints:
        stages.extend([f"Command surface: `{rel_path(path, analysis.root)}`" for path in analysis.cli_entrypoints[:6]])
    if analysis.skill_meta.agent_manifests:
        stages.extend(
            [f"Agent manifest surface: `{rel_path(path, analysis.root)}`" for path in analysis.skill_meta.agent_manifests[:4]]
        )

    guidance = [
        "Treat the first visible or invoked surface as part of the product contract.",
        "Keep user-facing names aligned across README examples, manifests, routes, and commands.",
    ]
    if analysis.repo_type == "web-app":
        guidance.append("Preserve route semantics and component hierarchy before redesigning layout or navigation.")
    elif analysis.repo_type == "skill-meta":
        guidance.append("Treat install, invocation, and prompt surfaces as the equivalent of a frontend contract.")
    confirmed = supporting_doc_insight_lines(analysis, "product", "confirmed")
    conflicting = supporting_doc_insight_lines(analysis, "product", "conflicting")
    unresolved = supporting_doc_insight_lines(analysis, "product", "unresolved")

    return f"""# App Flow

## Surfaces Detected

{format_bullets(stages, "No routes, command surfaces, or manifest surfaces were detected automatically.")}

## Guidance

{format_bullets(guidance, "Add repository-specific flow guidance.")}

## Supporting Doc Synthesis (Flow)

### Confirmed

{format_bullets(confirmed, "No clear flow facts were synthesized from supporting docs.")}

### Conflicting

{format_bullets(conflicting, "No direct flow conflicts were synthesized from supporting docs.")}

### Unresolved

{format_bullets(unresolved, "No unresolved flow items were synthesized from supporting docs.")}
"""


def build_layered_tech_stack(analysis: RepoAnalysis) -> str:
    stack = [
        f"Repo type: `{analysis.repo_type}`.",
        f"Doc profile: `{analysis.doc_profile}`.",
        f"Classification confidence: `{analysis.classification.confidence}`.",
        f"Package manager: `{analysis.package_manager}`.",
        f"Frontend stack: {analysis.frontend_stack}",
        f"Backend/runtime stack: {analysis.backend_stack}",
    ]
    if analysis.frontend_root:
        stack.append(f"Frontend root: `{rel_path(analysis.frontend_root, analysis.root)}`.")
    if analysis.backend_root:
        stack.append(f"Backend root: `{rel_path(analysis.backend_root, analysis.root)}`.")

    return f"""# Tech Stack

## Confirmed Facts

{format_bullets(stack, "Needs human confirmation: record the canonical stack facts.")}

## Secondary Traits

{format_bullets(list(analysis.classification.secondary_traits), "No secondary traits were detected automatically.")}
"""


def build_layered_frontend_guidelines(analysis: RepoAnalysis) -> str:
    guidance = [
        "Keep user-facing routes, labels, prompts, or commands stable unless the repository intentionally renames them.",
        "Review README examples and visible entry surfaces before changing interaction flows.",
    ]
    if analysis.repo_type == "web-app":
        guidance.extend(
            [
                "Treat routes and component hierarchy as part of the working product contract.",
                "Preserve the main interaction path before optimizing styling or layout details.",
            ]
        )
    elif analysis.repo_type == "skill-meta":
        guidance.extend(
            [
                "Treat skill manifests, trigger phrasing, and invocation prompts as the user-facing interface.",
                "Do not let manifest language drift away from what the generator actually supports.",
            ]
        )

    evidence = []
    if analysis.routes:
        evidence.extend([f"Detected route: `{route}`" for route in analysis.routes[:6]])
    if analysis.components:
        evidence.extend([f"Detected component: `{component}`" for component in analysis.components[:6]])
    if analysis.skill_meta.agent_manifests:
        evidence.extend(
            [f"Detected manifest: `{rel_path(path, analysis.root)}`" for path in analysis.skill_meta.agent_manifests[:4]]
        )

    return f"""# Frontend Guidelines

## Guidance

{format_bullets(guidance, "Add repository-specific frontend or interaction-surface guidance.")}

## Evidence

{format_bullets(evidence, "No route, component, or manifest evidence was detected automatically.")}
"""


def build_layered_backend_structure(analysis: RepoAnalysis) -> str:
    responsibilities = [
        "Identify the runtime or automation entrypoint before changing behavior.",
        "Treat outputs, contracts, and side effects as downstream-facing surfaces.",
    ]
    if analysis.repo_type == "skill-meta":
        responsibilities.append("The generator script and helper scripts are the backend-like execution layer.")
    elif analysis.repo_type == "backend-service":
        responsibilities.append("HTTP endpoints and returned payload shapes are the clearest service contract.")

    runtime_entries = []
    if analysis.skill_meta.scripts:
        runtime_entries.extend([f"`{rel_path(path, analysis.root)}`" for path in analysis.skill_meta.scripts[:6]])
    if analysis.cli_entrypoints:
        runtime_entries.extend([f"`{rel_path(path, analysis.root)}`" for path in analysis.cli_entrypoints[:6]])
    if analysis.endpoints:
        runtime_entries.extend([f"`{endpoint}`" for endpoint in analysis.endpoints[:8]])

    return f"""# Backend Structure

## Responsibilities

{format_bullets(responsibilities, "Add repository-specific backend responsibilities.")}

## Runtime Entry Points

{format_bullets(runtime_entries, "No runtime entrypoints were detected automatically.")}

## Stable Contract Fields

{format_bullets(list(analysis.contract_fields), "No stable contract fields were detected automatically.")}

## Storage And Outputs

{format_bullets(list(analysis.storage_rules), "No storage or output rules were detected automatically.")}
"""


def build_layered_architecture_compatibility(analysis: RepoAnalysis) -> str:
    source_of_truth = infer_source_of_truth_lines(analysis)
    references = supporting_docs_for_role(analysis, "architecture")
    confirmed = supporting_doc_insight_lines(analysis, "architecture", "confirmed")
    conflicting = supporting_doc_insight_lines(analysis, "architecture", "conflicting")
    unresolved = supporting_doc_insight_lines(analysis, "architecture", "unresolved")

    boundaries = [
        "Prefer changing source code and configuration first, then refresh `AGENTS/` docs.",
        "Do not let generated docs drift away from the repository's actual entrypoints and workflows.",
    ]
    if analysis.repo_type == "skill-meta":
        boundaries.append("Skill manifests, README examples, and generator output should describe the same capability surface.")

    return f"""# Architecture Compatibility

## Repo-Type Signals

{format_bullets(list(analysis.repo_type_reasons), "No strong classification signals were detected automatically.")}

## Source Of Truth

{format_bullets(source_of_truth, "Needs human confirmation: add canonical source-of-truth files.")}

## Supporting Doc Synthesis (Architecture)

### Confirmed

{format_bullets(confirmed, "No clear architecture facts were synthesized from supporting docs.")}

### Conflicting

{format_bullets(conflicting, "No direct architecture conflicts were synthesized from supporting docs.")}

### Unresolved

{format_bullets(unresolved, "No unresolved architecture items were synthesized from supporting docs.")}

## Referenced Architecture Docs

{format_bullets(supporting_doc_lines(references, analysis.root), "No additional architecture docs were detected outside AGENTS/.")}

## Compatibility Boundaries

{format_bullets(boundaries, "Add explicit compatibility boundaries.")}

## Conflicting Signals

{format_bullets(list(analysis.classification.conflicting_signals), "No major conflicting signals were detected automatically.")}
"""


def build_layered_implementation_plan(analysis: RepoAnalysis) -> str:
    next_steps = [
        "Validate setup, run, and verify commands before broad edits.",
        "Refresh AGENTS docs after changing repository structure or workflow commands.",
    ]
    if analysis.repo_type_questions:
        next_steps.append("Resolve the open repository-shape questions before taking on large refactors.")

    setup_lines = []
    run_lines = []
    verify_lines = []
    root_package_scripts = detect_root_package_scripts(analysis.root)

    if analysis.frontend_root:
        frontend_prefix = (
            f"cd {rel_path(analysis.frontend_root, analysis.root)}"
            if analysis.frontend_root != analysis.root
            else "# already at repo root"
        )
        install_cmd = {
            "npm": "npm install",
            "pnpm": "pnpm install",
            "yarn": "yarn install",
        }.get(analysis.package_manager, "npm install")
        setup_lines.extend([frontend_prefix, install_cmd])
        if "dev" in analysis.frontend_scripts:
            run_lines.extend(
                [
                    frontend_prefix,
                    f"{analysis.package_manager} run dev" if analysis.package_manager != "yarn" else "yarn dev",
                ]
            )
    elif root_package_scripts:
        install_cmd = {
            "npm": "npm install",
            "pnpm": "pnpm install",
            "yarn": "yarn install",
        }.get(analysis.package_manager, "npm install")
        setup_lines.append(install_cmd)
        append_package_script_commands(run_lines, analysis.package_manager, root_package_scripts, ("dev", "start"))
        append_package_script_commands(
            verify_lines,
            analysis.package_manager,
            root_package_scripts,
            ("lint", "test", "build", "typecheck", "check"),
        )
    if analysis.backend_root and (analysis.backend_root / "requirements.txt").exists():
        backend_prefix = (
            f"cd {rel_path(analysis.backend_root, analysis.root)}"
            if analysis.backend_root != analysis.root
            else "# backend at repo root"
        )
        setup_lines.extend([backend_prefix, "python3 -m pip install -r requirements.txt"])
        if (analysis.backend_root / "app").exists():
            run_lines.extend([backend_prefix, "uvicorn app.main:app --reload"])

    extend_unique(verify_lines, detect_unittest_commands(analysis.root))
    extend_unique(verify_lines, detect_verify_script_commands(analysis.root))

    if not setup_lines:
        setup_lines = ["Review README setup steps and install dependencies with the repository's package manager."]
    if not run_lines:
        run_lines = ["Run the primary local command from README examples (app start, CLI invocation, or generator refresh)."]
    if not verify_lines:
        verify_lines = ["Run repository verification commands from README or CI (lint/test/build equivalents)."]
    references = supporting_docs_for_role(analysis, "execution")
    confirmed = supporting_doc_insight_lines(analysis, "execution", "confirmed")
    conflicting = supporting_doc_insight_lines(analysis, "execution", "conflicting")
    unresolved = supporting_doc_insight_lines(analysis, "execution", "unresolved")

    return f"""# Implementation Plan

## Current Operating Posture

- {current_operating_posture(analysis)}

## Immediate Next Steps

{format_bullets(next_steps, "Add the next repository-specific execution steps.")}

## Setup

```bash
{chr(10).join(setup_lines)}
```

## Run

```bash
{chr(10).join(run_lines)}
```

## Verify

```bash
{chr(10).join(verify_lines)}
```

## Supporting Doc Synthesis (Execution)

### Confirmed

{format_bullets(confirmed, "No clear execution facts were synthesized from supporting docs.")}

### Conflicting

{format_bullets(conflicting, "No direct execution conflicts were synthesized from supporting docs.")}

### Unresolved

{format_bullets(unresolved, "No unresolved execution items were synthesized from supporting docs.")}

## Supporting Execution Docs

{format_bullets(supporting_doc_lines(references, analysis.root), "No additional execution docs were detected outside AGENTS/.")}
"""


def build_layered_progress(analysis: RepoAnalysis) -> str:
    facts = [
        f"Detected repo type: `{analysis.repo_type}`.",
        f"Doc profile in use: `{analysis.doc_profile}`.",
        f"Classification confidence: `{analysis.classification.confidence}`.",
    ]
    if analysis.summary:
        facts.append(f"Repository summary: {analysis.summary}")
    if analysis.frontend_root:
        facts.append(f"Frontend root detected at `{rel_path(analysis.frontend_root, analysis.root)}`.")
    if analysis.backend_root:
        facts.append(f"Backend root detected at `{rel_path(analysis.backend_root, analysis.root)}`.")

    focus = list(analysis.repo_type_questions) or [
        "Confirm the next milestone and keep this file updated with human-approved progress.",
    ]
    references = supporting_docs_for_role(analysis, "memory")
    confirmed = supporting_doc_insight_lines(analysis, "memory", "confirmed")
    conflicting = supporting_doc_insight_lines(analysis, "memory", "conflicting")
    unresolved = supporting_doc_insight_lines(analysis, "memory", "unresolved")

    return f"""# Progress

## Confirmed Facts

{format_bullets(facts, "Add confirmed current-state facts.")}

## Current Focus

{format_bullets(focus, "Add the current focus items.")}

## Supporting Doc Synthesis (Memory)

### Confirmed

{format_bullets(confirmed, "No clear progress facts were synthesized from supporting docs.")}

### Conflicting

{format_bullets(conflicting, "No direct memory conflicts were synthesized from supporting docs.")}

### Unresolved

{format_bullets(unresolved, "No unresolved memory items were synthesized from supporting docs.")}

## Referenced Memory Docs

{format_bullets(supporting_doc_lines(references, analysis.root), "No additional progress or memory docs were detected automatically.")}
"""


def build_layered_lessons(analysis: RepoAnalysis) -> str:
    lessons = [
        "Read the entry and architecture docs before large structural edits.",
        "Refresh generated agent docs after meaningful repository-shape changes.",
        "Prefer explicit contracts and stable names over agent improvisation.",
    ]
    if analysis.repo_type == "skill-meta":
        lessons.append("Keep manifests, README examples, and generator behavior aligned so the skill does not overpromise.")
    if analysis.classification.conflicting_signals:
        lessons.append("Mixed repository signals are a warning to inspect before refactoring across boundaries.")
    references = supporting_docs_for_role(analysis, "memory")
    confirmed = supporting_doc_insight_lines(analysis, "memory", "confirmed")
    conflicting = supporting_doc_insight_lines(analysis, "memory", "conflicting")
    unresolved = supporting_doc_insight_lines(analysis, "memory", "unresolved")

    return f"""# Lessons

## Durable Lessons

{format_bullets(lessons, "Add durable lessons that should survive session resets.")}

## Supporting Doc Synthesis (Memory)

### Confirmed

{format_bullets(confirmed, "No clear historical lessons were synthesized from supporting docs.")}

### Conflicting

{format_bullets(conflicting, "No direct historical conflicts were synthesized from supporting docs.")}

### Unresolved

{format_bullets(unresolved, "No unresolved historical items were synthesized from supporting docs.")}

## Referenced Historical Docs

{format_bullets(supporting_doc_lines(references, analysis.root), "No additional lessons or status docs were detected automatically.")}
"""


def generate_bootstrap_docs(analysis: RepoAnalysis) -> Dict[str, str]:
    return {
        "README.md": build_readme(analysis),
        "product.md": build_product(analysis),
        "architecture.md": build_architecture(analysis),
        "frontend.md": build_frontend(analysis),
        "backend.md": build_backend(analysis),
        "workflows.md": build_workflows(analysis),
        "glossary.md": build_glossary(analysis),
    }


def generate_layered_docs(analysis: RepoAnalysis) -> Dict[str, str]:
    return {
        "00-entry/AGENTS.md": build_layered_entry(analysis),
        "01-product/001-core-goals.md": build_layered_core_goals(analysis),
        "01-product/002-prd.md": build_layered_prd(analysis),
        "01-product/003-app-flow.md": build_layered_app_flow(analysis),
        "02-architecture/004-tech-stack.md": build_layered_tech_stack(analysis),
        "02-architecture/005-frontend-guidelines.md": build_layered_frontend_guidelines(analysis),
        "02-architecture/006-backend-structure.md": build_layered_backend_structure(analysis),
        "02-architecture/007-architecture-compatibility.md": build_layered_architecture_compatibility(analysis),
        "03-execution/008-implementation-plan.md": build_layered_implementation_plan(analysis),
        "04-memory/009-progress.md": build_layered_progress(analysis),
        "04-memory/010-lessons.md": build_layered_lessons(analysis),
    }


def generate_docs(analysis: RepoAnalysis) -> Dict[str, str]:
    if analysis.doc_profile == "layered":
        return generate_layered_docs(analysis)
    return generate_bootstrap_docs(analysis)


def build_human_overview(analysis: RepoAnalysis) -> str:
    confirmed = supporting_doc_insight_lines(analysis, "product", "confirmed")
    conflicting = supporting_doc_insight_lines(analysis, "product", "conflicting")
    unresolved = supporting_doc_insight_lines(analysis, "product", "unresolved")
    inferred = human_inferred_lines(analysis, "product")
    confirmed, inferred, unresolved, conflicting = compact_human_evidence(
        confirmed,
        inferred,
        unresolved,
        conflicting,
    )
    provenance = supporting_doc_provenance_lines(analysis, "product")
    synthesis_summary = synthesis_summary_lines(analysis, "product")
    audiences = human_audience_lines(analysis)

    core = []
    if analysis.summary:
        core.append(analysis.summary)
    core.append(f"Current repo shape: `{repo_type_label(analysis.repo_type)}`.")
    if analysis.frontend_root:
        core.append(f"Frontend root: `{rel_path(analysis.frontend_root, analysis.root)}`.")
    if analysis.backend_root:
        core.append(f"Backend root: `{rel_path(analysis.backend_root, analysis.root)}`.")
    priorities = []
    if conflicting:
        priorities.append("Resolve conflicting product statements before locking roadmap or interface commitments.")
    if unresolved:
        priorities.append("Convert unresolved items into explicit owner+deadline decisions.")
    if not priorities:
        priorities.append("Capture latest decisions in `docs/` and keep AGENTS synchronized after changes.")
    documentation_gaps = list(unresolved)
    if not documentation_gaps:
        documentation_gaps.append("No major product documentation gaps were detected from supporting sources.")
    maintenance = human_maintenance_lines(analysis, "product", len(unresolved), len(conflicting))
    update_triggers = human_update_trigger_lines(analysis, "product")
    bootstrap_backlog = human_bootstrap_backlog_lines("product", bool(provenance))

    return f"""# Project Overview

## What This Project Is

{format_bullets(core, "Project overview should be confirmed with maintainers.")}

## Intended Audience

{format_bullets(audiences, "Add the primary maintainer audiences for this project.")}

## Key Entry Points

{format_bullets(product_entry_point_lines(analysis), "No clear routes or invocation entrypoints were detected automatically.")}

## Synthesis Summary

{format_bullets(synthesis_summary, "No synthesis summary available.")}

## Knowledge Status

### Confirmed Signals

{format_bullets(confirmed, "No clear project facts were synthesized from supporting docs.")}

### Derived Signals

{format_bullets(inferred, "No additional derived product signals were detected from repository structure.")}

### Open Questions

{format_bullets(unresolved, "No unresolved project items were synthesized from supporting docs.")}

### Conflict Watchlist

{format_bullets(conflicting, "No direct project conflicts were synthesized from supporting docs.")}

## Current Priorities

{format_bullets(priorities, "No immediate priorities were derived automatically.")}

## Documentation Gaps To Close

{format_bullets(documentation_gaps, "No explicit product documentation gaps were detected.")}

## Update Triggers

{format_bullets(update_triggers, "No explicit update triggers were derived automatically.")}

## Maintenance Workflow

{format_bullets(maintenance, "No maintenance workflow suggestions were derived automatically.")}

## Bootstrap Backlog (When Docs Are Thin)

{format_bullets(bootstrap_backlog, "No bootstrap backlog suggestions were derived automatically.")}

## Provenance

{format_bullets(provenance, "No supporting product documents were discovered outside generated outputs.")}
"""


def build_human_architecture(analysis: RepoAnalysis) -> str:
    confirmed = supporting_doc_insight_lines(analysis, "architecture", "confirmed")
    conflicting = supporting_doc_insight_lines(analysis, "architecture", "conflicting")
    unresolved = supporting_doc_insight_lines(analysis, "architecture", "unresolved")
    inferred = human_inferred_lines(analysis, "architecture")
    confirmed, inferred, unresolved, conflicting = compact_human_evidence(
        confirmed,
        inferred,
        unresolved,
        conflicting,
    )
    provenance = supporting_doc_provenance_lines(analysis, "architecture")
    synthesis_summary = synthesis_summary_lines(analysis, "architecture")
    boundaries = [
        "Treat source-of-truth files as canonical when supporting docs disagree.",
        "Refresh both `docs/` and `AGENTS/` after architecture-impacting changes.",
    ]
    system_map = []
    if analysis.frontend_root:
        system_map.append(f"Frontend surface: `{rel_path(analysis.frontend_root, analysis.root)}`")
    if analysis.backend_root:
        system_map.append(f"Backend/runtime surface: `{rel_path(analysis.backend_root, analysis.root)}`")
    if analysis.routes:
        system_map.append(f"Route coverage detected: {', '.join(f'`{route}`' for route in analysis.routes[:4])}")
    if analysis.endpoints:
        system_map.append(f"Endpoint coverage detected: {', '.join(f'`{endpoint}`' for endpoint in analysis.endpoints[:4])}")
    maintenance = human_maintenance_lines(analysis, "architecture", len(unresolved), len(conflicting))
    update_triggers = human_update_trigger_lines(analysis, "architecture")
    bootstrap_backlog = human_bootstrap_backlog_lines("architecture", bool(provenance))

    return f"""# Architecture

## Source Of Truth

{format_bullets(infer_source_of_truth_lines(analysis), "No canonical source-of-truth files were detected automatically.")}

## Detected Signals

{format_bullets(list(analysis.repo_type_reasons), "No strong repo-type signals were detected automatically.")}

## System Map

{format_bullets(system_map, "No system map details were detected automatically.")}

## Synthesis Summary

{format_bullets(synthesis_summary, "No synthesis summary available.")}

## Knowledge Status

### Confirmed Signals

{format_bullets(confirmed, "No clear architecture facts were synthesized from supporting docs.")}

### Derived Signals

{format_bullets(inferred, "No additional derived architecture signals were detected from repository structure.")}

### Open Questions

{format_bullets(unresolved, "No unresolved architecture items were synthesized from supporting docs.")}

### Conflict Watchlist

{format_bullets(conflicting, "No direct architecture conflicts were synthesized from supporting docs.")}

## Stability Boundaries

{format_bullets(boundaries, "No architecture boundaries were derived automatically.")}

## Update Triggers

{format_bullets(update_triggers, "No explicit update triggers were derived automatically.")}

## Maintenance Workflow

{format_bullets(maintenance, "No maintenance workflow suggestions were derived automatically.")}

## Bootstrap Backlog (When Docs Are Thin)

{format_bullets(bootstrap_backlog, "No bootstrap backlog suggestions were derived automatically.")}

## Provenance

{format_bullets(provenance, "No supporting architecture documents were discovered outside generated outputs.")}
"""


def build_human_workflows(analysis: RepoAnalysis) -> str:
    setup_lines = []
    run_lines = []
    verify_lines = []
    root_package_scripts = detect_root_package_scripts(analysis.root)
    confirmed = supporting_doc_insight_lines(analysis, "execution", "confirmed")
    conflicting = supporting_doc_insight_lines(analysis, "execution", "conflicting")
    unresolved = supporting_doc_insight_lines(analysis, "execution", "unresolved")
    inferred = human_inferred_lines(analysis, "execution")
    confirmed, inferred, unresolved, conflicting = compact_human_evidence(
        confirmed,
        inferred,
        unresolved,
        conflicting,
    )
    provenance = supporting_doc_provenance_lines(analysis, "execution")
    synthesis_summary = synthesis_summary_lines(analysis, "execution")

    if analysis.frontend_root:
        frontend_prefix = (
            f"cd {rel_path(analysis.frontend_root, analysis.root)}"
            if analysis.frontend_root != analysis.root
            else "# already at repo root"
        )
        install_cmd = {
            "npm": "npm install",
            "pnpm": "pnpm install",
            "yarn": "yarn install",
        }.get(analysis.package_manager, "npm install")
        setup_lines.extend([frontend_prefix, install_cmd])
        append_package_script_commands(run_lines, analysis.package_manager, analysis.frontend_scripts, ("dev", "start"))
        append_package_script_commands(
            verify_lines,
            analysis.package_manager,
            analysis.frontend_scripts,
            ("lint", "test", "build", "typecheck", "check"),
        )
    elif root_package_scripts:
        install_cmd = {
            "npm": "npm install",
            "pnpm": "pnpm install",
            "yarn": "yarn install",
        }.get(analysis.package_manager, "npm install")
        setup_lines.append(install_cmd)
        append_package_script_commands(run_lines, analysis.package_manager, root_package_scripts, ("dev", "start"))
        append_package_script_commands(
            verify_lines,
            analysis.package_manager,
            root_package_scripts,
            ("lint", "test", "build", "typecheck", "check"),
        )

    if analysis.backend_root and (analysis.backend_root / "requirements.txt").exists():
        backend_prefix = (
            f"cd {rel_path(analysis.backend_root, analysis.root)}"
            if analysis.backend_root != analysis.root
            else "# backend at repo root"
        )
        setup_lines.extend([backend_prefix, "python3 -m pip install -r requirements.txt"])
        if (analysis.backend_root / "app").exists():
            run_lines.extend([backend_prefix, "uvicorn app.main:app --reload"])

    extend_unique(verify_lines, detect_unittest_commands(analysis.root))
    extend_unique(verify_lines, detect_verify_script_commands(analysis.root))

    if not setup_lines:
        setup_lines = ["Review README setup steps and install dependencies with the repository's package manager."]
    if not run_lines:
        run_lines = ["Run the main local command from README examples."]
    if not verify_lines:
        verify_lines = ["Run verification commands from CI or README (lint/test/build equivalents)."]
    operational_notes = []
    if conflicting:
        operational_notes.append("Resolve conflicting workflow instructions before standardizing CI or release checks.")
    if unresolved:
        operational_notes.append("Assign owners for unresolved runbook items to prevent drift in release operations.")
    if not operational_notes:
        operational_notes.append("Keep command examples in this file aligned with CI and README instructions.")
    maintenance = human_maintenance_lines(analysis, "execution", len(unresolved), len(conflicting))
    update_triggers = human_update_trigger_lines(analysis, "execution")
    bootstrap_backlog = human_bootstrap_backlog_lines("execution", bool(provenance))

    return f"""# Workflows

## Setup

```bash
{chr(10).join(setup_lines)}
```

## Run

```bash
{chr(10).join(run_lines)}
```

## Verify

```bash
{chr(10).join(verify_lines)}
```

## Synthesis Summary

{format_bullets(synthesis_summary, "No synthesis summary available.")}

## Knowledge Status

### Confirmed Signals

{format_bullets(confirmed, "No clear execution facts were synthesized from supporting docs.")}

### Derived Signals

{format_bullets(inferred, "No additional derived execution signals were detected from repository structure.")}

### Open Questions

{format_bullets(unresolved, "No unresolved execution items were synthesized from supporting docs.")}

### Conflict Watchlist

{format_bullets(conflicting, "No direct execution conflicts were synthesized from supporting docs.")}

## Operational Notes

{format_bullets(operational_notes, "No additional operational notes were derived automatically.")}

## Update Triggers

{format_bullets(update_triggers, "No explicit update triggers were derived automatically.")}

## Maintenance Workflow

{format_bullets(maintenance, "No maintenance workflow suggestions were derived automatically.")}

## Bootstrap Backlog (When Docs Are Thin)

{format_bullets(bootstrap_backlog, "No bootstrap backlog suggestions were derived automatically.")}

## Provenance

{format_bullets(provenance, "No supporting execution documents were discovered outside generated outputs.")}
"""


def build_human_glossary(analysis: RepoAnalysis) -> str:
    terms = [re.sub(r"^[-*]\s+", "", entry).strip() for entry in analysis.glossary_entries if entry.strip()]
    if analysis.skill_meta.skill_name:
        terms.append(f"`skill`: `{analysis.skill_meta.skill_name}`")
    unresolved = supporting_doc_insight_lines(analysis, "memory", "unresolved")
    conflicting = supporting_doc_insight_lines(analysis, "memory", "conflicting")
    inferred = human_inferred_lines(analysis, "memory")
    confirmed, inferred, unresolved, conflicting = compact_human_evidence(
        terms,
        inferred,
        unresolved,
        conflicting,
    )
    provenance = supporting_doc_provenance_lines(analysis, "memory")
    synthesis_summary = synthesis_summary_lines(analysis, "memory")
    candidate_terms = []
    if analysis.routes:
        candidate_terms.extend(f"- `route:{route}`" for route in analysis.routes[:4])
    if analysis.endpoints:
        candidate_terms.extend(f"- `endpoint:{endpoint}`" for endpoint in analysis.endpoints[:4])
    if not candidate_terms:
        candidate_terms.append("- No additional term candidates were derived from routes/endpoints.")
    maintenance = human_maintenance_lines(analysis, "memory", len(unresolved), len(conflicting))
    update_triggers = human_update_trigger_lines(analysis, "memory")
    bootstrap_backlog = human_bootstrap_backlog_lines("memory", bool(provenance))

    return f"""# Glossary

## Confirmed Terms

{format_bullets(confirmed, "No canonical terms were detected automatically.")}

## Naming Rules

- Keep user-facing names, commands, and labels consistent across docs and scripts.
- Prefer canonical project terms over ad-hoc synonyms.

## Synthesis Summary

{format_bullets(synthesis_summary, "No synthesis summary available.")}

## Candidate Terms From Code Signals

{chr(10).join(candidate_terms)}

## Derived Terminology Signals

{format_bullets(inferred, "No additional derived terminology signals were detected from repository structure.")}

## Unresolved Terminology Items

{format_bullets(unresolved, "No unresolved terminology or memory items were synthesized from supporting docs.")}

## Conflicting Terminology Signals

{format_bullets(conflicting, "No conflicting terminology signals were synthesized from supporting docs.")}

## Update Triggers

{format_bullets(update_triggers, "No explicit update triggers were derived automatically.")}

## Maintenance Workflow

{format_bullets(maintenance, "No maintenance workflow suggestions were derived automatically.")}

## Bootstrap Backlog (When Docs Are Thin)

{format_bullets(bootstrap_backlog, "No bootstrap backlog suggestions were derived automatically.")}

## Provenance

{format_bullets(provenance, "No supporting memory documents were discovered outside generated outputs.")}
"""


def generate_human_docs(analysis: RepoAnalysis) -> Dict[str, str]:
    return {
        "docs/overview.md": build_human_overview(analysis),
        "docs/architecture.md": build_human_architecture(analysis),
        "docs/workflows.md": build_human_workflows(analysis),
        "docs/glossary.md": build_human_glossary(analysis),
    }
