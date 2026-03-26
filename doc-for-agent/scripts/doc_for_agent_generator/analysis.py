from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from .models import DocumentationInventory, RepoAnalysis, RepoClassification, RepoSignals, SkillMetadata
from .utils import (
    extract_readme_summary,
    find_files,
    find_first_existing,
    list_top_level_dirs,
    list_top_level_files,
    load_json,
    read_text,
)

SUPPORTED_REPO_TYPES = (
    "skill-meta",
    "cli-tool",
    "library-sdk",
    "backend-service",
    "web-app",
    "monorepo",
    "unknown",
)

FRONTEND_FRAMEWORK_PACKAGES = {"next", "react", "vue", "svelte", "astro"}
BACKEND_NODE_FRAMEWORK_PACKAGES = {"express", "fastify", "koa", "hono", "nestjs"}
FLAT_AGENTS_FILENAMES = {
    "README.md",
    "product.md",
    "architecture.md",
    "frontend.md",
    "backend.md",
    "workflows.md",
    "glossary.md",
}
LAYERED_AGENTS_PREFIXES = ("00-entry", "01-product", "02-architecture", "03-execution", "04-memory")
GENERATED_HUMAN_DOC_PATHS = {
    "docs/overview.md",
    "docs/architecture.md",
    "docs/workflows.md",
    "docs/glossary.md",
}


def load_package_metadata(package_path: Path) -> Tuple[Dict[str, str], Dict[str, str]]:
    package = load_json(package_path)
    deps = {
        str(key): str(value)
        for key, value in {
            **(package.get("dependencies") or {}),
            **(package.get("devDependencies") or {}),
        }.items()
        if isinstance(key, str)
    }
    scripts = {
        str(key): str(value)
        for key, value in (package.get("scripts") or {}).items()
        if isinstance(key, str) and isinstance(value, str)
    }
    return deps, scripts


def collect_candidate_dirs(
    root: Path,
    fixed_rel_paths: Sequence[str],
    parent_dirs: Sequence[str],
) -> List[Path]:
    candidates: List[Path] = []
    seen: set[str] = set()

    def add(path: Path) -> None:
        resolved = str(path.resolve())
        if path.is_dir() and resolved not in seen:
            candidates.append(path)
            seen.add(resolved)

    for rel_path in fixed_rel_paths:
        add(root / rel_path)

    for parent_dir in parent_dirs:
        parent_path = root / parent_dir
        if not parent_path.is_dir():
            continue
        for child in sorted(parent_path.iterdir()):
            add(child)

    add(root)
    return candidates


def detect_frontend_root(root: Path) -> Optional[Path]:
    candidates = collect_candidate_dirs(
        root,
        fixed_rel_paths=(
            "frontend",
            "client",
            "web",
            "apps/web",
            "apps/frontend",
            "apps/client",
            "apps/site",
            "packages/web",
            "packages/frontend",
            "packages/client",
        ),
        parent_dirs=("apps", "packages"),
    )

    for candidate in candidates:
        package_json = candidate / "package.json"
        if not package_json.exists():
            continue
        deps, _ = load_package_metadata(package_json)
        if FRONTEND_FRAMEWORK_PACKAGES.intersection(deps):
            return candidate
    return None


def detect_backend_root(root: Path) -> Optional[Path]:
    candidates = collect_candidate_dirs(
        root,
        fixed_rel_paths=(
            "backend",
            "api",
            "server",
            "services/api",
            "services/backend",
            "apps/api",
            "apps/server",
            "packages/api",
            "packages/server",
        ),
        parent_dirs=("services", "apps", "packages"),
    )

    for candidate in candidates:
        if (candidate / "app").exists() or (candidate / "requirements.txt").exists() or (candidate / "requirements-dev.txt").exists():
            if candidate != root or (candidate / "app").exists():
                return candidate

        package_json = candidate / "package.json"
        if not package_json.exists():
            continue
        deps, scripts = load_package_metadata(package_json)
        if BACKEND_NODE_FRAMEWORK_PACKAGES.intersection(deps):
            if candidate != root or {"start", "dev", "serve"}.intersection(scripts):
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


