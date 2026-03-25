#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    version_path = repo_root / "src/doc_for_agent/version.py"
    package_json_path = repo_root / "cli/package.json"
    changelog_path = repo_root / "CHANGELOG.md"

    version_text = read_text(version_path)
    match = re.search(r'__version__\s*=\s*"([^"]+)"', version_text)
    if not match:
        print("Failed: could not read __version__ from src/doc_for_agent/version.py")
        return 1
    version = match.group(1)

    package_json = json.loads(read_text(package_json_path))
    package_version = str(package_json.get("version", "")).strip()
    if package_version != version:
        print(f"Failed: cli/package.json version {package_version!r} does not match source version {version!r}")
        return 1

    changelog_text = read_text(changelog_path)
    if f"## [{version}]" not in changelog_text:
        print(f"Failed: CHANGELOG.md is missing a section for version {version}")
        return 1

    print(f"Product metadata verified for version {version}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
