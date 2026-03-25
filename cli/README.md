# doc-for-agent CLI

Minimal installer and maintenance CLI for the platformized `doc-for-agent` skill repo.

## Commands

### Install into Codex

```bash
python3 cli/docforagent.py init --ai codex
```

Default install path:

```text
~/.codex/skills/doc-for-agent
```

### Install into Claude-style project skills

From the target project directory:

```bash
python3 /path/to/DocForAgent_skill/cli/docforagent.py init --ai claude
```

Default install path:

```text
<current-working-directory>/.claude/skills/doc-for-agent
```

### Install into Cursor / Continue / Windsurf

From the target project directory:

```bash
python3 /path/to/DocForAgent_skill/cli/docforagent.py init --ai cursor
python3 /path/to/DocForAgent_skill/cli/docforagent.py init --ai continue
python3 /path/to/DocForAgent_skill/cli/docforagent.py init --ai windsurf
```

Default install paths:

```text
<current-working-directory>/.cursor/skills/doc-for-agent
<current-working-directory>/.continue/skills/doc-for-agent
<current-working-directory>/.windsurf/skills/doc-for-agent
```

### Install both adapters

```bash
python3 cli/docforagent.py init --ai all
```

### Override destination

```bash
python3 cli/docforagent.py init --ai codex --dest /custom/path/doc-for-agent
```

### Sync adapter copies from source-of-truth

```bash
python3 cli/docforagent.py sync
```

### Check repository health

```bash
python3 cli/docforagent.py doctor
```

## pipx Installation

You can also install the CLI itself as a Python package:

```bash
pipx install /path/to/DocForAgent_skill
docforagent doctor
```

## Notes

- The source of truth lives under `src/doc_for_agent/`.
- `sync` updates all platform adapter copies from the source of truth.
- `init` copies an adapter package into the target environment; it does not create symlinks.
