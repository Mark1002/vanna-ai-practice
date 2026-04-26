# sql-debug-logging Specification

## Purpose
TBD - created by archiving change add-sql-debug-logger. Update Purpose after archive.
## Requirements
### Requirement: SQL Debug Logger Prints Generated SQL to Terminal

The system SHALL print to stdout the SQL string from each `run_sql` tool invocation that the agent processes, so a developer can observe the natural-language → SQL translation in real time during local development.

#### Scenario: User question generates a SELECT statement

- **WHEN** a user submits a natural-language question that the LLM translates into a `run_sql` tool call
- **THEN** the SQL string from the tool call's `sql` argument SHALL be printed to stdout exactly once
- **AND** the printed line SHALL be prefixed with the literal token `[SQL]`

#### Scenario: User question triggers multiple SQL invocations in one turn

- **WHEN** the LLM emits more than one `run_sql` tool call within a single user turn
- **THEN** each `run_sql` invocation SHALL produce its own printed line in invocation order

### Requirement: Logger Filters to `run_sql` Only

The logger SHALL only print events whose `tool_name` equals `"run_sql"`. Invocations of other tools (e.g., `visualize_data`, agent memory tools) SHALL NOT produce terminal output from this logger.

#### Scenario: Visualize tool is invoked

- **WHEN** the agent invokes a non-`run_sql` tool such as `visualize_data`
- **THEN** the logger SHALL NOT print any line for that invocation

### Requirement: Logger Includes Correlation Identifiers

Each printed line SHALL include the `conversation_id` and `request_id` from the audit event, so concurrent or sequential turns can be disambiguated when reading the terminal.

#### Scenario: Two concurrent conversations issue SQL

- **WHEN** two conversations each trigger a `run_sql` invocation in overlapping time
- **THEN** the two printed lines SHALL each carry their own distinct `conversation_id` and `request_id` values

### Requirement: Logger Wired into Agent via `audit_logger` Parameter

The logger SHALL be installed by passing an instance to the `audit_logger` keyword argument of the `Agent` constructor. The system SHALL NOT require any other configuration change to enable the logger.

#### Scenario: Application starts with the logger wired in

- **WHEN** `main.py` constructs the `Agent` with an instance of the SQL debug logger as `audit_logger`
- **THEN** the agent SHALL invoke the logger's `log_event` method for every tool invocation, with no further configuration

### Requirement: Logger Does Not Mutate or Suppress Tool Behavior

The logger's only side effect SHALL be printing to stdout. It SHALL NOT alter `ToolInvocationEvent` contents, SHALL NOT raise exceptions that propagate into the agent loop, and SHALL NOT prevent the underlying `run_sql` tool from executing.

#### Scenario: SQL execution proceeds after logging

- **WHEN** a `run_sql` tool invocation is logged
- **THEN** the SQL SHALL still be executed by `RunSqlTool.execute` against `Chinook.sqlite` exactly as it would without the logger

