import re

from vanna.core.audit import AuditLogger
from vanna.core.audit.models import AuditEvent, ToolInvocationEvent


_WHITESPACE = re.compile(r"\s+")


class TerminalSqlAuditLogger(AuditLogger):
    async def log_event(self, event: AuditEvent) -> None:
        if not isinstance(event, ToolInvocationEvent):
            return
        if event.tool_name != "run_sql":
            return

        sql = event.parameters.get("sql", "")
        sql_one_line = _WHITESPACE.sub(" ", sql).strip()

        try:
            print(
                f"[SQL] conversation={event.conversation_id} "
                f"request={event.request_id} :: {sql_one_line}",
                flush=True,
            )
        except Exception:
            pass