def sort_paths(paths: Sequence[Path]) -> List[Path]:
    return sorted(paths, key=lambda path: str(path).replace("\\", "/"))


def discover_documentation_inventory(root: Path) -> DocumentationInventory:
    agent_roots = sort_paths(
        [
            path
            for path in root.rglob("*")
            if path.is_dir() and path.name == "AGENTS"
        ]
    )
    root_agents_dir = root / "AGENTS"
    if root_agents_dir.is_dir() and root_agents_dir not in agent_roots:
        agent_roots.insert(0, root_agents_dir)

    flat_agent_files: List[Path] = []
    layered_agent_files: List[Path] = []
    root_agent_files: List[Path] = []
    archive_candidates: List[Path] = []

    for agent_root in agent_roots:
        files = sort_paths([path for path in agent_root.rglob("*") if path.is_file()])
        if agent_root == root_agents_dir:
            root_agent_files.extend(files)

        for path in files:
            try:
                rel = path.relative_to(agent_root)
            except ValueError:
                continue
            normalized = str(rel).replace("\\", "/")
            parts = rel.parts
            if len(parts) == 1 and rel.name in FLAT_AGENTS_FILENAMES:
                flat_agent_files.append(path)
                if agent_root == root_agents_dir:
                    archive_candidates.append(path)
            if parts and parts[0] in LAYERED_AGENTS_PREFIXES:
                layered_agent_files.append(path)

    canonical_agents_root: Optional[Path]
    if root_agents_dir.is_dir():
        canonical_agents_root = root_agents_dir
    elif len(agent_roots) == 1:
        canonical_agents_root = agent_roots[0]
    elif agent_roots:
        layered_roots = [
            agent_root
            for agent_root in agent_roots
            if any((agent_root / prefix).exists() for prefix in LAYERED_AGENTS_PREFIXES)
        ]
        canonical_agents_root = layered_roots[0] if layered_roots else agent_roots[0]
    else:
        canonical_agents_root = root_agents_dir

    supporting_patterns = [
        "README.md",
        "CLAUDE.md",
        "docs/**/*.md",
        "plan/**/*.md",
        "notes/**/*.md",
        "specs/**/*.md",
        "roadmap/**/*.md",
    ]
    supporting_docs = sort_paths(find_files(root, supporting_patterns, limit=20))
    reference_only_docs = []
    for path in supporting_docs:
        if root_agents_dir in path.parents:
            continue
        try:
            normalized = str(path.relative_to(root)).replace("\\", "/")
        except ValueError:
            normalized = str(path).replace("\\", "/")
        if normalized in GENERATED_HUMAN_DOC_PATHS:
            continue
        reference_only_docs.append(path)

    if layered_agent_files and flat_agent_files:
        detected_state = "migrate"
    elif layered_agent_files:
        detected_state = "refresh"
    elif flat_agent_files or agent_roots:
        detected_state = "migrate"
    else:
        detected_state = "initialize"

    return DocumentationInventory(
        canonical_agents_root=canonical_agents_root,
        detected_state=detected_state,
        agent_roots=agent_roots,
        flat_agent_files=sort_paths(flat_agent_files),
        layered_agent_files=sort_paths(layered_agent_files),
        root_agent_files=sort_paths(root_agent_files),
        supporting_docs=supporting_docs,
        archive_candidates=sort_paths(archive_candidates),
        reference_only_docs=sort_paths(reference_only_docs),
    )


