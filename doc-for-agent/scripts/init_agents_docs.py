#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


MANUAL_START = "<!-- doc-for-agent:manual-start -->"
MANUAL_END = "<!-- doc-for-agent:manual-end -->"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def write_file(path: Path, content: str) -> None:
    path.write_text(content.strip() + "\n", encoding="utf-8")


def split_markdown_sections(content: str) -> Tuple[str, List[Tuple[str, str]]]:
    lines = content.strip().splitlines()
    if not lines:
        return ("", [])

    title = lines[0].strip()
    sections: List[Tuple[str, str]] = []
    current_heading: Optional[str] = None
    current_lines: List[str] = []

    for line in lines[1:]:
        if line.startswith("## "):
            if current_heading is not None:
                sections.append((current_heading, "\n".join(current_lines).strip()))
            current_heading = line.strip()
            current_lines = []
        else:
            if current_heading is not None:
                current_lines.append(line)

    if current_heading is not None:
        sections.append((current_heading, "\n".join(current_lines).strip()))

    return (title, sections)


def is_manual_section(content: str) -> bool:
    stripped = content.strip()
    if not stripped:
        return False
    if MANUAL_START in stripped and MANUAL_END in stripped:
        return True

    useful_lines = []
    for line in stripped.splitlines():
        text = line.strip()
        if not text:
            continue
        if text.startswith("TODO:") or text.startswith("- TODO:") or text.startswith("# TODO:"):
            continue
        useful_lines.append(text)

    if not useful_lines:
        return False

    placeholder_patterns = [
        "identify",
        "describe",
        "record",
        "list primary users",
        "list important",
        "未检测到",
        "needs human confirmation",
        "open questions",
    ]
    joined = " ".join(useful_lines).lower()
    return not any(pattern in joined for pattern in placeholder_patterns) or len(useful_lines) > 2


def should_preserve_section(content: str) -> bool:
    return is_manual_section(content)


def extract_manual_blocks(content: str) -> List[str]:
    pattern = re.compile(
        rf"{re.escape(MANUAL_START)}\n?(.*?){re.escape(MANUAL_END)}",
        re.DOTALL,
    )
    blocks = []
    for match in pattern.findall(content):
        block = match.strip()
        if block:
            blocks.append(block)
    return blocks


def append_manual_blocks(content: str, manual_blocks: Sequence[str]) -> str:
    if not manual_blocks:
        return content

    lines = [content.rstrip()] if content.strip() else []
    for block in manual_blocks:
        if lines:
            lines.append("")
        lines.append(MANUAL_START)
        lines.extend(block.splitlines())
        lines.append(MANUAL_END)
    return "\n".join(lines).strip()


def merge_markdown(existing: str, generated: str) -> str:
    existing_title, existing_sections = split_markdown_sections(existing)
    generated_title, generated_sections = split_markdown_sections(generated)
    if not existing_sections:
        return generated.strip() + "\n"

    existing_map = {heading: body for heading, body in existing_sections}
    merged_lines = [generated_title or existing_title]
    seen = set()

    for heading, body in generated_sections:
        chosen = body
        existing_body = existing_map.get(heading, "")
        manual_blocks = extract_manual_blocks(existing_body)
        if manual_blocks:
            chosen = append_manual_blocks(body, manual_blocks)
        elif is_manual_section(existing_body):
            chosen = existing_body
        merged_lines.extend(["", heading, "", chosen or ""])
        seen.add(heading)

    remaining_sections = [
        (heading, body)
        for heading, body in existing_sections
        if heading not in seen and heading != "## Preserved Notes" and body.strip() and should_preserve_section(body)
    ]
    if remaining_sections:
        merged_lines.extend(["", "## Preserved Notes", ""])
        for heading, body in remaining_sections:
            merged_lines.append(f"- {heading.removeprefix('## ').strip()}")
            merged_lines.append("  - Preserved from previous manual edits.")
            if body.strip():
                for line in body.splitlines():
                    merged_lines.append(f"  {line}" if line.strip() else "")

    return "\n".join(merged_lines).strip() + "\n"


def find_first_existing(root: Path, candidates: Sequence[str]) -> Optional[Path]:
    for candidate in candidates:
        path = root / candidate
        if path.exists():
            return path
    return None


