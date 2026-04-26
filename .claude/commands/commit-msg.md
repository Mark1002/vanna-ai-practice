---
description: Suggest a short Conventional Commit message (one sentence, under 20 words) based on current uncommitted changes (reference only — does not commit)
---

Look at the current uncommitted changes in this repo and propose a short commit message I can use as a reference. Do NOT run `git commit` — this is for me to read and decide.

Steps:
1. Run `git status` (no `-uall`) to see staged, unstaged, and untracked files.
2. Run `git diff` and `git diff --staged` to see actual content changes.
3. Run `git log --oneline -10` so the suggestion matches this repo's commit style.
4. Write a single commit message:
   - **One sentence, under 20 words total.** No body, no line break.
   - **Must start with a Conventional Commit prefix**, choosing the most appropriate one:
     - `feat:` — new user-facing feature
     - `fix:` — bug fix
     - `chore:` — tooling, deps, config, build, non-functional housekeeping
     - `docs:` — documentation only
     - `refactor:` — code change that neither fixes a bug nor adds a feature
     - `test:` — adding or fixing tests
     - `perf:` — performance improvement
     - `style:` — formatting only, no logic change
     - `ci:` — CI/CD config
   - Add a scope in parentheses when it clarifies the area touched, e.g. `feat(agent):`, `fix(sql-runner):`, `chore(claude):`.
   - Imperative mood after the prefix ("add X", "fix Y"). Lowercase after the colon.

Output format:

- A single fenced code block containing the suggested commit message.
- One short line below the block noting which files the message covers, and flagging any untracked or unrelated files that look like they should be excluded.
- If changes clearly belong in separate commits, output 2–3 short messages (each still one sentence, under 20 words, with a prefix) instead of one.

Keep the whole response tight — this is a reference, not a writeup.