def supporting_doc_roles(path: Path, root: Path) -> List[str]:
    normalized = str(path.relative_to(root)).replace("\\", "/").lower()
    roles: List[str] = []
    if normalized == "readme.md" or normalized.startswith("docs/product/") or normalized.startswith("specs/"):
        roles.append("product")
    if normalized == "readme.md":
        roles.append("execution")
        roles.append("architecture")
    if (
        normalized.startswith("docs/architecture/")
        or "/architecture/" in normalized
        or normalized.startswith("docs/adr")
        or "adr" in path.name.lower()
    ):
        roles.append("architecture")
    if (
        normalized.startswith("plan/")
        or normalized.startswith("roadmap/")
        or "runbook" in path.name.lower()
        or "quickstart" in path.name.lower()
        or "getting-started" in path.name.lower()
        or "platform" in path.name.lower()
    ):
        roles.append("execution")
    if any(token in normalized for token in ("progress", "lessons", "handoff", "status")):
        roles.append("memory")
    if not roles and normalized.startswith("docs/"):
        roles.append("product")
    return roles


def normalize_snippet_key(text: str) -> str:
    lowered = re.sub(r"[^a-z0-9\s]", " ", text.lower())
    tokens = [token for token in lowered.split() if len(token) >= 3]
    return " ".join(tokens[:8])


def clean_doc_line(line: str) -> str:
    line = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", line)
    line = line.replace("`", "")
    line = re.sub(r"\s+", " ", line.strip())
    return line.rstrip(" .")


def extract_supporting_doc_snippets(text: str) -> List[str]:
    snippets: List[str] = []
    in_code_block = False
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block or not stripped:
            continue

        candidate = ""
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            if len(heading.split()) >= 4:
                candidate = heading
        elif re.match(r"^[-*]\s+", stripped):
            candidate = re.sub(r"^[-*]\s+", "", stripped).strip()
        elif re.match(r"^\d+\.\s+", stripped):
            candidate = re.sub(r"^\d+\.\s+", "", stripped).strip()
        elif len(stripped) >= 24:
            candidate = stripped

        cleaned = clean_doc_line(candidate)
        if not cleaned:
            continue
        snippets.append(cleaned)
        if len(snippets) >= 12:
            break
    return snippets


def extract_execution_command_snippets(text: str) -> List[str]:
    commands: List[str] = []
    in_code_block = False
    code_lang = ""
    command_prefixes = (
        "docagent",
        "python",
        "python3",
        "pipx",
        "pip ",
        "npm",
        "pnpm",
        "yarn",
        "npx",
        "uv ",
        "pytest",
    )

    def add_command(raw: str) -> None:
        candidate = raw.strip()
        if candidate.startswith("$"):
            candidate = candidate[1:].strip()
        if not candidate:
            return
        if not any(candidate.startswith(prefix) for prefix in command_prefixes):
            return
        formatted = f"Run `{candidate}`"
        if formatted not in commands:
            commands.append(formatted)

    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_lang = stripped[3:].strip().lower()
            else:
                in_code_block = False
                code_lang = ""
            continue
        if not in_code_block:
            continue
        if code_lang and code_lang not in {"bash", "sh", "zsh", "shell", "console"}:
            continue
        add_command(stripped)
        if len(commands) >= 8:
            break

    if len(commands) < 8:
        for raw_line in text.splitlines():
            stripped = raw_line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            bullet = re.sub(r"^[-*]\s+", "", stripped).strip()
            bullet = re.sub(r"^\d+\.\s+", "", bullet).strip()
            if bullet.startswith("`") and bullet.endswith("`") and len(bullet) > 2:
                bullet = bullet[1:-1].strip()
            add_command(bullet)
            if len(commands) >= 8:
                break
    return commands


