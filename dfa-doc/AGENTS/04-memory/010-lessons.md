# Lessons

## Memory Layer Contract

- Treat each lesson as a reusable operating rule tied to concrete failures or regressions.
- Write lessons in imperative form so agents can execute them directly in later sessions.
- When a lesson is outdated, append a superseding note with date and trigger instead of deleting context.

## Durable Lessons

- Read the entry and architecture docs before large structural edits.
- Refresh generated agent docs after meaningful repository-shape changes.
- Prefer explicit contracts and stable names over agent improvisation.
- Keep manifests, README examples, and generator behavior aligned so the skill does not overpromise.
- Mixed repository signals are a warning to inspect before refactoring across boundaries.

## Lessons Log (Append-Only)

- Append human-validated milestones, lessons, and terminology decisions with dates.
- Keep history append-only: add corrections instead of rewriting old entries.
- Refresh-safe rule: this section is preserved during refresh; use manual blocks only for stricter sub-block protection.