def load_json(path: Path) -> Dict[str, object]:
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError:
        return {}


def extract_readme_summary(root: Path) -> str:
    readme = find_first_existing(root, ["README.md", "readme.md"])
    if not readme:
        return ""
    lines = read_text(readme).splitlines()
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(">"):
            return stripped.lstrip(">").strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith("-") and not stripped.startswith("```"):
            return stripped
        if index > 40:
            break
    return ""


def extract_markdown_title(root: Path) -> str:
    readme = find_first_existing(root, ["README.md", "readme.md"])
    if not readme:
        return ""
    for line in read_text(readme).splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip(" *`")
    return ""


def infer_project_name(root: Path, explicit_name: Optional[str]) -> str:
    if explicit_name:
        return explicit_name
    title = extract_markdown_title(root)
    if title:
        return title
    return root.name or "project"


def rel_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def list_top_level_dirs(root: Path) -> List[str]:
    return sorted([path.name for path in root.iterdir() if path.is_dir() and not path.name.startswith(".")])


def list_top_level_files(root: Path) -> List[str]:
    return sorted([path.name for path in root.iterdir() if path.is_file() and not path.name.startswith(".")])


def find_files(root: Path, patterns: Sequence[str], limit: int = 12) -> List[Path]:
    matches: List[Path] = []
    seen = set()
    for pattern in patterns:
        for path in sorted(root.glob(pattern)):
            normalized = str(path.resolve())
            if path.is_file() and normalized not in seen:
                matches.append(path)
                seen.add(normalized)
            if len(matches) >= limit:
                return matches[:limit]
    return matches[:limit]


def detect_frontend_root(root: Path) -> Optional[Path]:
    candidates = [root / "frontend", root]
    for candidate in candidates:
        if (candidate / "package.json").exists():
            package = load_json(candidate / "package.json")
            deps = {
                **(package.get("dependencies") or {}),
                **(package.get("devDependencies") or {}),
            }
            if any(key in deps for key in ("next", "react", "vue", "svelte", "astro")):
                return candidate
    return None


def detect_backend_root(root: Path) -> Optional[Path]:
    candidates = [root / "backend", root]
    for candidate in candidates:
        if (candidate / "app").exists() or (candidate / "requirements.txt").exists() or (candidate / "requirements-dev.txt").exists():
            if candidate != root or (candidate / "app").exists():
                return candidate
    return None


def detect_package_manager(frontend_root: Optional[Path], repo_root: Path) -> str:
    candidates = [
        repo_root / "pnpm-lock.yaml",
        repo_root / "yarn.lock",
        repo_root / "package-lock.json",
    ]
    if frontend_root:
        candidates.extend(
            [
                frontend_root / "pnpm-lock.yaml",
                frontend_root / "yarn.lock",
                frontend_root / "package-lock.json",
            ]
        )
    for path in candidates:
        if path.name == "pnpm-lock.yaml" and path.exists():
            return "pnpm"
        if path.name == "yarn.lock" and path.exists():
            return "yarn"
        if path.name == "package-lock.json" and path.exists():
            return "npm"
    return "npm"


def describe_frontend(frontend_root: Optional[Path]) -> Tuple[str, List[str], List[str], Dict[str, str]]:
    if not frontend_root:
        return ("No dedicated frontend detected.", [], [], {})

    package_json = frontend_root / "package.json"
    package = load_json(package_json)
    deps = {
        **(package.get("dependencies") or {}),
        **(package.get("devDependencies") or {}),
    }
    scripts = package.get("scripts") or {}

    stack_parts: List[str] = []
    if "next" in deps:
        stack_parts.append(f"Next.js {deps['next']}")
    if "react" in deps:
        stack_parts.append(f"React {deps['react']}")
    if "tailwindcss" in deps:
        stack_parts.append(f"TailwindCSS {deps['tailwindcss']}")
    if "vite" in deps:
        stack_parts.append(f"Vite {deps['vite']}")
    if "vue" in deps:
        stack_parts.append(f"Vue {deps['vue']}")
    if not stack_parts:
        stack_parts.append("Frontend package.json detected, but no common framework was recognized")

    route_root = find_first_existing(frontend_root, ["app", "src/app", "pages", "src/pages"])
    routes = detect_routes(route_root, frontend_root) if route_root else []

    component_root = find_first_existing(frontend_root, ["src/components", "components"])
    components: List[str] = []
    if component_root:
        components = [
            str(path.relative_to(frontend_root)).replace("\\", "/")
            for path in sorted(component_root.glob("*.tsx"))
        ][:8]

    normalized_scripts = {
        str(key): str(value)
        for key, value in scripts.items()
        if isinstance(key, str) and isinstance(value, str)
    }
    return (", ".join(stack_parts), routes, components, normalized_scripts)


