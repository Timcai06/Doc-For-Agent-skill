---
name: sync-doc-for-agent
description: Analyzes repository structure to generate and synchronize dual-language (English/Chinese) documentation for AI agents and human maintainers. Use this when the user asks to refresh docs, update the AGENTS directory, or sync docs after code changes.
---
# doc-for-agent

You are equipped with the `doc-for-agent` documentation engine, a system designed to maintain Quad-View documentation (Agent & Human, English & Chinese) for this repository.

When the user asks you to initialize, refresh, or sync documentation, follow these strict orchestration steps:

## Step 1: Run Fact Extraction and Base Generation

Execute the CLI tool to perform AST scanning, route detection, and baseline fact generation. The tool defaults to outputting the complete `quad` view.

```bash
docagent refresh
```

*Note: If `docagent` is not found globally, try `npx -y doc-for-agent refresh` or fall back to `python3 doc-for-agent/installer/assets/installer/docagent.py refresh`.*

## Step 2: Intelligent Quad-View Synchronization

The `docagent refresh` tool will generate or update standard Markdown files in four directories:
- `AGENTS/` (English Agent Docs)
- `AGENTS.zh/` (Chinese Agent Docs)
- `human/` (English Human Docs)
- `human.zh/` (Chinese Human Docs)

Your critical job is to elevate these standard text templates by applying your deep LLM understanding of the repository.
1. Review the generated core files, starting with `AGENTS/001-core-goals.md` and `AGENTS.zh/001-core-goals.md`.
2. Ensure the Chinese translation in the `.zh` folders is native, highly professional, and accurate to the current codebase. The tool provides a good baseline, but you must ensure it does not contain awkward "mixed English/Chinese" artifacts.
3. If you find any hardcoded English artifacts or suboptimal literal translations in the Chinese directories, **explicitly rewrite those files** using your file editing tools to be 100% native Chinese.

## Step 3: Protect Manual Knowledge

If you are modifying established Markdown files, never remove or overwrite content wrapped in `<!-- doc-for-agent:manual-start -->` and `<!-- doc-for-agent:manual-end -->` blocks. These notes are manually maintained by human operators.

## Step 4: Report Status

After creating or refreshing the files, and performing your language refinement pass, provide the user with a concise summary of the files updated. Mention specifically if you improved any of the Chinese baseline text.
