from __future__ import annotations

from setuptools import setup


setup(
    name="doc-for-agent",
    version="0.2.0.dev0",
    description="Installable product surface for doc-for-agent platform adapters and AGENTS generation.",
    python_requires=">=3.9",
    package_dir={"": "doc-for-agent"},
    packages=["installer"],
    include_package_data=True,
    package_data={"installer": ["assets/**/*"]},
    entry_points={"console_scripts": ["docagent=installer.docagent:cli"]},
)