def detect_routes(route_root: Path, frontend_root: Path) -> List[str]:
    routes: List[str] = []
    for file_path in sorted(route_root.rglob("page.tsx")):
        relative = file_path.relative_to(route_root)
        parts = list(relative.parts[:-1])
        route_parts = []
        for part in parts:
            if part.startswith("(") and part.endswith(")"):
                continue
            route_parts.append(part)
        route = "/" + "/".join(route_parts)
        routes.append(route if route != "/" else "/")
    if (frontend_root / "app/page.tsx").exists() or (frontend_root / "src/app/page.tsx").exists():
        if "/" not in routes:
            routes.insert(0, "/")
    return routes[:16]


def detect_backend_stack(backend_root: Optional[Path]) -> Tuple[str, List[str], List[str]]:
    if not backend_root:
        return ("No dedicated backend detected.", [], [])

    stack_parts: List[str] = []
    requirements = read_text(backend_root / "requirements.txt") + "\n" + read_text(backend_root / "requirements-dev.txt")
    requirements_lower = requirements.lower()
    if "fastapi" in requirements_lower:
        stack_parts.append("FastAPI")
    if "uvicorn" in requirements_lower:
        stack_parts.append("Uvicorn")
    if "flask" in requirements_lower:
        stack_parts.append("Flask")
    if "django" in requirements_lower:
        stack_parts.append("Django")
    if (backend_root / "pyproject.toml").exists():
        pyproject = read_text(backend_root / "pyproject.toml").lower()
        if "fastapi" in pyproject and "FastAPI" not in stack_parts:
            stack_parts.append("FastAPI")

    endpoints = detect_backend_endpoints(backend_root)
    storage_rules = detect_storage_rules(backend_root)
    if not stack_parts:
        stack_parts.append("Backend-like Python structure detected, but no common framework was recognized")
    return (", ".join(stack_parts), endpoints, storage_rules)


def detect_backend_endpoints(backend_root: Path) -> List[str]:
    endpoints: List[str] = []
    python_files = list((backend_root / "app").rglob("*.py")) if (backend_root / "app").exists() else list(backend_root.rglob("*.py"))
    pattern = re.compile(r"@(router|app)\.(get|post|put|delete|patch)\(\s*[\"']([^\"']+)[\"']")
    for path in python_files:
        text = read_text(path)
        for _, method, route in pattern.findall(text):
            label = f"{method.upper()} {route}"
            if label not in endpoints:
                endpoints.append(label)
    return endpoints[:16]


def detect_storage_rules(backend_root: Path) -> List[str]:
    rules: List[str] = []
    local_storage = backend_root / "app/storage/local.py"
    if local_storage.exists():
        rules.append("Local file storage is used for generated artifacts.")
    result_service = backend_root / "app/services/result_service.py"
    result_text = read_text(result_service)
    if "history-" in result_text and "zip" in result_text:
        rules.append("Historical exports appear to support zip bundle generation.")
    mapper = backend_root / "app/core/category_mapper.py"
    if mapper.exists():
        rules.append("Backend normalizes categories before returning them to clients.")
    return rules


def detect_scripts(repo_root: Path) -> List[str]:
    scripts_dir = repo_root / "scripts"
    if not scripts_dir.exists():
        return []
    return [str(path.relative_to(repo_root)).replace("\\", "/") for path in sorted(scripts_dir.iterdir()) if path.is_file()]


def detect_glossary(root: Path) -> List[str]:
    entries: List[str] = []
    mapper = find_first_existing(root, ["backend/app/core/category_mapper.py", "app/core/category_mapper.py"])
    mapper_text = read_text(mapper) if mapper else ""
    mapping_pairs = [
        ("crack", "裂缝"),
        ("breakage", "破损"),
        ("comb", "梳齿缺陷"),
        ("hole", "孔洞"),
        ("reinforcement", "钢筋外露"),
        ("seepage", "渗水"),
    ]
    for key, label in mapping_pairs:
        if key in mapper_text:
            entries.append(f"- `{key}`: `{label}`")
    return entries


