## Context

The Vanna agent in this project translates user questions into SQL via Anthropic's LLM and executes the SQL against `Chinook.sqlite` through the `RunSqlTool`. During local development we want immediate, terminal-visible feedback on what SQL the model produced for each question.

Vanna exposes four extensibility points where the SQL string is reachable:

- `LlmMiddleware.after_llm_response` — pre-execution; sees rejected/errored SQL.
- `AuditLogger.log_tool_invocation` (via `log_event`) — purpose-built; receives `ToolInvocationEvent` with `parameters["sql"]`.
- Subclassing `RunSqlTool` — couples logging to execution; heavier surface.
- `LifecycleHook.before_tool` — does NOT receive arguments; not viable for SQL access.

The audit logger is the canonical seam Vanna ships for "observe tool calls," and `AgentConfig.audit_config` is enabled by default with `log_tool_invocations=True`.

## Goals / Non-Goals

**Goals:**
- Print the generated SQL string to stdout each time the `run_sql` tool is invoked.
- Include enough metadata (request id, conversation id) to correlate a printed SQL line with a specific user turn.
- Add no new dependencies and require no fork of the Vanna package.
- Keep the logger trivially removable — wiring is one constructor argument.

**Non-Goals:**
- Persisting SQL to a file, database, or external sink.
- Logging non-`run_sql` tools (visualize, memory) — those add noise without aiding SQL debugging.
- Pretty-printing or formatting SQL (e.g., `sqlparse`).
- Pairing each SQL line with the original user question text — this requires holding extra state and is out of scope for a debug print.
- Production-grade redaction or compliance handling.

## Decisions

### D1: Use `AuditLogger`, not `LlmMiddleware`

`AuditLogger` is the typed, schema-stable seam Vanna ships for tool-call observation. `ToolInvocationEvent` exposes `tool_name` and `parameters` directly, so filtering by `tool_name == "run_sql"` and reading `parameters["sql"]` is straightforward.

**Alternative considered:** `LlmMiddleware.after_llm_response` would also see SQL the LLM proposed but the tool later rejected. Rejected here: the user wants debug visibility for executed queries, and the middleware path requires walking `LlmResponse.tool_calls` and re-checking tool names — more code for behavior we don't need.

### D2: Override `log_event` only

`AuditLogger` is an `ABC` whose only abstract method is `log_event`. The convenience methods (`log_tool_invocation`, `log_tool_result`, etc.) are concrete and route into `log_event` with typed event objects. Overriding just `log_event` and dispatching on `isinstance(event, ToolInvocationEvent)` keeps the logger compact.

### D3: Filter on `tool_name == "run_sql"`

Without a filter, every tool call (`visualize_data`, `save_question_tool_args`, `search_saved_correct_tool_uses`) would print, drowning the SQL we care about. The `run_sql` name is set in `RunSqlTool.name` and is stable; the user has not configured `custom_tool_name`, so a literal `"run_sql"` check is correct for this codebase.

### D4: Keep sanitization defaults

`AuditConfig.sanitize_tool_parameters` defaults to `True`, but the redaction list (`password`, `secret`, `token`, `api_key`, `auth`, `credential`, `private_key`, `access_key`) does not match the field name `sql`. The SQL string passes through unredacted. No config change required.

### D5: Logger lives in its own module

A new module `sql_debug_logger.py` (alongside `main.py`) holds the class. `main.py` imports it and passes an instance to `Agent(audit_logger=...)`. This keeps the wiring change in `main.py` to a single import + single keyword argument.

### D6: Output format

A single line per invocation:

```
[SQL] conversation=<id> request=<id> :: <sql>
```

Single-line, prefix-tagged so it greps cleanly. No multi-line pretty-print — the user can pipe to `sqlparse` if desired.

## Risks / Trade-offs

- **[Multi-line SQL]** → Multi-line SQL strings will break the single-line shape. Mitigation: collapse newlines to spaces before printing; raw SQL is preserved in the audit event for any future use.
- **[Stdout pollution under uvicorn]** → `VannaFastAPIServer.run()` likely uses uvicorn, which already writes access logs to stdout. Mitigation: distinctive `[SQL]` prefix makes lines easy to filter or grep.
- **[Tool name renamed]** → If someone passes `custom_tool_name` to `RunSqlTool`, the filter misses. Mitigation: document the assumption in the module; if it becomes a real risk later, switch to checking `parameters` for an `sql` key.
- **[Sensitive literals leak]** → User questions may include values that show up in SQL `WHERE` clauses. Acceptable for local debug; not a production logger.