def extract_distribution_snippets(text: str, role: str) -> List[str]:
    snippets: List[str] = []
    role_tokens = {
        "product": ("human", "agent", "dual", "workflow", "users", "maintainer"),
        "architecture": ("platform", "adapter", "distribution", "cli", "entry", "python", "npm", "npx"),
    }
    shared_tokens = ("docagent", "codex", "claude", "continue", "copilot")
    tokens = role_tokens.get(role, ()) + shared_tokens
    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("```"):
            continue
        plain = re.sub(r"^[-*]\s+", "", stripped)
        lowered = plain.lower()
        if len(plain) < 20 or len(plain) > 180:
            continue
        if not any(token in lowered for token in tokens):
            continue
        cleaned = clean_doc_line(plain)
        if cleaned and cleaned not in snippets:
            snippets.append(cleaned)
        if len(snippets) >= 4:
            break
    return snippets


def summarize_sources(paths: Sequence[Path], root: Path) -> str:
    labels: List[str] = []
    for path in paths[:2]:
        relative = str(path.relative_to(root)).replace("\\", "/")
        labels.append(f"`{relative}`")
    if not labels:
        return ""
    if len(paths) > 2:
        return f"{', '.join(labels)} (+{len(paths) - 2} more)"
    return ", ".join(labels)


def synthesize_role_supporting_insights(root: Path, paths: Sequence[Path], role: str) -> Dict[str, List[str]]:
    confirmed_groups: Dict[str, Tuple[str, List[Path]]] = {}
    unresolved_groups: Dict[str, Tuple[str, List[Path]]] = {}
    explicit_conflicts: Dict[str, Tuple[str, List[Path]]] = {}
    aggregate_text = ""

    unresolved_pattern = re.compile(r"\b(todo|tbd|pending|open question|unresolved|confirm|decide)\b|\?", re.IGNORECASE)
    explicit_conflict_pattern = re.compile(r"\b(conflict|inconsistent|contradict|not aligned|vs\.?)\b", re.IGNORECASE)

    for path in paths:
        text = read_text(path)
        aggregate_text += "\n" + text.lower()
        primary_snippets: List[str] = []
        if role == "execution":
            primary_snippets.extend(extract_execution_command_snippets(text))
        if role in {"product", "architecture"}:
            primary_snippets.extend(extract_distribution_snippets(text, role))
        secondary_snippets = extract_supporting_doc_snippets(text)
        snippets = primary_snippets + secondary_snippets
        for snippet in snippets:
            key = normalize_snippet_key(snippet)
            if not key:
                continue

            target = confirmed_groups
            if unresolved_pattern.search(snippet):
                target = unresolved_groups
            elif explicit_conflict_pattern.search(snippet):
                target = explicit_conflicts

            if key not in target:
                target[key] = (snippet, [path])
            else:
                existing_text, existing_paths = target[key]
                if len(snippet) < len(existing_text):
                    existing_text = snippet
                if path not in existing_paths:
                    existing_paths.append(path)
                target[key] = (existing_text, existing_paths)

    conflicting: List[str] = []
    package_managers = sorted(set(re.findall(r"\b(npm|pnpm|yarn)\b", aggregate_text)))
    if len(package_managers) >= 2:
        conflicting.append(
            f"Supporting docs disagree on package manager ({', '.join(f'`{name}`' for name in package_managers)})."
        )
    runtimes = sorted(set(re.findall(r"\b(fastapi|flask|django|express|fastify|koa|nestjs)\b", aggregate_text)))
    if len(runtimes) >= 2:
        conflicting.append(
            f"Supporting docs disagree on runtime/framework ({', '.join(f'`{name}`' for name in runtimes)})."
        )

    for snippet, snippet_paths in explicit_conflicts.values():
        sources = summarize_sources(snippet_paths, root)
        conflicting.append(f"{snippet} (sources: {sources})" if sources else snippet)

    confirmed: List[str] = []
    for snippet, snippet_paths in confirmed_groups.values():
        sources = summarize_sources(snippet_paths, root)
        confirmed.append(f"{snippet} (sources: {sources})" if sources else snippet)

    unresolved: List[str] = []
    for snippet, snippet_paths in unresolved_groups.values():
        sources = summarize_sources(snippet_paths, root)
        unresolved.append(f"{snippet} (sources: {sources})" if sources else snippet)

    return {
        "confirmed": confirmed[:6],
        "conflicting": conflicting[:4],
        "unresolved": unresolved[:5],
    }


