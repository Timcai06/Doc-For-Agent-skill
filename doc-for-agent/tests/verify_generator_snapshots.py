#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


DEFAULT_REQUIRED_DOCS = [
    "README.md",
    "product.md",
    "architecture.md",
    "frontend.md",
    "backend.md",
    "workflows.md",
    "glossary.md",
]
DEFAULT_HUMAN_REQUIRED_DOCS = [
    "dfa-doc/handbook/overview.md",
    "dfa-doc/handbook/architecture.md",
    "dfa-doc/handbook/workflows.md",
    "dfa-doc/handbook/glossary.md",
]

MANUAL_START = "<!-- doc-for-agent:manual-start -->"
MANUAL_END = "<!-- doc-for-agent:manual-end -->"


def run_generator(generator: Path, root: Path, mode: str, profile: str = "bootstrap", output_mode: str = "agent") -> None:
    subprocess.run(
        [
            sys.executable,
            str(generator),
            "--root",
            str(root),
            "--mode",
            mode,
            "--profile",
            profile,
            "--output-mode",
            output_mode,
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def verify_fixture(generator: Path, fixture_root: Path, expectations: dict) -> list[str]:
    failures: list[str] = []
    profile = expectations.get("__profile", "bootstrap")
    output_mode = expectations.get("__output_mode", "agent")
    if output_mode == "human":
        default_required = DEFAULT_HUMAN_REQUIRED_DOCS
    elif output_mode == "dual":
        default_required = DEFAULT_REQUIRED_DOCS + DEFAULT_HUMAN_REQUIRED_DOCS
    else:
        default_required = DEFAULT_REQUIRED_DOCS
    required_docs = expectations.get("__required_docs", default_required)

    def resolve_generated_path(path: str) -> str:
        normalized = path.replace("\\", "/")
        if normalized.startswith("dfa-doc/AGENTS/") or normalized.startswith("dfa-doc/handbook/"):
            return normalized
        if output_mode in {"agent", "dual"}:
            return f"dfa-doc/AGENTS/{normalized}"
        return normalized

    with tempfile.TemporaryDirectory(prefix="doc-for-agent-fixture-") as tmpdir:
        sandbox_root = Path(tmpdir) / fixture_root.name
        shutil.copytree(fixture_root, sandbox_root)

        run_generator(generator, sandbox_root, "init", profile=profile, output_mode=output_mode)

        for filename in required_docs:
            generated_rel = resolve_generated_path(filename)
            if not (sandbox_root / generated_rel).exists():
                failures.append(f"{fixture_root.name}: missing {generated_rel}")

        outputs_after_init = {
            resolve_generated_path(filename): read_text(sandbox_root / resolve_generated_path(filename))
            for filename in required_docs
            if (sandbox_root / resolve_generated_path(filename)).exists()
        }

        run_generator(generator, sandbox_root, "refresh", profile=profile, output_mode=output_mode)
        outputs_after_refresh = {
            resolve_generated_path(filename): read_text(sandbox_root / resolve_generated_path(filename))
            for filename in required_docs
            if (sandbox_root / resolve_generated_path(filename)).exists()
        }

        if outputs_after_init != outputs_after_refresh:
            failures.append(f"{fixture_root.name}: refresh output was not idempotent after init")

        for filename, checks in expectations.items():
            if filename.startswith("__"):
                continue
            generated_rel = resolve_generated_path(filename)
            content = outputs_after_refresh.get(generated_rel)
            if content is None:
                failures.append(f"{fixture_root.name}: expected file {generated_rel} was not generated")
                continue

            for needle in checks.get("contains", []):
                if needle not in content:
                    failures.append(f"{fixture_root.name}: {filename} missing expected text: {needle}")

            for needle in checks.get("absent", []):
                if needle in content:
                    failures.append(f"{fixture_root.name}: {filename} unexpectedly contained: {needle}")

    return failures


def verify_manual_preservation(generator: Path, fixture_root: Path) -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory(prefix="doc-for-agent-manual-") as tmpdir:
        sandbox_root = Path(tmpdir) / fixture_root.name
        shutil.copytree(fixture_root, sandbox_root)

        run_generator(generator, sandbox_root, "init")

        product_path = sandbox_root / "dfa-doc" / "AGENTS" / "product.md"
        original = read_text(product_path)
        marker = "\n".join(
            [
                MANUAL_START,
                "- Human-maintained: keep the success metric tied to deployment confidence.",
                MANUAL_END,
            ]
        )
        product_path.write_text(original.rstrip() + "\n\n" + marker + "\n", encoding="utf-8")

        run_generator(generator, sandbox_root, "refresh")
        refreshed = read_text(product_path)
        if marker not in refreshed:
            failures.append("manual-preservation: explicit manual block was not preserved across refresh")

    return failures


def main() -> int:
    repo_root = Path(__file__).resolve().parents[2]
    generator = repo_root / "doc-for-agent/scripts/init_agents_docs.py"
    fixtures_root = repo_root / "doc-for-agent/tests/fixtures"
    snapshots_path = repo_root / "doc-for-agent/tests/snapshots.json"

    expectations = json.loads(read_text(snapshots_path))
    failures: list[str] = []

    for fixture_name, checks in sorted(expectations.items()):
        fixture_root = fixtures_root / fixture_name
        if not fixture_root.exists():
            failures.append(f"{fixture_name}: fixture directory is missing")
            continue
        failures.extend(verify_fixture(generator, fixture_root, checks))

    preservation_fixture = fixtures_root / "cli_tool"
    if preservation_fixture.exists():
        failures.extend(verify_manual_preservation(generator, preservation_fixture))
    else:
        failures.append("manual-preservation: cli_tool fixture directory is missing")

    if failures:
        print("Snapshot verification failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(f"Verified {len(expectations)} fixtures successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
