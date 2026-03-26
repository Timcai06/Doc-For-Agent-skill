#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path


def main() -> None:
    installer_root = Path(__file__).resolve().parent
    skill_root = installer_root.parent
    assets_root = installer_root / "assets"
    assets_root.mkdir(parents=True, exist_ok=True)

    # Source-of-truth folders that the packaged installer needs at runtime.
    for directory_name in ("scripts", "templates", "references", "agents"):
        source = skill_root / directory_name
        target = assets_root / directory_name
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)

    installer_target = assets_root / "installer"
    installer_target.mkdir(parents=True, exist_ok=True)
    for filename in ("__init__.py", "__main__.py", "docagent.py"):
        shutil.copy2(installer_root / filename, installer_target / filename)

    node_target = installer_target / "node"
    node_target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(installer_root / "node" / "docagent.js", node_target / "docagent.js")

    print(f"Synchronized installer runtime assets in: {assets_root}")


if __name__ == "__main__":
    main()
