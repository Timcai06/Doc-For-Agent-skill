from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from .models import RepoAnalysis, SkillMetadata
from .utils import (
    extract_readme_summary,
    find_files,
    find_first_existing,
    list_top_level_dirs,
    list_top_level_files,
    load_json,
    read_text,
)


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
    return [
        str(path.relative_to(repo_root)).replace("\\", "/")
        for path in sorted(scripts_dir.iterdir())
        if path.is_file()
    ]


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


def detect_skill_metadata(root: Path) -> SkillMetadata:
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

    return SkillMetadata(
        skill_file=skill_file,
        skill_name=skill_name,
        agent_manifests=yaml_files,
        references=references,
        scripts=scripts,
    )


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
    return find_files(
        root,
        [
            "bin/*",
            "cli/**/*.ts",
            "cli/**/*.js",
            "cli/**/*.py",
        ],
        limit=8,
    )


def detect_repo_type(
    root: Path,
    frontend_root: Optional[Path],
    backend_root: Optional[Path],
    cli_entrypoints: Sequence[Path],
) -> Tuple[str, List[str], List[str]]:
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
                open_questions.append(
                    f"Package `{package_name}` was detected, but repository type still needs human confirmation."
                )

    if find_first_existing(root, ["pyproject.toml", "setup.py"]) and not backend_root:
        reasons.append("Python packaging files detected without service-style app layout.")
        return ("library-sdk", reasons, open_questions)

    if top_files:
        open_questions.append(
            "Repository shape was not strongly classified; confirm whether this is an app, library, or tooling repo."
        )
    return ("unknown", reasons, open_questions)


def analyze_repo(root: Path, project_name: str) -> RepoAnalysis:
    frontend_root = detect_frontend_root(root)
    backend_root = detect_backend_root(root)
    cli_entrypoints = detect_cli_entrypoints(root)
    library_entrypoints = detect_library_entrypoints(root)
    repo_type, repo_type_reasons, repo_type_questions = detect_repo_type(
        root,
        frontend_root,
        backend_root,
        cli_entrypoints,
    )

    summary = extract_readme_summary(root)
    package_manager = detect_package_manager(frontend_root, root)
    frontend_stack, routes, components, frontend_scripts = describe_frontend(frontend_root)
    backend_stack, endpoints, storage_rules = detect_backend_stack(backend_root)

    return RepoAnalysis(
        root=root,
        project_name=project_name,
        repo_type=repo_type,
        repo_type_reasons=repo_type_reasons,
        repo_type_questions=repo_type_questions,
        summary=summary,
        frontend_root=frontend_root,
        backend_root=backend_root,
        package_manager=package_manager,
        frontend_stack=frontend_stack,
        routes=routes,
        components=components,
        frontend_scripts=frontend_scripts,
        backend_stack=backend_stack,
        endpoints=endpoints,
        storage_rules=storage_rules,
        script_files=detect_scripts(root),
        glossary_entries=detect_glossary(root),
        contract_fields=detect_result_contract(root),
        skill_meta=detect_skill_metadata(root),
        library_entrypoints=library_entrypoints,
        cli_entrypoints=cli_entrypoints,
    )
