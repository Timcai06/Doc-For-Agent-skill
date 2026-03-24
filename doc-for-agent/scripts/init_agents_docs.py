#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def write_file(path: Path, content: str) -> None:
    path.write_text(content.strip() + "\n", encoding="utf-8")


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


def first_nonempty_line(lines: Sequence[str]) -> str:
    for line in lines:
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


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


def detect_frontend_root(root: Path) -> Optional[Path]:
    candidates = [
        root / "frontend",
        root,
    ]
    for candidate in candidates:
        package_json = candidate / "package.json"
        if package_json.exists():
            return candidate
    return None


def detect_backend_root(root: Path) -> Optional[Path]:
    candidates = [
        root / "backend",
        root,
    ]
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
        candidates.extend([
            frontend_root / "pnpm-lock.yaml",
            frontend_root / "yarn.lock",
            frontend_root / "package-lock.json",
        ])
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
        return ("未检测到独立前端目录。", [], [], {})

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
    if not stack_parts:
        stack_parts.append("已检测到前端 package.json，但未识别出常见框架")

    route_root = find_first_existing(frontend_root, ["app", "src/app", "pages", "src/pages"])
    routes = detect_routes(route_root, frontend_root) if route_root else []

    component_root = find_first_existing(frontend_root, ["src/components", "components"])
    components = []
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
        return ("未检测到独立后端目录。", [], [])

    stack_parts: List[str] = []
    requirements = read_text(backend_root / "requirements.txt") + "\n" + read_text(backend_root / "requirements-dev.txt")
    if "fastapi" in requirements.lower():
        stack_parts.append("FastAPI")
    if "uvicorn" in requirements.lower():
        stack_parts.append("Uvicorn")
    if "ultralytics" in requirements.lower():
        stack_parts.append("ultralytics")
    if "torch" in requirements.lower():
        stack_parts.append("PyTorch")
    if (backend_root / "pyproject.toml").exists():
        pyproject = read_text(backend_root / "pyproject.toml").lower()
        if "fastapi" in pyproject and "FastAPI" not in stack_parts:
            stack_parts.append("FastAPI")

    endpoints = detect_backend_endpoints(backend_root)
    storage_rules = detect_storage_rules(backend_root)
    if not stack_parts:
        stack_parts.append("已检测到后端目录，但未识别出常见框架")
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
        rules.append("使用本地文件产物存储结果、上传图、结果图与诊断文本。")
    result_service = backend_root / "app/services/result_service.py"
    result_text = read_text(result_service)
    if "history-" in result_text and "zip" in result_text:
        rules.append("支持历史记录批量导出压缩包。")
    mapper = backend_root / "app/core/category_mapper.py"
    if mapper.exists():
        rules.append("后端会先执行类别标准化映射，再返回前端。")
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
    if not entries:
        entries.append("- TODO: add canonical domain terms from the repository")
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


def build_readme(project_name: str) -> str:
    return f"""# AGENTS

This directory contains agent-facing project docs for `{project_name}`.

Files:

- `product.md`: product purpose, users, and key flows
- `architecture.md`: system structure and data flow
- `frontend.md`: frontend routes, components, and UI semantics
- `backend.md`: backend services, contracts, and storage rules
- `workflows.md`: install, run, lint, test, and build commands
- `glossary.md`: project-specific terminology and canonical labels
"""


def build_product(project_name: str, summary: str, routes: Sequence[str]) -> str:
    route_lines = "\n".join(f"- `{route}`" for route in routes[:8]) if routes else "- TODO: identify user-facing routes"
    summary_line = summary or "TODO: summarize the product based on the repository README and current app behavior."
    return f"""# Product

## Summary

- {summary_line}

## Current User-Facing Entry Points

{route_lines}

## Users

- TODO: list primary users based on the actual product and domain

## Primary Flows

- TODO: upload / create / inspect flow
- TODO: history / review / export flow
- TODO: model selection / comparison flow if applicable

## Output Expectations

- TODO: describe the outputs users actually rely on
"""


def build_architecture(repo_root: Path, frontend_root: Optional[Path], backend_root: Optional[Path], storage_rules: Sequence[str]) -> str:
    frontend_desc = str(frontend_root.relative_to(repo_root)) if frontend_root and frontend_root != repo_root else ("repo root" if frontend_root else "未检测到")
    backend_desc = str(backend_root.relative_to(repo_root)) if backend_root and backend_root != repo_root else ("repo root" if backend_root else "未检测到")
    storage_lines = "\n".join(f"- {rule}" for rule in storage_rules) if storage_rules else "- TODO: describe storage and persistence behavior"
    return f"""# Architecture

## System Shape

- Repository root: `{repo_root}`
- Frontend root: `{frontend_desc}`
- Backend root: `{backend_desc}`

## Main Parts

- Frontend: handles user entry, result views, history, and client-side interactions
- Backend: handles inference orchestration, result normalization, export, and persistence
- Storage:
{storage_lines}

## Data / Result Flow

1. User enters from the frontend and submits input
2. Backend runs processing or inference and normalizes the response contract
3. Results, artifacts, and history records are persisted and exposed for later review

## Constraints

- Keep this file aligned with real routes, storage, and output contract behavior
- Prefer describing current behavior over planned architecture
"""