def synthesize_supporting_doc_insights(root: Path, docs_inventory: DocumentationInventory) -> Dict[str, Dict[str, List[str]]]:
    role_paths: Dict[str, List[Path]] = {
        "product": [],
        "architecture": [],
        "execution": [],
        "memory": [],
    }
    for path in docs_inventory.reference_only_docs:
        roles = supporting_doc_roles(path, root)
        for role in roles:
            role_paths[role].append(path)

    insights: Dict[str, Dict[str, List[str]]] = {}
    for role, paths in role_paths.items():
        insights[role] = synthesize_role_supporting_insights(root, sort_paths(paths), role)
    return insights


def synthesize_supporting_doc_provenance(root: Path, docs_inventory: DocumentationInventory) -> Dict[str, List[str]]:
    role_paths: Dict[str, List[str]] = {
        "product": [],
        "architecture": [],
        "execution": [],
        "memory": [],
    }
    for path in docs_inventory.reference_only_docs:
        try:
            normalized = str(path.relative_to(root)).replace("\\", "/")
        except ValueError:
            normalized = str(path).replace("\\", "/")
        for role in supporting_doc_roles(path, root):
            if normalized not in role_paths[role]:
                role_paths[role].append(normalized)
    return role_paths


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


def is_primary_skill_file(path: Optional[Path], root: Path) -> bool:
    if not path:
        return False
    try:
        rel = path.relative_to(root)
    except ValueError:
        return False
    return str(rel).replace("\\", "/") in {"SKILL.md", "skill.md", "doc-for-agent/SKILL.md"}