def detect_result_contract(root: Path) -> List[str]:
    entries: List[str] = []
    types_path = find_first_existing(root, ["frontend/src/lib/types.ts", "src/lib/types.ts"])
    schemas_path = find_first_existing(root, ["backend/app/models/schemas.py", "app/models/schemas.py"])
    text_parts = []
    if types_path:
        text_parts.append(read_text(types_path))
    if schemas_path:
        text_parts.append(read_text(schemas_path))
    text = "\n".join(text_parts)
    for field in ["has_masks", "mask_detection_count", "model_version", "detections", "artifacts"]:
        if field in text:
            entries.append(f"- `{field}`")
    return entries


def detect_skill_metadata(root: Path) -> Dict[str, object]:
    skill_file = find_first_existing(root, ["SKILL.md", "skill.md", "doc-for-agent/SKILL.md"])
    yaml_files = find_files(root, ["agents/*.yaml", "agents/*.yml", "*/agents/*.yaml", "*/agents/*.yml"], limit=8)
    references = find_files(root, ["references/*.md", "*/references/*.md"], limit=12)
    scripts = find_files(root, ["scripts/*", "*/scripts/*"], limit=12)

    skill_name = ""
    if skill_file:
        text = read_text(skill_file)
        name_match = re.search(r"^name:\s*(.+)$", text, re.MULTILINE)
        if name_match:
            skill_name = name_match.group(1).strip()

    return {
        "skill_file": skill_file,
        "skill_name": skill_name,
        "agent_manifests": yaml_files,
        "references": references,
        "scripts": scripts,
    }


def detect_library_entrypoints(root: Path) -> List[Path]:
    return find_files(
        root,
        [
            "src/index.ts",
            "src/index.js",
            "src/index.py",
            "src/**/*.py",
            "src/**/*.ts",
            "src/**/*.tsx",
            "src/**/*.js",
            "*.py",
            "*.ts",
            "*.js",
        ],
        limit=8,
    )


def detect_cli_entrypoints(root: Path) -> List[Path]:
    candidates = find_files(
        root,
        [
            "bin/*",
            "cli/**/*.ts",
            "cli/**/*.js",
            "cli/**/*.py",
        ],
        limit=8,
    )
    return candidates


def detect_repo_type(root: Path, frontend_root: Optional[Path], backend_root: Optional[Path]) -> Tuple[str, List[str], List[str]]:
    top_dirs = list_top_level_dirs(root)
    top_files = list_top_level_files(root)
    reasons: List[str] = []
    open_questions: List[str] = []

    has_skill_markers = (
        find_first_existing(root, ["SKILL.md", "skill.md"]) is not None
        or bool(find_files(root, ["agents/*.yaml", "agents/*.yml", "*/agents/*.yaml", "*/agents/*.yml"], limit=1))
    )
    if has_skill_markers:
        reasons.append("Skill markers detected (`SKILL.md`, agent manifests, or an existing `AGENTS/` directory).")
        return ("skill-meta", reasons, open_questions)

    if {"packages", "apps"}.intersection(top_dirs) or (root / "pnpm-workspace.yaml").exists():
        reasons.append("Workspace-style directories or pnpm workspace config detected.")
        return ("monorepo", reasons, open_questions)

    cli_entrypoints = detect_cli_entrypoints(root)
    if cli_entrypoints:
        reasons.append("CLI-like entrypoints detected in `bin/` or `cli/`.")
        if find_first_existing(root, ["package.json", "pyproject.toml"]):
            return ("cli-tool", reasons, open_questions)

    if frontend_root and backend_root:
        reasons.append("Both frontend and backend roots were detected.")
        return ("web-app", reasons, open_questions)

    if backend_root and not frontend_root:
        reasons.append("Backend-like Python service structure detected without a separate frontend.")
        return ("backend-service", reasons, open_questions)

    package_json = root / "package.json"
    if package_json.exists():
        package = load_json(package_json)
        package_name = str(package.get("name") or "")
        deps = {
            **(package.get("dependencies") or {}),
            **(package.get("devDependencies") or {}),
        }
        if not frontend_root and not backend_root:
            if any(key in deps for key in ("typescript", "tsup", "rollup", "vite")):
                reasons.append("Package manifest suggests a library or tool package.")
                return ("library-sdk", reasons, open_questions)
            if package_name:
                open_questions.append(f"Package `{package_name}` was detected, but repository type still needs human confirmation.")

    if find_first_existing(root, ["pyproject.toml", "setup.py"]) and not backend_root:
        reasons.append("Python packaging files detected without service-style app layout.")
        return ("library-sdk", reasons, open_questions)

    if top_files:
        open_questions.append("Repository shape was not strongly classified; confirm whether this is an app, library, or tooling repo.")
    return ("unknown", reasons, open_questions)


