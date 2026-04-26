## 1. Implement the SQL Debug Logger

- [x] 1.1 Create `sql_debug_logger.py` next to `main.py`.
- [x] 1.2 Define class `TerminalSqlAuditLogger` that subclasses `vanna.core.audit.AuditLogger`.
- [x] 1.3 Implement `async def log_event(event)` to dispatch on `isinstance(event, ToolInvocationEvent)` (imported from `vanna.core.audit.models`).
- [x] 1.4 Inside the dispatch, return early when `event.tool_name != "run_sql"`.
- [x] 1.5 Read the SQL from `event.parameters.get("sql", "")`; collapse newlines/tabs to single spaces before printing.
- [x] 1.6 Print the line in the format `[SQL] conversation=<conversation_id> request=<request_id> :: <sql>` to stdout.
- [x] 1.7 Wrap the print in a try/except that swallows any exception so logger failure cannot break the agent loop.

## 2. Wire the Logger into the Agent

- [x] 2.1 In `main.py`, import `TerminalSqlAuditLogger` from the new module.
- [x] 2.2 Pass `audit_logger=TerminalSqlAuditLogger()` as a keyword argument to the `Agent(...)` constructor.
- [x] 2.3 Confirm no other constructor arguments need to change; `AgentConfig()` defaults already enable tool-invocation auditing.

## 3. Manual Verification

- [x] 3.1 Run `uv run python main.py`; confirm the server starts without import or wiring errors.
- [x] 3.2 Open the Vanna UI and ask a question that should yield a SELECT (e.g., "top 5 artists by track count"); confirm exactly one `[SQL] ...` line appears in the terminal containing the SELECT statement.
- [x] 3.3 Ask a question that triggers a follow-up `visualize_data` call; confirm no extra `[SQL]` line is emitted for the visualize step.
- [x] 3.4 Ask a question that yields multiple `run_sql` invocations in one turn (or simulate it); confirm one printed line per invocation, in order.
- [x] 3.5 Confirm `conversation_id` and `request_id` in the printed lines change between separate user turns.
