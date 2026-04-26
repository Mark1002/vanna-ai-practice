# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

This project uses `uv` for dependency management.

```bash
# Install dependencies
uv sync

# Run the server
uv run python main.py

# Add a dependency
uv add <package>
```

## Architecture

This is a [Vanna AI](https://vanna.ai/) practice project that exposes a natural-language-to-SQL agent via a FastAPI server, backed by the Chinook SQLite sample database.

**Entry point:** `main.py`

The application wires together these Vanna abstractions:

- **`AnthropicLlmService`** — LLM backend using `claude-opus-4-6`
- **`ToolRegistry`** — registers tools with per-group access control (`admin`, `user`)
  - `RunSqlTool` — executes SQL against `Chinook.sqlite` via `SqliteRunner`
  - `VisualizeDataTool` — renders query results as charts
  - `SaveQuestionToolArgsTool` / `SearchSavedCorrectToolUsesTool` — agent memory tools for learning from corrections
- **`DemoAgentMemory`** — in-process memory store (max 1000 items) for saving correct tool usage examples
- **`SimpleUserResolver`** — reads a `vanna_email` cookie to resolve `User` objects with group memberships; defaults to `admin@example.com`
- **`Agent`** — the core Vanna agent combining LLM, tools, user resolver, and memory
- **`VannaFastAPIServer`** — wraps the agent in a FastAPI app and calls `.run()`

**Database:** `Chinook.sqlite` — a sample music store database included in the repo root.

## GitHub Actions

Two Claude Code workflows are configured:

- **`claude.yml`** — triggered when `@claude` is mentioned in issues, PR comments, or PR reviews; runs Claude Code to handle the request
- **`claude-code-review.yml`** — runs automatically on PRs to perform a code review using the `code-review` Claude Code plugin

Both require `CLAUDE_CODE_OAUTH_TOKEN` to be set as a repository secret.
