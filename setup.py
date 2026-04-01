from setuptools import find_packages, setup

# The version is managed across multiple files. Keep synced with:
# - package.json
# - doc-for-agent/package.json
# - doc-for-agent/templates/product.json
# - doc-for-agent/INSTALLATION.json
VERSION = "0.3.0.dev1"

setup(
    name="doc-for-agent",
    version=VERSION,
    author="Timcai06",
    description="Unified docagent CLI for Claude/Codex/CodeBuddy-style terminal agent workflows.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Timcai06/Doc-For-Agent-skill",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "click",
        "requests",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "docagent-py=doc_for_agent.installer.docagent:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
