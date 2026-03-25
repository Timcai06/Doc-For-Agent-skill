from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass(frozen=True)
class SkillMetadata:
    skill_file: Optional[Path] = None
    skill_name: str = ""
    agent_manifests: List[Path] = field(default_factory=list)
    references: List[Path] = field(default_factory=list)
    scripts: List[Path] = field(default_factory=list)


@dataclass(frozen=True)
class RepoAnalysis:
    root: Path
    project_name: str
    repo_type: str
    repo_type_reasons: List[str] = field(default_factory=list)
    repo_type_questions: List[str] = field(default_factory=list)
    summary: str = ""
    frontend_root: Optional[Path] = None
    backend_root: Optional[Path] = None
    package_manager: str = "npm"
    frontend_stack: str = "No dedicated frontend detected."
    routes: List[str] = field(default_factory=list)
    components: List[str] = field(default_factory=list)
    frontend_scripts: Dict[str, str] = field(default_factory=dict)
    backend_stack: str = "No dedicated backend detected."
    endpoints: List[str] = field(default_factory=list)
    storage_rules: List[str] = field(default_factory=list)
    script_files: List[str] = field(default_factory=list)
    glossary_entries: List[str] = field(default_factory=list)
    contract_fields: List[str] = field(default_factory=list)
    skill_meta: SkillMetadata = field(default_factory=SkillMetadata)
    library_entrypoints: List[Path] = field(default_factory=list)
    cli_entrypoints: List[Path] = field(default_factory=list)
