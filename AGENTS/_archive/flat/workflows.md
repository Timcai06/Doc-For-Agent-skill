# Workflows

## Best Used For

- Getting an agent from zero context to runnable context quickly
- Running the minimum commands needed to inspect or validate changes
- Refreshing agent docs after the repository shape changes

## Setup

```bash
# skill repositories are usually installed by symlink or copied into a local skills directory
```

## Run

```bash
python3 doc-for-agent/scripts/init_agents_docs.py --root /path/to/target-repo --mode refresh
```

## Verify

```bash
python3 -m unittest discover -s doc-for-agent/tests/unit -p 'test_*.py'
python3 doc-for-agent/tests/verify_generator_snapshots.py
```

## Refresh / Handoff Notes

- python3 doc-for-agent/scripts/init_agents_docs.py --root /Users/tim/DocForAgent_skill --mode refresh
- Review generated `AGENTS/*.md` files and tighten any sections still marked as needing human confirmation.

## Codex App Team Pattern

- Keep one Codex app window on `main` for integration only.
- Use one dedicated `git worktree` per worker branch.
- Ask each worker to return exact `git add`, `git commit`, and `git push` commands instead of committing from the integrator window.
- Merge worker branches back through the `main` integrator window after verification.
