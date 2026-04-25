# vanna-ai-practice

A natural-language-to-SQL agent built with [Vanna AI](https://vanna.ai/), exposed via a FastAPI server and backed by the Chinook SQLite sample database.

## Overview

This project wires together Vanna abstractions to let users query a music store database in plain English. The agent translates questions into SQL, executes them, and can visualize results as charts.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) for dependency management
- An Anthropic API key

## Setup

```bash
# Install dependencies
uv sync

# Set your Anthropic API key
export ANTHROPIC_API_KEY=your_key_here
```

## Running

```bash
uv run python main.py
```

The FastAPI server starts and listens for requests. By default, users are resolved from a `vanna_email` cookie; if absent, the request is treated as `admin@example.com`.

## Architecture

| Component | Role |
|-----------|------|
| `AnthropicLlmService` | LLM backend using `claude-opus-4-6` |
| `ToolRegistry` | Registers tools with per-group access control (`admin`, `user`) |
| `RunSqlTool` | Executes SQL against `Chinook.sqlite` via `SqliteRunner` |
| `VisualizeDataTool` | Renders query results as charts |
| `SaveQuestionToolArgsTool` | Saves correct tool-use examples to agent memory (admin only) |
| `SearchSavedCorrectToolUsesTool` | Retrieves saved examples to improve future queries |
| `DemoAgentMemory` | In-process memory store (max 1,000 items) |
| `SimpleUserResolver` | Reads `vanna_email` cookie to resolve users and group memberships |
| `VannaFastAPIServer` | Wraps the agent in a FastAPI app |

## Database

`Chinook.sqlite` is a sample music store database included in the repo. It contains tables for artists, albums, tracks, invoices, customers, and more.

## Access Control

Two user groups are supported:

- **`admin`** — full access to all tools including saving memory corrections
- **`user`** — can run SQL and search saved examples, but cannot save new corrections

## GitHub Actions

Two Claude Code workflows are configured:

- **`claude.yml`** — triggered when `@claude` is mentioned in issues, PR comments, or PR reviews
- **`claude-code-review.yml`** — runs automatically on PRs to perform a code review

Both require `CLAUDE_CODE_OAUTH_TOKEN` to be set as a repository secret.