def format_bullets(items: Sequence[str], empty_line: str) -> str:
    if not items:
        return f"- {empty_line}"
    return "\n".join(f"- {item}" for item in items)


def format_path_bullets(paths: Sequence[Path], root: Path, empty_line: str) -> str:
    if not paths:
        return f"- {empty_line}"
    return "\n".join(f"- `{rel_path(path, root)}`" for path in paths)


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


def build_readme(project_name: str, repo_type: str) -> str:
    return f"""# AGENTS

## Best Used For

- Fast onboarding when a new coding agent enters this repository
- Multi-agent work where terminology, workflow, and ownership boundaries need to stay aligned
- Refreshing repo-specific context after the codebase structure changes

## Repository Classification

- Detected repo type: `{repo_type_label(repo_type)}`

## Files

- `product.md`: why this repository exists and what agents should preserve
- `architecture.md`: repository shape, source-of-truth files, and handoff boundaries
- `frontend.md`: UI/client context for frontend-facing repos, or agent-facing interface notes otherwise
- `backend.md`: service/runtime contract notes or implementation/runtime entrypoints
- `workflows.md`: setup, execution, verification, and refresh commands
- `glossary.md`: canonical names, labels, and terminology that should stay stable
"""


def build_product(project_name: str, repo_type: str, summary: str, skill_meta: Dict[str, object], routes: Sequence[str]) -> str:
    route_lines = format_bullets([f"`{route}`" for route in routes[:8]], "No user-facing routes were detected automatically.")
    facts = []
    if summary:
        facts.append(summary)
    if repo_type == "skill-meta":
        skill_file = skill_meta.get("skill_file")
        skill_name = skill_meta.get("skill_name")
        if skill_name:
            facts.append(f"Skill name declared in metadata: `{skill_name}`.")
        if isinstance(skill_file, Path):
            facts.append(f"Primary skill definition file: `{skill_file.name}`.")
        facts.append("This repository appears to ship reusable instructions and scripts for coding agents rather than a standalone product app.")

    inferences = [
        f"This repository is best understood as a `{repo_type_label(repo_type)}`.",
    ]
    if repo_type == "skill-meta":
        inferences.append("Primary users are likely maintainers installing or evolving the skill, plus agents that consume the generated guidance.")
    elif repo_type in {"library-sdk", "cli-tool"}:
        inferences.append("Primary users are likely developers integrating or running the packaged tooling.")

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


def build_architecture(
    repo_root: Path,
    repo_type: str,
    frontend_root: Optional[Path],
    backend_root: Optional[Path],
    repo_type_reasons: Sequence[str],
    repo_type_questions: Sequence[str],
    skill_meta: Dict[str, object],
) -> str:
    facts = [
        f"Repository root: `{repo_root}`.",
        f"Detected repo type: `{repo_type}`.",
    ]
    if frontend_root:
        facts.append(f"Frontend root: `{rel_path(frontend_root, repo_root)}`.")
    if backend_root:
        facts.append(f"Backend root: `{rel_path(backend_root, repo_root)}`.")

    if repo_type == "skill-meta":
        skill_file = skill_meta.get("skill_file")
        if isinstance(skill_file, Path):
            facts.append(f"Skill definition entrypoint: `{rel_path(skill_file, repo_root)}`.")
        manifests = skill_meta.get("agent_manifests") or []
        if manifests:
            facts.append("Agent manifest files are present for marketplace or launcher integration.")

    source_of_truth = []
    if repo_type == "skill-meta":
        source_of_truth.extend(
            [
                "`doc-for-agent/SKILL.md` for trigger conditions and operator workflow",
                "`doc-for-agent/scripts/` for generation behavior and repository scanning",
                "`doc-for-agent/references/` for output structure and style constraints",
            ]
        )
    else:
        if frontend_root:
            source_of_truth.append(f"`{rel_path(frontend_root, repo_root)}` for client-side code and scripts")
        if backend_root:
            source_of_truth.append(f"`{rel_path(backend_root, repo_root)}` for service/runtime logic")
        if not source_of_truth:
            source_of_truth.append("Needs human confirmation: identify the files agents should treat as canonical entrypoints")

    handoff = []
    if repo_type == "skill-meta":
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