def build_frontend(stack: str, routes: Sequence[str], components: Sequence[str]) -> str:
    route_lines = "\n".join(f"- `{route}`" for route in routes) if routes else "- 未检测到明确的前端 page 路由"
    component_lines = "\n".join(f"- `{component}`" for component in components) if components else "- TODO: identify the core UI components"
    return f"""# Frontend

## Stack

- {stack}

## Routes

{route_lines}

## Key Components

{component_lines}

## UI Semantics

- Record view semantics that must stay stable, especially result views, history views, and export language
- Note which screens are primary workflows versus supporting flows

## Frontend Constraints

- Keep route, state, and result-view language aligned with the actual codebase
- Prefer canonical labels over model raw output when the project normalizes categories
"""


def build_backend(stack: str, endpoints: Sequence[str], storage_rules: Sequence[str], contract_fields: Sequence[str]) -> str:
    endpoint_lines = "\n".join(f"- `{endpoint}`" for endpoint in endpoints) if endpoints else "- TODO: identify actual API endpoints"
    storage_lines = "\n".join(f"- {rule}" for rule in storage_rules) if storage_rules else "- TODO: describe actual storage behavior"
    contract_lines = "\n".join(contract_fields) if contract_fields else "- TODO: list critical result contract fields"
    return f"""# Backend

## Stack

- {stack}

## Main Services / Endpoints

{endpoint_lines}

## API / Result Contract

Important fields currently detected:

{contract_lines}

## Storage Rules

{storage_lines}

## Backend Constraints

- Keep response fields and category semantics stable for the frontend
- Prefer documenting real environment and compatibility constraints here
"""


def build_workflows(repo_root: Path, package_manager: str, frontend_root: Optional[Path], frontend_scripts: Dict[str, str], backend_root: Optional[Path], script_files: Sequence[str]) -> str:
    setup_lines: List[str] = []
    run_lines: List[str] = []
    verify_lines: List[str] = []

    if frontend_root:
        frontend_prefix = f"cd {frontend_root.relative_to(repo_root)}" if frontend_root != repo_root else "# already at repo root"
        install_cmd = {"npm": "npm install", "pnpm": "pnpm install", "yarn": "yarn install"}.get(package_manager, "npm install")
        setup_lines.extend([frontend_prefix, install_cmd])
        for key in ("dev",):
            if key in frontend_scripts:
                run_lines.extend([frontend_prefix, f"{package_manager} run {key}" if package_manager != "yarn" else f"yarn {key}"])
        for key in ("lint", "test", "build"):
            if key in frontend_scripts:
                verify_lines.extend([frontend_prefix, f"{package_manager} run {key}" if package_manager != "yarn" else f"yarn {key}"])

    if backend_root:
        backend_prefix = f"cd {backend_root.relative_to(repo_root)}" if backend_root != repo_root else "# backend at repo root"
        requirements = []
        if (backend_root / "requirements-dev.txt").exists():
            requirements.append("python3 -m pip install -r requirements-dev.txt")
        elif (backend_root / "requirements.txt").exists():
            requirements.append("python3 -m pip install -r requirements.txt")
        if requirements:
            setup_lines.extend([backend_prefix, *requirements])
        if (backend_root / "app").exists():
            run_lines.extend([backend_prefix, "uvicorn app.main:app --reload"])

    if script_files:
        run_lines.extend(f"./{script}" for script in script_files[:6])

    if not setup_lines:
        setup_lines = ["# TODO: add repository setup commands"]
    if not run_lines:
        run_lines = ["# TODO: add local run commands"]
    if not verify_lines:
        verify_lines = ["# TODO: add lint / test / build commands"]

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

## Notes

- Refresh this file whenever scripts, package manager, or service entry points change
"""


def build_glossary(entries: Sequence[str]) -> str:
    glossary_entries = "\n".join(entries)
    return f"""# Glossary

## Canonical Terms

{glossary_entries}

## Naming Rules

- Prefer canonical domain labels in docs and UI over legacy aliases
- If the backend normalizes labels, document the normalized values here first

## Terms To Avoid

- Avoid ambiguous synonyms when the project already has canonical names
- Avoid mixing raw model labels with product-facing labels unless both are explicitly documented
"""


def generate_docs(root: Path, project_name: str) -> Dict[str, str]:
    frontend_root = detect_frontend_root(root)
    backend_root = detect_backend_root(root)
    summary = extract_readme_summary(root)
    package_manager = detect_package_manager(frontend_root, root)
    frontend_stack, routes, components, frontend_scripts = describe_frontend(frontend_root)
    backend_stack, endpoints, storage_rules = detect_backend_stack(backend_root)
    script_files = detect_scripts(root)
    glossary_entries = detect_glossary(root)
    contract_fields = detect_result_contract(root)

    return {
        "README.md": build_readme(project_name),
        "product.md": build_product(project_name, summary, routes),
        "architecture.md": build_architecture(root, frontend_root, backend_root, storage_rules),
        "frontend.md": build_frontend(frontend_stack, routes, components),
        "backend.md": build_backend(backend_stack, endpoints, storage_rules, contract_fields),
        "workflows.md": build_workflows(root, package_manager, frontend_root, frontend_scripts, backend_root, script_files),
        "glossary.md": build_glossary(glossary_entries),
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
        write_file(agents_dir / name, content)

    print(f"{args.mode.capitalize()}ed AGENTS docs in: {agents_dir}")


if __name__ == "__main__":
    main()
