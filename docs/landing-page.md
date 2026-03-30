# Landing Page Prototype

Language: English | [简体中文](landing-page.zh.md)

This repository now includes a React landing page prototype for the public-facing product surface.

## Location

- `landing/`

## Goal

The landing page is aimed at CLI coding-agent users and explains the short product path:

1. install
2. init
3. refresh

Two-step entry model: global install exposes the skill to your coding agent, and repo-local init enables workflow in each repository.
For temporary Node onboarding, `npx -y doc-for-agent init ...` can combine both steps.
It also frames `doc-for-agent` as a project documentation system tool rather than a one-shot markdown generator.
The docs output model is `agent`, `human`, `dual`, or `quad` according to user intent.
Mode map: `agent` for `AGENTS/`, `human` for `docs/`, `dual` for both, and `quad` for `AGENTS/`, `AGENTS.zh/`, `docs/`, and `docs.zh/`.
Dual mode keeps `docs/` (human docs) and `AGENTS/` (agent docs) paired in one refresh flow. Quad mode establishes the bilingual four-view layout.
The product message is dual-system, not AGENTS-only.

## Entry Path

From repository entry docs, use this order:

1. `README.md`
2. `docs/landing-page.md`
3. `docs/quickstart.md`
4. `docs/platforms.md`

If you prefer Chinese docs, use the `.zh.md` counterparts in the same order.

## Local Preview

```bash
cd landing
npm install
npm run dev
```

## See Also

After this note, go to `Quickstart`, then `Platform Guide`.
This keeps the dual-doc message and command path aligned end to end.

- [Quickstart](quickstart.md)
- [Platform Guide](platforms.md)