{format_bullets(list(repo_type_reasons), "No strong classification signals were detected automatically.")}

## Source Of Truth For Agents

{format_bullets(source_of_truth, "Needs human confirmation: identify canonical files and directories.")}

## Handoff Boundaries

{format_bullets(handoff, "Needs human confirmation: add handoff and ownership notes.")}

## Open Questions

{format_bullets(list(repo_type_questions), "No open architecture questions recorded.")}
"""


def build_frontend(
    repo_type: str,
    stack: str,
    routes: Sequence[str],
    components: Sequence[str],
    skill_meta: Dict[str, object],
    repo_root: Path,
) -> str:
    best_used_for = [
        "UI-facing changes, route discovery, and component-level edits" if repo_type == "web-app" else "Agent-facing interface context and user entrypoint discovery",
        "Checking which screens, prompts, or interaction surfaces must stay consistent",
    ]

    facts: List[str] = []
    inferences: List[str] = []
    route_heading = "Routes Or Interaction Entry Points"
    component_heading = "Key Components Or Interface Files"
    manifest_heading = "Agent Manifests / Prompt Surfaces"
    route_lines = format_bullets([f"`{route}`" for route in routes], "No browser routes were detected automatically.")
    component_lines = format_bullets([f"`{component}`" for component in components], "No component inventory was detected automatically.")
    manifest_lines = format_path_bullets(skill_meta.get("agent_manifests") or [], repo_root, "No agent manifest files were detected automatically.")

    if repo_type == "web-app":
        facts.append(f"Detected frontend stack: {stack}.")
        if routes:
            facts.append("User-facing routes were detected from app/page structure.")
        if components:
            facts.append("Top-level components were detected from common component directories.")
    elif repo_type == "skill-meta":
        manifests = skill_meta.get("agent_manifests") or []
        if manifests:
            facts.append("Agent-facing interface manifests are present.")
        facts.append("Primary user interaction likely happens through an AI assistant invoking this skill rather than a browser UI.")
        inferences.append("The closest thing to a frontend here is the installation and invocation surface exposed through skill manifests and prompts.")
    elif repo_type == "cli-tool":
        cli_entrypoints = detect_cli_entrypoints(repo_root)
        best_used_for = [
            "Understanding command entrypoints, command UX, and user-triggered scripts",
            "Checking which command names, flags, or help text must remain stable",
        ]
        route_heading = "CLI Entry Points"
        component_heading = "User-Facing Command Files"
        manifest_heading = "Install / Invocation Surfaces"
        facts.append("Primary user interaction happens through the command line rather than a browser UI.")
        if cli_entrypoints:
            facts.append("CLI entrypoint files were detected.")
        route_lines = format_path_bullets(cli_entrypoints, repo_root, "No CLI entrypoints were detected automatically.")
        component_lines = format_bullets([], "No additional user-facing command files were detected automatically.")
        manifest_lines = format_bullets(
            [
                "Check package metadata, README examples, and shell scripts before renaming commands or changing default behavior."
            ],
            "No install or invocation surfaces were detected automatically.",
        )
        inferences.append("For CLI repositories, the most frontend-like surface is the command syntax, help output, and install story.")
    elif repo_type == "library-sdk":
        library_entrypoints = detect_library_entrypoints(repo_root)
        best_used_for = [
            "Understanding public entrypoints and integration-facing surface area",
            "Checking which exported modules or examples downstream users depend on",
        ]
        route_heading = "Public Entry Points"
        component_heading = "Export Surface Files"
        manifest_heading = "Integration Surfaces"
        facts.append("Primary user interaction is likely through imports, exported helpers, or integration examples rather than an interactive UI.")
        if library_entrypoints:
            facts.append("Library entrypoint files were detected.")
        route_lines = format_path_bullets(library_entrypoints, repo_root, "No public entrypoints were detected automatically.")
        component_lines = format_path_bullets(library_entrypoints[:4], repo_root, "No export surface files were detected automatically.")
        manifest_lines = format_bullets(
            [
                "Check README usage snippets and package exports before changing names or module layout."
            ],
            "No integration surfaces were detected automatically.",
        )
        inferences.append("For library repositories, the user-facing surface is the exported API and import paths, not a browser or CLI shell.")
    else:
        facts.append(stack)

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


def build_backend(
    repo_type: str,
    stack: str,
    endpoints: Sequence[str],
    storage_rules: Sequence[str],
    contract_fields: Sequence[str],
    skill_meta: Dict[str, object],
    repo_root: Path,
) -> str:
    facts: List[str] = []
    inferences: List[str] = []
    runtime_heading = "Runtime Entry Points"
    endpoint_heading = "Main Services / Endpoints"
    contract_heading = "Stable Contract Fields"
    storage_heading = "Storage / Output Rules"
    runtime_files = format_path_bullets(skill_meta.get("scripts") or [], repo_root, "No runtime script files were detected automatically.")
    endpoint_lines = format_bullets([f"`{endpoint}`" for endpoint in endpoints], "No API endpoints were detected automatically.")
    storage_lines = format_bullets(list(storage_rules), "No storage or persistence rules were detected automatically.")
    contract_lines = format_bullets(list(contract_fields), "No stable result-contract fields were detected automatically.")

    if repo_type in {"backend-service", "web-app"}:
        facts.append(f"Detected backend/runtime stack: {stack}.")
        if endpoints:
            facts.append("HTTP endpoints were detected from router decorators.")
        if storage_rules:
            facts.append("Storage-related behavior was inferred from backend source files.")
    elif repo_type == "skill-meta":
        scripts = skill_meta.get("scripts") or []
        if scripts:
            facts.append("Generation or support scripts are present and act as the runtime behavior of this skill.")
        inferences.append("The most important backend-like surface is the generator script and any install/runtime commands that mutate repository docs.")
    elif repo_type == "cli-tool":
        cli_entrypoints = detect_cli_entrypoints(repo_root)
        runtime_heading = "Execution Entry Points"
        endpoint_heading = "Automation / Script Hooks"
        contract_heading = "Stable CLI Contracts"
        storage_heading = "Outputs / Side Effects"
        facts.append("Operational behavior is driven by CLI entrypoints and helper scripts rather than a networked service.")
        if cli_entrypoints:
            facts.append("CLI execution entrypoints were detected.")
        runtime_files = format_path_bullets(cli_entrypoints, repo_root, "No CLI execution entrypoints were detected automatically.")
        endpoint_lines = format_path_bullets(skill_meta.get("scripts") or [], repo_root, "No automation or helper scripts were detected automatically.")
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
    elif repo_type == "library-sdk":
        library_entrypoints = detect_library_entrypoints(repo_root)
        runtime_heading = "Implementation Entry Points"
        endpoint_heading = "Public Modules"
        contract_heading = "Stable API Contracts"
        storage_heading = "Side Effects / Persistence"
        facts.append("Operational behavior is likely exposed through imported modules and exported functions rather than a long-running service.")
        if library_entrypoints:
            facts.append("Library implementation entrypoints were detected.")
        runtime_files = format_path_bullets(library_entrypoints, repo_root, "No implementation entrypoints were detected automatically.")
        endpoint_lines = format_path_bullets(library_entrypoints[:6], repo_root, "No public modules were detected automatically.")
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
        facts.append(stack)

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


def build_workflows(
    repo_root: Path,
    repo_type: str,
    package_manager: str,
    frontend_root: Optional[Path],
    frontend_scripts: Dict[str, str],
    backend_root: Optional[Path],
    script_files: Sequence[str],
) -> str:
    setup_lines: List[str] = []
    run_lines: List[str] = []
    verify_lines: List[str] = []
    refresh_lines: List[str] = []

    if frontend_root:
        frontend_prefix = f"cd {rel_path(frontend_root, repo_root)}" if frontend_root != repo_root else "# already at repo root"
        install_cmd = {"npm": "npm install", "pnpm": "pnpm install", "yarn": "yarn install"}.get(package_manager, "npm install")
        setup_lines.extend([frontend_prefix, install_cmd])
        if "dev" in frontend_scripts:
            run_lines.extend([frontend_prefix, f"{package_manager} run dev" if package_manager != "yarn" else "yarn dev"])
        for key in ("lint", "test", "build"):
            if key in frontend_scripts:
                verify_lines.extend([frontend_prefix, f"{package_manager} run {key}" if package_manager != "yarn" else f"yarn {key}"])

    if backend_root:
        backend_prefix = f"cd {rel_path(backend_root, repo_root)}" if backend_root != repo_root else "# backend at repo root"
        if (backend_root / "requirements-dev.txt").exists():
            setup_lines.extend([backend_prefix, "python3 -m pip install -r requirements-dev.txt"])
        elif (backend_root / "requirements.txt").exists():
            setup_lines.extend([backend_prefix, "python3 -m pip install -r requirements.txt"])
        if (backend_root / "app").exists():
            run_lines.extend([backend_prefix, "uvicorn app.main:app --reload"])

    if repo_type == "skill-meta":
        setup_lines.append("# skill repositories are usually installed by symlink or copied into a local skills directory")
        skill_script = "doc-for-agent/scripts/init_agents_docs.py" if (repo_root / "doc-for-agent/scripts/init_agents_docs.py").exists() else ""
        if skill_script:
            run_lines.append(f"python3 {skill_script} --root /path/to/target-repo --mode refresh")
            refresh_lines.append(f"python3 {skill_script} --root {repo_root} --mode refresh")
        refresh_lines.append("Review generated `AGENTS/*.md` files and tighten any sections still marked as needing human confirmation.")

    if script_files:
        run_lines.extend(f"./{script}" for script in script_files[:6])

    if not setup_lines:
        setup_lines = ["# TODO: add repository setup commands"]
    if not run_lines:
        run_lines = ["# TODO: add local run commands"]
    if not verify_lines:
        verify_lines = ["# TODO: add lint / test / build commands"]
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


def build_glossary(entries: Sequence[str], repo_type: str, skill_meta: Dict[str, object]) -> str:
    facts = list(entries)
    skill_name = str(skill_meta.get("skill_name") or "")
    if repo_type == "skill-meta" and skill_name:
        facts.append(f"- `skill`: `{skill_name}`")
    naming_rules = [
        "- Prefer canonical repository terms over improvised synonyms in generated docs.",
        "- When a command, file path, or manifest label is user-facing, keep it stable unless the repository intentionally renames it.",
    ]
    if repo_type == "skill-meta":
        naming_rules.append("- Keep skill names, manifest display names, and installation commands aligned across README, manifests, and generator output.")

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


def generate_docs(root: Path, project_name: str) -> Dict[str, str]:
    frontend_root = detect_frontend_root(root)
    backend_root = detect_backend_root(root)
    repo_type, repo_type_reasons, repo_type_questions = detect_repo_type(root, frontend_root, backend_root)
    summary = extract_readme_summary(root)
    package_manager = detect_package_manager(frontend_root, root)
    frontend_stack, routes, components, frontend_scripts = describe_frontend(frontend_root)
    backend_stack, endpoints, storage_rules = detect_backend_stack(backend_root)
    script_files = detect_scripts(root)
    glossary_entries = detect_glossary(root)
    contract_fields = detect_result_contract(root)
    skill_meta = detect_skill_metadata(root)

    return {
        "README.md": build_readme(project_name, repo_type),
        "product.md": build_product(project_name, repo_type, summary, skill_meta, routes),
        "architecture.md": build_architecture(root, repo_type, frontend_root, backend_root, repo_type_reasons, repo_type_questions, skill_meta),
        "frontend.md": build_frontend(repo_type, frontend_stack, routes, components, skill_meta, root),
        "backend.md": build_backend(repo_type, backend_stack, endpoints, storage_rules, contract_fields, skill_meta, root),
        "workflows.md": build_workflows(root, repo_type, package_manager, frontend_root, frontend_scripts, backend_root, script_files),
        "glossary.md": build_glossary(glossary_entries, repo_type, skill_meta),
    }


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