def is_primary_agent_manifest(path: Path, root: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return False
    if not parts:
        return False
    if len(parts) >= 2 and parts[0] == "agents":
        return True
    if len(parts) >= 3 and parts[0] == "doc-for-agent" and parts[1] == "agents":
        return True
    return False


def collect_repo_signals(
    root: Path,
    frontend_root: Optional[Path],
    backend_root: Optional[Path],
    cli_entrypoints: Sequence[Path],
    library_entrypoints: Sequence[Path],
    skill_meta: SkillMetadata,
) -> RepoSignals:
    top_level_dirs = list_top_level_dirs(root)
    package_json = root / "package.json"
    package = load_json(package_json) if package_json.exists() else {}
    deps = {
        **(package.get("dependencies") or {}),
        **(package.get("devDependencies") or {}),
    }
    dependency_names = sorted(str(key) for key in deps if isinstance(key, str))
    package_bin = package.get("bin")
    has_package_bin = isinstance(package_bin, str) or (
        isinstance(package_bin, dict) and any(isinstance(key, str) for key in package_bin)
    )

    has_workspace_config = any(
        (root / filename).exists() for filename in ("pnpm-workspace.yaml", "turbo.json", "nx.json", "lerna.json")
    )
    has_workspace_layout = bool({"packages", "apps"}.intersection(top_level_dirs)) or has_workspace_config
    if isinstance(package.get("workspaces"), list):
        has_workspace_layout = True

    has_skill_file = skill_meta.skill_file is not None
    has_agent_manifests = bool(skill_meta.agent_manifests)
    has_root_skill_markers = is_primary_skill_file(skill_meta.skill_file, root) or any(
        is_primary_agent_manifest(path, root) for path in skill_meta.agent_manifests
    )
    has_embedded_skill_markers = (has_skill_file or has_agent_manifests) and not has_root_skill_markers

    return RepoSignals(
        top_level_dirs=top_level_dirs,
        top_level_files=list_top_level_files(root),
        has_skill_file=has_skill_file,
        has_agent_manifests=has_agent_manifests,
        has_root_skill_markers=has_root_skill_markers,
        has_embedded_skill_markers=has_embedded_skill_markers,
        has_workspace_layout=has_workspace_layout,
        has_frontend=frontend_root is not None,
        has_backend=backend_root is not None,
        has_package_json=package_json.exists(),
        has_package_bin=has_package_bin,
        has_python_packaging=find_first_existing(root, ["pyproject.toml", "setup.py"]) is not None,
        package_name=str(package.get("name") or ""),
        package_dependencies=dependency_names,
        cli_entrypoints=list(cli_entrypoints),
        library_entrypoints=list(library_entrypoints),
    )


def append_unique(target: List[str], item: str) -> None:
    if item and item not in target:
        target.append(item)


def reduce_confidence(level: str, hard_conflicts: int, soft_conflicts: int = 0) -> str:
    levels = ["low", "medium", "high"]
    index = levels.index(level)
    penalty = min(hard_conflicts, 2)
    if soft_conflicts >= 2:
        penalty = min(2, penalty + 1)
    return levels[max(0, index - penalty)]


def classify_repo(signals: RepoSignals) -> RepoClassification:
    reasons: List[str] = []
    secondary_traits: List[str] = []
    conflicting_signals: List[str] = []
    open_questions: List[str] = []
    primary_type = "unknown"
    confidence = "low"
    hard_conflicts = 0
    soft_conflicts = 0

    def add_conflict(message: str, severity: str = "hard") -> None:
        nonlocal hard_conflicts, soft_conflicts
        if message in conflicting_signals:
            return
        conflicting_signals.append(message)
        if severity == "soft":
            soft_conflicts += 1
        else:
            hard_conflicts += 1

    build_like_deps = {"typescript", "tsup", "rollup", "vite"}
    has_build_deps = bool(build_like_deps.intersection(signals.package_dependencies))
    has_skill_markers = signals.has_skill_file or signals.has_agent_manifests
    has_packaged_distribution = signals.has_package_json or signals.has_python_packaging
    has_primary_skill_markers = signals.has_root_skill_markers
    has_strong_application_envelope = signals.has_workspace_layout or (signals.has_frontend and signals.has_backend)

    if has_skill_markers and (has_primary_skill_markers or not has_strong_application_envelope):
        primary_type = "skill-meta"
        confidence = "high"
        reasons.append("Skill markers detected (`SKILL.md`, agent manifests, or an existing `AGENTS/` directory).")
        if signals.has_embedded_skill_markers and not has_primary_skill_markers:
            reasons.append("Skill markers were detected in nested directories and no stronger app envelope was detected.")
        if signals.cli_entrypoints:
            append_unique(secondary_traits, "CLI distribution surface is also present.")
        if signals.has_package_json:
            append_unique(secondary_traits, "JavaScript package/distribution metadata is also present.")
        if signals.has_python_packaging:
            append_unique(secondary_traits, "Python packaging metadata is also present.")
        if signals.library_entrypoints:
            append_unique(secondary_traits, "Library-style entrypoints are also present.")
        if signals.has_workspace_layout:
            append_unique(secondary_traits, "Workspace/monorepo layout is also present.")
        if signals.cli_entrypoints or has_packaged_distribution:
            add_conflict(
                "Skill markers dominate classification, but packaged tooling signals suggest this repository may also ship installable utilities."
            )
    elif signals.has_workspace_layout:
        primary_type = "monorepo"
        confidence = "high"
        reasons.append("Workspace-style directories or pnpm workspace config detected.")
        if signals.has_frontend:
            append_unique(secondary_traits, "Frontend application signals are also present.")
        if signals.has_backend:
            append_unique(secondary_traits, "Backend service signals are also present.")
        if signals.cli_entrypoints:
            append_unique(secondary_traits, "CLI tooling is also present.")
        if signals.has_package_json:
            append_unique(secondary_traits, "Package/distribution metadata is also present.")
        if has_skill_markers:
            append_unique(secondary_traits, "Embedded skill metadata is also present.")
            if has_primary_skill_markers:
                add_conflict(
                    "Root-level skill markers exist alongside workspace signals; confirm whether this repository is primarily a skill package or an application monorepo.",
                    severity="soft",
                )
    elif (signals.cli_entrypoints or signals.has_package_bin) and has_packaged_distribution and not has_strong_application_envelope:
        primary_type = "cli-tool"
        confidence = "high"
        if signals.cli_entrypoints and signals.has_package_bin:
            reasons.append("CLI-like entrypoints and package `bin` metadata were detected.")
        elif signals.cli_entrypoints:
            reasons.append("CLI-like entrypoints detected in `bin/` or `cli/`.")
        else:
            reasons.append("Package `bin` metadata indicates a CLI distribution surface.")
        if signals.has_package_json:
            append_unique(secondary_traits, "JavaScript package/distribution metadata is also present.")
        if signals.has_python_packaging:
            append_unique(secondary_traits, "Python packaging metadata is also present.")
        if signals.library_entrypoints:
            append_unique(secondary_traits, "Library-style entrypoints are also present.")
        if signals.has_frontend:
            add_conflict(
                "Frontend application signals exist alongside CLI entrypoints; confirm whether the CLI is the primary user surface."
            )
        if signals.has_backend:
            add_conflict(
                "Backend service signals exist alongside CLI entrypoints; confirm whether the CLI is the primary user surface."
            )
    elif signals.cli_entrypoints:
        reasons.append("CLI-like entrypoints detected in `bin/` or `cli/`.")
        open_questions.append(
            "CLI-like entrypoints were found without clear package metadata; confirm whether command files are examples, fixtures, or the primary product surface."
        )

    if primary_type == "unknown" and signals.has_frontend and signals.has_backend:
        primary_type = "web-app"
        confidence = "high"
        reasons.append("Both frontend and backend roots were detected.")
        if signals.cli_entrypoints or signals.has_package_bin:
            append_unique(secondary_traits, "CLI distribution surface is also present.")
        if signals.has_package_json:
            append_unique(secondary_traits, "JavaScript package/distribution metadata is also present.")
        if signals.has_python_packaging:
            append_unique(secondary_traits, "Python packaging metadata is also present.")
        if has_skill_markers:
            append_unique(secondary_traits, "Embedded skill metadata is also present.")
            if has_primary_skill_markers:
                add_conflict(
                    "Root-level skill markers exist alongside web-app signals; confirm whether this repository is primarily a skill package or an application.",
                    severity="soft",
                )

    if primary_type == "unknown" and signals.has_backend and not signals.has_frontend:
        primary_type = "backend-service"
        confidence = "medium"
        reasons.append("Backend-like Python service structure detected without a separate frontend.")
        if signals.cli_entrypoints or signals.has_package_bin:
            append_unique(secondary_traits, "CLI distribution surface is also present.")
        if signals.has_python_packaging:
            append_unique(secondary_traits, "Python packaging metadata is also present.")

    if primary_type == "unknown" and signals.has_package_json and not signals.has_frontend and not signals.has_backend:
        if has_build_deps or signals.library_entrypoints:
            primary_type = "library-sdk"
            confidence = "medium"
            reasons.append("Package manifest suggests a library or tool package.")
            if signals.cli_entrypoints:
                append_unique(secondary_traits, "CLI distribution surface is also present.")
            if signals.has_python_packaging:
                add_conflict(
                    "Both JavaScript and Python packaging metadata are present; confirm which install surface is canonical."
                )
        elif signals.package_name:
            open_questions.append(
                f"Package `{signals.package_name}` was detected, but repository type still needs human confirmation."
            )

    if primary_type == "unknown" and signals.has_python_packaging and not signals.has_backend:
        primary_type = "library-sdk"
        confidence = "medium"
        reasons.append("Python packaging files detected without service-style app layout.")
        if signals.cli_entrypoints:
            append_unique(secondary_traits, "CLI distribution surface is also present.")

    if primary_type == "unknown" and has_skill_markers:
        primary_type = "skill-meta"
        confidence = "medium"
        reasons.append("Skill markers were detected, but the repository shape remained ambiguous.")

    if primary_type == "unknown" and signals.top_level_files:
        open_questions.append(
            "Repository shape was not strongly classified; confirm whether this is an app, library, or tooling repo."
        )

    confidence = reduce_confidence(confidence, hard_conflicts=hard_conflicts, soft_conflicts=soft_conflicts)

    return RepoClassification(
        primary_type=primary_type,
        confidence=confidence,
        reasons=reasons,
        secondary_traits=secondary_traits,
        conflicting_signals=conflicting_signals,
        open_questions=open_questions,
    )


def apply_repo_type_override(
    classification: RepoClassification,
    forced_primary_type: Optional[str],
) -> RepoClassification:
    if not forced_primary_type:
        return classification

    reasons = [f"Repo type overridden via CLI: `{forced_primary_type}`."]
    reasons.extend(classification.reasons)

    conflicting_signals = list(classification.conflicting_signals)
    if classification.primary_type != forced_primary_type:
        conflicting_signals.insert(
            0,
            f"Automatic classification would have selected `{classification.primary_type}` instead.",
        )

    return RepoClassification(
        primary_type=forced_primary_type,
        confidence="high",
        reasons=reasons,
        secondary_traits=list(classification.secondary_traits),
        conflicting_signals=conflicting_signals,
        open_questions=list(classification.open_questions),
    )


def detect_repo_type(
    root: Path,
    frontend_root: Optional[Path],
    backend_root: Optional[Path],
    cli_entrypoints: Sequence[Path],
) -> Tuple[str, List[str], List[str]]:
    skill_meta = detect_skill_metadata(root)
    signals = collect_repo_signals(
        root,
        frontend_root,
        backend_root,
        cli_entrypoints,
        detect_library_entrypoints(root),
        skill_meta,
    )
    classification = classify_repo(signals)
    return (
        classification.primary_type,
        classification.reasons,
        classification.open_questions,
    )


def analyze_repo(
    root: Path,
    project_name: str,
    repo_type_override: Optional[str] = None,
    doc_profile: str = "bootstrap",
) -> RepoAnalysis:
    frontend_root = detect_frontend_root(root)
    backend_root = detect_backend_root(root)
    cli_entrypoints = detect_cli_entrypoints(root)
    library_entrypoints = detect_library_entrypoints(root)
    skill_meta = detect_skill_metadata(root)
    signals = collect_repo_signals(
        root,
        frontend_root,
        backend_root,
        cli_entrypoints,
        library_entrypoints,
        skill_meta,
    )
    classification = apply_repo_type_override(
        classify_repo(signals),
        repo_type_override,
    )

    summary = extract_readme_summary(root)
    package_manager = detect_package_manager(frontend_root, root)
    frontend_stack, routes, components, frontend_scripts = describe_frontend(frontend_root)
    backend_stack, endpoints, storage_rules = detect_backend_stack(backend_root)
    docs_inventory = discover_documentation_inventory(root)
    supporting_doc_insights = synthesize_supporting_doc_insights(root, docs_inventory)
    supporting_doc_provenance = synthesize_supporting_doc_provenance(root, docs_inventory)

    return RepoAnalysis(
        root=root,
        project_name=project_name,
        repo_type=classification.primary_type,
        doc_profile=doc_profile,
        repo_type_reasons=classification.reasons,
        repo_type_questions=classification.open_questions,
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
        skill_meta=skill_meta,
        library_entrypoints=library_entrypoints,
        cli_entrypoints=cli_entrypoints,
        signals=signals,
        classification=classification,
        docs_inventory=docs_inventory,
        supporting_doc_insights=supporting_doc_insights,
        supporting_doc_provenance=supporting_doc_provenance,
    )
